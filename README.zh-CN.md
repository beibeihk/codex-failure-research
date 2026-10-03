# Codex Failure Research

面向自主编程 Agent 的可复现可靠性研究。社区项目，非 OpenAI 官方项目。

已提交唯一上游 Issue [#50636](https://github.com/openai/codex/issues/50636)，
独立审查与 CI 已通过；尚未获得维护者实质回复，也未验证上游修复。
[v0.1.0 Release](https://github.com/beibeihk/codex-failure-research/releases/tag/v0.1.0)。

项目重视问题定义：先确定被破坏的不变量，再做复现、对照、消融、查重与
根因分析。不会把一次模型失败包装成稳定缺陷，也不会向 Codex 提交代码 PR。

本次筛查 24 个候选、200 条 main 提交、100 个近期 open Issue 和 100 个近期
closed Issue。筛查不等于发现 24 个新 Bug；候选池明确区分已有报告、main 已
处理的路径和证据不足的猜测。[候选池](research/candidate_failures.md)。

首个确认案例是 MCP 资源清单的错误信息丢失：已成功初始化、明确声明支持
resources 的服务器返回合法 `-32603` 错误，无指定服务器的查询却返回成功的
空清单或不完整清单；同一服务器的具名查询会明确报错。
[失败卡片](docs/failures/F001.md)与[完整结果](reports/mcp-inventory-results.md)。

实验执行真实公开 Codex 二进制，但使用本地 Responses 协议回放固定工具
调用，隔离软件路径。**不调用真实模型、不需要 API key，也不据此估计模型
失败率。** Windows 版本矩阵与 WSL 验证结果分别记录。main 只做源码核验，
不会把 alpha 二进制称为 main build。

```sh
python -m harness.replay --codex /path/to/codex --condition error_aggregate
python -m harness.replay --codex /path/to/codex --condition error_named
```

需要 Python 3.10+ 和单独下载的 Codex 二进制。默认回放无第三方依赖；若启用
请求压缩，安装可选 `compressed` 依赖。实际凭据目录与配置保持原状。

公开内容包括 harness、最小合成 fixture、版本化 JSONL、客观 scorer、schema、
统计报告、失败分类、脱敏器、测试、CI 与技术报告。完整请求、私人会话、
凭据、个人路径和账户标识不收集、不上传。[隐私规则](docs/privacy.md)。

研究方法见[methodology](docs/methodology.md)；架构学习、白板讲解和 30 个
面试题参考答案见[学习指南](CODEX_FAILURE_RESEARCH_STUDY_GUIDE.md)。
当前案例属于 **harness 层**，未证明真实模型的长期任务失败，也未声称上游
已经修复。[技术报告](docs/technical-report.md)。

只在通过最新版验证、查重、对照与独立评审后提交一个官方 Issue；若未达
门槛则不提交。安全问题遵循官方私密报告流程。[披露规则](docs/responsible-disclosure.md)。
