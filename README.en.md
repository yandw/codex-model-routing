# Codex Model Routing

[简体中文](README.md) | **English**

A research, experimentation, and reusable configuration repository for **Model-Aware Orchestration** in Codex App / Codex multi-agent workflows.

## Why this project exists

This repository is not about simply asking “which model is stronger,” and it is not about sending every task to the strongest model by default.

The actual problem is:

> **Given limited tokens, quotas, and reasoning budget, how can we assign different kinds of work to the most suitable and cost-effective model so that each model spends most of its budget on the work it is best at—and the system produces more useful engineering output per token?**

Models are not just “stronger” or “weaker.” They often have different capability and cost profiles across requirement understanding, architecture judgment, difficult reasoning, code execution, search, testing, mechanical edits, and parallel work.

Sending everything to an expensive model is simple but burns scarce tokens. Optimizing only for the cheapest call can also be wasteful when misjudgment, rework, or context loss creates a larger total cost.

This project therefore explores a finer-grained **Model Routing / Model Division of Labor** approach:

- assign clear, bounded, verifiable execution to cost-effective models;
- reserve stronger reasoning models for architecture, ambiguity, high-risk judgment, and difficult root-cause work;
- route by cognitive complexity, ambiguity, risk, blast radius, reversibility, and verifiability;
- reduce both “strong model doing mechanical work” and “cheap model making high-risk decisions” waste;
- improve token efficiency without giving up engineering quality.

Another important principle is: **preserve the user's existing Root-model habit.**

Some users prefer Sol High as the primary thread and want it to retain planning, architecture, and final acceptance. Others prefer Luna Max for daily work and want to call Sol High only at difficult judgment points.

So this repository does not prescribe one universally correct Root model. Instead it asks:

> **While preserving the user's Root-model habit, how can `AGENTS.md` orchestration policy and Custom Agents create a more efficient division of labor between models?**

## Two currently validated modes

The repository currently contains two modes that have been tested in real workflows. They are not competitors and not an A/B test. They represent different working habits while validating the same core idea: **a good model division of labor can improve overall engineering efficiency and token utilization.**

### Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

Keep **Sol High as Root**:

- LOW: low-ambiguity, verifiable execution → `luna-worker` / Luna Max;
- MEDIUM: reasoning-heavy but still bounded execution → `sol-worker` / Sol Medium;
- HIGH: architecture, ambiguity, high-risk judgment, integration, final acceptance → Root Sol High.

Best for users who already prefer Sol High as Root but want to move large amounts of execution-token usage to better-suited models.

### Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

Keep **Luna Max as Root**:

- ordinary daily work → Primary Luna;
- genuinely independent parallel tasks → `luna-worker` / Luna Max;
- high-value, high-risk, high-ambiguity judgment → `sol-advisor` / Sol High, read-only;
- after Sol returns a decision, implementation and validation return to Luna.

Best for users who already prefer Luna Max as Root and want to buy stronger reasoning only at critical judgment points.

In current Codex multi-agent practice, both modes have demonstrated that the routing architecture can be implemented, Custom Agents can hold explicit model roles, Root habits can be preserved, worker/advisor boundaries can be controlled, and runtime/session JSONL can be used to verify actual model usage.

“Validated” here means practical runnability and observed workflow effectiveness. It **does not claim these topologies are theoretically globally optimal**. The repository will continue to test other tasks, model combinations, and runtime evidence.

---

# Quick Start

The repository has only two operational layers:

```text
Install once globally
~/.codex/agents/*.toml
        ↓
provides Codex with an Agent Capability Pool

Choose a mode per project
<your-repo>/AGENTS.md
        ↓
defines when that project calls each Agent
```

In practice: **install the Agent files globally once, then choose a routing mode inside each code repository you work on.**

## Step 1 — Install the three global Agents

The repository's [`.codex/agents/`](.codex/agents/) directory is the direct-install Agent payload:

```text
.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
└── sol-advisor.toml
```

The target layout is:

```text
~/.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
└── sol-advisor.toml
```

If you cloned this repository:

```bash
mkdir -p ~/.codex/agents
cp .codex/agents/*.toml ~/.codex/agents/
```

Or paste this instruction into Codex:

```text
Install luna-worker.toml, sol-worker.toml, and sol-advisor.toml from
https://github.com/yandw/codex-model-routing/tree/main/.codex/agents
into the current user's ~/.codex/agents/ directory.
Do not delete unrelated existing agents.
After installation, verify all three files are directly under ~/.codex/agents/.
```

> The final path should be `~/.codex/agents/luna-worker.toml`, not `~/.codex/agents/agents/luna-worker.toml`.

## Step 2 — Enter your own repository and choose one mode

Move into the project you actually want to develop:

```bash
cd /path/to/your-project
```

Then choose one mode and give the corresponding Prompt **in full to Codex**. The prompt reads the existing `AGENTS.md`, changes only the routing layer, and tries to preserve existing Skills, worktrees, TDD, testing, debugging, review, Git workflow, and other engineering rules.

| Your Root habit | Recommended mode | 中文 | English Prompt |
|---|---|---|---|
| I prefer Sol High as primary | Strong Orchestrator | [`中文`](prompts/strong-orchestrator-agents-md.prompt.md) | [`AGENTS.md Prompt`](prompts/en/strong-orchestrator-agents-md.prompt.md) |
| I prefer Luna Max as primary | Cheap Orchestrator + Strong Advisor | [`中文`](prompts/luna-first-advisor-agents-md.prompt.md) | [`AGENTS.md Prompt`](prompts/en/luna-first-advisor-agents-md.prompt.md) |

These are **AGENTS-only Prompts**. Use them when the three Agents are already installed and you only want to enable or switch the routing mode for the current repository.

## Recommended: let Codex do installation + project initialization in one pass

If you do not want to handle Step 1 and Step 2 separately, paste one of the following **One-shot Setup Prompts** into Codex from the target repository.

Each one combines:

> **Agent installation instructions + the full `AGENTS.md` routing prompt for the selected mode.**

| Mode | 中文 One-shot Setup | English One-shot Setup |
|---|---|---|
| Strong Orchestrator | [`中文`](prompts/setup-strong-orchestrator.prompt.md) | [`Paste into Codex`](prompts/en/setup-strong-orchestrator.prompt.md) |
| Cheap Orchestrator + Strong Advisor | [`中文`](prompts/setup-luna-first-advisor.prompt.md) | [`Paste into Codex`](prompts/en/setup-luna-first-advisor.prompt.md) |

**For first-time setup, the One-shot Setup Prompt is the easiest path.** In later repositories, the Agents are usually already installed, so you normally only need the corresponding AGENTS-only Prompt.

---

# What do the three Agents actually do?

`.codex/agents/` is not a directory of examples. It defines three concrete execution roles. `AGENTS.md` decides **when** to call each role; the TOML file decides **which model it uses, what permissions it has, and how it behaves once called**.

| Agent | Model / Reasoning | Permission | Main job | Position in the two modes |
|---|---|---|---|---|
| [`luna-worker`](.codex/agents/luna-worker.toml) | Luna / Max | workspace-write | Clear, bounded, verifiable execution: search, mechanical edits, small implementations, tests, docs | LOW in Mode A; parallel worker in Mode B |
| [`sol-worker`](.codex/agents/sol-worker.toml) | Sol / Medium | workspace-write | Objective is known, but implementation needs cross-file understanding, difficult debugging, root-cause analysis, or localized engineering judgment | MEDIUM in Mode A; not used by default in Mode B |
| [`sol-advisor`](.codex/agents/sol-advisor.toml) | Sol / High | **read-only** | Architecture, security, compatibility, data-integrity, difficult root-cause, and other high-value judgment; returns decisions/constraints instead of routine coding | SOL_ADVISED in Mode B; not used by default in Mode A |

Why install all three? Together they form a shared **Agent Capability Pool**. Different projects can select different subsets through `AGENTS.md`, so you do not need to repeatedly install and remove agents when switching routing styles.

## What does each configuration layer control?

```text
Codex App / .codex/config.toml
        ↓
which model your current Root / Primary uses by default

~/.codex/agents/*.toml
        ↓
which callable roles exist; each role's model / reasoning / permissions / behavior

<project>/AGENTS.md
        ↓
when the current project calls each role and how escalation / integration / acceptance work
```

This is why installing TOML alone is not enough, and why writing only `AGENTS.md` is not enough. The two layers work together.

---

# How do you verify that Model Routing really worked?

This section is an **installation acceptance check**, not a theoretical note.

`AGENTS.md` and TOML only describe the routing you intend. They do not prove that Codex actually used the expected model at runtime. The source of truth is Codex session / Agent Activity / JSONL runtime metadata.

For example, if you configure:

```text
luna-worker → gpt-5.6-luna / max
```

then you only know the routing actually worked when a real sub-agent session contains evidence such as:

```text
thread_source = subagent
agent_role = luna-worker
model = gpt-5.6-luna
reasoning_effort = max
```

Expected mapping:

| Role | Expected runtime model | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-5.6-luna` | `max` |
| `sol-worker` | `gpt-5.6-sol` | `medium` |
| `sol-advisor` | `gpt-5.6-sol` | `high` |

Check runtime especially after:

- first installing these Agents;
- changing project routing rules;
- a Codex App / multi-agent update;
- changing model names or reasoning configuration;
- suspecting a worker did not use the intended model.

See [`docs/runtime-verification.md`](docs/runtime-verification.md) for JSONL inspection examples.

---

# Why is it designed this way?

These rules are not intended to add process for its own sake. They exist to avoid the most common forms of Model Routing waste.

### 1. Optimize for useful work per Token

The goal is not the cheapest single call. The goal is **more correct, accepted engineering work per token**. A cheap model that causes repeated rework can be more expensive overall.

### 2. Use the cheapest capable model

When task risk, ambiguity, and reasoning demand allow it, use the more cost-effective model and reserve expensive reasoning for genuinely difficult decisions.

### 3. Difficulty ≠ Size

A thousand lines of mechanical edits may be ideal for Luna, while ten lines of authentication or migration logic may require high reasoning. File count and code volume are not routing criteria.

### 4. Route by cognitive complexity

The main signals are ambiguity, solution-path uncertainty, blast radius, reversibility, risk, and verifiability—not simply whether the task is “large.”

### 5. Preserve the user's Root habit

Model Routing should strengthen existing working habits rather than force everyone onto the same Root model. The two modes deliberately preserve both Sol-root and Luna-root styles.

### 6. Bounded task packet first

The cheaper the worker, the more important task boundaries become. Clear objectives, scope, writable files, acceptance criteria, and validation make it safer to delegate execution.

### 7. Worker completion ≠ task completion

A worker completes its packet, not the whole project task. Integration, conflict resolution, and final acceptance remain with the owner defined by the selected mode.

### 8. No recursive agent tree by default

Workers should not continuously spawn or self-escalate to other agents. Keeping model-routing authority centralized preserves cost control and clear ownership.

### 9. Runtime metadata is the source of truth

Static configuration is intent. Evaluating whether a model division of labor is actually effective requires looking at who ran, which model/reasoning level was used, and what quality of work resulted.

---

## Research lineage / inspirations

This work is mainly inspired by two public practices:

- **Vox / `@Voxyz_ai`**: inspired the idea of keeping judgment/planning in a strong primary thread while delegating bounded execution to Luna Max. Strong Orchestrator adds a Sol Medium layer for reasoning-heavy but bounded execution.
- **BruceLanLan / `sol-luna-engineering-workflow`**: provides a more complete Luna-first + Sol Advisor pattern with Luna primary, parallel Luna workers, a read-only Sol High advisor, task packets, file ownership, escalation gates, and runtime evidence as the source of truth.

This repository is an **organization, abstraction, validation, and extension** of those ideas. The goal is not to reproduce one implementation, but to keep exploring more efficient model divisions of labor.

References:

- Vox / `@Voxyz_ai`: https://x.com/Voxyz_ai/status/2083583538830410127
- `@Lonely__MH`: https://x.com/Lonely__MH/status/2083762211449684344
- BruceLanLan / sol-luna-engineering-workflow: https://github.com/BruceLanLan/sol-luna-engineering-workflow

## Repository Structure

```text
.
├── README.md
├── README.en.md
├── .codex/
│   └── agents/
│       ├── luna-worker.toml
│       ├── sol-worker.toml
│       └── sol-advisor.toml
├── docs/
│   ├── diagrams/
│   ├── mode-selection.md
│   ├── research-notes.md
│   ├── runtime-verification.md
│   └── task-packet-template.md
└── prompts/
    ├── setup-strong-orchestrator.prompt.md
    ├── setup-luna-first-advisor.prompt.md
    ├── strong-orchestrator-agents-md.prompt.md
    ├── luna-first-advisor-agents-md.prompt.md
    └── en/
        ├── setup-strong-orchestrator.prompt.md
        ├── setup-luna-first-advisor.prompt.md
        ├── strong-orchestrator-agents-md.prompt.md
        └── luna-first-advisor-agents-md.prompt.md
```

## Star & Fork

If this project helps your Codex / multi-agent workflow, a **Star** helps more people discover an engineering approach based on model division of labor rather than making one strong model do everything.

You are also very welcome to **Fork** the repository and try your own model combinations, Agent roles, routing policies, Task Packets, or escalation rules. Different task types, model versions, and engineering habits may lead to different optimal divisions of labor.

If you find a more efficient routing approach, contributions backed by runtime evidence, experiment results, or practical observations are especially welcome. The goal is not a one-time “standard answer,” but continuously finding **more engineering output per token**.

## Status

This repository is a **research baseline / working configuration**. Both modes have demonstrated practical runnability and good workflow efficiency in real Codex multi-agent use, and will continue to evolve based on actual JSONL / Agent Activity, different model combinations, and different task types.
