# Evidence-Grounded Failure Analysis for Long-Horizon Coding Agents

## 1. Introduction

Autonomous coding agents depend on the truthfulness of environment feedback.
An incomplete tool result that looks successful can distort later planning,
even when the model itself is operating correctly. This project investigates
that boundary with public Codex source and synthetic reproducible fixtures.
It follows [the current upstream contribution policy](https://github.com/openai/codex/blob/main/docs/contributing.md): detailed evidence and analysis, with no upstream code PR.

The first case is a deterministic MCP inventory error-propagation failure.
It was selected after screening 24 candidates, the latest 200 main commits,
100 recent open issues, 100 recent closed issues, and separate global searches.
The remaining candidates include known reports, recently addressed paths, and
unverified hypotheses. Screening counts are not counts of newly discovered bugs.

## 2. Failure taxonomy

[The taxonomy](failure-taxonomy.md) distinguishes context loss, stale state,
recovery failures, premature completion, false success, and tool-state mismatch.
Symptoms are distinct from causal attribution: model, harness, environment,
evaluation, or ambiguous. This case uses F07/F08 at the harness tool boundary.

## 3. Experimental harness

`harness/replay.py` starts a loopback Responses-compatible server and invokes an
unmodified public Codex binary through its official `exec --json` interface.
The server deterministically requests one advertised MCP inventory tool. A
separate stdio subprocess initializes successfully and returns a declared
resource catalog, a valid JSON-RPC error, or an experimental invalid payload.
The replay captures the inventory output in the following model request and
compares it with the independently recorded MCP method/error counters.

Full requests, headers, private sessions, credentials, and arbitrary stderr
are excluded. The model provider is synthetic; no inference is performed.
The harness never changes credential stores or `CODEX_HOME`.

## 4. Reproducibility

The scenario invariant predates execution. Pilots are excluded; the complete
confirmatory records and their generated statistics are linked in
[the result table](../reports/mcp-inventory-results.md). Windows runs cover
stable `0.160.0`, previous stable `0.159.3`, and prerelease
`0.162.0-alpha.10`. Current main at
[`b741e480`](https://github.com/openai/codex/tree/b741e480e203f037ca726bc2a76d99a8e8668e66)
was inspected separately; it was not built or executed. A prerelease binary
is never relabeled as a main build. Platform details and binary hashes are
recorded per run.

## 5. Case study: unavailable inventory becomes successful emptiness

Observed fact: when the initialized resource-supporting `probe` server returns
JSON-RPC `-32603` to `resources/list`, unscoped `list_mcp_resources({})` returns
`{"resources":[]}` and a completed MCP tool item with no error. The server's
error appears in Windows stderr but not in the model-facing output. WSL stderr
did not contain that warning; other WSL log channels were not inspected. A genuinely
empty, healthy server returns the same inventory text.

Proposed invariant / expected behavior: an inventory failure from a resource-supporting server must
remain visible in the model-facing result, instead of becoming an unqualified
successful empty or partial inventory.
This is a research requirement for feedback integrity, not proof that an
official contract requires atomic failure.

In a mixed-server condition, the healthy server's resource remains, while the
failed server disappears without partial-success metadata. Named-server calls
surface the original error. Resource-template listing exhibits the same
aggregate/named asymmetry. These are different observations of one shared
error-propagation path, not several independently filed bugs.

## 6. Controls and ablations

The named-server control changes only the `server` argument. Healthy and empty
controls establish that valid resources and genuine emptiness work. The mixed
condition establishes preservation of healthy results but omission of failure
provenance. The template variant tests a second method using the same collector.
Malformed payloads test another transport-layer failure and are clearly separate
from a standards-conforming server error. Repetitions and exclusions are visible
in the [machine-readable summary](../reports/mcp-inventory-summary.json).

## 7. Harness versus model failure

High-confidence source mechanism: both resource/template aggregate paths use
[`collect_resource_results`](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/codex-mcp/src/binding_clients.rs).
Successful catalogs enter a map; the error branch logs a warning and retains no
error in the returned map. The
[`resource handler`](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/core/src/tools/handlers/mcp_resource.rs)
serializes this map with a success flag. Named-server branches propagate their
`Result` error instead. The same collector is present at the executed tags.

This explains the runtime observation at the software boundary. The proposed
direction—preserve per-server errors/partialness alongside successful results—is
a design hypothesis, not a validated upstream patch. No local Rust patch was
built, no production fix is claimed, and no code PR is proposed. High confidence
in this propagation mechanism does not establish downstream task harm, frequency
of real backend outages, or the best public API design.

## 8. Limitations

The first case is a harness diagnosis rather than a long-horizon benchmark.
It does not measure compaction, goal drift, real model accuracy, task completion,
or training effectiveness. The replay deliberately selects the exact advertised
tool call to isolate software behavior; this is not evidence of spontaneous
model behavior. It uses stdio MCP and localhost HTTP, not remote OAuth MCP.
Repeated software executions are not independent samples of users or tasks.
There is no benchmark score or cross-agent ranking.

Best-effort aggregate discovery may be intentional. The concern is the loss of
failure provenance and completed status, not the decision to keep healthy
results. A documented contract that exposes partialness through another
model-visible channel, or a current fix that preserves the error, would weaken
or overturn the claim. Logs available only to a human do not demonstrate that
the next model request can see the error.
[#6217](https://github.com/openai/codex/issues/6217) already records aggregate
emptiness versus a named missing-method error. This case contributes evidence
for a declared-resource internal error, rather than claiming the asymmetry or
collector mechanism is wholly new. Maintainers may select a canonical related issue.

## 9. Implications for agent evaluations

Evaluate feedback integrity before rewarding downstream agent behavior. A
verifier should inspect both protocol execution and the context delivered to
the model. Successful tool transport is not equivalent to complete environment
knowledge. Failures caused by result construction belong in harness regression
tests; asking post-training to infer hidden errors addresses the wrong layer.
Model-focused cases should use real trajectories, task invariants, treatment
controls, repeated trials, and separately validated graders.

