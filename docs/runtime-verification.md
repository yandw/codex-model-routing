# Runtime Verification

## Why

Custom Agent TOML 和 `AGENTS.md` 表示期望配置，但不能单独证明 Codex App 实际使用了对应模型。

真正的 source of truth 是 sub-agent runtime / session metadata。

## Inspect recent sessions

macOS / Linux：

```bash
find ~/.codex/sessions -type f -name "*.jsonl" -mmin -15 -print0 \
| xargs -0 rg -n '"thread_source"|"agent_nickname"|"agent_role"|"model"|"reasoning_effort"|"multi_agent_version"'
```

如果已知道具体 sub-agent JSONL：

```bash
rg -n '"thread_source"|"agent_nickname"|"agent_role"|"model"|"reasoning_effort"|"multi_agent_version"' \
  rollout-....jsonl
```

## What to look for

确认这是 sub-agent：

```json
"thread_source": "subagent"
```

然后查看 `turn_context` 中实际运行信息：

```json
"model": "gpt-5.6-luna"
```

或：

```json
"model": "gpt-5.6-sol"
```

以及对应 reasoning effort。

## Expected runtime by role

| Role | Expected model | Reasoning |
|---|---|---|
| `luna-worker` | `gpt-5.6-luna` | `max` |
| `sol-worker` | `gpt-5.6-sol` | `medium` |
| `sol-advisor` | `gpt-5.6-sol` | `high` |

## Verification rule

不要根据以下内容声称模型已运行：

- TOML 文件存在；
- `name` 字段；
- `AGENTS.md` 写了 routing rule；
- Root Agent 自己说“我调用了 Luna / Sol”。

应以真实 runtime/session metadata 为准。
