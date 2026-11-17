"""Fetch or check the reviewed TLC JAR in an explicitly selected external cache."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

URL = 'https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar'
SHA256 = '936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88'
FILENAME = 'tla2tools-1.7.4.jar'


def package_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / 'plugin.json').is_file():
            return parent
    return Path(__file__).resolve().parents[1]


def prepare(cache: Path, check: bool = False) -> Path:
    cache = cache.resolve()
    if cache.is_relative_to(package_root()):
        raise ValueError('Keep the tools cache outside the immutable plugin package')
    target = cache / FILENAME
    if target.exists():
        if sha256(target.read_bytes()).hexdigest() != SHA256:
            raise ValueError(f'Checksum mismatch; existing file left untouched: {target}')
        return target
    if check:
        raise FileNotFoundError(f'Pinned TLC is not cached: {target}')
    request = Request(URL, headers={'User-Agent': 'nanobot-workflows-statechart'})
    with urlopen(request, timeout=60) as response:
        data = response.read(20 * 1024 * 1024 + 1)
    if sha256(data).hexdigest() != SHA256:
        raise ValueError('Downloaded TLC checksum mismatch; no JAR published')
    cache.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=cache, prefix='.tlc-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.link(temporary, target)  # publish without replacing a concurrent writer's file
    finally:
        if temporary is not None:
            temporary.unlink()
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--check', action='store_true', help='verify only; no network or writes')
    args = parser.parse_args()
    try:
        target = prepare(args.cache, args.check)
    except (OSError, ValueError) as error:
        parser.exit(2, f'{error}\n')
    print(json.dumps({'path': str(target), 'release': 'v1.7.4', 'sha256': SHA256}))


if __name__ == '__main__':
    main()
