# Paper Review Atlas

**Evidence-grounded peer review, experiment auditing, figure/table inspection, and revision of Chinese and English research papers.**

[中文](README.md) · [Capabilities](docs/CAPABILITY_MAP.md) · [Conflict decisions](docs/CONFLICTS.md) · [Sources](docs/SOURCES.md) · [Validation](docs/VALIDATION.md) · [Extension guide](docs/EXTENDING.md)

Atlas synthesizes concepts from **13 public repositories and 61 skill/workflow modules** into **36 capabilities, 12 specialist protocols and 9 composable modes**. This is an original implementation. All 61 inventoried primary skill bodies were read; their subordinate scripts and references were not comprehensively audited. Source inspection, implemented workflow, deterministic helpers, measured behavior and external dependencies are recorded separately. Inclusion in the source inventory does not imply a complete port of an upstream tool.

![Capability coverage](docs/coverage.svg)

**W** = implemented workflow; **D** = bounded deterministic helper; **A** = external tool, model, visual access, data or execution environment needed. Coverage is not a measured scientific-error detection rate.

## Install and invoke

Python 3.10+ is required for local helpers. The runtime and automated tests use the standard library.

```bash
git clone https://github.com/PresleyRen/paper-review-atlas.git
cd paper-review-atlas
python scripts/install_skill.py --project /absolute/path/to/your-paper-project
```

This installs the self-contained skill at `.agents/skills/paper-review-atlas/` in the chosen project. Existing installations are preserved; `--replace` makes a timestamped backup in the project's `.paper-review-atlas-backups/` directory, outside active skill discovery, before updating. Host skill discovery varies. Reload its skill list when needed, or provide the complete skill directory to a host that loads `SKILL.md`.

```text
Use $paper-review-atlas for a full, rigorous review of this manuscript.
Review claims, experiments, statistics, code/result consistency, all figures
and tables, references, and language. Give the report in English.
For Chinese passages, retain Chinese in proposed replacements.
For each finding provide the exact location, evidence, consequence,
actionable fix and acceptance check. Mark unavailable evidence explicitly.
```

Focused tasks can request `figures`, `experiments`, or `writing`. To apply changes, explicitly request `revise`; use `rereview` to check the resulting evidence. A review-only request does not trigger manuscript rewriting, while authorized revision does not require repeated routine confirmations.

## Capability detail

| Area | What the protocol examines |
|---|---|
| Contribution and argument | Question, novelty positioning, abstract/title/contribution consistency, claim–evidence map, alternatives, counterexamples, structure, survey selection and coverage |
| Experiment design | Strong controls, matched resources, baseline tuning, attribution, ablations, negative results, discriminating experiments, datasets and benchmark design |
| Evaluation validity | Leakage, actual independent units, seeds/tasks/participants, pairing and repeated measures, uncertainty and effect size, multiplicity, LLM judge bias and human assessment |
| Systems and artifacts | Compute/latency/cost, tool calls, environment/config/data/model versions, metric implementation, logs, traceability from artifact to displayed result |
| Mathematics | Notation, dimensions, assumptions, equations, proof obligations, boundary cases and theorem-to-experiment scope; no automatic proof claim |
| Figures, tables and values | Scientific interpretation, actual rendered appearance, axes/units/scale, legends, uncertainty, sample size, table semantics, captions and source-data reconciliation |
| Bilingual writing | Chinese and English structure/grammar/terminology, abstract consistency, exact replacements, translation, preservation of quantities, negations, uncertainty and causal strength |
| Review and revision | Specialist perspectives, adversarial challenge and defense, false-positive adjudication, severity, feasible repair, stable issue IDs, re-review, rebuttal and cover letters |
| Submission and maintenance | Citation identity versus claim support, current venue requirements, ethics/disclosure/artifacts, limitations, coverage ledger, provenance and extension roadmap |

The [capability register](docs/CAPABILITY_MAP.md) lists every stable ID, its implementation route, helpers, external requirements and evidence. The Agent track adds six profiles: routing/intent, RAG, planning/tools/memory, answer generation/self-evaluation, multi-agent cooperation, and knowledge graphs/ontologies. Each profile covers claims, baselines, ablations, leakage, metrics/judges, costs and robustness. Discipline-specific standards are routed by relevance rather than imposed universally.

Additional protocols cover limited-surface first impressions, claim-to-section and experiment-to-result navigation, benchmark leaderboard governance, annotation disagreements, study attrition and carryover, qualitative coding, measurement overhead and energy estimates, local bibliography retrieval/export, and Typst/Hayagriva preservation. Submission work includes evidence-based venue comparison, sentence-level cover-letter alignment and recorded adjudication of external reviews. These are conditional workflows; parsers, compilers, inferential statistics and external retrieval remain host-dependent, and unmeasured behavior stays marked in the registry.

## Modes

| Mode | Purpose |
|---|---|
| `full` | All applicable review areas, with explicit evidence gaps |
| `quick` | Central claim, strongest evidence, principal validity risks |
| `experiments` | Design, fairness, statistics, leakage, cost and reproducibility |
| `figures` | Scientific, rendered and numerical layers of each visual/table |
| `writing` | Chinese/English prose and evidence-preserving replacements |
| `revise` | Authorized edits and change records |
| `rereview` | Recheck old findings against revised evidence |
| `rebuttal` | Comment triage, evidence-based responses and change mapping |
| `submission` | Current requirements and final deliverable checks |

Modes can be composed. PDFs, DOCX, LaTeX and Typst require host-provided extraction/rendering/compilation tools; missing tools remain visible in the scope ledger.

## Conflict resolution

The [16-entry conflict ledger](docs/CONFLICTS.md) records alternatives, selection, rationale and executed/planned evidence. Examples:

- **Rounding vs raw equality:** Decimal arithmetic, explicit units and declared rounding accept `0.9477 → 0.948`; percentage points and relative percent remain distinct.
- **Strictness vs fault quotas:** zero findings are allowed; serious objections receive a reasoned defense before retention or withdrawal.
- **Style vs science:** punctuation preferences and valid raster figures do not become scientific defects automatically.
- **More samples vs correct units:** seed, question, participant and repeated-answer counts cannot be substituted for one another.
- **Personas vs independent models:** single-model role coverage is labeled honestly; cross-family declarations require actual family records.
- **Missing evidence vs allegations:** unavailable data limit verification; they do not prove misconduct.
- **Text extraction vs visual inspection:** interpreting a figure, viewing pixels and recomputing values are separate activities.
- **Claimed completion vs closure:** an issue requires original and revised evidence plus a substantive check; supported numeric/quote checks can be rerun.

Tests support these specific choices. They do not establish universal superiority across all disciplines, manuscripts or models. Partial evidence stays partial in the register.

## Deterministic CLI and its limits

The CLI does not call an LLM or generate a peer review by itself. The host model performs semantic review using the protocols.

| Command | What it does |
|---|---|
| `plan` | Select protocol references and outputs |
| `preflight` | Check declared file availability; no content review |
| `audit` | Verify exact UTF-8 quote anchors; recompute declared CSV/JSON value/mean/sum/count, units, rounding, relative changes and paired descriptive summaries |
| `validate-report` | Validate records, evidence anchors, coverage logs and reviewer declarations; not scientific correctness |
| `recheck` | Recompute supported checks or verify concrete manual-check records, keeping their scopes distinct |
| `capabilities` | Print the installed registry |
| `verify-install` | Check package files and registry readability |

```bash
python skills/paper-review-atlas/scripts/atlas.py plan --mode full --language en --domain agent
python skills/paper-review-atlas/scripts/atlas.py preflight --root tests/fixtures/en_agent --manifest manifest.json
python skills/paper-review-atlas/scripts/atlas.py audit --root tests/fixtures --spec integration-audit.json
```

The last command intentionally returns **1**: the synthetic paper's mean and relative gain are wrong, while its calibration rounding is correct. Exit codes: **0** declared checks successful; **1** mismatch/invalid record; **2** invalid input; **3** unverified evidence. Success never means “paper accepted” or “science validated.”

No network calls, arbitrary expressions, shell fragments or manuscript code execution occur in the helpers. Evidence paths are confined to the explicit root, including symlink resolution. Numeric sources are bounded to 5 MiB / 10,000 records; command JSON to 4 MiB. The paired helper reports sample SD and differences, without a p-value or CI. Full interfaces and recheck examples: [CLI_REFERENCE.md](docs/CLI_REFERENCE.md).

## Review output

A retained finding has a stable ID, title, severity, status, precise location and quote/object, evidence basis, consequence, remedy and acceptance check. The complete report includes scope, a claim–evidence table, original-language replacements, feasible experiment alternatives, priorities and unresolved checks.

Issue status is `confirmed | unverified | closed`; severity is `critical | major | minor | editorial`; evidence basis is `observed | inferred | missing`. These dimensions are not interchangeable. Exact quote matching proves an anchor, not that a criticism is scientifically sound. An inspection log proves a recorded observation, not automatic pixel understanding.

## Validation and development

```bash
python -m unittest discover -s tests -v
python scripts/check_package.py
python scripts/build_coverage.py --check
python skills/paper-review-atlas/scripts/atlas.py verify-install
```

[VALIDATION.md](docs/VALIDATION.md) records executed tests, fresh-context Chinese/English forward reviews, correct controls, defects repaired during integration and remaining uncertainty. The fictional fixtures contain no user manuscripts or real research results. Fresh-context agents were not given the answer key, but remain development tests within one model family, not independent human evaluation or a calibrated benchmark.

The optional figure-rebuild script needs matplotlib; the runtime and test suite do not. `skills/paper-review-atlas/` is the portable package; `docs/` holds maps/provenance/validation; `tests/` holds fixtures and checks; root `scripts/` maintains installation and generated documentation.

To add a capability, give it a stable registry ID, implement its actual protocol/helper, add positive and negative examples, record concrete verification evidence, and regenerate the SVG/Markdown/Mermaid outputs. See [EXTENDING.md](docs/EXTENDING.md) for the current gaps and process.

## Sources and license

Original implementation files are [MIT licensed](LICENSE). External projects retain their licenses. The source ledger records full-text inspection, its scope and available blob identifiers, plus restrictions or uncertainty. Restricted or unclear sources are conceptual references only; no upstream skill text or implementation is vendored in this release.
