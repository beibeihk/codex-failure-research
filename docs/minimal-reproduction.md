# Minimal standalone reproduction

The v0.1.0 release includes a small ZIP with eight files. It is sufficient to
exercise the declared-resource internal-error path without the full research
dataset or a model account. The Codex binary is downloaded separately.

1. Extract the ZIP into a fresh directory.
2. Download official Codex 0.160.0 for your platform.
3. From the extracted directory, use Python 3.10+:

```sh
python -m harness.replay --codex /path/to/codex --condition error_aggregate
python -m harness.replay --codex /path/to/codex --condition error_named
```

Compare `tool_outputs`, `mcp_items`, and `server_traces` in the printed synthetic
records. The aggregate output is `{"resources":[]}` and `completed`; the named
output contains the original `probe` / `-32603` error and `failed`. Both records
show successful initialization and the actual inventory request. `exec` itself
exits successfully in both conditions, which is distinct from the tool outcome.

Optional controls: `healthy_aggregate`, `empty_aggregate`, `mixed_aggregate`,
`template_error_aggregate`, `template_error_named`. `invalid_aggregate` is a
separate malformed-payload ablation, not the standards-conforming error case.

The endpoint binds only to localhost. It replays one advertised tool call and
does not perform model inference. Default output is ignored `.cache/pilot.jsonl`.
Credentials, CODEX_HOME and persistent configuration are not changed. Startup
stderr is not exported. If requests are compressed, the full repository exposes
an optional `compressed` dependency; standard default replay uses only stdlib.
