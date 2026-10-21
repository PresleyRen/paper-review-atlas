# Reviewer priorities / 审稿关键问题

Use this pass before a full review, during quick triage, or via `priorities`. It connects the central scientific case to the smallest set of changes that would make it assessable. Read review-contract.md first. Use Chinese or English for discussion and preserve the manuscript language in replacements.

## 1. Recover the actual paper before judging it

Create a one-page paper card: problem and affected setting; contribution type; closest prior result; central claim; proposed change; decisive evidence; observed benefit and cost. Trace a concrete input through the method to an output. Each important module should have an operational definition, role and evaluation link. Not every module is itself a contribution.

Use this navigation spine:

```text
Problem / failure condition
  -> scientific contribution (without acronym or promotional name)
  -> operation / variable / testable prediction
  -> comparison that distinguishes the prediction from alternatives
  -> observed effect, uncertainty and cost
  -> supported conclusion and reader-facing explanation
```

For a descriptive dataset, replication, theory or system paper, adapt the spine to the contribution rather than demanding a new causal mechanism. Several contributions are acceptable if their evidence and relationship are clear. Neither module count nor an acronym establishes or disproves novelty. A non-SOTA result may still establish a useful tradeoff, dataset, explanation or failure condition.

## 2. Select the destination's actual criteria

Record the venue, article type, current official policy URL, access date and the relevant criterion. Select an importance-selective, soundness-focused or unknown profile; the profile is not inferred from SCI indexing, quartile, impact factor or a blogger's preference.

Nature's stated interest/significance criteria differ from the soundness-focused criteria of Scientific Reports and PLOS ONE. Technical validity applies in both settings. Keep originality/unpublished work, ethics and reporting obligations even when perceived importance is not a selection criterion. Missing policy means retrieve it, not silently apply Nature's bar.

Separate three judgments in the report: scientific support; contribution relative to located prior work; fit to the verified destination. A venue-fit concern must not be described as a mathematical or experimental error. Registered Reports and protocol papers are reviewed at their actual stage; a planned study is not defective merely because it has no final results yet.

## 3. Check the decisive questions

| Question | Inspect | Deliver |
|---|---|---|
| Why this problem? | Concrete affected cases, relevant population, motivating evidence, prior solutions | Located motivation gap or a concise supported problem statement |
| What is actually new? | Closest work at claim/setting level, contribution type, what survives removal of the method name | Contribution comparison and exactly what remains different |
| Why should the change work? | Failure condition, transformed variable, operational details, prediction | Mechanism/operation map linked to tests |
| Does the experiment distinguish explanations? | Equal information/budgets, controls, simple substitutes, ablations, raw metric implementation | Claim-specific decisive test or reanalysis |
| How trustworthy is the result? | Unit/denominator, pairing, missing runs, uncertainty, leakage, measurement/version lineage | Supported effect and unresolved evidence questions |
| Is the benefit worthwhile? | Absolute gain and task relevance versus calls, tokens, latency, setup, robustness | Matched-budget result or quality-cost tradeoff |
| Can the reader recover the case? | Abstract, central figure/table, caption, method-to-result navigation, precise language | Original-language replacement and linked evidence |

For an Agent/RAG paper, test whether the apparent benefit instead follows from a changed retriever, a stronger backbone, more sampling, extra tool access or a larger token budget. If a paper claims only measured performance, missing mechanism identification is not by itself a blocker. If it claims a mechanism, a score increase alone does not isolate that mechanism. Preserve the measured effect while requiring discriminating evidence or a justified narrower statement.

## 4. Separate reading friction, serious findings and blockers

A first-pass concern is provisional. Revisit the methods, appendix, captions and available artifacts before retaining it. Track `initial observation -> located clarification -> final disposition`. Later clarification can remove a scientific objection while leaving a modest navigation edit.

Add the following fields to a retained issue alongside its stable ID, location, evidence, consequence and fix:

- `decision_dimension`: validity, contribution, venue_fit or presentation.
- `blocking`: true only when an unresolved, evidenced gap prevents establishment of the central case under the applicable criteria; minor/editorial items are not blocking.
- `resolution_question`: the exact uncertainty the fix must resolve.
- `minimum_repair`: reanalysis, focused experiment, operational detail, clarification, or evidence-supported narrowing.
- `sufficient_when`: an observable acceptance condition, including where the updated result must appear.

Do not hardcode an abstract/figure-first rejection, a fixed defect quota, mandatory page-1 figure, required reviewer count, punctuation bans or universal SOTA demand. Substantive language ambiguity can matter; routine grammar is not a proxy for invalid science. A small edit can remove an unsupported major claim, but cannot repair an invalid dataset behind the remaining claim.

## 5. Ask for the smallest sufficient repair

For each requested experiment, state the existing claim, unresolved alternative, controlled variable, appropriate unit, comparator, measure, analysis and decision-changing outcome. Distinguish essential evidence for the current case from optional work that expands scope. Consider existing-data reanalysis first. Where sound evidence supports a narrower contribution, offer that route without erasing supported strengths. Do not require a new research project as the default revision.

Recheck the original closure condition and linked revision. Stop escalating a resolved objection unless new evidence introduces a distinct issue. Give any new issue its own ID and justification.

## 6. Optional blind reports and a separate audit

When the environment can run isolated invocations, freeze a fact-only packet and preassign relevant emphases. Reviewers receive no common suspicion list or other review. Preserve each frozen report before synthesis. The number of roles follows the task and available tools.

Run numerical/figure consistency checks as a separate audit lane. An audit discovery is not reviewer consensus. Convergence means the same concern occurred in at least two eligible frozen reports; do not retroactively edit reports to manufacture diversity or agreement. Record actual contexts/models and input hashes. Isolated prompts do not establish statistically independent model errors. Without isolation, use an honestly labeled single-context multi-perspective review.

## 7. Converting external advice into a rule

`config/reviewer-advice.json` records direct URLs, access depth, adopted ideas and exclusions. A video title, search snippet about an unrelated creator, or inaccessible short link cannot establish what a speaker said. With a usable transcript, store the relevant timestamp and a short faithful excerpt, identify its context, compare it with official policy and existing rules, then add a positive, negative and insufficient-evidence test. Personal style preferences remain optional unless an applicable venue requirement makes them material.

## Deliverable

Return a priority table: issue ID; decision dimension; evidence pointer; blocker status; strongest author-side counterevidence; minimum repair; acceptance condition; dependencies. Keep unresolved source requests in the coverage record. Finish with a practical repair order based on scientific consequence, dependency and effort, not the number of requested experiments.

The executable CFX17–CFX22 rules in `scripts/reviewer_priorities.py` route explicit reviewer-derived facts. They do not read a manuscript, authenticate a policy or decide acceptance. Consult the advice registry for the actual source basis.

Use [the priority-report template](../assets/priority-report.template.md) for the deliverable.
