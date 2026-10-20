# Extension index / 缺口定位与补强

Search by capability, module name, feature ID or gap ID. Each open task identifies the actual protocol, the missing implementation, a test entry and a closure criterion.

```bash
python skills/paper-review-atlas/scripts/atlas.py locate C19
python skills/paper-review-atlas/scripts/atlas.py locate F030
python skills/paper-review-atlas/scripts/atlas.py locate G03
```

| Gap | Capability IDs | Edit here | Add / implement | Test entry | Close when |
|---|---|---|---|---|---|
| G01 真实论文专家盲测 | C03, C05, C07, C22, C27 | [references/adversarial-review.md](../skills/paper-review-atlas/references/adversarial-review.md) | 建立获授权的论文与专家逐条标签；按问题类型统计漏检、误报和严重度分歧。 | `python -m unittest discover -s tests -p test_feature_contracts.py -v` | 新增冻结基准、盲测输出、独立判读与重复运行结果 |
| G02 跨模型实际执行 | C12, C27 | [references/adversarial-review.md](../skills/paper-review-atlas/references/adversarial-review.md) | 接入用户选择的模型后端；保存模型家族、版本、输入哈希和原始输出，再交叉裁决。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 不同模型实际调用记录可复查，不能以角色名代替来源 |
| G03 复杂统计推断引擎 | C07, C11, C12 | [references/experiments-statistics.md](../skills/paper-review-atlas/references/experiments-statistics.md) | 增加设计驱动的配对/分层区间与检验适配器；先固定独立单位，再用解析解及模拟覆盖率验证。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 配对、聚类、缺失和多重比较正反对照及数值参考一致 |
| G04 PDF与多栏公式解析 | C01, C19, C35 | [references/input-output.md](../skills/paper-review-atlas/references/input-output.md) | 实现宿主解析适配器；留页图和文字坐标映射，增加中文、多栏与公式案例。 | `python -m unittest discover -s tests -p test_feature_contracts.py -v` | 图注、表格、公式锚点与实际页图一致 |
| G05 DOCX修订痕迹交付 | C23, C28, C35 | [references/revision-rebuttal.md](../skills/paper-review-atlas/references/revision-rebuttal.md) | 将稳定问题ID绑定Word修订与批注；保留原稿并渲染比较。 | `python -m unittest discover -s tests -p test_feature_contracts.py -v` | 接受/拒绝修订后文本、表格、公式和引用仍正确 |
| G06 LaTeX与Typst编译适配 | C15, C30, C35 | [references/input-output.md](../skills/paper-review-atlas/references/input-output.md) | 加入隔离构建；锁定编译器和字体，记录返回码与PDF页图差异。 | `python -m unittest discover -s tests -p test_feature_contracts.py -v` | 标签、引用、公式宏、Hayagriva与中文字体实测通过 |
| G07 文献在线身份与支持核验 | C03, C24, C32 | [references/citations-venues.md](../skills/paper-review-atlas/references/citations-venues.md) | 接入公开元数据与全文；分别记录身份、版本、勘误/撤稿、命题支持。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 已知DOI错配、标题重名、真实但不支持命题均被区分 |
| G08 图表视觉标注基准 | C19, C20, C21 | [references/figures-tables.md](../skills/paper-review-atlas/references/figures-tables.md) | 建立坐标截断、线图缩放、单位、误差线和清晰位图正反图集；用实际视觉输出判读。 | `python -m unittest discover -s tests -p test_real_paper.py -v` | 至少两种图类型和清晰正确对照具有专家标签及视觉日志 |
| G09 实验可复现环境 | C08, C13, C16, C17 | [references/code-reproducibility.md](../skills/paper-review-atlas/references/code-reproducibility.md) | 添加安全运行适配器；锁定环境、真实ground truth、随机种子和结果哈希。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 从干净环境执行到论文表图的完整运行链可重建 |
| G10 更多学科专门规范 | C07, C15, C25, C31, C32 | [references/domain-agent.md](../skills/paper-review-atlas/references/domain-agent.md) | 由领域专家补充地球物理、临床、质性、形式化等profile；记录适用条件和反例。 | `python -m unittest discover -s tests -p test_feature_contracts.py -v` | 各profile有真正适用与不适用的研究案例并经领域核查 |
| G11 返修长期回归 | C23, C28, C29, C34 | [references/revision-rebuttal.md](../skills/paper-review-atlas/references/revision-rebuttal.md) | 准备多版本稿件；检测问题修复后在摘要、附录、译文或图表中重新出现。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 旧问题ID不变、回归问题重新打开、全部受影响位置被复核 |
| G12 BibTeX扩展语法 | C24, C35 | [references/citations-venues.md](../skills/paper-review-atlas/references/citations-venues.md) | 加入宏展开、crossref继承及复杂查询过滤；保留原始条目，使用标准语法对照集。 | `python -m unittest discover -s tests -p test_extensions.py -v` | 宏、交叉引用、括号引用和坏文件恢复各有对照 |

## Maintenance sequence

1. Locate Cxx/Fxxx/Gxx; retain existing IDs. Add a new ID only for a genuinely new capability or source module.
2. Implement the missing protocol/helper/adapter, update the feature facets and reciprocal source mappings.
3. Add an erroneous example, a similar correct control and a missing-evidence case. Exercise actual code or save an actual semantic review, labeling the execution type.
4. Record disagreements and the rule used to resolve them in the conflict register.
5. Run all tests, regenerate both sets of documentation, and commit the inputs and generated outputs together.

```bash
python scripts/build_coverage.py
python scripts/build_feature_docs.py
python -m unittest discover -s tests -v
python scripts/build_coverage.py --check
python scripts/build_feature_docs.py --check
python scripts/check_package.py
```
