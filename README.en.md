# Paper Review Atlas

**Locate research-paper weaknesses, produce actionable revisions, and verify the fixes—in Chinese and English.**

Atlas reviews arguments, experiments, statistics, code/results, figures, tables, references and writing. Authors receive traceable findings, proposed replacements, experiment plans and a revision ledger. The AI track covers LLMs, agents, RAG and knowledge graphs.

[中文](README.md) · [Source features](docs/FEATURE_MATRIX.md) · [Real-paper example](docs/validation/real-react-review.md) · [Tests](docs/validation/v1.1-audit.md) · [Extension index](docs/EXTENSION_INDEX.md)

## What you get

| Task | Deliverable |
|---|---|
| Strict pre-submission review | Located evidence, impact, severity, remedy and acceptance check |
| Experiments and statistics | Claim-to-experiment matrix, fairness/leakage checks and targeted repair plan |
| Figures and tables | Scientific interpretation, rendered inspection, numerical reconciliation and replacement captions |
| Bilingual editing | Original/replacement/reason with consistent terminology and scientific meaning |
| Revision and rebuttal | Stable issue IDs, changes, rechecks and point-by-point responses |
| Extension | Capability, feature and gap IDs resolving to files, tests and repair routes |

## Install and invoke

```bash
git clone https://github.com/PresleyRen/paper-review-atlas.git
cd paper-review-atlas
python scripts/install_skill.py --project /absolute/path/to/your-paper-project
```

Python 3.10+; local helpers use the standard library. The host model performs semantic review. Installation places the skill in `.agents/skills/paper-review-atlas/`. Reload skill discovery in a compatible host, then invoke:

```text
Use $paper-review-atlas in full mode to review this manuscript.
Check claims, experiments, statistics, code/results, every figure/table,
references and language. Report in English; keep Chinese replacements
in Chinese. Give a location, evidence, consequence, remedy and acceptance
check for every retained finding.
```

Provide the manuscript and available supplements, figures, tables, CSV/JSON outputs, configurations and code. PDF, Word, LaTeX and Typst routes use the host's extraction, rendering, compilation and editing tools.

## Complete text map

```text
Paper Review Atlas
├── Evidence and traceability
│   ├── C01 Intake and provenance
│   ├── C04 Claim–evidence linkage
│   ├── C24 Citation integrity
│   └── C36 Reporting and provenance
├── Contribution and reasoning
│   ├── C02 Venue fit
│   ├── C03 Novelty and literature
│   ├── C05 Arguments and counterexamples
│   └── C26 Limitations and threats
├── Experiment design
│   ├── C07 Experiment design
│   ├── C08 Baselines and budgets
│   ├── C09 Ablation and attribution
│   └── C14 Robustness and generalization
├── Evaluation validity
│   ├── C10 Leakage and contamination
│   ├── C11 Statistical inference
│   ├── C12 Human and LLM evaluation
│   └── C13 Systems and resource cost
├── Methods and artifacts
│   ├── C15 Theory and formulas
│   ├── C16 Artifact reproducibility
│   ├── C17 Code–result integrity
│   └── C31 Datasets and benchmarks
├── Figures, tables and numbers
│   ├── C18 Numeric traceability
│   ├── C19 Visual figure inspection
│   ├── C20 Figure scientific support
│   └── C21 Table semantics
├── Bilingual writing
│   ├── C06 Structure and narrative
│   ├── C22 Chinese and English style
│   ├── C23 Evidence-preserving edits
│   └── C34 Translation preservation
├── Review and revision
│   ├── C25 Ethics and research safety
│   ├── C27 Reviewer adjudication
│   ├── C28 Revision and re-check
│   └── C29 Rebuttal and response
└── Delivery and extension
    ├── C30 Submission readiness
    ├── C32 Surveys and reviews
    ├── C33 Coverage and extension
    └── C35 Formats and rendering
```

Inputs → claims/evidence → methods/experiments/statistics → numbers/visuals → writing/citations → challenge/adjudication → revision → recheck.

[SVG](docs/coverage.svg) · [Plain text](docs/coverage.txt) · [Capability registry](docs/CAPABILITY_MAP.md)

## 36 capabilities and outputs

Each ID links directly to its implementation protocol.

| ID | Capability | Function and output |
|---|---|---|
| [C01](skills/paper-review-atlas/references/review-contract.md) | Intake and provenance | Versioned manuscript, supplement, visual, data and code inventory |
| [C02](skills/paper-review-atlas/references/citations-venues.md) | Venue fit | Destination-specific fit and criteria checklist |
| [C03](skills/paper-review-atlas/references/argument-novelty.md) | Novelty and literature | Nearest-work comparison and evidence-backed contribution positioning |
| [C04](skills/paper-review-atlas/references/argument-novelty.md) | Claim–evidence linkage | Claim-to-experiment, proof, figure and citation map |
| [C05](skills/paper-review-atlas/references/argument-novelty.md) | Arguments and counterexamples | Located logical gaps, counterexamples and alternative explanations |
| [C06](skills/paper-review-atlas/references/bilingual-writing.md) | Structure and narrative | Coherent title, abstract, section and paragraph structure |
| [C07](skills/paper-review-atlas/references/experiments-statistics.md) | Experiment design | Claim-specific experiment cards and analysis decisions |
| [C08](skills/paper-review-atlas/references/experiments-statistics.md) | Baselines and budgets | Matched-data, model, tuning, inference and hardware comparison |
| [C09](skills/paper-review-atlas/references/experiments-statistics.md) | Ablation and attribution | Mechanism-isolating ablations and interaction analysis |
| [C10](skills/paper-review-atlas/references/experiments-statistics.md) | Leakage and contamination | Data-lineage and train/test contamination audit |
| [C11](skills/paper-review-atlas/references/experiments-statistics.md) | Statistical inference | Design-aware statistics, uncertainty and multiplicity review |
| [C12](skills/paper-review-atlas/references/experiments-statistics.md) | Human and LLM evaluation | Human/LLM judge design, bias and agreement checks |
| [C13](skills/paper-review-atlas/references/experiments-statistics.md) | Systems and resource cost | End-to-end performance, resource and measurement audit |
| [C14](skills/paper-review-atlas/references/experiments-statistics.md) | Robustness and generalization | Claim-relevant stress tests and generalization analysis |
| [C15](skills/paper-review-atlas/references/formal-theory.md) | Theory and formulas | Notation, dimensional, proof and asymptotic-growth review |
| [C16](skills/paper-review-atlas/references/code-reproducibility.md) | Artifact reproducibility | Artifact-to-command reproducibility map |
| [C17](skills/paper-review-atlas/references/code-reproducibility.md) | Code–result integrity | Code, reference answer, configuration and output consistency |
| [C18](skills/paper-review-atlas/references/figures-tables.md) | Numeric traceability | Source-number reconciliation and checked numeric macros |
| [C19](skills/paper-review-atlas/references/figures-tables.md) | Visual figure inspection | Rendered-figure readability and encoding inspection |
| [C20](skills/paper-review-atlas/references/figures-tables.md) | Figure scientific support | Figure-to-claim reasoning, redesign sketches and captions |
| [C21](skills/paper-review-atlas/references/figures-tables.md) | Table semantics | Table semantics, denominators and comparability checks |
| [C22](skills/paper-review-atlas/references/bilingual-writing.md) | Chinese and English style | Chinese/English grammar, terminology and local prose editing |
| [C23](skills/paper-review-atlas/references/bilingual-writing.md) | Evidence-preserving edits | Meaning-preserving revisions with tracked changes |
| [C24](skills/paper-review-atlas/references/citations-venues.md) | Citation integrity | Citation identity/support checks and local bibliography audit |
| [C25](skills/paper-review-atlas/references/review-contract.md) | Ethics and research safety | Research ethics, authorization and release review |
| [C26](skills/paper-review-atlas/references/argument-novelty.md) | Limitations and threats | Claim-specific limitations, mitigations and residual questions |
| [C27](skills/paper-review-atlas/references/adversarial-review.md) | Reviewer adjudication | Adversarial adjudication, guided dialogue and labeled calibration |
| [C28](skills/paper-review-atlas/references/revision-rebuttal.md) | Revision and re-check | Stable-ID revision tracking and evidence-backed recheck |
| [C29](skills/paper-review-atlas/references/revision-rebuttal.md) | Rebuttal and response | Point-by-point rebuttal and change correspondence |
| [C30](skills/paper-review-atlas/references/citations-venues.md) | Submission readiness | Destination-specific submission and cover-letter preparation |
| [C31](skills/paper-review-atlas/references/argument-novelty.md) | Datasets and benchmarks | Dataset construction, labeling and benchmark governance |
| [C32](skills/paper-review-atlas/references/domain-agent.md) | Surveys and reviews | Review-article search, selection and synthesis audit |
| [C33](skills/paper-review-atlas/references/input-output.md) | Coverage and extension | Capability/feature/gap lookup and extension planning |
| [C34](skills/paper-review-atlas/references/bilingual-writing.md) | Translation preservation | Cross-language preservation of scientific meaning |
| [C35](skills/paper-review-atlas/references/input-output.md) | Formats and rendering | Format-aware extraction, editing and rendering routes |
| [C36](skills/paper-review-atlas/references/input-output.md) | Reporting and provenance | Traceable findings, coverage ledger and actionable report |

### AI / Agent profiles

Intent routing; RAG; planning/tools/memory; generation/self-evaluation; multi-agent cooperation; knowledge graphs/ontologies. Check matched token/call budgets, answer leakage through retrieval, memory across test splits, retry costs and graph-specific gains.

## 11 modes

| Modes | Purpose |
|---|---|
| `full`, `quick` | Full review or central-claim triage |
| `experiments`, `figures`, `writing` | Specialist passes |
| `revise`, `rereview` | Authorized revision and acceptance checks |
| `rebuttal`, `submission` | Responses and submission preparation |
| `guided`, `calibration` | Progressive author dialogue and labeled review evaluation |

Compose modes, for example `full → revise → rereview → submission`.

## Source features and complementary checks

**61 source modules → 227 named facets.** Every Fxxx entry has implementation paths, complementary lanes and a representative case: [integration matrix](docs/FEATURE_MATRIX.md), [walkthroughs](docs/FEATURE_WALKTHROUGH.md).

```text
Experiment design ──is the comparison informative?──> Numeric audit
       ^                                                   |
       | identify confounding                              | units/aggregation
       |                                                   v
Claim/evidence <────────what does it establish?──────── Figure review
       |                                                   |
       └────────supported wording──────────> Bilingual editing
                                                   |
                                       Challenge <-> Adjudication
                                                   |
                                           Revision -> Recheck
```

A correct mean still needs an appropriate comparison; a clear plot still needs data provenance; fluent writing still needs supported claims. Adjudication removes false objections before revision, and recheck verifies the specific repair.

| Source repository | Modules |
|---|---:|
| SRC01 · [augustocamargo/paper-reviewer-skills](https://github.com/augustocamargo/paper-reviewer-skills) | 29 |
| SRC02 · [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 1 |
| SRC03 · [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) | 6 |
| SRC04 · [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | 1 |
| SRC05 · [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 7 |
| SRC06 · [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 4 |
| SRC07 · [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | 3 |
| SRC08 · [CloudWave818/ieee-skills](https://github.com/CloudWave818/ieee-skills) | 3 |
| SRC09 · [manoloss612/peer-review-skill](https://github.com/manoloss612/peer-review-skill) | 1 |
| SRC10 · [GuangyaoYin/skill-scientific-manuscript-review](https://github.com/GuangyaoYin/skill-scientific-manuscript-review) | 1 |
| SRC11 · [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 3 |
| SRC12 · [slark-prime/ml-paper-writing](https://github.com/slark-prime/ml-paper-writing) | 1 |
| SRC13 · [scdenney/open-science-skills](https://github.com/scdenney/open-science-skills) | 1 |

## Real-paper example: ReAct

The [ReAct v3](https://arxiv.org/abs/2210.03629v3) demonstration examines published results and rendered pages, then recomputes transcribed table values.

| Input | Concrete output |
|---|---|
| WebShop Table 4: ReAct 40.0%, Act 30.1% | **9.9 percentage points**; **32.9% relative** to one decimal |
| Wording needs explicit comparators | 9.9/10.9/11.3-point gains against Act/IL/IL+RL and an exact replacement sentence |
| Different main-text/appendix HotpotQA scores | Preserve the distinct evaluations after checking the appendix's 500-question subset |
| Line-chart nonzero y-axis | Inspect actual labeling and purpose; retain readable zoomed ranges |

Suggested wording:

> On WebShop, ReAct achieves a 40.0% success rate, exceeding Act, IL, and IL+RL by 9.9, 10.9, and 11.3 percentage points, respectively.

[Full review, sources and execution output](docs/validation/real-react-review.md). A separately labeled intentional error probe confuses relative percent with percentage points; the CLI detects it.

```bash
python skills/paper-review-atlas/scripts/atlas.py audit \
  --root tests/fixtures/real_react --spec verified-spec.json
```

## Conflict tests and local helpers

Sixteen conflicts cover rounding, issue quotas, sampling units, style/format, evidence access, bilingual preservation, reviewer provenance and closure. On 58 fixed structured cases, the selected policies match 58 expected decisions; the explicitly implemented alternatives match 13. Inputs, policy code, comparison method and outputs are in the [audit record](docs/validation/v1.1-audit.md).

| Commands | Function |
|---|---|
| `plan`, `preflight` | Protocol routing and material inventory |
| `audit` | Exact text anchors, values, units, rounding and paired descriptive summaries |
| `policy` | CFX01–CFX16 decisions from explicit evidence records |
| `export-macros` | Checked LaTeX numerical definitions |
| `bib-audit` | Local BibTeX search, exact-entry export, duplicate and undefined keys |
| `calibrate` | Confusion counts and derived metrics on adjudicated labels |
| `validate-report`, `recheck` | Record checks and supported acceptance-check execution |
| `locate`, `capabilities`, `verify-install` | Extension lookup, capability register and installation checks |

Examples and JSON contracts: [CLI_REFERENCE.md](docs/CLI_REFERENCE.md).

## Find and repair a gap

```bash
python skills/paper-review-atlas/scripts/atlas.py locate C19
python skills/paper-review-atlas/scripts/atlas.py locate academic-paper-reviewer
python skills/paper-review-atlas/scripts/atlas.py locate G03
```

Results identify capabilities, features, protocol files, complements, open tasks, edit locations, test commands and closure criteria. The [extension index](docs/EXTENSION_INDEX.md) contains 12 concrete development directions, including statistical inference, cross-model execution, document adapters, citation retrieval and visual benchmarks.

```text
Missing capability
  └─ locate Cxx / Fxxx / Gxx
      ├─ references/: review steps and output
      ├─ scripts/: executable helper or adapter
      ├─ config/features.json: distinctive facets and complements
      ├─ config/gaps.json: remedy and closure criterion
      └─ tests/: flawed case + correct control + missing evidence
          └─ test -> regenerate README/text map/coverage -> commit
```

```bash
python -m unittest discover -s tests -v
python scripts/build_coverage.py
python scripts/build_feature_docs.py
python scripts/build_coverage.py --check
python scripts/build_feature_docs.py --check
python scripts/check_package.py
```

Both READMEs, the text map, feature matrix and extension index are generated from registries and `docs/templates/`. Update these inputs, regenerate, test and commit them together.

## Layout and license

`skills/paper-review-atlas/` is the portable skill, `tests/` holds checks and fixtures, `docs/` holds capabilities/results/evidence, and `scripts/` maintains installation and generated documentation.

Original implementation: [MIT](LICENSE). External sources retain their licenses. See [source provenance](docs/SOURCES.md) and [implementation/test progress](docs/validation/v1.1-audit.md).
