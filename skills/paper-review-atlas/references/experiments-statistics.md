# Experimental design and statistical evidence

Use this protocol for empirical claims. Adapt the design logic to the field; a clinical-trial checklist is not a default requirement for an Agent or retrieval benchmark.

## Contents

- Claim-to-experiment design
- Comparators, ablations, and leakage
- Measurement and inference
- Results, claim support, and decisions
- Human and model judgments
- Cost, robustness, and repair priorities

## Claim-to-experiment design

Create one row per central empirical claim.

| Claim | Estimand or target | Independent unit | Comparator | Data/setting | Metric | Analysis | Decision |
|---|---|---|---|---|---|---|---|
| Memory improves completion | Mean task-level change under a fixed budget | Task, with repeated runs modeled | Same agent without memory | Held-out long tasks | Success and cost | Paired/hierarchical as justified | Supports, limits, or fails to distinguish |

Define what is being estimated before interpreting significance.
Identify the observational/experimental unit, repeated measurements, clustering, pairing, and selection process.
Count independent replications separately from test examples, folds, judge votes, and repeated decoding on the same run.
Check whether the data and protocol represent the population and conditions named in the claim.
A pilot can demonstrate feasibility; sample size alone does not authorize a broad reliability or superiority claim.
If power or precision is discussed, check its assumed effect, variability, design, and whether it was planned or retrospective.
Do not invent a required sample size without a design-specific rationale.

For experiments spanning multiple datasets, regimes, or analysis stages, provide navigation from each claim to its exact supporting result.
Reuse claim and experiment identifiers across the manuscript, supplements, and analysis artifacts.

| Navigation field | Record |
|---|---|
| Claim | Exact proposition and estimand or target |
| Setting | Dataset/version, population, operating conditions, and relevant configuration |
| Independent unit and n | Unit being replicated, eligible and analyzed counts, exclusions, and nested/repeated observations |
| Comparison | Comparator, pairing or allocation, and conditions held fixed or intentionally changed |
| Endpoint | Outcome definition, units, direction, aggregation, and primary/exploratory status where applicable |
| Analysis | Estimator, uncertainty procedure, test or qualitative method, and analysis artifact when available |
| Result location | Exact table row/column, figure panel, appendix result, or output file and record; include its version |

Keep unavailable counts or result locations explicit instead of filling them from assumptions.
Before proposing or running an experiment, specify how favorable, unfavorable, and inconclusive outcomes would change the claim or next action.

| Possible outcome | Decision to define in advance |
|---|---|
| Favorable | Which claim would gain support, under what effect size, uncertainty, cost, or operating conditions? |
| Unfavorable | Which claim would be narrowed or rejected, or which mechanism/design would be revised? |
| Inconclusive | Would additional precision, a different measurement, or a distinguishing comparison resolve the uncertainty? |

Use design-specific criteria when justified; do not invent universal thresholds or require every study to make a binary decision.
For completed experiments, distinguish documented advance decisions from a reviewer's later reconstruction; do not imply preregistration that did not occur.

## Comparators, ablations, and leakage

Include relevant simple, standard, and strong comparators where they answer the research question.
Check whether a recently published competitor is necessary for the claimed frontier; availability, scope, and reproducibility may justify exclusions.
Record comparison conditions rather than asserting “fair” globally.

| Fairness dimension | Check |
|---|---|
| Data | Same permissible information, splits, labels, preprocessing, and filtering |
| Model | Backbone/version, parameters, training/adaptation, context window |
| Search | Tuning effort, trial count, validation access, stopping and selection rules |
| Inference | Prompts, tool access, decoding, token/call budget, retries |
| Systems | Hardware, precision, batching, concurrency, cache, warm-up, I/O |
| Reporting | Same metric, aggregation, exclusions, and uncertainty convention |

Differences can be intentional experimental factors. Expose them and limit what the comparison identifies.
Ablate the proposed mechanism and plausible confounders, not arbitrary components solely to fill a table.
Check interactions when the contribution concerns a combination; removing one part at a time may miss synergy or compensation.
Use matched-budget and simple-substitute ablations when extra computation, context, or supervision could explain the result.
An ablation that breaks the interface or disables essential infrastructure may test system damage rather than the intended mechanism.

Trace the split unit and time boundary through preprocessing, augmentation, retrieval indexes, caches, prompt development, tuning, and evaluation.
Look for duplicate or related entities across partitions, shared answers in retrieval material, future information, test-driven model selection, and benchmark contamination.
Differentiate demonstrated leakage from unresolved contamination risk.
A pretrained model's exposure cannot be inferred solely from high benchmark accuracy; request provenance, controlled tests, or an appropriately qualified limitation.
Report train/validation/test counts and exclusions at the relevant unit, with reasons.

## Measurement and inference

Check metric definitions, direction, units, denominator, class weighting, averaging, and missing-result handling.
Confirm that a percentage change, a percentage-point change, and a fraction are not conflated.
For a rate rising from 0.80 to 0.84, the change is 4 percentage points or 5% relative, not 4% relative.
Inspect whether “best” means best seed, checkpoint, task, or hyperparameter and whether selection used held-out information.
Check that mean, median, maximum, macro average, and pooled/micro average are labeled accurately.
Review floor/ceiling effects, saturation, imbalance, censoring/timeouts, ties, and metric gaming.

When raw data are supplied, recompute only analyses supported by the documented schema and design.
Check distributions and dependence before choosing a test; do not automatically run a t-test on every table.
For paired tasks/runs, preserve pairing in comparisons and resampling.
For nested users, tasks, sites, models, or seeds, account for clustering or explain the inferential limit.
Report effect size and an uncertainty interval appropriate to the design, alongside a test where justified.
Distinguish standard deviation, standard error, confidence interval, credible interval, quantiles, and min–max.
Bootstrap resampling must use the relevant independent unit; repeated correlated rows do not create new evidence.
Multiplicity arises from many hypotheses, outcomes, comparisons, subgroups, or analysis choices; assess adjustment or exploratory labeling in context.
Do not impose a blanket correction across unrelated predeclared analyses without examining the inferential family.
Check test assumptions, one/two-sided choice, thresholds, exclusions, and whether analysis choices were data-dependent.
“Not significant” is not evidence of equivalence; equivalence and noninferiority need a justified margin and appropriate design.
A narrow interval for one dataset does not establish generalization to a different task distribution.
Bayesian results require stated priors, likelihood, convergence/diagnostics when relevant, and interpretation within that model.
Do not turn a p-value into the probability that a hypothesis is true, or convert it into venue acceptance odds.

## Results, claim support, and decisions

After analysis, connect each observed result to the strongest wording its design and evidence permit.

| Record | Required distinction |
|---|---|
| Intended claim | What the experiment was meant to establish |
| Observed result | Located estimate or qualitative observation, uncertainty, setting, and actual analysis performed |
| Permitted statement | Wording supported by that result and design, including relevant conditions |
| Unsupported extension | Generalization, mechanism, causal conclusion, or comparison the evidence does not establish |
| Alternative explanation | Plausible remaining explanation and evidence that would distinguish it |
| Next decision | Retain or revise the claim, reanalyze, collect targeted evidence, or stop with a bounded conclusion |

Assess these three questions separately for each material result:

| Question | Evidence needed |
|---|---|
| Is evidence available? | Identify the supplied and actually inspected manuscript, data, code, and output records, plus access gaps |
| Is the number correct? | Check the specified values, units, transformations, aggregation, and rounding against the relevant records |
| Does it support the scientific claim? | Evaluate the design, independent unit, comparison, uncertainty, alternatives, and claimed scope |

An available output does not establish that its calculation was checked; a correct calculation does not establish a valid causal or generalization claim.
Record the inspected basis and remaining uncertainty for each question, including when only the manuscript value could be read.
If tables, plots, notebooks, or run summaries conflict, retain the conflicting artifacts and their exact locations while checking versions, filters, units, aggregation, and rounding.
Keep the affected scientific result unverified until the discrepancy is resolved; do not erase a conflicting output or select the more favorable value to make the analysis agree.
A directly observed discrepancy can be a confirmed finding while the correct underlying result remains unverified.

## Human and model judgments

For human evaluation, inspect recruitment/sampling, task instructions, allocation, blinding where feasible, rating scale, adjudication, compensation/consent where applicable, and quality checks.
Identify whether participants experience one condition or several; check sequence, learning, fatigue, and carryover effects when they can change the comparison.
Inspect randomization or counterbalancing, participant training, and spacing or washout between conditions as the study design requires.
Reconcile recruitment, enrollment, completion, exclusions, and analyzed counts; inspect attrition, attention-check rules, missing responses, and condition-specific losses.
Check that scale endpoints and task instructions make the measured construct recoverable, and that the participants and tasks support the stated population and use setting.
For qualitative studies, inspect the coding framework, coder roles, revisions, disagreement handling, and traceable examples supporting each theme.
Assess how contrary or ambiguous observations were handled; a small selection of agreeable quotations does not establish that a theme represents the material.
Choose agreement/reliability measures appropriate to the rating scale and design; no single coefficient is universally required.
Distinguish preference, perceived usability, or perceived fluency from demonstrated correctness and task performance.

For LLM judges, record model/version/date, rubric, prompt, decoding, input order, candidate identity visibility, repetitions, and tie handling.
Test position/order, verbosity/style, self-preference, reference-answer contamination, and prompt sensitivity where they can change the conclusion.
Calibrate judge scores against a relevant human-rated subset or explain why the claim remains limited to automated preference.
Do not treat many votes from one model and prompt as independent human opinions.
Separate answer correctness, grounding, helpfulness, safety, and style; one scalar may hide incompatible tradeoffs.
If agreement is weak, inspect disagreement patterns rather than averaging away the uncertainty.

## Cost, robustness, and repair priorities

Record end-to-end cost: tokens, calls, latency distribution, failures/retries, compute, memory, index construction, training/adaptation, and human labor when material.
For latency, specify measurement boundary, warm/cold state, concurrency, hardware, sample count, and distribution or quantiles relevant to use.
Separate throughput from latency and online costs from amortized setup; report the amortization assumption.
Pair relative speedups with absolute time or resource measurements, and inspect results by workload before accepting an aggregate that may conceal substantial regressions.
Check whether batching or queueing used to improve throughput preserves the latency conditions claimed for the system.
Inspect measurement instrumentation, counter polling, sampling frequency, and monitoring overhead when they can perturb the workload or dominate the reported effect.
For energy claims, distinguish observed energy from estimates derived from power and duration; record measurement scope, units, integration or estimation method, and relevant assumptions.
Check whether background activity, shared hardware, or cloud co-tenancy could materially change the comparison; inspect controls and repeated measurements appropriate to that uncertainty.
Choose environment controls and estimators for the measurement question; do not require a particular machine arrangement, timing summary, or energy instrument for every study.
Distinguish algorithmic improvement from engineering, hardware, caching, and additional resources.
Use quality–cost curves or matched operating points when one method trades more compute for higher quality.
Evaluate robustness to plausible changes: data shift, task difficulty, prompt paraphrase, seeds, missing tools, noisy retrieval, longer horizons, or altered budgets.
Do not demand every stress test; select those implied by the paper's claims and deployment assumptions.
Record failure categories and worst-relevant regimes as well as averages.
For negative or mixed results, check whether the interpretation fairly represents the distribution of outcomes.

Classify suggested work as required to support an existing claim, useful to distinguish mechanisms, or optional to extend scope.
Prefer reanalysis of existing valid data when it can resolve the issue; new experiments should answer a specific unresolved question.
Supply an experiment card: claim, hypothesis, controlled variables, independent unit, comparator, metric, analysis, estimated resources, and closure criterion.
If data or compute are unavailable, propose an honest scope change without automatically erasing a well-supported contribution.
Mark whether each result was read from the manuscript, recomputed from supplied data, or actually reproduced by execution.
