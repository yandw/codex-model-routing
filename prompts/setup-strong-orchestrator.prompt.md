# One-shot Setup — Strong Orchestrator

**简体中文** | [English](en/setup-strong-orchestrator.prompt.md)

把下面整段内容直接交给 Codex，并在你希望启用该模式的项目根目录中执行。

---

请在当前项目启用 **Codex Model Routing — Strong Orchestrator** 模式。

目标有两个：

1. 把本项目依赖的三个 Custom Agents 安装到当前用户的全局 `~/.codex/agents/`；
2. 在当前仓库中按照 Strong Orchestrator 规则创建或更新 `AGENTS.md` 的 routing policy。

请按下面顺序执行，不要跳步。

## Step 1 — 安装 / 更新 Custom Agents

只安装下面三个文件，不要删除或覆盖 `~/.codex/agents/` 中其他无关 Agent：

- `luna-worker.toml`
- `sol-worker.toml`
- `sol-advisor.toml`

来源固定为：

- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/luna-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-advisor.toml`

推荐命令：

```bash
mkdir -p ~/.codex/agents
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/luna-worker.toml -o ~/.codex/agents/luna-worker.toml
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-worker.toml -o ~/.codex/agents/sol-worker.toml
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-advisor.toml -o ~/.codex/agents/sol-advisor.toml
```

安装后确认三个文件存在。不要把路径安装成 `~/.codex/agents/agents/...`。

## Step 2 — 在当前项目应用 Strong Orchestrator routing policy

只修改当前项目根目录的 `AGENTS.md` routing layer；不要重新设计已有 engineering workflow。

不要修改 `CODING_ENGINEERING_REQUIREMENTS.md`、Skills、worktree、TDD、testing、debugging、review、Git workflow 或其他方法论文档，除非只是解决与 routing policy 的直接冲突。

### Architecture Exclusivity

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

不要兼容、叠加或保留。必须删除或替换冲突的 Agent Routing section。

最终只能存在 `STRONG_ORCHESTRATOR` 一种 routing architecture。

### Runtime Assumption

本模式要求 Root Agent 运行：

`gpt-5.6-sol / high`

Root 是唯一 orchestrator 和最终责任主体。

如果实际 runtime 不是 Sol High，不要声称本模式已经正确运行；报告 mismatch，但不要自行修改 Codex 全局配置。

### Available Routing Agents

自动 routing 只使用：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

即使 `sol-advisor` 已安装，也不得成为本模式的默认自动 routing role；除非用户显式要求，否则不要调用。

### Root Responsibilities

Root Sol High 始终负责：requirement understanding / clarification、constraints、planning、task decomposition、dependency analysis、architecture、routing、parallelization、escalation、worker result evaluation、integration、conflict resolution、final review、final verification、acceptance / rejection，以及最终用户输出。

### Routing Model

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

#### LOW → luna-worker

用于 objective、scope、相关文件、solution path、acceptance criteria 基本明确，architecture impact 低，并且可客观验证的 bounded execution。

典型任务：repository exploration、targeted search、evidence collection、mechanical edits、bounded implementation、小型 bug fix、targeted tests、lint、type-check、build、documentation、bounded review。

判断：**Tell it what to do, and that is mostly enough.**

#### MEDIUM → sol-worker

用于 objective / scope 已 bounded，但 solution path 不明显，需要跨文件理解、复杂 debugging、root-cause analysis、理解 existing abstractions / design intent，或需要局部工程判断的执行任务。

判断：**Tell it what to do, but it still needs to reason carefully about how to do it.**

#### HIGH → Root Sol High

以下任务保留给 Root：requirement ambiguity、architecture / system design、high-impact strategy、public API / schema decisions、security-sensitive judgment、destructive / irreversible decisions、unknown blast radius、conflicting requirements、broad refactor decisions、task decomposition、worker conflict resolution、integration、final review / acceptance。

判断：**If deciding what should be done, why, or what the system-level consequences are is itself the hard problem, keep it on Root.**

### Task Packet

Root 委派前应形成 bounded Task Packet，尽可能包含：Objective、Relevant context、In scope、Out of scope、Writable files、Constraints、Acceptance criteria、Required validation、Expected return、Escalation conditions。

Task size 不是 routing 标准。

### Explicit Selection

符合 `luna-worker` profile 时，优先显式选择 `luna-worker`；符合 `sol-worker` profile 时，优先显式选择 `sol-worker`。不要 spawn generic/default Root copy 替代已有 Custom Agent。

### Escalation

Worker 不拥有 Model Routing 权限。

禁止 worker 自行 `luna-worker → sol-worker`。

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

### Parallelism

只在至少两个 task packets 真正独立、不依赖彼此 unfinished output、writable files disjoint、one writable owner per file、each packet independently verifiable，且并行收益大于协调成本时并行。

### Acceptance

Worker completion ≠ task completion。

Root 必须检查 actual changes、evidence、validation，解决冲突，并负责 integration-level verification 和最终 Accept / Reject / Rework。不要只根据 worker summary 验收。

### Runtime Truth

TOML / `AGENTS.md` 只能表达预期配置，不能证明实际模型运行。

预期：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

如果能够读取 Codex session / Agent Activity / JSONL，请验证实际 `model` 和 `reasoning_effort`；如果不能验证，就明确写“未验证 runtime”，不要假装成功。

## Step 3 — 最终校验与报告

完成后确认：

- `~/.codex/agents/` 中三个 Agent 文件均存在；
- 当前项目 Root 预期为 Sol High；
- LOW → `luna-worker`；
- MEDIUM → `sol-worker`；
- HIGH → Root；
- `sol-advisor` 不在默认 routing path；
- 没有 Luna-first routing；
- 没有 recursive delegation；
- 当前 `AGENTS.md` 只有一个 routing architecture marker；
- 非 routing 的工程规则没有被无关改写。

最后报告：Agent 安装结果、`AGENTS.md` 修改位置、删除的冲突规则、最终 routing graph、实际 diff，以及能够验证到的 runtime model 信息。
