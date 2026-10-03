# Failure taxonomy

Taxonomy labels describe symptoms; attribution must be established separately.

| ID | Symptom | Example invariant / measurement |
|---|---|---|
| F01 | Context loss | Relevant constraint remains available in the next request |
| F02 | Stale repository assumption | Decisions match the current checkout and diff |
| F03 | Repeated tool call | Repetition has a new purpose or changes state |
| F04 | Failed recovery | Recovery preserves completed work and pending actions |
| F05 | Premature completion | All task acceptance conditions are satisfied |
| F06 | Verification omission | Required verification is executed on the final state |
| F07 | False success claim | Reported outcome agrees with execution evidence |
| F08 | Tool-state mismatch | Tool availability/result status matches runtime state |
| F09 | Session-resume inconsistency | Replayed history and filesystem assumptions agree |
| F10 | Compaction regression | A preregistered invariant changes after compaction |
| F11 | Sandbox failure | Authorized supported operation executes in its policy |
| F12 | Git-state misunderstanding | Branch, HEAD, worktree, and untracked state are correct |
| F13 | Multi-agent coordination | Results and ownership survive lifecycle transitions |
| F14 | Excessive exploration | Exploration yields progress within an explicit budget |
| F15 | Constraint violation | Forbidden file/API changes remain absent |

First case: F07 describes the **harness tool item's** completed status despite
an unavailable inventory; F08 describes the mismatch between server outcome and
model-facing tool result. These labels do not claim that a real model issued a
false final answer. Attribution is `harness`, not `model`.

Case statuses: `candidate`, `confirmed`, `reported`, `fixed`, `not reproducible`,
`duplicate`, and `fixed on main / awaiting release`. “Duplicate” in the candidate
pool means an existing report already covers the screened symptom, not that we
independently reproduced that report or that a maintainer confirmed its cause.

