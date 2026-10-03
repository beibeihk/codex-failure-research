# Publication quality gate — 2026-10-03

This records checks, including their limits. It is not a guarantee of upstream
acceptance, novelty, model-task impact, or a production fix.

| Requirement | Evidence / outcome |
|---|---|
| Current stable | Latest release rechecked as rust-v0.160.0 before publication; actual binary executed |
| Current main | b741e480 source inspected, unchanged at final check; not built |
| Duplicate review | 24 screened candidates, recorded searches, adjacent issues and independent review; novelty uncertainty explicit |
| Non-security | Synthetic inventory internal errors; no exploit, auth manipulation, escape or private backend |
| Normal-use trigger | Query an initialized resource-supporting server while its inventory backend is unavailable |
| Repetition | 240 Windows + 24 WSL valid software executions; zero exclusions; pilots excluded |
| Minimal artifact | Eight-file ZIP, 7,899 bytes; extracted standalone replay verified for aggregate and named cases |
| Expected / actual | Proposed explicit failure-provenance invariant versus completed unqualified empty/partial inventory |
| Controls | Named error, healthy resource, genuinely empty inventory |
| Ablations | Mixed servers, templates, separately labeled malformed payload |
| Privacy | Allowlist capture, redactor tests, schema/data validation, document scanning, independent audit; no private sessions published |
| Causal mechanism | Shared aggregate collector drops errors; handler serializes remaining map; named Result propagates errors |
| Alternative explanation | Best-effort may be intentional; request preserves healthy catalogs; official contract not asserted |
| Fixed evidence | Real full-SHA permalinks in final Issue draft; independent readability check |
| Independent review | Adversarial reruns, strict 264-record audit, verifier counterexamples and revision checks |
| Code checks | 23 unit tests, schemas, score/hash recomputation and deterministic report consistency |
| Public CI | Windows/Ubuntu × Python 3.10/3.12 passed on 3ba3412; final release commit checked separately |
| External-host replay | [Ubuntu public-binary workflow](https://github.com/beibeihk/codex-failure-research/actions/runs/37126639229): 24/24 valid checks; outside confirmatory denominators |
| Upstream contribution | At most one Issue; no upstream PR; no employee mentions or job-seeking content |

The original scorer had counterexamples; it was corrected after the matrix.
Raw results, predeclared scenario, fixture and all denominators remained intact.
This is a correction to evidence verification, not a redefinition of failure.

No real model inference, downstream task harm, long-horizon failure frequency,
local Rust patch, main binary execution or upstream fix is demonstrated. The
small replay validates the software path and does not represent a full coding task.
