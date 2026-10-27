# Nanobot Workflows

[English](README.md) | 简体中文

Nanobot Agent Plugin，通过 [`$workflow`](skills/workflow/SKILL.md) 提供面向软件项目的常见工程工作流。

## 安装与启用

需要支持 **Agent Plugins v1** 和 `$skill-name` 调用的 nanobot。打开你要安装插件的 nanobot 对话，把下面整段内容发给它：

```text
请从 https://github.com/chengyongru/skills 安装 nanobot-workflows Agent Plugin 到当前 nanobot 实例。

1. 先确认目标实例、配置路径、agent workspace，以及是否支持 Agent Plugins v1 和 $skill-name 调用。目标不明确或有多个实例时，先让我选择；不支持时停止，不要修改文件。
2. 在插件目录之外的临时目录克隆仓库并记录准确 commit SHA。审阅 README.md、plugin.json、LICENSE、THIRD_PARTY_NOTICES.md、provenance.json 和会被调用的 helper；不要运行仓库里的安装脚本。
3. 检查是否已有 nanobot-workflows、旧 pstack 插件或本仓库的 standalone skills。不要覆盖已有安装、源码工作区或本机改动。若需要移动、禁用或备份冲突项，先列出路径和影响并征求我的同意。若当前账号无权写入目标目录，停止并告诉我需要管理员做什么。
4. 审阅通过后，只把 plugin.json、skills/、LICENSE、LICENSES/、THIRD_PARTY_NOTICES.md、provenance.json、third_party/、README.md、README.zh-CN.md、MAINTAINING.md 和 MAINTAINING.zh-CN.md 复制到 <agent-workspace>/plugins/nanobot-workflows/。保留实例配置、凭据、模型、个人资料和记忆。
5. 验证插件提供 workflow，并报告安装路径、commit SHA、发现的冲突和启用状态。不要代替我启用插件；保持当前 gateway 运行。
```

安装完成后，在 WebUI 打开 **Apps**，把筛选从 **Ready** 切换到 **Apps**，找到 **Nanobot Workflows**，审阅后启用。若列表未更新，先刷新 Apps 页面；仍找不到时，不要重复安装，向管理员确认当前实例是否支持 Agent Plugins。启用后新开一个对话，试发：

```text
$workflow 用几句话介绍你能帮我做什么；只做说明，不要修改文件。
```

## 使用

直接在 nanobot 对话中描述任务；任务范围重叠时，用 `$workflow` 明确选择入口。

- 正式开发或修复任务在有可用 Linear 工具时，先关联已有 Issue，没有对应事项才创建。更新聚焦已确认的范围、关键决策、阻塞和交付；没有 Linear 集成就跳过，无需额外配置。讨论和只读请求不自动建单。
- 为已知 Linear 任务交付 PR 时，区分 `Resolves`（完整交付）、`Contributes to`（部分推进）和 `Related to`（仅作关联），并核对实际关联；合并后的自动流转取决于仓库集成和团队工作流。
- 技术解释关注行为和完整链路的正确性，关系适合图示时优先使用 Mermaid。介绍 PR 时先说明不修改会在什么场景下出现什么问题、造成什么影响；实现审查是单独的请求。

示例：

```text
$workflow 介绍这个 PR 解决的用户问题，以及不修改会发生什么；只读，不做实现审查或发布评论。
$workflow 解释这个缺陷的原因，并提出修复方案；先不要改文件。
```
