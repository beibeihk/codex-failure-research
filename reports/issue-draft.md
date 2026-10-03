### What version of Codex CLI is running?

Reproduced with current stable `codex-cli 0.160.0`, previous stable `0.159.3`, and
`0.162.0-alpha.10`. Current main source checked separately at
`b741e480e203f037ca726bc2a76d99a8e8668e66`; I did not build main.

### What subscription do you have?

Not applicable: the reproduction uses a loopback scripted Responses endpoint;
no OpenAI API key, subscription, or real model inference is required.

### Which model were you using?

No model inference. The custom local provider accepts the `gpt-5.2` slug and
replays a single advertised inventory tool call to isolate the client path.
This is a deterministic harness/tool failure, not a model reliability result.

### What platform is your computer?

Windows x64, NT build `10.0.26200`; also verified on Linux x86_64 under WSL2
(`6.18.40.1-microsoft-standard-WSL2`). Platform and binary hashes are recorded.
Safe runtime metadata was captured on the same hosts after the confirmatory
matrix; it is linked with the evidence and is not asserted per run.

### What terminal emulator and version are you using (if applicable)?

Non-interactive subprocess pipes; no terminal emulator or multiplexer involved.
Python 3.12.3 on WSL; Python 3.11.5 on Windows.

### Codex doctor report

Not collected: this reproduction bypasses user config with CLI-only overrides,
requires no auth, successfully initializes its synthetic MCP server, and records
fixture-side protocol counters. Full host diagnostics are unnecessary for this
isolated error-propagation path.

### What issue are you seeing?

`list_mcp_resources({})` and `list_mcp_resource_templates({})` omit a server's
inventory error and return an unqualified successful empty/partial catalog.
The affected server initializes successfully and explicitly advertises
`capabilities.resources: {}`. It returns a valid JSON-RPC internal error
`-32603` to the inventory request, not an unsupported optional method.

Observed aggregate model-facing output:

```json
{"resources":[]}
```

The corresponding `exec --json` MCP tool item has `status: "completed"` and
`error: null`. Windows stderr contains the inventory warning, but that error
does not appear in the tool output sent to the next model request. The WSL
stderr flag was false; other WSL log channels were not inspected. A genuinely healthy empty
server returns the same inventory text. With one healthy and one failing server,
the successful resource is retained but the failed server disappears without
partialness/error metadata.

### What steps can reproduce the bug?

1. Download public Codex stable `0.160.0` for your platform.
2. Obtain the pinned minimal fixture and replay harness linked under Evidence.
3. From the research repository, using Python 3.10+:

```sh
python -m harness.replay --codex /path/to/codex --condition error_aggregate
python -m harness.replay --codex /path/to/codex --condition error_named
```

The harness starts a loopback Responses-compatible endpoint and the actual
stdio MCP subprocess. The replay asks Codex to call an advertised inventory
tool, records only its model-facing output, and stops. The fixture independently
records successful initialization and `resources/list -> -32603`. It contains
no real backend or adversarial prompt and preserves credential stores/config.

Only the named control's tool arguments change from `{}` to
`{"server":"probe"}`. That control returns the original error and
`status: "failed"`. `mixed_aggregate`, `empty_aggregate`,
`template_error_aggregate`, and `template_error_named` exercise the relevant
ablations. `invalid_aggregate` is an additional, separately identified malformed
payload check; it is not needed for the valid-error reproduction.

### What is the expected behavior?

Preserve the failure of a resource-supporting server in the model-facing
inventory result. Best-effort aggregation can retain healthy resources while
identifying unavailable servers or marking the inventory partial. A complete
empty inventory must remain distinguishable from a failed query.

**Proposed invariant / expected behavior:** a declared-resource server's inventory error must not
become an unqualified successful empty/partial catalog.
This is an error-provenance request, not a claim that an official contract
requires atomic failure. Best-effort preservation of healthy results is useful.

### Additional information

#### Reproduction rate and controls

Windows results below are **failed invariant / valid software executions**;
they are not rates of spontaneous model behavior. Each cell is repeated
independently in a fresh ephemeral exec invocation, with pilots excluded.

| Condition | 0.160.0 | 0.159.3 | 0.162.0-alpha.10 |
|---|---:|---:|---:|
| Valid `-32603`, aggregate resources | 10/10 | 10/10 | 10/10 |
| Same error, named server | 0/10 | 0/10 | 0/10 |
| Healthy resource, aggregate | 0/10 | 0/10 | 0/10 |
| Healthy empty catalog, aggregate | 0/10 | 0/10 | 0/10 |
| One failing + one healthy server | 10/10 | 10/10 | 10/10 |
| Valid `-32603`, aggregate templates | 10/10 | 10/10 | 10/10 |
| Same template error, named server | 0/10 | 0/10 | 0/10 |

The named error passes the **error-visibility invariant**, not resource retrieval.
The generated full table includes durations, tool counts, malformed-payload
ablation, WSL replication, and all execution exclusions.

There were 240 valid Windows executions (eight conditions × ten repetitions ×
three versions) and 24 valid WSL stable executions (eight × three), with zero
execution exclusions. WSL reproduced aggregate resource/template and mixed
failures in 3/3 each; named, healthy, and genuine-empty controls violated the
invariant in 0/3 each. These counts are software reproduction checks, not
estimates of stochastic agent failure or real-world prevalence.

#### Evidence

Public evidence pinned to commit `cacc0d77cdc3d7aa8fefd1065c70575205747e19`:

- [Minimal fixture](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/fixtures/mcp_inventory/server.py)
- [Replay harness](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/harness/replay.py)
- [Standalone instructions](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/docs/minimal-reproduction.md)
- [Windows records (240)](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/results/confirmatory-windows.jsonl)
- [WSL records (24)](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/results/confirmatory-wsl.jsonl)
- [Generated results and controls](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/reports/mcp-inventory-results.md)
- [Duplicate/current-source audit](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/research/duplicate-audit.md)
- [Technical report](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/docs/technical-report.md)
- [Safe post-run runtime metadata](https://github.com/beibeihk/codex-failure-research/blob/cacc0d77cdc3d7aa8fefd1065c70575205747e19/research/runtime-metadata.json)

#### Source mechanism and design hypothesis

High confidence in the observed mechanism: aggregate resource/template calls
reach [`collect_resource_results`](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/codex-mcp/src/binding_clients.rs#L137-L156). Its error
branch logs a warning without preserving the server error in its returned map.
The [core resource handler](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/core/src/tools/handlers/mcp_resource.rs#L351-L370) serializes that map with a success flag. Named calls
instead propagate their `Result` error. The same path remains in inspected main.

Preserving per-server failures alongside healthy catalogs is a possible design
direction, not a validated patch. I have not demonstrated downstream model-task
harm or measured real backend-outage prevalence. No model change is proposed.

#### Related reports checked

#6217 already records aggregate emptiness versus a named `-32601` error, so
this symptom and possibly the error-dropping mechanism are not claimed as new.
#11264, #14242 and #6215 concern tools-only servers and empty-resource
interpretation; #37468 concerns `-32601` and optional capability probing;
#25061 concerns a non-returning resource probe. This reproduction instead uses
a successfully initialized, resource-advertising server and an immediate valid
internal error. Happy-path results remain available; failure provenance is lost.
The contribution is stronger evidence under this declared-resource/internal-error
condition. I found no report with this complete predicate in the recorded searches, but
will defer to maintainers if an existing canonical issue should receive the evidence.
