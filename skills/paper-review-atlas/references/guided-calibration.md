# Guided review and reviewer calibration

## Guided review

Use `guided` when the author wants to understand a weakness and decide how to repair it. Read the actual manuscript and select one consequential claim with its strongest existing evidence. Open with a genuine supported strength when relevant; do not manufacture praise.

1. Locate the claim and give a short quotation. Ask one concrete question about the assumption, comparison, independent unit, evidence or interpretation needed to support it.
2. Listen to the answer before supplying the next layer. Accept evidence that resolves the question; update the issue instead of repeating a prepared objection.
3. When a gap remains, contrast two explanations with a small worked example. Explain which observation would distinguish them.
4. Offer a minimal correction and a stronger research option, with their expected resources and consequences. Preserve the author's chosen research objective.
5. End the exchange with the agreed wording, experiment or open question, a stable issue ID, and a checkable completion criterion. Resume from that record next time.

Example: a memory-enabled agent also receives twice as many tokens. Ask what comparison separates memory from computation. A same-budget control is useful; requiring a new dataset unrelated to the claim is not. If the author supplies an existing matched-budget appendix experiment, inspect it and revise the objection.

## Criteria binding and rubric use

When a target venue or rubric is provided, freeze its source, date/version and criterion IDs. Use the same criteria for all review perspectives. Keep criteria for competing venues or disciplines separate. First understand a criterion, then determine its applicability to the manuscript; do not silently replace it with a generic standard.

For a material finding, report the scholarly consequence separately from relevance to the chosen destination. Provide a minimum remedy, an optional stronger remedy, dependencies/costs and the author's decision. An institution name, citation count or journal prestige is not evidence that an argument is valid.

Qualitative judgments should be tied to stated anchors, supporting and contrary evidence. Missing, not applicable and low confidence are distinct. If scores are explicitly requested, define their construct and anchors before rating. Do not turn an ordinal rubric into a publication probability.

## Calibration workflow

Use `calibration` to evaluate review behavior against supplied labels, not to generate labels that automatically validate the reviewer.

1. Freeze the paper revisions, task prompts, rubric, label version, unit of analysis and evaluation split. Keep the answer key out of the reviewer input when a blind evaluation is intended.
2. Execute the review and save its actual output and model/human identity. Record whether the session was fresh and whether model families differed. Distinguish repeated sessions from statistically independent errors.
3. Match findings to labeled issues using an explicit matching policy, including merged root causes, partial matches and severity disagreements. Let a qualified adjudicator decide disputed semantic matches.
4. Convert the adjudicated binary issue records to `{id, gold, predicted}` and run `calibrate`. The helper computes TP, FP, TN, FN, precision, recall and false-positive/negative rates. An undefined denominator yields null.
5. Report the label source, sample count, scope and unresolved disagreements alongside results. For severity levels, record a separate ordinal confusion matrix; binary issue counts do not measure severity agreement.
6. Use errors to update the matching protocol or review instructions on a development split, then evaluate on a held-out split. Do not report tuning-set improvements as independent test performance.

Three deliberately constructed examples can diagnose a failure; they do not calibrate a venue's editorial decisions. A calibration file never automatically modifies live review thresholds.

## Separate report channels

Provide author-facing criticism and repairs in the main review. If the task includes a confidential editor channel, place only appropriate editorial matters there, with clear scope and sources. Do not hide a repairable scientific criticism from the author in a private channel. Preserve bilingual issue IDs so Chinese explanations and English comments refer to the same finding.

## Useful commands

```bash
python SKILL_DIR/scripts/atlas.py plan --mode guided --language zh
python SKILL_DIR/scripts/atlas.py calibrate --root PAPER_DIR --packet calibration.json
python SKILL_DIR/scripts/atlas.py locate academic-paper-reviewer
```
