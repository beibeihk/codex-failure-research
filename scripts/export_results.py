"""Export only reviewed synthetic records; refuse detected sensitive patterns."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analyzers.redact import sensitive_findings

ALLOWED = {
    "run_id", "scenario", "condition", "repetition", "codex_version", "platform",
    "harness_version", "fixture_version", "scenario_version", "model", "duration_seconds",
    "exit_code", "model_requests", "tool_outputs", "mcp_items", "tool_available", "tool_calls",
    "server_traces", "stderr_inventory_warning", "diagnostic", "execution_valid", "success",
    "failure_types", "attribution", "reason", "fixture_sha256", "scenario_sha256", "binary_sha256", "order_seed",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    exported = []
    for line in args.input.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if set(row) - ALLOWED:
            raise SystemExit("Unexpected collected field; review before exporting.")
        if sensitive_findings(line):
            raise SystemExit("Sensitive category detected; export refused, value suppressed.")
        exported.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in exported), encoding="utf-8")
    print("Exported", len(exported), "allowlisted synthetic records.")


if __name__ == "__main__":
    main()
