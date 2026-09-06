# Research Notes

## 研究问题

这项研究关注 Codex multi-agent 中一个比“选哪个模型”更重要的问题：

> 如何通过 orchestration policy，把不同成本 / 推理能力的模型组织成稳定的 coding workflow？

## 关键发现

### 1. Agent TOML 与 AGENTS.md 的职责不同

- `agents/*.toml`：定义可调用角色、model、reasoning effort、sandbox 与角色 instructions。
- `AGENTS.md`：定义当前项目如何拆任务、什么时候调用哪个 Agent、什么时候升级、谁负责 integration / acceptance。

因此，同一套 Agent Pool 可以支撑不同的工作方式。

### 2. Vox 路线提供了 Strong Orchestrator 的重要启发

讨论中的核心思路是：

- 主线程保持强推理能力；
- 对边界明确、可验证的工作使用 Luna Max worker；
- 不要因为任务是 sub-agent task 就默认复制昂贵的主模型；
- worker 任务必须有明确的 scope / deliverable / validation。

在本研究中进一步抽象出：

- LOW → Luna Max
- MEDIUM → Sol Medium worker
- HIGH → Root Sol High

`sol-worker` 是本研究为了填补“bounded but reasoning-heavy execution”而增加的中间层。

### 3. BruceLanLan 路线完整实现了 Luna-first + Sol Advisor

BruceLanLan/sol-luna-engineering-workflow 的核心结构：

- Primary = Luna Max；
- 普通工作 Luna 自己完成；
- independent packets → Luna workers；
- difficult judgment → Sol High Advisor；
- Sol Advisor read-only，只回答明确 decision question；
- Sol 给完 decision / constraints / acceptance criteria 后，执行返回 Luna。

项目还明确强调：

- Difficulty is not size；
- parallel task 必须 file ownership disjoint；
- delegated task 应有结构化 task packet；
- runtime evidence 才能证明模型实际被调用。

## 两种模式不是竞争关系

### Strong Orchestrator

像“资深架构师亲自带队”：

- Root 很强；
- Root 持续规划 / 判断 / 验收；
- worker 根据认知复杂度分层执行。

### Luna-first Advisor

像“高效执行团队 + 按需专家咨询”：

- Luna 负责日常 orchestration / execution；
- Sol 只在高价值判断时出现；
- Sol 的输出是 decision，而不是 implementation。

它们应当作为 **两种不同的工作习惯 / orchestration modes** 存在，而不是一个模式必须战胜另一个模式。

## 共同原则

### Difficulty ≠ Size

任务大小不能直接决定模型层级。

更重要的 routing signals：ambiguity、solution uncertainty、blast radius、reversibility、plausible error cost、security / data integrity、verifiability。

### Delegation Contract / Task Packet

一个好的 worker packet 至少应尽可能明确：

1. Objective
2. Relevant context
3. In scope
4. Out of scope
5. Writable ownership
6. Constraints
7. Acceptance criteria
8. Required validation
9. Expected return
10. Escalation conditions

### No recursive delegation by default

worker 不应该自行构建新的 Agent hierarchy。需要更高能力时，worker 返回 evidence / blocker，由 orchestrator 重新判断并决定 re-scope / escalate / take over。

### Runtime Truth

静态配置只能说明 intent，不能说明实际 execution。

应通过 Codex App session JSONL / Agent Activity 检查真实：`thread_source`、agent role / nickname、`model`、`reasoning_effort`。

## Sources

- Vox: https://x.com/Voxyz_ai/status/2083583538830410127
- Lonely__MH: https://x.com/Lonely__MH/status/2083762211449684344
- BruceLanLan: https://github.com/BruceLanLan/sol-luna-engineering-workflow
