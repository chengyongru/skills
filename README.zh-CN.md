# Nanobot Workflows

[English](README.md) | 简体中文

一套用于工程化维护软件项目的工作流，以 nanobot Agent Plugin 提供，整合 chengyongru 的 skills 与适配后的 [pstack](https://github.com/cursor/plugins/tree/99743e9c151c8537cbbf1f98bb38f34ef3368453/pstack) 方法。各项目提供自己的规范、技术栈、命令和验收要求，nanobot 提供执行工具。

只有两个可发现的 skill：

| 入口 | 用途 |
|---|---|
| [`$workflow`](skills/workflow/SKILL.md) | 维护当前项目：先确认项目规范与工具，再按需读取工程工作流。 |
| [`$nanobot-gate`](skills/nanobot-gate/SKILL.md) | HKUDS/nanobot 及其 fork 可选的快照就绪检查，通过字面显式调用选择。 |

调查、代码、PR、验证、写作、协作、技能维护和环境操作都由主入口路由。具体工作流、审查方法、原则和 playbook 是按需读取的文件，不单独注册为 skill。它们的描述不会进入 nanobot 的常规 skill 摘要，主入口也不内嵌完整目录。

## 用 prompt 安装

需要支持 **Agent Plugins v1** 和 `$skill-name` 调用的 nanobot 版本。把下面的 prompt 发给要安装的 nanobot 实例：

```text
请从 https://github.com/chengyongru/skills 安装 nanobot-workflows Agent Plugin 到我当前的 nanobot 实例。

1. 确认目标实例的配置路径、agent workspace，以及 Agent Plugins v1 支持情况。目标不明确或有多个实例时，请我选择。
2. 在插件发现目录之外的任务临时目录克隆仓库，记录准确 commit SHA，审阅 README.md、plugin.json、LICENSE、THIRD_PARTY_NOTICES.md、provenance.json 和可执行 helper。审阅时不要运行仓库中的安装脚本。
3. 检查已有 nanobot-workflows 安装、旧 pstack 插件和来自此仓库的 standalone skills。报告冲突并保留本地改动，不要覆盖已有安装或修改我的源码工作区。如果需要禁用或备份冲突安装，列出具体路径并先取得我的同意。
4. 审阅通过后，只把 plugin.json、skills/、LICENSE、LICENSES/、THIRD_PARTY_NOTICES.md、provenance.json、third_party/、README.md 和 README.zh-CN.md 复制到 <agent-workspace>/plugins/nanobot-workflows/。保留我当前的实例配置、凭据、模型、个人资料和记忆。
5. 验证此包提供 workflow 和 nanobot-gate，通过受支持的启用入口批准最终快照。启用接口不可用时，保持禁用，并告诉我到 Apps 启用 Nanobot Workflows。
6. 保持当前 gateway 运行，最后给出安装摘要：安装路径、来源 SHA、启用状态、未解决的冲突，以及一个 $workflow 示例。
```

复制完成后，到 **Apps** 审阅并启用 **Nanobot Workflows**；列表未更新时刷新页面。

启用后的包不可变：修改任何包文件都会使启用状态失效。请在独立源码工作区开发，在发现目录之外准备更新，审阅最终内容并在替换后重新启用。不要在已启用的包目录中运行 `git pull` 或测试。

## 使用

```text
$workflow triage 这个 PR。说明主要变化、风险和下一步；不要创建本地 checkout 或发布评论。
$workflow 解释请求取消的调用链和状态归属，只读并引用当前代码。
$workflow 复现并在本地修复这个缺陷，再验证公开行为。不要提交或推送。
$workflow review PR 123，目标 SHA 为 <sha>。保留我的 dirty worktree，不发布 review。
$workflow simplify 当前 diff，保持行为不变，再运行聚焦检查。
$workflow 修改这份 README，保留准确命令和兼容条件。
$workflow 在右侧 Herdr pane 打开当前 worktree。
```

主入口的简短描述也支持按明确的自然语言任务选择；多个已安装能力重叠时，显式 `$workflow` 最清楚。可以用 `$workflow pr-review`、`$workflow how`、`$workflow architect` 选择具体方法。

## 按项目选择流程

先读取当前仓库的 `AGENTS.md`、贡献指南、项目配置、脚本和 CI，使用它自己的构建、格式化、测试、启动命令以及支持的浏览器或终端。优先使用项目已有的验证器，需要设计验证方案时使用公开接口验证工作流。

专用流程放在[项目适配层](skills/workflow/references/project.md)。随包提供的 [HKUDS/nanobot 适配](skills/workflow/projects/nanobot/workflow.md)包含它的 WebUI 启动器、WezTerm 检查和 UI 校准，用于该仓库及其 fork。其他项目按各自的工程配置执行。

## 从旧安装迁移

本仓库提供完整的 nanobot 插件。

- 把 `$pr-review`、`$verify`、`$how`、`$poteto-mode` 等旧调用改为 `$workflow <任务或方法>`。`$nanobot-gate` 保留独立、字面显式调用的入口。
- 审阅并把确认属于旧版的 standalone 安装移出发现路径，保留备份和本地改动。Workspace skills 的优先级高于插件，残留的旧技能仍会增加摘要条目。
- 用本包替换旧 pstack 时，先禁用旧 `pstack` 插件；同时启用两者不会消除旧插件的 54 条描述。
- 不要因为源码目录曾被链接为 skill 就删除源码。先确认每个安装副本或链接的路径与归属。
- 工作流偏好现在放在 `<agent-workspace>/.nanobot-workflows/`。不会自动迁移或删除已有 `.pstack/` 状态；需要时仅复制明确选定、受支持的偏好字段。

## 按需加载与目录

```text
plugin.json
skills/
  workflow/
    SKILL.md                 # 简短、可发现的主路由
    routes/                  # 每个领域一个索引
    workflows/               # 具体工作流及其相邻 helper
    projects/                # 按需选择的项目适配
    playbooks/               # 按领域分组的任务步骤
    principles/              # 按需读取的决策原则
    references/              # runtime 与 worker 约束
    scripts/workflow.py      # 路径、决策日志、只读 worktree 盘点
  nanobot-gate/
    SKILL.md                 # 独立的显式调用入口
    scripts/gate_state.py
```

先读入口，再读一个领域路由和匹配的工作流；只有需要时才读取更多方法或领域。共享资源放在已注册 skill 的目录内，保持在 nanobot 已批准的插件只读范围中。

共享 helper 只依赖 Python 标准库，使用实际安装路径运行：

```text
python -B "<plugin-root>/skills/workflow/scripts/workflow.py" paths
```

`paths` 只读输出外部设置和任务目录，不创建状态；`log` 向包外日志追加经过清理的 TSV 行；`worktrees --repo <repo>` 只读盘点本地登记的 worktree，不 fetch 或删除。GitHub、浏览器、PowerShell 和 Herdr 工作流各有前提，见具体工作流和 [runtime 约束](skills/workflow/references/runtime.md)。

## 验证改动

在独立源码工作区使用 Python 3.11+ 和 Git 运行：

```text
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s skills/workflow/workflows/pr/worktree/tests -v
python -B -m unittest discover -s skills/workflow/workflows/environment/worktree-right/scripts -p "test_*.py" -v
```

包测试覆盖路由和资源链接、公开入口边界、保留的来源契约以及真实 helper 命令。Python 环境中有兼容的 nanobot 安装时执行原生 loader 测试，否则明确跳过；原生集成检查应使用目标 nanobot 的同一环境。

## 许可证与版权

- 原创 skills 与整合部分：**Copyright (c) 2026 chengyongru**，MIT。
- pstack 衍生内容：**Copyright (c) 2026 Lauren Tan**，MIT。上游为 `cursor/plugins/pstack` 的 **v0.15.25**，固定 commit `99743e9c151c8537cbbf1f98bb38f34ef3368453`。

详细来源与整合记录见 [LICENSE](LICENSE)、原样保留的 [上游 MIT 声明](LICENSES/pstack-MIT.txt)、[第三方版权说明](THIRD_PARTY_NOTICES.md) 和 [provenance](provenance.json)。
