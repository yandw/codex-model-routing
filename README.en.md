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

Some users prefer Sol High as the primary thread and want it to retain planning, architecture, and final acceptance. Others prefer Luna Max for daily work and want to consult Sol or Astra only at difficult judgment points.

So this repository does not prescribe one universally correct Root model. Instead it asks:

> **While preserving the user's Root-model habit, how can `AGENTS.md` orchestration policy and Custom Agents create a more efficient division of labor between models?**

## Two modes · GPT-6 migration baseline

Preserve two Root preferences. One invocation check matched all four role model/effort pairs. Advisor effective permissions still mismatch, and full routing workflows remain unverified. GPT-5.6 practice results do not replace current evidence.

### Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

Default to **GPT-6.1 Sol / high Root**, with an explicitly selected **GPT-6 Astra / high Root** profile also available:

- Work Root can reliably execute and validate, with a local cost/context advantage → Root;
- clear, bounded, verifiable execution worth delegating → `luna-worker` / GPT-6 Luna / max;
- bounded execution requiring cross-file reasoning or difficult debugging → `sol-worker` / GPT-6.1 Sol / medium;
- requirements, architecture, routing, integration, and final acceptance → Root;
- major judgment Sol Root cannot reliably resolve after inspection, or high failure cost combined with substantial ambiguity → `astra-advisor` / GPT-6 Astra / high, read-only.

Astra Root handles the hardest judgment directly rather than routinely calling another Astra advisor. `sol-advisor` is not used by default in this mode; it is available for independent consultation explicitly requested by the user.

### Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

Keep **GPT-6 Luna / max as Root**:

- `LUNA_LOCAL`: Luna performs and validates daily work;
- `LUNA_PARALLEL`: clear, independent work worth parallelizing → `luna-worker`;
- `SOL_EXECUTION`: bounded implementation that exceeds Luna's reliable capability → `sol-worker`;
- `SOL_ADVISED`: local design, compatibility trade-offs, or root-cause analysis requiring stronger judgment → `sol-advisor`, read-only;
- `ASTRA_ADVISED`: high failure cost with substantial ambiguity, major cross-system trade-offs, or material judgment unresolved after Sol advice → `astra-advisor`, read-only.

Advice returns to Luna, which selects local or suitable worker execution. Luna retains scheduling, integration, and final acceptance. A Sol worker can execute a single independent packet without prior consultation or a parallel batch.

Both modes let Root select the appropriate tier directly, without calling every model in sequence. Address missing permissions, tools, or user facts as blockers; model escalation does not supply them.

Configure model and reasoning separately. These efforts are starting points, not proven optima. Compare task quality, elapsed time, tokens, and rework on representative tasks. Model positioning follows the [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model), checked on 2026-10-03; the routing design is this project's proposal.

---

# Quick Start

Choose one of the following two setup paths.

## Option A — Let Codex install everything (recommended)

Open the repository you actually want to work on, then give Codex the matching **Setup Prompt URL** for your preferred Root-model habit.

### Strong Orchestrator — Sol High / optional Astra High Root

Paste this into Codex:

```text
First read the following Setup Prompt in full and execute it strictly:
https://raw.githubusercontent.com/yandw/codex-model-routing/main/prompts/en/setup-strong-orchestrator.prompt.md

Treat it as the complete instruction set for installing Codex Model Routing and initializing the current project.
Do not skip Agent installation, AGENTS.md routing, or validation steps.
If the URL cannot be read, stop and report the network-access failure instead of guessing the Prompt contents.
```

### Cheap Orchestrator + Strong Advisor — Luna Max Root

Paste this into Codex:

```text
First read the following Setup Prompt in full and execute it strictly:
https://raw.githubusercontent.com/yandw/codex-model-routing/main/prompts/en/setup-luna-first-advisor.prompt.md

Treat it as the complete instruction set for installing Codex Model Routing and initializing the current project.
Do not skip Agent installation, AGENTS.md routing, or validation steps.
If the URL cannot be read, stop and report the network-access failure instead of guessing the Prompt contents.
```

The Setup Prompt performs the whole flow:

```text
Read the canonical Setup Prompt
        ↓
install / update the four Custom Agents under ~/.codex/agents/
        ↓
read the current project's existing AGENTS.md
        ↓
apply the selected routing mode
        ↓
preserve non-conflicting Skills / worktree / TDD / testing / review / Git workflow
        ↓
validate installation, routing architecture, and any runtime evidence that is available
```

**This is the recommended first-time setup path.** Future updates to the Setup Prompt are picked up automatically because the Raw URL stays the same.

> Codex must be able to access public GitHub / Raw URLs. If the current environment blocks network access, use the Manual option below.

## Option B — Manual

The Manual path has two steps: **install the Agents yourself → enable one routing mode in your own project.**

### 1. Install the four Agents manually

Clone this repository and run:

For an existing installation, back up the role files being replaced outside agent-loading directories first. The commands below create a separate `agent-backups/` directory and stop installation if any backup fails. Do not store `.toml` backups in `agents/`, where their unchanged `name` is loaded again. A custom `CODEX_HOME` is respected.

```bash
git clone https://github.com/yandw/codex-model-routing.git
cd codex-model-routing
(
  routing_codex_home="${CODEX_HOME:-$HOME/.codex}"
  mkdir -p "$routing_codex_home/agents" "$routing_codex_home/agent-backups" || exit 1
  routing_backup_dir="$(mktemp -d "$routing_codex_home/agent-backups/routing-XXXXXX")" || exit 1
  for routing_role in luna-worker sol-worker sol-advisor astra-advisor; do
    routing_target="$routing_codex_home/agents/$routing_role.toml"
    if [ -e "$routing_target" ]; then
      cp -p "$routing_target" "$routing_backup_dir/" || exit 1
    fi
  done
  cp .codex/agents/*.toml "$routing_codex_home/agents/"
)
```

The final layout should be:

```text
~/.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
├── sol-advisor.toml
└── astra-advisor.toml
```

Do not install them as:

```text
~/.codex/agents/agents/luna-worker.toml
```

### 2. Enable one routing mode in your own project

Move into the target project:

```bash
cd /path/to/your-project
```

Then give Codex one **AGENTS-only Prompt**. It changes only the current project's `AGENTS.md` routing layer and does not reinstall the global Agents.

| Root habit | Mode | 中文 | English Prompt |
|---|---|---|---|
| Sol High / Astra High as primary | Strong Orchestrator | [`中文`](prompts/strong-orchestrator-agents-md.prompt.md) | [`AGENTS.md Prompt`](prompts/en/strong-orchestrator-agents-md.prompt.md) |
| Luna Max as primary | Cheap Orchestrator + Strong Advisor | [`中文`](prompts/luna-first-advisor-agents-md.prompt.md) | [`AGENTS.md Prompt`](prompts/en/luna-first-advisor-agents-md.prompt.md) |

If Codex can access public URLs, you can also ask it to read the corresponding Raw AGENTS-only Prompt directly. If not, open the file and paste its contents into Codex.

### Initialize another project after installation

Global agents can be reused on the same machine under the same `CODEX_HOME`; each project selects its routing mode through its own `AGENTS.md`. Initializing another project does not require reinstalling the four agents.

1. Open the target project root in Codex. For the CLI, run `codex -C /path/to/your-project`.
2. Select the Root model and reasoning effort: Strong Orchestrator defaults to `gpt-6.1-sol / high`; Luna-first uses `gpt-6-luna / max`. For Astra Root, explicitly select `gpt-6-astra / high` and state that choice in the initialization request. A prompt cannot switch the current session's model automatically.
3. Send the matching prompt below to the target project's chat. Replace `/path/to/codex-model-routing` with this repository's absolute local path. If the local file is inaccessible, paste the complete matching AGENTS-only Prompt instead.

**Strong Orchestrator initialization:**

```text
Read the complete local prompt:
/path/to/codex-model-routing/prompts/en/strong-orchestrator-agents-md.prompt.md

Apply its Strong Orchestrator policy to the current project's root AGENTS.md.
Preserve existing engineering workflow, skills, worktree, testing, review, and Git rules; update only model routing.
Check the installed Custom Agents and the current role-selection interface.
Do not reinstall global agents or change global model or permission settings.
Report the selected Root profile, unique architecture marker, available roles, and runtime checks that remain unverified.
```

**Luna-first initialization:**

```text
Read the complete local prompt:
/path/to/codex-model-routing/prompts/en/luna-first-advisor-agents-md.prompt.md

Apply its Luna-first / Cheap Orchestrator + Strong Advisor policy to the current project's root AGENTS.md.
Preserve existing engineering workflow, skills, worktree, testing, review, and Git rules; update only model routing.
Check the installed Custom Agents and the current role-selection interface.
Do not reinstall global agents or change global model or permission settings.
Report the selected Root profile, unique architecture marker, available roles, and runtime checks that remain unverified.
```

4. Start a new session after initialization so the project rules load. Check the selected Root profile and all four role mappings. Report and address missing roles, stale mappings, or runtime mismatches; files on disk alone do not establish success.

Then describe a task and let Root choose a role under the project policy, or request one explicitly:

```text
Use luna-worker to inspect test coverage for this module. Investigate without modifying code.
Have the main thread summarize the findings and decide what to change next.
```

```text
Use sol-worker to fix this cross-file issue.
Define the writable scope and acceptance criteria first; have the main thread perform final verification.
```

Verify effective read-only permissions before invoking an advisor. If it inherits write access or permissions are unknown, stop substantive consultation and use the [permission-mismatch recovery procedure](docs/runtime-verification.md#recover-from-advisor-permission-mismatch) for a separate read-only session. Installed files and generated `AGENTS.md` do not establish full runtime acceptance.

---

# What do the four Agents do?

`AGENTS.md` decides when to call a role; TOML defines its model, reasoning effort, permissions, and behavior.

| Agent | Model / reasoning | Permissions | Responsibility and mode |
|---|---|---|---|
| [`luna-worker`](.codex/agents/luna-worker.toml) | `gpt-6-luna / max` | workspace-write | Clear, verifiable execution in both modes |
| [`sol-worker`](.codex/agents/sol-worker.toml) | `gpt-6.1-sol / medium` | workspace-write | Bounded execution requiring substantial reasoning in both modes |
| [`sol-advisor`](.codex/agents/sol-advisor.toml) | `gpt-6.1-sol / high` | **read-only** | Local design, compatibility trade-offs, and difficult root-cause judgment; on demand in Mode B, only on explicit user request in Mode A |
| [`astra-advisor`](.codex/agents/astra-advisor.toml) | `gpt-6-astra / high` | **read-only** | High-cost ambiguous decisions and major cross-system trade-offs; on demand for Sol Root in Mode A and for Mode B |

These roles form a shared Agent Pool; a task need not use every role. Workers and advisors return escalation questions to Root rather than spawning agents. Advice does not replace validation.

## Effort and permission compatibility

Role efforts are fixed baselines in TOML. To change one, update the TOML plus project mapping and verification expectations, reload, and check actual metadata. The custom agent file takes precedence over spawn model/effort parameters; this version does not promise per-task dynamic effort. Use `agent_type` with `fork_turns="none"` on the current interface, without conflicting model/effort overrides. A client lacking role selection cannot verify this architecture merely by installing files.

Advisor `read-only` in the tables is the required sandbox, not a guarantee that every host enforces it. Live parent permissions can override role defaults. Before substantive consultation, use a no-tool handshake and verify effective child sandbox/approval metadata; mismatches or missing evidence block that consultation. Use an independently read-only environment/session for further verification, without changing global permissions automatically. Connector permissions remain separate from the shell sandbox. See [official subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [runtime guide](docs/runtime-verification.md).

## Upgrading an existing installation

Re-run the setup prompt for your selected mode. Update the four TOML files and replace the old project routing section together; changing model strings alone leaves obsolete routing rules active. Use the commands above to back up existing agent files in `agent-backups/`, without creating `.toml` backups in `agents/`.

Mode A adds an optional Astra Root profile and Astra consultation for Sol Root. Mode B removes the old `sol-worker` exclusion and routes post-consultation implementation to a suitable executor. Keep one architecture marker and one selected Root profile. Verify current role registration and runtime separately.

Raw setup URLs serve the version published on GitHub `main`. Local edits do not update those URLs; for an unpublished checkout, use the checked-out agent files and local AGENTS-only prompt.

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

# How do you verify that Model Routing worked?

Check repository configuration, roles registered in the current session, and actual runtime evidence separately. Updating TOML on disk proves neither that a session reloaded it nor that an agent ran with the expected model.

| Role | Expected model | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-6-luna` | `max` |
| `sol-worker` | `gpt-6.1-sol` | `medium` |
| `sol-advisor` | `gpt-6.1-sol` | `high` |
| `astra-advisor` | `gpt-6-astra` | `high` |

Also match Root to the selected profile: Mode A defaults to `gpt-6.1-sol / high` with optional `gpt-6-astra / high`; Mode B defaults to `gpt-6-luna / max`. Explicitly selected alternative supported efforts must be recorded as custom profiles.

If the current session lacks roles or exposes old mappings after installation, reload/start a session as required by the client, then verify registration and actual runtime. A prompt cannot switch the current thread's model. Report mismatches without changing global configuration or silently substituting a model.

New baseline status: **full workflow runtime unverified; advisor permissions limited**. See the [review and smoke results](docs/verification/gpt6-routing-smoke.md) for the four-role model/effort checks and fixes. Mark only roles actually invoked with matching session / Agent Activity evidence as verified. See [`docs/runtime-verification.md`](docs/runtime-verification.md) for verification and migration acceptance scenarios.

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

Model Routing should strengthen existing working habits rather than force everyone onto the same Root model. The two modes preserve strong-root (Sol or Astra) and Luna-root styles.

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
│       ├── sol-advisor.toml
│       └── astra-advisor.toml
├── scripts/
│   └── verify_runtime.py
├── tests/
│   └── test_verify_runtime.py
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

GPT-6 migration baseline (2026-10-03): routing design and configuration updated; all four role model/effort pairs were checked, but advisor effective sandbox mismatches leave full workflows, quality, and efficiency unverified. Earlier GPT-5.6 practice is historical context, not validation of this revision. Reasoning settings require representative-task evaluation.
