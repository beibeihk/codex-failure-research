# Codex Failure Research

Reproducible reliability experiments for autonomous coding agents.

This **community research project** studies failure diagnosis and interventions
in coding-agent workflows, using public Codex source and synthetic fixtures. It
is not affiliated with or endorsed by OpenAI. It does not rank model providers.

[中文说明](README.zh-CN.md)

## Motivation

The valuable contribution is a problem another engineer can reproduce and
investigate: a clear invariant, clean evidence, controls, alternative
explanations, and appropriately limited causal claims.

## Methodology

We screened **24 candidates**, **200 main commits**, **100 recent open issues**,
and **100 recent closed issues**, then investigated one deterministic software
path. [Methodology](docs/methodology.md) and the
[candidate pool](research/candidate_failures.md) distinguish screened symptoms
from independently confirmed failures.

## Scenarios

The first case examines MCP aggregate inventory error visibility. A successfully
initialized resource server returns a valid `-32603` error; an unscoped call
returns a completed empty/partial inventory, while a named call surfaces the
error. [Failure card](docs/failures/F001.md).

## Failure taxonomy

[F01–F15](docs/failure-taxonomy.md) describe symptoms separately from causal
layers: model, harness, environment, evaluation, and ambiguous.

## Reproduction harness

Python 3.10+ and a separately downloaded public Codex binary are sufficient for
the default fixture. **No API key or model inference is required.** Existing
Codex credentials/configuration are preserved.

```sh
python -m harness.replay --codex /path/to/codex --condition error_aggregate
python -m harness.replay --codex /path/to/codex --condition error_named
```

The default pilot output goes to ignored `.cache/`. For a complete experiment:

```sh
python -m harness.matrix --codex /path/to/codex --repetitions 10 --output .cache/new-matrix.jsonl
python -m analyzers.report --input .cache/new-matrix.jsonl --output-dir .cache/report
```

The server is standard line-delimited JSON-RPC MCP; the Responses replay asks
the actual Codex binary to invoke an advertised tool. Full request bodies and
headers are never recorded. [Minimal fixture](fixtures/mcp_inventory).

## Results

[Results and controls](reports/mcp-inventory-results.md) ·
[JSON summary](reports/mcp-inventory-summary.json) ·
[Technical report](docs/technical-report.md).

The records measure deterministic software executions, **not model failure
frequency**. Versions, fixture/scenario hashes, platform, tool counters, and
exclusions are recorded. Pilots are excluded.

## Privacy

[Privacy policy](docs/privacy.md): allowlist collection, redaction, validation,
and review. Private sessions, credentials, personal paths, and account IDs are
excluded. Binaries and raw public issue downloads remain local and ignored.

## Limitations

The initial case is a harness diagnosis. No real model behavior, long-horizon
task performance, RL improvement, or production fix is claimed. Main source
inspection is distinguished from executed stable/prerelease binaries.

## Responsible disclosure

Follow [the upstream contribution policy](https://github.com/openai/codex/blob/main/docs/contributing.md).
At most one evidence-backed issue; no external code PR. Security findings use
OpenAI's private process. [Disclosure policy](docs/responsible-disclosure.md).

## Related issues

[Duplicate audit](research/duplicate-audit.md) distinguishes resource-capability
and tools-only-server reports from failure provenance in a declared resource
server. Submission/resolution status appears in [the failure card](docs/failures/F001.md).

## Development

```sh
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python scripts/validate.py
python -m analyzers.report --check
```

Public CI validates code, fixtures, schemas, redaction, and report consistency.
It never calls a real model or requires a personal Codex account. Real model
experiments belong to a separately authorized local manual workflow.

