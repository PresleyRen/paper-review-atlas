# Agent, RAG, multiagent, and knowledge-graph review profiles

Use these profiles when the manuscript's actual contribution concerns an Agent pipeline or related component. Combine applicable profiles; do not force every profile onto every paper.

## Contents

- Select the unit of contribution
- Shared experiment contract
- Six component profiles
- End-to-end integration and field fallback

## Select the unit of contribution

| Contribution | Primary profile | Common linked profile |
|---|---|---|
| Intent detection, task dispatch, abstention | Intention routing | Planning/tools or answer generation |
| Retrieval, grounding, indexing, reranking | Retrieval/RAG | Knowledge graph or answer generation |
| Decomposition, action choice, tool use, memory | Planning/tools/memory | Routing or multiagent |
| Response synthesis, citation, faithfulness | Answer generation | Retrieval/RAG |
| Collaboration, debate, role allocation, coordination | Multiagent | Planning/tools/memory |
| Entity/relation/ontology modeling or graph reasoning | Knowledge graph/ontology | Retrieval/RAG |

Identify whether the contribution is a component, a complete system, a benchmark, a dataset, a theoretical result, or a study of existing systems.
For general dataset or benchmark contributions, start with the resource-paper checks in [argument-novelty.md](argument-novelty.md) and the design and measurement checks in [experiments-statistics.md](experiments-statistics.md).
Apply the component profiles below where the dataset or benchmark also makes a specific Agent, retrieval, coordination, or graph claim.
Judge the claimed mechanism and operating conditions rather than applying a generic LLM checklist.
Record the task unit: query, dialogue, episode, user, environment, graph, document, or another justified unit.
When the paper spans components, map each central claim to the component responsible and the end-to-end outcome it affects.
An end-to-end gain alone does not prove which component caused it.

## Shared experiment contract

For each profile record claims, baselines, ablations, leakage controls, measurement/judgment, cost, and robustness.
Fix or expose backbone/version, tools, knowledge access, prompts, decoding, context, training/adaptation, and token/call budgets.
Use identical permissible information across comparators unless the information change is the experimental factor.
Include failures, timeouts, retries, abstentions, and invalid tool actions in the declared outcome policy.
Separate task correctness from format validity, tool-call syntax, judge preference, and completion.
Preserve repeated-task/run structure in analysis; task count, seed count, and judge-vote count are different quantities.
Record provider/service dates when hosted model or tool behavior may change.
Distinguish implemented behavior, inspected code, recomputed results, and actual rerun evidence.
These profiles are review workflows; they do not provide a built-in benchmark runner or access to unavailable model/tool services.

## 1. Intention routing

- **Claims:** Correctly identify intent, choose a task/tool/agent, reject out-of-scope requests, or reduce routing cost without harming end-to-end success.
- **Baselines:** Appropriate rules, direct model classification, nearest-neighbor/classifier routing, single generalist, or a simple fixed route.
- **Ablations:** Remove intent hierarchy, conversation context, confidence threshold, examples, or learned routing; compare equal downstream resources.
- **Leakage:** Keep paraphrases, users, templates, conversations, and label aliases appropriately separated; do not tune thresholds on the test set.
- **Metrics/judges:** Per-intent precision/recall, confusion, macro/micro choices, rejection/coverage, calibrated decision behavior where claimed, and downstream task success.
- **Cost:** Routing latency/tokens plus misroute recovery and the downstream work actually selected.
- **Robustness:** Ambiguous and multi-intent inputs, rare/unseen intents, paraphrase, context shifts, noisy instructions, and distribution shift.
- **Mechanism check:** A higher classification score may not improve task outcomes; show the route decision's actual contribution when the paper claims system benefit.
- **Closure example:** Report performance and downstream cost at matched coverage, with held-out threshold selection and a visible confusion matrix.

## 2. Retrieval and RAG

- **Claims:** Improve retrieval relevance, answer support, multi-hop coverage, freshness, efficiency, or performance under limited context.
- **Baselines:** Relevant lexical/dense/hybrid retrieval, reranking, direct long-context input, or no-retrieval generation under comparable knowledge and budgets.
- **Ablations:** Chunking, query rewriting, reranker, retrieval depth, context ordering, compression, and each proposed retrieval mechanism.
- **Leakage:** Check whether indexes, examples, caches, query development, synthetic QA, or document versions expose test answers or future information.
- **Metrics/judges:** Retrieval recall/precision/ranking under defined gold relevance; answer correctness; claim-level support and citation attribution; unanswerable cases.
- **Cost:** Index build/update, embedding/storage, retrieval, reranking, context tokens, generation latency, and amortization assumptions.
- **Robustness:** Missing/noisy/conflicting evidence, long documents, multi-hop dependencies, stale knowledge, domain shift, and retrieved instruction attacks when in scope.
- **Mechanism check:** Better answer scores do not by themselves establish better retrieval; better retrieval scores do not guarantee faithful answer use.
- **Closure example:** Compare retrieval and answer outcomes under the same corpus snapshot and context allowance, including a relevant no-retrieval baseline.

## 3. Planning, tools, and memory

- **Claims:** Improve decomposition, sequential decisions, tool choice/arguments, recovery, long-horizon completion, or use of past experience.
- **Baselines:** Direct action, fixed workflow, a simple established planner/tool policy, shorter context or no-memory systems under relevant matched budgets.
- **Ablations:** Planner, verifier, replanning, memory read/write policy, summarization, retrieval of memory, and extra context or calls as separate factors.
- **Leakage:** Separate episodes/users/time, distinguish training traces from test trajectories, and prevent cross-task cached answers unless that setting is explicit.
- **Metrics/judges:** End-to-end success, valid/effective actions, step-level errors, recovery, completion horizon, and observable environment state; syntax alone is insufficient.
- **Cost:** Tool calls, retries, failed episodes, tokens, latency, memory growth, storage/cleanup, and human intervention.
- **Robustness:** Tool failure, partial observability, long horizons, stale/contradictory memory, changed interfaces, interrupted tasks, and budget limits.
- **Mechanism check:** An “agent” label does not establish autonomy or planning; inspect actual policy, state, feedback, termination, and opportunities for intervention.
- **Closure example:** Hold call/context budgets fixed, disable memory without changing unrelated tools, and evaluate both task success and stale-memory failures.

## 4. Answer generation

- **Claims:** Improve correctness, grounded synthesis, completeness, faithful citation, calibrated abstention, or usefulness for a defined audience.
- **Baselines:** Same backbone/prompt budget without the proposed component, strong relevant prompting, or standard grounded generation.
- **Ablations:** Evidence selection, synthesis order, verification pass, uncertainty policy, citation generation, and extra sampling/compute.
- **Leakage:** Keep reference answers, grading rubrics with answer content, evaluation examples, and test-guided prompt selection out of the generation path.
- **Metrics/judges:** Separate correctness, supportedness, coverage, attribution, uncertainty, and style; validate model judges against relevant human evidence when claimed.
- **Cost:** Input/output tokens, revision/verification rounds, judge calls used during inference, and latency through the final answer.
- **Robustness:** Unanswerable, conflicting, underdetermined, adversarially phrased, long-context, multilingual, and out-of-domain questions when relevant.
- **Mechanism check:** A citation's presence or valid URL does not prove that it supports the attached assertion; inspect the cited passage.
- **Closure example:** Report claim-level support and answer correctness separately, with blinded/order-controlled judging and explicit abstention scoring.

## 5. Multiagent systems

- **Claims:** Coordination, specialization, communication, or diverse reasoning improves task outcomes beyond extra computation.
- **Baselines:** A single agent with matched total tokens/calls, repeated self-review, independent sampling plus aggregation, and simple role allocation where relevant.
- **Ablations:** Agent count, role specialization, shared state, communication topology, voting/arbiter, debate rounds, and different-model diversity.
- **Leakage:** Prevent test answers entering shared memory, inter-agent messages, simulated user state, or privileged judge feedback.
- **Metrics/judges:** End-to-end success, coordination failures, disagreement resolution, error propagation, and benefit by task regime.
- **Cost:** Total work across agents, communication tokens, wall-clock critical path, concurrency, retries, and arbitration overhead.
- **Robustness:** Correlated errors, misleading peer messages, failed agents, asymmetric information, communication limits, and scaling beyond the chosen agent count.
- **Mechanism check:** Multiple prompts to one model are multiple roles, not verified independent experts; cross-family diversity is not calibrated independence.
- **Closure example:** Demonstrate the collaboration benefit against a matched-compute single-agent or sampling baseline and report failures from shared incorrect beliefs.

## 6. Knowledge graphs and ontologies

- **Claims:** Improve entity/relation representation, semantic consistency, retrieval, reasoning, explainability, or maintenance through explicit graph/ontology structure.
- **Baselines:** Appropriate flat text/table retrieval, dense/lexical retrieval, graph-free representations, standard graph methods, or rules with the same information.
- **Ablations:** Entity linking, relation extraction, schema/ontology constraints, graph traversal, reasoning rules, graph augmentation, and equivalent extra context.
- **Leakage:** Control train/test entity and relation overlap as the claimed setting requires; inspect held-out triples, reverse relations, derived edges, and future knowledge.
- **Metrics/judges:** Extraction/linking quality, graph validity, entailment/reasoning correctness, query/answer outcomes, and provenance; graph size alone is not quality.
- **Cost:** Graph construction, annotation, extraction/model calls, storage, updates, query traversal, and downstream generation.
- **Robustness:** Missing/spurious edges, ambiguous entities, ontology mismatch, temporal changes, contradictory sources, and unseen entities/relations.
- **Mechanism check:** An answer path is explanatory only if edges are supported and the inference is valid; visual connectivity is not factual proof.
- **Closure example:** Compare against a same-information graph-free baseline and trace decisive graph answers to supported edges and a valid reasoning rule.

## End-to-end integration and field fallback

Map the full path from input and available knowledge through routing, retrieval, planning, tools, memory, coordination, and answer.
Identify where errors first occur, which later stages amplify or repair them, and whether evaluation can attribute the final outcome.
Use an oracle component only as an explicitly labeled diagnostic upper bound; do not present privileged information as a deployable fair baseline.
Evaluate component metrics and end-to-end outcomes together when the paper claims both.
Match tradeoffs at meaningful operating points; more tools, agents, context, or graph edges can increase both quality and cost.
For domain-specific agents, inspect whether the task metric and available information match the actual professional workflow claimed.
Do not infer deployment safety, clinical efficacy, or legal correctness from a general benchmark score.
For another field, first identify its question, design, sampling unit, evidence standard, and destination; reuse only applicable scientific principles.
Route theory to formal-theory.md, human studies to relevant design/reporting checks, surveys to argument-novelty.md, and artifact questions to code-reproducibility.md.
Record unsupported domain expertise or missing evaluation resources as coverage gaps rather than fabricating a specialist sign-off.
Future profiles should add a distinct claim, comparator, attribution test, failure mode, and verification method; avoid duplicating existing labels without new checks.
