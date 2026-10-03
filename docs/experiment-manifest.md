# Experiment manifest

| Artifact | Recorded value |
|---|---|
| Latest public stable checked | rust-v0.160.0, published 2026-10-01 |
| Stable source SHA | 79b1b666f2e8551f8abbbca34957227f67f3f553 |
| Previous stable checked | rust-v0.159.3 |
| Previous stable source SHA | 8e46774a94a745ffdf676bd7a8aa36466bbd4f99 |
| Prerelease checked | rust-v0.162.0-alpha.10 |
| Prerelease source SHA | 0b9e1d86d40400191c78f1f8a242aee725a02c31 |
| Main source inspected | b741e480e203f037ca726bc2a76d99a8e8668e66 |
| Main build | not executed |
| Windows | x64, NT 10.0.26200, Python 3.11.5 |
| WSL | Linux x86_64, 6.18.40.1-microsoft-standard-WSL2, Python 3.12.3 |
| Model | deterministic loopback Responses replay; gpt-5.2 routing slug; no inference |
| MCP transport | actual stdio subprocess |
| Config | command-line overrides in harness/replay.py; ignore-user-config, ephemeral, read-only |
| Repetition schedule | fixed shuffle seed 20261003; fresh process per run |
| Windows executions | 240, eight conditions × ten repetitions × three binaries |
| WSL executions | 24, eight conditions × three repetitions × stable binary |
| Pilots | ignored .cache; excluded from all public denominators |
| Dataset hashes | fixture, scenario, binary SHA-256 in every result |
| Real model/account usage | none required or measured |

Releases were downloaded separately into ignored local directories. The user's
installed Codex and credentials were not replaced. NT version 10.0 is a kernel
identifier; it does not by itself classify the Windows marketing version.

Safe [runtime metadata](../research/runtime-metadata.json) was collected on the
same hosts after the confirmatory matrix. It verifies the kernel and Python
details above; it is not a per-run capture. No hostname, address, account, or
home directory is included.
