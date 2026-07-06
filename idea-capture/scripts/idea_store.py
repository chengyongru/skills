#!/usr/bin/env python3
"""Mechanical helper for Markdown idea stores.

The skill should use this for deterministic filesystem operations and leave
meaning-making, prioritization, and language choices to the model.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CONFIG_NAME = "idea-store.json"
ORDERED_META_KEYS = [
    "id",
    "created",
    "status",
    "project",
    "kind",
    "source_id",
    "source_url",
    "title",
    "cost",
    "impact",
    "confidence",
    "related",
    "events",
]
UNQUOTED_KEYS = {
    "id",
    "created",
    "status",
    "project",
    "kind",
    "source_id",
    "cost",
    "impact",
    "confidence",
}
SECTION_ORDER = [
    "Why",
    "Current State",
    "Evidence",
    "Blocker",
    "Next",
    "为什么",
    "当前状态",
    "证据",
    "阻塞",
    "下一步",
]


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def config_path() -> Path:
    return codex_home() / CONFIG_NAME


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON config at {path}: {exc}")


def save_config(ideas_dir: Path) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"ideas_dir": str(ideas_dir)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_ideas_dir(args: argparse.Namespace, *, create: bool = False) -> Path:
    if getattr(args, "dir", None):
        ideas_dir = Path(args.dir).expanduser()
    elif getattr(args, "file", None):
        ideas_dir = Path(args.file).expanduser().resolve().parent
    else:
        configured = load_config().get("ideas_dir")
        if not configured:
            die("No idea directory configured. Provide --dir or save one with resolve --save.")
        ideas_dir = Path(configured).expanduser()

    ideas_dir = ideas_dir.resolve()
    if create:
        ideas_dir.mkdir(parents=True, exist_ok=True)
    if not ideas_dir.exists() or not ideas_dir.is_dir():
        die(f"Idea directory does not exist: {ideas_dir}")
    return ideas_dir


def yaml_unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def yaml_quote(value: Any) -> str:
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_frontmatter(raw: str) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    current_list: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if current_list and line.startswith("  - "):
            meta.setdefault(current_list, []).append(yaml_unquote(line[4:].strip()))
            continue
        current_list = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "[]":
            meta[key] = []
        elif value == "":
            meta[key] = []
            current_list = key
        else:
            meta[key] = yaml_unquote(value)
    return meta


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, text
    raw_meta = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).strip()
    return parse_frontmatter(raw_meta), body


def format_frontmatter(meta: dict[str, Any]) -> str:
    lines = ["---"]
    keys = [key for key in ORDERED_META_KEYS if key in meta]
    keys.extend(sorted(key for key in meta if key not in ORDERED_META_KEYS))
    for key in keys:
        value = meta[key]
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {yaml_quote(item)}")
        elif key in UNQUOTED_KEYS and value not in ("", None):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines)


def parse_sections(body: str) -> tuple[str | None, dict[str, str]]:
    title = None
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            current = None
        elif line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return title, {key: "\n".join(value).strip() for key, value in sections.items()}


def format_body(title: str, sections: dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    keys = [key for key in SECTION_ORDER if key in sections]
    keys.extend(key for key in sections if key not in keys)
    for index, key in enumerate(keys):
        if index:
            lines.append("")
        lines.append(f"## {key}")
        content = str(sections[key]).strip()
        if content:
            lines.append(content)
    return "\n".join(lines).strip()


def read_note(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    title, sections = parse_sections(body)
    return {
        "path": str(path),
        "filename": path.name,
        "stem": path.stem,
        "metadata": meta,
        "title": title or meta.get("title") or path.stem,
        "sections": sections,
        "body": body,
    }


def iter_notes(ideas_dir: Path) -> list[dict[str, Any]]:
    return [read_note(path) for path in sorted(ideas_dir.glob("*.md")) if path.is_file()]


def find_notes(
    ideas_dir: Path,
    *,
    note_id: str | None = None,
    source_id: str | None = None,
    path: str | None = None,
) -> list[dict[str, Any]]:
    if path:
        target = Path(path).expanduser()
        if not target.is_absolute():
            target = ideas_dir / target
        target = target.resolve()
        if target.exists() and target.suffix.lower() == ".md":
            return [read_note(target)]
        return []

    matches = []
    for note in iter_notes(ideas_dir):
        meta = note["metadata"]
        if note_id and meta.get("id") == note_id:
            matches.append(note)
        elif source_id and meta.get("source_id") == source_id:
            matches.append(note)
    return matches


def require_one(matches: list[dict[str, Any]], label: str) -> dict[str, Any]:
    if not matches:
        die(f"No idea matched {label}.")
    if len(matches) > 1:
        die(f"More than one idea matched {label}.")
    return matches[0]


def safe_filename(text: str) -> str:
    stem = text.strip()
    if stem.lower().endswith(".md"):
        stem = stem[:-3]
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", stem)
    stem = re.sub(r"\s+", "-", stem.strip())
    stem = re.sub(r"-{2,}", "-", stem).strip("-._ ")
    if not stem:
        die("Filename is empty after normalization.")
    return f"{stem}.md"


def normalize_related(value: Any) -> list[str]:
    if value in (None, "", []):
        return []
    items = value if isinstance(value, list) else [value]
    normalized = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if not text.startswith("[["):
            text = f"[[{text.removesuffix('.md')}]]"
        normalized.append(text)
    return normalized


def load_note_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.note_json:
        raw = Path(args.note_json).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        die(f"Invalid note JSON: {exc}")
    if not isinstance(payload, dict):
        die("Note JSON must be an object.")
    return payload


def cmd_resolve(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args, create=args.create)
    if args.save:
        save_config(ideas_dir)
    print(json.dumps({"ideas_dir": str(ideas_dir)}, ensure_ascii=False, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args)
    statuses = set(args.status or [])
    result = []
    for note in iter_notes(ideas_dir):
        meta = note["metadata"]
        if statuses and meta.get("status") not in statuses:
            continue
        if args.project and meta.get("project") != args.project:
            continue
        item = {
            "path": note["path"],
            "filename": note["filename"],
            "stem": note["stem"],
            "metadata": meta,
            "title": note["title"],
        }
        if args.include_body:
            item["sections"] = note["sections"]
            item["body"] = note["body"]
        result.append(item)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_find(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args)
    matches = find_notes(ideas_dir, note_id=args.id, source_id=args.source_id, path=args.path)
    if args.require_one:
        matches = [require_one(matches, args.id or args.source_id or args.path)]
    print(json.dumps(matches, ensure_ascii=False, indent=2))


def cmd_read(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args)
    note = require_one(find_notes(ideas_dir, note_id=args.id, source_id=args.source_id, path=args.path), args.id or args.source_id or args.path)
    print(json.dumps(note, ensure_ascii=False, indent=2))


def cmd_write(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args, create=True)
    payload = load_note_payload(args)
    meta = dict(payload.get("metadata") or {})
    sections = dict(payload.get("sections") or {})
    title = str(payload.get("title") or meta.get("title") or "").strip()
    filename = safe_filename(str(payload.get("filename") or title))

    for key in ["id", "created", "status", "project", "kind", "title", "cost", "impact", "confidence"]:
        if not meta.get(key):
            die(f"Missing required metadata field: {key}")
    if not title:
        title = str(meta["title"])
    meta["title"] = title
    meta["related"] = normalize_related(meta.get("related"))
    events = meta.get("events")
    if not isinstance(events, list) or not events:
        meta["events"] = [f"{date.today().isoformat()} captured"]

    existing = find_notes(ideas_dir, note_id=meta.get("id"), source_id=meta.get("source_id"))
    target = (ideas_dir / filename).resolve()
    if not str(target).startswith(str(ideas_dir)):
        die(f"Target escapes idea directory: {target}")

    action = "created"
    if existing:
        current = require_one(existing, meta.get("id") or meta.get("source_id"))
        current_path = Path(current["path"]).resolve()
        if target.exists() and target != current_path:
            die(f"Target filename already exists: {target}")
        if target != current_path:
            current_path.rename(target)
        action = "updated"
    elif target.exists():
        die(f"Target filename already exists: {target}")

    target.write_text(format_frontmatter(meta) + "\n\n" + format_body(title, sections) + "\n", encoding="utf-8")
    print(json.dumps({"action": action, "path": str(target), "id": meta.get("id")}, ensure_ascii=False, indent=2))


def cmd_mark(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args)
    note = require_one(find_notes(ideas_dir, note_id=args.id, source_id=args.source_id, path=args.path), args.id or args.source_id or args.path)
    path = Path(note["path"])
    meta = note["metadata"]
    meta["status"] = args.status
    events = meta.get("events")
    if not isinstance(events, list):
        events = []
    events.append(args.event or f"{date.today().isoformat()} {args.status}")
    meta["events"] = events
    title = str(meta.get("title") or note["title"])
    path.write_text(format_frontmatter(meta) + "\n\n" + format_body(title, note["sections"]) + "\n", encoding="utf-8")
    print(json.dumps({"action": "marked", "path": str(path), "status": args.status}, ensure_ascii=False, indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    ideas_dir = resolve_ideas_dir(args)
    note = require_one(find_notes(ideas_dir, note_id=args.id, source_id=args.source_id, path=args.path), args.id or args.source_id or args.path)
    path = Path(note["path"]).resolve()
    if path.parent != ideas_dir:
        die(f"Refusing to delete outside idea directory: {path}")
    path.unlink()
    print(json.dumps({"action": "deleted", "path": str(path)}, ensure_ascii=False, indent=2))


def cmd_slug(args: argparse.Namespace) -> None:
    print(json.dumps({"filename": safe_filename(args.text)}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    resolve = sub.add_parser("resolve")
    resolve.add_argument("--dir")
    resolve.add_argument("--file")
    resolve.add_argument("--create", action="store_true")
    resolve.add_argument("--save", action="store_true")
    resolve.set_defaults(func=cmd_resolve)

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--dir")
    list_cmd.add_argument("--status", action="append")
    list_cmd.add_argument("--project")
    list_cmd.add_argument("--include-body", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    find = sub.add_parser("find")
    find.add_argument("--dir")
    find.add_argument("--id")
    find.add_argument("--source-id")
    find.add_argument("--path")
    find.add_argument("--require-one", action="store_true")
    find.set_defaults(func=cmd_find)

    read = sub.add_parser("read")
    read.add_argument("--dir")
    read.add_argument("--id")
    read.add_argument("--source-id")
    read.add_argument("--path")
    read.set_defaults(func=cmd_read)

    write = sub.add_parser("write")
    write.add_argument("--dir")
    write.add_argument("--note-json")
    write.set_defaults(func=cmd_write)

    mark = sub.add_parser("mark")
    mark.add_argument("--dir")
    mark.add_argument("--id")
    mark.add_argument("--source-id")
    mark.add_argument("--path")
    mark.add_argument("--status", required=True, choices=["open", "doing", "done", "dropped", "duplicate"])
    mark.add_argument("--event")
    mark.set_defaults(func=cmd_mark)

    delete = sub.add_parser("delete")
    delete.add_argument("--dir")
    delete.add_argument("--id")
    delete.add_argument("--source-id")
    delete.add_argument("--path")
    delete.set_defaults(func=cmd_delete)

    slug = sub.add_parser("slug")
    slug.add_argument("text")
    slug.set_defaults(func=cmd_slug)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
