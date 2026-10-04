# Runtime Verification

## Status and evidence layers

GPT-6 迁移基线（2026-10-03）：**完整流程未验证；顾问权限受限**。四个角色模型/effort 的实际调用结果见[验证记录](verification/gpt6-routing-smoke.md)。旧版 GPT-5.6 的实践记录不证明新版映射、路由、质量或成本已验证。

分开记录：

1. **静态配置**：TOML 可解析、model / reasoning / sandbox 正确，提示词与所选模式一致。
2. **角色注册**：当前会话实际暴露预期角色与模型映射。磁盘更新不保证运行中的会话重新加载。
3. **实际运行**：匹配的子会话身份、角色、model、reasoning、有效 sandbox/approval 元数据以及任务结果。未调用过的角色不能标为已验证。

## Expected runtime

| Role / Root profile | Expected model | Reasoning | Sandbox |
|---|---|---|---|
| `luna-worker` | `gpt-6-luna` | `max` | workspace-write |
| `sol-worker` | `gpt-6.1-sol` | `medium` | workspace-write |
| `sol-advisor` | `gpt-6.1-sol` | `high` | read-only |
| `astra-advisor` | `gpt-6-astra` | `high` | read-only |
| Strong Orchestrator default Root | `gpt-6.1-sol` | `high` | 当前会话权限 |
| Strong Orchestrator optional Root | `gpt-6-astra` | `high` | 当前会话权限 |
| Luna-first Root | `gpt-6-luna` | `max` | 当前会话权限 |

档位是初始基线。用户明确选择其他受支持的 Root effort 时，将其记录为自定义 profile 并按该值验证。Advisor 必须遵守不写入的行为约束；表中的 read-only 是有效权限验收要求，不能仅由 TOML 推断已强制生效。父会话实时权限可能覆盖该值。

## Automated metadata check

需要 Python 3.11+，无第三方依赖。在仓库根目录运行：

```bash
python3 scripts/verify_runtime.py \
  --session /path/to/child-session.jsonl \
  --agent-file .codex/agents/sol-advisor.toml \
  --parent-thread ACTUAL_PARENT_THREAD_ID
python3 -m unittest discover -s tests -v
```

脚本只读取 session_meta / turn_context 等结构化记录，不把消息文本当作证据；检查父子关联、角色、每个已记录 turn 的模型、effort 和有效文件沙箱，并要求/报告 approval 元数据（它不等于独立的连接器权限认证）。字段缺失或格式不支持时返回 unverified；不匹配返回 mismatch，退出码均为 1。退出码 0 仅表示配置元数据匹配，不证明任务质量、所有连接器权限或最终验收；task_completed 单独报告。

父会话实时权限可能覆盖角色沙箱。实质咨询前先用无工具握手取得元数据；advisor 实际为 workspace-write 或无法确认 read-only 时，停止该咨询并报告受限。可在支持独立角色权限的宿主或独立 read-only 会话中重新验证；后者不能冒充同一 Custom Agent 调用链已验证。不要自动修改全局权限。来源：[官方 Subagents 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)。

## Inspect relevant sessions

优先定位本次实际调用对应的子会话，而不是把无关会话中的模型字符串当作证据。已知 JSONL 路径后可用下面的命令定位候选记录：

```bash
rg -n '"thread_source"|"source"|"agent_role"|"agent_nickname"|"turn_context"|"model"|"reasoning_effort"|"effort"|"sandbox_policy"|"approval_policy"' \
  /path/to/rollout-....jsonl
```

字段和嵌套结构随客户端版本变化。读取实际 JSON 对象，确认记录类型、父子会话关联、角色和同一次调用的 model / reasoning / sandbox_policy / approval_policy。`thread_source = subagent` 只是一种可能表示；也可能通过嵌套 source / parent 信息表达来源。普通消息正文、复制的 TOML、工具输出中的字符串都不是实际调用元数据。

示例预期值（示意，不是真实运行证据）：`astra-advisor`、`gpt-6-astra`、`high`。必须同时关联角色与实际执行上下文，不能仅找到其中一个字符串就判定成功。

缺少或无法访问必要字段时，标为未验证并说明缺失。若注册角色缺失或仍使用旧模型，按客户端要求重新加载/开启会话后重查。不可静默回退到其他模型，也不可自动修改全局默认模型。

## Migration acceptance scenarios

使用明确授权的、边界清晰的任务检验下列行为；静态审阅只能证明规则表达一致，不能替代运行：

| Scenario | Expected behavior |
|---|---|
| 两种模式的小任务，Root 能可靠执行和验证且委派收益不足 | Root 本地完成 |
| 很小但超出 Luna 可靠能力的复杂实现 | Mode B 直接 Sol worker，不能因行数少而留在 Luna |
| 顾问 TOML 只读，但实际 sandbox 是 workspace-write | 无工具握手后报告 mismatch，停止实质咨询 |
| Custom Agent 固定 effort 与调用参数冲突 | 以角色 TOML 为准；不声称动态覆盖成功 |
| 当前客户端缺少角色选择入口 | 配置安装与运行能力分开报告，runtime 不可用 |
| Mode A，清晰且值得委派的执行 | Luna worker |
| 两种模式，目标明确但实现需要复杂推理 | Sol worker |
| Mode A / Sol Root，重大判断尚未可靠解决 | Astra advisor 只读咨询后返回 Root |
| Mode A / Astra Root，困难判断 | Root 直接处理，不例行调用同级 Astra advisor |
| Mode B，局部设计或根因判断需要较强推理 | Sol advisor，只读 |
| Mode B，高代价且高歧义决策 | 可直接咨询 Astra，不强制先经过 Sol |
| Mode B，咨询后仍有复杂实现 | Luna 调度 Sol worker，不强制 Luna 模型实现 |
| 缺少权限、工具或用户事实 | 报告对应阻塞，不以此为由盲目升级模型 |
| Worker 遇到 scope expansion | 返回 Root，不递归委派 |
| 顾问返回建议但缺少验证结果 | Root 补充验证或报告阻塞，不直接验收 |

## Evaluation record

记录日期、客户端版本、模式、选定 Root profile、任务与验收标准、角色、实际 model / effort / sandbox / approval、最小 runtime 元数据证据、验证结果、耗时、可获得的 Token 指标、返工次数和阻塞。缺失指标记为 unavailable，不填零。

对外分享时只摘录必要的模型和调用元数据，避免提交包含私有项目内容或凭据的完整 session JSONL。先确认映射与边界，再比较代表性任务上的质量和成本。不要根据配置、角色名称或 Agent 自述宣称模型已运行。

English: distinguish static configuration, registered roles, and actual runtime. Match role, child-session identity, model, reasoning, and effective sandbox/approval from execution metadata. Message text is not runtime evidence. Uninvoked roles and inaccessible metadata remain unverified; evaluate full-task quality, time, tokens, and rework separately.
