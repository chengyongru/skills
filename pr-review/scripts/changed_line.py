#!/usr/bin/env python3
"""Validate GitHub PR inline-comment anchors.

Given a PR, file, and actual file line or grep pattern, checks whether the line is
inside the PR diff and emits a REST review comment anchor skeleton.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

AnchorSets = dict[str, dict[str, set[int]]]


def run_gh(args: list[str]) -> str:
    env = dict(os.environ)
    env.setdefault("NO_COLOR", "1")
    proc = subprocess.run(
        ["gh", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    return proc.stdout


def clean_diff_path(raw: str) -> str | None:
    token = raw.strip().split("\t", 1)[0]
    if token == "/dev/null":
        return None
    if token.startswith('"') and token.endswith('"'):
        token = token[1:-1].encode("utf-8").decode("unicode_escape")
    if token.startswith("a/") or token.startswith("b/"):
        token = token[2:]
    return token


def parse_hunk_header(line: str) -> tuple[int, int]:
    match = re.search(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
    if not match:
        raise ValueError(f"cannot parse hunk header: {line}")
    return int(match.group(1)), int(match.group(2))


def parse_diff(diff_text: str) -> tuple[AnchorSets, dict[tuple[str, str, int], str]]:
    anchors: AnchorSets = defaultdict(lambda: {"RIGHT_changed": set(), "RIGHT_context": set(), "LEFT_changed": set(), "LEFT_context": set()})
    line_text: dict[tuple[str, str, int], str] = {}
    old_path: str | None = None
    new_path: str | None = None
    old_line: int | None = None
    new_line: int | None = None
    in_hunk = False

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("--- "):
            old_path = clean_diff_path(raw_line[4:])
            in_hunk = False
            continue
        if raw_line.startswith("+++ "):
            new_path = clean_diff_path(raw_line[4:])
            in_hunk = False
            continue
        if raw_line.startswith("@@ "):
            old_line, new_line = parse_hunk_header(raw_line)
            in_hunk = True
            continue
        if not in_hunk or old_line is None or new_line is None:
            continue
        if raw_line.startswith("\\"):
            continue

        prefix = raw_line[:1]
        text = raw_line[1:] if raw_line else ""
        if prefix == "+":
            if new_path is not None:
                anchors[new_path]["RIGHT_changed"].add(new_line)
                line_text[(new_path, "RIGHT", new_line)] = text
            new_line += 1
        elif prefix == "-":
            if old_path is not None:
                anchors[old_path]["LEFT_changed"].add(old_line)
                line_text[(old_path, "LEFT", old_line)] = text
            old_line += 1
        elif prefix == " ":
            if old_path is not None:
                anchors[old_path]["LEFT_context"].add(old_line)
                line_text[(old_path, "LEFT", old_line)] = text
            if new_path is not None:
                anchors[new_path]["RIGHT_context"].add(new_line)
                line_text[(new_path, "RIGHT", new_line)] = text
            old_line += 1
            new_line += 1

    return anchors, line_text


def read_worktree_lines(worktree: Path, file_path: str) -> list[str]:
    path = worktree / file_path
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        raise SystemExit(f"file not found in worktree: {path}")


def match_pattern(lines: list[str], pattern: str, regex: bool) -> list[tuple[int, str]]:
    matches = []
    compiled = re.compile(pattern) if regex else None
    for idx, text in enumerate(lines, start=1):
        ok = bool(compiled.search(text)) if compiled else pattern in text
        if ok:
            matches.append((idx, text))
    return matches


def choose_line(
    *,
    explicit_line: int | None,
    pattern: str | None,
    regex: bool,
    occurrence: int | None,
    side: str,
    file_path: str,
    worktree: Path,
    anchors: AnchorSets,
    line_text: dict[tuple[str, str, int], str],
    allow_context: bool,
) -> tuple[int, str | None, list[tuple[int, str]]]:
    if explicit_line is not None:
        text = None
        if side == "RIGHT":
            lines = read_worktree_lines(worktree, file_path)
            if 1 <= explicit_line <= len(lines):
                text = lines[explicit_line - 1]
        else:
            text = line_text.get((file_path, side, explicit_line))
        return explicit_line, text, []

    if not pattern:
        raise SystemExit("provide --line or --pattern")

    candidates = [
        (line, text)
        for (path, item_side, line), text in line_text.items()
        if path == file_path and item_side == side and (re.search(pattern, text) if regex else pattern in text)
    ]
    candidates.sort()

    if not candidates:
        raise SystemExit("pattern matched no lines")
    if occurrence is not None:
        if occurrence < 1 or occurrence > len(candidates):
            raise SystemExit(f"occurrence {occurrence} out of range; {len(candidates)} matches")
        line, text = candidates[occurrence - 1]
        return line, text, candidates

    changed_key = f"{side}_changed"
    context_key = f"{side}_context"
    changed = [(line, text) for line, text in candidates if line in anchors.get(file_path, {}).get(changed_key, set())]
    context = [(line, text) for line, text in candidates if line in anchors.get(file_path, {}).get(context_key, set())]

    if len(changed) == 1:
        line, text = changed[0]
        return line, text, candidates
    if allow_context and len(context) == 1:
        line, text = context[0]
        return line, text, candidates
    if len(candidates) == 1:
        line, text = candidates[0]
        return line, text, candidates

    preview = "\n".join(f"  {line}: {text[:160]}" for line, text in candidates[:20])
    raise SystemExit(
        "pattern is ambiguous; pass --occurrence or --line. Matches:\n" + preview
    )


def build_result(
    *,
    file_path: str,
    side: str,
    line: int,
    text: str | None,
    anchors: AnchorSets,
    allow_context: bool,
    all_candidates: list[tuple[int, str]],
) -> dict[str, Any]:
    file_anchors = anchors.get(file_path, {})
    changed = line in file_anchors.get(f"{side}_changed", set())
    context = line in file_anchors.get(f"{side}_context", set())
    ok = changed or (allow_context and context)
    if changed:
        reason = "line is changed in PR diff"
    elif context:
        reason = "line is only context in PR diff; rerun with --allow-context if intentional"
    else:
        reason = "line is not present on this side of the PR diff"

    return {
        "ok": ok,
        "path": file_path,
        "line": line,
        "side": side,
        "inChangedLines": changed,
        "inDiffContext": context,
        "reason": reason,
        "lineText": text,
        "anchor": {"path": file_path, "line": line, "side": side} if ok else None,
        "candidateCount": len(all_candidates),
        "candidates": [{"line": n, "text": t} for n, t in all_candidates[:20]],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Line anchor: {'OK' if result['ok'] else 'NOT OK'}",
        f"- Path: {result['path']}",
        f"- Line: {result['line']}",
        f"- Side: {result['side']}",
        f"- Changed line: {result['inChangedLines']}",
        f"- Diff context: {result['inDiffContext']}",
        f"- Reason: {result['reason']}",
    ]
    if result.get("lineText") is not None:
        lines.append(f"- Text: `{result['lineText']}`")
    if result.get("anchor"):
        lines.append("\n```json")
        lines.append(json.dumps(result["anchor"], ensure_ascii=False, indent=2))
        lines.append("```")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a GitHub PR inline-comment line anchor.")
    parser.add_argument("pr", help="PR number")
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--file", required=True, help="repository-relative file path")
    parser.add_argument("--side", choices=("RIGHT", "LEFT"), default="RIGHT")
    parser.add_argument("--line", type=int, help="actual file line number")
    parser.add_argument("--pattern", help="substring or regex to locate the line")
    parser.add_argument("--regex", action="store_true", help="treat --pattern as a regular expression")
    parser.add_argument("--occurrence", type=int, help="1-based match occurrence when --pattern is ambiguous")
    parser.add_argument("--allow-context", action="store_true", help="allow anchoring to unchanged context lines in the diff")
    parser.add_argument("--worktree", default=".", help="worktree root for RIGHT-side file reads")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    if args.line is None and args.pattern is None:
        raise SystemExit("provide --line or --pattern")
    if args.line is not None and args.pattern is not None:
        raise SystemExit("provide only one of --line or --pattern")

    diff_text = run_gh(["pr", "diff", args.pr, "--repo", args.repo])
    anchors, line_text = parse_diff(diff_text)
    line, text, candidates = choose_line(
        explicit_line=args.line,
        pattern=args.pattern,
        regex=args.regex,
        occurrence=args.occurrence,
        side=args.side,
        file_path=args.file,
        worktree=Path(args.worktree),
        anchors=anchors,
        line_text=line_text,
        allow_context=args.allow_context,
    )
    result = build_result(
        file_path=args.file,
        side=args.side,
        line=line,
        text=text,
        anchors=anchors,
        allow_context=args.allow_context,
        all_candidates=candidates,
    )

    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
