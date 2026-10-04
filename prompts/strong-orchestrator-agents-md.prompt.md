# Generate / Modify AGENTS.md — Strong Orchestrator

**简体中文** | [English](en/strong-orchestrator-agents-md.prompt.md)

本提示词只更新项目根目录 `AGENTS.md`，不安装全局 Agent、不修改其他文件。先确认所需角色可用；缺少角色时报告缺失，不声称已安装。

完整读取项目根目录已有 `AGENTS.md`。只更新 routing layer，保留无冲突的工程流程、Skills、worktree、testing、review 和 Git 规则。替换冲突的路由规则，不叠加两种架构。同一模式从旧版升级时，也要完整替换旧 routing section，清理过时的角色禁用规则；保留同一个 marker 不代表升级完成。不存在 `AGENTS.md` 时创建。生成简洁、可执行的规则，不原样复制本提示词。

## 模式与 Root Profile

保留唯一 architecture marker：

`<!-- ROUTING_ARCHITECTURE: STRONG_ORCHESTRATOR -->`

默认 Root profile 为 `gpt-6.1-sol / high`。用户已明确选择 Astra Root 时使用 `gpt-6-astra / high` profile。在 routing section 记录唯一选定的 Root model / reasoning，不能同时声明两个 Root。采用其他受支持的 reasoning 档位时必须由用户明确选择并记录为自定义 profile。

Root 始终拥有需求理解、规划、拆解、架构、路由、集成、冲突处理和最终验收。提示词不能切换当前线程的实际模型；runtime 与选定 profile 不符时报告 mismatch，不自行修改全局配置，也不声称模式已正确运行。

## 路由

| 工作 | Owner / Role |
|---|---|
| Root 能可靠执行并验证，且本地完成更经济的小任务或已有充分上下文的工作 | Root |
| 清晰、bounded、可验证且值得委派的执行 | `luna-worker` |
| 目标和范围明确，但需要跨文件推理、复杂调试或局部工程判断的执行 | `sol-worker` |
| 需求、架构、调度、集成和最终验收 | Root |
| Sol Root 经调查仍不能可靠解决的重大判断，或失败代价高且歧义显著的决策 | `astra-advisor`，只读咨询 |

Astra Root profile 下，最高难度判断由 Root 处理，不例行调用另一个 Astra advisor。`sol-advisor` 属于共享角色池，在本模式不默认使用；仅用户明确要求独立咨询时调用。

判断是否咨询 Astra 要给出具体决策问题和证据缺口，不能仅凭“安全”“迁移”等关键词升级。明确、已验证路径下的执行工作仍交给适合的 worker。

所有咨询返回 Root，所有 worker 的升级请求也返回 Root。保留 Strong Orchestrator 的最终责任归属。

## 共享 Agent Pool

| 角色 | 模型 | Reasoning | Sandbox |
|---|---|---|---|
| `luna-worker` | `gpt-6-luna` | `max` | `workspace-write` |
| `sol-worker` | `gpt-6.1-sol` | `medium` | `workspace-write` |
| `sol-advisor` | `gpt-6.1-sol` | `high` | `read-only` |
| `astra-advisor` | `gpt-6-astra` | `high` | `read-only` |

## 共同执行规则

### Task Packet 与角色调用

Root 在委派前形成清晰的 Task Packet：Objective、Relevant evidence、In scope、Out of scope、Writable ownership、Constraints、Acceptance criteria、Required validation、Expected return、Escalation conditions。

先判断工作属于执行还是决策，再根据 ambiguity、solution-path uncertainty、blast radius、failure cost、reversibility、verifiability 选择角色。Task size 不是 routing 标准。

只有 Root 能可靠执行并验证，且小任务、已有充分上下文或委派成本使本地执行更经济时，才由 Root 直接完成；能力条件优先于成本和任务大小。委派应带来成本、上下文隔离或并行效率收益；只有多个真正独立的 packets 才并行。

调用前检查当前工具是否提供 Custom Agent 角色选择及独立上下文能力；不支持时报告 runtime 不可用，不把文件安装成功当作模式可运行。

当前支持 `agent_type` 的接口使用以下形式（按任务替换角色）：

```json
{"agent_type":"sol-worker","fork_turns":"none","message":"明确的 Task Packet"}
```

固定角色的 model / effort 由 TOML 决定，不同时传入 model 或 reasoning_effort 覆盖值。完整历史 fork 可能继承 Root 设置，不能用来验证这些角色的模型分工。其他客户端只使用其已确认等价的角色调用方式；没有等价入口时报告不兼容。

只传必要证据和任务边界。角色不可用时报告缺失；只有 Root 能可靠完成并验证且符合所选模式时才由 Root 接手，并明确记录。不得用模型不明的 generic/default agent 冒充已配置角色。


### 升级与阻塞

Root 可以直接选择合适层级，无需先调用 Luna、再 Sol、最后 Astra。高失败代价且歧义显著的问题，可直接咨询 Astra；普通局部问题无需例行咨询最高层模型。

Worker 遇到范围扩大、事实与 packet 冲突、系统级决策或无法可靠验证时，返回具体证据、已尝试方法和阻塞给 Root。Root 决定补充调查、修改 packet、换 worker 或咨询 advisor。重复失败是重新诊断的信号，不自动触发模型升级。

工具不可用、权限不足或缺少用户事实时，先解决对应阻塞；更强模型不能替代缺失的权限、工具或事实。遵守当前运行环境的权限与指令优先级。

Worker 和 advisor 不自行创建或升级其他 agent；路由权集中在 Root。

### Advisor Contract

咨询包含：一个明确 Decision question、Relevant evidence、Constraints / non-negotiables、Options considered、Expected return。

Advisor 使用只读检查，返回 recommendation、decisive evidence、alternatives / trade-offs、risks、implementation constraints、acceptance criteria、remaining uncertainty。证据不足时指出最小补充检查；不假装已有结论。

顾问意见返回 Root，由 Root 按实现难度选择自己或 worker 执行。Advisor 不接管调度、实现、集成或最终验收；再次咨询必须有新的证据或明确未解决的决策问题。

### 并行与验收

并行 packet 必须独立、不依赖对方未完成的输出、写入范围不重叠、每个文件仅一个 active writer，并能分别验证。Root 可混合调度不同 worker，但始终负责集成。

Worker completion ≠ task completion。Root 检查实际 diff、验证结果和证据，解决冲突，完成适当的集成验证，作出 Accept / Reject / Rework。Advisor 的建议不能代替验证。阻塞或未解决的高风险判断必须如实报告。

### Effort 与有效权限

本版使用固定角色档位，不执行按任务动态 effort 路由。用户要求调整子角色档位时，应修改该角色的 TOML，并同步本项目映射和验证预期，重新加载后检查实际 effort；提示词中的“多想一点”不能代替配置，调用参数也不能保证覆盖 TOML。只选择当前客户端与模型均支持的值。`ultra` 等可能附带自动委派的档位不属于本版基线，验证其与 Root 集中调度兼容后才能另行采用。

Advisor 的“不写入”行为约束与运行时强制只读是两个检查项。父会话的实时权限设置可能覆盖角色 TOML 的 sandbox_mode。首次使用或权限变更后，先做不使用工具、不携带敏感内容的元数据握手；Root 核对关联子会话的 model、effort、有效 sandbox/approval 元数据。有效文件沙箱不是 read-only，或无法确认时，不继续派发实质咨询，报告权限 mismatch / 未验证。可在支持独立只读权限的环境或独立只读会话中重新验证；不自动修改全局权限，不把独立会话测试当作已验证 Custom Agent 路由。Shell 沙箱也不能证明所有外部连接器都只读；顾问仍只使用只读操作。

### Runtime Truth

TOML 和 AGENTS.md 只表达意图；实际模型与推理档位以 runtime/session/Agent Activity 为准。检查 Root 所选 profile 和实际调用过的角色；未调用的角色仍为“未验证 runtime”。无法读取运行证据时也明确标注未验证，不得以静态配置推断成功。

以下档位是迁移基线，不是已证实的最优组合。评估时分别记录模型、reasoning effort、任务质量、耗时、Token 和返工。子 agent 的 reasoning 必须由角色配置或受支持的显式参数指定，不依赖隐式继承。

## 验收与报告

确认只有一个 architecture marker、一个选定 Root profile，模型/档位映射与有效角色权限正确（不能只检查 TOML 声明），路由和验收归 Root，worker/advisor 无递归委派。检查所有规则符合所选模式且旧角色禁用条款已清理。报告修改位置、删除的冲突规则、最终 routing graph、diff，以及实际 runtime 证据或缺失情况。区分静态配置检查与实际运行时验证。
