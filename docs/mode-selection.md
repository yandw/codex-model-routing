# Choosing an Orchestration Mode

这两种模式不是竞争关系，而是不同的工作习惯。

## Strong Orchestrator

更适合：

- 希望主 Agent 始终维持高判断力；
- 需求 / 架构变化较多；
- Root 需要持续做拆解与验收；
- 更关注稳健性和主控一致性；
- 愿意为 Root Sol High 持续付出更多 compute / credits。

核心：

> Strong model controls the work; cheaper workers execute bounded packets.

## Luna-first Advisor

更适合：

- 大多数日常任务本身不复杂；
- 机械实现、测试、探索占比高；
- 成本敏感；
- 希望 Sol 的额度集中用于 architecture / security / high-impact judgment；
- Luna 有能力承担普通 integration / acceptance。

核心：

> Cheap model controls normal work; strong model is consulted only for expensive decisions.

## Do not mix both policies in one AGENTS.md

混合后的典型问题：

- Root ownership 不清楚；
- Sol Advisor 与 Root Sol High 职责重叠；
- `sol-worker` 与 `sol-advisor` escalation 条件冲突；
- final acceptance ownership 冲突；
- 同一个任务可能命中多个 routing rule。

因此项目级 `AGENTS.md` 应明确选择一个 architecture marker，并移除另一套 routing policy。
