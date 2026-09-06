# Generate / Modify AGENTS.md — Strong Orchestrator Mode

> Language: [中文](../strong-orchestrator-agents-md.prompt.md) | **English**

Modify the current project root `AGENTS.md` to establish a strict **Strong Orchestrator** Agent / Model Routing Architecture.

This change is limited to the Agent / Model Routing Layer. Do not redesign the project's existing engineering workflow.

Do not modify `CODING_ENGINEERING_REQUIREMENTS.md`, Skills, worktree rules, TDD, testing, debugging, review, Git workflow, or other methodology documents unless a direct conflict with the routing policy must be resolved.

## 1. Architecture Exclusivity

Add this unique marker to the routing section:

`<!-- ROUTING_ARCHITECTURE: STRONG_ORCHESTRATOR -->`

Read the entire existing `AGENTS.md` first.

If any conflicting routing architecture is present, including but not limited to:

- Luna-first primary orchestration;
- Cheap Orchestrator + Strong Advisor;
- `LUNA_LOCAL` / `LUNA_PARALLEL` / `SOL_ADVISED` routing;
- Luna acting as Root / Primary orchestrator;
- `sol-advisor` as the default automatic escalation path;
- any other `ROUTING_ARCHITECTURE` marker;

then do not merge, stack, or preserve the conflicting architecture.

Delete or replace the conflicting Agent Routing section.

The final `AGENTS.md` must contain only one routing architecture: `STRONG_ORCHESTRATOR`.

Preserve all engineering rules that do not conflict with routing.

## 2. Runtime Assumption

This mode requires the Root Agent to run:

`gpt-5.6-sol / high`

Root is the single orchestrator and final owner of the task.

If the actual runtime is not Sol High, do not claim that this mode is operating correctly. Report the mismatch, but do not automatically modify global Codex configuration.

## 3. Available Routing Agents

Automatic routing may use only:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

Even if `sol-advisor` exists in the global Agent Pool, it must not become a default automatic routing role in this mode. Do not call it unless the user explicitly requests it.

## 4. Root Responsibilities

Root Sol High always owns:

- requirement understanding / clarification;
- constraints identification;
- planning;
- task decomposition;
- dependency analysis;
- architecture;
- routing;
- parallelization decisions;
- escalation decisions;
- worker result evaluation;
- integration;
- conflict resolution;
- final review;
- final verification;
- acceptance / rejection;
- final user-facing output.

Root must not delegate orchestration or final judgment merely to reduce its own workload.

## 5. Routing Model

Choose the execution owner based on cognitive complexity, ambiguity, solution-path uncertainty, blast radius, risk, reversibility, and verifiability:

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

Explicitly select `luna-worker` when most of the following are true:

- the objective is clear;
- scope is clear;
- relevant files are mostly known;
- the solution path is mostly explicit;
- acceptance criteria are clear;
- architecture impact is low;
- the task can be executed independently;
- the result can be objectively verified.

Typical tasks include repository exploration, targeted search, evidence collection, mechanical / repetitive edits, bounded implementation, small bug fixes, targeted tests, lint, type-check, build, documentation, and bounded review.

Rule of thumb:

> Tell it what to do, and that is mostly enough.

### MEDIUM → sol-worker

Explicitly select `sol-worker` when:

- objective and scope are already bounded;
- the solution path is not obvious;
- multiple related files or modules must be understood together;
- root cause requires stronger reasoning;
- existing abstractions or design intent must be inferred;
- several localized implementation options exist;
- integration complexity is moderate;
- the work is still independently delegable execution work.

Rule of thumb:

> Tell it what to do, but it still needs to reason carefully about how to do it.

### HIGH → Root Sol High

Keep the following on Root:

- requirement ambiguity;
- architecture / system design;
- high-impact technical strategy;
- public API / schema decisions;
- security-sensitive judgment;
- destructive / irreversible decisions;
- unknown blast radius;
- conflicting requirements;
- broad refactor decisions;
- task decomposition;
- worker conflict resolution;
- integration;
- final review / acceptance.

Rule of thumb:

> If deciding what should be done, why it should be done, or what the system-level consequences are is itself the hard problem, keep it on Root.

## 6. Task Packet

Before delegation, Root should create a bounded Task Packet that includes as much of the following as practical:

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

Task size is not a routing criterion.

## 7. Explicit Agent Selection

When a task matches the `luna-worker` profile, explicitly select `luna-worker`.

When a task matches the `sol-worker` profile, explicitly select `sol-worker`.

Do not spawn a generic/default Root copy when an existing Custom Agent matches the work.

## 8. Escalation

Workers do not own Model Routing authority.

The following direct self-escalation is forbidden:

`luna-worker → sol-worker`

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

If `sol-worker` encounters an architecture-level decision, major scope expansion, security/data-integrity issue, public API/schema decision, or requirement ambiguity, it must also return the issue to Root.

Recursive delegation is forbidden by default.

## 9. Parallelism

Parallelize only when:

- at least two genuinely independent packets exist;
- they do not depend on each other's unfinished output;
- writable files are disjoint;
- each writable file has one active owner;
- each packet is independently verifiable;
- parallel benefit is greater than coordination overhead.

A mix of `luna-worker` and `sol-worker` is allowed, but Root always owns scheduling and integration.

## 10. Acceptance

Worker completion ≠ task completion.

Root must inspect actual changes, evidence, and validation results, resolve conflicts, perform integration-level verification when needed, and decide Accept / Reject / Rework.

Do not accept work based only on a worker summary.

## 11. Runtime Truth

TOML / `AGENTS.md` cannot prove which model actually ran.

Only runtime/session/Agent Activity is the final source of truth.

Expected runtime:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-worker` → `gpt-5.6-sol / medium`

If actual runtime differs, report the real runtime and do not pretend the requested routing succeeded.

## 12. Modification Rules

Do the following:

1. Read the entire current `AGENTS.md`;
2. locate delegation / routing sections;
3. remove routing architecture that conflicts with Strong Orchestrator;
4. generate a concise, high-density, executable routing section;
5. add the unique architecture marker;
6. preserve non-routing engineering rules;
7. use the smallest necessary diff;
8. do not copy this entire prompt verbatim into `AGENTS.md`;
9. do not modify other files.

Final validation must confirm:

- Root = Sol High;
- LOW → `luna-worker`;
- MEDIUM → `sol-worker`;
- HIGH → Root;
- `sol-advisor` is not in the default routing path;
- no Luna-first routing remains;
- no generic/default worker is preferred over matching Custom Agents;
- no recursive delegation exists;
- only one routing architecture marker exists.

Finally report: the modified location, removed conflicting rules, final routing graph, diff, architecture exclusivity status, and any runtime model information that can actually be verified.