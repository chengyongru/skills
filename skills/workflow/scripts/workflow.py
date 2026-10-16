"""Portable, explicit-path helpers for Nanobot Workflows."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parents[3]
HEADER = 'ts\tphase\tdecision\twhy\tevidence\tresult\n'


def paths(workspace: str | None) -> dict[str, str]:
    if workspace is None:
        if PACKAGE.parent.name != 'plugins':
            raise ValueError('Not installed under <agent-workspace>/plugins; pass --workspace for staging.')
        root = PACKAGE.parent.parent
    else:
        root = Path(workspace).expanduser().resolve()
    state = root / '.nanobot-workflows'
    return {'package': str(PACKAGE), 'workspace': str(root), 'state': str(state),
            'settings': str(state / 'settings.json'), 'runs': str(state / 'runs')}


def clean_cell(value: str) -> str:
    value = value.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    if value.lstrip().startswith(('=', '+', '-', '@')):
        value = "'" + value
    return value


def log_row(file: str, values: list[str]) -> Path:
    target = Path(file).expanduser().resolve()
    if target.is_relative_to(PACKAGE):
        raise ValueError('Runtime logs must be outside the immutable plugin package.')
    target.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    row = '\t'.join([timestamp, *(clean_cell(value) for value in values)]) + '\n'
    # Each task owns its own log. No multi-writer lock is implied.
    with target.open('a+', encoding='utf-8', newline='\n') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(HEADER)
        handle.write(row)
    return target


def git(repo: str, *args: str) -> str:
    result = subprocess.run(['git', '--no-optional-locks', '-C', repo, *args], check=True, text=True,
                            encoding='utf-8', capture_output=True, timeout=60)
    return result.stdout


def worktrees(repo: str) -> list[dict[str, object]]:
    raw = git(repo, 'worktree', 'list', '--porcelain', '-z')
    records: list[dict[str, object]] = []
    current: dict[str, object] = {}
    for item in raw.split('\0'):
        if not item:
            if current:
                records.append(current)
                current = {}
            continue
        key, _, value = item.partition(' ')
        current[key] = value if value else True
    if current:
        records.append(current)
    for record in records:
        path = record.get('worktree')
        if isinstance(path, str) and 'bare' not in record:
            record['exists'] = Path(path).is_dir()
            if record['exists']:
                record['status'] = git(path, 'status', '--porcelain=v1', '--untracked-files=normal')
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    location = commands.add_parser('paths', help='Print package and external state locations without writing.')
    location.add_argument('--workspace', help='Explicit agent workspace for staging verification.')
    log = commands.add_parser('log', help='Append one decision row to a task-owned TSV outside the package.')
    log.add_argument('file')
    for field in ('phase', 'decision', 'why', 'evidence', 'result'):
        log.add_argument(field)
    audit = commands.add_parser('worktrees', help='Read-only registered worktree inventory; never deletes.')
    audit.add_argument('--repo', required=True)
    args = parser.parse_args()
    if args.command == 'paths':
        result: object = paths(args.workspace)
    elif args.command == 'log':
        result = {'file': str(log_row(args.file, [args.phase, args.decision, args.why, args.evidence, args.result]))}
    else:
        result = worktrees(args.repo)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
