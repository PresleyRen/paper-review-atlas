# 扩展与缺口登记 / Extending Paper Review Atlas

能力覆盖图的目的，是帮助后续贡献者发现已有能力、重复建设和缺口。新增一个名字不等于实现能力；新增一个测试也不等于证明真实论文审查有效。

## 唯一数据源

在 `skills/paper-review-atlas/config/` 维护三份 JSON：

| 文件 | 用途 |
|---|---|
| `capabilities.json` | 稳定 Cxx ID、分组、中文/英文标题、协议路径、W/D/A 实现层、状态、来源、验证、限制 |
| `sources.json` | 来源仓库与模块、直接链接、查阅日期、正文/目录查阅深度、许可备注、能力对应 |
| `conflicts.json` | 稳定 CFXxx ID、冲突候选策略、取舍理由、适用能力、测试种类和证据 |

生成器输出 `CAPABILITY_MAP.md`、`SOURCES.md`、`CONFLICTS.md`、`coverage.svg`、`coverage.mmd`。不要手工修改这些生成文件作为长期修复；修改登记后重新生成。

## 添加一项能力的步骤

1. **确定问题和边界。** 指出哪类论文、什么证据、何种错误需要检查；说明不适用的情形。先检索现有 Cxx，避免把同一能力换个名字。
2. **分配稳定 ID。** 当前为 C01–C36；扩展可用 C37 起，不重编号旧条目。新组最多四列显示，图会自动增加行数。
3. **实现协议。** 在对应 reference 增补输入、检查步骤、反例、实际输出、修改建议与验收条件。只有实际工具已实现才填写 `implementation.deterministic`；外部需求写入 `adapter`。
4. **核对来源与授权。** 来源必须有主项目链接、查阅深度和许可记录。映射双向一致。来源许可不清楚时，不复制正文/代码；原创实现仍要标清概念来源。涉及实际上游复用时，应另行明确许可范围，不能把 `copied_code` 改成 false 来通过校验。
5. **记录冲突。** 对不同规则的分歧，写明至少一个失败情形、选定规则的依据及可接受的替代路线。不要宣称未经比较的“最好”。
6. **准备正反例。** 至少一例应检出的问题、一例相似但正确的材料、一例证据缺失情形。数字、引用、图像等需要区分定位成功与语义正确。
7. **实际执行。** 工具做自动化测试；语义能力做新上下文任务，输入不附答案。保存原始输出及人工/模型判读规则，披露模型来源。禁止把多角色当独立模型。
8. **更新证据。** `verification.evidence` 可用报告路径，或 `tests/file.py::Class::test_name`。`planned` 表示计划，`partial` 表示部分覆盖，`passed` 只能限于实际运行通过的指定测试。能力图不能暗示一个局部测试覆盖整个科学领域。
9. **生成并检查。** 运行下列命令；更新 README 的数量、接口和变更日志。用真实图像查看器检查 SVG 渲染结果。
10. **版本化发布。** 对接口不兼容变化升级主版本；新增能力升级次版本；明确修复升级补丁版本。保留旧问题 ID 和已有验证记录。

```bash
python scripts/build_coverage.py
python scripts/build_coverage.py --check
python scripts/check_package.py
python -m unittest discover -s tests -v
```

## 当前值得补充的实际缺口

| 方向 | 目前能力 | 可验证的下一步 |
|---|---|---|
| 真实论文基准 | 两份中英文合成全文前向案例及规则测试 | 获得授权的多领域论文集、专家标注、误报/漏报与严重度评估，公开脱敏评测协议 |
| 跨模型一致性 | 定义来源记录与仲裁流程，未内置外部模型服务 | 实际调用两个不同模型家族，保存独立输出与分歧裁决，测量成本和相关错误 |
| 统计推断 | 设计审查协议与配对描述统计 | 增加设计驱动的 CI/检验适配器、正确/错误统计单位对照；不以阈值口诀替代设计 |
| 图表自动解析 | 模型查看实际图像；结构化源数据核对 | 有标注的轴/图例/刻度/误差线图集，测试视觉误报；检测与数据真实性保持区分 |
| 文档格式 | PDF/DOCX/LaTeX/Typst 路由，需要宿主工具 | 独立解析/编译适配器、多栏/公式/交叉引用/中文字体实测与完整渲染比较 |
| 文献支持 | 元数据与实质支持分开的审查流程 | 对接实际文献服务、版本/撤稿状态与逐主张支持判断，记录访问日期和不可获取项 |
| 理论与形式化 | 假设/符号/证明义务/反例协议 | 明确语言范围的形式证明或符号计算适配器；不能从语法通过推断定理成立 |
| 更多学科 | 一般科学与 AI/Agent 扩展；按学科选择标准 | 新建生医/社会/材料等经过专家评估的 profile，附适用条件与学科正反例 |
| 返修长期跟踪 | 稳定 ID、修订证据与声明式重算 | 多版本真实项目的长期回归，检测问题转移、回退与跨图表数字遗漏 |

## English maintenance notes

The three JSON registries are the source of truth. Stable capability IDs, protocol files, source mappings, conflict decisions, and concrete test evidence must evolve together. Generated maps describe implementation scope, not detection accuracy. Add an adverse case, a correct control and a missing-evidence case; use fresh-context behavioral review where a unit test cannot measure semantics. A source inventory entry is not a port. Keep external licenses separate and record actual reuse honestly.

The generator validates registry references, test-symbol existence, safe paths and source reciprocity. It does not execute or authenticate the evidence files. The test suite separately exercises these invariants, including adding C37 without editing the graph template.

## v1.1 feature-level navigation

Start with [EXTENSION_INDEX.md](EXTENSION_INDEX.md) or `atlas.py locate Cxx/Fxxx/Gxx`. The new `features.json` records module-specific facets, complements and representative cases; `gaps.json` records the missing implementation, edit path, test entry and closure criterion. `guide.json` supplies concise bilingual capability descriptions for README. The two existing/generated documentation paths are both maintained: `build_coverage.py` and `build_feature_docs.py`.

For README edits, change `docs/templates/README.zh.md` / `README.en.md`, then regenerate. Keep explanatory validation methodology in validation documents rather than duplicating it throughout the user-facing README. New source modules need a fresh stable Fxxx ID and a representative fixture; the inventory equality tests detect an unmapped module. Source-feature fixture tests check records and anchors, so genuine behavior changes also need an actual review or executable helper test.
