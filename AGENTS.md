# 项目模型路由

<!-- ROUTING_ARCHITECTURE: STRONG_ORCHESTRATOR -->

## Root 与责任

- 选定 Root profile：`gpt-6.1-sol / high`。
- Root 负责需求、规划、拆解、架构、路由、集成、冲突处理、最终验收和用户输出。
- 本文件不能切换当前线程模型。实际模型或 effort 与 profile 不符时报告 mismatch，不自动修改全局配置。
- 保留适用的工程、Skills、worktree、测试、review 和 Git 规则。保护已有未提交内容，部署不隐含提交或推送授权。

## 角色池与路由

| Role | Model / effort | Sandbox | 使用条件 |
|---|---|---|---|
| `luna-worker` | `gpt-6-luna / max` | workspace-write | 清晰、边界明确、可验证且值得委派的执行 |
| `sol-worker` | `gpt-6.1-sol / medium` | workspace-write | 目标明确，但需要跨文件推理、复杂调试或局部工程判断的执行 |
| `sol-advisor` | `gpt-6.1-sol / high` | read-only | 本模式仅在用户明确要求独立咨询时使用 |
| `astra-advisor` | `gpt-6-astra / high` | read-only | Sol Root 经调查仍无法可靠解决的重大判断，或高失败代价且歧义显著的决策 |

- 只有 Root 能可靠执行并验证，且本地执行更经济时，才由 Root 直接完成。任务大小或已有上下文不能替代能力判断。
- 先区分执行与决策，再按歧义、解决路径、影响范围、失败代价、可逆性和可验证性选择角色。直接选择合适层级，不要求逐级调用所有模型。
- 需要委派时显式调用对应 Custom Agent，不用模型不明的 generic/default agent 冒充角色。
- 当前支持的独立上下文调用形式：`{"agent_type":"sol-worker","fork_turns":"none","message":"明确的 Task Packet"}`。按任务替换角色，不传与固定 TOML 冲突的 model / reasoning_effort 覆盖值。
- 调用接口不支持角色选择、角色缺失或无法验证时，报告具体限制。Root 仅在能够可靠执行和验证时接手。

## 委派与升级

- 委派前给出 Objective、Relevant evidence、In scope、Out of scope、Writable ownership、Constraints、Acceptance criteria、Required validation、Expected return、Escalation conditions。
- 只传必要上下文。并行 packet 必须独立、不依赖对方未完成输出、写入范围不重叠、每个文件仅一个 active writer，并可分别验证。
- Worker 和 advisor 不创建或升级其他 agent。范围扩大、证据冲突、系统级决策、无法可靠验证或重复失败时，返回证据、已尝试方法及阻塞，由 Root 重新路由。
- 权限不足、工具缺失或缺少用户事实应先解决对应阻塞，不能仅因此升级模型。
- 顾问咨询包含一个明确决策问题、相关证据、约束、已考虑方案及预期返回。顾问返回建议、关键证据、取舍、风险、实现约束、验收标准和剩余不确定性，不接管实现、调度或最终验收。

## 权限与运行证据

- TOML 声明的 read-only 不代表有效权限已生效。顾问首次使用或权限变更后，先做无工具、无敏感内容的握手，核对关联子会话的 model、effort、有效 sandbox 和 approval 元数据。
- 顾问实际可写时返回 `PERMISSION_MISMATCH`，权限无法确认时返回 `PERMISSION_UNVERIFIED`；不继续实质咨询，不请求权限升级，不使用有写入效果的连接器操作。
- 可在独立只读会话中咨询后把结论返回 Root，但独立会话不能证明可写 Root 到只读 Custom Agent 的调用链已验证。操作见 `docs/runtime-verification.md`。
- 固定角色 effort 的调整必须同步 TOML、项目映射和验证预期，重新加载并核验；不能依赖提示词或调用参数覆盖。额外 reasoning 档位需用户明确选择并确认客户端支持。
- 磁盘配置、会话角色注册、真实执行是三个不同检查项。未调用的角色、缺失元数据和模型不匹配均如实报告，不能宣称 runtime 已验证。

## 验收

- Worker 完成不等于任务完成；Root 检查实际 diff、验证结果和证据，处理冲突并完成必要的集成验证。
- 顾问意见不能替代验证。按证据作出 Accept / Reject / Rework，保留失败和未解决风险。
- 配置与文档改动检查 TOML、角色映射、模式唯一性、提示词一致性及相关链接。
- 运行时校验器的回归验证：`python3 -m unittest discover -s tests -v`；差异检查：`git diff --check`。
- 实际子会话核验使用 `scripts/verify_runtime.py`。自动测试通过不代表真实模型路由、权限隔离、质量或成本已验收。
