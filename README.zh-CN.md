Agent skills
============

[English](README.md) | 简体中文

一组聚焦单一工作流的可复用 [Agent Skills](https://agentskills.io/)。每个顶层目录都可以独立安装。

按任务安装最小组合。通用 skill 与项目专属 skill 同时匹配时，优先使用项目专属 skill。

Skill 索引
----------

| Skill | 用途 |
|---|---|
| [`repo-prose`](repo-prose/SKILL.md) | 让仓库文字保持当前、具体，并清除创作过程残留。 |
| [`web-design-taste`](web-design-taste/SKILL.md) | 统一产品界面的控件、排版与交互，提高信息含量。 |
| [`simplify`](simplify/SKILL.md) | 清理代码、注释和 workaround 并保持行为；审计时返回高层计划。 |
| [`verify`](verify/SKILL.md) | 用黑盒证据验证公共行为。 |
| [`nanobot-webui-verify`](nanobot-webui-verify/SKILL.md) | 通过真实 gateway 和浏览器验证 nanobot WebUI。 |
| [`nanobot-gate`](nanobot-gate/SKILL.md) | 协调 nanobot 的 simplify、verify、review 和 CI gate。 |
| [`triage`](triage/SKILL.md) | 为复杂对象生成简短决策简报。 |
| [`herdr-scode-delegate`](herdr-scode-delegate/SKILL.md) | 通过 Herdr 把后台任务委派给另一个 `scode` 会话。 |
| [`herdr-worktree-right`](herdr-worktree-right/SKILL.md) | 在当前 Herdr pane 右侧打开正在使用的 worktree，优先复用已有 pane。 |
| [`pr-worktree`](pr-worktree/SKILL.md) | 为每个分支维护唯一的 attached worktree。 |
| [`pr-review`](pr-review/SKILL.md) | 审查 PR 正确性、可达性和合并价值。 |
| [`pr-fix`](pr-fix/SKILL.md) | 在授权范围内修复 PR 分支。 |
| [`pr-rebase`](pr-rebase/SKILL.md) | 安全地 rebase 并验证 PR 分支。 |
| [`pr-label`](pr-label/SKILL.md) | 根据仓库证据分类和更新 PR 标签。 |
| [`pr-metadata`](pr-metadata/SKILL.md) | 让 PR 标题和描述与已推送内容保持一致。 |

路由
----

- 仓库文字：文档、注释和贡献者说明使用 `repo-prose`。
- Agent 委派：使用 `herdr-scode-delegate` 把边界明确的后台任务交给另一个 `scode` 会话，无需持续盯住其 pane。
- PR 代码工作：本地 review、测试、修复和 rebase 使用 `pr-worktree`。`triage`、`pr-label` 和 `pr-metadata` 直接操作远端 PR；`pr-fix` 在授权推送后组合调用 `pr-metadata`。
- 注释/workaround 审计：使用 `simplify` 返回只读高层计划。全仓审计可以按模块分给只读代理。清理请求执行范围内的修复及相应验证；`pr-review` 检查 PR 中相关注释和工具指令的变化。
- 验证：跨项目使用 `verify`；nanobot 浏览器/gateway 场景使用 `nanobot-webui-verify`；完整 nanobot 就绪检查使用 `nanobot-gate`。
- 人类可读的计划和结果直接在对话中交付；确定性状态和原始证据按需落盘。

推送、PR 评论、标签、合并和其他远端修改从对应操作的明确授权开始。

安装
----

克隆仓库，再把选中的 skill 复制或链接到 Agent 使用的发现目录：

    git clone https://github.com/chengyongru/skills.git ~/src/agent-skills
    mkdir -p ~/.agents/skills
    ln -s ~/src/agent-skills/pr-worktree ~/.agents/skills/pr-worktree
    ln -s ~/src/agent-skills/pr-review ~/.agents/skills/pr-review

不同 Agent 运行时可能使用不同路径。Codex 用户可以参考 [Build skills](https://learn.chatgpt.com/docs/build-skills)。

调用
----

多个已安装 skill 范围相近时，显式名称最清楚：

    Use $triage to explain PR #123 before a local review.
    Use $simplify to audit repository comments and workarounds; return a high-level plan without editing files.
    Use $nanobot-gate to check this change before PR creation.
    Use $pr-review to perform a read-only review of PR #123.

贡献
----

- 每个 skill 只保留一个职责和精确触发边界。
- `SKILL.md` 只写模型无法可靠自行推导的决策、契约和 helper 用法。
- 确定性机械操作放进 `scripts/`，真正按需使用的领域知识放进 `references/`。
- 按 [`AGENTS.md`](AGENTS.md) 使用动作导向的表达，并直接交付验证结果。
- skill 或路由变化时同步更新两份 README。
