# Duplicate and current-source audit

Search snapshots are in [source-audit.json](source-audit.json). The pool has 24
screened candidates, each with symptom/component searches across open and closed
issues and source/release checks. Search results are capped at 50 per broad
query; the focused `list_mcp_resources` search was expanded to 100. Search
coverage is not a proof of novelty. Raw issue bodies stay local to avoid copying
other users' private paths or session details into this repository.

The selected case uses an initialized server that **declares resources** and
returns **`-32603` internal error**. It concerns the model-facing aggregate
result and its completed status. It does not claim missing tool discovery,
failure to initialize, or absence of an optional capability.

| Related issue | Why it is adjacent | Difference from selected predicate |
|---|---|---|
| [#11264](https://github.com/openai/codex/issues/11264) | Empty resource list interpreted as no MCP access | Healthy tools-only servers; no declared-resource inventory error |
| [#14242](https://github.com/openai/codex/issues/14242) | Agent stops at empty resources list | Tool-only server discovery/model behavior |
| [#6215](https://github.com/openai/codex/issues/6215), [#6217](https://github.com/openai/codex/issues/6217) | Aggregate emptiness versus named Method not found | Missing optional resources method, rather than internal failure of a declared resource server |
| [#37468](https://github.com/openai/codex/issues/37468) | Optional resource-template probe reports startup failure | `-32601` and absent capability; selected server initializes and advertises resources |
| [#25061](https://github.com/openai/codex/issues/25061) | Resource probe hangs before tool call | Missing response/timeout; selected response arrives immediately |
| [#16899](https://github.com/openai/codex/issues/16899) | Stdio transport degrades in long session | Connection recovery; selected first resource call uses an initialized live transport |
| [#26072](https://github.com/openai/codex/issues/26072) | Enabled server unusable to agent | HTTP initialize transport closes; no successful resource invocation |
| [#35450](https://github.com/openai/codex/issues/35450) | Resource pagination boundary | Pagination/resource caps; selected server returns one error without pagination |
| [#44308](https://github.com/openai/codex/issues/44308) | Silent tool omission | Schema-budget omission; selected resource helper is advertised and invoked |

The same source collector exists at stable `rust-v0.160.0`, previous stable
`rust-v0.159.3`, prerelease `rust-v0.162.0-alpha.10`, and main
`b741e480e203f037ca726bc2a76d99a8e8668e66`. Main's recent Code Mode resource-helper
fix (`55b6f282`) affects availability, whereas the selected replay disables Code
Mode and verifies the helper is available. Recent tool catalog, pagination,
output truncation, and context-preservation commits do not change the selected
collector's warning-only error branch.

Alternative interpretation: aggregate discovery may deliberately be best effort.
The collector mechanism and aggregate/named asymmetry may be shared with #6217;
neither is claimed as an entirely new discovery. The evidence added here is a
declared-resource server's immediate internal error after successful initialization.
The requested behavior does not require discarding healthy catalogs or throwing
a whole-operation exception. Preserving failed-server provenance or marking the
inventory partial would satisfy the invariant. A maintainer may still choose a
canonical adjacent issue; that decision will be accepted without argument.

Independent review additionally checked [#39483](https://github.com/openai/codex/issues/39483)
and [#16834](https://github.com/openai/codex/issues/16834), both concerned with
missing-method startup/retry conditions. See the [review](../reports/independent-review.md)
for its separate searches, counterexamples, and explicit novelty limits.

