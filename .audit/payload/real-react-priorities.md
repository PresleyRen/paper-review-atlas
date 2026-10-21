# ReAct: reviewer-priority exercise / 真实论文审稿重点示例

Input: [ReAct v3, ICLR 2023](https://arxiv.org/pdf/2210.03629v3). Inspection date: 2026-10-21. Printed pages 5–6 were viewed directly: Table 1, Figure 2, Table 2 and the nearby Section 3.3 discussion. Existing table transcriptions were checked against the actual page images. This is a focused excerpt review, not a fresh full-paper review or a model-training reproduction.

## Located evidence and a corrected reviewer objection

Table 1 reports ReAct/CoT as 27.4/29.4 on HotpotQA and 60.9/56.3 on FEVER. The corresponding differences are −2.0 and +4.6 percentage points. Section 3.3 explicitly discusses that mixed result and investigates reasoning/search failure modes. ReAct exceeds Act on both displayed tasks. Thus an objection that the authors concealed the weaker HotpotQA comparison is not supported by the inspected pages. A blanket rejection because one metric is lower is also not a novelty assessment.

| Reviewer question | Decision and repair |
|---|---|
| Must every method win every column? | No. Compare the stated contribution and tradeoff with evidence and closest work; keep the mixed outcome explicit. |
| Is the central comparison understandable? | Identify the comparator, task and metric beside every gain. ReAct-versus-Act and ReAct-versus-CoT support different statements. |
| Does observing mixed performance prove the proposed mechanism? | No. Treat observed effects separately from any mechanism claim; a causal mechanism requires discriminating evidence. |
| Which experiment is necessary? | Only a test that resolves an identified uncertainty in the existing claim; testing unrelated new languages is an extension unless general-language performance was claimed. |

## Original-language writing output

Suggested synthesis of the inspected evidence, not a correction of an alleged original sentence:

> ReAct improves FEVER accuracy by 4.6 percentage points relative to CoT but yields 2.0 points lower exact-match accuracy on HotpotQA. It outperforms Act on both tasks, indicating that the benefit depends on the comparator and setting.

中文对应：相对 CoT，ReAct 的 FEVER 准确率提高4.6个百分点，而 HotpotQA 精确匹配准确率低2.0个百分点；相对 Act，两项任务均有提升。贡献表述应注明任务、比较对象和权衡。

## Explicit mutation probe, not the authors' wording

Synthetic input: “ReAct is universally superior to CoT across all tasks.” The displayed HotpotQA comparison contradicts this injected sentence. Proposed repair: replace it with the task-specific synthesis above. Acceptance: recomputed differences and both comparator/task qualifiers agree. The actual paper's mixed-results discussion is retained as a correct control.

[Execution JSON](real-react-priorities-output.json) records source-file hashes, Decimal computations, CLI priority routing, the non-SOTA policy and the unavailable-video attribution policy. These checks test declared calculations/rules, while the semantic reasoning above was performed by the authoring assistant in this conversation.
