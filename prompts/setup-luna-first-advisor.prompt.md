# One-shot Setup — Luna-first / Cheap Orchestrator + Strong Advisor

**简体中文** | [English](en/setup-luna-first-advisor.prompt.md)

把下面整段内容直接交给 Codex，并在你希望启用该模式的项目根目录中执行。

---

请在当前项目启用 **Codex Model Routing — Luna-first / Cheap Orchestrator + Strong Advisor** 模式。

目标有两个：

1. 把本项目依赖的三个 Custom Agents 安装到当前用户的全局 `~/.codex/agents/`；
2. 在当前仓库中按照 Luna-first / Strong Advisor 规则创建或更新 `AGENTS.md` 的 routing policy。

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

## Step 2 — 在当前项目应用 Luna-first / Strong Advisor routing policy

只修改当前项目根目录的 `AGENTS.md` routing layer；不要重新设计已有 engineering workflow。

不要修改 `CODING_ENGINEERING_REQUIREMENTS.md`、Skills、worktree、TDD、testing、debugging、review、Git workflow 或其他方法论文档，除非只是解决与 routing policy 的直接冲突。

### Architecture Exclusivity

在 routing section 中加入唯一标识：

`<!-- ROUTING_ARCHITECTURE: LUNA_FIRST_STRONG_ADVISOR -->`

完整检查现有 `AGENTS.md`。

如果发现任何与本模式冲突的 routing architecture，包括但不限于：

- Sol High Root orchestration；
- Strong Orchestrator；
- LOW / MEDIUM / HIGH → Luna / Sol Medium / Root routing；
- `sol-worker` 自动 routing；
- Sol 作为永久 supervisor / final acceptance owner；
- 其他 `ROUTING_ARCHITECTURE` marker；

不要兼容、叠加或保留。必须删除或替换冲突的 Agent Routing section。

最终只能存在 `LUNA_FIRST_STRONG_ADVISOR` 一种 routing architecture。

### Runtime Assumption

本模式要求 Primary / Root Agent 运行：

`gpt-5.6-luna / max`

Primary Luna 是 daily primary model、normal orchestrator、normal executor、worker scheduler、integration owner、normal final acceptance owner。

如果实际 runtime 不是 Luna Max，不要声称本模式已经正确运行；报告 mismatch，但不要自行修改 Codex 全局配置。

### Available Routing Agents

自动 routing 只使用：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`, read-only

即使 `sol-worker` 已安装，也不得成为本模式的自动 routing role；除非用户显式要求，否则不要调用。

### Core Philosophy

**Sol is an on-demand advisor, not the default supervisor.**

不要因为任务长、文件多、工作量大或测试多就升级 Sol。Difficulty ≠ Size。

Sol escalation 主要根据 uncertainty、ambiguity、blast radius、reversibility、plausible failure cost、reasoning difficulty、security / integrity impact。

### Three Routing Modes

#### LUNA_LOCAL

requirements 清晰、风险低到中等、单线程更经济、delegation overhead 大于收益时，Primary Luna 自己完成并验证。不要为了“使用 Agent”而 spawn worker。

#### LUNA_PARALLEL

存在至少两个 genuinely independent、disjoint、separately verifiable 的 task packets，并行有实际收益时，调用 `luna-worker`。

每个 packet 必须具备明确 objective、scope、writable ownership、acceptance criteria、validation。每个 writable file 只能有一个 active owner。Primary Luna 最终 integration / normal acceptance。

#### SOL_ADVISED

只有真正高价值 Judgment 才调用 `sol-advisor`。

典型升级条件：targeted inspection 后 requirements 仍 materially ambiguous / contradictory；architecture；security / privacy；authentication / authorization；cryptography / payments；destructive migration；data integrity；distributed consistency；breaking compatibility；cross-system interface decisions；cheap discriminating checks 后仍有多个 plausible root causes；两次 evidence-based attempts 失败；final validation 暴露高代价 unresolved risk。

不要让 Sol Advisor “完成整个功能”“review everything”或接管 routine implementation。

### Sol Advisor Contract

Primary Luna 在咨询 Sol 前先收集尽量便宜的 evidence。

交给 `sol-advisor` 的 request 应包含：one Decision question、Relevant evidence、Constraints / non-negotiables、Options considered（如有）、Expected return。

Expected return：recommendation、rationale / decisive evidence、rejected alternatives、risks、implementation constraints、acceptance criteria、remaining uncertainty。

如果 evidence 不够，Sol 只指出 cheapest additional check。

### Return Execution to Luna

Sol Advisor 给出 decision 后，常规执行必须立即返回 Luna：

```text
Luna collects evidence
        ↓
sol-advisor
        ↓
decision / constraints / acceptance criteria
        ↓
Luna or luna-worker implements
        ↓
validation
        ↓
Primary Luna integrates / accepts
```

Sol 不进行 routine coding、tests、integration、normal final acceptance。只有最终 artifact 仍存在 high-risk unresolved judgment 时，才允许针对性再次咨询 Sol。

### Parallelism / Task Packet

积极使用 `luna-worker`，但只在 genuinely independent work 值得并行时。

所有 delegated packet 尽可能包含：Objective、Relevant context、In scope、Out of scope、Writable ownership、Constraints、Acceptance criteria、Required validation、Expected return、Escalation conditions。

Worker 遇到 ambiguity、repo facts conflict、unexpected interface/dependency change、security/data-integrity/compatibility impact、validation unavailable、material scope expansion、repeated evidence-based failure 时必须停止返回。

### Acceptance

Primary Luna owns normal integration / review / verification / final acceptance。

必须检查 actual diffs、actual validation、worker evidence；不要只接受 summary。Sol Advisor 只对明确咨询的 difficult decision 负责。

### Explicitly Forbidden Routing

禁止自动形成：Root Sol High → workers；Luna → sol-worker Medium → Sol High Root；sol-worker 自动 routing；Sol Advisor → routine implementation；Sol permanent supervisor。

正常拓扑只能是：

```text
Primary Luna Max
├── LUNA_LOCAL
├── luna-worker / Luna Max
└── sol-advisor / Sol High
        ↓
     decision only
        ↓
Primary Luna / luna-worker executes
```

### Runtime Truth

TOML / `AGENTS.md` 只能表达预期配置，不能证明实际模型运行。

预期：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`

如果能够读取 Codex session / Agent Activity / JSONL，请验证实际 `model` 和 `reasoning_effort`；如果不能验证，就明确写“未验证 runtime”，不要假装成功。

## Step 3 — 最终校验与报告

完成后确认：

- `~/.codex/agents/` 中三个 Agent 文件均存在；
- 当前项目 Primary / Root 预期为 Luna Max；
- normal local work = Primary Luna；
- independent parallel work = `luna-worker`；
- difficult judgment = `sol-advisor`；
- Sol decision 后 execution 返回 Luna；
- `sol-worker` 不在自动 routing graph；
- 没有 Sol High permanent supervisor；
- 没有 recursive delegation；
- 当前 `AGENTS.md` 只有一个 routing architecture marker；
- 非 routing 的工程规则没有被无关改写。

最后报告：Agent 安装结果、`AGENTS.md` 修改位置、删除的冲突规则、最终 routing graph、Sol escalation gates、实际 diff，以及能够验证到的 runtime model 信息。
