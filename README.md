# Codex Model Routing

**简体中文** | [English](README.en.md)

一套面向 Codex App / Codex multi-agent 的 **Model-Aware Orchestration** 研究、实验与可复用配置。

## 为什么做这个项目

这个仓库并不是为了简单比较“哪个模型更强”，也不是为了让所有任务都默认使用最强模型。

真正想解决的问题是：

> **在有限的 Token、额度和推理预算下，如何把不同类型的工作交给最合适、最具性价比的模型，让每一种模型主要做自己更擅长的事情，从而提升单位 Token 的工程产出。**

大模型之间并不是只有“强”和“弱”的区别。不同模型在任务理解、架构判断、复杂推理、代码执行、检索、测试、机械修改、并行工作等方面，往往有不同的能力特点与成本结构。

如果所有工作都交给高成本模型，虽然简单，但会快速消耗有限的 Token；如果一味追求低成本，又可能因为错误判断、返工和上下文损失，最终付出更高代价。

因此，本项目尝试研究的是一种更细粒度的 **Model Routing / Model Division of Labor**：

- 让高性价比模型承担边界清晰、可验证、执行型的工作；
- 让更强的推理模型集中处理架构、歧义、高风险判断和复杂 root cause；
- 根据 cognitive complexity、ambiguity、risk、blast radius、reversibility、verifiability 等因素动态选择执行主体；
- 尽量减少“强模型做机械工作”和“弱模型处理高风险决策”两种浪费；
- 在保证工程质量的同时，提高有限 Token 的利用效率。

另一个重要原则是：**不破坏用户已经形成的 Root 模型使用习惯。**

有人习惯使用 Sol High 作为主线程，希望它持续掌握规划、架构和最终验收；也有人更愿意使用 Luna Max 作为日常主线程，只在真正需要高级判断时调用 Sol High。

所以这个仓库不是试图规定唯一正确的 Root 模型，而是尝试回答：

> **在保持用户 Root 模型习惯不变的前提下，怎样通过 `AGENTS.md` 的 orchestration policy 和 Custom Agents，让不同模型形成更高效的分工？**

## 当前验证结果

目前整理了两种已经实际验证过的工作模式：

- **Mode A — Strong Orchestrator**：保留 Sol High 作为 Root，把低歧义执行交给 Luna Max，把需要较强工程推理但仍可独立委派的执行交给 Sol Medium。
- **Mode B — Cheap Orchestrator + Strong Advisor**：保留 Luna Max 作为 Root，日常工作继续由 Luna 完成，只在高价值、高风险或高歧义 Judgment 上按需咨询只读的 Sol High Advisor。

这两种模式**不是竞争关系，也不是 A/B Test**。它们代表两种不同的 Agent / 团队工作习惯，同时验证同一个核心命题：

> **合理的模型分工可以让强模型把 Token 花在真正需要强推理的位置，同时让高性价比模型承担大量可界定、可验证的工程执行，从而获得更好的整体效率。**

在当前 Codex multi-agent 实践中，两种模式都已经验证了：

- routing architecture 可以实际落地；
- Custom Agent 可以承担明确的模型角色；
- Root 可以保持原有使用习惯而不必被替换；
- worker / advisor 的职责边界可以通过 Task Packet 和 escalation rule 控制；
- runtime/session JSONL 可以用于确认实际调用的模型与 reasoning effort；
- 这种分工方式在实践中表现出较好的 Token 利用率和工程效率。

这里的“验证”指实际工作流中的可运行性与实践效果，**不是宣称这两种拓扑已经是理论上的全局最优解**。本仓库仍会继续通过不同任务、模型组合和真实 runtime evidence，寻找更优的模型分工方式。

## Research lineage / Inspirations

这项整理主要受到两组公开实践的启发：

- **Vox / `@Voxyz_ai`**：启发了“强主线程负责判断与规划、把边界明确的执行工作交给 Luna Max”的思路。本仓库的 **Strong Orchestrator** 模式进一步把 bounded execution 分成 Luna Max 与 Sol Medium 两层，用于区分低歧义执行和需要较强工程推理的执行。
- **BruceLanLan / `sol-luna-engineering-workflow`**：提供了一个更完整的 **Luna-first + Sol Advisor** 实现范式，包括 Luna 作为 primary、Luna worker 并行、Sol High read-only advisor、task packet、file ownership、升级门槛，以及 runtime evidence 才是模型实际调用事实来源等原则。

本仓库是在这些思路基础上的**整理、抽象、验证与扩展**，目标不是复刻某一个实现，而是持续探索不同模型之间更有效的工程分工。

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

## 安装 Agents

仓库中的 [`.codex/agents/`](.codex/agents/) 目录就是 **可直接安装的 Agent payload**。目录结构刻意与 Codex 的实际安装路径保持一致，并且只保留最终可运行的 `.toml` 文件。

把 `.codex/agents/` 目录里的三个文件**直接复制到**：

```text
~/.codex/agents/
```

最终应是：

```text
~/.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
└── sol-advisor.toml
```

如果已经 clone 本仓库，可直接执行：

```bash
mkdir -p ~/.codex/agents
cp .codex/agents/*.toml ~/.codex/agents/
```

不要把仓库里的 `.codex/agents` 目录整体再嵌套一层。以下路径是错误的：

```text
~/.codex/agents/agents/luna-worker.toml
```

三个 Agent 可以同时安装；当前项目究竟使用哪些角色、如何路由，仍由该项目的 `AGENTS.md` 决定。

## Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

核心工作习惯：

- Root Sol High 始终掌握全局；
- LOW complexity bounded execution → `luna-worker`；
- MEDIUM complexity reasoned execution → `sol-worker`；
- HIGH judgment / architecture / integration → Root Sol High；
- worker 不自行升级模型；升级必须回到 Root 决策；
- `sol-advisor` 不在默认自动 routing path。

适合已经习惯使用 Sol High 作为 Root，同时希望把大量执行型 Token 转移给更合适模型的工作方式。

## Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

核心工作习惯：

- Luna Max 是日常主线程、执行层和普通验收者；
- 简单任务直接 `LUNA_LOCAL`；
- 真正独立的任务包使用 `luna-worker` 并行；
- 只有高风险、高歧义、高错误代价的 Judgment 才咨询 `sol-advisor`；
- Sol Advisor 给出 decision / constraints / acceptance criteria 后，执行立即返回 Luna；
- `sol-worker` 不在默认自动 routing path。

适合已经习惯使用 Luna Max 作为 Root，希望只在关键判断点购买更强推理能力的工作方式。

> 两种模式不是竞争关系，而是两种不同的 Orchestration Style / 工作习惯。它们可以共享同一套 Custom Agent Pool，但项目级 `AGENTS.md` 必须互斥，避免路由规则冲突。

## Architecture Layers

```text
.codex/config.toml / Codex App model selection
        ↓
决定 Primary / Root 的默认运行模型

.codex/agents/*.toml
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

- [`.codex/agents/luna-worker.toml`](.codex/agents/luna-worker.toml)
- [`.codex/agents/sol-worker.toml`](.codex/agents/sol-worker.toml)
- [`.codex/agents/sol-advisor.toml`](.codex/agents/sol-advisor.toml)

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

1. **Optimize for useful work per Token**：目标不是最低单次调用成本，而是更高的整体工程产出 / Token。
2. **Use the cheapest capable model**：只要任务的 ambiguity、risk 和 reasoning demand 允许，就优先交给更具性价比的模型。
3. **Difficulty ≠ Size**：文件多不代表难；几行安全 / 授权代码也可能需要 High reasoning。
4. **Route by cognitive complexity**：结合 ambiguity、blast radius、reversibility、risk、verifiability 判断。
5. **Preserve the user's Root habit**：Model Routing 应增强现有工作方式，而不是强迫所有用户切换到同一个 Root 模型。
6. **Bounded task packet first**：Model Routing 的效果高度依赖任务拆解质量。
7. **Worker completion ≠ task completion**：谁拥有最终验收权由当前 orchestration mode 决定。
8. **No recursive agent tree by default**：worker 不应自行不断 spawn worker。
9. **Runtime metadata is the source of truth**。

## Repository Structure

```text
.
├── README.md
├── README.en.md
├── .codex/
│   └── agents/          # 直接复制其中的 TOML 到 ~/.codex/agents/
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

如果这个项目对你的 Codex / multi-agent 工作流有帮助，欢迎给仓库一个 **Star**，让更多人看到这种基于模型分工而不是单模型硬扛的工程方式。

也非常欢迎 **Fork** 本仓库，尝试你自己的模型组合、Agent 角色、routing policy、Task Packet 或 escalation rule。不同任务类型、不同模型版本和不同工程习惯，很可能会得到不同的最优分工。

如果你验证出了更高效的 routing 方式，也欢迎把你的 runtime evidence、实验结论或改进思路带回来交流。这个仓库的目标不是给出一次性的“标准答案”，而是持续寻找 **更高的工程产出 / Token**。

## Status

当前内容定位为 **research baseline / working configuration**。两种模式已经在实际 Codex multi-agent 工作流中验证了可运行性与较好的实践效率，后续仍会继续基于真实 JSONL / Agent Activity、不同模型组合和不同任务类型迭代。