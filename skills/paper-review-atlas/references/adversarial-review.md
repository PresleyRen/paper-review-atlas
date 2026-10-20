# Adversarial review and objection adjudication

Use strong criticism to expose real failure modes, then test the criticism itself. The objective is a more accurate assessment, not a predetermined negative verdict.

## Contents

- Role design and honest provenance
- Construct the strongest objection
- Challenge and adjudicate objections
- Merge findings and advise the author
- Common false positives

## Role design and honest provenance

Choose roles for their distinct questions, not for the appearance of a larger reviewer count.

| Role | Central question |
|---|---|
| Domain reviewer | Does the work address a meaningful gap with appropriate field assumptions? |
| Methods reviewer | Does the design identify the claimed effect or mechanism? |
| Evidence auditor | Do claims, source data, code, tables, and figures agree? |
| Skeptical reviewer | What plausible alternative most threatens the central contribution? |
| Author-side responder | What existing evidence or reasoning defeats that objection? |
| Adjudicator | Which objections survive checking, with what scope and severity? |

A single model can perform these passes. Explicitly label them as roles from one model rather than independent reviewers.
If different models or people are available, record their actual identities/roles, materials, and outputs as appropriate.
Different model families can add diversity; they do not establish calibrated independence or a measured error rate.
Do not invent external reviewers, backend calls, multiple model execution, or reviewer agreement.
Use an independent execution context when available and useful, but do not block a useful review solely because one is unavailable.
Keep a common manuscript version and evidence inventory so disagreement is not merely version mismatch.
For higher-stakes or difficult claims, consider genuinely separate expert checking when available; state what actually occurred.

## Construct the strongest objection

For each central claim, develop the most consequential plausible challenge grounded in the inspected work.
Examples include a competing mechanism, confounded comparison, invalid statistical unit, hidden leakage, an unmet theorem assumption, or an evaluation metric that misses the claimed capability.
Do not generate objections simply to reach a target number.
Form the objection as a testable statement:

1. The exact claim or inference under challenge.
2. The inspected evidence prompting the concern.
3. The alternative explanation or failure condition.
4. Why it would change the paper's conclusion.
5. The evidence that would defeat or confirm the objection.

Example: “The proposed planner outperforms the baseline, but it receives twice the tool-call allowance. A budget advantage could explain the gain. A matched-budget curve would distinguish planning quality from additional search.”
Avoid: “The planner is probably just brute force” without examining the actual search and comparison.
For a theoretical objection, construct a counterexample that satisfies all stated assumptions.
For a robustness objection, specify a plausible condition inside the claimed scope.
For a novelty objection, identify the actual overlapping prior mechanism and explain the difference, not merely a similar title.
For a writing objection, explain how the phrasing changes or obscures meaning; stylistic dislike is not enough.

## Challenge and adjudicate objections

Before admitting a major concern to the final report, perform an author-side response using the strongest available evidence.
Search the relevant methods, appendix, figures, code, and definitions for an existing answer.
Check whether a seeming contradiction results from OCR, text extraction, column order, equation rendering, stale versions, or an omitted supplement.
Check whether the objection attacks a stronger claim than the paper makes.
Check whether the requested experiment is needed for the existing contribution or would instead create a different paper.
Check whether a claimed missing baseline is applicable, reproducible, and within the same information/resource setting.
Check whether a limitation is already accurately stated and whether that statement is sufficient for the claimed scope.
Do not accept the author's rebuttal merely because it is confident; compare it to the evidence.

| Adjudication | Required reasoning | Treatment |
|---|---|---|
| Sustained | Evidence supports the concern after counterchecking | Retain with justified severity and remedy |
| Narrowed | Part of the concern survives | Limit the finding to the actual affected claim/setting |
| Rejected | A valid response or inspection defeats it | Record why; remove it from active findings |
| Unverified | Missing evidence prevents a decision | State the specific missing check and conditional impact |

Rejected objections may be retained in an adjudication log, but are not active issues.
Use issue.status confirmed for supported findings, unverified for unresolved evidence questions, and closed only after the defined recheck succeeds.
Do not encode rejected criticisms as confirmed findings merely to preserve reviewer output.
For a confirmed reporting omission, separately state that the underlying procedure remains unknown.
Text-anchor validation proves only that a quote exists at a location; it does not validate an objection's scientific reasoning.
An actual image-view record can support a visual observation; a filename or string match cannot.

## Merge findings and advise the author

Merge objections that share the same cause, affected claim, and remedy.
Keep issues separate when different evidence or fixes are required.
Retain distinct scientific, presentation, and reproducibility consequences even when they arise from one source.
Resolve disagreements by examining assumptions and evidence; a majority vote among role prompts is not a reliability estimate.
If reviewers disagree about value or scope after factual resolution, present the judgment difference transparently.
Use severity from materiality, not the aggressiveness of the reviewer persona.
Do not force a fixed number of critical, major, or minor findings.
Do not estimate acceptance percentages or claim a simulated reviewer predicts real editorial decisions.
If requested, provide a reasoned advisory readiness assessment tied to unresolved conditions and the actual destination.
Keep author-facing comments constructive: identify what is wrong, why it matters, and what would resolve it.
Retain supported strengths in the final assessment, especially where they rebut an initial objection.
Do not weaken a valid theorem, robust result, or clearly bounded contribution solely to sound cautious.
Where new experiments are unrealistic, distinguish a defensible narrowing from an unresolved central validity problem.

## Common false positives

- Mistaking a table's rounded value for an incorrect result.
- Treating a raster photograph or screenshot as inherently unacceptable.
- Calling a missing methodological sentence proof that the procedure was not performed.
- Reading a PDF extraction artifact as a typo in the actual rendered page.
- Rejecting a resource or negative-result paper for lacking a new algorithm.
- Demanding clinical reporting standards from an unrelated ML benchmark.
- Assuming all seeds, test cases, or model-judge votes are independent.
- Treating an unreplicated implementation inspection as a reproduced result.
- Rejecting a supported claim because it uses strong language.
- Treating a citation's existence as confirmation that it supports the attached claim.

The adjudication log should make the review auditable: objection, counterargument, inspected evidence, decision, reason, and surviving issue IDs.
Finish when the material objections have been tested against available evidence, not when every imaginable criticism has been generated.
