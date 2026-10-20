# Chinese and English scholarly writing

Default to Simplified Chinese explanations and edits in the manuscript's source language. For an English manuscript, supply formal scholarly English replacements; for a Chinese manuscript, supply natural academic Chinese. Follow an explicit user language preference.

## Contents

- Meaning-preservation contract
- Diagnostic sequence
- Chinese and English checks
- Translation and bilingual consistency
- Revision records and verification

## Meaning-preservation contract

Before revising a sentence, identify its proposition and the evidence that supports it.
Preserve these invariants unless the user authorizes a substantive change supported by evidence:

- Numbers, signs, significant information, units, denominators, ranges, and uncertainty.
- Model, dataset, method, variable, organization, and task identities.
- Negation, modality, comparison direction, and quantifiers such as some, all, or only.
- Conditions, assumptions, population, time/version, and operational limits.
- Citation identities, equation/figure/table references, and their relationship to the claim.
- Causal versus associative meaning and observed versus hypothesized status.

Preserving meaning does not require preserving an unsupported overclaim. Separate a scientific correction from a stylistic edit and explain the evidence for it.
Preserve strong language when justified; routinely replacing “demonstrates” with “may suggest” can distort valid evidence.
Do not add new results, superiority claims, mechanisms, citations, or completed experiments to make prose smoother.
Do not remove caveats that define the result's valid scope.
Do not insert generic limitations that obscure a clearly supported contribution.
For audit-only requests, propose changes in the report. For authorized review-and-revise requests, apply relevant edits and record them without repeatedly seeking confirmation.

## Diagnostic sequence

1. Identify the purpose of the paragraph and the claim it must convey.
2. Check consistency with methods, results, and nearby terminology.
3. Repair missing logical links, ambiguous referents, and unexplained concepts.
4. Improve sentence structure and information order.
5. Correct grammar, punctuation, spelling, and local formatting.
6. Recheck all scientific invariants and cross-references.

Do not polish an ambiguous technical claim into a confident but invented interpretation.
When two readings remain plausible, provide alternatives and identify the author decision needed.
Separate a reporting omission from a language defect: an absent split policy needs information, not merely a more elegant sentence.
Check paragraph flow through actual reasoning, not compulsory connector words.
Use section-specific criteria: an abstract needs an accurate problem/contribution/result summary; a method needs reproducible definitions; a discussion needs bounded interpretation.
Avoid fixed sentence counts, paragraph-length limits, mandatory active voice, or bans on first person unless required by the destination.

Check repeated openings, empty transitions, and referents in context rather than treating them as forbidden patterns:

| Pattern | Useful check and possible repair |
|---|---|
| Several sentences start with “This method” | Keep intentional parallelism; if different components perform the actions, name the supported actors, such as “The retriever” and “The reranker.” |
| “Furthermore, the next step is to normalize the scores.” | If the relation is procedural order, “Next, normalize the scores” makes that relation explicit without adding a claim. |
| “模型将结果交给重排器，它筛除重复项。” | Confirm which component removes duplicates; replace “它” with that component's name only after resolving the ambiguity. |

Preserve the author's voice, useful repetition, and field-specific conventions when they aid comprehension.
Judge whether a revision clarifies the reasoning; sentence openings, connector frequency, or cadence do not establish AI authorship.

## Chinese and English checks

| Area | Chinese focus | English focus |
|---|---|---|
| Clarity | 省略主语造成归属不清；“其”“该”指代不明 | Ambiguous pronouns, dangling modifiers, unclear agency |
| Structure | 过长定语、层层套用、同义反复 | Overloaded clauses, buried main verbs, redundant nominalization |
| Logic | “因此”“证明”是否超出实际证据 | Whether therefore, proves, and causal verbs are warranted |
| Terminology | 中文译名、缩写及中英混排一致 | Stable technical names, acronym expansion, singular/plural |
| Tone | 减少空泛评价和宣传语，保留有据结论 | Precise measured claims, restrained promotion, direct explanation |
| Grammar | 搭配、成分残缺、关联词配对 | Articles, tense, agreement, prepositions, countability |
| Quantities | 单位、百分比、范围与统计量含义 | Units, intervals, significant information, metric direction |
| Citations | 引文与具体论断相邻且关系明确 | Clear attribution and accurate scope of cited evidence |

Chinese example:

- Original: “通过引入记忆模块，使得系统能够显著地提升性能。”
- If only a score difference is shown: “引入记忆模块后，系统在数据集 A 上的任务成功率由 80% 提高至 84%。”
- If the numbers are unavailable, do not invent them; use a located comment requesting the actual metric and evidence for “显著”.

English example:

- Original: “Our method significantly improves all tasks.”
- If improvement occurs on 7 of 10 tasks without a significance test: “Our method improves the observed score on 7 of the 10 evaluated tasks.”
- If a valid analysis supports statistical significance on all 10 tasks, retain that strength and specify the metric and tested comparison.

“Significant” and “显著” can imply a statistical claim; clarify whether the meaning is statistical, practical, or descriptive.
Avoid translating an increase of 4 percentage points as “improved by 4%”.
Do not change “less than” to “at most,” “at least” to “greater than,” or a strict inequality to a non-strict one for style.
Do not treat specific vocabulary as proof of AI authorship, plagiarism, or poor scholarship.
Em dashes, passive voice, and long sentences are local readability choices, not automatic major findings.
Respect discipline-specific style when it aids precision, and defer to verified author guidelines where required.

## Translation and bilingual consistency

Translate the meaning and logical force, then check the technical content independently.
Maintain a bilingual glossary for recurring terms and abbreviations.
Preserve proper names and official dataset/model titles unless an established translation is required.
For bilingual titles and abstracts, compare the problem, contribution, experimental scope, quantities, limitations, and conclusion.
Do not allow an English abstract to claim “robust across domains” when the Chinese abstract reports one domain.
Back-check negation, hedging, causal language, comparatives, and quantifiers; these often change unintentionally.
Keep citations and equation/table/figure numbers attached to the same proposition after reordering.
For captions, use terminology consistent with axes, table headers, and main text.
Translate natural academic usage rather than mechanically reproducing Chinese syntax in English or English nominalization in Chinese.
If a source-language sentence is scientifically ambiguous, resolve or annotate the ambiguity before producing a definitive translation.
When asked for both languages, provide paired versions with an explicit note on any substantive correction.
Do not assume English journal conventions, Chinese university thesis rules, GB/T, APA, or IEEE formatting apply without the actual destination and article type.
Check currently applicable institutional or venue rules when a formatting judgment depends on them.

## Revision records and verification

For material edits, record:

| Location | Original | Replacement | Reason | Scientific effect |
|---|---|---|---|---|
| Abstract, sentence 3 | Exact source text | Proposed/applied text | Specific defect repaired | None, scope clarified, or evidence-dependent correction |

For routine repeated typos, a grouped record is acceptable if all affected locations remain recoverable.
Do not overwhelm the author with trivial comments before identifying structural or scientific problems.
Review numerical and semantic invariants after the full paragraph is revised, not only sentence by sentence.
Check that no citation, LaTeX/Typst construct, math delimiter, label, table alignment, or formatting instruction was broken.
For Typst, preserve citation/reference keys such as `@key`, label declarations such as `<label>`, imports, user-defined functions, and formatting constructs unless their change is part of the authorized repair.
Keep bibliography keys stable across `.typ` sources and BibTeX or Hayagriva records; an editorial rewrite must not detach a citation or label from the proposition it identifies.
Render or build when a supported host tool is available and the edit could affect the final layout.
If rendering is unavailable, state that source-level editing was completed and final layout remains unverified.
For a translation, compare both versions against the same evidence rather than trusting a fluent result.
For a substantive scope correction, link the edit to the relevant claim or finding ID.
For a purely editorial change, do not imply the paper's scientific validity improved.
Close a writing finding after checking the revised passage in context and confirming its scientific invariants.

## Source-specific writing diagnostics

When repetition is suspected, count the repeated words, sentence openings or transitions in the inspected span and show locations before recommending deletion. Those counts describe the text, not its author's identity. A rhetorical variation is useful only when it improves the reader's understanding. Retain clear sentences rather than always generating a replacement.

Preserve an explicitly requested author style, section purpose and glossary. For long documents, keep an edited/remaining section ledger and revisit terminology, quantities and references across section boundaries. Source-format edits must protect citation keys, equation labels, custom macros, Typst functions and Hayagriva entries. Compile and render when those tools are available; report separately what text was changed and what build was run.
