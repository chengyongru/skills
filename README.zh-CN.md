Agent skills
============

[English](README.md) | 简体中文

一组聚焦单一工作流的可复用 [Agent Skills](https://agentskills.io/)。每个顶层目录都可以独立安装。

按任务安装最小组合。通用 skill 与项目专属 skill 同时匹配时，优先使用项目专属 skill。

Skill 索引
----------

| Skill | 用途 |
|---|---|
| [`grill-me`](grill-me/SKILL.md) | 逐个决策压力测试计划。 |
| [`idea-capture`](idea-capture/SKILL.md) | 保存和维护可行动想法。 |
| [`idea-next`](idea-next/SKILL.md) | 选择一个有证据支持的下一步。 |
| [`material`](material/SKILL.md) | 保存值得分享的已验证素材。 |
| [`draft`](draft/SKILL.md) | 把素材或原始输入写成可发布内容。 |
| [`rewrite`](rewrite/SKILL.md) | 在保护事实和声音的前提下润色中文技术写作。 |
| [`autoresearch`](autoresearch/SKILL.md) | 准备单目标的可量化改进实验。 |
| [`abtest`](abtest/SKILL.md) | 准备隔离的 control/treatment 实验。 |
| [`simplify`](simplify/SKILL.md) | 执行行为保持型代码清理。 |
| [`verify`](verify/SKILL.md) | 用黑盒证据验证公共行为。 |
| [`nanobot-webui-verify`](nanobot-webui-verify/SKILL.md) | 通过真实 gateway 和浏览器验证 nanobot WebUI。 |
| [`nanobot-gate`](nanobot-gate/SKILL.md) | 协调 nanobot 的 simplify、verify、review 和 CI gate。 |
| [`triage`](triage/SKILL.md) | 为复杂对象生成简短决策简报。 |
| [`pr-worktree`](pr-worktree/SKILL.md) | 为 PR 工作流准备隔离 worktree。 |
| [`pr-review`](pr-review/SKILL.md) | 审查 PR 正确性、可达性和合并价值。 |
| [`pr-fix`](pr-fix/SKILL.md) | 在授权范围内修复 PR 分支。 |
| [`pr-rebase`](pr-rebase/SKILL.md) | 安全地 rebase 并验证 PR 分支。 |
| [`pr-label`](pr-label/SKILL.md) | 根据仓库证据分类和更新 PR 标签。 |

路由
----

- 内容：`material -> draft -> rewrite`。
- PR：先用 `pr-worktree`，再按请求加入 `triage`、`pr-review`、`pr-fix`、`pr-rebase` 或 `pr-label`。
- 验证：跨项目使用 `verify`；nanobot 浏览器/gateway 场景使用 `nanobot-webui-verify`；完整 nanobot 就绪检查使用 `nanobot-gate`。
- 实验：迭代改进使用 `autoresearch`；control/treatment 对照使用 `abtest`。
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

    Use $idea-capture to save this idea.
    Use $nanobot-gate to check this change before PR creation.
    Use $pr-review to perform a read-only review of PR #123.

贡献
----

- 每个 skill 只保留一个职责和精确触发边界。
- `SKILL.md` 只写模型无法可靠自行推导的决策、契约和 helper 用法。
- 确定性机械操作放进 `scripts/`，真正按需使用的领域知识放进 `references/`。
- 按 [`AGENTS.md`](AGENTS.md) 使用动作导向的表达，并直接交付验证结果。
- skill 或路由变化时同步更新两份 README。
