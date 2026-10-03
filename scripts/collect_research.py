"""Search public GitHub metadata; keep raw public issue text in ignored cache."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def gh_json(args):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise RuntimeError(proc.stderr[:300])
    return json.loads(proc.stdout)


def search(query):
    for attempt in range(4):
        try:
            body = gh_json(["api", "-X", "GET", "search/issues", "-f", "q=repo:openai/codex is:issue " + query, "-f", "per_page=50"])
            return {"query": query, "total_count": body["total_count"], "incomplete_results": body["incomplete_results"], "issues": [{"number": i["number"], "title": i["title"], "state": i["state"], "url": i["html_url"]} for i in body["items"]]}
        except RuntimeError:
            if attempt == 3:
                raise
            time.sleep(3 + attempt * 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, default=ROOT.parent / "research/codex-upstream")
    args = parser.parse_args()
    candidates = json.loads((ROOT / "research/candidates.json").read_text(encoding="utf-8"))
    queries = sorted({q for c in candidates for q in c["queries"]})
    searches = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        jobs = {executor.submit(search, q): q for q in queries}
        for future in as_completed(jobs):
            q = jobs[future]
            try:
                searches[q] = future.result()
            except Exception as exc:
                searches[q] = {"query": q, "error": str(exc)}
            print(q, searches[q].get("total_count", "ERROR"), flush=True)
    commits = []
    for line in (ROOT / ".cache/commits.tsv").read_text(encoding="utf-8-sig").splitlines():
        sha, date, title = line.split("\t", 2)
        commits.append({"sha": sha, "date": date, "title": title, "url": "https://github.com/openai/codex/commit/" + sha})
    issues = {}
    for state in ("open", "closed"):
        raw = json.loads((ROOT / f".cache/{state}-issues.json").read_text(encoding="utf-8-sig"))
        issues[state] = [{k: i[k] for k in ("number", "title", "url", "createdAt", "updatedAt", "labels")} for i in raw]
    releases_raw = json.loads((ROOT / ".cache/releases.json").read_text(encoding="utf-8-sig"))
    releases = [{"tag": r["tag_name"], "prerelease": r["prerelease"], "published_at": r["published_at"], "url": r["html_url"]} for r in releases_raw]
    latest = json.loads((ROOT / ".cache/latest-release.json").read_text(encoding="utf-8-sig"))
    data = {"collected_at_utc": datetime.now(timezone.utc).isoformat(), "latest_stable": latest["tag_name"], "latest_stable_published_at": latest["published_at"], "upstream_sha": commits[0]["sha"], "commits": commits, "issues": issues, "releases": releases, "searches": searches, "scope": "100 recently created open issues, 100 recently created closed issues; 200 latest main commits; separate global open+closed candidate searches. PRs excluded."}
    (ROOT / "research/source-audit.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Saved research/source-audit.json", flush=True)


if __name__ == "__main__":
    main()
