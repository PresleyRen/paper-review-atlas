# CLI 与证据接口 / CLI and evidence interface

所有命令从 `skills/paper-review-atlas/scripts/atlas.py` 运行。它们不调用 LLM、不联网、不执行论文代码。指定 `--root` 授权证据根目录，JSON 中的路径限定在该目录内。

## 命令与退出码

```text
atlas.py plan --mode MODE --language auto|zh|en --domain general|agent
atlas.py preflight --root DIR --manifest manifest.json
atlas.py audit --root DIR --spec audit-spec.json
atlas.py validate-report --root DIR --report review.json
atlas.py recheck --root DIR --packet recheck.json
atlas.py capabilities
atlas.py verify-install
```

| 退出码 | 含义 |
|---|---|
| 0 | 对该命令声明范围的操作成功；不是论文通过审稿 |
| 1 | 存在 mismatch、invalid，或复核中的已知无效记录 |
| 2 | 输入不合法、文件解析错误、不支持的操作或路径越界 |
| 3 | 源证据不可用或复核未验证，不能当成功 |

结果保留逐项状态；混合情况优先返回已发现的不一致。`recheck` 顶层 `open` 表示原问题仍开放，`validation.status` 区分无效记录和缺失证据。问题本身仍采用 confirmed/unverified/closed。

## 材料清单

```json
{"artifacts":[{"path":"manuscript.md","role":"manuscript"},{"path":"figure1.png","role":"rendered_figure"}]}
```

`preflight` 的 `available_uninspected` 仅说明文件存在。源文件存在、图像已查看、源数据已重算是不同状态。

## 数值检查

`audit` 接受 `quotes`、`numeric_claims`、`paired_runs` 三个数组，至少一项检查。完整示例见 [audit-spec.example.json](../skills/paper-review-atlas/assets/audit-spec.example.json)。

```json
{
  "numeric_claims": [{
    "id": "accuracy-mean",
    "source": {"path":"results.csv","format":"csv","where":{"model":"proposed"}},
    "operation":"mean", "field":"accuracy",
    "source_unit":"fraction", "reported_unit":"percent",
    "reported":"84.0", "rounding":{"places":1,"mode":"half_even"},
    "tolerance":"0"
  }]
}
```

`source` 支持 CSV、JSON 对象数组、或 JSON 对象中 `records_key` 指定的一层数组。JSON 键重复、非有限值、缺字段、数据超界等不会被静默接受。`where` 是最多 16 个标量相等条件，没有表达式解释器。CSV 单元格是字符串，因此按种子筛选时使用 `"seed":"11"`；JSON 标量保留类型，字符串 `"11"` 不等于数字 `11`。

操作为 `value`、`mean`、`sum`、`count`。`value` 恰好选择一行；`count` 省略 field 且使用 number 单位。空组保守地视为 unverified，不能用它证明不存在任何观测。缺值不被偷偷删除。总文件不超过 5 MiB，记录不超过 10,000。

单位为 `number`、`fraction`、`percent`、`percentage_point`。只进行声明支持的转换；不自动识别秒/毫秒、金额或其他物理单位。时间单位换算需要审稿人明确核验，或另行准备可追溯计算。

`rounding.places` 为 -12 到 12 的整数；mode 支持 `half_even` 和 `half_up`。容差是**舍入后、报告单位中的绝对容差**，默认 0。使用 Decimal，命令规格中的小数也在解析时保持十进制精度；推荐把高精度数值写为字符串，便于上下游系统保留。

### 相对百分比与百分点

主 `source` 是新方法，`comparison` 是基线；两者共用 `source_unit`。

```json
{
  "source":{"path":"results.csv","format":"csv","where":{"model":"proposed"}},
  "operation":"mean", "field":"accuracy",
  "comparison":{"source":{"path":"results.csv","format":"csv","where":{"model":"baseline"}},"operation":"mean","field":"accuracy"},
  "change":"relative_percent", "source_unit":"fraction", "reported_unit":"percent",
  "reported":"5.0", "rounding":{"places":1,"mode":"half_even"}
}
```

`relative_percent = (new − baseline) / baseline × 100`。例如 80%→84% 是相对提升 5%；`percentage_points` 则是提升 4 个百分点，须用 `reported_unit:"percentage_point"`。基线为零时相对变化未定义，返回 unverified。

### 配对描述统计

```json
{"paired_runs":[{"id":"seeds","left":{"11":0.79,"22":0.80,"33":0.81},"right":{"11":0.80,"22":0.84,"33":0.88}}]}
```

必须有完全相同的非空 run ID 集合；不按位置猜测配对，不丢弃多余行。输出两侧均值、样本 SD（n−1）、right−left 的逐对差与差值描述统计。只有一个配对时差值可计算，但 SD 和推断保持未验证。即使 n>1，也不会输出 p 值/置信区间或声称独立单位已经成立。

## 精确引用

```json
{"quotes":[{"path":"manuscript.md","quote":"The baseline accuracy was 80.0%.","line":12}]}
```

line 可省略；提供时要求引用从真实 1-based 行开始。不模糊匹配、不自动改 Unicode、不修正伪造行号。原文可为中文、多行、CRLF；返回实际匹配范围。引用存在只验证定位。

## 报告结构

每个 issue 使用 `id`、`status`、`severity`、`location`、`evidence`、`fix` 和 `acceptance_check`。推荐同时提供 title、consequence、evidence_basis 与 provenance。见 [report.example.json](../skills/paper-review-atlas/assets/report.example.json)。

`confirmed` / `closed` 的原文证据必须在 root 下匹配；无 root 的 Python API 不会把自称 verified 的记录升级为已验证。`issues:[]` 合法，不强制产生问题。结构化录用概率字段被拒绝；这不是对任意自然语言概率文本的完整检测。

多审稿来源可声明 `reviewers:[{id,model,family,persona}]` 和 `independence_claim:none|multi_persona|cross_family`。cross_family 至少需要两个不同家族；工具只检查声明一致性，不认证远端模型身份。

视觉覆盖示例：

```json
{"coverage":{"figures":{"status":"passed","kind":"visual","artifacts":["figure1.png"],"evidence":[{"path":"inspection.md","quote":"I viewed figure1.png and checked the visible axis labels."}]}}}
```

这只验证记录锚点和图像文件可用。检查者仍须实际查看图像，不能以此 JSON 制造“看过”的事实。

## 修改后复核

复核 packet 包含 `issue`（原问题）、`revision_evidence`（新版本位置与引用）和 `check`。

```json
{
  "issue":{"id":"PRA-001","status":"confirmed","severity":"major","location":{"path":"old.md"},"evidence":{"quote":"The mean accuracy is 88.0%."},"fix":"Use the mean across all declared seeds.","acceptance_check":"Recompute the mean and reconcile the revised text."},
  "revision_evidence":{"path":"revised.md","quote":"The mean accuracy is 84.0%."},
  "check":{"status":"passed","method":"Recomputed the three-seed mean using the bundled numeric checker.","evidence":{"path":"check-log.md","quote":"Calculated accuracy: 84 percent."},"evaluation":{"kind":"number","claim":{"source":{"path":"runs.csv","format":"csv"},"operation":"mean","field":"accuracy","source_unit":"fraction","reported_unit":"percent","reported":"84.0"}}}
}
```

`evaluation.kind` 支持 `number` 或 `quote`。声明式重算真实执行；若重算失败，自称 passed 不能关闭问题。其闭环范围标为 `declarative_check_recomputed`。

人工/视觉检查省略 evaluation，但必须提供具体 method、observations 和可定位的检查日志；范围标为 `recorded_evidence_only`。泛泛的“looks good / reviewer approved / 已完成”不够。仍需原问题证据、修改证据和真正执行的验收。工具没有能力凭日志认证某个人确实看过图或某个完整实验确实运行成功。

## v1.1 helpers

All packet commands take `--root EVIDENCE_DIR --packet FILE.json`. The packet itself and declared evidence paths remain within that root.

### Feature and repair lookup

```bash
python skills/paper-review-atlas/scripts/atlas.py locate C19
python skills/paper-review-atlas/scripts/atlas.py locate F030
python skills/paper-review-atlas/scripts/atlas.py locate G03
```

`locate` returns capability definitions, matching source features and complementary lanes, plus open gaps containing `edit_location`, `remedy`, `test_command` and `acceptance_check`. Unknown queries return empty results; no new capability is invented. All five registries travel with the installed skill. `guide.json` is a documentation presentation register.

### Calibration

```json
{"records":[{"id":"issue-1","gold":true,"predicted":true},{"id":"control-1","gold":false,"predicted":false}]}
```

`calibrate` computes TP/FP/TN/FN, precision, recall and false-positive/negative rates. IDs must be unique and labels strict booleans. Undefined denominators return null. Labels and finding matches must be established before this arithmetic step.

### Conflict policy

```json
{"rule":"CFX04","facts":{"unit_ids":["task-1","task-1","task-2","task-2"],"independence_justified":true}}
```

`policy` returns `group_or_justify`, four observations and two distinct units. The complete CFX01–CFX16 packet examples are in `tests/fixtures/conflicts/cases.json`. CFX01 and CFX16 perform source checks; other rules route supplied facts. Missing or incorrectly typed facts are errors. A detected numeric mismatch or failed closure produces exit 1; a requested unverified numeric source produces exit 3.

### Numerical macros

```json
{"claims":[{"name":"MeanScore","claim":{"source":{"path":"runs.csv","format":"csv"},"operation":"mean","field":"accuracy","reported":"84","source_unit":"fraction","reported_unit":"percent"}}]}
```

`export-macros` returns JSON with `tex` and source checks. Output is emitted only when every claim verifies. The above source values 0.80, 0.84, 0.88 produce `\newcommand{\MeanScore}{84\%}`. Only unique ASCII-letter names are accepted and common TeX control names are rejected. No manuscript is changed and no TeX is executed. Save the `tex` field only after reviewing the check output.

### Local bibliography

```json
{"bib_path":"references.bib","citations":["used2024"],"query":"memory"}
```

`bib-audit` returns matching original entries, duplicate keys, undefined citations and informational uncited keys. Balanced braces, quoted fields and parenthesized entries are scanned; broken entries are rejected. Query matching is literal, case-insensitive text search. Macro expansion, crossref inheritance, advanced author/year operators and online identity/claim support are separate adapter work (G07/G12).

### Additional modes

`plan --mode guided` and `plan --mode calibration` route to `references/guided-calibration.md`. The installed helper does not silently launch external reviewers or load gold labels into a purportedly blind reviewer context.

## Reviewer priorities (1.2)

`plan --mode priorities --domain agent --language zh` selects the new pass. Full/quick automatically include it. `policy` now accepts CFX17–CFX22 with the fact schemas demonstrated in `tests/fixtures/reviewer-priorities-cases.json`. `locate F062`, `locate F063` and `locate G13` navigate the two new source integrations and video-source repair task.

Reproduce decisions with `python scripts/compare_reviewer_priorities.py`. Policy exit 0 means the input was valid and an action was returned, not that the paper passed review.
