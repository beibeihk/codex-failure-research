"""Schema, fixture, outcome, privacy, and version integrity checks for public CI."""
import hashlib
import json
from pathlib import Path
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analyzers.invariants import score_inventory
from analyzers.redact import sensitive_findings


def main():
    scenario_schema = json.loads((ROOT / "schemas/scenario.schema.json").read_text(encoding="utf-8"))
    for path in (ROOT / "scenarios").glob("*.json"):
        jsonschema.validate(json.loads(path.read_text(encoding="utf-8")), scenario_schema)
    schema = json.loads((ROOT / "schemas/run.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    seen = set()
    count = 0
    for path in (ROOT / "results").glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            jsonschema.validate(row, schema)
            if row["run_id"] in seen:
                raise AssertionError("Duplicate run ID")
            seen.add(row["run_id"])
            current = score_inventory(row)
            for key in ("execution_valid", "success", "failure_types", "attribution"):
                if row[key] != current[key]:
                    raise AssertionError("Stored score disagrees with independent recomputation")
            for filename, key in (("fixtures/mcp_inventory/server.py", "fixture_sha256"), ("scenarios/mcp_inventory.json", "scenario_sha256")):
                if hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() != row[key]:
                    raise AssertionError("Fixture/scenario version changed without a new experiment")
            if sensitive_findings(line):
                raise AssertionError("Sensitive category detected in result; value suppressed")
            count += 1
    print("Validated scenario/fixture versions, schemas, recomputed scores, unique run IDs and privacy for", count, "public records.")


if __name__ == "__main__":
    main()

