# Paper Review Atlas · 论文审查图谱

**把中文、英文论文变成可定位、可修改、可复核的审稿任务。**

Atlas 面向论文作者、博士生与研究团队：审查研究论证、实验、统计、代码、图表和写作，给出具体修改，并在修改后逐条验收。重点支持 AI、LLM、Agent、RAG 和知识图谱研究，也按研究类型调用一般科学审查流程。

[English](README.en.md) · [逐技能特色](docs/FEATURE_MATRIX.md) · [真实论文示例](docs/validation/real-react-review.md) · [测试记录](docs/validation/v1.1-audit.md) · [扩展定位](docs/EXTENSION_INDEX.md)

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
Paper Review Atlas
├── 证据与溯源
│   ├── C01 材料接收与溯源
│   ├── C04 主张—证据闭环
│   ├── C24 引文与引用支持
│   └── C36 报告与能力来源
├── 贡献与论证
│   ├── C02 目标期刊与会议适配
│   ├── C03 创新性与文献定位
│   ├── C05 论证与反例
│   └── C26 局限与效度威胁
├── 实验设计
│   ├── C07 实验设计与因果边界
│   ├── C08 基线与预算公平
│   ├── C09 消融与归因
│   └── C14 稳健性与泛化
├── 评测有效性
│   ├── C10 泄漏与污染
│   ├── C11 统计推断
│   ├── C12 人工与大模型评测
│   └── C13 系统性能与资源成本
├── 方法与复现
│   ├── C15 理论、公式与证明
│   ├── C16 产物与复现
│   ├── C17 代码与结果一致性
│   └── C31 数据集与基准论文
├── 图表与数值
│   ├── C18 数值追溯与一致性
│   ├── C19 图形视觉检查
│   ├── C20 图形与科学结论
│   └── C21 表格语义与可比性
├── 中英文写作
│   ├── C06 结构与叙事
│   ├── C22 中英文书写审校
│   ├── C23 保留证据的改写
│   └── C34 翻译与跨语种保真
├── 审稿与修改
│   ├── C25 伦理与研究安全
│   ├── C27 多视角审稿与裁决
│   ├── C28 修订追踪与复核
│   └── C29 回复审稿人与申辩
└── 交付与扩展
    ├── C30 投稿与提交检查
    ├── C32 综述与文献评述
    ├── C33 能力地图与扩展
    └── C35 文件格式与渲染
```

输入材料 → 主张与证据 → 方法/实验/统计 → 数值/图表 → 语言/引用 → 质疑与裁决 → 修改 → 复核。

[SVG 图](docs/coverage.svg) · [纯文本文件](docs/coverage.txt) · [详细能力登记](docs/CAPABILITY_MAP.md)

## 36 项能力与作用

点击编号可直达执行协议。

| 编号 | 能力 | 作用与输出 |
|---|---|---|
| [C01](skills/paper-review-atlas/references/review-contract.md) | 材料接收与溯源 | 整理版本、原稿、附件、原图、结果和代码，建立材料清单 |
| [C02](skills/paper-review-atlas/references/citations-venues.md) | 目标期刊与会议适配 | 对照目标期刊/会议读者、范围和具体标准，给出适配路线 |
| [C03](skills/paper-review-atlas/references/argument-novelty.md) | 创新性与文献定位 | 比较最近邻工作，明确已知内容、真实差异和贡献定位 |
| [C04](skills/paper-review-atlas/references/argument-novelty.md) | 主张—证据闭环 | 把每个重要主张连到实验、理论、图表或文献 |
| [C05](skills/paper-review-atlas/references/argument-novelty.md) | 论证与反例 | 找出逻辑跳跃、反例、替代解释和缺失前提 |
| [C06](skills/paper-review-atlas/references/bilingual-writing.md) | 结构与叙事 | 调整标题、摘要、章节和段落，使问题、方法、结果衔接 |
| [C07](skills/paper-review-atlas/references/experiments-statistics.md) | 实验设计与因果边界 | 把主张转成可检验假设、对照、独立单位和实验决定 |
| [C08](skills/paper-review-atlas/references/experiments-statistics.md) | 基线与预算公平 | 核对数据、模型、调参、token、调用次数和硬件公平性 |
| [C09](skills/paper-review-atlas/references/experiments-statistics.md) | 消融与归因 | 检查消融能否识别模块作用、交互效应和额外预算贡献 |
| [C10](skills/paper-review-atlas/references/experiments-statistics.md) | 泄漏与污染 | 追踪切分、标注、检索、缓存和未来信息泄漏路径 |
| [C11](skills/paper-review-atlas/references/experiments-statistics.md) | 统计推断 | 检查配对、重复测量、效应量、区间、检验与多重比较 |
| [C12](skills/paper-review-atlas/references/experiments-statistics.md) | 人工与大模型评测 | 检查评委盲化、评分量表、顺序、自偏好与人工一致性 |
| [C13](skills/paper-review-atlas/references/experiments-statistics.md) | 系统性能与资源成本 | 检查端到端延迟、吞吐、内存、能源、费用与测量条件 |
| [C14](skills/paper-review-atlas/references/experiments-statistics.md) | 稳健性与泛化 | 检查数据变化、长任务、缺工具、噪声和预算变化下的表现 |
| [C15](skills/paper-review-atlas/references/formal-theory.md) | 理论、公式与证明 | 核查符号、维度、假设、证明、反例与复杂度增长区间 |
| [C16](skills/paper-review-atlas/references/code-reproducibility.md) | 产物与复现 | 把图表连接到环境、数据、命令、运行日志与输出 |
| [C17](skills/paper-review-atlas/references/code-reproducibility.md) | 代码与结果一致性 | 核对指标实现、真实标签、配置和结果的对应关系 |
| [C18](skills/paper-review-atlas/references/figures-tables.md) | 数值追溯与一致性 | 重算声明的CSV/JSON值，区分均值、最大值、单位和舍入 |
| [C19](skills/paper-review-atlas/references/figures-tables.md) | 图形视觉检查 | 实际检查坐标、标注、图例、颜色、字体和裁切 |
| [C20](skills/paper-review-atlas/references/figures-tables.md) | 图形与科学结论 | 判断图能支持什么结论，设计替代图与可直接采用的图注 |
| [C21](skills/paper-review-atlas/references/figures-tables.md) | 表格语义与可比性 | 检查表头、分母、指标方向、最优值和比较条件 |
| [C22](skills/paper-review-atlas/references/bilingual-writing.md) | 中英文书写审校 | 检查中英文语法、术语、长句、重复与学术表达 |
| [C23](skills/paper-review-atlas/references/bilingual-writing.md) | 保留证据的改写 | 给出原句—改句—理由，实施已授权修改并保护科研含义 |
| [C24](skills/paper-review-atlas/references/citations-venues.md) | 引文与引用支持 | 核对文献身份、引用支持、本地BibTeX键与原始条目 |
| [C25](skills/paper-review-atlas/references/review-contract.md) | 伦理与研究安全 | 检查参与者、隐私、授权、数据发布和双重用途问题 |
| [C26](skills/paper-review-atlas/references/argument-novelty.md) | 局限与效度威胁 | 把局限和效度威胁对应到具体结论，说明已有缓解 |
| [C27](skills/paper-review-atlas/references/adversarial-review.md) | 多视角审稿与裁决 | 挑战、辩护、裁决并撤回误报；支持引导问答和标注集校准 |
| [C28](skills/paper-review-atlas/references/revision-rebuttal.md) | 修订追踪与复核 | 用稳定ID跟踪修改，重跑验收条件并发现问题回归 |
| [C29](skills/paper-review-atlas/references/revision-rebuttal.md) | 回复审稿人与申辩 | 逐条回应审稿意见，明确修改位置、合理异议和待做工作 |
| [C30](skills/paper-review-atlas/references/citations-venues.md) | 投稿与提交检查 | 检查目标要求、投稿信、补充材料和最终交付稿 |
| [C31](skills/paper-review-atlas/references/argument-novelty.md) | 数据集与基准论文 | 检查数据集代表性、标注、版本、许可与榜单治理 |
| [C32](skills/paper-review-atlas/references/domain-agent.md) | 综述与文献评述 | 检查综述检索范围、筛选、分类、遗漏和选择偏差 |
| [C33](skills/paper-review-atlas/references/input-output.md) | 能力地图与扩展 | 按能力、来源特色或缺口ID定位文件、测试和补强步骤 |
| [C34](skills/paper-review-atlas/references/bilingual-writing.md) | 翻译与跨语种保真 | 保持翻译前后的数值、否定、比较、不确定性与因果关系 |
| [C35](skills/paper-review-atlas/references/input-output.md) | 文件格式与渲染 | 按PDF、Word、LaTeX、Typst分流，保护公式、标签和引用 |
| [C36](skills/paper-review-atlas/references/input-output.md) | 报告与能力来源 | 输出带位置、证据、严重度、改法和验收条件的报告 |

### AI / Agent 专项

覆盖意图路由、RAG、规划/工具/长期记忆、答案生成与自评、多 Agent 协作、知识图谱与本体。检查重点包括：多 Agent 是否只是增加了采样和调用预算；测试答案是否进入检索索引；记忆是否跨测试集污染；失败重试是否计入成本；图结构是否真的贡献增益。

## 11 种工作模式

| 模式 | 用途 |
|---|---|
| `full` / `quick` | 全文审查 / 主要问题快速分诊 |
| `experiments` / `figures` / `writing` | 实验、图表、写作专项 |
| `revise` / `rereview` | 实施修改 / 逐条验收 |
| `rebuttal` / `submission` | 回复审稿 / 投稿准备 |
| `guided` / `calibration` | 引导作者理解并修复问题 / 对照标注评估审查行为 |

模式可串联，例如：`full → revise → rereview → submission`。

## 来源特色如何互补

61 个来源模块被展开为 **227 个特色检查点**。每个模块有稳定 `Fxxx` 编号、实现位置、互补路径和一个代表案例，见[逐技能矩阵](docs/FEATURE_MATRIX.md)与[案例记录](docs/FEATURE_WALKTHROUGH.md)。

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
| SRC01 · [augustocamargo/paper-reviewer-skills](https://github.com/augustocamargo/paper-reviewer-skills) | 29 |
| SRC02 · [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 1 |
| SRC03 · [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) | 6 |
| SRC04 · [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | 1 |
| SRC05 · [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 7 |
| SRC06 · [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 4 |
| SRC07 · [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | 3 |
| SRC08 · [CloudWave818/ieee-skills](https://github.com/CloudWave818/ieee-skills) | 3 |
| SRC09 · [manoloss612/peer-review-skill](https://github.com/manoloss612/peer-review-skill) | 1 |
| SRC10 · [GuangyaoYin/skill-scientific-manuscript-review](https://github.com/GuangyaoYin/skill-scientific-manuscript-review) | 1 |
| SRC11 · [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 3 |
| SRC12 · [slark-prime/ml-paper-writing](https://github.com/slark-prime/ml-paper-writing) | 1 |
| SRC13 · [scdenney/open-science-skills](https://github.com/scdenney/open-science-skills) | 1 |

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

16项冲突规则包含舍入、问题配额、统计单位、格式偏好、证据缺失、跨语言保真、多角色来源和修改验收。58个固定输入案例对比两类明确规则：所选规则58项符合预期，对照规则13项符合预期。输入、规则实现和输出都在[测试记录](docs/validation/v1.1-audit.md)中。

| 工具 | 功能 |
|---|---|
| `plan` / `preflight` | 选择协议、检查材料清单 |
| `audit` | 引文锚点、数值、单位、舍入、配对描述统计 |
| `policy` | 依据明确证据记录处理 CFX01–CFX16 冲突 |
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

返回：能力编号、来源特色、协议路径、互补能力、缺口、修改入口、测试命令和验收条件。[扩展索引](docs/EXTENSION_INDEX.md)登记了12个具体后续方向，如复杂统计、跨模型执行、格式适配、引用核验和图表视觉基准。

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

原创实现使用 [MIT](LICENSE)；外部来源保留各自许可。完整来源与版本信息见 [SOURCES.md](docs/SOURCES.md)，具体实现与验证进度见[审计记录](docs/validation/v1.1-audit.md)。
