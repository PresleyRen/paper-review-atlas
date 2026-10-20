# Argument, contribution, and novelty review

Use this protocol to examine whether the paper asks a meaningful question, explains a distinct contribution, and connects its conclusions to sufficient evidence.

## Contents

- Reconstruct the argument
- Review first impressions within a declared scope
- Test novelty and positioning
- Audit claims and alternatives
- Link limitations to evidence
- Review structure and article types
- Record findings and remedies

## Reconstruct the argument

Write a neutral summary before criticizing: problem, audience, current limitation, proposed idea, mechanism, evidence, and supported conclusion.
If this summary requires guesswork, identify the missing connection; do not replace the author's actual objective with a more ambitious one.
Separate:

- The practical problem the paper addresses.
- The research question or hypothesis.
- The technical or conceptual contribution.
- The evidence that the contribution works.
- The broader significance, which may remain conditional.

Build a claim map with stable claim IDs.

| Field | What to record |
|---|---|
| Claim | Exact sentence or faithful narrow paraphrase |
| Kind | Descriptive, comparative, causal, theoretical, generalization, efficiency, dataset, or synthesis |
| Scope | Population, tasks, conditions, resources, assumptions, and time/version |
| Evidence | Experiment, table, figure, proof, source, or qualitative observation |
| Support state | Supported, partially supported, contradicted, or unverified |
| Alternative | A plausible competing explanation |
| Repair | Clarification, reanalysis, new evidence, or appropriately bounded wording |

Do not collapse several claims into one “works well” statement. Accuracy, latency, usability, robustness, and novelty need different evidence.
Distinguish a mechanism explanation from a performance observation; an improved score does not by itself establish why it improved.
Distinguish causal claims from associations, predictions, or comparisons under one fixed configuration.
Check the same claim in title, abstract, introduction, results, captions, discussion, and conclusion for scope drift.

## Review first impressions within a declared scope

When first-page or triage feedback is requested, identify the material inspected: title, abstract, introductory contribution statement, principal figures/tables and captions, and conclusion.
View the actual rendered objects before judging their visual communication; record unavailable surfaces.
Check whether the intended reader can recover the problem, contribution, strongest evidence, and tested limits from these materials.
Map substantive title promises and contribution statements to their evidence locations.
Identify a buried contribution, unexplained comparison, or inconsistent scope as a located communication problem and offer a concrete wording or ordering repair.
Do not require the contribution in a particular sentence or prescribe an abstract formula unless the destination does.

Keep the evidence boundary visible: this pass assesses the presentation encountered first and does not establish mathematical correctness, experimental validity, or reproducibility.
Distinguish information absent from the inspected surfaces from information absent from the paper.
Check the relevant methods, appendices, and artifacts before promoting an apparent gap to a scientific finding; otherwise name the unresolved question.
Report the clearest supported improvement without inventing an acceptance probability or a prediction of an editor's decision.

## Test novelty and positioning

First identify the nearest relevant prior approaches, including simple competitors and work using different terminology for the same mechanism.
Search when current or external verification is needed. Record queries, date, included sources, and important access gaps.
Read the relevant method and result context in primary sources; a title, search snippet, or citation count cannot establish equivalence or difference.
Assess novelty along separate axes:

| Axis | Useful comparison |
|---|---|
| Question | Does the paper expose a previously unresolved or differently specified problem? |
| Method | What operation, assumption, representation, or optimization changes? |
| Explanation | Does it establish a mechanism or boundary not already known? |
| Evidence | Does it supply a credible new evaluation or surprising reproducible result? |
| Resource | Does a dataset, benchmark, artifact, or taxonomy enable new work? |
| Synthesis | Does it integrate a field with a transparent and useful organizing principle? |

An incremental method may still be a valuable contribution; the issue is whether the claimed contribution matches its actual increment.
Combining known parts is neither automatically novel nor automatically trivial. Ask whether the combination resolves a documented obstacle and whether that interaction is tested.
Do not demand a new algorithm from a reproducibility study, resource paper, negative-result paper, or well-scoped survey.
“First,” “only,” “state of the art,” and “universal” require especially clear search scope, comparison conditions, and temporal bounds.
If no novelty search was possible, state that novelty is unverified; do not report a confident global originality judgment.
Assess venue fit against current stated scope and contribution expectations when available; do not invent immutable standards for a named venue.

## Audit claims and alternatives

For each central claim, ask:

1. What observation would distinguish this claim from the strongest plausible alternative?
2. Does the existing evaluation make that distinction?
3. Are other variables changed with the proposed mechanism?
4. Does the selected metric reflect the user's or field's actual objective?
5. Are the reported settings representative of the claimed scope?
6. Would the conclusion survive a reasonable change in analysis, operating point, or exclusion rule?

Example: “Memory improves long-horizon planning” may be supported by a higher completion rate, but a larger context window, extra retrieval calls, or additional tokens could explain the gain.
The useful remedy is a matched-budget comparison and a targeted memory ablation, not an unspecified request for more benchmarks.
Example: a negative result on four well-defined tasks may strongly support a limitation in those tasks. Preserve that result while preventing a claim about all agents.
Example: a dataset paper may demonstrate distinct coverage and annotation reliability without showing that every future model benefits.

Treat a missing counterargument as a reasoning gap when it could change interpretation.
Do not require the author to experimentally reject every imaginable alternative; prioritize plausible alternatives tied to the design and central claim.
When theoretical and empirical evidence disagree, inspect their assumptions and scopes before treating one as a refutation of the other.
Use explicit uncertainty: “These results do not distinguish A from B” is more precise than “A is false.”

## Link limitations to evidence

For limitations that materially affect a central conclusion, maintain a compact ledger:

| Claim and stated scope | Validity threat | Completed check and evidence | Residual uncertainty | Supported scope |
|---|---|---|---|---|
| Stable claim ID and relevant conditions | Specific confound, measurement issue, selection effect, or coverage gap | Actual analysis/test and location, or explicitly not tested | What the completed work cannot distinguish or establish | Conclusion justified now and any evidence needed to extend it |

Keep planned checks separate from completed checks; a proposed sensitivity analysis does not mitigate a threat until its result is available.
Explain whether the threat affects the central inference, the precision of an estimate, or transfer beyond the evaluated conditions.
Retain useful bounded conclusions and avoid a generic list of every imaginable risk.
Preserve the chronology of hypotheses and findings: do not rewrite an unexpected or post hoc result as a prior prediction without evidence of that timing.
Distinguish an honest scope limit from a validity problem that the current wording still leaves unresolved.

## Review structure and article types

Check whether each section serves a necessary role in the argument.
The introduction should establish the problem and contribution without promising results the paper cannot support.
Related work should make the relevant differences recoverable; a citation catalog without comparison may hide rather than clarify positioning.
Methods should expose assumptions and implementation choices needed to interpret the evidence.
Results should separate observations from explanation, and discussion should connect those observations back to the research question.
Allow combined Results and Discussion or other discipline-appropriate structures when those roles remain clear.
The conclusion should retain the tested conditions and avoid introducing a new untested central claim.
Do not force a fixed number of abstract sentences, contributions, paragraphs, or section headings unless the destination requires it.

For an authorized substantial reorganization, map each central claim to the reader questions needed to assess it, then to the proposed section order and evidence locations.
Order definitions and assumptions before dependent reasoning, place comparisons where their conditions can be understood, and retain a visible path from research question to result and interpretation.
Distinguish moving existing evidence from adding a missing analysis; an improved outline cannot supply absent support.
Preserve citation-to-claim relationships and cross-references when relocating material, and identify which dependent passages need revision.

Choose the presentation form according to what the reader must understand:

| Communication task | Suitable form and check |
|---|---|
| Compare exact values or conditions | Table with compatible units, grouping, and denominators |
| Inspect trends, distributions, or uncertainty | Plot whose encodings expose the relevant comparison |
| Specify a mathematical relation or assumption | Equation with defined symbols, domain, and intended interpretation |
| Follow a computational procedure | Algorithm or pseudocode with inputs, outputs, control flow, and relevant stopping conditions |
| Understand components, dependencies, or study stages | Structure or workflow diagram with explicit edge meaning and scope |

Use a navigation table linking claims and evaluations to their reported locations when a complex design is otherwise difficult to follow.
Add a figure, equation, algorithm, or table only when it resolves a specific explanatory need; a paper need not contain every form.
Use [figures-tables.md](figures-tables.md) to inspect rendered communication and [formal-theory.md](formal-theory.md) to check formal content.

For surveys and review articles:

- Define scope, inclusion logic, search/selection process appropriate to the claimed review type, and time boundary.
- Distinguish a narrative survey from a systematic review or meta-analysis; assess it against its actual declared method.
- Check whether the taxonomy is consistent, whether omitted major work affects conclusions, and whether comparisons use compatible evidence.
- Treat counts, trends, or pooled effects as empirical claims requiring traceable extraction and appropriate analysis.
- Do not demand PRISMA compliance merely because a paper has a literature-review section.

For dataset and benchmark papers:

- Review the need, target constructs, collection and annotation process, provenance, splits, task definitions, limitations, and maintenance plan.
- Compare the sampling frame, selection and exclusion rules, sources, time period, and relevant subgroup coverage with the population the paper claims to represent. Document undercoverage and selection effects without imposing an unrelated universal balance rule.
- Test whether benchmark scores measure the advertised capability or a proxy vulnerable to shortcuts.
- Assess annotation instructions, uncertainty, agreement where relevant, and how disagreements, ambiguous items, adjudication, and label changes are handled. Preserve substantive disagreement when one consensus label would hide it.
- Inspect dataset and leaderboard versions, evaluation-code changes, hidden-test access, repeated submissions, and score feedback when these can enable test-set adaptation. Check whether results from different versions remain comparable and whether the governance process records corrections and material changes.
- Examine intended and unsupported uses, access conditions, maintenance responsibility, update policy, and applicable correction, withdrawal, or deletion mechanisms. Distinguish a documented process from evidence that it has been exercised.
- Assess contamination and saturation in relation to the claimed measurement. Saturation may be a valid finding about the benchmark's remaining discrimination; it does not automatically invalidate the study or require harder tasks merely to produce a positive contribution.
- Distinguish documentation quality from empirical evidence that a benchmark is useful.

## Record findings and remedies

Use a claim/evidence/gap matrix before drafting criticism; it reduces repeated objections across sections.
Assign materiality according to the conclusion affected, not the prominence of the sentence.
Offer the least disruptive scientifically adequate remedy: cite and explain existing evidence, reanalyze available data, perform a discriminating test, or change scope.
When a wording change suffices, provide an actual replacement preserving the strongest defensible contribution.
When further work is necessary, state the decision it would resolve and an acceptable alternative if resources are limited.
Preserve useful negative results, bounded findings, and clearly labeled hypotheses.
Record both accepted and rejected major objections so subsequent revisions do not recycle a resolved misunderstanding.
