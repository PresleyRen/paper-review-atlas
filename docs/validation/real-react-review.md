# Real-paper demonstration: ReAct v3

## Material and actual work

Source: Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models, v3](https://arxiv.org/abs/2210.03629v3), ICLR 2023. The PDF was downloaded, its text extracted, and rendered pages 5, 6, 8 and 14 inspected. Table values were transcribed and checked against those page images before computation.

The paper identity, SHA-256, page/object inspection log and transcription hashes are recorded in [source.json](../../tests/fixtures/real_react/source.json). The fixtures contain published aggregate values, not original run-level results. This is a targeted review of results, interpretation and presentation; it is not a re-execution of the model experiments or an overall editorial recommendation.

## R01 — Make the WebShop improvement explicit

**Location:** page 8, Table 4 and its following results paragraph. **Disposition:** minor clarification.

The prose uses an approximate absolute improvement. Table 4 permits a more precise statement identifying the comparator and percentage-point unit. The recomputed gains from ReAct's 40.0% success rate are 9.9 points over Act, 10.9 over IL and 11.3 over IL+RL. Relative to Act, the relative percentage improvement is 32.9% to one decimal.

**Suggested replacement:**

> On WebShop, ReAct achieves a 40.0% success rate, exceeding Act, IL, and IL+RL by 9.9, 10.9, and 11.3 percentage points, respectively.

中文解释：写清楚与谁比较、提高的是百分点还是相对百分比；不把论文中的近似表达升级为实验造假或错误数据。

**Acceptance:** each comparator and unit matches Table 4 and the source calculation. The five declared arithmetic checks passed with exit code 0; [actual JSON output](react-correct.json).

## R02 — Preserve the mixed task result

**Location:** pages 5–6, Table 1 and the ReAct/CoT comparison. **Disposition:** retain.

The table shows a 2.0-point disadvantage on HotpotQA and a 4.6-point advantage on FEVER against CoT. The surrounding discussion already describes the mixed result. A reviewer should preserve this distinction, rather than accuse the authors of claiming that the stand-alone method wins on every task.

中文解释：审查同时读取表和解释；不存在的“全面胜出”主张不能成为审稿意见。

## R03 — Do not merge different evaluation subsets

**Location:** page 5, Table 1; page 14, Table 5 and caption. **Disposition:** withdraw a hypothetical mismatch objection.

The appendix explicitly evaluates a 500-question HotpotQA validation subset. Its PaLM/ReAct number differs from the main table, but the evaluations are not established as identical. Keep the different cohort identifiers and ask for clearer cross-referencing if needed. Do not mechanically force the numbers to agree.

中文解释：数字不相同先核查实验范围；原始比较条件不同，不能做错误的全文替换。

## R04 — Preserve a readable zoomed line chart

**Location:** page 5, Figure 2. **Disposition:** retain the axis range.

The displayed line-chart ticks identify a nonzero y range. This is not automatically a misleading bar-length encoding. Review labeling, trends and surrounding claims rather than impose zero on every plot.

中文解释：图表检查应考虑图类型；清晰的线图缩放是本例的正确对照。

## R05 — Preserve the error-analysis denominator

**Location:** page 6, Table 2 and surrounding sampling description. **Disposition:** scope reminder for reuse.

The manual error analysis uses sampled success/failure trajectories. A zero entry in one inspected category is not a population guarantee that hallucination is impossible. Retain the stated sample and category when describing the observation. This reminder applies to any rewrite or secondary summary; it is not an allegation that the paper omitted its sampling description.

## Executed positive/negative control

```bash
# Published values, correctly specified differences: exit 0.
python skills/paper-review-atlas/scripts/atlas.py audit \
  --root tests/fixtures/real_react --spec verified-spec.json

# Deliberate reviewer-created probe: claims 9.9% relative, not 9.9 points.
# Expected actual result: 32.9% rounded; mismatch; exit 1.
python skills/paper-review-atlas/scripts/atlas.py audit \
  --root tests/fixtures/real_react --spec intentional-error-spec.json
```

[Error-probe output](react-error.json). The erroneous relative-percent claim is a test we introduced, not a sentence attributed to the paper. The corrected wording above is a proposal; the public original was not modified.

Ten automated tests check the transcriptions, specified computations, CLI exit codes and numerical macro export. The image interpretation and scientific decisions above were made by the authoring assistant in this development conversation; there was no independent human scoring. This separation keeps a real demonstration distinct from a claimed detection-accuracy benchmark.
