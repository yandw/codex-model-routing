# Codex Model Routing

**简体中文** | [English](README.en.md)

一套面向 Codex App / Codex multi-agent 的 **Model-Aware Orchestration** 研究、实验与可复用配置。

## 为什么做这个项目

这个仓库并不是为了简单比较“哪个模型更强”，也不是为了让所有任务都默认使用最强模型。

真正想解决的问题是：

> **在有限的 Token、额度和推理预算下，如何把不同类型的工作交给最合适、最具性价比的模型，让每一种模型主要做自己更擅长的事情，从而提升单位 Token 的工程产出。**

大模型之间并不只有“强”和“弱”的区别。不同模型在任务理解、架构判断、复杂推理、代码执行、检索、测试、机械修改、并行工作等方面，往往有不同的能力特点与成本结构。

如果所有工作都交给高成本模型，虽然简单，但会快速消耗有限 Token；如果一味追求低成本，又可能因为错误判断、返工和上下文损失，最终付出更高代价。

因此，本项目尝试研究更细粒度的 **Model Routing / Model Division of Labor**：

- 让高性价比模型承担边界清晰、可验证、执行型的工作；
- 让更强的推理模型集中处理架构、歧义、高风险判断和复杂 root cause；
- 根据 cognitive complexity、ambiguity、risk、blast radius、reversibility、verifiability 等因素动态选择执行主体；
- 尽量减少“强模型做机械工作”和“弱模型处理高风险决策”两种浪费；
- 在保证工程质量的同时，提高有限 Token 的利用效率。

另一个重要原则是：**不破坏用户已经形成的 Root 模型使用习惯。**

有人习惯使用 Sol High 作为主线程，希望它持续掌握规划、架构和最终验收；也有人更愿意使用 Luna Max 作为日常主线程，只在真正需要高级判断时调用 Sol High。

所以这个仓库不是试图规定唯一正确的 Root 模型，而是尝试回答：

> **在保持用户 Root 模型习惯不变的前提下，怎样通过 `AGENTS.md` 的 orchestration policy 和 Custom Agents，让不同模型形成更高效的分工？**

## 当前验证的两种模式

目前整理了两种已经实际验证过的工作模式。它们不是竞争关系，也不是 A/B Test，而是两种不同的工作习惯，用来验证同一个核心命题：**合理的模型分工可以提高整体工程效率与 Token 利用率。**

### Mode A — Strong Orchestrator

![Strong Orchestrator](docs/diagrams/strong-orchestrator.svg)

保留 **Sol High 作为 Root**：

- LOW：低歧义、可验证执行 → `luna-worker` / Luna Max；
- MEDIUM：需要较强工程推理的 bounded execution → `sol-worker` / Sol Medium；
- HIGH：架构、歧义、高风险判断、integration、final acceptance → Root Sol High。

适合已经习惯使用 Sol High 作为 Root，同时希望把大量执行型 Token 转移给更合适模型的用户。

### Mode B — Cheap Orchestrator + Strong Advisor

![Cheap Orchestrator + Strong Advisor](docs/diagrams/cheap-orchestrator-strong-advisor.svg)

保留 **Luna Max 作为 Root**：

- 普通日常工作 → Primary Luna；
- 真正独立的并行任务 → `luna-worker` / Luna Max；
- 高价值、高风险、高歧义 Judgment → `sol-advisor` / Sol High，只读咨询；
- Sol 给出 decision 后，implementation / validation 回到 Luna。

适合已经习惯使用 Luna Max 作为 Root，希望只在关键判断点调用更强推理能力的用户。

在当前 Codex multi-agent 实践中，两种模式都已经验证：routing architecture 可以落地、Custom Agent 可以承担明确模型角色、Root 使用习惯可以保持、worker / advisor 边界可以控制，并且 runtime/session JSONL 可以用于确认实际模型调用。

这里的“验证”指实际工作流中的可运行性与实践效果，**不是宣称这两种拓扑已经是理论上的全局最优解**。项目会继续通过不同任务、模型组合和真实 runtime evidence，探索更优的分工方式。

---

# 快速开始

第一次使用只需要在下面两种方式中选一种。

## 方式 A — 让 Codex 自动安装（推荐）

进入你真正要开发的项目目录，然后根据自己的 Root 使用习惯，把对应的 **Setup Prompt URL** 交给 Codex。

### Strong Orchestrator — Sol High Root

把下面这段直接发给 Codex：

```text
请先完整读取并严格执行下面的 Setup Prompt：
https://raw.githubusercontent.com/yandw/codex-model-routing/main/prompts/setup-strong-orchestrator.prompt.md

将它视为本次 Codex Model Routing 安装与当前项目初始化的完整指令。
不要省略其中的 Agent 安装、AGENTS.md routing 和验证步骤。
如果无法读取该 URL，请停止并报告网络访问失败，不要猜测 Prompt 内容。
```

### Cheap Orchestrator + Strong Advisor — Luna Max Root

把下面这段直接发给 Codex：

```text
请先完整读取并严格执行下面的 Setup Prompt：
https://raw.githubusercontent.com/yandw/codex-model-routing/main/prompts/setup-luna-first-advisor.prompt.md

将它视为本次 Codex Model Routing 安装与当前项目初始化的完整指令。
不要省略其中的 Agent 安装、AGENTS.md routing 和验证步骤。
如果无法读取该 URL，请停止并报告网络访问失败，不要猜测 Prompt 内容。
```

Setup Prompt 会一次完成：

```text
读取官方 Setup Prompt
        ↓
安装 / 更新 ~/.codex/agents/ 中三个 Custom Agents
        ↓
读取当前项目已有 AGENTS.md
        ↓
应用你选择的 routing mode
        ↓
保留无冲突的 Skills / worktree / TDD / testing / review / Git workflow
        ↓
校验安装、routing architecture 和能够读取到的 runtime evidence
```

**这是推荐的第一次安装方式。** 后续 Setup Prompt 更新后，新用户只要继续使用同一个 Raw URL，就会读取最新版本。

> Codex 需要能够访问公开 GitHub / Raw URL。如果当前运行环境禁止网络访问，请使用下面的 Manual 方式。

## 方式 B — Manual

Manual 方式分两步：**手动安装 Agent → 在自己的项目里启用一种 routing mode。**

### 1. 手动安装三个 Agent

Clone 本仓库后执行：

```bash
git clone https://github.com/yandw/codex-model-routing.git
cd codex-model-routing
mkdir -p ~/.codex/agents
cp .codex/agents/*.toml ~/.codex/agents/
```

最终应该得到：

```text
~/.codex/agents/
├── luna-worker.toml
├── sol-worker.toml
└── sol-advisor.toml
```

不要安装成：

```text
~/.codex/agents/agents/luna-worker.toml
```

### 2. 在自己的项目里启用 routing mode

进入目标项目：

```bash
cd /path/to/your-project
```

然后选择一份 **AGENTS-only Prompt** 交给 Codex。它只负责当前项目的 `AGENTS.md` routing layer，不再安装全局 Agent。

| Root 使用习惯 | 模式 | 中文 Prompt | English |
|---|---|---|---|
| Sol High 做主线程 | Strong Orchestrator | [`AGENTS.md Prompt`](prompts/strong-orchestrator-agents-md.prompt.md) | [`English`](prompts/en/strong-orchestrator-agents-md.prompt.md) |
| Luna Max 做主线程 | Cheap Orchestrator + Strong Advisor | [`AGENTS.md Prompt`](prompts/luna-first-advisor-agents-md.prompt.md) | [`English`](prompts/en/luna-first-advisor-agents-md.prompt.md) |

如果 Codex 可以访问公开 URL，也可以让它直接读取对应的 Raw AGENTS-only Prompt；如果不能，就打开文件并把内容复制给 Codex。

---

# 三个 Agent 分别是干什么的？

`.codex/agents/` 不是三份“示例配置”，而是三种明确的执行角色。`AGENTS.md` 决定何时调用它们，而 TOML 文件决定“被调用以后这个 Agent 用什么模型、有什么权限、应该怎么工作”。

| Agent | 模型 / Reasoning | 权限 | 主要职责 | 在两种模式里的位置 |
|---|---|---|---|---|
| [`luna-worker`](.codex/agents/luna-worker.toml) | Luna / Max | workspace-write | 清晰、bounded、可验证的执行：检索、机械修改、小型实现、tests、docs | Mode A 的 LOW；Mode B 的并行 worker |
| [`sol-worker`](.codex/agents/sol-worker.toml) | Sol / Medium | workspace-write | objective 已明确，但 implementation path 需要跨文件理解、复杂 debugging、root-cause 或局部工程判断 | Mode A 的 MEDIUM；Mode B 默认不用 |
| [`sol-advisor`](.codex/agents/sol-advisor.toml) | Sol / High | **read-only** | 架构、安全、兼容性、数据完整性、高风险 root cause 等高价值 Judgment，只给 decision / constraints，不做日常 coding | Mode B 的 SOL_ADVISED；Mode A 默认不用 |

为什么三个都建议安装？因为它们组成一个共享的 **Agent Capability Pool**。不同项目通过不同 `AGENTS.md` 选择其中一部分使用，不需要每换一种模式就反复安装 / 删除 Agent。

## 三层配置分别控制什么？

```text
Codex App / .codex/config.toml
        ↓
你当前 Root / Primary 默认用什么模型

~/.codex/agents/*.toml
        ↓
有哪些可调用角色；每个角色的 model / reasoning / permission / behavior

<project>/AGENTS.md
        ↓
当前项目什么时候调用哪个角色，以及 escalation / integration / acceptance 规则
```

这也是为什么**只安装 TOML 不够**，也为什么**只写 AGENTS.md 也不够**：两层需要一起工作。

---

# 如何确认 Model Routing 真的生效？

这一段不是理论说明，而是**安装后的验收方法**。

`AGENTS.md` 和 TOML 只能说明“我们希望 Codex 怎么路由”，不能证明运行时真的调用了对应模型。真正的事实来源是 Codex session / Agent Activity / JSONL runtime metadata。

例如，你配置了：

```text
luna-worker → gpt-5.6-luna / max
```

只有当实际 sub-agent session 中也看到类似：

```text
thread_source = subagent
agent_role = luna-worker
model = gpt-5.6-luna
reasoning_effort = max
```

才能确认这个 worker **实际**按预期运行。

当前预期映射：

| Role | 预期实际模型 | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-5.6-luna` | `max` |
| `sol-worker` | `gpt-5.6-sol` | `medium` |
| `sol-advisor` | `gpt-5.6-sol` | `high` |

建议在以下情况检查 runtime：

- 第一次安装这些 Agent 后；
- 修改 `AGENTS.md` routing 后；
- Codex App / multi-agent 机制升级后；
- 模型名称或 reasoning 配置调整后；
- 你怀疑 worker 没有使用预期模型时。

详细的 JSONL 检查方法与示例见 [`docs/runtime-verification.md`](docs/runtime-verification.md)。

---

# 为什么这样设计？

这些规则不是为了增加流程，而是为了避免 Model Routing 最常见的几种浪费。

### 1. Optimize for useful work per Token

优化目标不是“每次调用最便宜”，而是**单位 Token 最终完成多少正确、可验收的工程工作**。低价模型导致大量返工同样是浪费。

### 2. Use the cheapest capable model

只要任务风险、歧义和 reasoning demand 允许，就把它交给更具性价比的模型；真正昂贵的推理能力留给真正困难的决策。

### 3. Difficulty ≠ Size

1000 行机械修改可能非常适合 Luna；10 行 authentication / migration 代码却可能必须由高 reasoning 模型判断。文件数和代码量不是 routing 标准。

### 4. Route by cognitive complexity

主要看 ambiguity、solution-path uncertainty、blast radius、reversibility、risk、verifiability，而不是简单看“任务大不大”。

### 5. Preserve the user's Root habit

Model Routing 应该增强你的工作习惯，而不是强迫所有人都使用同一个 Root。两种模式分别保留 Sol-root 和 Luna-root 的使用方式。

### 6. Bounded task packet first

越希望把执行交给高性价比 worker，就越需要明确 objective、scope、writable files、acceptance criteria 和 validation。清晰边界是低成本委派仍然可靠的前提。

### 7. Worker completion ≠ task completion

Worker 完成的是自己的 packet，不代表整个任务已经完成。integration、conflict resolution 和 final acceptance 仍由当前模式定义的 owner 负责。

### 8. No recursive agent tree by default

Worker 不应自行不断 spawn / 升级其他 Agent。Model Routing 权限保持集中，才能控制成本、职责和上下文扩散。

### 9. Runtime metadata is the source of truth

静态配置只是 intent。要研究模型分工是否真的更高效，最终必须看谁实际运行、用了什么 model / reasoning、完成质量和返工情况。

---

## Research lineage / Inspirations

这项整理主要受到两组公开实践的启发：

- **Vox / `@Voxyz_ai`**：启发了“强主线程负责判断与规划、把边界明确的执行工作交给 Luna Max”的思路。Strong Orchestrator 进一步加入 Sol Medium，处理 reasoning-heavy but bounded execution。
- **BruceLanLan / `sol-luna-engineering-workflow`**：提供了更完整的 Luna-first + Sol Advisor 范式，包括 Luna primary、parallel Luna workers、read-only Sol High advisor、task packet、file ownership、escalation gates，以及 runtime evidence 才是模型实际调用事实来源等原则。

本仓库是在这些思路基础上的**整理、抽象、验证与扩展**，目标不是复刻某一个实现，而是持续探索不同模型之间更有效的工程分工。

参考：

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

如果这个项目对你的 Codex / multi-agent 工作流有帮助，欢迎给仓库一个 **Star**，让更多人看到这种基于模型分工而不是单模型硬扛的工程方式。

也非常欢迎 **Fork** 本仓库，尝试你自己的模型组合、Agent 角色、routing policy、Task Packet 或 escalation rule。不同任务类型、不同模型版本和不同工程习惯，很可能会得到不同的最优分工。

如果你验证出了更高效的 routing 方式，也欢迎把 runtime evidence、实验结论或改进思路带回来交流。这个仓库的目标不是给出一次性的“标准答案”，而是持续寻找 **更高的工程产出 / Token**。

## Status

当前内容定位为 **research baseline / working configuration**。两种模式已经在实际 Codex multi-agent 工作流中验证了可运行性与较好的实践效率，后续仍会继续基于真实 JSONL / Agent Activity、不同模型组合和不同任务类型迭代。