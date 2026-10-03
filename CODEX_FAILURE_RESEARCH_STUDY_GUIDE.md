# Codex Failure Research Study Guide

这份指南帮助研究者解释实际证据。它依据公开源码和本次合成实验；不涉及
OpenAI 内部架构、训练配方或未公开服务实现。源码基线为
[`b741e480`](https://github.com/openai/codex/tree/b741e480e203f037ca726bc2a76d99a8e8668e66)。
CLI 的 main 源码与桌面产品/托管服务不是同一层，也不能把相同术语自动视为
相同实现。未执行 main build；执行版本和平台见结果记录。

## 公开架构地图

| 部分 | 公开源码入口 | 研究时关注的不变量 |
|---|---|---|
| CLI | `codex-rs/cli/src/main.rs` | 参数正确进入 exec/TUI/app-server 路径 |
| 非交互运行 | `codex-rs/exec` | JSON 事件与真实执行状态一致 |
| Core | `codex-rs/core/src/lib.rs`、`session/` | turn 生命周期、工具执行和状态更新一致 |
| Thread / Session | `core/src/codex_thread.rs`、`core/src/session/session.rs` | 恢复和追加输入保留最新状态 |
| Context | `core/src/context/`、`context_manager/` | 指令、环境、工具目录与历史的构造正确 |
| Compaction | `core/src/compact.rs`、`compact_remote_v2.rs` | 替换历史保留必要上下文；不能仅凭结果变差断言丢失 |
| Tool 执行 | `core/src/tools/registry.rs`、`tools/handlers/` | advertised schema、路由、运行结果一致 |
| MCP | `codex-mcp/src/binding_clients.rs`、`rmcp-client/src/rmcp_client.rs` | 协议错误和能力状态进入上层反馈 |
| Sandbox | `sandboxing/`、`linux-sandbox/`、`windows-sandbox-rs/` | 支持的授权操作与执行策略对应 |
| Configuration | `config/`、`core/src/config/` | 层叠配置与运行快照一致；未知字段不应静默误导 |
| App-server / Daemon | `app-server/`、`app-server-protocol/`、`app-server-daemon/` | 多客户端连接、重连和服务器状态保持一致 |
| History / Persistence | `history/`、`state/`、`core/src/rollout.rs` | 持久化、分页读取和恢复的逻辑状态一致 |

这些路径是研究入口，不构成逐模块行为的完整证明。具体代码行需要使用固定
commit 的链接核验。官方文档：
[exec](https://developers.openai.com/codex/noninteractive)、
[配置](https://developers.openai.com/codex/config-reference)、
[MCP](https://developers.openai.com/codex/mcp)、
[AGENTS.md](https://developers.openai.com/codex/guides/agents-md)、
[安全边界](https://developers.openai.com/codex/security)。

## 本次案例的白板讲法

1. **User task**：编程前发现 MCP 提供的 schema 或文档资源。
2. **Relevant state**：服务器已初始化并声明 resources，工具也已向模型公开。
3. **Trigger**：工具无指定 server 地查询清单；一个资源服务器返回合法内部错误。
4. **Failure**：聚合路径丢弃服务器错误，只返回成功的空/部分清单。
5. **Evidence**：fixture 记录 `resources/list -> -32603`；下一模型请求实际收到
   `{"resources":[]}`；JSON tool item 为 completed。正常空清单与失败清单文本相同。
6. **Source mechanism**：collector 的 error 分支只记 warning；返回 map 不含失败；
   handler 将 map 序列化为成功结果。具名路径保留 Result 的 error。
7. **Control / ablation**：具名查询、健康空清单、健康资源、混合服务器、template
   方法、前一 stable 和最新 alpha、WSL。所有原始确认记录公开。
8. **Proposed direction**：保留每个服务器的失败或标记 partial；这只是设计方向，
   没有声称实现/验证了生产修复。

可以画成：

```mermaid
flowchart LR
    A[发现编程所需资源] --> B[已初始化且声明 resources]
    B --> C[服务器返回 -32603]
    C --> D[聚合 collector 只写 warning]
    D --> E[错误未进入返回 map]
    E --> F[工具显示 completed 空清单]
    C --> G[具名路径传播 error]
    G --> H[对照显示 failed 和原错误]
```

## 30 个面试题与参考答案

**1. 什么叫 reproducible agent failure？**

在明确版本、初始环境、任务和评分不变量下，他人可以重复触发同一可观测
失败。软件缺陷关注固定触发路径；模型行为还需要频率与随机性描述。

**2. 为什么一次失败往往不够？**

单次行为可能是采样、环境波动或评分误差。确定性软件路径的一次最小复现
可以很强，但仍要检查版本、环境和替代解释。本次重复不用于推断模型能力。

**3. Deterministic bug 和 behavioral failure 有何区别？**

前者是客户端状态/协议/逻辑路径错误，可以固定工具调用隔离；后者依赖模型
规划和选择，需要真实推理、多次任务与预先定义的 verifier。

**4. 怎么设计 control？**

让两个条件共享任务、工具、服务器和错误，只改变主要变量。本次只从 `{}`
改成 `{"server":"probe"}`，比较同一错误是否进入模型可见结果。

**5. Ablation 是什么？**

改变或移除机制的一部分，检查结论是否依赖它。混合服务器显示问题不只是
全空结果；template 检查共享 collector；健康空清单排除评分禁止空结果。

**6. 如何避免 confounding？**

固定二进制、配置、初始状态和协议响应，记录版本/hash，随机化条件顺序。
版本分块仍可能受时间影响，因此不把不同版本的运行时间差解释为版本因果效应。

**7. Context compaction 是什么？**

将长历史替换为更紧凑的上下文表示，以继续运行。要区分本地摘要与远程路径，
比较替换前后模型请求中的约束。本次未测量 compaction。

**8. Tool catalog 为什么可能出错？**

模型看到的目录、schema 和运行时路由分别维护，刷新或继承失败会产生差异。
需要同时记录 advertised tool 和实际可调用状态，不凭模型口头报告判断。

**9. MCP state 如何影响 Agent？**

初始化能力、连接状态、缓存工具、认证和资源响应决定可用反馈。本次连接和
能力正常，错误在资源清单聚合后丢失，因此不应归为无法初始化。

**10. Session resume 有哪些 invariant？**

历史、完成工作、待办、约束、权限、工具状态与最新文件状态应一致。恢复后
还应重新检查可能外部变化的仓库，持久化历史不保证文件系统没变。

**11. Sandbox failure 和 model failure 怎么区分？**

先确认被请求操作是否支持、授权和可在相同策略下直接执行；检查 OS/工具
错误。模型选错操作与执行层拒绝正确操作属于不同原因，证据不足可标 ambiguous。

**12. Git state 为什么重要？**

分支切换、worktree 和未提交文件改变代码事实。Agent 若沿用旧 HEAD 或测试
输出，会把已失效的证据当作当前事实。记录 HEAD、diff 与测试时点。

**13. 怎样把 Bug 转成 eval？**

固定最小环境、触发条件和期望不变量；自动比较实际反馈。此案 verifier 对比
服务器错误计数与 model-facing output，不需要另一个 LLM 判断。

**14. Verifier 如何设计？**

检查结果和数据来源，区分实验未运行与产品失败。预定义空结果的合法情况，
也允许未来采用 partial metadata 的修复，避免把当前 implementation 写成答案。

**15. 为什么 reward 应该 verifiable？**

可检查的目标减少主观偏差，便于自动训练/评估。但 verifier 也可能遗漏真实
目标，需要隐藏测试、反例和人工审查；可验证不等于完整。

**16. Grader 会不会被 hack？**

会。只搜“error”字符串可能被无关文本欺骗。本次 scorer 同时要求真实错误
计数、对应调用和模型输出；它仍是有限规则，不能覆盖任意未来消息格式。

**17. 怎么评估 long-horizon tasks？**

预设里程碑和不变量，监测状态改变、恢复、compaction、最终验证与成本；
控制条件与处理条件均重复。不要把步数增加本身当成现实任务复杂度。

**18. pass@k 适不适合？**

适合回答 k 次尝试至少一次成功的特定问题，不直接反映单次可靠性、诊断原因
或总成本。本项目报告每条件 n 和频率；确定性错误不需要 pass@k 排名。

**19. 哪些 failure 可以靠 RL 修？**

在反馈可靠且 verifier 对齐目标时，规划、恢复、遵守约束等行为可能适合 RL。
无法从本次协议回放推出任何 RL 效果，也不能要求模型猜测被 harness 删除的错误。

**20. 哪些更应改 harness？**

工具路由、错误传播、历史替换、会话持久化和状态同步的确定性缺陷。本次
错误已经在服务器返回，collector 丢失它，修复层应优先定位反馈构造。

**21. 如何把 failure 变成 training data？**

先确认是模型行为，再制作 synthetic task、环境、失败轨迹摘要、期望行为和
verifier。本案是 harness 层，未生成或宣称模型训练轨迹。

**22. Reward 怎么定义？**

围绕任务真实目标和不可妥协约束，区分结果质量、资源成本和安全边界。本案
工具错误可见性是软件回归断言，不能直接当作模型 reward 已改善的证据。

**23. OOD 如何验证？**

保留不同仓库、任务族、服务器实现、失败类型和平台作为外部验证。版本/
WSL 复现仅扩展此软件路径覆盖，不能称为所有 coding-agent 任务的 OOD 泛化。

**24. 为什么选择此案？**

24 个筛查候选中，它有合法触发、实际 stable 复现、单变量对照、共享源码
机制和便宜的小 fixture。P0/P1 更重要，但当时没有足够重复的独立行为证据。

**25. 什么证据会推翻 hypothesis？**

若模型可见的其他标准通道已保留服务器错误，或新代码在同一复现下提供
partial/failed metadata，核心判断会改变。仅 stderr 有 warning 不能证明模型看到了它。

**26. 样本量为什么这样选？**

软件路径固定且成本低，Windows 每条件十次检查重复性和版本一致性；WSL
每条件三次做平台复现。这个样本不是用户随机样本，也不估计模型失败率。

**27. 最大限制是什么？**

使用 scripted Responses 确定工具选择，未测量真实模型后续决策、长任务危害、
远端 OAuth 服务或实际服务器故障普遍性；main 只有源码检查。

**28. 如果 OpenAI 说无法复现怎么办？**

先核对版本/hash、schema、MCP 初始化、工具是否公开、方法计数和原始不变量。
提供最小脱敏记录；按其环境重跑。若结果推翻旧结论，更新报告并接受。

**29. 进入 Codex 团队后下一步怎么做？**

先确认 aggregate best-effort 的 API 意图，设计失败 provenance 的回归测试，
验证 live/captured binding 一致性，再评估真实任务影响与兼容成本。不能假设知道内部方案。

**30. 你本人做了哪些判断，Codex 做了哪些 implementation？**

准确说明：用户提出研究目标、因果对照原则、验收门槛和贡献边界；Codex
执行公开资料筛查、harness 实现、实验与初步分析；第二 Agent 做独立复现和
反驳审查。不要把尚未由本人复核的每个判断说成独立完成；面试前需亲自重跑并能解释。

## 面试前必须懂的五件事

1. “成功工具调用”与“完整、真实反馈”为什么不同。
2. 合法 JSON-RPC `-32603`、已声明 resources 与 `-32601` tools-only 的区别。
3. Aggregate collector 丢错、named Result 传播错误的具体数据流。
4. 对照、消融、跨版本复现能支持什么，又不能支持什么。
5. 为什么这是 harness 回归测试问题；为何未证明模型失败、训练改善或上游已修复。

