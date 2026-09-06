# One-shot Setup — Strong Orchestrator

[简体中文](../setup-strong-orchestrator.prompt.md) | **English**

Paste the full prompt below into Codex while you are in the root of the project where you want to enable this mode.

---

Enable **Codex Model Routing — Strong Orchestrator** for the current project.

You have two goals:

1. install the three required Custom Agents into the current user's global `~/.codex/agents/` directory;
2. create or update the current repository's `AGENTS.md` routing policy for Strong Orchestrator mode.

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

## Step 2 — Apply Strong Orchestrator routing to this project

Modify only the routing layer of the current project's root `AGENTS.md`. Do not redesign the project's existing engineering workflow.

Do not modify `CODING_ENGINEERING_REQUIREMENTS.md`, Skills, worktrees, TDD, testing, debugging, review, Git workflow, or methodology documents unless required only to remove a direct routing conflict.

### Architecture exclusivity

Add exactly one routing marker:

`<!-- ROUTING_ARCHITECTURE: STRONG_ORCHESTRATOR -->`

Inspect the complete existing `AGENTS.md`. Remove or replace conflicting routing architectures, including Luna-first orchestration, Cheap Orchestrator + Strong Advisor, `LUNA_LOCAL` / `LUNA_PARALLEL` / `SOL_ADVISED`, Luna as Root, `sol-advisor` as the default escalation path, or any other routing architecture marker.

The final file must contain only the `STRONG_ORCHESTRATOR` routing architecture while preserving non-conflicting engineering rules.

### Runtime assumption

The Root is expected to run:

`gpt-5.6-sol / high`

Root is the sole orchestrator and final owner. If actual runtime is not Sol High, report the mismatch and do not pretend the mode is active. Do not change global Codex model configuration automatically.

### Automatic routing agents

Use only:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

Even though `sol-advisor` is installed, it is not part of the default automatic routing path unless the user explicitly requests it.

### Root responsibilities

Root Sol High owns requirement understanding, clarification, constraints, planning, decomposition, dependency analysis, architecture, routing, parallelization, escalation, worker evaluation, integration, conflict resolution, final review, final verification, acceptance/rejection, and final user output.

### Routing model

Route by cognitive complexity, ambiguity, solution-path uncertainty, blast radius, risk, reversibility, and verifiability:

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

Use for bounded, low-ambiguity, objectively verifiable work where objective, scope, relevant files, solution path, and acceptance criteria are mostly explicit.

Typical work: repository exploration, targeted search, evidence collection, mechanical edits, bounded implementation, small bug fixes, targeted tests, lint, type-check, build, documentation, bounded review.

Heuristic: **Tell it what to do, and that is mostly enough.**

#### MEDIUM → sol-worker

Use when objective and scope are bounded but the implementation path requires meaningful engineering reasoning, cross-file understanding, difficult debugging, root-cause analysis, design-intent inference, or localized engineering judgment.

Heuristic: **Tell it what to do, but it still needs to reason carefully about how to do it.**

#### HIGH → Root Sol High

Keep requirement ambiguity, architecture/system design, high-impact strategy, public API/schema decisions, security-sensitive judgment, destructive or irreversible changes, unknown blast radius, conflicting requirements, broad refactor decisions, task decomposition, worker conflict resolution, integration, final review, and final acceptance on Root.

Heuristic: **If deciding what should be done, why, or what the system-level consequences are is itself the hard problem, keep it on Root.**

### Task packets

Before delegation, Root should create a bounded task packet containing as much as possible: Objective, Relevant context, In scope, Out of scope, Writable files, Constraints, Acceptance criteria, Required validation, Expected return, and Escalation conditions.

Task size alone is not a routing signal.

### Escalation

Workers do not own model routing. `luna-worker` must not self-upgrade to `sol-worker`.

Correct flow:

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

`sol-worker` must also return to Root for architecture-level decisions, major scope expansion, security/data-integrity issues, public API/schema decisions, or requirement ambiguity.

No recursive delegation by default.

### Parallelism and acceptance

Parallelize only genuinely independent, disjoint, separately verifiable packets with one writable owner per file and real coordination benefit.

Worker completion is not task completion. Root must inspect actual changes, evidence, and validation, resolve conflicts, run integration-level verification, and make the final Accept / Reject / Rework decision.

### Runtime truth

TOML and `AGENTS.md` express intended configuration; they do not prove which model actually ran.

Expected runtime:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

If Codex session / Agent Activity / JSONL metadata is available, verify actual `model` and `reasoning_effort`. If runtime cannot be verified, explicitly report that it is unverified.

## Step 3 — Final verification

Confirm:

- all three Agent files exist in `~/.codex/agents/`;
- Root is expected to be Sol High;
- LOW → `luna-worker`;
- MEDIUM → `sol-worker`;
- HIGH → Root;
- `sol-advisor` is not in the default routing path;
- no Luna-first routing remains;
- no recursive delegation rule exists;
- only one routing architecture marker remains in `AGENTS.md`;
- unrelated engineering rules were preserved.

Finally report: Agent installation result, `AGENTS.md` changes, removed routing conflicts, final routing graph, actual diff, and any runtime model information you could verify.
