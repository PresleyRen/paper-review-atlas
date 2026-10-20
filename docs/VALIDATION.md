# 验证记录 / Validation record

版本：v1.0.0。日期：2026-10-20。

发布后的标签、内容哈希、Python 3.10/3.12 远端 CI 和页面截图见 [发布后核验](validation/publication.md)。该后验记录保存在主分支，不改动已发布标签。

本记录将**代码行为、技能审稿行为和尚未测量的能力**分开。项目通过的检查不能解释为“论文必定通过审稿”，也不能据此估算真实论文中的漏检率。

## 1. 验证摘要

| 层次 | 实际范围 | 结果与证据 |
|---|---|---|
| 自动化单元与集成检查 | 数值、引文锚点、问题记录、复核、CLI、安装、路径边界、登记与覆盖图生成 | 88 项测试通过；[原始日志](validation/unit-tests.txt) |
| 运行包检查 | frontmatter、长度、链接、界面元数据、JSON 登记、安装文件 | 包检查及 `verify-install` 通过；[执行摘要](validation/automated-summary.json) |
| 图表生成一致性 | JSON 为唯一来源、36 个能力 ID、XML 转义、新能力扩展、过期图表检出 | 生成器检查通过；原始 SVG 已实际渲染查看；[覆盖图](coverage.svg) |
| 英文全文前向审查 | 合成 Agent/RAG 论文、数据、8 行示例代码、配置、2 张实际 PNG | 9 项有证据问题，保留合法舍入与栅格图；[完整报告](validation/forward-en.md) |
| 中文全文前向审查 | 合成多 Agent 论文、重复测量、预算混杂、数据和实际 PNG | 12 项问题，区分已见报告缺口与未知实际程序；[完整报告](validation/forward-zh.md) |
| 正确双语写作对照 | 证据范围一致、数值正确、没有必要修改的两段文字 | 0 项问题，保留原文；[完整报告](validation/forward-control.md) |
| 修改闭环正反对照 | 原稿 88%，修订真实均值应为 84%；检查记录可以故意声称通过 | 未改正仍 `open` / exit 1；改正并重算才 `closed` / exit 0；[失败记录](validation/recheck-failed.json)、[通过记录](validation/recheck-passed.json) |
| 独立上下文包复查 | CLI 数值精度、退出码、安装边界、备份发现行为 | 找到并修复 4 个具体问题，加入回归；[修复记录](validation/integration-review.md) |

本地自动化运行使用 Python 3.12.14；仓库 CI 另配置 Python 3.10 和 3.12。CI 的配置本身不等于 CI 已成功运行，实际状态以该提交对应的 GitHub Actions 记录为准。

## 2. 自动化测试具体测了什么

| 文件 | 测试数 | 关键范围 |
|---|---:|---|
| `tests/test_audit_checks.py` | 44 | CSV/JSON 数值来源、单位/舍入/容差、相对百分比与百分点、配对描述统计、缺失/非有限数据、路径越界、真实引用锚点、零问题报告、视觉记录、问题关闭证据 |
| `tests/test_cli_install.py` | 27 | 命令路由与退出码、原始十进制精度、重复 JSON 键、复核重算、独立运行包、已有安装保护、替换备份与双向目录重叠 |
| `tests/test_coverage.py` | 17 | 来源与能力互相映射、测试符号、状态及证据、路径限制、SVG 中的完整 ID、XML 转义、加入 C37 后自动扩展、生成内容过期检出 |

数值测试验证给定声明的计算规则，不判断作者是否选对了指标、数据、独立实验单位或统计模型。报告校验验证字段和可核对的位置，不判断批评的科学正确性。视觉记录检查要求文件和记录存在，不会自行“看懂”图片。

原始测试日志里如果出现 `Generated coverage files are stale`，它来自隔离临时目录的**预期失败测试**：测试故意修改一份临时图，要求生成器发现不一致并且不覆盖它。发布目录另行通过 `build_coverage.py --check`；不能把这条预期输出误读为发布文件过期。

复现：

```bash
python -m unittest discover -s tests -v
python scripts/check_package.py
python scripts/build_coverage.py --check
python skills/paper-review-atlas/scripts/atlas.py verify-install
```

## 3. 前向审查的设置与观察

三个执行者均使用新上下文，只获得技能以及各自的原始材料，不读取期望问题列表、其它案例和现有报告。它们实际查看了指定 PNG，使用了可核对的数值计算，并记录检查范围及输入哈希。原始材料在审查后保持不变。

英文案例中，执行者识别出测试答案入索引、预算不匹配、把最大值写成均值、评委身份/盲化矛盾、相对提升口径错误、过度外推和图形比例问题。它同时保留 `0.9477 → 0.948` 的合法舍入、可读 PNG 和普通破折号。示例代码仅在检查其内容后用于小型受控函数调用；没有声称完成模型训练或论文实验复现。

中文案例中，执行者识别出同源改写分割设计不足、重复测量独立单位错误、多个组件与预算同时变化、评测偏差风险、4 个百分点与 5% 相对提升混淆、全语言/全领域外推、延迟与开销主张矛盾和百分比轴标签错误。它保留了正确的秒到毫秒转换与正确均值；没有凭分割设计缺陷编造真实泄漏数量。

双语正确对照允许执行者给出“没有必要修改”。实际结果为 0 项问题，保留中英文原文。这是对“必须凑够审稿意见”和过度润色倾向的有限正面对照。

逐情形判读见 [behavioral-rubric.md](validation/behavioral-rubric.md)。9 项和 12 项是报告条数，不是审稿准确率；同一根因可以合并，严重度仍可能需要领域专家调整。

## 4. 冲突裁决的证据范围

16 项冲突均有明确候选、取舍、验收期望和具体证据路径。当前登记为：**1 项在限定确定性范围内 `passed`，15 项 `partial`**。36 项能力中，**26 项有部分验证证据，10 项尚未做端到端效果测量**。这些状态来自登记，能力表和图同步显示，避免把“流程已经写好”当作“能力已经充分证明”。

关键正反对照包括合法舍入与真实数值错误、清晰 PNG 与错误坐标、零问题文本与明显语法错误、缺少资料与已观察到的矛盾、单模型多视角与真实独立模型来源、失败修订与成功重算。具体链接见 [CONFLICTS.md](CONFLICTS.md)。

没有将上游意见按出现频次投票：当取舍依赖统计设计、科学含义或证据范围时，保留条件化规则和无法验证的部分。有限案例支持当前选择，不支持宣称已经找到了所有学科与所有模型上普遍最优的审稿策略。

## 5. 发布前修复与最后补充

独立上下文的集成复查发现并修复：JSON 命令入口的二进制浮点精度丢失；无效原文锚点被误报为证据不足退出码；安装目录仅检查单向重叠；更新备份可能被发现为第二份活跃技能。每项都保留具体复现与回归测试。

最后一轮来源检查补读了原先仅目录收录的 27 个主技能文件。因此本次 13 个来源的 61 个主技能文件均已核读；其中这 27 次读取的 blob SHA 已登记。所有附属脚本与参考文件并未穷尽审查，上游能力也未逐一移植执行。

据此补充了基准榜单治理、HCI/定性研究、系统测量、有限表面第一印象审查、复杂度增长区间、Typst/Hayagriva 保护、本地文献库检索、投稿信逐句对齐等协议。**三份前向报告来自这些末尾补充之前的开发版本；末尾补充未另做逐项前向效果测量。**最终自动化与包检查覆盖发布文件，但不替代这些新增语义流程的行为验证。

## 6. 尚未证明的部分

- 案例全部是开发者构造的合成材料，不包含用户论文；许多缺陷较明显，不能代表真实投稿难度。
- 三个新上下文仍在同一宿主模型体系中，不是不同模型家族的独立实验，也没有盲法人类专家评分。
- 没有计算真实论文的召回率、误报率、专家一致性或接收概率。
- 引用实质支持、当前 venue 规则、完整数学证明、隐私合规、真实训练复现和领域特定评估仍需要实际材料与相应工具或专家。
- PDF/OCR、DOCX、LaTeX、Typst、统计推断和视觉理解依赖宿主或外部适配器；本包没有捆绑通用解析器、编译器、显著性检验引擎或自动定理证明器。
- 在真实返修中，人工记录型关闭与重新执行的确定性关闭仍有不同证据强度，输出会保留该区别。

后续优先补真实论文盲测、跨模型复核、长周期修改回归和上述适配器测试。入口和登记规则见 [EXTENDING.md](EXTENDING.md)。

## English verification note

The release has 88 deterministic and integration tests, three fresh-context synthetic review records, and explicit passing/failing revision checks. The same host model family performed the behavioral reviews; there was no blinded human evaluation or real-paper accuracy estimate. Behavioral reports predate the final source-completion protocol additions, which remain unmeasured where applicable. A documented protocol, a structurally valid record, a recomputed number and a scientifically justified review finding are distinct forms of evidence.
