# Nanobot Workflows：维护者说明

[English](MAINTAINING.md) | 简体中文

本文面向维护者；普通用户的安装与首次使用见 [README](README.zh-CN.md)。

## 旧版迁移

没有旧安装的用户可跳过本节。

- 旧调用 `$pr-review`、`$verify`、`$how`、`$poteto-mode` 等改为 `$workflow <任务或方法>`；`$nanobot-gate` 仍须显式调用。
- 先确认旧 standalone skill 的安装路径和归属，再移出发现目录；保留本地修改。Workspace skills 优先于插件，残留副本会增加 skill 摘要条目。
- 替换旧 pstack 插件前先禁用它；两者同时启用会保留旧插件的 54 条描述。
- 不要因 skill 是源码链接就删除源码目录。确认链接、安装副本和归属后再操作。
- 工作流偏好存放于 `<agent-workspace>/.nanobot-workflows/`。不会自动迁移或删除 `.pstack/` 状态；只迁移明确选择且受支持的偏好字段。

## 项目适配与按需加载

先读取目标仓库的 `AGENTS.md`、贡献指南、项目配置、脚本和 CI，再使用项目自己的命令与验收要求。优先使用项目已有验证器；仅在需要设计验证方案时使用公开接口验证流程。

项目专用流程见[项目适配层](skills/workflow/references/project.md)。随包提供的 [HKUDS/nanobot 适配](skills/workflow/projects/nanobot/workflow.md)适用于该仓库及其 fork；其他项目按自身工程配置执行。

只发现 `skills/workflow/SKILL.md` 与显式入口 `skills/nanobot-gate/SKILL.md`。主入口按需路由到 `routes/`、`workflows/`、`projects/`、`playbooks/`、`principles/`、`references/` 和辅助脚本；这些内部文档不是独立 skill。

共享 helper 使用实际安装路径调用，且用 `-B` 避免写入 bytecode：

```text
python -B "<plugin-root>/skills/workflow/scripts/workflow.py" paths
```

`paths` 只读打印外部设置和任务目录；`log` 向包外日志追加清理过的 TSV 行；`worktrees --repo <repo>` 只读盘点已登记 worktree，不 fetch 或删除。GitHub、浏览器、PowerShell 和 Herdr 流程各有前置条件，详见对应工作流及 [runtime 约束](skills/workflow/references/runtime.md)。

## 验证

在独立源码工作区使用 Python 3.11+ 和 Git 运行：

```text
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s skills/workflow/workflows/pr/worktree/tests -v
python -B -m unittest discover -s skills/workflow/workflows/environment/worktree-right/scripts -p "test_*.py" -v
```

若环境中有兼容的 nanobot 安装，包测试会执行原生 loader 测试；否则会明确跳过。原生集成检查应使用目标 nanobot 的同一环境。

## 许可证与来源

- 原创 skills 与整合部分：Copyright (c) 2026 chengyongru，MIT。
- pstack 衍生内容：Copyright (c) 2026 Lauren Tan，MIT；上游为 `cursor/plugins/pstack` v0.15.25，固定 commit `99743e9c151c8537cbbf1f98bb38f34ef3368453`。
- 完整说明见 [LICENSE](LICENSE)、[上游 MIT 声明](LICENSES/pstack-MIT.txt)、[第三方版权说明](THIRD_PARTY_NOTICES.md) 和 [provenance](provenance.json)。
