# One-shot Setup — Luna-first / Cheap Orchestrator + Strong Advisor

[简体中文](../setup-luna-first-advisor.prompt.md) | **English**

Paste the full prompt below into Codex while you are in the root of the project where you want to enable this mode.

---

Enable **Codex Model Routing — Luna-first / Cheap Orchestrator + Strong Advisor** for the current project.

You have two goals:

1. install the three required Custom Agents into the current user's global `~/.codex/agents/` directory;
2. create or update the current repository's `AGENTS.md` routing policy for Luna-first / Strong Advisor mode.

Execute the following steps in order.

## Step 1 — Install / update Custom Agents

Install only these three files. Do not delete or overwrite unrelated agents already present in `~/.codex/agents/`:

- `luna-worker.toml`
- `sol-worker.toml`
- `sol-advisor.toml`

Use these exact sources:

- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/luna-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-advisor.toml`

Recommended commands:

```bash
mkdir -p ~/.codex/agents
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/luna-worker.toml -o ~/.codex/agents/luna-worker.toml
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-worker.toml -o ~/.codex/agents/sol-worker.toml
curl -fsSL https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-advisor.toml -o ~/.codex/agents/sol-advisor.toml
```

After installation, verify all three files exist directly under `~/.codex/agents/`. Do not create `~/.codex/agents/agents/...`.

## Step 2 — Apply Luna-first / Strong Advisor routing to this project

Modify only the routing layer of the current project's root `AGENTS.md`. Do not redesign the project's existing engineering workflow.

Do not modify `CODING_ENGINEERING_REQUIREMENTS.md`, Skills, worktrees, TDD, testing, debugging, review, Git workflow, or methodology documents unless required only to remove a direct routing conflict.

### Architecture exclusivity

Add exactly one routing marker:

`<!-- ROUTING_ARCHITECTURE: LUNA_FIRST_STRONG_ADVISOR -->`

Inspect the complete existing `AGENTS.md`. Remove or replace conflicting routing architectures, including Sol High Root orchestration, Strong Orchestrator, LOW/MEDIUM/HIGH → Luna/Sol Medium/Root routing, automatic `sol-worker` routing, Sol as permanent supervisor/final owner, or any other routing marker.

The final file must contain only `LUNA_FIRST_STRONG_ADVISOR` while preserving non-conflicting engineering rules.

### Runtime assumption

The Primary / Root is expected to run:

`gpt-5.6-luna / max`

Primary Luna is the daily primary model, normal orchestrator, normal executor, worker scheduler, integration owner, and normal final acceptance owner.

If actual runtime is not Luna Max, report the mismatch and do not pretend the mode is active. Do not change global Codex model configuration automatically.

### Automatic routing agents

Use only:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`, read-only

Even though `sol-worker` is installed, it is not part of the automatic routing path unless the user explicitly requests it.

### Core philosophy

**Sol is an on-demand advisor, not the default supervisor.**

Do not escalate to Sol merely because a task is long, touches many files, requires many tests, or represents a large amount of work. Difficulty ≠ Size.

Escalate based on uncertainty, ambiguity, blast radius, reversibility, plausible failure cost, reasoning difficulty, and security/integrity impact.

### Three routing modes

#### LUNA_LOCAL

When requirements are clear, risk is low-to-medium, one thread is more efficient, and delegation overhead would exceed the benefit, Primary Luna should execute and validate the work directly.

#### LUNA_PARALLEL

When there are at least two genuinely independent, disjoint, separately verifiable task packets and parallelism creates real benefit, delegate them to `luna-worker` agents.

Each packet must have a clear objective, scope, writable ownership, acceptance criteria, and validation. Each writable file has only one active owner. Primary Luna performs final integration and normal acceptance.

#### SOL_ADVISED

Use `sol-advisor` only for high-value judgment.

Typical escalation gates: requirements remain materially ambiguous or contradictory after targeted inspection; architecture; security/privacy; authentication/authorization; cryptography/payments; destructive migration; data integrity; distributed consistency; breaking compatibility; cross-system interface decisions; multiple plausible root causes remain after cheap discriminating checks; two evidence-based attempts fail; or final validation reveals a high-cost unresolved risk.

Do not ask Sol Advisor to “implement the whole feature,” “review everything,” or take over routine execution.

### Sol Advisor contract

Primary Luna should gather the cheapest useful evidence before consulting Sol.

A Sol Advisor request should contain one explicit Decision question, Relevant evidence, Constraints/non-negotiables, Options considered when known, and Expected return.

Expected return: recommendation, decisive evidence/rationale, rejected alternatives, risks, implementation constraints, acceptance criteria, and remaining uncertainty. If evidence is insufficient, Sol should identify the cheapest additional check.

### Return execution to Luna

After Sol Advisor returns a decision, routine work must return immediately to Luna:

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

Sol does not own routine coding, tests, integration, or normal final acceptance. A second targeted Sol consultation is allowed only when high-risk unresolved judgment remains.

### Parallelism, task packets, and acceptance

Use `luna-worker` proactively only for genuinely independent work.

Delegated packets should contain as much as possible: Objective, Relevant context, In scope, Out of scope, Writable ownership, Constraints, Acceptance criteria, Required validation, Expected return, and Escalation conditions.

Workers must stop and return when they encounter material ambiguity, repository facts that contradict the packet, unexpected interface/dependency changes, security/data-integrity/compatibility implications, unavailable validation, material scope expansion, or repeated evidence-based failure.

Primary Luna owns normal integration, review, verification, and final acceptance. Inspect actual diffs, actual validation, and worker evidence rather than accepting summaries alone.

### Explicitly forbidden routing

Do not automatically create any of the following: Root Sol High → workers; Luna → sol-worker Medium → Sol High Root; automatic `sol-worker` routing; Sol Advisor → routine implementation; permanent Sol supervision.

The normal topology is:

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

### Runtime truth

TOML and `AGENTS.md` express intended configuration; they do not prove which model actually ran.

Expected runtime:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`

If Codex session / Agent Activity / JSONL metadata is available, verify actual `model` and `reasoning_effort`. If runtime cannot be verified, explicitly report that it is unverified.

## Step 3 — Final verification

Confirm:

- all three Agent files exist in `~/.codex/agents/`;
- Primary / Root is expected to be Luna Max;
- normal local work stays on Primary Luna;
- independent parallel work uses `luna-worker`;
- difficult judgment uses `sol-advisor`;
- execution returns to Luna after Sol's decision;
- `sol-worker` is not in the automatic routing graph;
- no permanent Sol supervisor remains;
- no recursive delegation rule exists;
- only one routing architecture marker remains in `AGENTS.md`;
- unrelated engineering rules were preserved.

Finally report: Agent installation result, `AGENTS.md` changes, removed routing conflicts, final routing graph, Sol escalation gates, actual diff, and any runtime model information you could verify.
