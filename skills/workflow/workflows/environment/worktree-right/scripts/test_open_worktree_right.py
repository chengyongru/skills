"""Exercise pane selection and shell safety without touching a live Herdr session."""

import importlib.util
import os
from pathlib import Path
import shlex
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "worktree_right", Path(__file__).with_name("open-worktree-right.py"),
)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class OpenWorktreeTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"HERDR_ENV": "1", "HERDR_PANE_ID": "w1:p1"})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.root = os.path.abspath("/tmp/work tree's $(touch nope)")
        self.cwd = os.path.abspath("/tmp/other")
        self.neighbor = "w1:p2"
        self.busy = False
        self.prompt = "user@host % "
        self.calls = []

    def fake_herdr(self, *args, text=False):
        self.calls.append(args)
        operation = args[1]
        caller = {"pane_id": "w1:p1", "tab_id": "w1:t1"}
        target = {"pane_id": "w1:p2", "tab_id": "w1:t1", "cwd": self.cwd}
        if operation == "current":
            requested = args[3] if args[2] == "--pane" else os.environ["HERDR_PANE_ID"]
            if requested != caller["pane_id"]:
                raise RuntimeError('herdr failed: {"error":{"code":"pane_not_found"}}')
            return {"pane": caller}
        if operation == "neighbor":
            return {"neighbor": {
                "pane_id": caller["pane_id"], "neighbor_pane_id": self.neighbor,
                "layout": {"tab_id": caller["tab_id"], "panes": [caller, target]},
            }}
        if operation == "get":
            return {"pane": target}
        if operation == "process-info":
            return {"process_info": {
                "pane_id": "w1:p2", "shell_pid": 10,
                "foreground_processes": [{"pid": 20 if self.busy else 10, "name": "zsh"}],
            }}
        if operation == "read":
            return self.prompt
        if operation == "run":
            self.assertEqual(shlex.split(args[3]), ["cd", "--", self.root])
            self.cwd = self.root
            return ""
        if operation == "split":
            self.assertIn("--no-focus", args)
            self.assertEqual(args[args.index("--cwd") + 1], self.root)
            self.cwd = self.root
            return {"pane": target}
        self.fail(f"Unexpected Herdr call: {args}")

    def execute(self, dry_run=False, caller_pane_id=None):
        with patch.object(helper, "run_command", return_value=self.root + "\n"), \
                patch.object(helper, "herdr", side_effect=self.fake_herdr):
            return helper.open_worktree(self.root, dry_run, caller_pane_id)

    def test_reuses_right_shell_with_quoted_path(self):
        self.assertEqual(self.execute()["status"], "reused")
        self.assertEqual(self.cwd, self.root)

    def test_creates_right_pane_preserving_focus(self):
        self.neighbor = None
        self.assertEqual(self.execute()["status"], "created")

    def test_matching_directory_needs_no_input(self):
        self.cwd = self.root
        self.busy = True
        self.assertEqual(self.execute()["status"], "reused")
        self.assertFalse(any(call[1] in {"run", "split", "process-info"} for call in self.calls))

    def test_busy_pane_is_untouched(self):
        self.busy = True
        with self.assertRaisesRegex(RuntimeError, "occupied"):
            self.execute()
        self.assertFalse(any(call[1] in {"run", "split"} for call in self.calls))

    def test_unfinished_prompt_is_untouched(self):
        self.prompt = "user@host % pending command"
        with self.assertRaisesRegex(RuntimeError, "empty prompt"):
            self.execute()

    def test_dry_run_does_not_mutate(self):
        for neighbor in (None, "w1:p2"):
            with self.subTest(neighbor=neighbor):
                self.neighbor = neighbor
                self.assertEqual(self.execute(True)["status"], "dry-run")
        self.assertFalse(any(call[1] in {"run", "split"} for call in self.calls))

    def test_missing_caller_stops_before_commands(self):
        with patch.dict(os.environ, {"HERDR_PANE_ID": ""}), \
                patch.object(helper, "run_command") as command:
            with self.assertRaisesRegex(RuntimeError, "inherited HERDR_PANE_ID"):
                helper.open_worktree(self.root)
            command.assert_not_called()

    def test_stale_caller_reports_recovery_before_neighbor_lookup(self):
        with patch.dict(os.environ, {"HERDR_PANE_ID": "w1:p99"}):
            with self.assertRaisesRegex(RuntimeError, "--caller-pane-id <verified-id>"):
                self.execute()
        self.assertEqual(self.calls, [("pane", "current", "--current")])

    def test_verified_caller_creates_neighbor_with_stale_or_missing_environment(self):
        self.neighbor = None
        for inherited_id in ("w1:p99", ""):
            with self.subTest(inherited_id=inherited_id), \
                    patch.dict(os.environ, {"HERDR_PANE_ID": inherited_id}):
                self.calls.clear()
                result = self.execute(caller_pane_id="w1:p1")
                self.assertEqual(result["status"], "created")
                self.assertEqual(result["caller_pane_id"], "w1:p1")
                self.assertEqual(self.calls[0], ("pane", "current", "--pane", "w1:p1"))
                split = next(call for call in self.calls if call[1] == "split")
                self.assertEqual(split[split.index("--pane") + 1], "w1:p1")
                self.assertEqual(os.environ["HERDR_PANE_ID"], inherited_id)

    def test_explicit_caller_still_requires_herdr_environment(self):
        with patch.dict(os.environ, {"HERDR_ENV": ""}), \
                patch.object(helper, "run_command") as command:
            with self.assertRaisesRegex(RuntimeError, "HERDR_ENV=1"):
                helper.open_worktree(self.root, caller_pane_id="w1:p1")
            command.assert_not_called()

    def test_invalid_neighbor_is_rejected(self):
        self.neighbor = "w1:p1"
        with self.assertRaisesRegex(RuntimeError, "invalid right-hand neighbor"):
            self.execute()

    def test_control_character_path_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "control characters"):
            helper.directory_command("zsh", "/tmp/bad\ncommand")


if __name__ == "__main__":
    unittest.main()
