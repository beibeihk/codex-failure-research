# Methodology

We diagnose reproducible reliability failures in normal coding workflows. This
is community research, not an OpenAI project or a cross-model leaderboard.

## Evidence and attribution

Every case separates observed fact, evidence, hypothesis, and confidence. A
visible error does not identify its causal layer. We classify attribution as
`model`, `harness`, `environment`, `evaluation`, or `ambiguous`. A scripted model
response can isolate tool execution and context construction; it cannot measure
planning quality, instruction following, or model failure frequency.

Type A cases are deterministic software paths. Type B cases concern stochastic
agent behavior and require at least ten independent repetitions, explicit
denominators, task invariants, and model/config parity. Repeated Type A runs
check reproducibility across invocations and versions, rather than estimating
general reliability. No real model-backed Type B result is claimed in v0.1.0.

## First case protocol

The invariant in [the scenario](../scenarios/mcp_inventory.json) was written
before the first pilot. Pilot runs are excluded from the confirmatory dataset.
After successful setup, repetitions increased from three to ten before starting
the matrix. Conditions are shuffled with seed `20261003` within each binary
block; versions are separate sequential blocks. Only one experimental axis
changes in the named-server control: `{}` becomes `{"server":"probe"}`. Both
conditions initialize the same resource-supporting server and receive the same
JSON-RPC `-32603` error.

Other ablations vary server health, add one healthy server, switch to resource
templates, or return a malformed resource payload. The malformed-payload arm is
reported separately from the standards-conforming error. MCP initialization,
the exact resource method, and returned error code are independently recorded
by the fixture. These counters prevent mistaking a missing server for the
selected failure.

The Responses endpoint deterministically requests the advertised resource
tool, captures only its output, and terminates with a fixed synthetic message.
The replay exercises the actual public Codex binary and actual stdio MCP
subprocess; it does not reimplement the Codex error handling being evaluated.
No OpenAI model inference is used, and no claim is made about what a real model
would conclude from the corrupted inventory.

## Scoring and reporting

`analyzers/invariants.py` checks successful initialize/initialized evidence and
one corresponding inventory request on every fixture server, expected modes,
the advertised tool and its exact server arguments, one final tool item and
model-facing output, and a clean process exit. Incomplete execution is an evaluation exclusion with
`success=null`, not a product failure. For an error condition, an explicit
server-bound error or structured per-server error metadata satisfies the
invariant. An explicit failed tool call is a successful truthfulness check,
not successful resource retrieval.
Healthy controls must retain the expected synthetic resource; mixed partial
results must preserve the healthy catalog. A genuine empty control must be empty.

Independent review found four counterexamples accepted by the original scorer:
unrelated UI failure, incidental error/partial words, a dropped healthy resource,
and missing initialization evidence. The verifier and adversarial tests were
strengthened after the confirmatory matrix, without changing the predeclared
invariant, fixture, scenario, or raw results. Recomputing all 264 scores caused
no changes. This correction is recorded in the independent review.

JSONL records include versions and SHA-256 hashes of the fixture, scenario, and
binary. Reports show n, exclusions, successes, failures, median duration, and
tool calls. Wilson intervals are descriptive only; no random user/task sample
or causal effect on model performance is implied. Failed runs and contrary
evidence remain in the dataset.

## Reporting threshold

Report at most one upstream issue after stable reproduction, current main
inspection, duplicate review, minimal fixture, controls, ablations, privacy
review, and independent adversarial review. A recent source fix is evidence
against filing a new issue. Source-only candidates remain candidates. The
fallback outcome is “No candidate met the reporting threshold.” Never invent
a failure to satisfy a contribution target.

