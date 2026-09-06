# Generate / Modify AGENTS.md — Luna-first Advisor Mode

> Language: [中文](../luna-first-advisor-agents-md.prompt.md) | **English**

Modify the current project root `AGENTS.md` to establish a strict **Luna-first / Cheap Orchestrator + Strong Advisor** Agent / Model Routing Architecture.

This change is limited to the Agent / Model Routing Layer. Do not redesign the project's existing engineering workflow.

Do not modify `CODING_ENGINEERING_REQUIREMENTS.md`, Skills, worktree rules, TDD, testing, debugging, review, Git workflow, or other methodology documents unless a direct conflict with the routing policy must be resolved.

## 1. Architecture Exclusivity

Add this unique marker to the routing section:

`<!-- ROUTING_ARCHITECTURE: LUNA_FIRST_STRONG_ADVISOR -->`

Read the entire existing `AGENTS.md` first.

If any conflicting routing architecture is present, including but not limited to:

- Sol High Root orchestration;
- Strong Orchestrator;
- LOW / MEDIUM / HIGH → Luna / Sol Medium / Root routing;
- automatic `sol-worker` routing;
- Sol acting as a permanent supervisor / final acceptance owner;
- any other `ROUTING_ARCHITECTURE` marker;

then do not merge, stack, or preserve the conflicting architecture.

Delete or replace the conflicting Agent Routing section.

The final `AGENTS.md` must contain only one routing architecture: `LUNA_FIRST_STRONG_ADVISOR`.

Preserve all engineering rules that do not conflict with routing.

## 2. Runtime Assumption

This mode requires the Primary / Root Agent to run:

`gpt-5.6-luna / max`

Primary Luna is the daily primary model, normal orchestrator, normal executor, worker scheduler, integration owner, and normal final acceptance owner.

If the actual runtime is not Luna Max, do not claim that this mode is operating correctly. Report the mismatch, but do not automatically modify global Codex configuration.

## 3. Available Routing Agents

Automatic routing may use only:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`, read-only

Even if `sol-worker` exists in the global Agent Pool, it must not become an automatic routing role in this mode. Do not call it unless the user explicitly requests it.

## 4. Core Philosophy

Sol is an on-demand advisor, not the default supervisor.

Do not escalate to Sol merely because the task is long, touches many files, involves substantial work, or requires many tests. Difficulty ≠ Size.

Escalate to Sol primarily based on uncertainty, ambiguity, blast radius, reversibility, plausible failure cost, reasoning difficulty, and security / integrity impact.

## 5. Three Routing Modes

### LUNA_LOCAL

If requirements are clear, risk is low to moderate, a single thread is more economical, and delegation overhead is larger than its benefit, Primary Luna should complete and validate the work directly.

Do not spawn a worker merely to “use agents.”

### LUNA_PARALLEL

If at least two genuinely independent, disjoint, separately verifiable task packets exist and parallelism creates real benefit, delegate to `luna-worker`.

Each packet must have a clear objective, scope, writable ownership, acceptance criteria, and validation requirements. Each writable file may have only one active owner.

Primary Luna owns final integration and normal acceptance.

### SOL_ADVISED

Call `sol-advisor` only for genuinely high-value judgment.

Typical escalation conditions include:

- requirements remain materially ambiguous or contradictory after targeted inspection;
- architecture decisions;
- security / privacy;
- authentication / authorization;
- cryptography / payments;
- destructive migration;
- data integrity;
- distributed consistency;
- breaking compatibility;
- cross-system interface decisions;
- multiple plausible root causes remain after the cheapest discriminating checks;
- two evidence-based implementation attempts have failed;
- final validation reveals an unresolved risk with high plausible failure cost.

Do not let Sol Advisor complete the whole feature, review everything indiscriminately, or take over routine implementation.

## 6. Sol Advisor Contract

Primary Luna should collect the cheapest useful evidence before consulting Sol.

The request to `sol-advisor` should include:

- one Decision question;
- Relevant evidence;
- Constraints / non-negotiables;
- Options considered, if any;
- Expected return.

Expected return:

- recommendation;
- rationale / decisive evidence;
- rejected alternatives;
- risks;
- implementation constraints;
- acceptance criteria;
- remaining uncertainty.

If evidence is insufficient, Sol should identify only the cheapest additional check needed.

## 7. Return Execution to Luna

After Sol Advisor returns a decision, routine execution must return to Luna:

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

Sol does not perform routine coding, tests, integration, or normal final acceptance.

A second targeted Sol consultation is allowed only when the final artifact still contains unresolved high-risk judgment.

## 8. Luna Parallelism

Use `luna-worker` actively, but only when genuinely independent work benefits from parallelism.

Required conditions:

- no dependency on another worker's unfinished output;
- explicit scope;
- explicit acceptance criteria;
- disjoint writable files;
- one writable owner per file;
- Primary Luna can integrate and validate the results.

Do not spawn agents for trivial work.

## 9. Task Packet

Every delegated packet should include as much of the following as practical:

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

A worker must stop and return when it encounters material ambiguity, repository facts that contradict the packet, unexpected interface/dependency changes, security/data-integrity/compatibility impact, unavailable validation, material scope expansion, or repeated evidence-based failure.

## 10. Acceptance

Primary Luna owns normal integration, review, verification, and final acceptance.

It must inspect actual diffs, actual validation results, and worker evidence. Do not accept a result based only on a summary.

Sol Advisor is responsible only for the specific difficult decision it was asked to resolve.

## 11. Explicitly Forbidden Routing

This mode must not automatically form any of the following:

- Root Sol High → workers;
- Luna → `sol-worker` Medium → Sol High Root;
- automatic `sol-worker` routing;
- Sol Advisor → routine implementation;
- Sol as a permanent supervisor.

The normal topology must be:

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

TOML / `AGENTS.md` cannot prove which model actually ran. Only runtime/session/Agent Activity is the final source of truth.

Expected runtime:

- `luna-worker` → `gpt-5.6-luna / max`
- `sol-advisor` → `gpt-5.6-sol / high`

If actual runtime differs, report the real runtime and do not pretend the requested routing succeeded.

## 13. Modification Rules

Do the following:

1. Read the entire current `AGENTS.md`;
2. locate delegation / routing sections;
3. remove routing architecture that conflicts with Luna-first / Strong Advisor;
4. generate a concise, high-density, executable routing section;
5. add the unique architecture marker;
6. preserve non-routing engineering rules;
7. do not add Strong Orchestrator compatibility;
8. do not add automatic `sol-worker` routing;
9. use the smallest necessary diff;
10. do not copy this entire prompt verbatim into `AGENTS.md`;
11. do not modify other files.

Final validation must confirm:

- Primary = Luna Max;
- normal work = Luna;
- independent parallel work = `luna-worker`;
- difficult judgment = `sol-advisor`;
- execution returns to Luna after a Sol decision;
- `sol-worker` is not in the automatic routing graph;
- Sol High is not a permanent supervisor;
- only one routing architecture marker exists.

Finally report: the modified location, removed conflicting rules, final routing graph, Sol escalation gates, diff, architecture exclusivity status, and any runtime model information that can actually be verified.