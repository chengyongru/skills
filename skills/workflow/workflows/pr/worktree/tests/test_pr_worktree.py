"""Exercise worktree naming and reuse against isolated local Git repositories."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pr_worktree.py"
spec = importlib.util.spec_from_file_location("pr_worktree", SCRIPT)
assert spec is not None and spec.loader is not None
worktrees = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worktrees)


class WorktreeNamingTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="pr-worktree-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo"
        self.root.mkdir()
        self.remote = self.root.parent / "remote.git"
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Worktree test")
        self.git("config", "user.email", "worktree@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        (self.root / ".gitignore").write_text(".worktrees\n", encoding="utf-8")
        (self.root / "tracked.txt").write_text("base\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "Fixture")
        self.git("init", "--bare", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "origin", "main")

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True,
            text=True, encoding="utf-8",
        ).stdout.strip()

    def start(self, branch: str, *extra: str, cwd: Path | None = None) -> dict:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "start", branch, "--repo", "fixture/repo",
             "--remote", "origin", "--format", "json", *extra],
            cwd=cwd or self.root, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_topic_names_preserve_branch_and_use_plain_branch_directory(self) -> None:
        for branch in ("feat/usage-chart", "fix/login-timeout"):
            with self.subTest(branch=branch):
                result = self.start(branch)
                path = self.root / ".worktrees" / branch.replace("/", "-")
                self.assertEqual(result["worktreeAction"], "created")
                self.assertEqual(Path(result["worktree"]["path"]), path)
                self.assertEqual(result["worktree"]["branch"], branch)
                self.assertFalse(result["worktree"]["detached"])
                reused = self.start(branch, cwd=path)
                self.assertEqual(reused["worktreeAction"], "reused")
                self.assertEqual(reused["worktree"]["path"], str(path))

    def test_sibling_directory_keeps_repository_and_branch_labels(self) -> None:
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        result = self.start("docs/quick-start")
        self.assertEqual(
            Path(result["worktree"]["path"]), self.root.parent / "repo-docs-quick-start",
        )

    def test_existing_worktrees_directory_is_used_even_when_not_ignored(self) -> None:
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        (self.root / ".worktrees").mkdir()
        result = self.start("refactor/parser")
        self.assertEqual(
            Path(result["worktree"]["path"]), self.root / ".worktrees" / "refactor-parser",
        )

    def test_registered_legacy_path_and_dirty_contents_are_preserved(self) -> None:
        branch = "codex/legacy-task"
        legacy = self.root / ".worktrees" / "pr-new-codex-legacy-task"
        self.git("worktree", "add", "-b", branch, str(legacy), "main")
        (legacy / "tracked.txt").write_text("in progress\n", encoding="utf-8")
        (legacy / "notes.txt").write_text("keep me\n", encoding="utf-8")
        before = self.git("worktree", "list", "--porcelain")
        result = self.start(branch)
        self.assertEqual(result["worktreeAction"], "reused")
        self.assertEqual(Path(result["worktree"]["path"]), legacy)
        self.assertEqual(self.git("worktree", "list", "--porcelain"), before)
        self.assertEqual((legacy / "tracked.txt").read_text(), "in progress\n")
        self.assertEqual((legacy / "notes.txt").read_text(), "keep me\n")
        self.assertFalse((self.root / ".worktrees" / "codex-legacy-task").exists())

    def test_explicit_path_and_branch_are_preserved(self) -> None:
        result = self.start("team/custom-topic", "--path", ".worktrees/custom-checkout")
        self.assertEqual(result["worktree"]["branch"], "team/custom-topic")
        self.assertEqual(
            Path(result["worktree"]["path"]), self.root / ".worktrees" / "custom-checkout",
        )

    def test_pr_directory_names_are_unchanged(self) -> None:
        self.assertEqual(
            worktrees.default_worktree_path(self.root, 42), self.root / ".worktrees" / "pr-42",
        )
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        self.assertEqual(
            worktrees.default_worktree_path(self.root, 42), self.root.parent / "repo-pr-42",
        )

    def test_help_uses_task_based_examples(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "start", "--help"],
            check=True, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertIn("feat/usage-chart", result.stdout)
        self.assertIn("fix/login-timeout", result.stdout)
        self.assertNotIn("codex/", result.stdout)


if __name__ == "__main__":
    unittest.main()
