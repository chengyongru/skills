#!/usr/bin/env python3
"""Mechanical helper for Markdown material stores.

The skill should use this for deterministic filesystem operations and leave
meaning-making, prioritization, and language choices to the model.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit, urlunsplit

CONFIG_NAME = "material-store.json"
ORDERED_META_KEYS = [
    "id",
    "created",
    "topic",
    "kind",
    "verification",
    "maturity",
    "platforms",
    "source_url",
    "related",
    "events",
]
UNQUOTED_KEYS = {
    "id",
    "created",
    "kind",
    "verification",
    "maturity",
}
SECTION_ORDER = [
    "Core Facts",
    "Evidence",
    "Notes",
    "核心事实",
    "证据",
    "备注",
]
CJK_RUN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
SEARCH_TOKEN_RE = re.compile(r"[a-z0-9]+|[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+", re.IGNORECASE)
SEARCH_FIELD_WEIGHTS = {
    "id": 8,
    "source_url": 8,
    "filename": 6,
    "stem": 6,
    "title": 5,
    "metadata": 2,
    "path": 2,
    "body": 1,
}
SEARCH_EXACT_FIELDS = ("id", "source_url", "filename", "stem", "path")


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def config_dir() -> Path:
    """Resolve the XDG-style config directory for this skill.

    Priority:
      1. $MATERIAL_CONFIG_HOME (full directory override)
      2. $XDG_CONFIG_HOME/material
      3. ~/.config/material
    """
    override = os.environ.get("MATERIAL_CONFIG_HOME")
    if override:
        return Path(override).expanduser()
    base = os.environ.get("XDG_CONFIG_HOME")
    root = Path(base).expanduser() if base else Path.home() / ".config"
    return root / "material"


def config_path() -> Path:
    return config_dir() / CONFIG_NAME


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON config at {path}: {exc}")


def save_config(materials_dir: Path) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"materials_dir": str(materials_dir)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_materials_dir(args: argparse.Namespace, *, create: bool = False) -> Path:
    if getattr(args, "dir", None):
        materials_dir = Path(args.dir).expanduser()
    elif getattr(args, "file", None):
        materials_dir = Path(args.file).expanduser().resolve().parent
    else:
        configured = load_config().get("materials_dir")
        if not configured:
            die("No material directory configured. Provide --dir or save one with resolve --save.")
        materials_dir = Path(configured).expanduser()

    materials_dir = materials_dir.resolve()
    if create:
        materials_dir.mkdir(parents=True, exist_ok=True)
    if not materials_dir.exists() or not materials_dir.is_dir():
        die(f"Material directory does not exist: {materials_dir}")
    return materials_dir


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


def normalize_search_text(value: Any) -> str:
    text = unquote("" if value is None else str(value)).strip().replace("\\", "/")
    if not text:
        return ""

    parsed = urlsplit(text)
    if parsed.scheme and parsed.netloc:
        return urlunsplit(
            (
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path.rstrip("/"),
                parsed.query,
                "",
            )
        ).lower()

    return text.rstrip("/").lower()


def tokenize_search_text(value: Any) -> list[str]:
    text = normalize_search_text(value)
    tokens: list[str] = []
    for token in SEARCH_TOKEN_RE.findall(text):
        token = token.lower()
        if CJK_RUN_RE.fullmatch(token):
            tokens.extend(token)
            for width in (2, 3):
                tokens.extend(token[index : index + width] for index in range(len(token) - width + 1))
        else:
            tokens.append(token)
    return tokens


def metadata_search_text(meta: dict[str, Any]) -> str:
    parts: list[str] = []
    for key, value in sorted(meta.items()):
        if isinstance(value, list):
            parts.append(str(key))
            parts.extend(str(item) for item in value)
        else:
            parts.append(f"{key} {value}")
    return " ".join(parts)


def note_search_fields(note: dict[str, Any]) -> dict[str, str]:
    meta = note["metadata"]
    return {
        "id": str(meta.get("id") or ""),
        "source_url": str(meta.get("source_url") or ""),
        "filename": str(note["filename"]),
        "stem": str(note["stem"]),
        "path": str(note["path"]),
        "title": str(note["title"]),
        "metadata": metadata_search_text(meta),
        "body": str(note.get("body") or ""),
    }


def weighted_token_counts(note: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for field, text in note_search_fields(note).items():
        weight = SEARCH_FIELD_WEIGHTS.get(field, 1)
        for token in tokenize_search_text(text):
            if not single_cjk_token(token):
                counts[token] += weight
    return counts


def add_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def single_cjk_token(token: str) -> bool:
    return len(token) == 1 and bool(CJK_RUN_RE.fullmatch(token))


def search_boost(
    query: str,
    query_tokens: set[str],
    fields: dict[str, str],
) -> tuple[float, list[str]]:
    normalized_query = normalize_search_text(query)
    score = 0.0
    reasons: list[str] = []

    for field in SEARCH_EXACT_FIELDS:
        normalized_value = normalize_search_text(fields.get(field))
        if not normalized_query or not normalized_value:
            continue
        if normalized_value == normalized_query:
            score += 100.0
            add_reason(reasons, f"exact {field}")
        elif normalized_query in normalized_value:
            score += 35.0
            add_reason(reasons, f"{field} contains query")
        elif len(normalized_value) >= 4 and normalized_value in normalized_query:
            score += 20.0
            add_reason(reasons, f"query contains {field}")

    field_token_boosts = {
        "title": 7.0,
        "stem": 6.0,
        "filename": 6.0,
        "source_url": 5.0,
        "metadata": 2.0,
        "body": 1.0,
    }
    meaningful_tokens = {token for token in query_tokens if not single_cjk_token(token)}
    for field, boost in field_token_boosts.items():
        field_text = fields.get(field, "")
        field_tokens = set(tokenize_search_text(field_text))
        overlap = meaningful_tokens & field_tokens
        if overlap:
            score += boost * len(overlap)
            add_reason(reasons, f"{field} token match")

        normalized_value = normalize_search_text(field_text)
        if len(normalized_query) >= 3 and normalized_query in normalized_value:
            score += boost * 2
            add_reason(reasons, f"{field} contains query")

    return score, reasons


def bm25_scores(notes: list[dict[str, Any]], query_tokens: set[str]) -> list[float]:
    query_tokens = {token for token in query_tokens if not single_cjk_token(token)}
    if not notes or not query_tokens:
        return [0.0 for _ in notes]

    documents = [weighted_token_counts(note) for note in notes]
    document_lengths = [sum(document.values()) for document in documents]
    average_length = sum(document_lengths) / len(document_lengths) if document_lengths else 0.0
    if average_length <= 0:
        return [0.0 for _ in notes]

    document_frequency: Counter[str] = Counter()
    for document in documents:
        for token in document:
            document_frequency[token] += 1

    total_documents = len(documents)
    k1 = 1.5
    b = 0.75
    scores: list[float] = []
    for document, document_length in zip(documents, document_lengths, strict=True):
        score = 0.0
        for token in query_tokens:
            frequency = document.get(token, 0)
            if not frequency:
                continue
            idf = math.log(1 + (total_documents - document_frequency[token] + 0.5) / (document_frequency[token] + 0.5))
            denominator = frequency + k1 * (1 - b + b * document_length / average_length)
            score += idf * (frequency * (k1 + 1)) / denominator
        scores.append(score)
    return scores


def clipped_snippet(text: str, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def search_snippet(note: dict[str, Any], query: str, query_tokens: set[str]) -> str:
    fields = note_search_fields(note)
    normalized_query = normalize_search_text(query)
    meaningful_tokens = {token for token in query_tokens if not single_cjk_token(token)}
    candidates = [
        fields["title"],
        fields["source_url"],
        *str(note.get("body") or "").splitlines(),
    ]
    for candidate in candidates:
        normalized_candidate = normalize_search_text(candidate)
        if len(normalized_query) >= 3 and normalized_query in normalized_candidate:
            return clipped_snippet(candidate)
        if meaningful_tokens and meaningful_tokens & set(tokenize_search_text(candidate)):
            return clipped_snippet(candidate)
    return clipped_snippet(fields["title"] or str(note.get("body") or ""))


def search_result(
    note: dict[str, Any],
    *,
    score: float,
    reasons: list[str],
    snippet: str,
    include_body: bool = False,
) -> dict[str, Any]:
    result = {
        "path": note["path"],
        "filename": note["filename"],
        "stem": note["stem"],
        "metadata": note["metadata"],
        "title": note["title"],
        "score": round(score, 3),
        "match_reason": reasons,
        "snippet": snippet,
    }
    if include_body:
        result["sections"] = note["sections"]
        result["body"] = note["body"]
    return result


def iter_notes(materials_dir: Path) -> list[dict[str, Any]]:
    return [read_note(path) for path in sorted(materials_dir.glob("*.md")) if path.is_file()]


def find_notes(
    materials_dir: Path,
    *,
    note_id: str | None = None,
    source_url: str | None = None,
    path: str | None = None,
) -> list[dict[str, Any]]:
    if path:
        target = Path(path).expanduser()
        if not target.is_absolute():
            target = materials_dir / target
        target = target.resolve()
        if target.exists() and target.suffix.lower() == ".md":
            return [read_note(target)]
        return []

    matches = []
    for note in iter_notes(materials_dir):
        meta = note["metadata"]
        if note_id and meta.get("id") == note_id:
            matches.append(note)
        elif source_url and normalize_search_text(meta.get("source_url")) == normalize_search_text(source_url):
            matches.append(note)
    return matches


def search_notes(
    materials_dir: Path,
    query: str,
    *,
    maturities: set[str] | None = None,
    verifications: set[str] | None = None,
    topics: set[str] | None = None,
    kinds: set[str] | None = None,
    limit: int = 10,
    min_score: float = 0.0,
    include_body: bool = False,
) -> list[dict[str, Any]]:
    if limit <= 0:
        die("--top must be greater than 0.")

    query_tokens = set(tokenize_search_text(query))
    if not query_tokens and not normalize_search_text(query):
        return []

    notes = []
    for note in iter_notes(materials_dir):
        meta = note["metadata"]
        if maturities and meta.get("maturity") not in maturities:
            continue
        if verifications and meta.get("verification") not in verifications:
            continue
        if kinds and meta.get("kind") not in kinds:
            continue
        if topics:
            note_topics = meta.get("topic") or []
            if isinstance(note_topics, str):
                note_topics = [note_topics]
            if not (topics & set(str(t) for t in note_topics)):
                continue
        notes.append(note)

    bm25 = bm25_scores(notes, query_tokens)
    results = []
    for note, bm25_score in zip(notes, bm25, strict=True):
        fields = note_search_fields(note)
        boost, reasons = search_boost(query, query_tokens, fields)
        score = bm25_score + boost
        if score <= min_score:
            continue
        if bm25_score > 0:
            add_reason(reasons, "bm25 token match")
        results.append(
            search_result(
                note,
                score=score,
                reasons=reasons,
                snippet=search_snippet(note, query, query_tokens),
                include_body=include_body,
            )
        )

    results.sort(key=lambda result: (-result["score"], result["filename"]))
    exact_results = [
        result
        for result in results
        if any(reason.startswith("exact ") for reason in result["match_reason"])
    ]
    if exact_results:
        results = exact_results
    return results[:limit]


def require_one(matches: list[dict[str, Any]], label: str) -> dict[str, Any]:
    if not matches:
        die(f"No material matched {label}.")
    if len(matches) > 1:
        die(f"More than one material matched {label}.")
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


def normalize_tag_list(value: Any) -> list[str]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        items = value
    elif isinstance(value, str):
        items = [part.strip() for part in value.split(",")]
    else:
        items = [value]
    seen: set[str] = set()
    normalized: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def load_note_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.note_json:
        try:
            payload = json.loads(args.note_json)
        except json.JSONDecodeError as inline_error:
            try:
                raw = Path(args.note_json).read_text(encoding="utf-8")
            except OSError as file_error:
                die(
                    "--note-json must be valid inline JSON or a readable JSON file: "
                    f"{inline_error}; {file_error}"
                )
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                die(f"Invalid note JSON in {args.note_json}: {exc}")
    else:
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            die(f"Invalid note JSON from stdin: {exc}")
    if not isinstance(payload, dict):
        die("Note JSON must be an object.")
    return payload


def cmd_resolve(args: argparse.Namespace) -> None:
    materials_dir = resolve_materials_dir(args, create=args.create)
    if args.save:
        save_config(materials_dir)
    print(json.dumps({"materials_dir": str(materials_dir)}, ensure_ascii=False, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    materials_dir = resolve_materials_dir(args)
    maturities = set(args.maturity or [])
    verifications = set(args.verification or [])
    topics = set(args.topic or [])
    kinds = set(args.kind or [])
    result = []
    for note in iter_notes(materials_dir):
        meta = note["metadata"]
        if maturities and meta.get("maturity") not in maturities:
            continue
        if verifications and meta.get("verification") not in verifications:
            continue
        if kinds and meta.get("kind") not in kinds:
            continue
        if topics:
            note_topics = meta.get("topic") or []
            if isinstance(note_topics, str):
                note_topics = [note_topics]
            if not (topics & set(str(t) for t in note_topics)):
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
    materials_dir = resolve_materials_dir(args)
    exact_locator = args.id or args.source_url or args.path
    if args.query and exact_locator:
        die("Use either a positional query or exact locator flags, not both.")
    if args.query:
        matches = search_notes(
            materials_dir,
            args.query,
            maturities=set(args.maturity or []),
            verifications=set(args.verification or []),
            topics=set(args.topic or []),
            kinds=set(args.kind or []),
            limit=args.top,
            min_score=args.min_score,
            include_body=args.include_body,
        )
    else:
        matches = find_notes(
            materials_dir,
            note_id=args.id,
            source_url=args.source_url,
            path=args.path,
        )
    if args.require_one:
        matches = [require_one(matches, args.query or exact_locator)]
    print(json.dumps(matches, ensure_ascii=False, indent=2))


def cmd_read(args: argparse.Namespace) -> None:
    materials_dir = resolve_materials_dir(args)
    label = args.id or args.source_url or args.path
    note = require_one(
        find_notes(
            materials_dir,
            note_id=args.id,
            source_url=args.source_url,
            path=args.path,
        ),
        label,
    )
    print(json.dumps(note, ensure_ascii=False, indent=2))


def cmd_write(args: argparse.Namespace) -> None:
    materials_dir = resolve_materials_dir(args, create=True)
    payload = load_note_payload(args)
    meta = dict(payload.get("metadata") or {})
    sections = dict(payload.get("sections") or {})
    title = str(payload.get("title") or meta.get("title") or "").strip()
    filename = safe_filename(str(payload.get("filename") or title))

    for key in ["id", "created", "kind", "verification", "maturity"]:
        if not meta.get(key):
            die(f"Missing required metadata field: {key}")
    if not title:
        title = str(meta["title"])
    meta["title"] = title
    meta["topic"] = normalize_tag_list(meta.get("topic"))
    meta["platforms"] = normalize_tag_list(meta.get("platforms"))
    meta["related"] = normalize_related(meta.get("related"))
    events = meta.get("events")
    if not isinstance(events, list) or not events:
        meta["events"] = [f"{date.today().isoformat()} captured"]

    existing = find_notes(
        materials_dir,
        note_id=meta.get("id"),
        source_url=meta.get("source_url") or None,
    )
    target = (materials_dir / filename).resolve()
    if not str(target).startswith(str(materials_dir)):
        die(f"Target escapes material directory: {target}")

    action = "created"
    if existing:
        current = require_one(existing, meta.get("id"))
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
    materials_dir = resolve_materials_dir(args)
    label = args.id or args.source_url or args.path
    note = require_one(
        find_notes(
            materials_dir,
            note_id=args.id,
            source_url=args.source_url,
            path=args.path,
        ),
        label,
    )
    path = Path(note["path"])
    meta = note["metadata"]
    meta["maturity"] = args.maturity
    events = meta.get("events")
    if not isinstance(events, list):
        events = []
    events.append(args.event or f"{date.today().isoformat()} {args.maturity}")
    meta["events"] = events
    title = str(meta.get("title") or note["title"])
    path.write_text(format_frontmatter(meta) + "\n\n" + format_body(title, note["sections"]) + "\n", encoding="utf-8")
    print(json.dumps({"action": "marked", "path": str(path), "maturity": args.maturity}, ensure_ascii=False, indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    materials_dir = resolve_materials_dir(args)
    label = args.id or args.source_url or args.path
    note = require_one(
        find_notes(
            materials_dir,
            note_id=args.id,
            source_url=args.source_url,
            path=args.path,
        ),
        label,
    )
    path = Path(note["path"]).resolve()
    if path.parent != materials_dir:
        die(f"Refusing to delete outside material directory: {path}")
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
    list_cmd.add_argument("--maturity", action="append")
    list_cmd.add_argument("--verification", action="append")
    list_cmd.add_argument("--topic", action="append")
    list_cmd.add_argument("--kind", action="append")
    list_cmd.add_argument("--include-body", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    find = sub.add_parser("find")
    find.add_argument("query", nargs="?")
    find.add_argument("--dir")
    find.add_argument("--id")
    find.add_argument("--source-url")
    find.add_argument("--path")
    find.add_argument("--maturity", action="append")
    find.add_argument("--verification", action="append")
    find.add_argument("--topic", action="append")
    find.add_argument("--kind", action="append")
    find.add_argument("--top", type=int, default=10)
    find.add_argument("--min-score", type=float, default=0.0)
    find.add_argument("--include-body", action="store_true")
    find.add_argument("--require-one", action="store_true")
    find.set_defaults(func=cmd_find)

    read = sub.add_parser("read")
    read.add_argument("--dir")
    read.add_argument("--id")
    read.add_argument("--source-url")
    read.add_argument("--path")
    read.set_defaults(func=cmd_read)

    write = sub.add_parser("write")
    write.add_argument("--dir")
    write.add_argument(
        "--note-json",
        help="inline JSON object or path to a UTF-8 JSON file; reads stdin when omitted",
    )
    write.set_defaults(func=cmd_write)

    mark = sub.add_parser("mark")
    mark.add_argument("--dir")
    mark.add_argument("--id")
    mark.add_argument("--source-url")
    mark.add_argument("--path")
    mark.add_argument("--maturity", required=True, choices=["raw", "incubating", "ready", "published", "archived"])
    mark.add_argument("--event")
    mark.set_defaults(func=cmd_mark)

    delete = sub.add_parser("delete")
    delete.add_argument("--dir")
    delete.add_argument("--id")
    delete.add_argument("--source-url")
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
