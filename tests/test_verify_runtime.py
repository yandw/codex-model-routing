"""Runtime verification must reject metadata gaps and inherited write permissions."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
META = {"type": "session_meta", "payload": {
    "id": "child", "agent_role": "sol-advisor",
    "source": {"subagent": {"thread_spawn": {
        "parent_thread_id": "parent", "agent_role": "sol-advisor"}}}}}
CONTEXT = {"type": "turn_context", "payload": {
    "model": "gpt-6.1-sol", "effort": "high",
    "approval_policy": "on-request",
    "sandbox_policy": {"type": "read-only"}}}


class RuntimeVerificationTests(unittest.TestCase):
    def check(self, records):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            path.write_text("".join(json.dumps(r) + "\n" for r in records))
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/verify_runtime.py"),
                "--session", str(path), "--agent-file",
                str(ROOT / ".codex/agents/sol-advisor.toml"),
                "--parent-thread", "parent",
            ], text=True, capture_output=True)
            return result, json.loads(result.stdout) if result.stdout else {}

    def test_matching_configuration_does_not_claim_task_completion(self):
        result, report = self.check([META, CONTEXT])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["configuration"], "verified")
        self.assertFalse(report["task_completed"])

    def test_parent_write_override_is_a_mismatch(self):
        bad = copy.deepcopy(CONTEXT)
        bad["payload"]["sandbox_policy"]["type"] = "workspace-write"
        result, report = self.check([META, bad])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("sandbox", " ".join(report.get("issues", [])))

    def test_copied_configuration_in_message_is_not_evidence(self):
        result, report = self.check([META, {"type": "response_item", "payload": CONTEXT}])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")

    def test_missing_permission_metadata_is_unverified(self):
        bad = copy.deepcopy(CONTEXT)
        del bad["payload"]["sandbox_policy"]
        result, report = self.check([META, bad])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")

    def test_missing_approval_metadata_is_unverified(self):
        bad = copy.deepcopy(CONTEXT)
        del bad["payload"]["approval_policy"]
        result, report = self.check([META, bad])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")

    def test_later_effort_change_is_not_hidden_by_earlier_match(self):
        bad = copy.deepcopy(CONTEXT)
        bad["payload"]["effort"] = "medium"
        result, report = self.check([META, CONTEXT, bad])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("effort", " ".join(report.get("issues", [])))

    def test_unrelated_parent_cannot_verify_this_call(self):
        bad = copy.deepcopy(META)
        bad["payload"]["source"]["subagent"]["thread_spawn"]["parent_thread_id"] = "unrelated"
        result, report = self.check([bad, CONTEXT])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("parent", " ".join(report.get("issues", [])))

    def test_wrong_role_cannot_verify_requested_role(self):
        bad = copy.deepcopy(META)
        bad["payload"]["agent_role"] = "sol-worker"
        result, report = self.check([bad, CONTEXT])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("role", " ".join(report.get("issues", [])))

    def test_wrong_model_cannot_verify_requested_model(self):
        bad = copy.deepcopy(CONTEXT)
        bad["payload"]["model"] = "gpt-6-astra"
        result, report = self.check([META, bad])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("model", " ".join(report.get("issues", [])))

    def test_completed_event_is_separate_from_configuration(self):
        result, report = self.check([META, CONTEXT,
            {"type": "event_msg", "payload": {"type": "task_complete"}}])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(report["task_completed"])

    def test_new_turn_does_not_reuse_old_completion(self):
        result, report = self.check([META, CONTEXT,
            {"type": "event_msg", "payload": {"type": "task_complete"}},
            {"type": "event_msg", "payload": {"type": "task_started"}}])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(report["task_completed"])

    def test_missing_session_identity_is_unverified(self):
        result, report = self.check([CONTEXT])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")

    def test_mixed_session_files_are_not_accepted(self):
        result, report = self.check([META, CONTEXT, META])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")

    def test_unknown_record_shape_fails_without_echoing_content(self):
        result, report = self.check(["private content must not be printed"])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report.get("configuration"), "unverified")
        self.assertNotIn("private content", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
