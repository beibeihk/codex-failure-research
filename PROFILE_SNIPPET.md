# Codex Failure Research

Reproducible coding-agent reliability research with controlled MCP inventory
experiments, public synthetic fixtures, and evidence-grounded source analysis.

- Research repository: https://github.com/beibeihk/codex-failure-research
- Upstream issue: [openai/codex#50636](https://github.com/openai/codex/issues/50636).
- Resolution: observed in tested public binaries; no upstream fix or endorsement claimed.
- Keywords: agent evaluation, MCP, error provenance, verifiable invariants,
  controlled experiments, minimal reproduction, Windows/WSL, harness reliability.

## Resume bullets supported by the current evidence

**English:** Built a reproducible Codex reliability harness and a synthetic MCP
fixture; screened 24 candidates and performed 264 controlled software executions
across three public versions and Windows/WSL, isolating aggregate inventory
error-provenance loss with named-server and healthy-catalog controls, and
reported the evidence in openai/codex#50636 after independent adversarial review.

**中文：** 构建 Codex 可靠性复现 harness 与合成 MCP fixture，筛查 24 个候选，
在三个公开版本及 Windows/WSL 完成 264 次受控软件执行；通过具名调用、健康
资源与混合服务器对照，定位聚合资源清单中的错误来源丢失路径，经独立反驳
审查后向 openai/codex 提交证据报告 #50636。

The study uses scripted Responses replay, not real model inference. It does
not demonstrate long-horizon model failure, a production fix, or an OpenAI
employment/contributor relationship. Update resolution wording only after an
actual upstream change has been independently verified.

AI assistance: the user specified research goals, controls, thresholds and
contribution boundaries; Codex implemented the harness and performed the first
analysis, and a separate agent conducted adversarial review. The owner should
personally rerun and explain the work before presenting it in an interview.
