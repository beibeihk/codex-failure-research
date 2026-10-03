import copy
import importlib.util
import json
from pathlib import Path
import unittest

from analyzers.invariants import MODES, score_inventory
from analyzers.redact import redact, sensitive_findings
from analyzers.report import summarize, wilson

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fixture", ROOT / "fixtures/mcp_inventory/server.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


def sample_row(condition="error_aggregate"):
    named = condition.endswith("_named")
    method = "resources/templates/list" if condition.startswith("template_") else "resources/list"
    return {
        "run_id": "synthetic-unit-test", "scenario": "mcp-inventory-error-visibility",
        "condition": condition, "codex_version": "test-only", "platform": "synthetic",
        "exit_code": 0, "tool_available": True, "model_requests": 2,
        "mcp_items": [{"type": "mcp_tool_call", "status": "completed", "error": None,
                       "tool": "list_mcp_resource_templates" if condition.startswith("template_") else "list_mcp_resources",
                       "server": "probe" if named else "codex", "arguments": {"server": "probe"} if named else {}}],
        "tool_outputs": ['{"resources":[]}'], "duration_seconds": 1.0, "tool_calls": 1,
        "server_traces": {name: [{"method": m, "mode": mode,
                                 "error_code": -32603 if m == method and mode == "error" else None}
                                for m in ("initialize", "notifications/initialized", "tools/list", method)]
                          for name, mode in MODES[condition].items()},
    }


class InvariantTests(unittest.TestCase):
    def test_silent_error_fails_even_when_process_succeeds(self):
        result = score_inventory(sample_row())
        self.assertTrue(result["execution_valid"])
        self.assertFalse(result["success"])

    def test_explicit_error_passes_truthfulness_invariant(self):
        row = sample_row("error_named")
        message = "resources/list failed for probe: Mcp error: -32603: Synthetic inventory unavailable"
        row["mcp_items"][0].update({"status": "failed", "error": {"message": message}})
        row["tool_outputs"] = [message]
        self.assertTrue(score_inventory(row)["success"])

    def test_future_partial_metadata_passes(self):
        row = sample_row()
        row["tool_outputs"] = [json.dumps({"resources": [], "partial": True, "errors": {"probe": "unavailable"}})]
        self.assertTrue(score_inventory(row)["success"])

    def test_missing_server_trace_is_execution_exclusion(self):
        row = sample_row()
        row["server_traces"] = {"probe": []}
        result = score_inventory(row)
        self.assertFalse(result["execution_valid"])
        self.assertIsNone(result["success"])

    def test_healthy_empty_inventory_is_allowed(self):
        row = sample_row("empty_aggregate")
        self.assertTrue(score_inventory(row)["success"])

    def test_unrelated_failure_does_not_disclose_inventory_error(self):
        row = sample_row()
        row["mcp_items"][0].update({"status": "failed", "error": {"message": "unrelated tool failed"}})
        self.assertFalse(score_inventory(row)["success"])

    def test_similar_server_name_does_not_disclose_target_error(self):
        row = sample_row("error_named")
        message = "resources/list failed for probe_other: Mcp error: -32603: Synthetic inventory unavailable"
        row["mcp_items"][0].update({"status": "failed", "error": {"message": message}})
        row["tool_outputs"] = [message]
        self.assertFalse(score_inventory(row)["success"])

    def test_healthy_text_mentions_are_not_partial_metadata(self):
        row = sample_row()
        row["tool_outputs"] = [json.dumps({"resources": [{"server": "probe", "name": "partial error unavailable"}]})]
        self.assertFalse(score_inventory(row)["success"])

    def test_missing_initialize_is_excluded(self):
        row = sample_row()
        row["server_traces"]["probe"] = row["server_traces"]["probe"][1:]
        self.assertFalse(score_inventory(row)["execution_valid"])

    def test_wrong_tool_is_excluded(self):
        row = sample_row()
        row["mcp_items"][0]["tool"] = "unrelated_tool"
        self.assertFalse(score_inventory(row)["execution_valid"])

    def test_wrong_named_arguments_are_excluded(self):
        row = sample_row("error_named")
        row["mcp_items"][0]["arguments"] = {}
        self.assertFalse(score_inventory(row)["execution_valid"])

    def test_healthy_resource_cannot_be_dropped(self):
        row = sample_row("healthy_aggregate")
        self.assertFalse(score_inventory(row)["success"])
        row["tool_outputs"] = [json.dumps({"resources": [{"server": "probe", "uri": "research://public/schema"}]})]
        self.assertTrue(score_inventory(row)["success"])

    def test_partial_result_must_retain_healthy_catalog(self):
        row = sample_row("mixed_aggregate")
        row["tool_outputs"] = [json.dumps({"resources": [], "partial": True, "errors": {"probe": "unavailable"}})]
        self.assertFalse(score_inventory(row)["success"])
        row["tool_outputs"] = [json.dumps({"resources": [{"server": "healthy", "uri": "research://public/schema"}],
                                          "partial": True, "errors": {"probe": "unavailable"}})]
        self.assertTrue(score_inventory(row)["success"])

    def test_partial_flag_without_identified_server_is_insufficient(self):
        row = sample_row()
        row["tool_outputs"] = ['{"resources":[],"partial":true}']
        self.assertFalse(score_inventory(row)["success"])

    def test_status_without_model_output_is_not_evidence(self):
        row = sample_row()
        row["tool_outputs"] = []
        self.assertFalse(score_inventory(row)["execution_valid"])


class FixtureTests(unittest.TestCase):
    def test_declared_resources_and_successful_initialize(self):
        reply = fixture.response({"id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25"}}, "error")
        self.assertEqual(reply["result"]["capabilities"]["resources"], {})
        self.assertEqual(reply["result"]["protocolVersion"], "2025-11-25")

    def test_standards_conforming_internal_error(self):
        for method in ("resources/list", "resources/templates/list"):
            reply = fixture.response({"jsonrpc": "2.0", "id": 2, "method": method}, "error")
            self.assertEqual(reply["error"]["code"], -32603)
            self.assertNotIn("result", reply)

    def test_notifications_receive_no_response(self):
        self.assertIsNone(fixture.response({"method": "notifications/initialized"}, "error"))


class PrivacyTests(unittest.TestCase):
    def test_secret_formats_and_personal_paths(self):
        inputs = ["sk-" + "A" * 32, "ghp_" + "B" * 40, "github_pat_" + "C" * 30,
                  "Bearer " + "D" * 30, "person" + "@" + "example.org",
                  "C:" + "\\Users\\Synthetic\\Documents\\private.txt",
                  "/home/" + "synthetic/private.txt", "api_key=" + "E" * 32]
        for value in inputs:
            output = redact(value)
            self.assertNotEqual(output, value)
            self.assertFalse(sensitive_findings(output))

    def test_fixture_evidence_survives_redaction(self):
        value = '{"resources":[],"uri":"research://public/schema","code":-32603}'
        self.assertEqual(redact(value), value)

    def test_explicit_personal_literal(self):
        self.assertEqual(redact("private-name", ["private-name"]), "<redacted>")


class SummaryTests(unittest.TestCase):
    def test_exclusion_does_not_become_success(self):
        a = sample_row(); a.update({"execution_valid": True, "success": False})
        b = copy.deepcopy(a); b.update({"execution_valid": False, "success": None})
        result = summarize([a, b])[0]
        self.assertEqual((result["n"], result["failures"], result["excluded"]), (1, 1, 1))

    def test_wilson_small_sample_bounds(self):
        low, high = wilson(10, 10)
        self.assertAlmostEqual(high, 1.0)
        self.assertGreater(low, 0.70)
        low, high = wilson(0, 10)
        self.assertAlmostEqual(low, 0.0)
        self.assertLess(high, 0.30)


if __name__ == "__main__":
    unittest.main()

