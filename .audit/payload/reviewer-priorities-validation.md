# Reviewer-priority validation · 1.2.0

Date: 2026-10-21. Base: `2c0fc694a34293328a1a8fd555fac8941f2e3fcf`.

This update adds a reviewer-priorities protocol, six executable conditional rules, two source modules and a pending-source repair route. The original 61 modules remain mapped. Source modules now total 63 with 239 named facets; 36 top-level capabilities remain stable. Source access, findings and adoption decisions are in [reviewer advice](../../skills/paper-review-atlas/config/reviewer-advice.json).

## What was actually checked

The 1.1 baseline ran 247 tests successfully before changes. New rule cases exercise CFX17–CFX22 using fixed, reviewer-labeled structured inputs. Additional tests check missing fields, wrong types, count limits, source attribution, installation, full/quick routing, CLI execution, new feature/gap lookup and public ReAct table arithmetic. The two new module cases are same-context developer walkthroughs, not independent model invocations.

Run `python scripts/compare_reviewer_priorities.py` to reproduce the comparison. The intentionally simplified alternatives are author-defined rules, not the upstream skills executed in an LLM. Case agreement is not real-paper detection accuracy. The policy helper does not establish whether an input fact is scientifically true or a venue policy is authentic. Existing 58 conflict cases remain in their original regression suite.

Raw new-rule decisions: [comparison JSON](reviewer-priorities-comparison.json). Full test execution: [test log](v1.2-unit-tests.txt). Current test count and commands: [summary](v1.2-summary.json).

## Source handling

The supplied Douyin shortlink did not return accessible video or transcript; exact-title and creator searches did not identify a reliable transcript. No claim from that video was attributed to its creator or used as an implemented rule. ADV00 remains pending, with gap G13 for timestamped integration when content is available.

Matt Might and Prem Devanbu's written reviewer advice was read. PLOS ONE's official reviewer page was read. Nature and Scientific Reports criteria were verified through primary-domain indexed excerpts; full-page retrieval redirected unsuccessfully. These are named, distinct source types, not interchangeable blogger authority.

The two new SKILL.md bodies were read; review-revision's framework reference was additionally read through line 150. No exhaustive subordinate-file audit or upstream runtime execution is claimed. Useful ideas were rewritten; source-specific reviewer counts, punctuation bans, blanket tier rules and mandatory mechanisms were not adopted.

## Real-paper exercise

[ReAct priorities review](real-react-priorities.md) uses the actual v3 Table 1 and its adjacent discussion. Printed pages 5 and 6 were viewed again in this update. Aggregate values were checked and recomputed; original experiments were not rerun. A deliberately overbroad sentence is labeled as a synthetic mutation, not attributed to the authors. Same-context analysis and deterministic regression are reported separately.

## Reproduction

```bash
python -m unittest discover -s tests -v
python scripts/compare_policies.py
python scripts/compare_reviewer_priorities.py
python scripts/check_package.py
python scripts/build_coverage.py --check
python scripts/build_feature_docs.py --check
python skills/paper-review-atlas/scripts/atlas.py verify-install
```
