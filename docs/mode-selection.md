# Choosing an Orchestration Mode

GPT-6 迁移基线，runtime 尚待验证。保留两种模式，每个项目只选一种；Strong Orchestrator 中的 Sol / Astra 是两个 Root profile。

| 需求 | 推荐模式 / Root | 执行与判断 |
|---|---|---|
| 主线程持续负责规划、架构与集成，兼顾成本 | Strong Orchestrator / `gpt-6.1-sol / high` | Luna 清晰执行、Sol 复杂执行、Astra 按需重大判断 |
| 希望最高能力模型持续掌握上下文 | Strong Orchestrator / `gpt-6-astra / high` | Luna / Sol 执行，Root 自己处理最高难度判断 |
| 日常任务明确，关注成本，Luna 能可靠验收 | Luna-first / `gpt-6-luna / max` | Luna 日常执行、Sol 复杂执行或局部咨询、Astra 按需重大判断 |

这些选择是待实测的设计建议，不保证哪种模式总是更快或更便宜。比较完整任务的质量、Token、耗时和返工，而不是只比较模型名称或单次 Token 单价。

## 共同边界

- 执行难度决定 worker；决策难度决定 advisor。
- 只有 Root 能可靠执行和验证，且小任务或充分上下文使本地完成更经济时，才本地完成。
- Sol worker 可执行单个独立任务，不以并行为前提。
- Root 直接选择合适层级，不要求按 Luna → Sol → Astra 顺序升级。
- 两种模式都由 Root 调度和验收。Advisor 只读、提供建议，不接管工程执行。
- Astra Root 不例行再调用 Astra advisor；Strong Orchestrator 不默认调用 Sol advisor。
- 缺少事实、权限或工具是对应阻塞，不应仅因此升级模型。
- `max / medium / high` 是初始基线，模型与 reasoning 档位分别评估。自定义 Root effort 需用户明确选择并记录。

## 升级现有 AGENTS.md

仅选择 `STRONG_ORCHESTRATOR` 或 `LUNA_FIRST_STRONG_ADVISOR` 一个 marker，并记录一个 Root model / reasoning profile。替换整个旧 routing section，保留无冲突的工程规则。

即使 marker 没变，也必须清理旧模型映射。Luna-first 还需移除禁止 `sol-worker` 和强制所有实现返回 Luna 模型的旧规则。不要混合两套 Root ownership。

TOML 安装、当前会话角色注册和真实 runtime 是三个不同检查项。修改提示词不能切换当前线程的模型；发现不匹配时报告，按客户端要求选择正确模型或重新加载会话，再验证。

English: choose one mode and one Root profile. Execution and judgment use separate roles; Root retains acceptance. The new baseline is runtime-unverified. See the [English README](../README.en.md) and [English prompts](../prompts/en/strong-orchestrator-agents-md.prompt.md).

权限前提：顾问 TOML 的 read-only 必须与实际子会话 sandbox 一起核验。父权限覆盖或无法确认时，停止实质咨询并报告受限。固定角色的 effort 由 TOML 决定，不能依赖调用参数覆盖。
