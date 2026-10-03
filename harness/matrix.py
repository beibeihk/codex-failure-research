"""Sequential matrix; full model-free runs are opt-in local experiments."""
import argparse
import hashlib
import json
from pathlib import Path
import random

from analyzers.invariants import score_inventory
from harness.replay import CONDITIONS, ROOT, run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex", type=Path, action="append", required=True)
    parser.add_argument("--repetitions", type=int, default=10)
    parser.add_argument("--output", type=Path, default=ROOT / ".cache/matrix.jsonl")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Output exists; choose a fresh output to preserve the experiment trail.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fixture_hash = hashlib.sha256((ROOT / "fixtures/mcp_inventory/server.py").read_bytes()).hexdigest()
    scenario_hash = hashlib.sha256((ROOT / "scenarios/mcp_inventory.json").read_bytes()).hexdigest()
    for binary in args.codex:
        binary = binary.resolve()
        binary_hash = hashlib.sha256(binary.read_bytes()).hexdigest()
        schedule = [(condition, repetition) for repetition in range(1, args.repetitions + 1) for condition in CONDITIONS]
        random.Random(20261003).shuffle(schedule)
        for condition, repetition in schedule:
            row = run(binary, condition, repetition)
            row.update(score_inventory(row))
            row.update({"fixture_sha256": fixture_hash, "scenario_sha256": scenario_hash, "binary_sha256": binary_hash, "order_seed": 20261003})
            with args.output.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps({k: row[k] for k in ("run_id", "execution_valid", "success", "duration_seconds")}), flush=True)


if __name__ == "__main__":
    main()
