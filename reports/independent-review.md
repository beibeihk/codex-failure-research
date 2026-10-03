# Independent adversarial review

审查日期：2026-10-03。审查对象为 `reports/issue-draft.md` 及其引用的实验记录、复现代码、评分器和 duplicate audit。初审时主动寻找反证；未读取原对话、私人会话、凭据或用户配置，未检查 `.codex` 中任何文件，未发布 Issue 或 PR。复现 CLI 保持原有 CODEX_HOME，不检查或改动认证存储。

## 初审结论

**事实层面的核心观察没有被驳倒。** 我用同一公开 Windows Codex 0.160.0 二进制独立重新执行三组对照，得到聚合调用返回成功空目录、指定服务器调用保留 `-32603`、健康服务器正常返回资源的差异。再用不依赖原评分器的严格内容检查逐行核对全部 264 条 confirmatory 记录，关键工具输出、参数、初始化 trace 和资源内容一致。

**它达到报告一个有限的客户端错误来源丢失问题所需的实证门槛。** 它没有证明真实模型可靠性下降、任务损害、生产后端故障频率、主分支二进制行为、新回归或完全独立的新机制。最强的反驳仍是有意的 best-effort 设计和相邻 Issue 的组件重叠；维护者可以合理选择按接口改进或既有 Issue 的补充证据处理。

**此初审不等于当前草稿已经可以原样提交。** 下述评分、证据链接和表述问题需要处理；作者修订后的复核另行记录，不回写或删除原始实验。

## 独立复现

运行命令均在研究仓库根目录执行，输出写入 `.cache/blind-review-replays.jsonl`：

```sh
python -m harness.replay --codex .cache/tools/0.160.0/codex.exe --condition error_aggregate --output .cache/blind-review-replays.jsonl
python -m harness.replay --codex .cache/tools/0.160.0/codex.exe --condition error_named --output .cache/blind-review-replays.jsonl
python -m harness.replay --codex .cache/tools/0.160.0/codex.exe --condition healthy_aggregate --output .cache/blind-review-replays.jsonl
```

| Condition | Model-facing output | CLI item | Fixture trace | 独立运行结果 |
|---|---|---|---|---|
| `error_aggregate` | `{"resources":[]}` | `completed`, `error:null` | initialize、initialized、tools/list、resources/list；最后返回 `-32603` | 现象复现，2.484 s |
| `error_named` | `resources/list failed`，包含 `probe` 和 `-32603` | `failed`，原错误文字 | 同一初始化与错误响应序列 | 对照成立，2.093 s |
| `healthy_aggregate` | 一条 `probe` 的 `research://public/schema` 资源 | `completed`, `error:null` | 正常初始化与正常 inventory 响应 | 对照成立，3.141 s |

三次均 exit 0、两次 Responses 请求、一个最终 inventory tool item，且实际工具已被广告。该实验复用了原 replay endpoint 和 fixture，是独立执行而非独立重写整套 harness；因此它主要排除原记录不能再次复现，不单独排除两份执行共有的 harness 设计假设。哈希绑定的 fixture 源码、指定调用对照及公开客户端源码提供另两层交叉核对。

Windows 0.160.0 二进制 SHA256：`fdda5fa3cf3fb3d000b876720742857676293e4315e4b045fae6f8bd7e866d1d`。

Fixture SHA256：`65cc7d44f5439fbfc0190e7a017cc71643013c4838554eeed5c5351cb4b129bf`。

Scenario SHA256：`9b2aa3d823c45dfac8f9689ae05e56f4349c63cf26bb5f77ce8e12d8fe96c824`。

三个哈希均与 confirmatory 记录一致。本轮没有独立执行 0.159.3、alpha、WSL 或构建 main；关于它们的检查是原始记录和公开源码复核。另从三个公开 release tag 独立获取 `binding_clients.rs`，都存在相同 warning-only collector，文件 SHA256 均为 `6902fce3a1e34922a6964b522a47de4041b8251eefad0504627017fb19f06856`；本地检查的 pinned main 文件也是该哈希。来源元数据在 `.cache/blind-review-tag-source-audit.json`，这是源码证据，不是额外二进制执行。

## 原记录与评分器审计

240 条 Windows 记录、24 条 WSL 记录均有唯一 run ID；每个版本/condition 的 repetition 序列完整，原评分器重算没有差异。当前 fixture/scenario 哈希一致。独立严格检查核对了工具名和调用参数、每个 fixture 的一次初始化及一次对应 inventory 请求、指定错误进入 model-facing output、聚合 UI 文本与下一次模型请求文本相同、健康与 mixed 资源字段正确、错误聚合没有额外错误元数据；这些内容检查全部通过。

检查脚本及结果在 `.cache/blind-review-record-audit.py`、`.cache/blind-review-record-audit.json`、`.cache/blind-review-strict-check.py`、`.cache/blind-review-strict-check.json`。它们为本地审查材料，没有改动原结果或 scenario。

原结果文件 SHA256：

| File | SHA256 |
|---|---|
| `confirmatory-windows.jsonl` | `ec5c0e3dbf58957f1886da2f86bd818190cc543f16001da5f0bdc35249844e2c` |
| `confirmatory-wsl.jsonl` | `aaa3c2c412254e85ba25ebf2e45ec2d022cd920ae13aa79377eb996f334c35db` |

原 scorer 确实接受以下反例：

| 对真实记录的单独变异 | 原 scorer 判定 | 问题 |
|---|---|---|
| 聚合记录的 CLI item 改为无关的 `failed` / `Unrelated tool dispatch failure`，model-facing output 仍为空目录 | `execution_valid:true, success:true` | UI 中任何失败都会被当成目标 inventory 错误已传给模型 |
| model-facing output 改为 `probe is healthy; resource name is partial_notes` | `success:true` | server 名 + 关键词的子串匹配不是错误证据 |
| 健康资源记录的 UI/model 目录同时改为空 | `success:true` | 健康控制只检查状态，不能证明内容通路正常 |
| 删除 initialize trace，保留 inventory error trace | `execution_valid:true` | 有效执行门槛没有核对初始化证据 |

这些是构造反例，不是声称原产品输出出现了它们。现有 264 条记录没有落入这些漏洞，故反例不足以推翻本案的原始输出观察。它们阻止把原 scorer 当作普适 verifier 或单凭分数证明所有控制条件正确。修正方向：验证对应工具/参数、初始化和目标请求证据；在 model-facing 文本中确认绑定目标服务器的 inventory 错误；对 JSON partial/error 元数据按结构判断；直接检查健康资源和真实空目录内容。

## 最强替代解释与其剩余力度

1. **Best-effort 是有意设计。** 这是仍成立的规范层面反驳。[main collector](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/codex-mcp/src/binding_clients.rs#L137-L156) 的返回类型只容纳成功目录，遇错记录 warning 后跳过。实验不能证明官方原本承诺原子失败。报告应把 invariant 明确称为提出的 expected behavior，允许成功资源保留；“整体调用应失败”不是本案已证明的修复要求。另一方面，[工具 schema](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/core/src/tools/handlers/mcp_resource_spec.rs#L7-L30) 宣传省略 server 可查询所有配置服务器，没有向模型说明失败会被静默略过。因此区分完整空目录和不可用目录是有证据支持的设计请求，但仍需维护者确认契约。

2. **Server 实际没有资源能力。** 本案的哈希绑定 fixture 在 initialize 中返回 `capabilities.resources:{}`，并正常完成握手；`-32603` 为立即返回的 JSON-RPC internal error。它与不支持方法的 `-32601` 不同。该反驳不能解释本案。当前 trace 不保留 initialize 响应原文，但 fixture 源码和 SHA 可交叉验证这一声明。

3. **模型选错工具或规划失败。** 没有模型推理，且被调用 helper 在实际工具广告中存在。只能说明这条软件路径的结果，不能推出模型自主使用率或用户任务失败率；草稿已经明确限制了归因。

4. **Custom Responses endpoint 特有的路由问题。** 健康 catalog 返回、指定错误传回以及 trace 的真实 inventory 请求排除了“工具未真正调用”。[resources handler](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/core/src/tools/handlers/mcp_resource/list_mcp_resources.rs#L85-L105) 中聚合和指定路径不同，前者直接接受 map；[公共序列化路径](https://github.com/openai/codex/blob/b741e480e203f037ca726bc2a76d99a8e8668e66/codex-rs/core/src/tools/handlers/mcp_resource.rs#L351-L370) 标为成功，足以解释观察。仍不能把本轮实测扩展为所有 provider、Code Mode 或桌面前端都已独立测试。

5. **重复的确定性执行造成统计夸大。** 10/10 只是对特定软件路径的可重复性；240/24 是软件执行数。Wilson 区间不能承担总体模型/用户失败概率解释。草稿的限定准确；建议在 Issue 保留原始分子分母，置信区间只留研究附件。

6. **真实 task harm 没有证据。** 成立。实验的第二个 Responses 回合固定结束，未观察恢复、重新询问指定服务器或实际任务结果。不能声称 agent 一定被误导、无法自救或导致研究/生产损失。当前 Issue 的 error-visibility 范围可以成立，不需要先补模型任务实验。

## Duplicate audit

我重新阅读了 [#6215](https://github.com/openai/codex/issues/6215)、[#6217](https://github.com/openai/codex/issues/6217)、[#11264](https://github.com/openai/codex/issues/11264)、[#14242](https://github.com/openai/codex/issues/14242)、[#37468](https://github.com/openai/codex/issues/37468)、[#25061](https://github.com/openai/codex/issues/25061)，并从新的公开查询补查 [#39483](https://github.com/openai/codex/issues/39483) 与 [#16834](https://github.com/openai/codex/issues/16834)。最接近的是 #6217：它已经记录聚合为空、指定调用显示缺方法错误。这说明“聚合/指定结果不一致”本身不是新发现，且可能共享同一错误吞掉路径。它没有提供已声明 resources 的服务器内部错误条件。#37468、#39483、#16834 关注缺方法和启动/重试；#25061 关注不返回的 probe。本案的新的可报告证据是有效能力声明与内部错误下仍无失败来源，不是声称发现从未见过的 collector 机制。

独立 GitHub 查询（包括 open/closed，is:issue，100 条上限）的结果：

| Query predicate within openai/codex | Total | Retained |
|---|---:|---:|
| `"list_mcp_resources" "error"` | 42 | 42 |
| `"resources/list" "-32603"` | 0 | 0 |
| `"resource" "partial"` | 129 | 100 |
| `"Failed to list resources"` | 17 | 17 |

查询元数据存于 `.cache/blind-review-public-audit.json`；未保存 Issue body。零命中不是新颖性证明；宽查询被截断，GitHub 搜索也不等于完整语义审查。本轮没有确认满足完整 predicate 的现成 canonical Issue，但不能排除维护者将其合并到上述相邻报告。公开 API 的 release/tree 请求曾遇到 rate limit，源码改用固定 SHA 的公开 raw 文件获取；[0.160.0 release 页面](https://github.com/openai/codex/releases/tag/rust-v0.160.0) 本轮仍显示 Latest。

## 提交前需修正及可选加固

| 项目 | 判断 | 最小修正 |
|---|---|---|
| Evidence 仍为待固定链接 | 已知发布阻碍，不是反证 | 用实际公开、可读取的完整 SHA permalink，包含 fixture、harness、原结果、报告和 audit；不得保留占位文案 |
| Scorer 接受上述反例 | 研究工件质量问题；当前事实仍由独立严格审计支持 | 修正 verifier 并加反例测试，原记录保持不变；复算应无统计变化 |
| WSL warning 的表述 | 本轮 9 条 error/mixed/template aggregate 的 `stderr_inventory_warning` 全为 false，Windows 对应记录为 true | 只说明 Windows stderr 捕获 warning；false 不能被解释为 WSL 没有任何日志，因为未检查其他日志通道 |
| 草稿的 WSL 精确 kernel、Python 版本 | 逐行公开记录不含 kernel release 或 Python version，本轮未独立确认 | 为精确值添加安全 runtime metadata 来源，或移除证据没有记录的精确值；Windows Python 3.11.5 本轮实测 |
| Broken invariant 与官方契约 | 预期行为是研究提出的要求，尚无维护者确认 | 保留 error-provenance 请求，明确接受 best-effort 健康结果；不宣称已经证明违反官方规范 |
| 相邻报告差异 | 不能据条件不同保证非重复 | 明确 #6217 已有同样聚合/指定症状，承认可能共享机制，接受 canonical issue 处理 |
| Setup failure 会打印最后 4000 字符 stderr | 现有有效实验未触发；未发现发布泄露 | 可选：诊断只输出 allowlist 错误类别或提示本地查看；避免以后把未脱敏的初始化诊断带进公开材料 |

## 隐私与边界核对

本轮对草稿、两份结果、报告、duplicate/source audit 和三个关键源码文件做了只输出命中数的 email、home path 与常见 token pattern 检查，命中数均为 0。逐行结果只包含 synthetic catalog/error、工具字段、版本/平台、哈希和计数。代码没有设置临时 CODEX_HOME、复制 auth、修改登录或写全局配置。该检查覆盖这些拟公开材料，不等于证明整个机器或仓库中不存在秘密；没有扫描私人目录，也没有读取认证存储。

## 修订后复核

2026-10-03，作者修订后再次检查 `analyzers/invariants.py`、`tests/test_research.py`、Issue draft、methodology、technical report、duplicate audit、runtime metadata，以及 replay 的失败诊断分支。初审意见和原始反例结果保留；四个初始反例的原结果另保存于 `.cache/blind-review-record-audit-initial.json`，新 scorer 重放结果在 `.cache/blind-review-record-audit.json`。

| 初审反例 | 修订后结果 |
|---|---|
| 无关 UI failure，model-facing 仍为空 | `success:false` |
| 文本包含 probe 和 incidental partial | `success:false` |
| 健康资源被静默改为空 | `success:false` |
| initialize 证据删除 | `execution_valid:false, success:null` |

独立重算 264 条原记录，评分无变化；两份原结果文件、fixture、scenario 和独立运行的 Windows binary 的 SHA256 均与初审一致。独立运行 22 个测试全部通过，`python -m analyzers.report --check` 确认报告与记录一致。再次严格内容审计的结论不变。

草稿和正文已明确 proposed invariant 是 error-provenance 请求，允许 best-effort 保留健康结果，没有主张官方契约要求原子失败。#6217 的共享症状和可能共享 collector 机制已承认。Windows stderr warning 与 WSL flag=false/未检查其他 log channel 的差异已澄清。`research/runtime-metadata.json` 使用安全字段，并明确同一主机在 confirmatory 执行之后采集，不是逐次运行断言。本轮独立调用 Windows Python 和 `wsl.exe --exec python3` 的 `platform` 信息，核对了这两个主机的全部所列字段：Windows Python 3.11.5、WSL Python 3.12.3 和 kernel release `6.18.40.1-microsoft-standard-WSL2` 均一致；这仍然是事后主机确认而不是历史 per-run 证明。失败初始化的诊断不再打印任意 stderr。

额外反例发现一处剩余、非当前数据的限制：把 named 错误的 UI/model-facing 两处文字同时改为 `resources/list failed for probe_other: Mcp error: -32603: ...`，修订 scorer 仍通过，因为 server 绑定使用 `probe` 子串匹配。反例在 `.cache/blind-review-revision-extra-check.json`。现有记录均准确写出 `probe`，独立严格审计也核对了实际文字；因此这个边界不推翻本案事实，也不阻止窄范围 Issue。若将 scorer 当作未来通用 verifier，应进一步改为明确服务器引用或 token 边界并加入测试。

**修订复核意见：技术 reporting threshold 已满足，可以提交一个以已声明资源服务器的有效内部错误为条件、仅请求保留错误来源的 evidence-backed Issue。** 这是审查结论，不是对维护者是否按 bug 接受、新颖性、修复优先级或最终 API 设计的保证。没有新增模型任务损害证据。**目前仅剩公开发布检查：真实 evidence commit SHA 和各 permalink 必须可读取；在具体 SHA 到达之前，本审查不把外部证据就绪状态标为通过。**

## 最终修订与公开证据验收

2026-10-03，再次独立复核 `_names_server` 的精确服务器 token 边界与新增 `probe_other` 测试。此前剩余反例现在得到 `execution_valid:true, success:false`；`probe_other`、`probe-other`、`probe.other`、`xprobe`、`probe2` 均不再被当作 `probe`，准确的 `probe` 与 `` `probe` `` 仍被识别。此前非阻碍的子串边界问题已关闭，其原反例结果另存 `.cache/blind-review-revision-extra-check-before.json`，最终结果在 `.cache/blind-review-revision-extra-check.json`。这项检查验证已发现的具体边界，不宣称 scorer 对任意未来 schema 已完备。

独立运行 23 项测试全部通过；264 条原记录再次重算，评分零变化，`report --check` 再次通过。fixture、scenario、Windows binary 和两份结果文件的初审 SHA256 均未变化，没有重写原实验。

我匿名读取两个公开 commit 的 raw 文件，不使用 GitHub token，并与本地对应 commit 的 `git show SHA:path` 字节逐一比较：

| Public commit | 可读取文件 | 与对应 Git 对象完全一致 | 与验收时本地工作文件一致 |
|---|---:|---:|---:|
| `cacc0d77cdc3d7aa8fefd1065c70575205747e19` | 13/13，HTTP 200 | 13/13 | 10/13；scorer、tests、review 为预期历史版本 |
| `3ba3412fab85d5e44afee0d3af24615020646586` | 13/13，HTTP 200 | 13/13 | 13/13，比较发生在本轮附录写入之前 |

每个 commit 检查了：minimal fixture、replay harness、standalone reproduction instructions、Windows/WSL 原记录、生成结果表、duplicate audit、technical report、safe runtime metadata、scenario、scorer、independent review 和测试文件。当前 draft 的九条证据链接全部包含实际初始 SHA，对应文件都可读取。fixture、scenario 与两份 hash-bound JSONL 在这两个公开提交中也与本地原字节相同；不存在仅由换行转换造成的证据哈希漂移。验收元数据保存在 `.cache/blind-review-public-evidence.json`，其中逐项记录匿名 raw URL、HTTP 状态、SHA256、工作文件和 Git 对象比较结果。

**最终审查意见：已发现的修正项和当前公开证据可读性检查通过；可以提交这一个窄范围 evidence-backed error-provenance Issue。** 本案仍不证明 task harm、模型失败频率、官方契约违背或完全新的 collector 机制；维护者选择相邻 canonical Issue 属于合理处理。本轮只读取公开证据并更新本地报告，未创建 Issue、评论或 PR。

本轮附录产生于上述公开提交之后。最终 Issue 若升级到包含本附录的新 commit，应统一使用其真实 SHA，并机械检查这些链接仍可读取、fixture/scenario/results 的原哈希不变；不应把尚不存在的未来 SHA 写成已经验收。此次验收结论覆盖上述两个具体 commit 和当前已审查内容。
