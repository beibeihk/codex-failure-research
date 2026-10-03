import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ["User impact", "Agent-core relevance", "Reproducibility", "Novelty", "Evidence quality", "Root-cause tractability", "Regression risk", "OpenAI relevance", "Research value"]


def main():
    candidates = json.loads((ROOT / "research/candidates.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "research/source-audit.json").read_text(encoding="utf-8"))
    lines = ["# Failure candidate pool", "", f"{len(candidates)} candidates screened. Only C10 has a fresh runtime confirmation in this project; others are existing reports, recently addressed paths, or unverified hypotheses. Scores are research triage judgments, not empirical benchmark measurements.", "", "Score vector (each 0–5): " + " / ".join(DIMENSIONS) + ". Regression risk means estimated breadth of a potential intervention; a high score does not establish a regression.", "", "| ID | Priority | Candidate | Status | Scores | Sum |", "|---|---|---|---|---|---:|"]
    for c in candidates:
        lines.append(f"| {c['id']} | {c['priority']} | {c['title']} | {c['status']} | {' / '.join(map(str,c['scores']))} | {sum(c['scores'])} |")
    for c in candidates:
        lines += ["", "## " + c["id"] + " — " + c["title"], "", c["reason"]]
        if "anchor_issue" in c:
            n = c["anchor_issue"]; lines += ["", f"Existing report: [#{n}](https://github.com/openai/codex/issues/{n})."]
        if "anchor_commit" in c:
            sha = c["anchor_commit"]; lines += ["", f"Main source evidence: [{sha[:8]}](https://github.com/openai/codex/commit/{sha}). Release inclusion and original symptom reproduction were not individually verified."]
        lines += ["", "Open+closed symptom/component searches:"]
        for q in c["queries"]:
            s = audit["searches"].get(q, {})
            lines += [f"- `{q}`: {s.get('total_count','unavailable')} matches, {len(s.get('issues',[]))} metadata records retained."]
    lines += ["", "Commit and release audit: see [source-audit.json](source-audit.json). For each candidate, its source/issue anchor was compared with the 200-commit keyword audit and public release notes. Source-only ideas remain unconfirmed. Selected case duplicate boundaries are in [duplicate-audit.md](duplicate-audit.md).", ""]
    (ROOT / "research/candidate_failures.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
