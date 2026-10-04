# One-shot Setup — Luna-first / Cheap Orchestrator + Strong Advisor

**English** | [简体中文](../setup-luna-first-advisor.prompt.md)

Run this prompt in the target project. Install the four shared Custom Agents, then update its `AGENTS.md` using the complete policy below.

## Step 1 — Install / update Custom Agents

Install only the four files below directly under `~/.codex/agents/`. Preserve unrelated agents and global configuration. Read existing target files first, preserve a recoverable backup of changed files, download all four files into a temporary directory, and validate their TOML, names, model/effort mappings, and sandbox modes against the Shared Agent Pool below before replacing any installed file. A failed download or validation must leave existing agents intact. Verify installed content after copying. Do not create an extra `agents/agents/` level.

Check current role-selection support, model/effort availability, and effective-permission verification capability before declaring readiness. Configuration may be installed for a future compatible session, but report runtime unavailable when the current client lacks these capabilities. If copying or post-copy verification fails, restore the changed target files from backups and stop before updating AGENTS.md.

Source files:
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/luna-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-worker.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/sol-advisor.toml`
- `https://raw.githubusercontent.com/yandw/codex-model-routing/main/.codex/agents/astra-advisor.toml`

## Step 2 — Apply the routing policy

Read the existing project-root `AGENTS.md` completely. Update only its routing layer, preserving unrelated engineering workflow, skills, worktree, testing, review, and Git rules. Replace conflicting routing rules instead of stacking architectures. When migrating an older version of the same mode, replace the complete old routing section, including obsolete role exclusions; retaining the same marker is not sufficient. Create `AGENTS.md` if absent. Produce a concise executable policy rather than copying this prompt verbatim.

## Mode and Root profile

Keep exactly one architecture marker:

`<!-- ROUTING_ARCHITECTURE: LUNA_FIRST_STRONG_ADVISOR -->`

The default Root profile is `gpt-6-luna / max`. Primary Luna owns daily execution, scheduling, integration, and final acceptance. Record a different supported reasoning effort as a custom profile only when explicitly selected by the user.

A prompt cannot switch the current thread's actual model. Report a runtime/profile mismatch without changing global configuration or claiming the mode is operating correctly.

## Five work paths

| Path | Condition and role |
|---|---|
| `LUNA_LOCAL` | Clear requirements, reliable Luna execution, and a local-work cost advantage: Primary Luna executes and validates |
| `LUNA_PARALLEL` | Clear independent packets with disjoint writable scopes and a concrete parallelism benefit → `luna-worker` |
| `SOL_EXECUTION` | Objective, scope, and acceptance are bounded, but cross-file reasoning, difficult debugging, or local implementation exceeds Luna's reliable capability → `sol-worker` |
| `SOL_ADVISED` | Local design, compatibility trade-offs, or root-cause analysis requiring stronger judgment → `sol-advisor`, read-only |
| `ASTRA_ADVISED` | High failure cost with substantial ambiguity, major cross-system trade-offs, or material judgment still unresolved after Sol advice → `astra-advisor`, read-only |

Route complex execution separately from difficult decisions. A `sol-worker` may execute a single independent packet; neither prior advisor consultation nor multiple parallel tasks are required.

Root may consult Astra directly without first consulting Sol. Sol and Astra are on-demand advisors, not permanent supervisors. File count, task duration, or domain keywords alone do not trigger escalation.

After advice returns decisions, constraints, and acceptance criteria, scheduling returns to Primary Luna. Luna chooses local execution, `luna-worker`, or `sol-worker` according to implementation difficulty. Do not force every implementation back onto the Luna model.

Luna retains integration and final acceptance based on actual validation evidence. If reliable acceptance is unavailable, obtain more validation or ask a specific advisor question. Report unresolved risks rather than treating advice as successful validation.

## Shared Agent Pool

| Role | Model | Reasoning | Sandbox |
|---|---|---|---|
| `luna-worker` | `gpt-6-luna` | `max` | `workspace-write` |
| `sol-worker` | `gpt-6.1-sol` | `medium` | `workspace-write` |
| `sol-advisor` | `gpt-6.1-sol` | `high` | `read-only` |
| `astra-advisor` | `gpt-6-astra` | `high` | `read-only` |

## Shared execution rules

### Task packets and role selection

Before delegation, Root defines a clear task packet: Objective, Relevant evidence, In scope, Out of scope, Writable ownership, Constraints, Acceptance criteria, Required validation, Expected return, and Escalation conditions.

Distinguish execution from judgment first. Select the role using ambiguity, solution-path uncertainty, blast radius, failure cost, reversibility, and verifiability. Task size is not a routing criterion.

Root handles such work locally only when it can reliably execute and validate it, and small size, sufficient existing context, or delegation overhead makes local work more economical. Capability takes precedence over cost or size. Delegate for a concrete cost, context-isolation, or parallelism benefit. Parallelize only genuinely independent packets.

Before calling, check that the current tool supports Custom Agent role selection and isolated context. Otherwise report runtime unavailable; installed files do not prove the mode can run.

For the current interface exposing `agent_type`, use this form with the selected role:

```json
{"agent_type":"sol-worker","fork_turns":"none","message":"Explicit task packet"}
```

The fixed role's TOML controls model / effort; do not also pass model or reasoning_effort overrides. Full-history forks may inherit Root settings and cannot verify these role mappings. On other clients, use only a confirmed equivalent role invocation; report incompatibility if none exists.

Pass only necessary evidence and boundaries. Report missing roles. Root may take over only when capable of reliable execution and validation and consistent with the mode, and must record the choice. Do not disguise a generic/default agent with an unknown model as the configured role.


### Escalation and blockers

Root selects the appropriate tier directly; Luna, Sol, and Astra are not a mandatory sequence. High-cost failures combined with substantial ambiguity may justify consulting Astra directly. Routine local questions do not require the highest-tier model.

When scope expands, evidence contradicts the packet, a system-level decision is required, or reliable validation is unavailable, workers return evidence, attempts, and the specific blocker to Root. Root chooses further inspection, a revised packet, another worker, or an advisor. Repeated failure triggers reassessment, not automatic model escalation.

Unavailable tools, insufficient permissions, and missing user facts must be addressed as those blockers. A stronger model cannot supply missing permissions, tools, or facts. Respect the current environment's permissions and instruction hierarchy.

Workers and advisors do not spawn or escalate to other agents. Root owns routing.

### Advisor contract

A consultation contains one Decision question, Relevant evidence, Constraints / non-negotiables, Options considered, and Expected return.

An advisor uses read-only inspection and returns a recommendation, decisive evidence, alternatives / trade-offs, risks, implementation constraints, acceptance criteria, and remaining uncertainty. If evidence is insufficient, identify the smallest additional check rather than inventing a conclusion.

Advice returns to Root, which chooses local or worker execution according to implementation difficulty. Advisors do not own scheduling, implementation, integration, or final acceptance. Follow-up consultations require new evidence or a specific unresolved decision.

### Parallelism and acceptance

Parallel packets must be independent, not depend on each other's unfinished outputs, have disjoint writable scopes and one active writer per file, and be separately verifiable. Root may mix worker roles and always owns integration.

Worker completion is not task completion. Root inspects actual diffs, validation results, and evidence; resolves conflicts; performs appropriate integration checks; and decides Accept / Reject / Rework. Advice is not validation. Report blockers and unresolved high-risk judgment honestly.

### Effort and effective permissions

This version uses fixed role efforts, not dynamic per-task effort routing. To honor an explicit request to change a child role's effort, update its TOML and the project's mapping and verification expectations, reload, and verify the actual effort. Asking the model to think harder is not configuration, and spawn parameters do not necessarily override TOML. Use only efforts supported by both the current client and model. Levels such as `ultra` that may include automatic delegation are outside this baseline until their compatibility with Root-owned routing is verified.

An advisor's no-write behavioral contract and enforced read-only runtime permissions are separate checks. Parent live permission settings may override the role's sandbox_mode. On first use or after permission changes, perform a no-tool metadata handshake without sensitive content. Root checks correlated child model, effort, and effective sandbox/approval metadata. If the effective filesystem sandbox is not read-only or cannot be established, do not dispatch substantive consultation; report permission mismatch / unverified status. Reverify in an environment supporting independent read-only permissions or a separate read-only session. Do not change global permissions automatically or treat a standalone session as proof of Custom Agent routing. A shell sandbox does not establish read-only permissions for every connector; advisors still use read-only operations only.

### Runtime truth

TOML and AGENTS.md express intent; runtime/session/Agent Activity establishes the actual model and reasoning effort. Check the selected Root profile and roles actually invoked. Uninvoked roles remain runtime-unverified. If runtime evidence is inaccessible, explicitly report it as unverified rather than inferring success from configuration.

The efforts below are migration baselines, not proven optima. Evaluate model, reasoning effort, task quality, elapsed time, tokens, and rework separately. Specify child reasoning through role configuration or supported explicit parameters rather than relying on implicit inheritance.

## Step 3 — Installation verification

Verify all four installed files and distinguish files present on disk from roles registered in the current session. If the current session still exposes old model mappings or lacks a new role, reload/start a new session as required by the client and then verify again. Do not claim a file edit changed an already-running agent. Do not silently fall back to a different model.

## Acceptance and report

Confirm one architecture marker and one selected Root profile, correct model/effort mappings, effective role permissions (not only TOML declarations), Root-owned routing and acceptance, and no worker/advisor recursive delegation. Check that all rules match the selected mode and obsolete exclusions are gone. Report changed locations, removed conflicts, the final routing graph, diff, and runtime evidence or its absence. Distinguish static configuration checks from actual runtime verification.
