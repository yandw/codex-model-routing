# Codex Model Routing

[简体中文](README.md) | **English**

A research, experimentation, and reusable configuration repository for **Model-Aware Orchestration** in Codex App / Codex multi-agent workflows.

## Why this project exists

This repository is not about simply asking “which model is stronger,” and it is not about sending every task to the strongest model by default.

The real question is:

> **With limited tokens, quotas, and reasoning budget, how can different types of work be assigned to the most appropriate and cost-effective model so that each model mostly does what it is best at—and useful engineering output per token increases?**

Models differ not only in raw capability. They also have different strengths and cost structures across task understanding, architecture decisions, difficult reasoning, implementation, repository search, testing, mechanical edits, and parallel execution.

Sending everything to an expensive model is simple, but consumes limited tokens quickly. Optimizing only for the cheapest model can be equally inefficient if poor judgment, rework, or context loss creates larger downstream costs.

This project therefore explores a more granular **Model Routing / Model Division of Labor** approach:

- let cost-effective models handle clearly bounded, verifiable execution work;
- reserve stronger reasoning models for architecture, ambiguity, high-risk decisions, and difficult root-cause analysis;
- route work using factors such as cognitive complexity, ambiguity, risk, blast radius, reversibility, and verifiability;
- reduce both “strong models doing mechanical work” and “weaker models making high-impact decisions”;
- improve token efficiency without sacrificing engineering quality.

A second principle is equally important: **preserve the user's existing Root-model habit.**

Some users prefer Sol High as the primary thread and want it to keep ownership of planning, architecture, and final acceptance. Others prefer Luna Max as the daily primary and only want to borrow Sol High when difficult judgment is actually needed.

So this repository does not prescribe one universally correct Root model. Instead, it asks:

> **While keeping the user's preferred Root model unchanged, how can `AGENTS.md` orchestration policies and Custom Agents create a more efficient division of labor across models?**

## Current validation

The repository currently contains two operating modes that have been validated in practical Codex multi-agent workflows:

- **Mode A — Strong Orchestrator**: keep Sol High as Root, delegate low-ambiguity execution to Luna Max, and delegate bounded but reasoning-heavy execution to Sol Medium.
- **Mode B — Cheap Orchestrator + Strong Advisor**: keep Luna Max as Root for daily work and consult a read-only Sol High Advisor only for high-value, high-risk, or high-ambiguity judgment.

These two modes are **not competing approaches and not an A/B test**. They represent different working habits while validating the same core hypothesis:

> **A good model division of labor lets expensive reasoning tokens concentrate where strong reasoning is actually required, while cost-effective models absorb large amounts of bounded and verifiable engineering execution.**

In current Codex multi-agent practice, both modes have demonstrated that:

- the routing architecture can be implemented in a real workflow;
- Custom Agents can carry explicit model roles;
- users can preserve their existing Root-model habit rather than replacing it;
- worker / advisor boundaries can be controlled with Task Packets and escalation rules;
- runtime/session JSONL can verify the actual model and reasoning effort used;
- the division of labor produces good practical token utilization and engineering efficiency.

“Validated” here means **practical executability and observed workflow effectiveness**. It does **not** mean these two topologies have been proven to be the theoretical global optimum. The repository remains an experimental baseline for testing additional tasks, model combinations, and routing rules in search of better model specialization.

## Research Lineage / Inspirations

This work is mainly inspired by two public practices:

- **Vox / `@Voxyz_ai`**: inspired the idea of keeping judgment and planning in a strong primary thread while delegating clearly bounded execution to Luna Max. This repository's **Strong Orchestrator** mode extends that idea by splitting bounded execution into Luna Max and Sol Medium layers, distinguishing low-ambiguity execution from execution that requires deeper engineering reasoning.
- **BruceLanLan / `sol-luna-engineering-workflow`**: provides a more complete **Luna-first + Sol Advisor** pattern, including Luna as the primary model, parallel Luna workers, a read-only Sol High advisor, task packets, file ownership, escalation gates, and the principle that runtime evidence—not static configuration—is the source of truth for actual model usage.

This repository is an **organization, abstraction, validation, and extension** of those ideas. The goal is not to reproduce one implementation, but to keep exploring more effective engineering divisions of labor across models.

References:

- Vox / `@Voxyz_ai`: https://x.com/Voxyz_ai/status/2083583538830410127
- `@Lonely__MH`: https://x.com/Lonely__MH/status/2083762211449684344
- BruceLanLan / sol-luna-engineering-workflow: https://github.com/BruceLanLan/sol-luna-engineering-workflow

## Shared Agent Pool

A shared Custom Agent Pool can contain three roles:

```text
~/.codex/agents/
├── luna-worker.toml   # GPT-5.6 Luna / Max: low-ambiguity, clearly bounded execution
├── sol-worker.toml    # GPT-5.6 Sol / Medium: execution requiring stronger engineering reasoning
└── sol-advisor.toml   # GPT-5.6 Sol / High: read-only, high-value judgment / advisory role
```

The Agent Pool defines which roles exist, which model each role uses, and how each role behaves.

The project-level `AGENTS.md` determines how those roles are actually orchestrated.

## Install Agents

The repository's [`.codex/agents/`](.codex/agents/) directory is the **direct-install Agent payload**. Its structure intentionally mirrors Codex's real installation path and contains only the final runnable `.toml` files.

Copy the three files inside `.codex/agents/` **directly into**:

```text
~/.codex/agents/
```

The final layout should be:

```text
~/.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
└── sol-advisor.toml
```

If you cloned the repository, run:

```bash
mkdir -p ~/.codex/agents
cp .codex/agents/*.toml ~/.codex/agents/
```

Do **not** nest the repository's `.codex/agents` directory itself under the target directory. This is incorrect:

```text
~/.codex/agents/agents/luna-worker.toml
```

All three agents can coexist in the same global Agent Pool. Which roles are actually used—and how they are routed—still depends on the current project's `AGENTS.md`.

## Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

Core working habits:

- Root Sol High always keeps global control;
- LOW-complexity bounded execution → `luna-worker`;
- MEDIUM-complexity reasoned execution → `sol-worker`;
- HIGH-level judgment / architecture / integration → Root Sol High;
- workers do not self-escalate models; escalation returns to Root;
- `sol-advisor` is not part of the default automatic routing path.

Best suited to users who already prefer Sol High as Root but want to move large amounts of execution-token consumption to more appropriate models.

## Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

Core working habits:

- Luna Max is the daily primary thread, routine execution layer, and normal acceptance owner;
- straightforward work stays `LUNA_LOCAL`;
- genuinely independent task packets use parallel `luna-worker`s;
- only high-risk, high-ambiguity, or high-cost judgment is escalated to `sol-advisor`;
- after Sol Advisor returns a decision / constraints / acceptance criteria, routine execution returns to Luna;
- `sol-worker` is not part of the default automatic routing path.

Best suited to users who already prefer Luna Max as Root and want to pay for stronger reasoning only at the judgment points that actually need it.

> The two modes are not competitors. They are different orchestration styles / work habits. They can share the same Custom Agent Pool, but project-level `AGENTS.md` routing policies should remain mutually exclusive.

## Architecture Layers

```text
.codex/config.toml / Codex App model selection
        ↓
defines the default Primary / Root runtime model

.codex/agents/*.toml
        ↓
defines the Agent Capability Pool

AGENTS.md
        ↓
defines the Orchestration / Routing Policy
```

## AGENTS.md Init Prompts

The Chinese prompts are the default versions. English versions are provided for English-language projects.

| Mode | 中文（默认） | English |
|---|---|---|
| Strong Orchestrator | [`prompts/strong-orchestrator-agents-md.prompt.md`](prompts/strong-orchestrator-agents-md.prompt.md) | [`prompts/en/strong-orchestrator-agents-md.prompt.md`](prompts/en/strong-orchestrator-agents-md.prompt.md) |
| Cheap Orchestrator + Strong Advisor | [`prompts/luna-first-advisor-agents-md.prompt.md`](prompts/luna-first-advisor-agents-md.prompt.md) | [`prompts/en/luna-first-advisor-agents-md.prompt.md`](prompts/en/luna-first-advisor-agents-md.prompt.md) |

Each pair of prompts is intentionally architecture-exclusive: if an incompatible routing architecture already exists in `AGENTS.md`, the prompt instructs Codex to replace the conflicting routing section rather than merge both modes.

## Agent Files

- [`.codex/agents/luna-worker.toml`](.codex/agents/luna-worker.toml)
- [`.codex/agents/sol-worker.toml`](.codex/agents/sol-worker.toml)
- [`.codex/agents/sol-advisor.toml`](.codex/agents/sol-advisor.toml)

## Runtime Truth

Static TOML / `AGENTS.md` configuration **does not prove that a specific model actually ran**. The final source of truth is Codex App session / sub-agent runtime metadata.

Expected roles:

| Role | Expected model | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-5.6-luna` | `max` |
| `sol-worker` | `gpt-5.6-sol` | `medium` |
| `sol-advisor` | `gpt-5.6-sol` | `high` |

See [`docs/runtime-verification.md`](docs/runtime-verification.md).

## Design Principles

1. **Optimize for useful work per token**: the goal is not the lowest call price, but higher total engineering output per token.
2. **Use the cheapest capable model**: when ambiguity, risk, and reasoning demand allow it, prefer the more cost-effective model that can safely complete the task.
3. **Difficulty ≠ Size**: many files do not necessarily mean a difficult task; a few lines touching authorization or security may require high reasoning.
4. **Route by cognitive complexity**: consider ambiguity, blast radius, reversibility, risk, and verifiability.
5. **Preserve the user's Root habit**: model routing should strengthen an existing workflow, not force everyone onto the same Root model.
6. **Bounded task packet first**: model routing quality depends heavily on task decomposition quality.
7. **Worker completion ≠ task completion**: final acceptance ownership depends on the selected orchestration mode.
8. **No recursive agent tree by default**: workers should not continuously spawn their own workers.
9. **Runtime metadata is the source of truth**.

## Repository Structure

```text
.
├── README.md
├── README.en.md
├── .codex/
│   └── agents/          # copy the TOML files directly into ~/.codex/agents/
│       ├── luna-worker.toml
│       ├── sol-worker.toml
│       └── sol-advisor.toml
├── docs/
│   ├── diagrams/
│   │   ├── strong-orchestrator.svg
│   │   └── cheap-orchestrator-strong-advisor.svg
│   ├── mode-selection.md
│   ├── research-notes.md
│   ├── runtime-verification.md
│   └── task-packet-template.md
└── prompts/
    ├── strong-orchestrator-agents-md.prompt.md
    ├── luna-first-advisor-agents-md.prompt.md
    └── en/
        ├── strong-orchestrator-agents-md.prompt.md
        └── luna-first-advisor-agents-md.prompt.md
```

## Star & Fork

If this project helps your Codex / multi-agent workflow, consider giving the repository a **Star** so more people can discover an engineering approach based on model specialization rather than forcing one model to do everything.

You are also very welcome to **Fork** the repository and experiment with your own model combinations, Agent roles, routing policies, Task Packets, and escalation rules. Different task classes, model versions, and engineering habits may produce different optimal divisions of labor.

If you find a more efficient routing pattern, contributions of runtime evidence, experiment results, or design ideas are welcome. The goal of this repository is not to publish a one-time “correct answer,” but to keep searching for **more useful engineering work per token**.

## Status

The repository remains a **research baseline / working configuration**. Both modes have been validated for practical executability and good observed workflow efficiency in real Codex multi-agent usage, and the project will continue evolving based on real JSONL / Agent Activity evidence, different model combinations, and different task types.