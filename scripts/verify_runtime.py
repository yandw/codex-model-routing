#!/usr/bin/env python3
"""Check an explicit child-session JSONL against an agent TOML (Python 3.11+).

Only execution metadata counts. A successful check verifies configuration, not
answer quality, tool-level permissions, or task acceptance. No session text is
printed. Unknown/missing metadata fails closed.
"""
import argparse
import json
from pathlib import Path
import sys
import tomllib


def verify(records, expected, parent_thread):
    issues = []
    missing = []
    metas = [r.get("payload") for r in records if r.get("type") == "session_meta"]
    contexts = [r.get("payload") for r in records if r.get("type") == "turn_context"]
    if len(metas) != 1 or not isinstance(metas[0], dict):
        missing.append("expected exactly one session_meta object")
    else:
        meta = metas[0]
        source = meta.get("source")
        subagent = source.get("subagent") if isinstance(source, dict) else None
        spawn = subagent.get("thread_spawn") if isinstance(subagent, dict) else None
        if not isinstance(spawn, dict):
            missing.append("missing supported subagent parent/role metadata")
        else:
            if spawn.get("parent_thread_id") != parent_thread:
                issues.append("parent thread mismatch or missing")
            roles = [value for value in (meta.get("agent_role"), spawn.get("agent_role")) if value]
            if not roles:
                missing.append("missing agent role")
            elif any(role != expected["name"] for role in roles):
                issues.append("agent role mismatch")
    if not contexts:
        missing.append("missing turn_context execution metadata")
    observations = []
    for number, context in enumerate(contexts, 1):
        if not isinstance(context, dict):
            missing.append(f"turn {number}: invalid context")
            continue
        policy = context.get("sandbox_policy")
        actual = {
            "model": context.get("model"),
            "effort": context.get("effort", context.get("reasoning_effort")),
            "sandbox": policy.get("type") if isinstance(policy, dict) else None,
            "approval_policy": context.get("approval_policy"),
        }
        observations.append(actual)
        if not isinstance(actual["approval_policy"], str) or not actual["approval_policy"]:
            missing.append(f"turn {number}: missing or unsupported approval_policy")
        for key, wanted in (("model", expected["model"]),
                            ("effort", expected["model_reasoning_effort"]),
                            ("sandbox", expected["sandbox_mode"])):
            if actual[key] is None:
                missing.append(f"turn {number}: missing {key}")
            elif actual[key] != wanted:
                issues.append(f"turn {number}: {key} mismatch (expected {wanted}, observed {actual[key]})")
    completed = False
    for record in records:
        payload = record.get("payload")
        if record.get("type") == "turn_context":
            completed = False
        if record.get("type") == "event_msg" and isinstance(payload, dict):
            if payload.get("type") in ("task_started", "turn_aborted"):
                completed = False
            elif payload.get("type") == "task_complete":
                completed = True
    return {
        "configuration": "mismatch" if issues else "unverified" if missing else "verified",
        "role": expected["name"],
        "observed_turns": observations,
        "task_completed": completed,
        "issues": issues + missing,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--agent-file", required=True, type=Path)
    parser.add_argument("--parent-thread", required=True)
    args = parser.parse_args()
    try:
        expected = tomllib.loads(args.agent_file.read_text())
        for field in ("name", "model", "model_reasoning_effort", "sandbox_mode"):
            if not isinstance(expected.get(field), str) or not expected[field]:
                raise ValueError("agent file is missing required verification fields")
        records = [json.loads(line) for line in args.session.read_text().splitlines() if line.strip()]
        if any(not isinstance(record, dict) for record in records):
            raise ValueError("session records must be objects")
        report = verify(records, expected, args.parent_thread)
    except (OSError, ValueError):
        # Do not echo file contents, credentials, or malformed session text.
        report = {"configuration": "unverified", "task_completed": False,
                  "issues": ["cannot parse/read supported agent TOML and session JSONL"]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["configuration"] == "verified" else 1


if __name__ == "__main__":
    sys.exit(main())
