# RouteMind 英文稿件完整审查报告

## 1. 结论、适用范围与审查者来源

**结论：当前文件支持一项有限、可复算的描述——所给三个种子记录中，Baseline 的平均准确率为 80.0%，RouteMind 为 84.0%，相差 4.0 个百分点，即相对 Baseline 提高 5.0%。它们不能支持“路由模块单独导致增益”“固定推理预算下提高准确率”或“跨所有领域的普遍可靠性保证”。** 主要障碍包括明确暴露测试答案的检索协议、同时改变路由与资源上限的比较、与实际说明矛盾的人工盲评表述，以及均值、相对改进与图形解释不一致。[依据：`manuscript.md` L6、L9、L12–16、L19–24、L34、L41；`config.json` L4–10；`evaluation.py` L3–8；`results.csv` L1–7。]

本报告针对 `manifest.json` 声明的 **en_agent / synthetic-v1 / English / agent**，执行 `full` 审查，中文报告、英文建议文本。源稿 L3 明确说明这是软件验证用的虚构材料，所有方法、数据集、名称和数值均属虚构，不声称真实研究新颖性或现实结果。因此，下面评判的是**材料内部的科学论证、数值、代码及呈现是否一致**；不把这些缺陷解释为真实作者不端，也不把本次检查称为真实论文效度验证。目标期刊、会议和正式提交格式未提供。[依据：`manifest.json` L2–5；`manuscript.md` L3、L44。]

审查日期：2026-10-20（UTC）。主要计算记录时间为 `2026-10-20T03:13:17.720030+00:00`。没有修改稿件、配置、代码、数据或图片；所有替换文字及代码均为报告内建议，问题尚未因修订而关闭。

### 实际来源与独立性

- 执行者：当前会话子代理 `/root/forward_en`；宿主会话声明模型为 **GPT-6 Astra Pro**，继承父代理配置，未另行调用外部模型或其他模型家族。
- 论证、方法、代码、视觉、作者辩护和最终裁决均由该同一代理完成。这些是审查角度，**不是独立评审者或独立模型复现**。
- 本报告形成时未阅读其他代理的审查报告、其他 fixture、仓库测试文件或验证答案。没有独立人类专家签字、模型间一致率或审查准确率可报告。
- 使用 `skills/paper-review-atlas/SKILL.md` 及其全部 12 篇相关 reference；实际工具为本地文件读取、技能的可用性/路由辅助命令、限定数值与引文辅助函数、Python 标准库计算及两张 PNG 的实际图像查看。未访问互联网；该材料没有真实引文、真实外部新颖性主张或需要当前外部信息的目标刊物规则。

### 已有且应保留的优点

1. 配置、种子、全部六条汇总分数和可编辑图源可见，允许定位内部不一致；这里的“可见”不等于证明实验真实发生。[`config.json`、`results.csv`、`figure1.svg`。]
2. Baseline 的 80.0% 均值与全部三条分数一致；Table 2 的 `0.9477 → 0.948` 是正常的三位小数舍入。[`results.csv` L2–4；`results.json` L3–5；`manuscript.md` L23、L26–32。]
3. Figure 2 明确定位为四个示例查询的诊断热图，实际查看后文字、计数和色标可辨认；它不是必须改成矢量图的缺陷。[`manuscript.md` L36；视觉记录 V-02。]
4. L38 明确未执行假设检验、也不主张统计显著性。这个表述本身正确，不应制造“缺 p 值即无效”的问题。

## 2. 证据清单与覆盖账本

所有下列输入路径均相对于 `/workspace/scratch/4244a6de7f92/paper-review-atlas/tests/fixtures/en_agent/`。

### 2.1 实际检查的输入

| 文件 | 实际检查内容 | 检查边界 |
|---|---|---|
| `manifest.json`，40 行 | 全文；版本、语言、领域与八项声明产物；逐项存在性 | manifest 是声明，不证明实验执行 |
| `manuscript.md`，44 行 | 全文；标题、摘要、方法、两个表、两个图的说明、限制及参考文献声明 | 未提供已排版 PDF/DOCX；未评价正式页宽下的版式 |
| `config.json`，12 行 | 全文；test 索引、gold answer、过滤开关、预算、judge、种子 | 配置声明未等同于实际运行日志 |
| `evaluation.py`，8 行 | 全文静态检查；受控调用两个无外部 I/O 的函数 | 该文件自称静态合成例子；没有 Agent 实验入口 |
| `results.csv`，7 行 | 表头及六条记录；按方法分组、种子匹配、均值、样本 SD、差值、百分比换算 | 只有每次运行的汇总值，不能重算每题正确性 |
| `results.json`，7 行 | 唯一 calibration scalar、字符串数值解析、三位小数舍入 | 没有该 scalar 的公式、输入或生成代码 |
| `figure1.svg`，182 行 | 全文 XML；数值文字、轴/柱路径、裁剪范围与 PNG 含义交叉检查 | 未单独用 SVG 渲染器渲染，也未比较 SVG/PNG 逐像素一致性 |
| `figure1.png`，1152 × 736 | 通过 `view_image(detail="original")` 实际查看完整图片 | 图片真实性与最终印刷尺寸未验证 |
| `figure2.png`，1080 × 612 | 通过同一图像工具实际查看完整图片；读出八个计数 | 无独立查询日志/绘图数据，不能验证图内计数的实验来源 |

以上是全部九个本目录文件（八项 artifact 加 manifest）。技能参考材料与检查脚本是审查方法资料，不当作稿件实验结果。

### 2.2 领域覆盖

| 审查领域 | 状态 | 实际完成 | 未完成或不适用 |
|---|---|---|---|
| 研究问题、贡献、论证链 | 已检查 | 检查固定预算问题、因果归因及 universal 主张与证据范围 | 没有证明实际路由机制在其他任务上好或坏 |
| 真实学术新颖性 | 不适用/未验证 | 确认稿件明确不提出真实新颖性 | 无文献搜索；不作原创性或前沿性裁决 |
| 实验设计、泄漏、对照 | 已检查所述协议 | 跨正文、配置、索引函数核对测试答案暴露及预算差异 | 无真实检索轨迹，未测定泄漏实际造成的分数幅度 |
| Judge 与评分程序 | 部分检查 | 确认非人工、非盲化、固定顺序和同基座的描述 | 无 rubric、提示、逐次判定、顺序互换结果或人工标注 |
| 统计及算术 | 已检查可支持部分 | 全部六条汇总值复算、样本 SD、按种子标签对齐的差值 | 不把三个标签证明为独立随机实验；未算 p 值或置信区间 |
| 代码—结果一致性 | 部分检查 | 静态函数语义及小规模动态诊断；核对均值/最大值 | 无表格生成调用链、完整路由实现、模型调用或模型权重 |
| 图形视觉 | 已检查两张 PNG | V-01、V-02 记录真实观看观察 | 未检查期刊缩放、灰度印刷、完整页面排版 |
| 图表底层数值 | 部分检查 | Figure 1/Table 1 对 CSV；Table 2 对 JSON | Figure 2 只有图上计数；calibration 原始计算未验证 |
| 英文学术写作 | 已检查 | 语法、术语、量词、因果强度、数字和图注；给出英文替换 | 没有直接改写源文件 |
| 引用、投稿规范 | 不适用 | 检查无外部引用及无目标 venue 的事实 | 无 DOI 验真、来源支撑或实时投稿规则核验 |
| 理论/数学证明 | 正式证明审查不适用 | 检查从局部观察推到普遍保证的逻辑越界 | 无定理、证明或形式化算法；未使用证明助手 |
| 人体研究/临床伦理 | 不适用 | 稿件明确没有人工标注者 | 不强加临床报告清单或推断缺失审批 |

## 3. 主张—证据—替代解释

| ID | 原文主张与位置 | 可用证据及最强替代解释 | 当前裁决 |
|---|---|---|---|
| C1 | L6：`88.0% mean accuracy over three seeds` | RouteMind 三值为 0.80、0.84、0.88；其均值 0.84、最大值 0.88 | 与声明的均值聚合矛盾；不能用“最佳种子”暗中解释 |
| C2 | L6：`a 20% relative improvement over the baseline` | 校正均值 0.84 vs 0.80 给出 5%；即使用原表 0.88 vs 0.80 也为 10% | 不是舍入误差；20% 可对应另一指标“校正后错误率相对下降”，但稿件没有这样定义 |
| C3 | L9：`under a fixed inference budget` | token 上限 600 vs 2400；检索调用上限 1 vs 4 | 该研究问题尚未被当前比较回答 |
| C4 | L6：`The routing module alone causes the gain.` | 路由、token 上限及调用上限同时变化，无匹配预算对照 | 资源变化可解释分数差异，无法识别路由的单独因果效应 |
| C5 | L6：`universally improves reliable reasoning across all domains`；L41：`universal guarantee` | 一个英文 QA 基准、一个 checkpoint；未测医学、法律、多语或交互任务 | 现有证据不支持普遍保证；不是已证明所有未测领域效果为负 |
| C6 | L16：`independent blinded human assessments` | 同段承认 LLM、方法可见、提出方法先出现、同基座且无人参与；配置一致 | 评估身份和盲化描述直接矛盾；具体偏差大小未知 |
| C7 | L34：`dramatic tenfold improvement` | 图上为 80 与 88；原值比 1.10；截断后可见柱高比约 9:1；校正均值比 1.05 | 十倍主张不成立；柱高不可解释为准确率比 |
| C8 | L26–32：calibration ratio 0.948，底层 0.9477 | JSON 单值舍入匹配；稿件明确这不是准确率 | 显示数值通过；该统计量的定义和上游生成尚未验证 |
| C9 | L36：Figure 2 是四个查询的 illustrative trace | 实际查看得到 Baseline 全为 1；RouteMind 为 2、3、4、2 | 图面与示例定位一致；不能推断总体平均成本或优势 |
| C10 | L38：未做检验，不主张显著性 | 全文没有另一个明确的统计显著性声明 | 保留该限定；无需为描述性六条记录自动追加假设检验 |

## 4. 数值核对：算法、单位与实际结果

### 4.1 聚合规则

遵照 Table 1 的明确说明，以**运行**为等权聚合单位；每个方法使用全部三个 seed ID 11、22、33。读取 `accuracy` 为 fraction，计算后乘 100 转成 percent，再按表格的一位小数显示。没有筛除种子、改变权重或为了匹配表格而改聚合方法。样本标准差用分母 `n−1`；它描述这三条运行分数的离散程度，不是均值标准误，也不是跨领域置信区间。

| 方法 | seed 11 | seed 22 | seed 33 | 均值 | 样本 SD | 最大值 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 79.0% | 80.0% | 81.0% | **80.0%** | 1.0 个百分点 | 81.0% |
| RouteMind (`proposed`) | 80.0% | 84.0% | 88.0% | **84.0%** | 4.0 个百分点 | 88.0% |
| 按同 seed 标签相减 | +1.0 pp | +4.0 pp | +7.0 pp | **+4.0 pp** | 3.0 pp | 不用于均值主张 |

计算来源：`results.csv` L2–7；实际执行 `audit_checks.paired_run_stats`，返回 `n=3`、上述均值和样本 SD、`p_value=null`、`confidence_interval=null`、`inference_status="unverified"`。同名种子允许描述性对齐，**并不独自证明配对实验的随机化或独立性**。100 个题目、3 个运行以及 LLM 判定次数是不同的数量，不能换算成 300 个已验证的独立重复。[对数量的稿件声明见 `manuscript.md` L12、L16。]

### 4.2 效应大小

正确的绝对准确率差：

\[
100\left(\frac{0.80+0.84+0.88}{3}-\frac{0.79+0.80+0.81}{3}\right)=4.0\text{ percentage points}.
\]

正确的相对准确率改进：

\[
\frac{0.84-0.80}{0.80}\times100\%=5.0\%.
\]

即使暂时接受错误的 88% 均值，`(0.88−0.80)/0.80 = 10%`，仍得不到稿件中的 20%。校正后错误率从 20% 到 16%，其相对下降 `(0.20−0.16)/0.20 = 20%`；这是另一种指标。它可解释一个可能的作者意图，但不能在没有定义的情况下把“relative improvement [in accuracy]”自动改读为错误率下降。

### 4.3 有限数值审计结果

这些声明是**审查者根据稿件构造**，不是作者附带的审计规范。使用技能公开函数 `reconcile_number`；准确率单位 `fraction→percent`，calibration 为 `number→number`，tolerance 为 0，显示舍入模式为 `half_even`。所涉数值都不在平局边界，换成常见的 `half_up` 也不会改变这里的结论。

| 核对对象 | 操作/筛选 | 声称值 | 重算显示值 | 工具状态 |
|---|---|---:|---:|---|
| Table 1 Baseline | CSV `model=baseline`，mean，3 行，1 位小数 | 80.0% | 80.0% | `verified` |
| Table 1 RouteMind | CSV `model=proposed`，mean，3 行，1 位小数 | 88.0% | 84.0% | `mismatch`；差 4 pp |
| 摘要 relative gain | 两方法 mean 后相对基线计算，1 位小数 | 20.0% | 5.0% | `mismatch`；差 15 个百分比数值单位 |
| Table 2 calibration | JSON `metric=calibration_ratio`，value，1 行，3 位小数 | 0.948 | 0.948 | `verified` |

Table 2 的 0.0003 显示差来自合法舍入，不是数据漂移，不应算作错误。它也不能与 accuracy 混合平均。此处只验证给定 scalar 的显示，未验证 scalar 本身由什么计算产生。

### 4.4 代码实际执行到了哪一步

静态检查全部八行后，通过 `runpy.run_path` 加载 `evaluation.py`，只对两个函数做局部诊断：

- `reported_score([Decimal('0.79'), Decimal('0.80'), Decimal('0.81')]) → Decimal('0.81')`。
- `reported_score([Decimal('0.80'), Decimal('0.84'), Decimal('0.88')]) → Decimal('0.88')`。
- 对审查者自造的一条记录 `{'question': 'reviewer toy question', 'gold_answer': 'reviewer toy answer'}` 调用 `build_index`，得到 `{'question': 'reviewer toy question', 'text': 'reviewer toy answer'}`。

前两项确认 `reported_score` 返回最大值；第三项确认该函数把 `gold_answer` 直接写入索引文本。**这不是重跑检索、生成或评分，不是复现 100 题结果。** 模块没有网络调用或训练入口。尤其，Baseline 表格为 80%，而该函数对 Baseline 返回 81%；缺少表格生成调用链，不能断言 Table 1 的两个数都由这一个函数实际生成。

## 5. 按影响排序的问题

下列九项均是目前版本的活动问题。`confirmed` 表示所列矛盾、实现语义或报告缺口有观察依据，不表示其潜在真实实验影响都已经测定。

### PRA-EN-001 — 所述检索协议暴露同一测试集的答案，不能支持独立泛化评估

- **状态 / 严重性：** `confirmed` / `critical`。
- **定位与精确锚点：** `manuscript.md` L12：`The retrieval index is built from all benchmark question records and includes each record's gold_answer field.`；同段：`The same 100 questions are then evaluated without filtering matching records from retrieval.`；`config.json` L4–7 为 test split、test index、gold_answer、`exclude_evaluation_question: false`；`evaluation.py` L4：`return [{"question": r["question"], "text": r["gold_answer"]} for r in records]`。
- **证据性质 / 实际来源：** observed 的正文、配置、函数语义及 toy 输入输出；inferred 的科学后果。审查者实际调用的 toy case 证明函数行为，不证明真实运行检索到了哪一条。
- **后果：** 该设置让被评估问题的标准答案直接成为可检索内容；结果无法用作独立于测试答案的推理/泛化能力证据。这直接影响中心效果主张，故列 `critical`。缺少逐题轨迹意味着泄漏带来多少分无法量化；不声称每次回答均抄取答案。
- **最强作者辩护与裁决：** 正常 RAG 的外部知识材料当然可以包含答案相关信息；“语料能回答问题”本身不等于违规。这里更具体的问题是相同 benchmark 的 question–gold_answer 标注记录直接入库且匹配记录不排除。若目的本就是 oracle/答案可见诊断，应明确改为这种任务；它仍不能支持当前独立推理与普遍泛化主张。双方共同有答案访问也不会使该评估自动成为隔离的泛化测试。
- **修复：** 若要保留一般评估结论，构建与测试标注隔离、版本固定的检索语料；按题目、重复/派生题及共享答案标注关系检查泄漏，再重跑。合法公开文档中的答案内容无需一概删除。若只保留本软件 fixture，则明确标注为答案可见的合成诊断并撤下泛化结论。
- **关闭条件：** 可检查的语料/切分清单与构建代码证明测试标注未入库；相同/相关题检索检查通过；新结果与逐题轨迹可追踪。或明确改写研究对象为有答案访问的诊断，并逐处删除不再成立的隔离评估推论。仅修改过滤开关而保留旧结果不能关闭科学问题。

### PRA-EN-002 — “三种子均值”使用了与最大值一致的 RouteMind 数字

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** `manuscript.md` L19：`Table 1. Mean accuracy across all three seeds, reported as a percent. No seeds were excluded.`；L24：`| RouteMind | 88.0 | 2400 |`；`evaluation.py` L6–8：`def reported_score(seed_scores):`、`return max(seed_scores)`；摘要 L6 与 Figure 1 也显示 88.0。
- **证据性质 / 实际来源：** observed；全部 CSV 记录复算及受控函数调用。RouteMind mean=0.84，max=0.88；Baseline mean=0.80，max=0.81。
- **后果：** 中心结果被夸大 4 pp，且摘要、表和图的 mean 标签错误。函数与文本不一致；实际如何生成表格尚无完整 provenance。
- **最强作者辩护与裁决：** “88% 是最好种子”在数值上成立，却与明确的全三种子均值及无排除声明不符。“只是舍入”不能解释 4 pp。“代码没实际用于表格”可能成立，因此本报告不把函数调用链当成已验证；但 CSV 与均值标签的矛盾独立成立。
- **修复：** 按统一定义改为三个运行的算术平均；同步修订摘要、Table 1、Figure 1 及派生效应。若另报最佳值，新增明确列而不替换平均值。提供从结果文件到显示产物的单一生成路径，解释 Baseline 没跟随 `max` 的原因。
- **关闭条件：** 使用三条指定记录重新运行汇总，获得 80.0% 与 84.0%；函数/生成脚本、表、图、正文全部一致；检查没有隐式种子筛选。此项关闭只能证明汇总一致，不能关闭泄漏和因果归因问题。

### PRA-EN-003 — 路由与资源预算同时变化，无法识别路由的单独因果效应

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** 摘要 L6：`The routing module alone causes the gain.`；L9：`under a fixed inference budget`；L14：`The baseline uses a fixed 600-token budget and one retrieval call. RouteMind uses a 2,400-token budget, up to four retrieval calls, and the routing module.`；`We did not run a token-matched baseline or a routing-disabled variant at the larger budget.`；配置 L8–9 一致。
- **证据性质 / 实际来源：** observed 的控制条件不匹配；inferred 的不可识别性。上限为四倍，不等于已测到实际 token、调用数、延迟或费用也全部四倍。
- **后果：** 既不能回答固定预算研究问题，也不能把观察差异单独归因于路由。更大 token/调用预算是有材料依据的替代解释。
- **最强作者辩护与裁决：** 比较完整系统各自的配置可有实用意义，但需称为这些不同资源配置的比较，不能保留“alone causes”和固定预算答案。没有实际用量数据也不能声称效率提升。
- **修复：** 最小新对照是在相同 2400 token/4-call 上限下比较 routing on/off，保持模型、语料、提示、解码、重试和评价一致；或在 600/1 条件下比较二者。预算×路由的 2×2 设计可进一步区分交互，但不是唯一可行方案。记录实际 token、调用和失败，避免只报配置上限。
- **关闭条件：** 经过 PRA-EN-001 的切分修复后，至少一组明确预算匹配的 on/off 对照具有可追踪配置和结果；据结果限定结论。资源不足时删除单独因果主张、承认当前比较未回答固定预算问题，可关闭过度归因的文字问题，不能宣布因果证据已经补齐。

### PRA-EN-004 — 评分被称为独立盲化人工评估，与所述协议直接矛盾

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** `manuscript.md` L16：`All judgments are described as independent blinded human assessments. No human annotators participated.`；同段：`A separate LLM judge sees the method name above each answer; proposed answers always appear first.`；`The judge uses the same base checkpoint as the answer generator.`；`config.json` L10。
- **证据性质 / 实际来源：** observed 的身份/盲化矛盾；missing 的逐次判定和偏差测量。确认无人参与及未盲化，不把潜在自偏好或位置偏好伪装成已经测出的效应。
- **后果：** 读者会误判证据来源和独立性；暴露方法身份、固定顺序、同基座使评分可能受非正确性因素影响。LLM judge 与生成器分开调用并不等于独立人工判断。
- **最强作者辩护与裁决：** “separate” 可以表示独立进程或调用，但无法使 judge 成为人类、盲化或统计独立。公开协议承认这些条件是有帮助的，却与相邻表述冲突，必须改正。
- **修复：** 立即将描述更正为 automated, unblinded LLM judgments；说明评分 rubric、模型版本、提示、温度、顺序、重复和并列处理；如要用判分支撑正确性，隐藏方法名称、平衡/随机化顺序并做顺序互换诊断，保留轨迹。若未来保留“human”表述，必须实际获得相应人工评估；也可完全采用明确限于该 judge 的结论。
- **关闭条件：** 全文不再称本批结果为人工盲评；协议、配置与评分记录一致。偏差控制需由新记录和敏感性结果验证；单纯删掉错误形容词不能证明原 judge 的排序可靠。

### PRA-EN-005 — 普遍可靠性与所有领域保证超过材料的范围

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** 标题 L1：`RouteMind: Universal Improvements in Retrieval Agents`；摘要 L6：`These results prove that routing universally improves reliable reasoning across all domains.`；L41：`These limitations do not affect our universal guarantee.`；同段只有一个 benchmark 和 checkpoint；L9 明确未测医学、法律、多语或交互任务。
- **证据性质 / 实际来源：** observed 的量词与已声明实验范围；inferred 的证据不足。没有把“没有支持”写成“已证明路由在所有领域失败”。
- **后果：** 从一组局部、含协议缺陷的合成汇总值推到全领域保证；同时把 accuracy 当成可靠推理的充分证明。数据里每个 seed 的分数都较高仍不能提供这种普遍保证。
- **最强作者辩护与裁决：** 若“universal”只用于营销性标题，正文仍用了 `prove`、`across all domains` 和 `guarantee`，不是一次可忽略的修辞。不存在足够的理论对象或证明能另行支持它。扩大几个 benchmark 也不会自动证明“所有领域”。
- **修复：** 统一收窄标题、摘要、限制与结论为该虚构单基准的描述性比较；若将来研究某类跨域可靠性，先定义目标领域、可靠性指标和合理任务取样，并将结论限定到实际覆盖范围。此处不要求为了修文字而无穷扩展实验。
- **关闭条件：** 全文不再从当前证据推到全域/保证/普遍因果提升；研究问题、指标、数据范围和结论量词一致。任何新外推主张另附对应证据。

### PRA-EN-006 — 相对准确率改进写成 20%，指标和分母不一致

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** 摘要 L6：`a 20% relative improvement over the baseline`；Table 1 的 80.0%、88.0%；CSV 的三个运行值。
- **证据性质 / 实际来源：** observed；`reconcile_number` 和 Decimal 算术均获得正确相对准确率提升 5.0%。
- **后果：** 对主要效果大小的叙述错误。此项与 PRA-EN-002 不完全相同：即使暂不修均值，80→88 也只有 10% 相对准确率提升；更正聚合后还必须重算/更正变化率。
- **最强作者辩护与裁决：** 20% 正好等于校正后 20%→16% 的相对错误率下降，但当前语境未定义这一指标，且与稿件的 88% 不兼容。不可用重新解释分母替代明确修订。
- **修复：** 写成 `a difference of 4.0 percentage points (a 5.0% relative increase over the baseline)`，并注明是所给合成记录的描述性差异。如果另报 error reduction，则明确命名、给公式且保持准确率一致。
- **关闭条件：** 公式、分母、单位、表格和摘要匹配，绝对百分点与相对百分比可区分；自动汇总不再硬编码 20。

### PRA-EN-007 — Figure 1 的截断柱长及“十倍”表述误导效果大小，并隐藏运行离散程度

- **状态 / 严重性：** `confirmed` / `major`。
- **定位与精确锚点：** `manuscript.md` L34：`The bars show a dramatic tenfold improvement.`；同段承认 79% 起始及不显示 seed uncertainty。实际对象 `figure1.png`，视觉记录 V-01；SVG L95–146 为 80–90 刻度，L164/L167 为 80.0/88.0，L153–161 为轴线，L40–54 为柱路径。
- **证据性质 / 实际来源：** observed 的真实图像与 SVG 对照、数值计算；没有用文件名或源码读取替代观看。
- **后果：** 柱图可见部分从约 79 到 80/88，对应柱高约 1:9，不能解读为准确率十倍。80→88 的数值比例仅为 1.10；校正均值后的 80→84 为 1.05。图还使用 PRA-EN-002 的错误均值，且没有呈现 79/80/81 与 80/84/88 的离散程度，使“可靠”更容易被误读。
- **最强作者辩护与裁决：** 非零纵轴并非所有图中的错误；局部范围可用于比较小差异。这里是以柱长表达幅度，同时正文声称十倍且未说明轴截断，组合造成实质误导。图上有 80/88 标签可供认真读者纠正印象，但不能消除错误文字。也不要求把三次运行 SD 误标为置信区间。
- **修复：** 先纠正均值。可保留以 0 起始的柱图并显示运行点，也可改为清楚标出 75–90% 等范围的点图，显示全部三个 seed 点、均值和定义明确的 sample SD。给出 n、统计单位及预算差异；删除 tenfold。不需要为了描述性图强行估计 p 值。
- **关闭条件：** 对重绘后的实际图像再次观看；图中每个值回溯 CSV；轴/图注明确，显示 80.0/84.0 与所有运行记录，任何误差线都写明 SD 而非 CI；正文不再用可见柱高比代替准确率效应大小。

### PRA-EN-008 — 路由机制及评分实现缺少足够信息，不能从现有产物复建 Agent 评估

- **状态 / 严重性：** `confirmed` / `major`（已确认报告/产物缺口，底层实际运行状态未验证）。
- **定位与精确锚点：** L6：`RouteMind adds a routing policy to a retrieval agent.`；L9：`Our contribution is a small routing module and an evaluation on one English question-answering benchmark.`；L41：`Source data are aggregate per-run accuracy; question-level outcomes and judge transcripts are not included.`；`evaluation.py` L1：`Synthetic example for static inspection, not an executed experiment.`。已检查整个 Method and evaluation、配置、八行代码和 manifest。
- **证据性质 / 实际来源：** observed 的提供范围与 reporting omission；missing 的路由决策、生成/评分程序、模型身份和运行路径。
- **后果：** 无路由输入/状态、决策规则或伪代码、训练/设定方法、结束条件；仅有 `routing: true/false` 不能确定实现。配置没有可识别的实际生成器 checkpoint/version，judge 只有 `same-as-generator`，没有准确率计分规则、prompt、rubric、重复/失败处理。不能从六条汇总分数核实分母是否为全部 100 题、失败如何计入，或复算逐题正确性。此问题影响方法可解释性与再执行，不证明作者未完成任何真实实验。
- **最强作者辩护与裁决：** 作者仅承诺发布 local configuration 和 aggregate scores，这两项确实存在；不能说发布承诺被违背。且 synthetic fixture 有意不是完整实验。本项限定为：若按正文的“方法与评估”作为研究结论使用，现有方法细节不足；若目标仅是软件测试样例，则明确这一边界即可，不应把完整真实实验当成已经完成。
- **修复：** 描述路由机制，给出可追踪的配置—输出—汇总关系；定义准确率、遗漏/超时与失败政策、judge 实际计分规则；要主张可复现真实实验时提供模型版本、执行入口、提示、记录及环境。保持 synthetic 定位时，直接声明这些产物仅支持静态与算术检查，不声称已复现 Agent 实验。
- **关闭条件：** 至少正文足以解释每个组件与指标、产物范围准确；若目标包括实验再执行，需由具体执行命令、模型/数据身份与逐题日志产生可重建的汇总。补一份空环境文件或写“已开源”不能替代这些链接。

### PRA-EN-009 — 引言的主谓一致、冠词及比较级错误妨碍专业表述

- **状态 / 严重性：** `confirmed` / `editorial`。
- **定位与精确锚点：** `manuscript.md` L9：`We studies an routing approach that retrieve documents and makes answers more better.`
- **证据性质 / 实际来源：** observed 的英文句子，全文语境审读；引文辅助函数验证匹配位置 L9。
- **后果：** `We studies`、`an routing`、`that retrieve` 和 `more better` 存在局部语法问题。不能据此推断作者身份、AI 生成、学术能力或数据不可信。
- **最强作者辩护与裁决：** 句意可推知，所以是 editorial；与主要科学问题分开，不按语言错误累加严重性。
- **修复：** `We study a routing approach that retrieves documents and aims to improve answer quality.` 此处 `aims to` 保留研究目的，避免将尚未隔离验证的效果当成句中事实。
- **关闭条件：** 在修订后的引言上下文中检查语法、指代和效果强度一致。当前未改源稿，所以没有关闭。

## 6. 两张图与两个表的逐对象检查

### V-01 — Figure 1 实际视觉记录

查看对象为原始 `figure1.png`（1152 × 736），通过图像查看工具以 original 级别显示。观察到白底双柱图，横轴 Baseline/RouteMind，纵轴 `Mean accuracy (%)`，可见刻度 80、82、84、86、88、90；图的底边低于 80 刻度，Baseline 可见柱非常短；两柱标注 80.0、88.0。没有误差线、运行点、n 或轴截断说明。字体与主标签在所看大小下可辨认，没有因像素格式导致的主要阅读障碍。底部有合成验证标记。

与 SVG 的柱端点/轴坐标及正文 L34 对照可确认下界约 79、上界 90；这一几何核对不是新的实验数据。Figure 1 的数字与原 Table 1 一致，却与全部运行均值不一致。问题是数据聚合和幅度编码/说明，见 PRA-EN-002/007；不是“PNG 格式不合格”。未实际渲染 SVG，也未检查最终印刷尺寸。

### V-02 — Figure 2 实际视觉记录

查看对象为原始 `figure2.png`（1080 × 612），以同样方式实际显示。观察到 2 行 × 4 列蓝色热图；行标签 Baseline、RouteMind，列标签 Q1–Q4；每格数字清楚：Baseline **1、1、1、1**，RouteMind **2、3、4、2**。右侧色标 0–4，单位为 `Calls per query`。深色格使用浅色数字，主要标签没有明显裁切；底部说明为四个示例查询的合成 trace。

这些显示计数处于配置的调用上限范围内。可以确认图在所看大小下清楚、与 L36 的示例性质相符；**不能**据此确认真实日志存在、这四个查询有代表性、全部题目的平均调用数为 2.75，或总体成本为基线的某个倍数。2.75 仅是所显示四格的算术平均，不是这里的总体估计。本报告不对该图提出强制矢量化、显著性标注或总体推断要求。

### Table 1

已检查两个方法、准确率单位、预算列和“全部三种子均值”的 caption。Baseline 行通过，RouteMind 行不通过。预算列对两个条件给出不同上限，但没有 actual token/use 分布；因此不能从表得出效率结论。建议将原始运行值和 SD 一并展示，见下节，不通过当前文件额外补造题级结果。

### Table 2

已验证唯一来源 `results.json` 中 `value="0.9477"`，三位小数显示 0.948 正确。稿件明确它不属于 accuracy，两个统计量不应混合。本次没有发现数值问题。缺少 calibration ratio 的定义、公式、计算输入和生成过程，所以只记录其科学解释/上游 provenance 为未验证；如果作者要用该值支撑“校准优良”之类新结论，必须补这些信息。当前并没有这样的明确效果主张，故不另制造一个重大问题。

## 7. 可直接采用的英文修订建议

以下文字是建议稿，尚未写入 manuscript。科学纠正和纯语言修饰已明确区分；没有把计划实验写成已完成。

### 7.1 标题（范围纠正；PRA-EN-005）

原文：`RouteMind: Universal Improvements in Retrieval Agents`

建议：

> RouteMind: A Synthetic Comparison of Routing in Retrieval Agents

### 7.2 摘要（数值、归因和证据范围纠正；PRA-EN-001–006/008）

替换现有摘要全文；保留单独的 synthetic disclosure：

> RouteMind adds a routing policy to a retrieval-agent design. We examine a synthetic comparison on TaskBench-Q using three seed-labeled aggregate accuracy records per method. The unweighted mean accuracy is 84.0% for RouteMind and 80.0% for the baseline, a difference of 4.0 percentage points and a 5.0% relative increase over the baseline. The documented protocol exposes benchmark gold answers through retrieval, assigns different token and retrieval-call budgets to the two methods, and uses an unblinded LLM judge. These conditions prevent attribution of the observed score difference to routing and do not establish held-out generalization. The supplied configuration, aggregate scores, and figures support inspection of this synthetic example; no real-world result or universal reliability guarantee is claimed.

该替换主动修正了原来不成立的含义，不是把原强断言仅做语言润色；数字源于本报告的实际重算。由于输入明确是虚构材料，使用 supplied records 和 documented protocol，没有虚构真实模型执行。

### 7.3 引言与研究问题（局部语言 + 澄清未回答的问题）

替换 L9 的病句：

> We study a routing approach that retrieves documents and aims to improve answer quality.

对固定预算研究问题，可写：

> The research question is whether routing improves accuracy when token and retrieval-call budgets are held fixed. The current synthetic comparison does not resolve this question because the configured budgets differ between methods.

原文 `Agents retrieve context—then choose an action.` 的破折号不构成科学错误，可以保留；未测四类任务的限定也应保留。

### 7.4 评估协议与判断来源（澄清；PRA-EN-001/003/004）

在尚未重跑的版本中，只能诚实描述现状：

> The documented retrieval index contains the benchmark question records and their gold answers. Matching evaluation records are not excluded. This setting exposes the evaluation answer key and therefore does not provide an answer-isolated test of generalization.

> The baseline is configured with a 600-token limit and one retrieval call per question. RouteMind is configured with a 2,400-token limit and up to four retrieval calls. These are configured limits; actual token use and end-to-end cost are not reported. The current comparison changes both routing and resource allowances.

> The evaluation protocol uses an LLM judge that can see the method names and always receives the RouteMind answer first. The judge uses the same base checkpoint as the answer generator. No human annotators participated. The judgments are therefore automated and unblinded; their statistical independence and agreement with human assessments have not been established.

不要在尚未有新数据时写成 `We removed all leakage`、`We conducted a matched-budget evaluation` 或 `We validated the judge with humans`。

### 7.5 可替换的 Table 1

> **Table 1. Descriptive summary of the supplied synthetic run scores.** Means are unweighted arithmetic means across the three seed-labeled records. SD is the sample standard deviation across run scores, expressed in percentage points. The resource columns give configured upper limits, not measured costs. The documented retrieval protocol exposes benchmark gold answers, and the comparison uses unequal budgets.

| Method | Seed 11 accuracy (%) | Seed 22 accuracy (%) | Seed 33 accuracy (%) | Mean accuracy (%) | SD (percentage points) | Max tokens per question | Max retrieval calls per question |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 79.0 | 80.0 | 81.0 | 80.0 | 1.0 | 600 | 1 |
| RouteMind | 80.0 | 84.0 | 88.0 | 84.0 | 4.0 | 2400 | 4 |

若正式版面太窄，可将三条种子列移至补充表或图中，不能把它们删掉后把 SD 当成 CI。这里不预判未知期刊的页宽规则。

### 7.6 结果段与 Table 2

> Across the three supplied run records, the mean accuracy is 80.0% for the baseline and 84.0% for RouteMind. The mean difference is 4.0 percentage points, corresponding to a 5.0% relative increase over the baseline. The differences for matching seed labels are 1.0, 4.0, and 7.0 percentage points. These quantities are descriptive; no hypothesis test was performed. The protocol and budget differences preclude a causal interpretation of the routing contribution.

Table 2 保留 0.948；如需把源值说明写得更紧凑：

> The supplied calibration scalar is 0.9477, which rounds to 0.948 at three decimal places. It is not an accuracy measurement. Its underlying calculation is not included in the supplied artifacts.

最后一句补充了可复建范围；不能把该段当成对 calibration 数学定义的替代。

### 7.7 Figure 1 重绘规格与英文图注

建议改为显示全部三个运行点、均值及 sample SD 的点图；若采用局部纵轴，明确给出 75–90% 等范围及全部刻度。也可用零起始柱图叠加运行点。全部点必须来自现有 CSV，显示 80.0% 与 84.0% 的均值。不生成新的实验记录，不增加虚构置信区间。

**以下图注仅适用于按“运行点 + 均值 + SD”规格完成重绘后的图；当前没有制作或替换该图。**

> Figure 1. Supplied run-level accuracy scores for the synthetic TaskBench-Q comparison. Small points show the three seed-labeled records for each method, and large markers show the unweighted means: 80.0% for Baseline and 84.0% for RouteMind. Error bars show the sample standard deviation across runs, 1.0 and 4.0 percentage points, respectively; they are not confidence intervals. The mean difference is 4.0 percentage points. The documented protocol exposes benchmark gold answers and uses different resource limits, so the plot does not isolate the effect of routing.

Figure 2 当前图形无必须修改项。若希望图注更自足，可用：

> Figure 2. Illustrative retrieval-call counts for four synthetic queries. Each cell shows the displayed count: Baseline uses one call in each example, and RouteMind uses 2, 3, 4, and 2 calls for Q1–Q4. This diagnostic trace is not an estimate of overall tool cost or evidence of performance superiority.

### 7.8 限制段（替换保证语句；PRA-EN-005/008）

> This fixture covers one English question-answering benchmark and one stated model checkpoint. Only aggregate run scores are supplied; question-level outcomes and judge transcripts are unavailable. The configuration exposes evaluation gold answers through retrieval, uses unequal inference budgets, and specifies an unblinded LLM judge. The artifacts permit descriptive checks of the supplied values but do not establish out-of-domain reliability, the causal contribution of routing, or a universal guarantee. Answer-isolated evaluation, controlled comparisons, and traceable scoring would be required before making those narrower empirical claims.

这里的 `one stated model checkpoint` 表示稿件声称只用一个 checkpoint，不表示审查者已识别或取得该 checkpoint。

### 7.9 局部代码修正建议（未应用）

若函数的既定契约确实是非空运行分数的算术均值，最小建议为：

```python
from statistics import mean

def reported_score(seed_scores):
    return mean(seed_scores)
```

应由表格/绘图代码实际统一调用这个汇总规则，并明确空输入与失败记录的处理。此建议不修复答案暴露、judge、路由实现或不匹配预算；未运行完整修订实验，也没有凭这个建议关闭 PRA-EN-002。

## 8. 修复顺序与有决策价值的实验

### 8.1 先处理哪些事项

| 顺序 | 必要行动 | 解决的具体不确定性 | 最小证据/低成本替代 | 验收 |
|---|---|---|---|---|
| P0 | 更正 synthetic 范围、人工评估身份和 universal/alone 文案 | 当前读者是否会误解证据来源与外推范围 | 不需新实验；用第 7 节诚实陈述现状 | 全文与实际材料一致；不把缺失证据宣称为已补齐 |
| P0 | 修正聚合、百分比、Figure 1 数字与幅度说明 | 原表到底是什么统计量 | 用六条现有记录重算，保留所有种子 | 80/84、4 pp、5%，源码与显示一致 |
| P1 | 隔离检索语料与测试答案 | 分数是否依赖直接暴露的答案标注 | 重新构建可审计语料与切分；资源不足则明确 oracle/答案可见诊断性质 | 语料及检索检查、逐题输出、新结果对应 |
| P1 | 预算匹配的路由开关对照 | 路由贡献还是更多推理资源 | 一个相同预算下的 on/off 比较；不能复用旧泄漏分数作为干净结果 | 两配置仅预定因素变化，实际预算可追踪 |
| P1 | 真实、可追踪的评分协议 | 自动评分是否稳定反映目标正确性 | 去身份、顺序平衡、rubric 与轨迹；可先做小范围顺序互换诊断 | 协议、配置、转写和结果一致；偏差影响有据 |
| P2 | 补路由、指标与结果生成说明 | 他人能否理解并重建每个数 | 若仅保留静态 fixture，准确声明不包含完整实验 | 明确从输入到运行再到表/图的路径与缺口 |
| P2 | 进行适当的描述或推断分析 | 有限运行分数能支持多强的可靠性结论 | 描述性均值/SD 即可匹配当前窄结论；推断需要逐题/运行层级数据 | 统计单位、依赖、缺失政策与结论一致 |
| P3 | 若要拓宽贡献，再选目标域/模型/难例 | 外推到明确新条件是否成立 | 依据目标主张有选择扩展；不是为修当前普遍保证而列无穷清单 | 新结论只覆盖实际评估范围 |

### 8.2 最小对照实验卡：隔离后的同预算 routing on/off

- **目标主张：** 在指定同一模型、语料和预算下，路由策略是否改变任务准确率。
- **前置条件：** 先修 PRA-EN-001；明确路由实现、正确性标准、失败/超时计分和模型版本；冻结评价题集及分析方案。
- **因素：** routing on/off。其余控制包括同一可访问语料、token/调用上限、模型、提示中无关部分、解码/重试、工具权限与 judge 协议。路由关闭应保持系统可用，避免通过破坏接口制造“消融”。
- **资源：** 若仅沿用“100 题、3 个 seed”这个计划规模，单一预算的两个条件需要 600 次 query-level 执行；这是透明的工作量示例，不是设计功效论证，也不意味着这些执行已完成。实际 token、延迟与费用需要真实轨迹，不能从上限推定。
- **扩展选项：** 加入 routing×budget 的 2×2 设计，用低预算 600/1 与高预算 2400/4；同样规模下为 1200 次 query-level 执行。它区分预算主效应和交互，比泛泛“多加几个 baseline”更直接；若只主张高预算下路由效果，最小两条件已经回答该问题。
- **观测：** 每题正确性、原始回答、检索记录、实际调用/token、失败和 judge 判定；保留 seed 与题目 ID。
- **分析单位：** 对固定题集的运行波动与对题目总体的外推分别定义目标。只有运行汇总时先给完整描述；有题目×运行结果后再按真实依赖关系选配对/分层方法。共同文档、重复题和重复评分可能需要进一步聚类；不预设所有行独立。
- **验收：** 任意方向的结果都如实报告；预算匹配和答案隔离可核对；路由贡献限于该设置。不存在“必须得到显著正效果才算实验通过”的条件。

### 8.3 Judge 检查卡

- **问题：** 名称或答案位置是否改变同一答案对的判定；同一 base checkpoint 的判定能否支持作者宣称的评价含义。
- **低成本起点：** 固定一组同样的答案对，去掉方法身份，对两种顺序都评分，保留评分说明；预先规定并列/格式失败处理。该诊断可以检验顺序敏感性，不能单独证明客观正确性。
- **可选人工校准：** 若要向人工判断或真实正确性外推，选有明确采样规则的答案子集，由合适的人类按同一 rubric 标注并检查分歧；不把一个 LLM 的更多票数算成人类独立样本。若论文只报告该自动 judge 的结果，则可明确限定，不强制伪造“人工验证”。
- **验收：** 记录实际模型版本、rubric、提示、顺序及转写；披露敏感性与分歧。换另一模型也不自动建立统计独立或真值。

### 8.4 描述性统计与可靠性边界

当前三条 seed 汇总足以复算均值与 SD，不能核实题目层面的准确率分母或建立跨域可靠性。保留 L38 的“未做假设检验”是可接受的最小方案。若希望提出推断结论，先明确目标量、独立/重复单位、配对与聚类，再选择检验或区间；不得把 `n=3` 的 sample SD 当成置信区间，也不得将 LLM 重复判分视为更多独立任务。无需为每个描述性表强制 t 检验、指定统一 seed 数或报告虚构功效。

## 9. 反方辩护与撤销的误报

| 候选批评 | 最强辩护/核查证据 | 裁决 |
|---|---|---|
| “0.9477 与 0.948 不一致，说明数据漂移” | Table 2 明确三位小数；实际按 Decimal 舍入为 0.948 | **驳回。** 通过显示数值核对，不列活动问题 |
| “Figure 2 是 raster，必须改矢量” | 实际 PNG 阅读清楚，格内有精确数值，caption 明确截图式诊断 | **驳回。** 未知 venue 下不强制格式偏好 |
| “没有假设检验，所以结果不合法” | L38 明确无统计显著性主张；现有数据可以作描述 | **驳回。** 不自动加 p 值；可靠性外推另受限制 |
| “同一组 seed 的三个差值都正，所以路由独立有效” | 资源和答案访问/评分条件未隔离 | **保留反对该推断。** 三个描述性差值无法消除设计混淆 |
| “RAG 语料包含任何答案都是泄漏” | 合法检索语料可以包含回答所需知识 | **收窄。** PRA-EN-001 只指同一 benchmark 的 gold-answer 标注与未过滤匹配记录 |
| “`max` 已证明全表由该函数产生” | 函数对 Baseline 为 81%，表却为 80%；无调用链 | **收窄。** 只确认函数语义及 RouteMind 均值错，不虚构实际表格生成路径 |
| “更大预算说明实际费用恰为四倍” | 配置是上限；Figure 2 只有四个示例 | **驳回。** 只确认资源控制不等，实际成本待日志 |
| “同基座 judge 必然偏袒 RouteMind，已解释全部分数差” | 配置能显示风险，缺少互换顺序/去身份/转写结果 | **未验证。** PRA-EN-004 确认描述错误，不量化未知偏差 |
| “没有真实引用，所以缺乏学术诚信” | L3、L44 明确虚构 fixture，未建立或声称真实新颖性 | **驳回。** 不编造 DOI，不做无关外部 novelty 搜索 |
| “没有完整原始数据，所以实验必然伪造” | 作者已经说明仅提供 aggregate；文件本身为合成示例 | **驳回。** 缺失限制验证范围，不构成真实不端推断 |
| “引言破折号或通用词汇说明 AI 写作” | 只是标点/风格，没有作者来源证据 | **驳回。** 仅保留可定位的语法问题 |

没有把以上驳回项编码为 `closed`：它们不是经过新修订关闭的有效缺陷，而是审查中排除的误报。九项活动问题仍保持原 ID。

## 10. 实际工具与可复核记录

### 10.1 已执行的工具和参数

1. `cat` 读取技能 `SKILL.md`；读取 `review-contract.md`、`input-output.md` 及其余十篇 reference；读取 `assets/review-report.template.md`、`assets/audit-spec.example.json`。`rg --files` 的路径参数**仅**为技能目录和 `en_agent` 目录。
2. 用 Python 为七个文本证据文件逐行编号输出（manuscript、manifest、config、evaluation、CSV、JSON、SVG）；原稿 44 行、代码 8 行以及两个结构化结果已完整看过。
3. `view_image` 两次，分别对 `figure1.png` 和 `figure2.png`，参数 `detail="original"`；V-01/V-02 是实际观图记录。
4. 执行：

   ```bash
   python /workspace/scratch/4244a6de7f92/paper-review-atlas/skills/paper-review-atlas/scripts/atlas.py preflight --root /workspace/scratch/4244a6de7f92/paper-review-atlas/tests/fixtures/en_agent --manifest manifest.json
   ```

   exit 0，`status="ready"`，八项声明 artifact 全部存在。辅助命令自身明确只检查可用性，所列 `available_uninspected` **不是科学或视觉通过状态**；后续人工/模型审读与实际图像查看才形成本报告的检查记录。
5. 执行 `python …/scripts/atlas.py plan --mode full --language zh --domain agent`，exit 0；返回参考路由与交付清单。该命令不读取稿件，不记作自动审稿成功。
6. 用 `sed` 检查 `atlas.py` L1–170、`audit_checks.py` L1–145；用 `rg -n` 针对 audit、单位、舍入、差值与命令行参数搜索技能脚本。没有完整审计 helper 的全部实现，也没有运行仓库测试套件。
7. Python **3.12.14**，通过 `python -B - <<'PY'` 执行审查者构造的本地诊断，exit 0。导入技能 `reconcile_number`、`paired_run_stats`、`verify_quote`，按第 4 节完整声明复算；读 manifest 指定的全部文件并算 SHA-256；解析 PNG IHDR 尺寸；静态检查后通过 `runpy.run_path` 加载那八行 example 并执行第 4.4 节三次调用。没有数据下载、模型推理、训练、Agent 回放或 judge 执行。
8. 实际 `verify_quote` 检查的八个锚点包括泄漏、未做匹配预算、人工盲评矛盾、Table 1 的 mean caption、`return max(seed_scores)`、universal 句、tenfold 句和引言语法句；全部 `verified`，匹配行分别为 12、14、16、19、8（代码）、6、34、9。这只证明引文存在和定位正确，不证明科学判断自动成立。

本次通过公开 helper 的 Python API 进行自建数值审计，**没有执行** CLI `atlas.py audit --spec …`，也未向输入目录放入审查者规范以假装其为作者材料。没有将成功的 `preflight` 或 `plan` 当作完整科学验证。

### 10.2 关键输出摘录

```text
Table 1 Baseline: calculated=80; rounded_calculated=80; status=verified
Table 1 RouteMind: calculated=84; reported=88; absolute_error=4; status=mismatch
Abstract relative gain: calculated=5; reported=20; absolute_error=15; status=mismatch
Calibration: calculated=0.9477; rounded_calculated=0.948; status=verified
Paired summary: n=3; left mean=0.8, sample_sd=0.01;
                right mean=0.84, sample_sd=0.04;
                difference mean=0.04, sample_sd=0.03;
                differences={11:0.01, 22:0.04, 33:0.07}
                p_value=null; confidence_interval=null; inference_status=unverified
reported_score diagnostic: baseline=0.81; proposed=0.88
build_index diagnostic: gold_answer copied to index text
```

数值 helper 的 `verified` 仅表示所声明操作与给定来源值相符；source selection、真实性、统计独立和实验有效性仍需审查判断。

### 10.3 输入指纹

以下是在审查中从实际字节生成的 SHA-256，可用于识别后续版本；不代表作者身份或真实实验认证。

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `manifest.json` | 677 | `d22ec6edcf9d18c4bffcb8f66c6b8ed9fa0864150c7241e26a05d05083128755` |
| `config.json` | 505 | `ff46b6bc783257196df446a992ddf96b08487b1b5b9f937dd130db922d0549c1` |
| `evaluation.py` | 303 | `f245fa847bcea51f84a1f96583ae5a5f931ecf3d1b7b68eea59fdb4a7fa31eab` |
| `figure1.png` | 43540 | `d865c892271904549b0f11c1da8dea40b97b6da836a1e443463c6d1903db467b` |
| `figure1.svg` | 8663 | `b988b97931ce55e9611da7379c0666b0f9ec469de3192562d8395089d184e73a` |
| `figure2.png` | 44943 | `3fe866be866efa0db71ffb793e365ad7684ff1f493c58adb9e57b742f9e87f83` |
| `manuscript.md` | 3598 | `f089f1fb687dd75417d765afab8c3b86ca3db3968b0b744f9a93ebd9d9b94ffd` |
| `results.csv` | 122 | `ec919a379068829f26b1cf6ba962a6e4a5db6445830a4151c73c52f28058949b` |
| `results.json` | 92 | `2d15913164f4d238f986fd2fb777278a97071ae3976ab4e466023022ef88644a` |

## 11. 未验证事项与后续关闭标准

明确未验证：100 个问题本身及其真实分母、任何实际模型训练/推理、被检索到的具体答案记录、实际 token/时间/费用、路由算法实现、真实 checkpoint 身份、judge 转写与偏差幅度、题级正确性、运行随机化/独立性、calibration scalar 上游计算、Figure 2 的查询日志/选择规则、跨域效果、真实文献新颖性、正式 venue 合规、最终文档排版以及图形的最终印刷效果。

本报告没有读取技能目录和 `en_agent` 输入以外的外部证据；没有读取 sibling fixtures、测试脚本或验证答案。工作产物仅为本报告；没有将新实验、人工评审、统计显著性或模型独立性伪造成已完成事实。

下一轮先核对**诚实的评估身份与结论范围**，再核对**统计汇总及图表一致性**，随后用**答案隔离、同预算比较、可追踪评分**解决中心实证问题。若目标继续只是软件验证用例，则原输入保留为原始 fixture，报告中的修复建议作为可审查的对照方案；本次已按要求保留源文件不变。所有关闭必须针对具体 acceptance check：纠正文字不等于完成实验，重算表格不等于重现模型，实际查看图片也不等于验证数据真实性。
