# Privacy and publishing policy

We collect only synthetic fixture outcomes, tool names, synthetic resource
catalogs, fixture method/error counters, public release/source metadata,
duration, operating-system build, version/hash information, and objective
scores. These fields are sufficient to reproduce the first case.

We exclude private session files, full model requests, model conversation
bodies, HTTP headers, authorization values, cookies, credentials, email
addresses, home-directory paths, account IDs, private repository names,
nonessential machine information, and commercial usage data. No private
research manuscript, company data, or real database is used.

The replay endpoint parses requests transiently in memory. It never records
headers or full request bodies and only exports the fixture call's output.
The fixture's trace contains method, fixture mode, and synthetic error code;
no request IDs, argument paths, or account fields. Generic Codex stderr is not
persisted. One boolean records whether the expected inventory warning occurred.
Local setup diagnostics may be printed transiently for troubleshooting; they
are never included in published results.

`CODEX_HOME` and `cli_auth_credentials_store` remain unchanged. No credential
file is copied, deleted, displayed, committed, or used as a temporary fixture.
The custom local provider requires no OpenAI authentication. CLI overrides
skip user config, disable project instructions for the replay, use ephemeral
sessions, and leave persistent configuration untouched. Synthetic final output
is fixed by our replay server; no private model output is published.

`analyzers/redact.py` handles common API/GitHub keys, bearer tokens, email,
home-directory paths, account fields, supplied personal literals, and secret
environment values. Redaction is defense in depth, not proof that arbitrary
logs are safe. Collection allowlists, record-schema checks, automatic scanning,
and human/independent review are all required before publication. Raw downloads,
public issue bodies, pilots, and binaries stay in ignored `.cache/`.

If a security boundary violation is suspected, stop public evidence export and
follow [OpenAI's security policy](https://github.com/openai/codex/blob/main/SECURITY.md).
Do not publish exploit instructions. The first case concerns truthful error
propagation from a declared resource server and does not demonstrate a security
boundary violation.

