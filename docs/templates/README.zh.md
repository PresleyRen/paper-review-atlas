# Paper Review Atlas · 论文审查图谱

**把中文、英文论文变成可定位、可修改、可复核的审稿任务。**

Atlas 面向论文作者、博士生与研究团队：审查研究论证、实验、统计、代码、图表和写作，给出具体修改，并在修改后逐条验收。重点支持 AI、LLM、Agent、RAG 和知识图谱研究，也按研究类型调用一般科学审查流程。

[English](README.en.md) · [逐技能特色](docs/FEATURE_MATRIX.md) · [真实论文示例](docs/validation/real-react-review.md) · [测试记录](docs/validation/reviewer-priorities-validation.md) · [扩展定位](docs/EXTENSION_INDEX.md)

## 使用后得到什么

| 任务 | 交付成果 |
|---|---|
| 投稿前严格审稿 | 原文位置、证据、严重度、影响、改法与验收条件齐全的问题清单 |
| 实验与统计检查 | 主张—实验矩阵、预算/基线核对、消融和泄漏问题、最小充分补实验方案 |
| 图表检查 | 逐图逐表的科学含义、视觉呈现、数据核对，以及替代布局和图注 |
| 中英文修改 | 原句—改句—理由；术语、数值、否定与结论强度保持一致 |
| 返修与回复审稿人 | 稳定问题编号、变更记录、逐项复核和回应信 |
| 扩展技能 | 输入能力或缺口ID，直接找到协议、来源特色、测试和补强步骤 |

## 安装与触发

```bash
git clone https://github.com/PresleyRen/paper-review-atlas.git
cd paper-review-atlas
python scripts/install_skill.py --project /absolute/path/to/your-paper-project
```

需要 Python 3.10+。本地检查工具使用标准库；语义审稿由加载技能的模型完成。项目安装路径为 `.agents/skills/paper-review-atlas/`。在支持该目录的宿主重新加载技能后，输入：

```text
使用 $paper-review-atlas，full 模式严格审查当前论文。
报告用中文，英文原文的修改建议保持英文。
覆盖论证、实验、统计、代码与结果、全部图表、引用和写作。
每条意见给出位置、证据、影响、改法和验收条件。
```

常见触发词：论文审稿、严格审查、实验审查、图表审查、中英文论文修改、投稿前检查、返修复核。可提供 PDF、Word、LaTeX、Typst、Markdown，以及原图、结果表、配置、日志和代码。图像查看、文档编译与实验执行使用宿主提供的工具。

## 完整能力文本图

```text
{{TREE}}
```

输入材料 → 主张与证据 → 方法/实验/统计 → 数值/图表 → 语言/引用 → 质疑与裁决 → 修改 → 复核。

[SVG 图](docs/coverage.svg) · [纯文本文件](docs/coverage.txt) · [详细能力登记](docs/CAPABILITY_MAP.md)

## {{CAP_COUNT}} 项能力与作用

点击编号可直达执行协议。

| 编号 | 能力 | 作用与输出 |
|---|---|---|
{{CAPABILITIES}}

### AI / Agent 专项

覆盖意图路由、RAG、规划/工具/长期记忆、答案生成与自评、多 Agent 协作、知识图谱与本体。检查重点包括：多 Agent 是否只是增加了采样和调用预算；测试答案是否进入检索索引；记忆是否跨测试集污染；失败重试是否计入成本；图结构是否真的贡献增益。

## 审稿人关键问题与修改优先级

新增 `priorities` 模式，先找影响论文核心结论的证据缺口，再处理局部表达。全文审查和快速审查会自动加载这一流程。

```text
研究问题 → 实际贡献 → 方法与预测 → 决定性证据
                                 ↓
                        反例、替代解释与成本
                                 ↓
                 科学有效性 / 期刊适配 / 表达清晰度
                                 ↓
                    最小充分修改 → 明确验收条件
```

| 审稿关注点 | 实际作用 |
|---|---|
| 期刊标准 | 区分关注重要性的期刊和侧重科学可靠性的期刊，按目标期刊核验要求 |
| 创新与机制 | 去掉名称看具体贡献；将方法操作、变量、预测与实验连起来 |
| 决定性实验 | 区分效果提升与机制识别，检查预算、基线和替代解释 |
| 修改优先级 | 标出阻碍核心结论的问题，给出重分析、补证据或收窄主张的最小方案 |
| 阅读与图表 | 阅读附录后复核初步质疑，定位主图主表与结论的对应关系 |
| 多视角审查 | 先冻结报告再汇总，将后续数字审计与既有审稿共识分开 |

```text
使用 $paper-review-atlas，priorities 模式审查当前论文。
围绕核心结论列出重要问题、支持和反对证据、最小修改及验收条件。
分别判断科学有效性、贡献增量、期刊适配和表达问题。
```

本轮融合 Matt Might、Prem Devanbu 的审稿经验、期刊官方规则，以及 `nature-reviewer`、`review-revision` 的适用能力。[来源与采用方式](docs/REVIEWER_ADVICE.md) · [真实 ReAct 重点审查示例](docs/validation/real-react-priorities.md)

## 12 种工作模式

| 模式 | 用途 |
|---|---|
| `priorities` | 核心贡献、决定性证据、期刊标准与最小充分修改 |
| `full` / `quick` | 全文审查 / 主要问题快速分诊 |
| `experiments` / `figures` / `writing` | 实验、图表、写作专项 |
| `revise` / `rereview` | 实施修改 / 逐条验收 |
| `rebuttal` / `submission` | 回复审稿 / 投稿准备 |
| `guided` / `calibration` | 引导作者理解并修复问题 / 对照标注评估审查行为 |

模式可串联，例如：`full → revise → rereview → submission`。

## 来源特色如何互补

{{FEATURE_COUNT}} 个来源模块被展开为 **{{FACET_COUNT}} 个特色检查点**。每个模块有稳定 `Fxxx` 编号、实现位置、互补路径和一个代表案例，见[逐技能矩阵](docs/FEATURE_MATRIX.md)与[案例记录](docs/FEATURE_WALKTHROUGH.md)。

```text
实验设计 ──检查是否回答问题──> 数值核对
   ▲                              │
   │ 识别混杂                     │ 校验聚合与单位
   │                              ▼
主张—证据 <──核对图支持的结论── 图表审查
   │                              │
   └──限定可支持的措辞──> 中英文改写
                              │
                      对抗质疑 ↔ 反证裁决
                              │
                       修改记录 → 实际复核
```

例如，数值工具能验证均值，但实验设计检查负责判断是否选对比较；视觉检查发现坐标问题，原始数据核对负责确认数字；语言润色给出可用句子，主张—证据检查负责保持科研含义。质疑通过裁决排除误报，再进入修改与复核。

| 来源仓库 | 收录模块数 |
|---|---:|
{{FAMILIES}}

## 实际示例：ReAct 公开论文

对 [ReAct v3](https://arxiv.org/abs/2210.03629v3) 的结果与图表进行了检查，并将已核对的表值制作成可复算案例。

| 输入 | Atlas 的具体输出 |
|---|---|
| WebShop 表4：ReAct 40.0%，Act 30.1% | 重算为 **9.9 个百分点**；相对提升为 **32.9%**（一位小数） |
| 需要精确说明相对已有方法的提升 | 逐个比较对象给出 9.9、10.9、11.3 个百分点，提供英文替换句 |
| 主文与附录出现不同的 HotpotQA 值 | 查到附录使用500题子集，保留各自结果，记录评测范围 |
| 主图线图使用非零纵轴 | 根据实际轴标签和图形用途判断，保留清楚表达的缩放 |

示例改写：

> On WebShop, ReAct achieves a 40.0% success rate, exceeding Act, IL, and IL+RL by 9.9, 10.9, and 11.3 percentage points, respectively.

[查看完整审查、输入来源和原始运行输出](docs/validation/real-react-review.md)。另设一个故意混淆“相对百分比/百分点”的错误探针，实际运行会返回不一致。

```bash
python skills/paper-review-atlas/scripts/atlas.py audit \
  --root tests/fixtures/real_react --spec verified-spec.json
```

## 冲突测试与本地工具

22项冲突规则覆盖原有数值、统计、图表、翻译和返修检查，并增加期刊标准、机制证据、最小修复、创新判断、冻结审稿与来源归因。原有58个案例与新增36个案例均有可执行输入和输出，见[本轮测试记录](docs/validation/reviewer-priorities-validation.md)。

| 工具 | 功能 |
|---|---|
| `plan` / `preflight` | 选择协议、检查材料清单 |
| `audit` | 引文锚点、数值、单位、舍入、配对描述统计 |
| `policy` | 依据明确证据记录处理 CFX01–CFX22 冲突 |
| `export-macros` | 从核对后的数据生成LaTeX数字宏 |
| `bib-audit` | 查询本地BibTeX，保留原始条目，找重复键和缺失引用键 |
| `calibrate` | 根据已判读标签计算混淆计数、精确率、召回率等 |
| `validate-report` / `recheck` | 校验问题记录、复核实际验收条件 |
| `locate` / `capabilities` / `verify-install` | 定位补强入口、列出能力、检查安装 |

接口和示例见 [CLI_REFERENCE.md](docs/CLI_REFERENCE.md)。

## 快速定位不足并扩展

```bash
python skills/paper-review-atlas/scripts/atlas.py locate C19
python skills/paper-review-atlas/scripts/atlas.py locate academic-paper-reviewer
python skills/paper-review-atlas/scripts/atlas.py locate G03
```

返回：能力编号、来源特色、协议路径、互补能力、缺口、修改入口、测试命令和验收条件。[扩展索引](docs/EXTENSION_INDEX.md)登记了13个具体后续方向，如复杂统计、跨模型执行、格式适配、引用核验和图表视觉基准。

```text
发现不足
  └─ locate Cxx / Fxxx / Gxx
      ├─ references/：补审查步骤和输出
      ├─ scripts/：补实际检查工具
      ├─ config/features.json：更新特色与互补关系
      ├─ config/gaps.json：更新问题、补法和验收
      └─ tests/：错误例 + 正确对照 + 资料缺失例
          └─ 运行测试 → 重建README/文本图/能力图 → 提交
```

```bash
python -m unittest discover -s tests -v
python scripts/build_coverage.py
python scripts/build_feature_docs.py
python scripts/build_coverage.py --check
python scripts/build_feature_docs.py --check
python scripts/check_package.py
```

中英文 README、文本图、特色矩阵和扩展索引由登记与 `docs/templates/` 生成。修改模板或登记后重新生成，能够同步维护文档与实现。

## 目录与许可

`skills/paper-review-atlas/` 是可安装技能；`tests/` 保存测试与案例；`docs/` 保存能力、效果与验证记录；`scripts/` 维护安装和文档生成。

原创实现使用 [MIT](LICENSE)；外部来源保留各自许可。完整来源与版本信息见 [SOURCES.md](docs/SOURCES.md)，具体实现与验证进度见[审计记录](docs/validation/reviewer-priorities-validation.md)。
