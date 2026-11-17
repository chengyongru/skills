"""Own one checker process tree until the CLI closes its control pipe.

Windows uses a kill-on-close Job Object, assigned before the gated child can run.
POSIX uses a new session whose gate kills its own group if the owner disappears.
Only the two CLI-created scratch directories are removed; published output stays.
"""
from __future__ import annotations

import ctypes
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import threading
import time


class WindowsJob:
    def __init__(self) -> None:
        from ctypes import wintypes as w

        class Limits(ctypes.Structure):
            _fields_ = [('process_time', ctypes.c_longlong), ('job_time', ctypes.c_longlong),
                        ('flags', w.DWORD), ('min_ws', ctypes.c_size_t), ('max_ws', ctypes.c_size_t),
                        ('active_limit', w.DWORD), ('affinity', ctypes.c_size_t),
                        ('priority', w.DWORD), ('scheduling', w.DWORD)]

        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in
                        ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]

        class Extended(ctypes.Structure):
            _fields_ = [('basic', Limits), ('io', IO), ('process_memory', ctypes.c_size_t),
                        ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t),
                        ('peak_job', ctypes.c_size_t)]

        class Accounting(ctypes.Structure):
            _fields_ = [(name, ctypes.c_longlong) for name in
                        ('user', 'kernel', 'period_user', 'period_kernel')] + [
                        (name, w.DWORD) for name in ('faults', 'total', 'active', 'terminated')]

        self.accounting = Accounting
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateJobObjectW': ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            'SetInformationJobObject': ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            'AssignProcessToJobObject': ([w.HANDLE, w.HANDLE], w.BOOL),
            'TerminateJobObject': ([w.HANDLE, w.UINT], w.BOOL),
            'QueryInformationJobObject': ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL),
            'CloseHandle': ([w.HANDLE], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(self.api, name)
            fn.argtypes, fn.restype = args, result
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        info = Extended()
        info.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process: subprocess.Popen) -> None:
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def stop(self) -> None:
        if not self.api.TerminateJobObject(self.handle, 2):
            raise ctypes.WinError(ctypes.get_last_error())
        deadline = time.monotonic() + 5
        while True:
            info = self.accounting()
            if not self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(info), ctypes.sizeof(info), None):
                raise ctypes.WinError(ctypes.get_last_error())
            if info.active == 0:
                return
            if time.monotonic() >= deadline:
                raise RuntimeError('Checker job still has active processes after termination')
            time.sleep(0.01)

    def close(self) -> None:
        if self.handle:
            if not self.api.CloseHandle(self.handle):
                raise ctypes.WinError(ctypes.get_last_error())
            self.handle = None


def stop_group() -> None:
    os.killpg(os.getpgrp(), signal.SIGKILL)


def gate(command: list[str]) -> int:
    if sys.stdin.buffer.readline() != b'go\n':
        return 2
    if os.name != 'nt':
        def orphaned() -> None:
            sys.stdin.buffer.read()
            stop_group()
        threading.Thread(target=orphaned, daemon=True).start()
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    code = child.wait()
    if code < 0:
        print(f'{signal.Signals(-code).name} killed the check, so the command wrote nothing.', file=sys.stderr)
    return code if code >= 0 else 2


def supervise(stage: Path, temporary: Path, command: list[str]) -> int:
    disconnected = threading.Event()
    def watch_parent() -> None:
        sys.stdin.buffer.read()
        disconnected.set()
    threading.Thread(target=watch_parent, daemon=True).start()
    job = WindowsJob() if os.name == 'nt' else None
    child = None
    try:
        child = subprocess.Popen([sys.executable, '-B', __file__, '--gate', *command],
                                 stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                 start_new_session=os.name != 'nt',
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        if job:
            job.assign(child)
        child.stdin.write(b'go\n')
        child.stdin.flush()
        while child.poll() is None and not disconnected.wait(0.05):
            pass
        status = child.poll()
        if job:
            job.stop()
        else:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        child.wait(timeout=5)
        if not disconnected.is_set():
            print(json.dumps({'exit': status if status in (0, 1) else 2}), flush=True)
            disconnected.wait()
        return 0
    finally:
        try:
            if job:
                job.stop()
            elif child is not None:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if child is not None:
                if child.poll() is None:
                    child.kill()
                child.wait(timeout=5)
                child.stdin.close()
        finally:
            if job:
                job.close()
            for directory in (stage, temporary):
                shutil.rmtree(directory)


if __name__ == '__main__':
    try:
        if sys.argv[1] == '--gate':
            sys.exit(gate(sys.argv[2:]))
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        sys.exit(supervise(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]))
    except Exception as error:
        print(f'Checker process owner failed: {error}', file=sys.stderr)
        sys.exit(2)
