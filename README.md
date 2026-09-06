# Codex Model Routing

**简体中文** | [English](README.en.md)

一套面向 Codex App / Codex multi-agent 的 **Model-Aware Orchestration** 研究与可复用配置。

本仓库关注的不是“哪个模型更强”，而是：

> 如何通过 `AGENTS.md` 的 orchestration policy，把 GPT-5.6 Sol 与 GPT-5.6 Luna 组织成不同的工程工作习惯。

当前整理两种独立工作模式。它们**不是竞争关系，也不是 A/B Test**；它们代表两种不同的 Agent / 团队工作习惯。两种模式可以共享同一套 Custom Agent Pool，但单个项目的 `AGENTS.md` 应只选择其中一种 routing architecture，避免职责和升级规则互相冲突。

## Research lineage / Inspirations

这项整理主要受到两组公开实践的启发：

- **Vox / `@Voxyz_ai`**：启发了“强主线程负责判断与规划、把边界明确的执行工作交给 Luna Max”的思路。本仓库的 **Strong Orchestrator** 模式进一步把 bounded execution 分成 Luna Max 与 Sol Medium 两层，用于区分低歧义执行和需要较强工程推理的执行。
- **BruceLanLan / `sol-luna-engineering-workflow`**：提供了一个更完整的 **Luna-first + Sol Advisor** 实现范式，包括 Luna 作为 primary、Luna worker 并行、Sol High read-only advisor、task packet、file ownership、升级门槛，以及 runtime evidence 才是模型实际调用事实来源等原则。

本仓库是在这些思路基础上的**整理、抽象与扩展**，目标不是复刻某一个实现，而是把不同模型角色组织成可复用的 Codex engineering workflow。

参考：

- Vox / `@Voxyz_ai`: https://x.com/Voxyz_ai/status/2083583538830410127
- `@Lonely__MH`: https://x.com/Lonely__MH/status/2083762211449684344
- BruceLanLan / sol-luna-engineering-workflow: https://github.com/BruceLanLan/sol-luna-engineering-workflow

## Shared Agent Pool

建议统一维护三个 Custom Agents：

```text
~/.codex/agents/
├── luna-worker.toml   # GPT-5.6 Luna / Max：低歧义、边界明确的执行
├── sol-worker.toml    # GPT-5.6 Sol / Medium：需要较强工程推理的执行
└── sol-advisor.toml   # GPT-5.6 Sol / High：只读、高价值 Judgment / Advisor
```

Agent Pool 只定义“有哪些角色、每个角色使用什么模型以及如何工作”。真正决定当前项目如何调度它们的是项目自己的 `AGENTS.md`。

## Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

核心工作习惯：

- Root Sol High 始终掌握全局；
- LOW complexity bounded execution → `luna-worker`；
- MEDIUM complexity reasoned execution → `sol-worker`；
- HIGH judgment / architecture / integration → Root Sol High；
- worker 不自行升级模型；升级必须回到 Root 决策；
- `sol-advisor` 不在默认自动 routing path。

适合偏好“强主控、强规划、强验收”的使用方式。

## Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

核心工作习惯：

- Luna Max 是日常主线程、执行层和普通验收者；
- 简单任务直接 `LUNA_LOCAL`；
- 真正独立的任务包使用 `luna-worker` 并行；
- 只有高风险、高歧义、高错误代价的 Judgment 才咨询 `sol-advisor`；
- Sol Advisor 给出 decision / constraints / acceptance criteria 后，执行立即返回 Luna；
- `sol-worker` 不在默认自动 routing path。

适合偏好“低成本主线程 + 按需专家咨询”的使用方式。

> 两种模式不是竞争关系，而是两种不同的 Orchestration Style / 工作习惯。它们可以共享同一套 Custom Agent Pool，但项目级 `AGENTS.md` 必须互斥，避免路由规则冲突。

## Architecture Layers

```text
.codex/config.toml / Codex App model selection
        ↓
决定 Primary / Root 的默认运行模型

agents/*.toml
        ↓
定义 Agent Capability Pool

AGENTS.md
        ↓
定义 Orchestration / Routing Policy
```

## AGENTS.md 初始化 Prompt

中文版本为默认版本；英文项目可以直接使用对应的 English prompt。

| 模式 | 中文（默认） | English |
|---|---|---|
| Strong Orchestrator | [`prompts/strong-orchestrator-agents-md.prompt.md`](prompts/strong-orchestrator-agents-md.prompt.md) | [`prompts/en/strong-orchestrator-agents-md.prompt.md`](prompts/en/strong-orchestrator-agents-md.prompt.md) |
| Cheap Orchestrator + Strong Advisor | [`prompts/luna-first-advisor-agents-md.prompt.md`](prompts/luna-first-advisor-agents-md.prompt.md) | [`prompts/en/luna-first-advisor-agents-md.prompt.md`](prompts/en/luna-first-advisor-agents-md.prompt.md) |

两套模式的 Prompt 仍然严格互斥：如果 `AGENTS.md` 中已经存在另一种 routing architecture，应替换冲突的 routing section，而不是将两种模式合并共存。

## Agent Files

- [`agents/luna-worker.toml`](agents/luna-worker.toml)
- [`agents/sol-worker.toml`](agents/sol-worker.toml)
- [`agents/sol-advisor.toml`](agents/sol-advisor.toml)

## Runtime Truth

静态 TOML / `AGENTS.md` **不能证明实际模型已经被调用**。最终应查看 Codex App session / sub-agent runtime metadata。

预期角色：

| Role | Expected model | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-5.6-luna` | `max` |
| `sol-worker` | `gpt-5.6-sol` | `medium` |
| `sol-advisor` | `gpt-5.6-sol` | `high` |

详见 [`docs/runtime-verification.md`](docs/runtime-verification.md)。

## Design Principles

1. **Difficulty ≠ Size**：文件多不代表难；几行安全 / 授权代码也可能需要 High reasoning。
2. **Route by cognitive complexity**：结合 ambiguity、blast radius、reversibility、risk、verifiability 判断。
3. **Bounded task packet first**：Model Routing 的效果高度依赖任务拆解质量。
4. **Worker completion ≠ task completion**：谁拥有最终验收权由当前 orchestration mode 决定。
5. **No recursive agent tree by default**：worker 不应自行不断 spawn worker。
6. **Runtime metadata is the source of truth**。

## Repository Structure

```text
.
├── README.md
├── README.en.md
├── agents/
│   ├── luna-worker.toml
│   ├── sol-worker.toml
│   └── sol-advisor.toml
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

## Status

当前内容定位为 **research baseline / working configuration**，用于持续观察 Codex App Multi-Agent 实际 runtime 行为，并根据真实 JSONL / Agent Activity 迭代。