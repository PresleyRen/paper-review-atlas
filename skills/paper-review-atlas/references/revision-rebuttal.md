# Revision, re-review, and rebuttal

Use this protocol to turn review findings into verified changes and credible responses.

## Contents

- Establish the authorized work
- Adjudicate external comments
- Plan and execute revisions
- Re-review and close findings
- Draft a rebuttal
- Prepare a cover letter
- Final package and handoff

## Establish the authorized work

Determine whether the user requests an audit, proposed edits, applied edits, re-review, or a response to external reviewers.
An audit alone does not authorize rewriting the manuscript.
A request to review and revise authorizes the relevant edits; do not ask for repeated confirmation of routine changes already covered by that request.
Preserve the reviewed version through a copy, revision history, or versioned diff.
Identify the manuscript/supplement/artifact versions to which the findings apply.
If reviewer comments refer to an older version, compare against both the reviewed and current text before proposing further changes.
Treat external reviewer comments as claims to assess, not automatically correct instructions.
Separate scientific repairs, explanatory repairs, editorial changes, and new work that would extend the paper.

## Adjudicate external comments

Compare each comment with the manuscript version it addresses, the actual rendered artifact when appearance matters, and any recorded author decision.
Check whether an alleged defect comes from extraction, a stale version, an overlooked explanation, or a deliberate choice about scope, terminology, contribution order, or voice.
A documented choice can explain a passage, but it does not override evidence of a scientific or communication problem.
Do not reopen a justified decision solely because another reviewer prefers a different style; record what new evidence would warrant reconsidering it.
Distinguish a material scientific concern, a fixable presentation problem, a misunderstanding, and a concern awaiting evidence in the adjudication notes.
Retain the original comment, relevant decision and evidence, disposition, reason, and any surviving finding IDs.
Use the existing finding statuses for active issues; retain rejected comments in the adjudication record rather than creating another machine lifecycle.
Repeated agreement among external models is a reason to investigate a concern, not independent verification of it.

## Plan and execute revisions

Build a revision plan ordered by dependency and effect on conclusions.

| Finding | Current evidence | Required action | Dependency | Deliverable | Acceptance check |
|---|---|---|---|---|---|
| PRA-004 | Task means treated as independent runs | Reanalyze at the justified unit | Raw run/task data | Analysis + revised Table 3 | Code/output/text agree and inference is justified |

Resolve central validity questions before polishing claims that may change.
Prefer the smallest scientifically adequate repair; avoid rewriting unrelated sections.
Possible repairs include locating existing evidence, clarifying reporting, correcting analysis, adding a discriminating experiment, modifying the method, or narrowing an unsupported claim.
A new experiment is not automatically superior to an adequate reanalysis or a precise explanation.
Do not silently replace an intended contribution with a different one.
When a substantive choice remains ambiguous, complete independent useful work and identify the specific author decision needed.
For planned experiments, document the hypothesis, comparison, variables, metric, independent unit, analysis, resource needs, and stopping rule before interpreting results.
Do not present a proposed experiment or anticipated improvement as a completed result.
Keep unsuccessful, negative, and mixed results visible under the declared reporting policy.

For each material edit, retain the original text, replacement, reason, affected claim/finding, and evidence impact.
Distinguish:

- Editorial revision: meaning unchanged.
- Clarification: existing meaning made explicit.
- Scientific correction: claim, method, analysis, or interpretation changed because of evidence.
- New evidence: an actual additional analysis or experiment.

Update all dependent locations: abstract, contribution list, main text, tables/figures, captions, supplements, conclusion, and response letter.
When a number changes, trace it from source data through every displayed occurrence.
When a method changes, identify which old results no longer describe the revised method.
When an assumption changes, revisit theorem statements, experiments, limitations, and practical claims relying on it.
Do not allow a polished abstract to retain a claim removed from the results.

## Re-review and close findings

Retain stable finding IDs. New independent problems receive new IDs; do not renumber the history.
For every previous finding, inspect the current evidence and perform the stated acceptance check.
Use the machine statuses confirmed, unverified, and closed consistently.

| Situation | Status and explanation |
|---|---|
| The defect remains supported | confirmed; describe the remaining issue |
| The author states a fix but evidence/checks are missing | unverified; identify the missing verification |
| The repair passes the actual acceptance check | closed; attach the inspected evidence and check result |
| The original criticism was mistaken | Remove from active issues and record the adjudication/retraction |

A closed finding requires more than a changed sentence or a “done” response.
For an analysis issue, inspect the corrected procedure and relevant output, not just the response letter.
For a visual issue, view the revised rendered figure or page.
For a citation-support issue, check the revised claim against the actual source.
For a writing issue, check the passage in context and confirm scientific invariants.
For a code bug, distinguish the repaired implementation from the still-unrerun experiment.
Check whether a fix introduces a new inconsistency or moves the same problem to another section.
Do not reopen a correctly closed issue merely to maintain a certain number of criticisms.
Limit additional tests to concrete remaining risks or required gates.

## Draft a rebuttal

Read the actual response instructions, word limits, anonymity rules, and deadlines when they matter.
Group related comments while preserving a clear mapping to each reviewer point.
Under a strict word budget, address concerns that can change the scientific assessment before local editorial preferences.
Give the decisive evidence and its scope enough space; a promise to clarify cannot answer a request for missing evidence.
For a journal revision, retain reviewer-by-reviewer coverage and a recoverable change record even when several comments share one repair.
Use a respectful, direct structure:

1. Restate the specific concern faithfully.
2. State agreement, partial agreement, or reasoned disagreement.
3. Present the relevant evidence or completed change.
4. Give the exact current manuscript/artifact location.
5. Acknowledge any remaining limit without promising unsupported future results.

Use “we have added” only when the change exists in the current version.
Use “we will” only for an explicit plan, clearly distinct from completed work and appropriate to the response process.
Do not invent new data, statistical significance, experiments, ethics approval, or a citation to answer a reviewer.
If the reviewer misunderstood an existing passage, explain the evidence and improve the passage when the misunderstanding reveals a real clarity problem.
If the reviewer requests an out-of-scope extension, explain the paper's actual scope and why the existing evidence supports it.
If the reviewer identifies a valid central flaw, acknowledge its effect and offer an adequate repair; polite phrasing cannot substitute for evidence.
If the objection is wrong, disagree using the relevant assumptions, data, definitions, or source rather than a personal judgment.
Preserve strong justified results; do not concede unsupported criticisms simply to sound cooperative.
Avoid excessive apology, defensive rhetoric, or claiming the reviewers are unanimous when they are not.

Example response pattern:
“We agree that the original table did not separate the effect of memory from the larger call budget. We added a matched-budget comparison in Table 4 using the same held-out tasks and call limit. The revised result supports the memory benefit under that budget; we narrowed the abstract's claim to those evaluated settings.”
Use this pattern only when each stated action and result is real.

## Prepare a cover letter

Use the actual target venue and article type. State the concrete problem, contribution,
main evidence and fit in a short original letter. Do not copy the abstract wholesale.
Include author/contact details only when supplied or explicitly authorized; mark missing details.
Verify any required exclusivity, prior-publication, competing-interest, ethics, data/code
availability and suggested-reviewer declarations against author-provided facts and current
venue instructions. Never invent an ethics approval, unanimous author consent or absence of conflicts.
A transfer, revised submission or related manuscript needs an accurate relationship statement.
Keep promotional language within the demonstrated claim scope; no guarantee of acceptance.
Check every substantive sentence about novelty, superiority, quantitative results, or applicability against a located manuscript claim and its evidence.
For each such sentence, retain the letter location, manuscript location, support assessment, and any required narrowing or missing author fact.
Compare numbers, comparison conditions, author/article identity, related submissions, and required disclosures across the letter and manuscript.
Where AI-use disclosure is required, verify its content and placement against current official instructions and the actual assistance used; do not infer disclosure facts from writing style.
Recheck the alignment after polishing. Fluent wording must not introduce a new result, stronger priority claim, or unsupported declaration.
Deliver an editable draft for the authorized submission workflow. Drafting is not sending.

## Final package and handoff

Deliver the revised artifact when authorized, a concise change summary, the stable-ID findings ledger, and verification evidence.
For rebuttals, include a comment-to-response-to-change mapping so the author can audit every assertion.
List unresolved central issues and the exact evidence needed to resolve them.
Separate submission readiness from a prediction of acceptance.
When relevant host tools exist, compile/render the final source and inspect the revised pages, references, figures, and tables.
If a tool or input is missing, state the incomplete check and avoid a blanket “fully verified” claim.
Drafting a response or preparing files does not itself authorize sending them to reviewers or submitting a manuscript.
Continue with publication or external communication only when that action is authorized by the user's request.
