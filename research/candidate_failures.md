# Failure candidate pool

24 candidates screened. Only C10 has a fresh runtime confirmation in this project; others are existing reports, recently addressed paths, or unverified hypotheses. Scores are research triage judgments, not empirical benchmark measurements.

Score vector (each 0–5): User impact / Agent-core relevance / Reproducibility / Novelty / Evidence quality / Root-cause tractability / Regression risk / OpenAI relevance / Research value. Regression risk means estimated breadth of a potential intervention; a high score does not establish a regression.

| ID | Priority | Candidate | Status | Scores | Sum |
|---|---|---|---|---|---:|
| C01 | P0 | Premature completion during extended review | duplicate | 5 / 5 / 1 / 0 / 1 / 2 / 4 / 5 / 5 | 28 |
| C02 | P0 | Repeated failed hypothesis in long coding loops | candidate | 5 / 5 / 1 / 1 / 1 / 2 / 4 / 5 / 5 | 29 |
| C03 | P1 | Repository constraints absent after manual compaction | candidate | 5 / 5 / 1 / 2 / 1 / 3 / 5 / 5 / 5 | 32 |
| C04 | P1 | Compaction lifecycle missing from exec JSON | duplicate | 3 / 4 / 5 / 0 / 4 / 5 / 3 / 4 / 4 | 32 |
| C05 | P1 | Memory summary middle truncation loses recent entries | duplicate | 4 / 5 / 4 / 0 / 3 / 4 / 4 / 5 / 5 | 34 |
| C06 | P2 | Code Mode discovery guidance changes with catalog | fixed on main / awaiting release | 4 / 5 / 2 / 0 / 4 / 5 / 5 / 5 / 4 | 34 |
| C07 | P2 | MCP resource helpers unavailable in Code Mode | fixed on main / awaiting release | 4 / 5 / 4 / 0 / 4 / 5 / 4 / 5 / 4 | 35 |
| C08 | P2 | Responses Lite stale incremental tool catalog | fixed on main / awaiting release | 4 / 5 / 2 / 0 / 4 / 4 / 5 / 5 / 5 | 34 |
| C09 | P2 | Plugin tools hidden when schema budget exhausted | duplicate | 4 / 5 / 4 / 0 / 3 / 4 / 5 / 5 / 5 | 35 |
| C10 | P3 | Aggregate MCP inventory masks server failure | confirmed | 4 / 5 / 5 / 4 / 5 / 5 / 4 / 5 / 5 | 42 |
| C11 | P3 | Resource pagination mutates opaque whitespace cursor | candidate | 2 / 4 / 3 / 4 / 2 / 5 / 3 / 4 / 3 | 30 |
| C12 | P3 | MCP tools/list only consumes first page | fixed on main / awaiting release | 4 / 5 / 4 / 0 / 4 / 5 / 4 / 5 / 4 | 35 |
| C13 | P3 | Unbounded resource pagination | duplicate | 4 / 4 / 3 / 0 / 3 / 5 / 4 / 4 / 4 | 31 |
| C14 | P3 | Tool-list-changed notification does not refresh catalog | candidate | 4 / 5 / 2 / 2 / 2 / 4 / 5 / 5 / 5 | 34 |
| C15 | P4 | Resume returns stale replay history | fixed on main / awaiting release | 5 / 5 / 2 / 0 / 4 / 4 / 5 / 5 / 5 | 35 |
| C16 | P4 | Queued agent messages lost across session eviction | fixed on main / awaiting release | 4 / 5 / 2 / 0 / 4 / 4 / 4 / 5 / 5 | 33 |
| C17 | P5 | Interrupted exec turn has no terminal JSON event | duplicate | 4 / 5 / 5 / 0 / 4 / 5 / 4 / 5 / 5 | 37 |
| C18 | P6 | Deleted cwd breaks daemon startup | fixed on main / awaiting release | 4 / 4 / 4 / 0 / 4 / 5 / 4 / 4 / 4 | 33 |
| C19 | P6 | Windows-mounted WSL home daemon startup | fixed on main / awaiting release | 4 / 4 / 3 / 0 / 4 / 5 / 4 / 4 / 4 | 32 |
| C20 | P7 | Cloud task workspace lacks origin remote | duplicate | 4 / 4 / 1 / 0 / 2 / 2 / 4 / 4 / 3 | 24 |
| C21 | P8 | Failed tests followed by successful final claim | candidate | 5 / 5 / 1 / 1 / 1 / 2 / 5 / 5 / 5 | 30 |
| C22 | P9 | Long task enters no-progress compaction loop | candidate | 5 / 5 / 1 / 1 / 1 / 2 / 5 / 5 / 5 | 30 |
| C23 | P10 | Subagent capacity retained below active-turn limit | duplicate | 4 / 5 / 2 / 0 / 3 / 3 / 5 / 5 / 5 | 32 |
| C24 | P10 | Subagent teardown leaves daemon descriptors open | duplicate | 5 / 5 / 3 / 0 / 4 / 4 / 5 / 5 / 5 | 36 |

## C01 — Premature completion during extended review

Recent report already covers stopping after an interim draft; no independently repeated model-backed evidence.

Existing report: [#50482](https://github.com/openai/codex/issues/50482).

Open+closed symptom/component searches:
- `"premature completion"`: 28 matches, 28 metadata records retained.
- `"stops" "review"`: 1132 matches, 50 metadata records retained.

## C02 — Repeated failed hypothesis in long coding loops

Recent symptom report has no public minimal fixture; cannot infer cause or frequency from it.

Existing report: [#50563](https://github.com/openai/codex/issues/50563).

Open+closed symptom/component searches:
- `"loop" "compact"`: 574 matches, 50 metadata records retained.
- `"repeated" "failure"`: 2874 matches, 50 metadata records retained.

## C03 — Repository constraints absent after manual compaction

Main has new remote compact context-preservation coverage. No fresh behavioral repetition justifies a claim.

Main source evidence: [86a54b05](https://github.com/openai/codex/commit/86a54b051c08f34f373c507ae16a91915ab08700). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"compaction" "constraints"`: 139 matches, 50 metadata records retained.
- `"compact" "AGENTS.md"`: 140 matches, 50 metadata records retained.

## C04 — Compaction lifecycle missing from exec JSON

Already requested in an existing focused issue; do not create another.

Existing report: [#50593](https://github.com/openai/codex/issues/50593).

Open+closed symptom/component searches:
- `"compaction" "exec"`: 728 matches, 50 metadata records retained.
- `"ContextCompaction"`: 42 matches, 42 metadata records retained.

## C05 — Memory summary middle truncation loses recent entries

Existing report identifies the same memory-summary budget behavior.

Existing report: [#48679](https://github.com/openai/codex/issues/48679).

Open+closed symptom/component searches:
- `"memory_summary.md" "truncated"`: 4 matches, 4 metadata records retained.
- `"memory" "2500"`: 8 matches, 8 metadata records retained.

## C06 — Code Mode discovery guidance changes with catalog

Latest main explicitly stabilizes discovery guidance across catalog changes.

Main source evidence: [58ca099b](https://github.com/openai/codex/commit/58ca099b03029bcffd1c56b33d31bf4913c61cc1). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"Code Mode" "catalog"`: 142 matches, 50 metadata records retained.
- `"tool discovery"`: 383 matches, 50 metadata records retained.

## C07 — MCP resource helpers unavailable in Code Mode

Main already fixes helper availability; selected case disables Code Mode to isolate a different path.

Main source evidence: [55b6f282](https://github.com/openai/codex/commit/55b6f282a810c3146a1f79c7c2e6e919cc0aa974). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"code mode" "resource"`: 178 matches, 50 metadata records retained.
- `"list_mcp_resources"`: 57 matches, 57 metadata records retained.

## C08 — Responses Lite stale incremental tool catalog

Main explicitly sends incremental catalog updates.

Main source evidence: [6326163b](https://github.com/openai/codex/commit/6326163b9abd7802c0e57be4e326e5f898bbba75). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"Responses Lite" "tools"`: 70 matches, 50 metadata records retained.
- `"catalog" "stale"`: 362 matches, 50 metadata records retained.

## C09 — Plugin tools hidden when schema budget exhausted

Existing report covers tool omission under schema budgeting.

Existing report: [#44308](https://github.com/openai/codex/issues/44308).

Open+closed symptom/component searches:
- `"schema budget"`: 12 matches, 12 metadata records retained.
- `"tools" "hidden"`: 352 matches, 50 metadata records retained.

## C10 — Aggregate MCP inventory masks server failure

Actual stable binary returns completed empty inventory for a valid server error; named control surfaces it. Needs full matrix and independent review before reporting.

Open+closed symptom/component searches:
- `"list_mcp_resources" "error"`: 42 matches, 42 metadata records retained.
- `"resources/list" "silent"`: 44 matches, 44 metadata records retained.
- `"resource" "partial"`: 129 matches, 50 metadata records retained.
- `"Failed to list resources"`: 17 matches, 17 metadata records retained.

## C11 — Resource pagination mutates opaque whitespace cursor

Source normalizes cursor through trim; runtime and prevalence not tested. Do not publish as a confirmed failure.

Open+closed symptom/component searches:
- `"resource" "cursor"`: 110 matches, 50 metadata records retained.
- `"opaque" "cursor"`: 35 matches, 35 metadata records retained.

## C12 — MCP tools/list only consumes first page

Main follows legacy tool pagination; same symptom already reported.

Existing report: [#28858](https://github.com/openai/codex/issues/28858).

Main source evidence: [cc31e374](https://github.com/openai/codex/commit/cc31e374fc15cd616fca19c07d55f9fa7e6d7e31). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"tools/list" "pagination"`: 16 matches, 16 metadata records retained.
- `"MCP" "nextCursor"`: 14 matches, 14 metadata records retained.

## C13 — Unbounded resource pagination

Existing issue; current source includes bounded pagination. No unsafe resource exhaustion experiment run.

Existing report: [#35450](https://github.com/openai/codex/issues/35450).

Open+closed symptom/component searches:
- `"resource" "pagination"`: 24 matches, 24 metadata records retained.
- `"Unbounded" "MCP"`: 482 matches, 50 metadata records retained.

## C14 — Tool-list-changed notification does not refresh catalog

Logging handler only logs notification; refresh paths and prior reports need distinction. No runtime proof.

Open+closed symptom/component searches:
- `"tools/list_changed"`: 13 matches, 13 metadata records retained.
- `"MCP" "list changed"`: 44 matches, 44 metadata records retained.

## C15 — Resume returns stale replay history

Recent main returns authoritative replay history; avoid reporting already-addressed path.

Main source evidence: [d7b0d4aa](https://github.com/openai/codex/commit/d7b0d4aa663172876871b605d53283bc0120882b). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"resume" "stale"`: 1285 matches, 50 metadata records retained.
- `"resume" "history"`: 1860 matches, 50 metadata records retained.

## C16 — Queued agent messages lost across session eviction

Main persists queued mail across eviction.

Main source evidence: [960e878d](https://github.com/openai/codex/commit/960e878df4bf87b9d7fa0849f14561d7cdcca942). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"session" "eviction"`: 63 matches, 50 metadata records retained.
- `"agent" "mail"`: 60 matches, 50 metadata records retained.

## C17 — Interrupted exec turn has no terminal JSON event

Existing focused issue documents exporter branch; add no duplicate.

Existing report: [#50585](https://github.com/openai/codex/issues/50585).

Open+closed symptom/component searches:
- `"exec" "interrupted"`: 234 matches, 50 metadata records retained.
- `"terminal turn event"`: 94 matches, 50 metadata records retained.

## C18 — Deleted cwd breaks daemon startup

Main recovers daemon startup and updater after cwd deletion.

Main source evidence: [cda82a2c](https://github.com/openai/codex/commit/cda82a2c6853b484e0ba56d38f13902adfb2a6a1). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"deleted" "cwd"`: 256 matches, 50 metadata records retained.
- `"current directory" "daemon"`: 76 matches, 50 metadata records retained.

## C19 — Windows-mounted WSL home daemon startup

Main skips daemon auto-start for Windows-mounted WSL homes; do not alter personal WSL auth.

Main source evidence: [6b43e6fe](https://github.com/openai/codex/commit/6b43e6fe1fca7c03f0b0689074cbf51100a7f9d2). Release inclusion and original symptom reproduction were not individually verified.

Open+closed symptom/component searches:
- `"WSL" "home" "daemon"`: 151 matches, 50 metadata records retained.
- `"Windows-mounted"`: 85 matches, 50 metadata records retained.

## C20 — Cloud task workspace lacks origin remote

Existing report; no reproducible cloud provisioning fixture.

Existing report: [#50575](https://github.com/openai/codex/issues/50575).

Open+closed symptom/component searches:
- `"workspace" "origin"`: 359 matches, 50 metadata records retained.
- `"Cloud" "remote"`: 476 matches, 50 metadata records retained.

## C21 — Failed tests followed by successful final claim

Requires real repeated model-backed trajectories and preregistered checks. Scripted responses cannot establish this.

Open+closed symptom/component searches:
- `"tests" "success"`: 557 matches, 50 metadata records retained.
- `"verification" "failed"`: 1228 matches, 50 metadata records retained.

## C22 — Long task enters no-progress compaction loop

Recent reports support investigating symptoms but not a new causal assertion.

Existing report: [#50563](https://github.com/openai/codex/issues/50563).

Open+closed symptom/component searches:
- `"no progress"`: 438 matches, 50 metadata records retained.
- `"compaction" "loop"`: 910 matches, 50 metadata records retained.

## C23 — Subagent capacity retained below active-turn limit

Recent report already matches symptom and has duplicate suggestion #49986.

Existing report: [#50584](https://github.com/openai/codex/issues/50584).

Open+closed symptom/component searches:
- `"agent thread limit reached"`: 30 matches, 30 metadata records retained.
- `"concurrency" "completed"`: 170 matches, 50 metadata records retained.

## C24 — Subagent teardown leaves daemon descriptors open

Existing detailed report includes descriptor counts; no new report justified.

Existing report: [#50498](https://github.com/openai/codex/issues/50498).

Open+closed symptom/component searches:
- `"subagent" "teardown"`: 84 matches, 50 metadata records retained.
- `"thread_spawn_edges"`: 62 matches, 50 metadata records retained.

Commit and release audit: see [source-audit.json](source-audit.json). For each candidate, its source/issue anchor was compared with the 200-commit keyword audit and public release notes. Source-only ideas remain unconfirmed. Selected case duplicate boundaries are in [duplicate-audit.md](duplicate-audit.md).
