Agent skills
============

[English](README.md) | 简体中文

这个仓库保存可复用的 AI Agent 工作流。每个顶层目录都是一个可以独立安装的
skill，其中包含 `SKILL.md`，并按需附带脚本或参考资料。

这些 skill 遵循开放的 [Agent Skills](https://agentskills.io/) 约定。大部分
skill 不绑定具体 Agent 运行时。`agents/` 目录中的文件只提供可选的运行时展示
信息，不定义工作流本身。

选择 skill
----------

不要安装这个仓库中的全部 skill。

只安装当前工作需要的最小组合。只有现有工作流产生了真实的交接需求时，才加入
另一个 skill。这样可以保持清晰的触发范围，避免无关工具依赖，也能减少专用
skill 在错误场景中被选中的可能。

常用的最小组合包括：

* 想法管理：`idea-capture` 和 `idea-next`。
* 内容发布：`material` 和 `draft`；中文编辑再加 `rewrite`。
* PR 审查：`pr-worktree` 和 `pr-review`；目的不清时再加 `triage`。
* PR 修复：`pr-worktree` 和 `pr-fix`；需要独立黑盒证据报告时再加 `verify`。
* 代码清理：`simplify`；需要用户侧证据时再接 `verify`。
* 实验规划：在 `autoresearch` 和 `abtest` 中选择一个，通常不必同时安装。

工作流与协作关系
----------------

规划与实验：

* [`grill-me`](grill-me/SKILL.md) 每次提出一个问题，逐步检查计划。目标或假设
  尚不清楚时，可以在实验规划 skill 之前使用它。
* [`autoresearch`](autoresearch/SKILL.md) 创建一个隔离 worktree，并为可量化的
  改进目标制定可审计计划。
* [`abtest`](abtest/SKILL.md) 创建 control 和 treatment worktree，用于严格的
  对照比较。

`autoresearch` 和 `abtest` 都在计划完成后停止，不会直接执行实验。

想法与内容发布：

* [`idea-capture`](idea-capture/SKILL.md) 保存可行动的工作并维护其状态。
* [`idea-next`](idea-next/SKILL.md) 读取想法目录，并选择一个具体的下一步。
* [`material`](material/SKILL.md) 保存经过验证、以后可能值得分享的事实、观察和
  经历片段。
* [`draft`](draft/SKILL.md) 把素材框架或原始输入写成适合目标平台的成稿。
* [`rewrite`](rewrite/SKILL.md) 对已有中文技术写作进行选择性编辑，同时保护
  事实、作者归属和声音。

想法目录和素材目录有意保持分离。`idea-capture` 记录“要做什么”，`material`
记录“什么值得分享”。正常的内容交接是 `material` 到 `draft`，`rewrite` 只是
可选的最后一步。

Pull Request 维护：

* [`pr-worktree`](pr-worktree/SKILL.md) 创建并检查隔离的 PR worktree。它是 PR
  场景下 `triage`、`pr-review` 和 `pr-fix` 的本地基础。
* [`triage`](triage/SKILL.md) 为 PR、Issue、文章、文档或陌生主题生成简短的
  决策简报。
* [`pr-review`](pr-review/SKILL.md) 从维护者视角检查正确性和合并价值。
* [`pr-fix`](pr-fix/SKILL.md) 在已有 PR 分支上完成聚焦修改，并且只在用户明确
  授权时推送。
* [`pr-label`](pr-label/SKILL.md) 根据仓库策略检查或修改 PR 标签。标签修改需要
  单独授权。

处理 PR 时，最长的交接路径通常是：

    pr-worktree -> triage -> pr-review -> pr-fix -> verify

并非每一步都是必需的。清晰的修复请求可以直接使用 `pr-worktree` 和 `pr-fix`。
Review 不会自动授权修复、推送、标签修改或 GitHub 评论。

清理与验证：

* [`simplify`](simplify/SKILL.md) 对最近或明确指定的代码进行不改变行为的清理，
  不负责寻找正确性问题。
* [`verify`](verify/SKILL.md) 通过 API、CLI、Web UI 或包消费者等公共接口检查
  已完成的改动，并报告具体证据。
* [`nanobot-webui-verify`](nanobot-webui-verify/SKILL.md) 是 nanobot WebUI 的
  专用验证器，通过真实 gateway 和 Playwright 检查用户流程。

nanobot WebUI 使用 `nanobot-webui-verify`，其他场景使用通用 `verify`。

交接规则
--------

* 每个工作流阶段只保留一个明确负责人。
* 交接具体产物，例如素材框架、worktree manifest、已确认的 review 问题或实验
  计划。
* 交接只提供上下文，不代表获得了外部修改权限。
* 专用 skill 保持可选，只在它声明的范围内安装或调用。
* 没有单独请求时，不要把规划工作流扩展为实际执行。

安装
----

先把仓库克隆到合适的位置：

    git clone https://github.com/chengyongru/skills.git ~/src/agent-skills

然后只把选中的顶层目录复制或链接到对应 Agent 使用的 skill 发现目录。

以 Codex 为例，用户级 skill 位于 `$HOME/.agents/skills`，仓库级 skill 位于
`<repo>/.agents/skills`。下面只安装 PR review 所需的组合：

    mkdir -p ~/.agents/skills
    ln -s ~/src/agent-skills/pr-worktree ~/.agents/skills/pr-worktree
    ln -s ~/src/agent-skills/pr-review ~/.agents/skills/pr-review

其他 Agent 可能使用不同的发现路径，请以对应运行时文档为准。Codex 用户可以
参考 [Build skills](https://learn.chatgpt.com/docs/build-skills)。

调用方式
--------

调用语法取决于具体运行时。支持显式指定 skill 的 Agent 通常接受这样的请求：

    Use $idea-capture to save this as an actionable idea.
    Use $draft to turn the ready material frame into an HN post.
    Use $pr-review to review PR #123; do not post anything to GitHub.

自然语言请求也可能根据描述选中 skill。如果已安装的 skill 范围相近，建议显式
写出名称。

仓库结构
--------

    <skill-name>/
        SKILL.md       必需的工作流与触发描述
        agents/        可选的运行时展示信息
        references/    相关时才加载的参考资料
        scripts/       可选的确定性辅助脚本

部分 skill 需要 Git、Python、PowerShell、GitHub CLI、Playwright 或其他本地
工具。安装依赖前先阅读选中的 `SKILL.md`。

贡献
----

* 每个 skill 只负责一个清晰职责，并明确触发边界。
* 写清 skill 接收什么，以及向下一个 skill 交接什么产物。
* 区分只读分析与编辑、推送、标签、评论等外部修改。
* 把确定性的机械操作放在 `scripts/`，可选背景资料放在 `references/`。
* 新增 skill 或修改协作边界时，同时更新两份 README。
