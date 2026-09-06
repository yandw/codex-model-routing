# Generate / Modify AGENTS.md — Strong Orchestrator Mode

> Language: **中文** | [English](en/strong-orchestrator-agents-md.prompt.md)

请修改当前项目根目录的 `AGENTS.md`，建立一套严格的 **Strong Orchestrator** Agent / Model Routing Architecture。

本次修改只负责 Agent / Model Routing Layer，不重新设计项目已有的 engineering workflow。

不要修改 `CODING_ENGINEERING_REQUIREMENTS.md`、Skills、worktree、TDD、testing、debugging、review、Git workflow 或其他方法论文档，除非只是解决与 routing policy 的直接冲突。

## 1. Architecture Exclusivity

在 routing section 中加入唯一标识：

`<!-- ROUTING_ARCHITECTURE: STRONG_ORCHESTRATOR -->`

完整检查现有 `AGENTS.md`。

如果发现任何与本模式冲突的 routing architecture，包括但不限于：

- Luna-first primary orchestration；
- Cheap Orchestrator + Strong Advisor；
- `LUNA_LOCAL` / `LUNA_PARALLEL` / `SOL_ADVISED`；
- Luna 作为 Root / Primary orchestrator；
- `sol-advisor` 作为默认自动 escalation path；
- 其他 `ROUTING_ARCHITECTURE` marker；

不要兼容、叠加或保留。

必须删除或替换冲突的 Agent Routing section。

最终只能存在 `STRONG_ORCHESTRATOR` 一种 routing architecture。

保留所有与 routing 无冲突的工程规则。

## 2. Runtime Assumption

本模式要求 Root Agent 运行：

`gpt-5.6-sol / high`

Root 是唯一 orchestrator 和最终责任主体。

如果实际 runtime 不是 Sol High，不要声称本模式已经正确运行；报告 mismatch，但不要自行修改 Codex 全局配置。

## 3. Available Routing Agents

自动 routing 只使用：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

即使 `sol-advisor` 存在于全局 Agent Pool，也不得成为本模式的默认自动 routing role；除非用户显式要求，否则不要调用。

## 4. Root Responsibilities

Root Sol High 始终负责：

- requirement understanding / clarification；
- constraints；
- planning；
- task decomposition；
- dependency analysis；
- architecture；
- routing；
- parallelization；
- escalation；
- worker result evaluation；
- integration；
- conflict resolution；
- final review；
- final verification；
- acceptance / rejection；
- 最终用户输出。

## 5. Routing Model

根据 cognitive complexity、ambiguity、solution-path uncertainty、blast radius、risk、reversibility、verifiability 选择执行主体：

```text
                    Root Sol High
                         │
                   Plan / Decompose
                         │
             ┌───────────┼───────────┐
             │           │           │
            LOW        MEDIUM       HIGH
             │           │           │
             ▼           ▼           ▼
      luna-worker    sol-worker      Root
       Luna Max      Sol Medium    Sol High
```

### LOW → luna-worker

满足大部分以下条件时显式调用 `luna-worker`：

- objective 清晰；
- scope 清晰；
- relevant files 基本已知；
- solution path 基本清晰；
- acceptance criteria 明确；
- architecture impact 低；
- 可以独立执行；
- 可以客观验证。

典型任务：repository exploration、targeted search、evidence collection、mechanical / repetitive edits、bounded implementation、小型 bug fix、targeted tests、lint、type-check、build、documentation、bounded review。

判断口诀：

> Tell it what to do, and that is mostly enough.

### MEDIUM → sol-worker

满足以下特征时显式调用 `sol-worker`：

- objective / scope 已 bounded；
- 但 solution path 不明显；
- 需要跨多个相关文件 / 模块理解；
- root cause 需要较强推理；
- 需要理解 existing abstractions / design intent；
- 存在多个局部实现方案；
- integration complexity 中等；
- 仍属于可独立委派的 execution work。

判断口诀：

> Tell it what to do, but it still needs to reason carefully about how to do it.

### HIGH → Root Sol High

以下任务保留给 Root：

- requirement ambiguity；
- architecture / system design；
- high-impact strategy；
- public API / schema decisions；
- security-sensitive judgment；
- destructive / irreversible decisions；
- unknown blast radius；
- conflicting requirements；
- broad refactor decisions；
- task decomposition；
- worker conflict resolution；
- integration；
- final review / acceptance。

判断口诀：

> If deciding what should be done, why, or what the system-level consequences are is itself the hard problem, keep it on Root.

## 6. Task Packet

Root 在委派前先形成 bounded Task Packet，尽可能包含：

- Objective
- Relevant context
- In scope
- Out of scope
- Writable files
- Constraints
- Acceptance criteria
- Required validation
- Expected return
- Escalation conditions

Task size 不是 routing 标准。

## 7. Explicit Selection

当任务符合 `luna-worker` profile，必须优先显式选择 `luna-worker`。

当任务符合 `sol-worker` profile，必须优先显式选择 `sol-worker`。

不要 spawn generic/default Root copy 来替代已有 Custom Agent。

## 8. Escalation

Worker 不拥有 Model Routing 权限。

禁止 worker 自行：

`luna-worker → sol-worker`

正确流程：

```text
luna-worker
     ↓
unexpected complexity
     ↓
return evidence to Root
     ↓
Root reassesses
     ├── refine packet → luna-worker
     ├── bounded reasoning-heavy → sol-worker
     └── architecture / high judgment → Root
```

`sol-worker` 遇到 architecture-level decision、major scope expansion、security/data integrity、public API/schema 或 requirement ambiguity，也必须返回 Root。

默认禁止 recursive delegation。

## 9. Parallelism

只在以下条件下并行：

- 至少两个真正独立的 packets；
- 不依赖彼此 unfinished output；
- writable files disjoint；
- one writable owner per file；
- each packet independently verifiable；
- parallel benefit > coordination overhead。

允许混合多个 `luna-worker` / `sol-worker`，但 Root 始终拥有 scheduling 和 integration 权限。

## 10. Acceptance

Worker completion ≠ task completion。

Root 必须检查 actual changes、evidence、validation，解决冲突，并负责 integration-level verification 和最终 Accept / Reject / Rework。

不要只根据 worker summary 验收。

## 11. Runtime Truth

TOML / AGENTS.md 不能证明实际模型运行。

只有 runtime/session/Agent Activity 才是最终事实来源。

预期：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

如果实际不匹配，报告真实 runtime，不得假装成功。

## 12. Modification Rules

请：

1. 完整读取当前 `AGENTS.md`；
2. 定位 delegation / routing section；
3. 删除与 Strong Orchestrator 冲突的 routing architecture；
4. 生成一个简洁、高密度、可执行的 routing section；
5. 加入唯一 architecture marker；
6. 保留非 routing 的工程规则；
7. 使用最小必要 diff；
8. 不把本提示词全文原样复制进 `AGENTS.md`；
9. 不修改其他文件。

最终确认：

- Root = Sol High；
- LOW → luna-worker；
- MEDIUM → sol-worker；
- HIGH → Root；
- sol-advisor 不在默认 routing path；
- 没有 Luna-first routing；
- 没有 generic/default worker 优先规则；
- 没有 recursive delegation；
- 只有一个 routing architecture marker。

最后报告：修改位置、删除的冲突规则、最终 routing graph、diff、architecture exclusivity，以及实际能够验证到的 runtime model 信息。
