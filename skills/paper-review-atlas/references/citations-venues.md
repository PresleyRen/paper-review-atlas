# Citations, venue requirements, and domain obligations

Use this protocol for literature verification, attribution, submission requirements, and reporting obligations. Treat each as a separate evidence question.

## Contents

- Citation identity and claim support
- Local bibliography retrieval and export
- Literature positioning
- Current venue requirements
- Ethics and reporting by relevance
- Privacy, security, and release scope
- Findings and verification records

## Citation identity and claim support

Perform two distinct checks for each important citation.

| Check | Question | Adequate evidence |
|---|---|---|
| Identity | Does the referenced work exist and match the metadata? | Publisher/repository record, DOI resolution, official bibliographic data |
| Support | Does the work support this particular proposition? | The relevant inspected passage, method, result, or limitation |

A valid DOI does not establish claim support.
A title match or search snippet does not establish that the entire paper was read.
Record author/title/year/venue/identifier/version mismatches separately from misattributed scientific claims.
Compare preprint and published versions when their differences matter to the cited statement.
Check whether a correction, retraction, superseding version, or changed dataset/model affects the reference; verify current status through appropriate sources.
Do not assume a preprint is invalid evidence merely because it is not peer reviewed; describe its status when relevant.
For pivotal claims, inspect the primary source when accessible.
If only an abstract is available, limit the support assessment to what the abstract actually establishes.
If only a secondary source is available, identify the chain and its limitation.
Do not fabricate missing bibliographic details, page numbers, quotations, identifiers, or confirmation of inaccessible material.

Build a citation-support ledger.

| Manuscript claim | Citation | Identity status | Support status | Inspected evidence | Action |
|---|---|---|---|---|---|
| “Method X is robust to domain shift” | Work A | Verified | Partial | Only two specified shifts tested | Bound the claim or add relevant evidence |

Distinguish direct support, partial support, contextual relevance, contradiction, and unverified support.
Check whether a citation supports the preceding clause, an entire compound sentence, or only one component.
Do not let a long citation list imply consensus without examining relevant differences and limitations.
Keep the author's own result distinct from a result attributed to another work.
Check references mentioned in text but missing from the bibliography, uncited entries where disallowed, duplicate records, and broken cross-references.
Metadata scripts can help locate inconsistencies; they do not establish substantive relevance or novelty.
Verify a newly introduced citation when adding it, then include it in the final bibliography audit; do not postpone unresolved identity or support checks until the prose looks complete.
Preserve existing citation keys unless a key change is necessary and every affected reference can be updated and checked.
Distinguish the manuscript's rendered reference list from a shared bibliography collection. An unused entry in a shared `.bib` file is not a defect and must not be deleted automatically.

## Local bibliography retrieval and export

When searching a supplied bibliography, record the file/version and interpreted topic, author, date, venue, identifier, and field filters.
Preserve explicit exclusions and state any inferred filter; do not silently broaden an empty search.
Return original citation keys, relevant metadata, and the fields that explain each match.
Treat matches in titles, abstracts, keywords, or annotations as retrieval evidence; lexical similarity does not establish support for a manuscript claim.
Apply the identity and support checks above before inserting a candidate as a verified citation.
If a parser skips malformed or unsupported entries, report the incomplete search rather than asserting that no relevant reference exists.
Offer a specific filter relaxation when no matches remain.

For exact selected-entry export, preserve the original entry text, key, field contents, and special-character syntax.
Separate a faithful export from a requested metadata cleanup or format conversion, and report any normalization that the latter requires.
Generate LaTeX or Typst citation snippets from the selected original keys; check them against the manuscript's citation conventions.
Do not overwrite the source bibliography or remove entries used by another manuscript as a side effect of search or export.
Use available host tooling and state its limits; this protocol does not imply a bundled universal BibTeX parser.

## Literature positioning

Identify the closest alternatives by problem, mechanism, assumptions, data, and evaluation conditions.
Search different names for the same idea, foundational work, and recent directly relevant results.
Prefer primary and authoritative sources for technical claims.
Record the date and scope of searches when claims depend on current literature.
Do not make a global “no prior work exists” claim from a few queries.
When suggesting citations, explain the exact comparison or claim they improve.
Do not pad the bibliography, insert vendor promotion, or cite a source solely because a skill or template recommends it.
Do not replace careful comparison with citation-count, venue-prestige, or author-reputation arguments.
Avoid demanding a citation for the author's own clearly labeled finding or ordinary connective prose.
For an unfamiliar claim that matters to the review, verify externally or mark the concern unverified.
If a recommended source cannot be inspected, offer it as a candidate for checking rather than a confirmed correction.

## Current venue requirements

Identify the actual venue, track, article type, submission round, and current official author instructions.
If the destination is unknown, review general clarity and completeness; do not enforce invented journal rules.
Separate mandatory requirements from reviewer preferences and optional improvements.
Check as applicable:

- Scope, article type, length/page rules, and what is included in the limit.
- Template/version, font/margin/column rules, anonymity, and permitted supplementary material.
- Abstract structure, title, keywords, references, figures, tables, and accessibility.
- Data/code/material availability statements, disclosures, authorship/contribution statements, and funding.
- Ethics/consent statements, registration/reporting requirements, or statistical reporting when relevant.
- File formats, build requirements, embedded fonts, figure exports, and submission metadata.

Verify changing requirements from current official sources rather than memory or an old skill.
Do not assert universal reading orders or automatic rejection triggers unless the destination explicitly states them.
A format violation may affect submission eligibility; distinguish that from scientific validity.
An editorial formatting preference does not become a major scientific finding because a template uses it.
For blind review, inspect the actual anonymous artifact for visible names, acknowledgments, links, metadata, and self-identifying prose under the venue's rules.
Do not remove attribution from public code or alter authorship without authorization.
Check the final compiled PDF or exported document after formatting changes.

When the user asks to choose among venues, compare actual candidates against current official scope and author instructions.
Use the following dimensions for each candidate, keeping evidence and unknowns visible:

| Dimension | Comparison to record |
|---|---|
| Official scope | Venue, track/article type, current source/date, intended audience, and eligible subject matter |
| Contribution | How the paper's actual contribution matches the stated expectations |
| Evidence | Which supplied results, analyses, or resources establish the relevant contribution |
| Gap | Missing evidence, scope conflicts, or submission requirements that remain unresolved |
| Adaptation | Specific changes needed to framing, evaluation, length, format, or materials |

Distinguish adapting presentation from conducting additional research or changing the contribution.
Recommend candidates with reasons and material uncertainties; do not convert fit judgments, prestige, or historical acceptance rates into a prediction for this paper.

## Ethics and reporting by relevance

Choose checks based on the actual research design and material.

| Research context | Potentially relevant checks |
|---|---|
| Agent/ML benchmark | Dataset rights/provenance, privacy, contamination, model/tool access, release implications |
| Human ratings/user study | Recruitment, consent, privacy, compensation, allocation, rating procedures, applicable approval |
| Clinical trial | Current trial registration and applicable clinical reporting standards |
| Observational health study | Appropriate design-specific reporting and privacy/ethics requirements |
| Systematic review/meta-analysis | Search, selection, extraction, synthesis, and relevant reporting guidance |
| Security research | Threat model, authorization, disclosure, exploit/release implications |
| Dataset/resource paper | Collection rights, sensitive attributes, documentation, access/maintenance constraints |

These examples are routing hints, not a claim that a particular legal or institutional obligation applies.
Verify domain-specific requirements when they affect an actual recommendation.
Do not apply CONSORT, clinical intention-to-treat analysis, or a medical evidence grading scheme to an ordinary Agent benchmark.
Do not infer lack of approval from the absence of a statement; identify missing reporting and request appropriate evidence when applicable.
Keep limitations proportionate to the study and central claims.
A generic “ethical risks” paragraph cannot repair a concrete privacy exposure, and an unrelated hypothetical risk should not dominate the review.
Distinguish ethical/reporting questions from legal advice; do not assert legal compliance from a manuscript review.

## Privacy, security, and release scope

For relevant claims, identify the protected assets, potential attackers or unintended users, their access and capabilities, and the system's trust assumptions.
Compare the evaluated attacks and defenses with that stated threat model; a test under one access condition does not establish security under every condition.
Keep demonstrations of a weakness distinct from speculation about untested attacks, and relate any requested test to a material claim.

Trace sensitive data through collection, storage, access, transformation, retention, withdrawal or removal, and release.
Inspect what is collected, why it is needed, who can access it, and what documented controls or procedures support the manuscript's statements.
Check direct identifiers, indirect identifying combinations, free text, images, logs, and linked records when present.
Describe the actual de-identification procedure and remaining re-identification risks; removal of names alone does not justify a blanket anonymity claim.
Verify relevant consent, agreements, and provenance without inferring their absence from missing prose.
Distinguish permission to access or use data, code, models, and other materials from permission to redistribute them; a public download link does not by itself establish redistribution rights.

Assess the proposed release against both the concrete risks and the evidence needed to reproduce the paper's claims.
Where relevant, compare full release, controlled access, a restricted subset, aggregate results, or synthetic examples, explaining which checks each option enables and which remain unavailable.
Do not treat a substitute dataset as equivalent evidence without justification, or demand unrestricted release when a proportionate access route can support the necessary checks.
Record residual risks, access conditions, removal procedures, and reproducibility limits instead of asserting universal safety or compliance.

## Findings and verification records

For each material citation issue, record the manuscript quote, source identity, exact inspected support, mismatch, and replacement or narrowing needed.
For each venue requirement, record the official source, access date, requirement, artifact location, and pass/gap/unverified result.
Label a current source that could not be accessed as unverified; do not silently rely on an outdated page.
Suggest precise edits rather than merely “add references” or “follow the journal style.”
After edits, rebuild bibliography/cross-references where tools permit and inspect the rendered output.
Close citation-support findings only after the revised claim and its actual supporting source agree.
Close a submission check only against the requested version and destination; a later template change may require rechecking.

## Local bibliography handoff

`bib-audit` can locate entries by a text query, preserve their original BibTeX and report duplicate or undefined citation keys. An uncited entry in a shared bibliography is informational, not an error requiring deletion. Match source identity first; then inspect the relevant claim in the full text. Local key validation does not perform that online/content check. Preserve correction, retraction and version observations with dates when actually checked.

## Explicit target and response channels

Load `guided-calibration.md` when criteria are supplied or rating behavior is being evaluated. Keep criterion IDs and versions stable across specialist perspectives. Do not merge incompatible venue criteria into a universal checklist. A cover letter should map every scientific assertion back to the paper and clearly distinguish author declarations that still require confirmation from observed manuscript content.
