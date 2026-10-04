# Task Packet Template

```markdown
## Objective
One concrete, observable outcome.

## Routing decision
Execution or judgment; selected role and why it is worth delegating.
For consultation, state one explicit decision question.

## Relevant context
Only facts and prior decisions required to execute the packet.

## In scope
- Files / modules that may be inspected.
- Writable files exclusively owned by this worker.

## Out of scope
- Files, systems, interfaces, or decisions the worker must not change.

## Constraints
- Repository conventions.
- Compatibility / safety / performance requirements.
- No new dependency unless explicitly authorized.

## Acceptance criteria
- Observable behavior.
- Required edge cases.

## Required validation
Exact tests, checks, builds, type-checks, lint, or deterministic inspection.

## Expected return
1. Result summary.
2. Exact files inspected / changed.
3. Commands / checks and each result.
4. Remaining risks / uncertainty.
5. Decisions required from the parent.
6. For advisors: recommendation, evidence, constraints, acceptance criteria, and remaining uncertainty.

## Escalate immediately if
- Repository evidence contradicts the packet.
- Scope must materially expand.
- Public interface / dependency must change.
- Security / authorization / privacy / data integrity / compatibility becomes material.
- Required validation cannot run.
- Repeated evidence-based attempts fail.
```

Routing remains with Root. Missing tools, permissions, or facts are concrete blockers, not automatic reasons to upgrade models. Advisors return advice to Root; Root selects the executor and retains final acceptance.
