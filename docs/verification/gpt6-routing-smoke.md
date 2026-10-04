# GPT-6 routing review and smoke results

Test window: 2026-10-03–2026-10-04 (Asia/Shanghai).

## Result

Four role invocations completed, and their correlated `session_meta` / `turn_context` records matched the configured model and effort. The two worker sandboxes matched. Both advisor sandboxes were **workspace-write**, despite `sandbox_mode = "read-only"` in their TOML files. The complete modes therefore remain **runtime-unverified / permission-limited** on this host.

This report is a bounded invocation/configuration check, not a quality, latency, cost, or full engineering-workflow benchmark. Raw session logs and private workspace contents are not committed.

## Observed role metadata

All four calls selected the custom role with `fork_turns="none"`, without model or effort overrides. Each received a no-tool arithmetic handshake and returned `17+25=42`. Parent-child identity and role were correlated before reading execution metadata.

| Role | Actual model | Actual effort | Required sandbox | Actual sandbox | Approval policy | Outcome |
|---|---|---|---|---|---|---|
| luna-worker | gpt-6-luna | max | workspace-write | workspace-write | on-request | Configuration matches |
| sol-worker | gpt-6.1-sol | medium | workspace-write | workspace-write | on-request | Configuration matches |
| sol-advisor | gpt-6.1-sol | high | read-only | workspace-write | on-request | Permission mismatch |
| astra-advisor | gpt-6-astra | high | read-only | workspace-write | on-request | Permission mismatch |

The Sol worker subsequently performed a bounded read-only review of the revised routing prompts and checker. It retained `gpt-6.1-sol / medium`; this is not evidence for a different effort profile.

## Problems found and corrected

1. **Declared sandbox mistaken for effective permissions.** Added a no-tool preflight, a substantive-consultation gate, and a metadata checker. Both advisor instructions now return `PERMISSION_MISMATCH` for known writable runtimes and `PERMISSION_UNVERIFIED` when permissions cannot be established. This corrects unsafe continuation and false readiness claims; it does not change the host's permission inheritance.
2. **Role invocation under-specified.** All eight prompts now show the current isolated-role call, avoid conflicting model/effort overrides, and report clients without a compatible role-selection interface.
3. **Small-task rule could override capability.** Root may execute locally only when it can reliably execute and validate the task. A tiny but difficult concurrency fix in Luna-first routes to Sol.
4. **Effort adjustment semantics unclear.** Fixed custom-role TOML values take precedence. A requested change must update the TOML and project expectations, reload, and be verified; prompt wording is not dynamic effort control.
5. **Approval metadata missing from acceptance evidence.** The runtime checker now fails closed when approval metadata is absent/unsupported, and reports it alongside actual sandbox. Its output does not certify connector permissions or task quality.
6. **Installation copy failures lacked recovery instructions.** Setup prompts now require restoring changed files from backups on copy/post-copy validation failure before editing AGENTS.md.

## Permission guard regression

New Sol and Astra advisor invocations under the same writable parent both returned `PERMISSION_MISMATCH` and made **zero tool calls**. The Astra probe asked for an ordinary document-based consultation without supplying the expected mismatch response; it refused before reading the document. This establishes the behavioral guard for that case, not enforced OS-level read-only permissions.

An independent `codex exec --ignore-user-config --sandbox read-only` session was also attempted. After transport retries it completed and reported that its collaboration interface lacked Custom Agent role selection; no children were spawned. It does not verify the four roles in an enforced read-only environment. No global permission configuration was changed.

## Textual routing regression

A separate bounded review consumed the revised prompts without invoking their routes:

| Scenario | Expected and reviewed outcome |
|---|---|
| Tiny concurrency fix beyond Luna capability | Mode B → Sol worker |
| Tiny routine typo Luna can validate | Local work |
| One complex bounded implementation | Sol worker; no parallel-batch prerequisite |
| Sol advice followed by hard implementation | Control returns to Luna; implementation may use Sol worker |
| High-cost ambiguous decision with verified read-only advisor | Direct Astra consultation allowed |
| Same decision with writable advisor runtime | Stop substantive consultation; report permission mismatch |
| Missing credentials | Address blocker, not automatic model escalation |
| Attempt to override fixed Sol worker effort through spawn | Update role configuration and verification expectations instead |
| Client without role selection | Report incompatible runtime; no generic-role impersonation |
| Astra Root handling hard judgment | Root handles it directly; no routine same-tier advisor |

These are textual simulations, not full end-to-end executions of the modes.

## Repeatable checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_runtime.py \
  --session /path/to/child-session.jsonl \
  --agent-file .codex/agents/sol-advisor.toml \
  --parent-thread ACTUAL_PARENT_THREAD_ID
git diff --check
```

The 14 regression tests cover inherited writable sandbox, changed effort/model/role, unrelated parents, missing metadata, message-text false positives, mixed sessions, and task completion separate from configuration. All passed. TOML mappings, supported effort values from the local model catalog, bilingual policy parity, relative links, and SVG rendering were also checked.

Remaining work before claiming complete runtime readiness: establish enforced advisor read-only permissions on a compatible host, rerun substantive consultations, and exercise both modes on representative engineering tasks. Other effort profiles, `ultra`, quality, and cost improvements remain untested.

## 2026-10-04 follow-up: backups and standalone sandbox

The four bilingual setup prompts now require backups outside agent-loading directories. Both READMEs provide the same backup-before-copy commands, respect a custom `CODEX_HOME`, preserve unrelated roles, and stop on backup failure. An isolated installation with four existing role files confirmed that all originals were preserved outside `agents/`, all four new files matched their sources, and Codex reported no duplicate-role loading warning.

An offline `codex sandbox --permission-profile :read-only` probe, run outside the enclosing agent sandbox, read this repository's README successfully and received `PermissionError` when attempting to create a temporary file in the repository. The probe made no model request and left no probe file. This verifies filesystem enforcement for that standalone sandbox command, not for a Custom Agent spawned from a writable Root.

The [runtime guide](../runtime-verification.md#recover-from-advisor-permission-mismatch) now explains a separate read-only consultation session and how to return its decision to the writable Root. The existing writable-parent advisor failures above remain valid historical evidence. No new advisor invocation or full workflow acceptance was performed in this follow-up. The 14 existing regression tests passed; global agent installations and permission defaults were not changed.
