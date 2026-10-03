# v0.1.0 — Reproducible MCP inventory error-provenance study

First community research release: a model-free public-binary replay harness,
synthetic stdio MCP fixture, versioned scenarios/results, explicit inventory
verifier, redactor, schemas, tests, failure taxonomy and bilingual documentation.

- Screened 24 candidates against 200 main commits, 100 open and 100 closed issues,
  separate component searches, current source and public release metadata.
- Recorded 240 Windows executions across 0.160.0, 0.159.3 and 0.162.0-alpha.10,
  plus 24 WSL stable executions; no execution exclusions.
- Valid internal-error aggregate conditions omit server failure provenance;
  named-server, healthy-resource and genuine-empty controls distinguish the path.
- Published controls, ablations, raw synthetic records, source mechanism,
  privacy policy, technical report and independent adversarial review.
- Included a study guide with 30 interview questions and factual profile/resume material.

No real model inference, long-horizon failure rate, downstream task harm, Rust
patch, upstream fix or endorsement is claimed. Main was inspected, not built.
Best-effort aggregation may be intentional; the proposed improvement is explicit
failed-server provenance while retaining healthy catalogs. Related #6217 may
share the mechanism. See the failure card for upstream reporting status.

The small reproduction ZIP contains only the fixture and replay entry point,
documentation, scenario and license. Download Codex separately from its official
release; the ZIP does not include binaries, credentials or personal sessions.
