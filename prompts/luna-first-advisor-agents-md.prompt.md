# Generate / Modify AGENTS.md — Luna-first Advisor Mode

> Language: **中文** | [English](en/luna-first-advisor-agents-md.prompt.md)

请修改当前项目根目录的 `AGENTS.md`，建立一套严格的 **Luna-first / Cheap Orchestrator + Strong Advisor** Agent / Model Routing Architecture。

本次修改只负责 Agent / Model Routing Layer，不重新设计项目已有的 engineering workflow。

不要修改 `CODING_ENGINEERING_REQUIREMENTS.md`、Skills、worktree、TDD、testing、debugging、review、Git workflow 或其他方法论文档，除非只是解决与 routing policy 的直接冲突。

## 1. Architecture Exclusivity

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

不要兼容、叠加或保留。

必须删除或替换冲突的 Agent Routing section。

最终只能存在 `LUNA_FIRST_STRONG_ADVISOR` 一种 routing architecture。

保留与 routing 无冲突的工程规则。

## 2. Runtime Assumption

本模式要求 Primary / Root Agent 运行：

`gpt-5.6-luna / max`

Primary Luna 是：daily primary model、normal orchestrator、normal executor、worker scheduler、integration owner、normal final acceptance owner。

如果实际 runtime 不是 Luna Max，不要声称本模式已经正确运行；报告 mismatch，但不要自行修改 Codex 全局配置。

## 3. Available Routing Agents

自动 routing 只使用：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`, read-only

即使 `sol-worker` 存在于全局 Agent Pool，也不得成为本模式的自动 routing role；除非用户显式要求，否则不要调用。

## 4. Core Philosophy

Sol is an on-demand advisor, not the default supervisor.

不要因为任务长、文件多、工作量大或测试多就升级 Sol。Difficulty ≠ Size。

Sol escalation 主要根据 uncertainty、ambiguity、blast radius、reversibility、plausible failure cost、reasoning difficulty、security / integrity impact。

## 5. Three Routing Modes

### LUNA_LOCAL

如果 requirements 清晰、风险低到中等、单线程更经济、delegation overhead 大于收益，则 Primary Luna 自己完成并验证。不要为了“使用 Agent”而 spawn worker。

### LUNA_PARALLEL

如果存在至少两个 genuinely independent、disjoint、separately verifiable 的 task packets，并行能产生实际收益，则调用 `luna-worker`。

每个 packet 必须具备明确 objective、scope、writable ownership、acceptance criteria、validation。每个 writable file 只能有一个 active owner。Primary Luna 最终 integration / normal acceptance。

### SOL_ADVISED

只有真正高价值 Judgment 才调用 `sol-advisor`。

典型升级条件：targeted inspection 后 requirements 仍 materially ambiguous / contradictory；architecture；security / privacy；authentication / authorization；cryptography / payments；destructive migration；data integrity；distributed consistency；breaking compatibility；cross-system interface decisions；cheapest discriminating checks 后仍有多个 plausible root causes；两次 evidence-based attempts 失败；final validation 暴露高代价 unresolved risk。

不要让 Sol Advisor “完成整个功能”“review everything”或接管 routine implementation。

## 6. Sol Advisor Contract

Primary Luna 在咨询 Sol 前先收集尽量便宜的 evidence。

交给 `sol-advisor` 的 request 应包含：one Decision question、Relevant evidence、Constraints / non-negotiables、Options considered（如有）、Expected return。

Expected return：recommendation、rationale / decisive evidence、rejected alternatives、risks、implementation constraints、acceptance criteria、remaining uncertainty。

如果 evidence 不够，Sol 只指出 cheapest additional check。

## 7. Return Execution to Luna

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

## 8. Luna Parallelism

积极使用 `luna-worker`，但只在 genuinely independent work 值得并行时。

必须满足：no dependency on unfinished output、explicit scope、explicit acceptance criteria、disjoint writable files、one writable owner per file、Primary Luna can integrate / validate。

不要为 trivial task spawn agents。

## 9. Task Packet

所有 delegated packet 尽可能包含：

- Objective
- Relevant context
- In scope
- Out of scope
- Writable ownership
- Constraints
- Acceptance criteria
- Required validation
- Expected return
- Escalation conditions

Worker 遇到 ambiguity、repo facts conflict、unexpected interface/dependency change、security/data-integrity/compatibility impact、validation unavailable、material scope expansion、repeated evidence-based failure 时必须停止返回。

## 10. Acceptance

Primary Luna owns normal integration / review / verification / final acceptance。

必须检查 actual diffs、actual validation、worker evidence；不要只接受 summary。Sol Advisor 只对明确咨询的 difficult decision 负责。

## 11. Explicitly Forbidden Routing

本模式禁止自动形成：Root Sol High → workers；Luna → sol-worker Medium → Sol High Root；sol-worker 自动 routing；Sol Advisor → routine implementation；Sol permanent supervisor。

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

## 12. Runtime Truth

TOML / AGENTS.md 不能证明实际模型运行。只有 runtime/session/Agent Activity 才是最终事实来源。

预期：

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`

如果实际不匹配，报告真实 runtime，不得假装成功。

## 13. Modification Rules

请：

1. 完整读取当前 `AGENTS.md`；
2. 定位 delegation / routing section；
3. 删除与 Luna-first / Strong Advisor 冲突的 routing architecture；
4. 生成一个简洁、高密度、可执行的 routing section；
5. 加入唯一 architecture marker；
6. 保留非 routing 的工程规则；
7. 不加入 Strong Orchestrator compatibility；
8. 不加入 sol-worker 自动 routing；
9. 使用最小必要 diff；
10. 不把本提示词全文原样复制进入 `AGENTS.md`；
11. 不修改其他文件。

最终确认：Primary = Luna Max；normal work = Luna；independent parallel work = luna-worker；difficult judgment = sol-advisor；Sol decision 后 execution 返回 Luna；sol-worker 不在自动 routing graph；没有 Sol High permanent supervisor；只有一个 routing architecture marker。

最后报告：修改位置、删除的冲突规则、最终 routing graph、Sol escalation gates、diff、architecture exclusivity，以及实际能够验证到的 runtime model 信息。
