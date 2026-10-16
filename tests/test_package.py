"""Check the shipped routing graph and exercise its real shared helper."""
from __future__ import annotations

import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / 'skills/workflow'
HELPER = WORKFLOW / 'scripts/workflow.py'
PACKAGE_PATHS = (
    'plugin.json', 'skills', 'LICENSE', 'LICENSES', 'THIRD_PARTY_NOTICES.md',
    'provenance.json', 'third_party', 'README.md', 'README.zh-CN.md',
)


def install_copy(workspace: Path) -> Path:
    target = workspace / 'plugins/nanobot-workflows'
    target.mkdir(parents=True)
    for name in PACKAGE_PATHS:
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, target / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        else:
            shutil.copyfile(source, target / name)
    return target


def document_links(document: Path) -> list[Path]:
    links: list[Path] = []
    fence: tuple[str, int] | None = None
    for line in document.read_text(encoding='utf-8').splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0], len(token)
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            continue
        if fence:
            continue
        for raw in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', line):
            if re.match(r'[a-z][a-z0-9+.-]*:', raw, re.I) or raw.startswith('#'):
                continue
            links.append((document.parent / unquote(raw.split('#', 1)[0])).resolve())
    return links


class PackageTests(unittest.TestCase):
    def test_public_entries_and_small_router(self) -> None:
        manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(manifest['name'], 'nanobot-workflows')
        self.assertEqual(manifest['repository'], 'https://github.com/chengyongru/skills')
        entries = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('SKILL.md'))
        self.assertEqual(entries, ['skills/nanobot-gate/SKILL.md', 'skills/workflow/SKILL.md'])
        for entry in entries:
            text = (ROOT / entry).read_text(encoding='utf-8')
            self.assertLessEqual(len(text.splitlines()), 60, entry)
            self.assertRegex(text, rf'(?m)^name: {Path(entry).parent.name}$')
        root_links = document_links(WORKFLOW / 'SKILL.md')
        domain_names = {p.name for p in root_links if p.parent == (WORKFLOW / 'routes').resolve()}
        self.assertEqual(domain_names, {'investigate.md', 'code.md', 'pr.md', 'verify.md',
                                        'writing.md', 'coordinate.md', 'authoring.md', 'environment.md'})

    def test_all_document_links_are_contained_and_resolve(self) -> None:
        for document in ROOT.rglob('*.md'):
            if '.git' in document.parts:
                continue
            for target in document_links(document):
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(target.is_relative_to(ROOT.resolve()), target)
                    self.assertTrue(target.exists(), target)
            quoted = re.findall(r'`((?:references|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|ps1))(?=[ `])',
                                document.read_text(encoding='utf-8'))
            for relative in quoted:
                with self.subTest(document=document.relative_to(ROOT), quoted=relative):
                    self.assertTrue((document.parent / relative).is_file(), relative)
        for path in (ROOT / 'skills').rglob('*'):
            self.assertFalse(path.is_symlink(), path)

    def test_integrated_capabilities_are_reachable_from_entries(self) -> None:
        provenance = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
        targets = provenance['integration']['legacy_workflow_targets']
        self.assertEqual(len(targets), 69)
        visited: set[Path] = set()
        pending = [WORKFLOW / 'SKILL.md', ROOT / 'skills/nanobot-gate/SKILL.md']
        while pending:
            current = pending.pop().resolve()
            if current in visited or current.suffix != '.md' or not current.is_file():
                continue
            visited.add(current)
            pending.extend(document_links(current))
        for name, relative in targets.items():
            with self.subTest(capability=name):
                self.assertIn((ROOT / relative).resolve(), visited)
        self.assertEqual(len(list((WORKFLOW / 'playbooks').rglob('*.md'))), 23)
        self.assertEqual(len(list((WORKFLOW / 'principles').glob('*.md'))), 24)

    def test_concrete_personal_helpers_preserve_source_content(self) -> None:
        provenance = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
        sources = provenance['sources']['personal_skills']['helper_sha256_lf']
        targets = provenance['integration']['legacy_workflow_targets']
        checked = 0
        for old, digest in sources.items():
            path = Path(old)
            if path.suffix not in {'.py', '.ps1'}:
                continue
            destination = (ROOT / targets[path.parts[0]]).parent / Path(*path.parts[1:])
            normalized = destination.read_text(encoding='utf-8').encode('utf-8')
            self.assertEqual(sha256(normalized).hexdigest(), digest, destination)
            checked += 1
        self.assertGreater(checked, 10)
        license_text = (ROOT / 'LICENSES/pstack-MIT.txt').read_text(encoding='utf-8')
        self.assertEqual(sha256(license_text.encode('utf-8')).hexdigest(),
                         provenance['sources']['pstack']['license_sha256_lf'])


class SharedHelperTests(unittest.TestCase):
    def run_helper(self, helper: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, '-B', str(helper), *args], check=check,
                              capture_output=True, text=True, encoding='utf-8', timeout=30)

    def test_installed_and_staging_paths_do_not_create_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix='workflow paths ') as temporary:
            workspace = Path(temporary) / 'agent workspace'
            package = install_copy(workspace)
            helper = package / 'skills/workflow/scripts/workflow.py'
            payload = json.loads(self.run_helper(helper, 'paths').stdout)
            self.assertEqual(Path(payload['package']).resolve(), package.resolve())
            self.assertEqual(Path(payload['workspace']).resolve(), workspace.resolve())
            self.assertEqual(Path(payload['settings']), workspace.resolve() / '.nanobot-workflows/settings.json')
            self.assertEqual(list(workspace.iterdir()), [workspace / 'plugins'])
            staged = json.loads(self.run_helper(HELPER, 'paths', '--workspace', str(workspace)).stdout)
            self.assertEqual(Path(staged['state']), workspace.resolve() / '.nanobot-workflows')
            missing_target = self.run_helper(HELPER, 'paths', check=False)
            self.assertNotEqual(missing_target.returncode, 0)
            self.assertIn('pass --workspace for staging', missing_target.stderr)

    def test_log_roundtrip_and_immutable_package_boundary(self) -> None:
        with tempfile.TemporaryDirectory(prefix='workflow log ') as temporary:
            workspace = Path(temporary) / 'agent workspace'
            package = install_copy(workspace)
            helper = package / 'skills/workflow/scripts/workflow.py'
            log = workspace / '.nanobot-workflows/runs/task/decisions.tsv'
            self.run_helper(helper, 'log', str(log), 'verify', '=value\twith newline\n',
                            'why', 'evidence', 'PASS')
            self.run_helper(helper, 'log', str(log), 'done', 'keep', 'why', 'evidence', 'PASS')
            rows = list(csv.DictReader(io.StringIO(log.read_text(encoding='utf-8')), delimiter='\t'))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['decision'], "'=value with newline ")
            self.assertEqual(rows[1]['result'], 'PASS')
            original = (package / 'README.md').read_bytes()
            refused = self.run_helper(helper, 'log', str(package / 'README.md'), 'x', 'x', 'x', 'x', 'x', check=False)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn('outside the immutable plugin package', refused.stderr)
            self.assertEqual((package / 'README.md').read_bytes(), original)

    def test_worktree_inventory_observes_real_git_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix='workflow git ') as temporary:
            root = Path(temporary)
            repo = root / 'repo with spaces'
            repo.mkdir()
            def git(*args: str) -> str:
                return subprocess.run(['git', '-C', str(repo), *args], check=True,
                                      capture_output=True, text=True, encoding='utf-8', timeout=30).stdout
            git('init')
            git('config', 'user.name', 'Workflow Test')
            git('config', 'user.email', 'workflow@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            git('commit', '--allow-empty', '-m', 'fixture')
            worktree = root / 'topic worktree'
            git('worktree', 'add', '-b', 'topic', str(worktree))
            (worktree / 'evidence.txt').write_text('untracked fixture', encoding='utf-8')
            git('worktree', 'lock', '--reason', 'fixture-owned', str(worktree))
            before = git('worktree', 'list', '--porcelain')
            records = json.loads(self.run_helper(HELPER, 'worktrees', '--repo', str(repo)).stdout)
            indexed = {Path(record['worktree']).resolve(): record for record in records}
            self.assertEqual(set(indexed), {repo.resolve(), worktree.resolve()})
            self.assertEqual(indexed[worktree.resolve()]['locked'], 'fixture-owned')
            self.assertIn('?? evidence.txt', indexed[worktree.resolve()]['status'])
            self.assertEqual(git('worktree', 'list', '--porcelain'), before)


if __name__ == '__main__':
    unittest.main()
