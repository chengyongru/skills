"""Drive the portable CLI and observe real checker/descendant lifetimes."""
from __future__ import annotations

import ctypes
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import venv

SCRIPTS = Path(__file__).resolve().parents[1]
NODE = shutil.which('node')


def wait_for(predicate, message: str, seconds: float = 10) -> None:
    deadline = time.monotonic() + seconds
    while not predicate():
        if time.monotonic() >= deadline:
            raise AssertionError(message)
        time.sleep(0.01)


class ProcessReceipt:
    def __init__(self, pid: int):
        self.pid = pid
        self.handle = None
        if os.name == 'nt':
            from ctypes import wintypes as w
            self.api = ctypes.WinDLL('kernel32', use_last_error=True)
            self.api.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
            self.api.OpenProcess.restype = w.HANDLE
            self.api.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
            self.api.WaitForSingleObject.restype = w.DWORD
            self.api.CloseHandle.argtypes = [w.HANDLE]
            self.handle = self.api.OpenProcess(0x100000, False, pid)
            if not self.handle:
                raise ctypes.WinError(ctypes.get_last_error())

    def stopped(self) -> bool:
        if self.handle:
            result = self.api.WaitForSingleObject(self.handle, 0)
            if result not in (0, 258):
                raise ctypes.WinError(ctypes.get_last_error())
            return result == 0
        try:
            os.kill(self.pid, 0)
        except ProcessLookupError:
            return True
        status = Path(f'/proc/{self.pid}/stat')
        if status.exists():
            return status.read_text().rsplit(')', 1)[1].split()[0] == 'Z'
        return False

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)


class PortableCliTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(NODE, 'Node is required; do not count a skipped CLI suite as a pass')
        temporary = tempfile.TemporaryDirectory(prefix='statechart-native-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.entry = SCRIPTS / 'statechart.ts'
        self.outputs = self.root / 'outputs'
        self.tmp = self.root / 'tmp'
        self.outputs.mkdir()
        self.tmp.mkdir()
        self.env = {**os.environ, 'STATECHART_PYTHON': sys.executable,
                    'TMPDIR': str(self.tmp), 'TMP': str(self.tmp), 'TEMP': str(self.tmp)}
        self.env.pop('JAVA_ARGS', None)
        self.spec = self.root / 'Check.tla'
        self.spec.write_text('---- MODULE Check ----\nVARIABLE x\nInit == x = 0\nNext == x\' = x\n====\n', encoding='utf-8')
        self.config = self.spec.with_suffix('.cfg')
        self.config.write_text('INIT Init\nNEXT Next\n', encoding='utf-8')

    def start(self, *args: str):
        return subprocess.Popen([NODE, '--disable-warning=ExperimentalWarning', str(self.entry),
                                 str(self.spec), '--out', str(self.outputs / 'out'), *args],
                                env=self.env, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding='utf-8',
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)

    def assert_clean(self):
        wait_for(lambda: not list(self.outputs.iterdir()) and not list(self.tmp.iterdir()),
                 'Owned staging/temp directories were not cleaned')

    def checker_tree(self):
        marker = self.root / 'ready.json'
        script = self.root / 'hold.mjs'
        script.write_text(
            'import fs from "node:fs"; import {spawn} from "node:child_process";\n'
            'const child = spawn(process.execPath, ["-e", "setInterval(()=>{}, 1000)"], '
            '{windowsHide:true, stdio:"ignore"});\n'
            f'fs.writeFileSync({json.dumps(str(marker))}, JSON.stringify({{pid:process.pid, descendant:child.pid}}));\n'
            'setInterval(()=>{}, 1000);\n', encoding='utf-8')
        self.env.update(JAVA=NODE, JAVA_ARGS=json.dumps([str(script)]), TLA2TOOLS='synthetic.jar')
        return marker

    def exercise_stop(self, action: str):
        marker = self.checker_tree()
        cancel = self.root / 'cancel'
        process = self.start('--timeout', '2' if action == 'timeout' else '30', '--cancel-file', str(cancel))
        receipts = []
        try:
            wait_for(lambda: marker.exists() and marker.stat().st_size > 0, 'Checker never reached readiness')
            pids = json.loads(marker.read_text())
            receipts = [ProcessReceipt(pid) for pid in pids.values()]
            self.assertTrue(all(not receipt.stopped() for receipt in receipts))
            if action == 'cancel':
                cancel.write_text('stop', encoding='utf-8')
            elif action == 'parent-exit':
                process.kill()
            stdout, stderr = process.communicate(timeout=15)
            if action != 'parent-exit':
                self.assertEqual(process.returncode, 124 if action == 'timeout' else 130, stderr)
                self.assertIn('stopped the check', stderr)
            self.assertEqual(stdout, '')
            for receipt in receipts:
                wait_for(receipt.stopped, f'Owned descendant {receipt.pid} survived {action}')
            self.assertEqual(stderr, '' if action == 'parent-exit' else f'{"timeout" if action == "timeout" else "cancelled"} stopped the check, so the command wrote nothing.\n')
            self.assert_clean()
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=10)
            for receipt in receipts:
                receipt.close()

    def test_timeout_stops_checker_and_descendant(self):
        self.exercise_stop('timeout')

    def test_file_cancellation_stops_checker_and_descendant(self):
        self.exercise_stop('cancel')

    def test_abrupt_cli_exit_stops_checker_and_descendant(self):
        self.exercise_stop('parent-exit')

    def test_venv_owner_keeps_descendants_owned_after_parent_exit(self):
        environment = self.root / 'venv'
        venv.EnvBuilder(with_pip=False).create(environment)
        executable = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        self.env['STATECHART_PYTHON'] = str(executable)
        self.exercise_stop('parent-exit')

    def test_exited_worker_with_live_pipe_holding_descendant_is_reaped(self):
        marker = self.root / 'descendant.json'
        release = self.root / 'release'
        view = self.root / 'view.mjs'
        view.write_text(
            'import fs from "node:fs"; import {spawn} from "node:child_process";\n'
            'const child = spawn(process.execPath, ["-e", "setInterval(()=>{}, 1000)"], '
            '{windowsHide:true, detached:process.platform==="win32", stdio:["ignore", "inherit", "inherit"]});\n'
            f'fs.writeFileSync({json.dumps(str(marker))}, JSON.stringify({{pid:child.pid}}));\n'
            f'setInterval(()=>{{if(fs.existsSync({json.dumps(str(release))})) process.exit(1);}},10);\n'
            'await new Promise(()=>{});\n', encoding='utf-8')
        process = self.start('--view', str(view), '--timeout', '30')
        receipt = None
        try:
            wait_for(lambda: marker.exists() and marker.stat().st_size > 0, 'View did not start its descendant')
            receipt = ProcessReceipt(json.loads(marker.read_text())['pid'])
            self.assertFalse(receipt.stopped())
            release.write_text('exit root', encoding='utf-8')
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 2, stderr)
            self.assertEqual(stdout, '')
            wait_for(receipt.stopped, 'Descendant survived its exited worker')
            self.assert_clean()
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=10)
            if receipt:
                receipt.close()

    def test_package_output_and_temp_paths_are_refused_without_writes(self):
        package = self.root / 'workflow-copy'
        shutil.copytree(SCRIPTS.parent, package, ignore=shutil.ignore_patterns('node_modules', '__pycache__'))
        self.entry = package / 'scripts/statechart.ts'
        before = {p.relative_to(package): p.read_bytes() for p in package.rglob('*') if p.is_file()}
        for target in ('output', 'temp'):
            with self.subTest(target=target):
                args = ['--out', str(package / 'generated')] if target == 'output' else []
                if target == 'temp':
                    self.env.update(TMPDIR=str(package), TMP=str(package), TEMP=str(package))
                process = self.start(*args)
                stdout, stderr = process.communicate(timeout=15)
                self.assertEqual(process.returncode, 2, stderr)
                self.assertIn('outside the immutable plugin package', stderr)
                self.assertEqual(stdout, '')
                self.assertEqual({p.relative_to(package): p.read_bytes() for p in package.rglob('*') if p.is_file()}, before)
                self.assertFalse((package / 'generated').exists())
                self.assert_clean()

    def test_missing_dependencies_fail_and_clean_scratch(self):
        original = self.env.copy()
        for tool, expected in [('TLA2TOOLS', 'Set TLA2TOOLS'), ('STATECHART_PYTHON', 'ENOENT')]:
            with self.subTest(tool=tool):
                self.env = original.copy()
                if tool == 'TLA2TOOLS':
                    self.env.pop(tool, None)
                else:
                    self.env[tool] = str(self.root / 'missing-python')
                process = self.start()
                stdout, stderr = process.communicate(timeout=15)
                self.assertEqual(process.returncode, 2, stderr)
                self.assertIn(expected, stderr)
                self.assertEqual(stdout, '')
                self.assert_clean()

    def test_invalid_budgets_do_not_start_the_checker(self):
        marker = self.checker_tree()
        for value in ('0', '-1', 'NaN', 'Infinity', '86401'):
            with self.subTest(timeout=value):
                process = self.start(f'--timeout={value}')
                stdout, stderr = process.communicate(timeout=15)
                self.assertEqual(process.returncode, 2, stderr)
                self.assertIn('--timeout must be positive', stderr)
                self.assertEqual(stdout, '')
                self.assertFalse(marker.exists())
                self.assert_clean()

    def test_real_tlc_invariant_deadlock_temporal_and_syntax_results(self):
        self.assertTrue(Path(self.env.get('TLA2TOOLS', '')).is_file(), 'Pinned TLC required for native proof')
        cases = [
            ('invariant', 'EXTENDS Naturals\nVARIABLE x\nInit == x = 0\nNext == x < 2 /\\ x\' = x + 1\nSafe == x < 2',
             'INIT Init\nNEXT Next\nINVARIANT Safe\nCHECK_DEADLOCK FALSE\n', 1, 'Safe breaks'),
            ('pass', 'EXTENDS Naturals\nVARIABLE x\nInit == x = 0\nNext == x < 1 /\\ x\' = x + 1\nSafe == x < 2',
             'INIT Init\nNEXT Next\nINVARIANT Safe\nCHECK_DEADLOCK FALSE\n', 0, 'Safe'),
            ('deadlock', 'VARIABLE x\nInit == x = 0\nNext == FALSE /\\ UNCHANGED x',
             'INIT Init\nNEXT Next\n', 1, 'NoDeadlock breaks'),
            ('temporal', 'VARIABLE x\nInit == x = 0\nNext == UNCHANGED x\nSpec == Init /\\ [][Next]_x\nProgress == <>(x = 1)',
             'SPECIFICATION Spec\nPROPERTY Progress\n', 1, 'Progress breaks'),
            ('syntax', 'VARIABLE x\nInit == x = 0\nNext == x\' = unknown',
             'INIT Init\nNEXT Next\n', 2, None),
        ]
        for name, model, config, code, expected in cases:
            with self.subTest(case=name):
                self.spec.write_text(f'---- MODULE Check ----\n{model}\n====\n', encoding='utf-8')
                self.config.write_text(config, encoding='utf-8')
                process = self.start('--out', str(self.outputs / name), '--timeout', '30')
                stdout, stderr = process.communicate(timeout=40)
                self.assertEqual(process.returncode, code, stderr)
                if expected:
                    self.assertIn(expected, stdout)
                    self.assertTrue((self.outputs / name / 'tlc.out').is_file())
                else:
                    self.assertIn('Unknown operator', stderr)
                    self.assertIn('line 4', stderr)
                    self.assertFalse((self.outputs / name).exists())
                self.assertEqual(list(self.tmp.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
