"""Exercise the package through a compatible installed nanobot runtime."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import re
import tempfile
import unittest

from test_package import install_copy

try:
    from nanobot.agent.plugins import discover_agent_plugins, set_agent_plugin_enabled
    from nanobot.agent.skills import SkillsLoader
    from nanobot.agent.tools.context import ToolContext
    from nanobot.agent.tools.filesystem import ReadFileTool, WriteFileTool
    from nanobot.config.loader import get_config_path, set_config_path
    from nanobot.config.schema import ToolsConfig
    from nanobot.security.workspace_access import (
        bind_workspace_scope, reset_workspace_scope, validate_workspace_scope_payload,
    )
    COMPATIBLE = True
except ImportError:
    if os.environ.get('NANOBOT_REQUIRE_INTEGRATION') == '1':
        raise
    COMPATIBLE = False


@unittest.skipUnless(COMPATIBLE, 'requires an installed nanobot with Agent Plugins v1')
class NativeLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='native workflow ')
        self.root = Path(self.temporary.name)
        self.workspace = self.root / 'agent workspace'
        self.package = install_copy(self.workspace)
        self.old_config = get_config_path()
        set_config_path(self.root / 'instance/config.json')
        self.loader = SkillsLoader(self.workspace, builtin_skills_dir=self.root / 'no-builtins')

    def tearDown(self) -> None:
        set_config_path(self.old_config)
        self.temporary.cleanup()

    def enable(self) -> None:
        set_agent_plugin_enabled(self.workspace, 'nanobot-workflows', True)

    def test_approval_discovery_summary_and_exact_entry_invocation(self) -> None:
        plugin = discover_agent_plugins(self.workspace)[0]
        self.assertEqual(plugin.name, 'nanobot-workflows')
        self.assertFalse(plugin.enabled)
        self.assertEqual(self.loader.list_skills(), [])
        self.enable()
        names = sorted(entry['name'] for entry in self.loader.list_skills())
        self.assertIn('workflow', names)
        summary = self.loader.build_skills_summary()
        summarized = sorted(re.findall(r'^- \*\*([^*]+)\*\*', summary, re.M))
        self.assertEqual(summarized, names)
        self.assertEqual(self.loader.get_always_skills(), [])
        self.assertEqual(self.loader.get_explicitly_invoked_skills('$workflow review PR 123'), ['workflow'])
        self.assertEqual(self.loader.get_explicitly_invoked_skills('$pr-review $how $poteto-mode'), [])
        context = self.loader.build_explicit_skill_runtime_context('$workflow review PR 123')
        self.assertIsNotNone(context)
        body = (self.package / 'skills/workflow/SKILL.md').read_text(encoding='utf-8').split('---', 2)[2].strip()
        self.assertEqual(context.content,
                         '[Active Skills — instructions for this user turn]\n'
                         f'### Skill: workflow\n\n{body}\n[/Active Skills]')
        self.assertEqual(discover_agent_plugins(self.workspace)[0].display_name, 'Nanobot Workflows')

    def test_deep_reference_reads_are_approved_but_not_writes(self) -> None:
        self.enable()
        project = self.root / 'separate project'
        project.mkdir()
        resources = [self.package / 'skills/workflow' / relative for relative in (
            'projects/nanobot/webui/workflow.md',
            'references/linear.md',
            'references/linear-pr-links.md',
            'references/explanation.md',
            'workflows/pr/explain/workflow.md',
        )]
        originals = {resource: resource.read_bytes() for resource in resources}
        read = ReadFileTool.create(ToolContext(config=ToolsConfig(restrict_to_workspace=True),
                                                workspace=str(self.workspace)))
        write = WriteFileTool.create(ToolContext(config=ToolsConfig(restrict_to_workspace=True),
                                                  workspace=str(self.workspace)))
        scope = validate_workspace_scope_payload(
            {'project_path': str(project), 'access_mode': 'restricted'},
            default_workspace=self.workspace, default_restrict_to_workspace=True)
        async def probe() -> tuple[list[str], list[str], list[str]]:
            token = bind_workspace_scope(scope)
            try:
                good = [await read.execute(path=str(resource)) for resource in resources]
                refused = [await write.execute(path=str(resource), content='overwrite probe')
                           for resource in resources]
                set_agent_plugin_enabled(self.workspace, 'nanobot-workflows', False)
                disabled = [await read.execute(path=str(resource)) for resource in resources]
                return good, refused, disabled
            finally:
                reset_workspace_scope(token)
        good, refused, disabled = asyncio.run(probe())
        for index, resource in enumerate(resources):
            with self.subTest(resource=resource.relative_to(self.package)):
                self.assertIn(originals[resource].decode('utf-8').splitlines()[0], good[index])
                self.assertIn('outside allowed directory', refused[index])
                self.assertIn('outside allowed directory', disabled[index])
                self.assertEqual(resource.read_bytes(), originals[resource])

    def test_package_update_requires_new_approval(self) -> None:
        self.enable()
        resource = self.package / 'skills/workflow/workflows/pr/review/workflow.md'
        resource.write_text(resource.read_text(encoding='utf-8') + '\nUpdated candidate.\n', encoding='utf-8')
        self.assertFalse(discover_agent_plugins(self.workspace)[0].enabled)
        self.assertEqual(self.loader.list_skills(), [])
        self.enable()
        self.assertIn('workflow', [entry['name'] for entry in self.loader.list_skills()])


if __name__ == '__main__':
    unittest.main()
