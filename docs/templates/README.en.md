# Paper Review Atlas

**Locate research-paper weaknesses, produce actionable revisions, and verify the fixes—in Chinese and English.**

Atlas reviews arguments, experiments, statistics, code/results, figures, tables, references and writing. Authors receive traceable findings, proposed replacements, experiment plans and a revision ledger. The AI track covers LLMs, agents, RAG and knowledge graphs.

[中文](README.md) · [Source features](docs/FEATURE_MATRIX.md) · [Real-paper example](docs/validation/real-react-review.md) · [Tests](docs/validation/reviewer-priorities-validation.md) · [Extension index](docs/EXTENSION_INDEX.md)

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
{{TREE}}
```

Inputs → claims/evidence → methods/experiments/statistics → numbers/visuals → writing/citations → challenge/adjudication → revision → recheck.

[SVG](docs/coverage.svg) · [Plain text](docs/coverage.txt) · [Capability registry](docs/CAPABILITY_MAP.md)

## {{CAP_COUNT}} capabilities and outputs

Each ID links directly to its implementation protocol.

| ID | Capability | Function and output |
|---|---|---|
{{CAPABILITIES}}

### AI / Agent profiles

Intent routing; RAG; planning/tools/memory; generation/self-evaluation; multi-agent cooperation; knowledge graphs/ontologies. Check matched token/call budgets, answer leakage through retrieval, memory across test splits, retry costs and graph-specific gains.

## Reviewer priorities and minimum sufficient repairs

The new `priorities` mode identifies evidence gaps affecting the central case before polishing local prose. Full and quick reviews load it automatically.

```text
Problem -> contribution -> operation and prediction -> decisive evidence
                                              |
                                  alternatives and quality-cost tradeoffs
                                              |
                         validity / contribution / venue fit / presentation
                                              |
                                minimum repair -> acceptance condition
```

The pass selects verified venue criteria, compares contributions without branding or module-count shortcuts, separates measured effects from mechanism claims, revisits initial concerns after reading supporting material, and produces a claim-specific repair plan. Optional isolated reviews are frozen before synthesis; later numerical audit findings retain their separate provenance.

```text
Use $paper-review-atlas in priorities mode.
Identify central-case concerns, supporting and opposing evidence,
the minimum sufficient repair and an observable acceptance condition.
Separate validity, contribution, venue fit and presentation.
```

The synthesis uses Matt Might and Prem Devanbu's reviewer advice, official journal criteria, and selected `nature-reviewer` and `review-revision` capabilities. [Sources and adoption](docs/REVIEWER_ADVICE.md) · [Real ReAct exercise](docs/validation/real-react-priorities.md)

## 12 modes

| Modes | Purpose |
|---|---|
| `priorities` | Central case, decisive evidence, venue criteria and minimum repairs |
| `full`, `quick` | Full review or central-claim triage |
| `experiments`, `figures`, `writing` | Specialist passes |
| `revise`, `rereview` | Authorized revision and acceptance checks |
| `rebuttal`, `submission` | Responses and submission preparation |
| `guided`, `calibration` | Progressive author dialogue and labeled review evaluation |

Compose modes, for example `full → revise → rereview → submission`.

## Source features and complementary checks

**{{FEATURE_COUNT}} source modules → {{FACET_COUNT}} named facets.** Every Fxxx entry has implementation paths, complementary lanes and a representative case: [integration matrix](docs/FEATURE_MATRIX.md), [walkthroughs](docs/FEATURE_WALKTHROUGH.md).

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
{{FAMILIES}}

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

Twenty-two conflict policies cover numeric checks, sampling units, evidence access, bilingual preservation, revision closure and the new reviewer-priority decisions. The original 58 fixed cases and 36 new cases have executable inputs and recorded results in the [validation record](docs/validation/reviewer-priorities-validation.md).

| Commands | Function |
|---|---|
| `plan`, `preflight` | Protocol routing and material inventory |
| `audit` | Exact text anchors, values, units, rounding and paired descriptive summaries |
| `policy` | CFX01–CFX22 decisions from explicit evidence records |
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

Results identify capabilities, features, protocol files, complements, open tasks, edit locations, test commands and closure criteria. The [extension index](docs/EXTENSION_INDEX.md) contains 13 concrete development directions, including statistical inference, cross-model execution, document adapters, citation retrieval and visual benchmarks.

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

Original implementation: [MIT](LICENSE). External sources retain their licenses. See [source provenance](docs/SOURCES.md) and [implementation/test progress](docs/validation/reviewer-priorities-validation.md).
