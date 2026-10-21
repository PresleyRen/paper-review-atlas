# Representative source-feature walkthrough / 逐技能特色案例

Inputs are deliberately small synthetic excerpts. The authoring assistant applied Atlas protocols in the same development conversation and recorded the following decisions. These records preserve concrete reasoning and fixes; tests replay their anchors and route checks, not an independent LLM evaluation.

## FC001
**F001 · cs-ai-paper-review**

Input: `The new system is universally better. Only task A is evaluated.`

Decision: **revise**

把全称主张改为已测试任务上的结论，并优先核查该任务的对照和结果。

验收 / acceptance: 摘要与结论不再把单任务结果扩展为所有任务。

[Frozen input](../tests/fixtures/feature_walkthrough/FC001.txt) · SHA-256 `0df2f67363b9f508224f9d36388ff19dd64c5fe1f76ae0acc663c928e847cfe0`

## FC002
**F002 · ieee-access-review**

Input: `Target brief V2 requires an artifact statement. The draft has none.`

Decision: **revise**

按用户给出的V2标准补充真实的数据代码可用性说明，记录该标准的来源版本。

验收 / acceptance: 每个适用标准ID均能找到对应材料或待办。

[Frozen input](../tests/fixtures/feature_walkthrough/FC002.txt) · SHA-256 `8272e509f3f999326de317e02099a9e34680ceeb270d868384085d67c5c273af`

## FC003
**F003 · paper-surgical-editor**

Input: `Issue I7 fixes Table 2; the abstract still reports the obsolete value.`

Decision: **revise**

保留I7，列出摘要与表2的依赖关系；同步修订后再核对数字。

验收 / acceptance: 原问题编号不变，摘要和表2均通过同源重算。

[Frozen input](../tests/fixtures/feature_walkthrough/FC003.txt) · SHA-256 `d389ece57fc8b5e26179c693c561f18fbad414d915c5c6f1164007e8489a72ea`

## FC004
**F004 · paper-busy-reviewer**

Input: `Visible materials: title, abstract and Figure 1 only. Methods are unavailable.`

Decision: **request_evidence**

先给有限表面审阅：说明主问题是否清楚，列出需读方法才能判断的问题。

验收 / acceptance: 不以未见方法为由断言实验没有做。

[Frozen input](../tests/fixtures/feature_walkthrough/FC004.txt) · SHA-256 `9b8e87fe6d7a04e2b4504698c94879e6ef390da0e7042182799c560535440b50`

## FC005
**F005 · paper-reviewer-sim**

Input: `Reviewer A says a baseline is missing. Appendix B contains that baseline.`

Decision: **retain**

定位附录B后撤回缺失指控，继续检查该基线是否匹配而非强行保留拒稿理由。

验收 / acceptance: 最终问题表不包含已被附录解决的指控。

[Frozen input](../tests/fixtures/feature_walkthrough/FC005.txt) · SHA-256 `e3378e24be3f99a0943f7d5e72b2b1446507d5a219a74770c29d1c4b7226dd19`

## FC006
**F006 · paper-venue-fit-strategy**

Input: `Venue X serves NLP readers; venue Y serves power systems. The paper studies parsing.`

Decision: **conditional**

按当前官方范围核验X的适配性；不根据易录用传闻把Y当同类选择。

验收 / acceptance: 比较表写出主题、读者与正式要求的证据。

[Frozen input](../tests/fixtures/feature_walkthrough/FC006.txt) · SHA-256 `4a295a1c7673f054fd4cb195a3cc5e6fd89e307578aef51f7c21f6c94728a51e`

## FC007
**F007 · paper-novelty-positioning**

Input: `Prior method uses retrieval plus reranking. Ours uses retrieval plus reranking too.`

Decision: **request_evidence**

比较具体交互、目标函数和可验证效果；不能只把组合名称作为创新。

验收 / acceptance: 贡献表指出实质差异或将定位改为应用/实证贡献。

[Frozen input](../tests/fixtures/feature_walkthrough/FC007.txt) · SHA-256 `08666f4c33bc3af3a2f0800ab1a643f78ca487b4851b79c62823419390b74777`

## FC008
**F008 · paper-abstract-title-contribution**

Input: `Title: Training-Free. Method: We fine-tune the encoder on labels.`

Decision: **revise**

明确训练免费指哪个组件，或修改标题；同步摘要和贡献表。

验收 / acceptance: 标题的训练范围与方法中的实际训练步骤一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC008.txt) · SHA-256 `305ae312c49007b99ff3634f2e9133299acd68086e095609e0914585ce5cb080`

## FC009
**F009 · paper-claim-evidence-auditor**

Input: `The theorem assumes independent errors. The conclusion applies it to correlated agents.`

Decision: **revise**

将定理应用限制到满足假设的情形，或提供相关误差下的新论证。

验收 / acceptance: 结论逐项绑定实际满足的假设。

[Frozen input](../tests/fixtures/feature_walkthrough/FC009.txt) · SHA-256 `f51d4f012e3fc21a010c785221c367c04a99c480d601d7bb128c5f371cd53d77`

## FC010
**F010 · paper-structure-pertinence**

Input: `The title promises efficiency; no runtime or cost measurement appears in results.`

Decision: **revise**

补充与效率主张对应的测量，或删除效率承诺；给出结果导航。

验收 / acceptance: 标题关键词均有可定位的证据。

[Frozen input](../tests/fixtures/feature_walkthrough/FC010.txt) · SHA-256 `ab7d93737394522e9d55e699329d4ed03331bd4b877dbaa380c303b8fb2ec2b7`

## FC011
**F011 · paper-experiment-design**

Input: `We will vary ten knobs and report whichever configuration wins.`

Decision: **revise**

先固定主张和比较问题，定义有利、不利、不确定结果下的决定；探索与确认分开。

验收 / acceptance: 实验规格写明变量、选择规则和对应结论。

[Frozen input](../tests/fixtures/feature_walkthrough/FC011.txt) · SHA-256 `cfbf4ab2b099f1554f3b0208a52ddbd4cfc36fcb2d50d719d02250bb847c9e6e`

## FC012
**F012 · paper-baseline-benchmark-audit**

Input: `Agent A uses 20 calls; Agent B uses 2 calls. The paper attributes the gain to memory.`

Decision: **revise**

加入同预算无记忆对照和质量成本曲线，区分记忆与额外计算。

验收 / acceptance: 只有控制调用预算后的差异用于记忆归因。

[Frozen input](../tests/fixtures/feature_walkthrough/FC012.txt) · SHA-256 `2209426e14f1a2c68d9116c79c3f4ed4cacdabe421bc5e2f36803d2105d9c031`

## FC013
**F013 · paper-ml-validity-leakage**

Input: `The retrieval index includes validation and test answers used during evaluation.`

Decision: **revise**

从索引剔除测试答案并重建评测；保留污染范围和重跑记录。

验收 / acceptance: 索引血缘和隔离后的结果可复查。

[Frozen input](../tests/fixtures/feature_walkthrough/FC013.txt) · SHA-256 `70b0e11d7aac33064b0dfaf33de5a357fe960c3ef2b7f679bcb1ad61d4fe7c18`

## FC014
**F014 · paper-claims-vs-data**

Input: `Runs: 0.80, 0.84, 0.88. Reported three-run mean: 88%.`

Decision: **revise**

重算均值为84%；将摘要表图转为同一数据来源生成。

验收 / acceptance: 对应声明全部为84%，最高值单独标注。

[Frozen input](../tests/fixtures/feature_walkthrough/FC014.txt) · SHA-256 `f8df7f93e8f7c9a669b2364528a97080516120e75251fdfde0ece1420b53ba07`

## FC015
**F015 · paper-figure-table-auditor**

Input: `Caption: 95% confidence interval. Plot metadata: error bars are standard deviations.`

Decision: **revise**

纠正误差线定义或按正确独立单位重新计算区间，核对图注和正文。

验收 / acceptance: 实际误差线计算与图注术语一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC015.txt) · SHA-256 `f9f332a1bb4140fb0ea9d9f8a2244bcd4c0f29203d2cabb338f985ceb8f50186`

## FC016
**F016 · paper-formula-audit**

Input: `O(NM) is always faster than O(N log N). No relation between M and N is given.`

Decision: **revise**

指定M与N的增长关系，区分渐近阶和实际耗时；给出M=N等反例。

验收 / acceptance: 不再以无条件Big-O比较证明运行更快。

[Frozen input](../tests/fixtures/feature_walkthrough/FC016.txt) · SHA-256 `24600b81933e8b68cffc5dde772467d99a6537ad5f4afd0a2dd98d621e5b6c0b`

## FC017
**F017 · paper-theory-proof-audit**

Input: `Claim: x squared is strictly positive for every real x.`

Decision: **revise**

用x=0反驳严格正性；改为非负，或增加x不等于0的假设。

验收 / acceptance: 原命题的零值边界被修正，修改后的假设与结论一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC017.txt) · SHA-256 `e7a14757cb5921a54d572cb53b24164ddb7373771b06a80ff30e93458f330722`

## FC018
**F018 · paper-systems-performance-audit**

Input: `A warm-cache run is compared with B cold-start latency; only the mean is reported.`

Decision: **revise**

按相同冷热条件比较，补充样本量和相关尾延迟，说明端到端范围。

验收 / acceptance: 相同测量条件下的分布而非混杂均值支持速度结论。

[Frozen input](../tests/fixtures/feature_walkthrough/FC018.txt) · SHA-256 `a55cbb899119babf8a8a620fd7bf3217a64f35d2e85e7f32fb62942efc73f035`

## FC019
**F019 · paper-dataset-benchmark-paper**

Input: `The leaderboard lets teams query hidden labels after every submission.`

Decision: **revise**

隔离测试反馈并定义提交策略和版本；检查反复调参带来的测试集适应。

验收 / acceptance: 维护政策和最终保留测试能够支持泛化评估。

[Frozen input](../tests/fixtures/feature_walkthrough/FC019.txt) · SHA-256 `4cc8ece153f40b12278a98a4997630733ea57606f0a77b9f0d75d1fa3aed54d4`

## FC020
**F020 · paper-user-study-audit**

Input: `All participants use A first and B second. Authors attribute better B scores to the UI.`

Decision: **revise**

检查学习与疲劳效应；采用反平衡设计或限定因果解释。

验收 / acceptance: 顺序效应与系统效应被识别或结论相应收窄。

[Frozen input](../tests/fixtures/feature_walkthrough/FC020.txt) · SHA-256 `5a7d03c6bdcd8eb9c5c67dc4edcf37436ff76e220513d35fbda5c5d6617b6748`

## FC021
**F021 · paper-citation-check**

Input: `A DOI resolves to a genuine paper on vision, but it is cited for a language-memory theorem.`

Decision: **request_evidence**

分别核验身份和定理支持；真实DOI不能替代文中命题的来源。

验收 / acceptance: 提供相关定理位置，或更换/删除不支持该断言的引用。

[Frozen input](../tests/fixtures/feature_walkthrough/FC021.txt) · SHA-256 `e5d0fdf9c103658131a12ddad186e63c4d358961cf4b818c1c1819d336cf7d74`

## FC022
**F022 · paper-security-ethics-safety**

Input: `Public examples contain named customer conversations without a documented release basis.`

Decision: **request_evidence**

检查授权与去标识化；用脱敏样例替换，并在发布前核验许可。

验收 / acceptance: 公开材料没有未授权可识别信息，授权依据可查。

[Frozen input](../tests/fixtures/feature_walkthrough/FC022.txt) · SHA-256 `34b00dbcef864df92c0c80d8cf2a6163fdadfa7aa75fa9a10cf8770b9916c634`

## FC023
**F023 · paper-limitations-threats**

Input: `Limitation: every study has limitations. All experiments use one hospital.`

Decision: **revise**

具体说明单中心选择如何影响目标人群泛化及已有缓解。

验收 / acceptance: 局限对应实际主张、影响路径和剩余证据。

[Frozen input](../tests/fixtures/feature_walkthrough/FC023.txt) · SHA-256 `5e3f2a6f39921b873254f54ac080d75c1c2ff6855ca88aedc198168d2d14fbd9`

## FC024
**F024 · paper-artifact-evaluation**

Input: `README lists a command, but no execution output or environment lock is available.`

Decision: **request_evidence**

把现状记录为可尝试的复现入口；请求环境锁定和实际输出。

验收 / acceptance: 实际命令、环境、返回码、输出与图表对应。

[Frozen input](../tests/fixtures/feature_walkthrough/FC024.txt) · SHA-256 `d0087b8e33d057599467b0541edbd3858348c30ac21bb02b08d95be2a1c570d5`

## FC025
**F025 · paper-repro-compliance**

Input: `The source compiles, but the submitted PDF clips the final column of Table 3.`

Decision: **revise**

检查最终PDF页图并调整表宽，重新编译后复查全部列。

验收 / acceptance: 目标版面中表3内容完整可读。

[Frozen input](../tests/fixtures/feature_walkthrough/FC025.txt) · SHA-256 `68e3440b8eedfaa71a7920417a12ddfe01184c9ad57e1a6b94e5eef8f27cec86`

## FC026
**F026 · paper-writing-auditor**

Input: `The results shows a higher success rate on the evaluated tasks.`

Decision: **revise**

改为The results show a higher success rate on the evaluated tasks.，保持评测范围。

验收 / acceptance: 主谓一致且不新增全领域或因果结论。

[Frozen input](../tests/fixtures/feature_walkthrough/FC026.txt) · SHA-256 `8543403d700001369b2afaed6fa8c95a5dfd80efbf2d1018e95ee4570c3925ec`

## FC027
**F027 · paper-ai-prose-signals**

Input: `Three adjacent paragraphs start with It is important to note that; a fourth uses an em dash.`

Decision: **revise**

指出前三处重复且检查是否有信息；普通破折号保留，不据此判定作者身份。

验收 / acceptance: 删除冗余但不因标点升级为科学问题。

[Frozen input](../tests/fixtures/feature_walkthrough/FC027.txt) · SHA-256 `5736361774ebf1c53e5e190af04407e6c1b0f98cde158d34873c5b580792023f`

## FC028
**F028 · paper-external-review-triage**

Input: `The external review says there is no ablation. Section 4.3 contains a matched-budget ablation.`

Decision: **retain**

核读4.3后撤回缺失意见；若仍有具体混杂，再单独列出。

验收 / acceptance: 最终意见忠实对应附录/正文已有实验。

[Frozen input](../tests/fixtures/feature_walkthrough/FC028.txt) · SHA-256 `16ec602adc005cf07397caef8ec0a7235714d706cd658fba45142462761c5635`

## FC029
**F029 · paper-rebuttal-response**

Input: `Response: We have run the requested experiment. The experiment is only planned next month.`

Decision: **revise**

改为拟开展并说明当前证据和可完成替代；完成后再更新为已运行。

验收 / acceptance: 回应中的完成时态与实际产物一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC029.txt) · SHA-256 `82e29f3d6dfa5edc64c5a101219e3b6454885172796d95cf852c18ab4043d41f`

## FC030
**F030 · academic-paper-reviewer**

Input: `The author asks why ten repetitions on each of five tasks are not fifty independent tasks.`

Decision: **conditional**

guided先问推断单位，再解释同题相关性；引导到按题配对或分层分析。

验收 / acceptance: 作者能指出独立单位，并将修订决定绑定问题ID。

[Frozen input](../tests/fixtures/feature_walkthrough/FC030.txt) · SHA-256 `110cf11ac5fe331b0c1a0fbcaeacf3a7c14807fe52286eaee350294f5f6a20f2`

## FC031
**F031 · paper-audit**

Input: `A deep-review request supplies only two abstract paragraphs and no figures.`

Decision: **request_evidence**

先审已提供段落，明确全文和图像未检查；保留后续全文路径。

验收 / acceptance: 报告不把未读部分列为通过。

[Frozen input](../tests/fixtures/feature_walkthrough/FC031.txt) · SHA-256 `28d9389de2df0821becb96b87da473a7691c29f79448383fe40a61f38db7b973`

## FC032
**F032 · latex-paper-en**

Input: `Edit prose but preserve the source tokens \cite{Smith2020} and \label{eq:loss}.`

Decision: **retain**

保持引用键和标签；只修改正文语法并对源代码差异核对。

验收 / acceptance: 键、标签、公式宏不被润色意外改写。

[Frozen input](../tests/fixtures/feature_walkthrough/FC032.txt) · SHA-256 `3c56c85eb3eb4f134f30548975234103a51f3d5bf9177698621ea6d7aff2d384`

## FC033
**F033 · latex-thesis-zh**

Input: `学校模板要求中英文摘要对应；英文摘要删除了中文中的未达到显著性。`

Decision: **revise**

恢复统计限定，建立中英术语与句子对照，并按实际学校模板检查。

验收 / acceptance: 两种摘要的结论强度和数量一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC033.txt) · SHA-256 `74b265d9e84810753e12f664acffc6f0bed160f9b271eaea9fa3d9bd9d374655`

## FC034
**F034 · typst-paper**

Input: `A prose edit renamed @smith2020 but did not change the Hayagriva bibliography key.`

Decision: **revise**

恢复或一致更新引用键；保留Typst函数和公式结构，执行实际构建。

验收 / acceptance: 无未解析引用，编辑前后文献身份相同。

[Frozen input](../tests/fixtures/feature_walkthrough/FC034.txt) · SHA-256 `2e9b97347e05bffb48e34cc9dccb8bf84b2387d0e77eb75dc9d3bfd9e6ffd880`

## FC035
**F035 · cover-letter**

Input: `Cover letter says first-ever clinical validation; manuscript reports an offline benchmark.`

Decision: **revise**

改为实际离线评测贡献；将投稿信逐项映射到正文，删除未做的临床验证。

验收 / acceptance: 每句研究声明有相应正文依据。

[Frozen input](../tests/fixtures/feature_walkthrough/FC035.txt) · SHA-256 `a47cbca6b2817b27cc8cf56d6e0e06fb84405157906550610e92c9cb1690aaa1`

## FC036
**F036 · bib-search-citation**

Input: `Shared library contains keys used2024 and spare2023. Only used2024 is cited.`

Decision: **retain**

保留未引用的共享条目，提供原始条目精确导出；另查真正未定义的键。

验收 / acceptance: unused不被自动删除，缺键与未用键分开。

[Frozen input](../tests/fixtures/feature_walkthrough/FC036.txt) · SHA-256 `b040a6b10b928c65a613b205fabdf32e128bd844ebcc6fb63db575a3e24b1394`

## FC037
**F037 · paper-skill**

Input: `Chinese draft: 可能改善已测任务. English draft: guarantees success in every domain.`

Decision: **revise**

英文保持可能性和已测范围；保留作者结构并同步论点证据图。

验收 / acceptance: 翻译不会把可能变保证、把局部变全部。

[Frozen input](../tests/fixtures/feature_walkthrough/FC037.txt) · SHA-256 `7598056cc590df5228106d213c897658b31beb5babfc99bab738d81dcee8869d`

## FC038
**F038 · peer-review**

Input: `A fixable statistical objection appears only in the confidential editor note.`

Decision: **revise**

在作者意见中清楚提出统计问题和可执行修复；保密通道用于适当编辑事项。

验收 / acceptance: 作者能够看到并修复影响结论的问题。

[Frozen input](../tests/fixtures/feature_walkthrough/FC038.txt) · SHA-256 `51636ab6d53570dc98dbbf5f4000b963938841a69367799339dd4a3f7c9502cb`

## FC039
**F039 · scientific-critical-thinking**

Input: `Patients self-select treatment; an observed association is called causal proof.`

Decision: **revise**

检查混杂与选择机制；采用与设计一致的关联措辞或补充识别策略。

验收 / acceptance: 不把未经识别的关联写成因果证明。

[Frozen input](../tests/fixtures/feature_walkthrough/FC039.txt) · SHA-256 `a84fec23ca9143c792ffe92d3864bcbad2386e925d0cd7cded73ecce0773e67c`

## FC040
**F040 · statistical-analysis**

Input: `p=0.08, therefore the two methods are equivalent.`

Decision: **revise**

非显著不等价；等效主张需要预设容许界值和相应区间/检验。

验收 / acceptance: 结论与实际检验目标一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC040.txt) · SHA-256 `ca9094118e0d96ef3e01eab729c84e8aaa6ed5b77523a2fd26d0ac08d2a6c81a`

## FC041
**F041 · scientific-visualization**

Input: `A line plot uses a clearly labeled y-axis from 25 to 40 to compare close scores.`

Decision: **retain**

检查比例和图注；清晰标示的线图缩放无需机械改成零起点。

验收 / acceptance: 未凭非零坐标单独制造科学缺陷。

[Frozen input](../tests/fixtures/feature_walkthrough/FC041.txt) · SHA-256 `57bab37163ca8b934b0dacc75e1811bd4915691402c97b4f48b77153314d8d65`

## FC042
**F042 · scientific-writing**

Input: `The Results section adds a new participant exclusion that is absent from Methods.`

Decision: **revise**

在方法中交代排除规则和时间点，在结果中报告对应数量与影响。

验收 / acceptance: 读者能够重建分析人群和选择过程。

[Frozen input](../tests/fixtures/feature_walkthrough/FC042.txt) · SHA-256 `cc79fe14cda8fef52b99abcebd2002059713e4f1c07505be9ac5a0634f2bd818`

## FC043
**F043 · citation-management**

Input: `Two BibTeX entries share one key but describe different papers.`

Decision: **revise**

分配稳定唯一键并校正文内引用；核验元数据，不静默覆盖。

验收 / acceptance: 每个引用键唯一对应一篇正确文献。

[Frozen input](../tests/fixtures/feature_walkthrough/FC043.txt) · SHA-256 `5a6d35bcb0d5283f394295d84775f94bf8e9c75b36214d3917e52a4995332385`

## FC044
**F044 · scholar-evaluation**

Input: `The rubric awards soundness points solely for author affiliation prestige.`

Decision: **revise**

移除名望代理，定义针对论文方法和证据的锚点；记录维度分歧。

验收 / acceptance: 评分与可观察研究内容对应。

[Frozen input](../tests/fixtures/feature_walkthrough/FC044.txt) · SHA-256 `ab213151b7b27d8db1636e27a451e30ef3b0ec4f21052e6085301291a6264a76`

## FC045
**F045 · research-review**

Input: `Two review rounds repeat the same resolved complaint without new evidence.`

Decision: **retain**

保存解决证据，停止重复升级；把下一轮用于仍开放的实质问题。

验收 / acceptance: 收敛记录区分已解决与未解决事项。

[Frozen input](../tests/fixtures/feature_walkthrough/FC045.txt) · SHA-256 `f0b8fd73a27a2fc439ea8e95d5e2387e20649c7ab8c53c1f231e6c107102e270`

## FC046
**F046 · experiment-audit**

Input: `The evaluator defines accuracy() but reports a fixed constant instead of calling it.`

Decision: **revise**

追踪实际指标调用到输出，移除常量替代并重跑受控评测。

验收 / acceptance: 执行轨迹和输出来自指定指标与真实标签。

[Frozen input](../tests/fixtures/feature_walkthrough/FC046.txt) · SHA-256 `901b61f970ffe85a2147d68ab22d2cfc650b19f47a4a3271bb5e56d16866f49c`

## FC047
**F047 · paper-claim-audit**

Input: `A report certifies Table 1 but its input hash belongs to yesterday's manuscript.`

Decision: **request_evidence**

重新绑定当前稿和结果的哈希，在新任务中核查受影响主张。

验收 / acceptance: 报告输入版本与交付稿一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC047.txt) · SHA-256 `8e7fdb2c6e4e6c93cddbde92fcdf9b28fa94d057294addaabda70ba09b038455`

## FC048
**F048 · result-to-claim**

Input: `The output exists and its mean is correct; the comparison changes both model and budget.`

Decision: **revise**

保留数值结论，拒绝单机制归因；增加匹配对照或限定为系统级比较。

验收 / acceptance: 可用性、算术、科学支持三种状态各自记录。

[Frozen input](../tests/fixtures/feature_walkthrough/FC048.txt) · SHA-256 `7f5667112e36d21ba19a32f5a542447449defda72d156376a816534dc3f0d526`

## FC049
**F049 · pre-submission-reviewer**

Input: `The draft uses a normal em dash and readable PNG; no venue rule prohibits either.`

Decision: **retain**

保留合法表达与图像，继续检查实际逻辑、语法、图注和排版。

验收 / acceptance: 不把风格偏好升级成重大缺陷。

[Frozen input](../tests/fixtures/feature_walkthrough/FC049.txt) · SHA-256 `b03058243681e03152efb241e1e012dfbafbbcdb4cefaa09b96d2e5df7c98f9a`

## FC050
**F050 · figure-designer**

Input: `The author needs a method overview linking retrieval, reranking and answer generation.`

Decision: **conditional**

给出左到右文本布局、各模块输入输出和箭头；标示真实组件并选择合适工具。

验收 / acceptance: 布局能画出且与方法一致，不虚构性能数字。

[Frozen input](../tests/fixtures/feature_walkthrough/FC050.txt) · SHA-256 `c98b6bd616ada189f99024f7ae7b785ab1b8bf653bc39afd69fac921b754fdb7`

## FC051
**F051 · paper-polish**

Input: `Original: The effect may be task-dependent. Proposed polish: The effect is universal.`

Decision: **revise**

保留may和task-dependent，仅改善语法节奏；原句清楚时可不改。

验收 / acceptance: 润色保持不确定性与适用范围。

[Frozen input](../tests/fixtures/feature_walkthrough/FC051.txt) · SHA-256 `4642dac3367cf9cddefd32e3414501396f3f5c22df793f5852c260c9a5e6ddbd`

## FC052
**F052 · ieee-reviewer**

Input: `Comment: Novelty is weak. No prior method or affected claim is named.`

Decision: **revise**

定位贡献和最接近方法，指出差异缺口并给最小修复建议。

验收 / acceptance: 质疑与具体证据、修复要求成对出现。

[Frozen input](../tests/fixtures/feature_walkthrough/FC052.txt) · SHA-256 `57d2ef3c5f49236e7970220ec1b3de03f73c7c54b5853e2abb17486711a033c6`

## FC053
**F053 · ieee-experiment**

Input: `A proposed ablation disables the input parser and makes the whole system unusable.`

Decision: **revise**

采用保持输入输出接口的替代组件，隔离目标机制而不是测试系统破坏。

验收 / acceptance: 对照仍可完成任务，只有目标因素变化。

[Frozen input](../tests/fixtures/feature_walkthrough/FC053.txt) · SHA-256 `b4a6c35a409b9d6b9c6f703537e500f5349daa2f84ff7d0b18bde365f86d08b0`

## FC054
**F054 · ieee-figure-table**

Input: `Table mixes accuracy values 0.84 and 82 under one percent header.`

Decision: **revise**

统一单位为84和82，标明分母、方向、聚合及不确定性。

验收 / acceptance: 同一表格列中的分母、百分比单位与指标含义均保持一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC054.txt) · SHA-256 `5f2669e999ca9a8096155fcb3f4aa839fec5a7be5b72ca9cc762baa6c251e175`

## FC055
**F055 · peer-review-skill**

Input: `The manuscript is a narrative survey; the reviewer demands a randomized clinical trial.`

Decision: **retain**

按综述目标检查覆盖、选择与分类，不套用不相关的试验要求。

验收 / acceptance: 审查规范与文章类型一致。

[Frozen input](../tests/fixtures/feature_walkthrough/FC055.txt) · SHA-256 `1798d4e9490c5e28cfc993572873101ef09e74a72bb1497af5d3cc50d9ba7d14`

## FC056
**F056 · scientific-manuscript-review**

Input: `A geophysical inversion claim ignores the sensor geometry used to recover the parameter.`

Decision: **request_evidence**

按物理可辨识性检查采集几何、前向模型和参数非唯一性；请求敏感性依据。

验收 / acceptance: 结论与实际观测几何的约束相符。

[Frozen input](../tests/fixtures/feature_walkthrough/FC056.txt) · SHA-256 `efe806ec07c730083d34e440eb52982b689239b3f19f5cc07614d0dd04fbf121`

## FC057
**F057 · paper-self-review**

Input: `Abstract says 100 tasks; Methods says 80 eligible tasks; the denominator is unexplained.`

Decision: **revise**

对照排除流程、分析集合和结果分母，统一口径并说明原因。

验收 / acceptance: 跨章节样本数量可核对。

[Frozen input](../tests/fixtures/feature_walkthrough/FC057.txt) · SHA-256 `025d1d331718dd8e9763a9029b965f088ec35a08aa72fd861a427b62bcf2dcd8`

## FC058
**F058 · results-analysis**

Input: `A plot was manually redrawn to make curves agree with a narrative; the CSV disagrees.`

Decision: **revise**

从冻结的结果生成图，保留冲突版本并重新确定能支持的论断。

验收 / acceptance: 图中值能够追溯到指定数据和脚本。

[Frozen input](../tests/fixtures/feature_walkthrough/FC058.txt) · SHA-256 `bd0a4750988f8b675abefde330934f903392c0a5efb1e30b01464c6f96d27460`

## FC059
**F059 · citation-verification**

Input: `A real 2020 DOI is attached to a different 2024 title and author list.`

Decision: **revise**

查规范元数据和实际全文，分别修正身份字段及支持关系。

验收 / acceptance: 作者、年份、标题、标识符对应同一文献。

[Frozen input](../tests/fixtures/feature_walkthrough/FC059.txt) · SHA-256 `2550410641a4cc7742ee1e3afad14c82998da48d2134e1565076a2d450001173`

## FC060
**F060 · ml-paper-writing**

Input: `The central story is speed, but the frozen results show only a robustness improvement.`

Decision: **revise**

重建主张证据表，选择有支持的稳健性叙事，保留未改进的速度结果。

验收 / acceptance: 标题到章节主线对应真实结果而非预设故事。

[Frozen input](../tests/fixtures/feature_walkthrough/FC060.txt) · SHA-256 `a18437ed00b90ff0c0ebb6fcaac9a84b48888fa8ce28a915bbf1d05a3cc26130`

## FC061
**F061 · paper-review-lite**

Input: `Nine roles use the same model family but are described as nine independent models.`

Decision: **revise**

标明同模型多视角，交叉检查实际意见；跨模型需真实调用来源。

验收 / acceptance: 来源记录不把角色数量当独立模型数量。

[Frozen input](../tests/fixtures/feature_walkthrough/FC061.txt) · SHA-256 `a029fa8208177c3bb16363c81037bfb5c6b4228ec36b2bfd7cc53817f6d14e8f`

## FC062
**F062 · nature-reviewer**

Input: `三份同上下文审稿没有提出数值矛盾。随后审计发现均值标错，汇总应把该错误写成三位审稿人的共同意见。`

Decision: **revise**

将数值矛盾作为审计新增问题，提供重算位置。保留原有报告；同上下文意见按多视角记录，不把后续发现写成既有共识。

验收 / acceptance: 汇总分别列出原始审稿意见与审计发现；均值重算可追溯且冻结报告保持不变。

[Frozen input](../tests/fixtures/feature_walkthrough/FC062.txt) · SHA-256 `28454f7729ab3ed14a73485869b80dbe80d59481448c1beee203e208d23d270f`

## FC063
**F063 · review-revision**

Input: `该方法用了五个模块，并且一项指标没有达到SOTA，所以没有创新，必须全部重做。`

Decision: **revise**

删除按模块数量和单项排名否定创新的结论。先按贡献类型对照最接近工作，定位主张、设置、证据与可保留增量，再提出针对性的实验或表述修订。

验收 / acceptance: 每条创新性质疑对应具体已有结果及本文差异；所要求实验解决现有主张的确切证据缺口。

[Frozen input](../tests/fixtures/feature_walkthrough/FC063.txt) · SHA-256 `6a3a927f6f95db4928feafe3fccf3ac09535a277794fba27c8e0a918799846e3`

