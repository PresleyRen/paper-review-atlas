"""Meaningful arithmetic, provenance, and conflicting-evidence regressions.

Conflict references use the registry's stable IDs: CFX01 numeric units and
rounding; CFX02 zero findings; CFX03 acceptance probabilities; CFX04 sampling
units; CFX09 reviewer independence; CFX12 unavailable images; CFX13 execution
provenance; CFX15 quote/adjudication evidence; CFX16 revision closure.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "skills" / "paper-review-atlas" / "scripts" / "audit_checks.py"
SPEC = importlib.util.spec_from_file_location("atlas_audit_checks", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="atlas-audit-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("manuscript.md", "# Study\nReported accuracy is 80%.\n该结果需要多次运行验证。\n")
        self.write("revision.md", "# Revised study\nReported accuracy is 82%.\n")
        self.write("checks.md", "Recomputed accuracy from two records: mean 0.82 = 82%.\n")
        self.write("results.csv", "model,run,score\nold,1,0.8\nnew,1,0.81\nnew,2,0.83\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def json_source(self, rows, name="values.json"):
        self.write(name, json.dumps(rows, ensure_ascii=False))
        return {"path": name, "format": "json"}

    def claim(self, **overrides):
        result = {"source": {"path": "results.csv", "format": "csv", "where": {"model": "new"}},
                  "operation": "mean", "field": "score", "reported": "82",
                  "source_unit": "fraction", "reported_unit": "percent"}
        result.update(overrides)
        return result

    def issue(self, **overrides):
        issue = {"id": "I1", "status": "confirmed", "severity": "major",
                 "location": {"path": "manuscript.md", "line": 2},
                 "evidence": {"quote": "Reported accuracy is 80%."},
                 "fix": "Recompute the stated accuracy from the supplied run records.",
                 "acceptance_check": "The stated accuracy equals the two-run mean expressed as a percent."}
        issue.update(overrides)
        return issue

    def revision(self):
        return {"path": "revision.md", "quote": "Reported accuracy is 82%.", "line": 2}

    def check(self, **overrides):
        check = {"status": "passed", "method": "Recompute the two-run mean from results.csv.",
                 "observations": "The records 0.81 and 0.83 average to 0.82, matching the revised 82%.",
                 "evidence": {"path": "checks.md", "quote": "Recomputed accuracy from two records: mean 0.82 = 82%.", "line": 1}}
        check.update(overrides)
        return check


class SafePathTests(FixtureCase):
    def test_rooted_relative_and_inside_absolute_paths(self):
        expected = self.root / "manuscript.md"
        self.assertEqual(audit.resolve_under_root(self.root, "manuscript.md"), expected)
        self.assertEqual(audit.resolve_under_root(self.root, expected), expected)

    def test_traversal_and_outside_absolute_rejected(self):
        for path in ("../escape.txt", "sub/../manuscript.md", str(self.root.parent / "outside.txt")):
            with self.subTest(path=path), self.assertRaises(audit.AuditInputError):
                audit.resolve_under_root(self.root, path, must_exist=False)

    def test_external_and_dangling_symlinks_rejected(self):
        (self.root / "escape").symlink_to(self.root.parent)
        (self.root / "dangling").symlink_to(self.root.parent / "not-present-atlas.txt")
        for path in ("escape/elsewhere.txt", "dangling"):
            with self.subTest(path=path), self.assertRaises(audit.AuditInputError):
                audit.resolve_under_root(self.root, path, must_exist=False)

    def test_internal_symlink_allowed_and_missing_file_unverified(self):
        (self.root / "alias.md").symlink_to(self.root / "manuscript.md")
        result = audit.verify_quote(self.root, "alias.md", "Reported accuracy is 80%.", line=2)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["source"], "manuscript.md")
        self.assertEqual(audit.verify_quote(self.root, "missing.md", "absent")["status"], "unverified")


class QuoteTests(FixtureCase):
    def test_exact_bilingual_multiline_quote_with_real_anchor(self):
        quote = "Reported accuracy is 80%.\n该结果需要多次运行验证。"
        result = audit.verify_quote(self.root, "manuscript.md", quote, line=2)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["matches"], [{"line_start": 2, "line_end": 3, "column_start": 1}])
        repeated = self.write("repeat.txt", "first\nquoted\nquoted\n")
        self.assertEqual([m["line_start"] for m in audit.verify_quote(self.root, repeated, "quoted")["matches"]], [2, 3])

    def test_wrong_quote_or_anchor_is_mismatch(self):
        """CFX15: a plausible quote or invented line cannot confirm an issue."""
        self.assertEqual(audit.verify_quote(self.root, "manuscript.md", "accuracy is 99%.")["status"], "mismatch")
        wrong_line = audit.verify_quote(self.root, "manuscript.md", "Reported accuracy is 80%.", line=3)
        self.assertEqual(wrong_line["status"], "mismatch")
        self.assertEqual(wrong_line["actual_start_lines"], [2])
        self.assertEqual(wrong_line["matches"], [])

    def test_quote_matching_is_literal_not_normalized(self):
        self.write("literal.txt", "A  B\r\ncaf\u00e9\n")
        for quote in ("A B", "A  B\ncafé", "cafe\u0301"):
            with self.subTest(quote=quote):
                self.assertEqual(audit.verify_quote(self.root, "literal.txt", quote)["status"], "mismatch")
        self.assertEqual(audit.verify_quote(self.root, "literal.txt", "A  B\r\ncafé")["status"], "verified")

    def test_bad_line_empty_or_huge_quote_rejected(self):
        for line in (0, -1, True, "2", 1.5):
            with self.subTest(line=line), self.assertRaises(audit.AuditInputError):
                audit.verify_quote(self.root, "manuscript.md", "Study", line=line)
        for quote in ("", " \n", "x" * (audit.MAX_QUOTE_CHARS + 1)):
            with self.subTest(length=len(quote)), self.assertRaises(audit.AuditInputError):
                audit.verify_quote(self.root, "manuscript.md", quote)

    def test_unreadable_encoding_and_nonfile_unverified(self):
        (self.root / "bad.bin").write_bytes(b"\xff\xfe")
        for path in ("bad.bin", "."):
            with self.subTest(path=path):
                self.assertEqual(audit.verify_quote(self.root, path, "Study")["status"], "unverified")


class NumericTests(FixtureCase):
    def test_value_mean_sum_count_csv(self):
        cases = [("mean", "0.82"), ("sum", "1.64"), ("count", "2")]
        for operation, reported in cases:
            claim = self.claim(operation=operation, reported=reported, source_unit="number", reported_unit="number")
            if operation == "count":
                del claim["field"]
            with self.subTest(operation=operation):
                result = audit.reconcile_number(self.root, claim)
                self.assertEqual(result["status"], "verified")
                self.assertEqual(result["source"]["rows_selected"], 2)
        claim = self.claim(source={"path": "results.csv", "format": "csv", "where": {"model": "old"}},
                           operation="value", reported="80")
        self.assertEqual(audit.reconcile_number(self.root, claim)["status"], "verified")

    def test_json_records_key_and_exact_typed_filters(self):
        self.json_source({"rows": [{"group": 1, "score": "4.5"}, {"group": True, "score": "100"}]})
        claim = self.claim(source={"path": "values.json", "format": "json", "records_key": "rows", "where": {"group": 1}},
                           operation="value", reported="4.5", source_unit="number", reported_unit="number")
        result = audit.reconcile_number(self.root, claim)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["source"]["rows_selected"], 1)

    def test_decimal_half_even_and_half_up_rounding(self):
        """CFX01: decimal ties do not inherit binary-float rounding errors."""
        for value, even, up in [("2.665", "2.66", "2.67"), ("2.675", "2.68", "2.68"), ("-2.665", "-2.66", "-2.67")]:
            source = self.json_source([{"score": value}])
            for mode, reported in (("half_even", even), ("half_up", up)):
                with self.subTest(value=value, mode=mode):
                    result = audit.reconcile_number(self.root, self.claim(source=source, operation="value", reported=reported,
                                                   source_unit="number", reported_unit="number", rounding={"places": 2, "mode": mode}))
                    self.assertEqual(result["status"], "verified")
                    self.assertEqual(result["rounded_calculated"], reported)

    def test_tolerance_applies_after_rounding_in_reported_units(self):
        source = self.json_source([{"score": "1.234"}])
        claim = self.claim(source=source, operation="value", reported="1.24", source_unit="number", reported_unit="number",
                           rounding={"places": 2}, tolerance="0.01")
        self.assertEqual(audit.reconcile_number(self.root, claim)["status"], "verified")
        claim["tolerance"] = "0.009"
        result = audit.reconcile_number(self.root, claim)
        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["absolute_error"], "0.01")
        with self.assertRaises(audit.AuditInputError):
            audit.reconcile_number(self.root, self.claim(tolerance="-0.1"))

    def test_fraction_percent_scaling_requires_explicit_units(self):
        """CFX01: 0.82 as a fraction means 82%, not 0.82%."""
        self.assertEqual(audit.reconcile_number(self.root, self.claim())["status"], "verified")
        self.assertEqual(audit.reconcile_number(self.root, self.claim(source_unit="percent"))["status"], "mismatch")
        with self.assertRaises(audit.AuditInputError):
            audit.reconcile_number(self.root, self.claim(source_unit="number"))
        source = self.json_source([{"score": "82"}])
        self.assertEqual(audit.reconcile_number(self.root, self.claim(source=source, operation="value", reported="0.82",
                        source_unit="percent", reported_unit="fraction"))["status"], "verified")

    def test_relative_percent_and_percentage_points_are_distinct(self):
        """CFX01: 80% to 82% is +2 points but +2.5 percent relative."""
        baseline = {"source": {"path": "results.csv", "format": "csv", "where": {"model": "old"}},
                    "operation": "value", "field": "score"}
        relative = self.claim(comparison=baseline, change="relative_percent", reported="2.5")
        points = self.claim(comparison=baseline, change="percentage_points", reported_unit="percentage_point", reported="2")
        self.assertEqual(audit.reconcile_number(self.root, relative)["status"], "verified")
        self.assertEqual(audit.reconcile_number(self.root, points)["status"], "verified")
        points["reported"] = "2.5"
        self.assertEqual(audit.reconcile_number(self.root, points)["status"], "mismatch")
        points["reported_unit"] = "percent"
        with self.assertRaises(audit.AuditInputError):
            audit.reconcile_number(self.root, points)

    def test_zero_baseline_is_unverified(self):
        baseline = {"source": self.json_source([{"score": 0}]), "operation": "value", "field": "score"}
        result = audit.reconcile_number(self.root, self.claim(comparison=baseline, change="relative_percent", reported="100"))
        self.assertEqual(result["status"], "unverified")
        self.assertIn("zero baseline", result["message"])

    def test_empty_missing_and_multiple_value_groups_unverified(self):
        claims = [self.claim(source={"path": "absent.csv", "format": "csv"}),
                  self.claim(source={"path": "results.csv", "format": "csv", "where": {"model": "absent"}}),
                  self.claim(operation="value"), self.claim(field="absent_column")]
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertEqual(audit.reconcile_number(self.root, claim)["status"], "unverified")
        empty_count = self.claim(source=self.json_source([]), operation="count", source_unit="number", reported_unit="number", reported="0")
        del empty_count["field"]
        self.assertEqual(audit.reconcile_number(self.root, empty_count)["status"], "unverified")

    def test_source_nan_inf_bool_and_missing_values_rejected(self):
        for value in ("NaN", "Infinity", "-Inf", True, None, "", " ", "1_000"):
            source = self.json_source([{"score": value}])
            with self.subTest(value=value):
                result = audit.reconcile_number(self.root, self.claim(source=source))
                self.assertEqual(result["status"], "unverified")
                self.assertNotIn("calculated", result)

    def test_bad_reported_numbers_and_declaration_bounds_rejected(self):
        for reported in ("NaN", float("inf"), True, None, "1e100", "1234567890123456789012345678901"):
            with self.subTest(reported=reported), self.assertRaises(audit.AuditInputError):
                audit.reconcile_number(self.root, self.claim(reported=reported))
        for overrides in ({"operation": "eval"}, {"rounding": {"places": True}}, {"rounding": {"places": 13}},
                          {"rounding": {"places": 1, "mode": "truncate"}}, {"formula": "os.system('bad')"},
                          {"reported_unit": []}, {"change": "relative_percent"}):
            with self.subTest(overrides=overrides), self.assertRaises(audit.AuditInputError):
                audit.reconcile_number(self.root, self.claim(**overrides))

    def test_malformed_csv_and_json_duplicate_keys_are_unverified(self):
        cases = [("duplicate.csv", "score,score\n1,2\n", "csv"),
                 ("ragged.csv", "score,run\n1\n", "csv"),
                 ("duplicate.json", '[{"score": 1, "score": 2}]', "json"),
                 ("nan.json", '[{"score": NaN}]', "json"),
                 ("invalid.json", '{"rows": [', "json")]
        for name, body, format_ in cases:
            self.write(name, body)
            with self.subTest(name=name):
                self.assertEqual(audit.reconcile_number(self.root, self.claim(source={"path": name, "format": format_}))["status"], "unverified")

    def test_injection_is_inert_text_not_expression(self):
        """CFX13: shell/Python-looking manuscript text is evidence, never code."""
        marker = self.root / "SHOULD_NOT_EXIST"
        injection = f"__import__('pathlib').Path({str(marker)!r}).touch(); $(touch SHOULD_NOT_EXIST)"
        self.write("project.py", injection)
        source = self.json_source([{"label": injection, "score": "0.82"}])
        source["where"] = {"label": injection}
        self.assertEqual(audit.reconcile_number(self.root, self.claim(source=source))["status"], "verified")
        self.assertEqual(audit.verify_quote(self.root, "project.py", injection)["status"], "verified")
        self.assertFalse(marker.exists())
        with self.assertRaises(audit.AuditInputError):
            audit.reconcile_number(self.root, self.claim(source=dict(source, command=injection)))

    def test_source_path_escape_rejected(self):
        with self.assertRaises(audit.AuditInputError):
            audit.reconcile_number(self.root, self.claim(source={"path": "../outside.csv", "format": "csv"}))

    def test_file_and_record_bounds_unverified(self):
        with patch.object(audit, "MAX_FILE_BYTES", 16):
            self.assertEqual(audit.reconcile_number(self.root, self.claim())["status"], "unverified")
        with patch.object(audit, "MAX_RECORDS", 2):
            self.assertEqual(audit.reconcile_number(self.root, self.claim())["status"], "unverified")


class PairedStatsTests(FixtureCase):
    def test_paired_sample_sd_and_difference_not_unpaired(self):
        """CFX04: explicit paired differences use n-1 sample SD."""
        result = audit.paired_run_stats({"s3": 3, "s1": 1, "s2": 2}, {"s1": 2, "s2": 4, "s3": 6})
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["run_ids"], ["s1", "s2", "s3"])
        self.assertEqual(result["left"], {"n": 3, "mean": "2", "sample_sd": "1"})
        self.assertEqual(result["right"], {"n": 3, "mean": "4", "sample_sd": "2"})
        self.assertEqual(result["difference"], {"n": 3, "mean": "2", "sample_sd": "1"})
        self.assertEqual(result["paired_differences"], {"s1": "1", "s2": "2", "s3": "3"})
        self.assertIsNone(result["p_value"])
        self.assertIsNone(result["confidence_interval"])
        self.assertEqual(result["inference_status"], "unverified")

    def test_single_seed_zero_difference_does_not_establish_no_effect(self):
        """CFX04: n=1 and a zero observed difference are not equivalence evidence."""
        result = audit.paired_run_stats({"seed1": "0.8"}, {"seed1": "0.8"})
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["n"], 1)
        self.assertEqual(result["difference"]["mean"], "0")
        self.assertIsNone(result["difference"]["sample_sd"])
        self.assertIn("does not establish equivalence", " ".join(result["limitations"]))

    def test_pair_ids_must_match_without_silent_dropping(self):
        result = audit.paired_run_stats({"a": 1, "b": 2}, {"b": 3, "c": 4})
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["missing_from_left"], ["c"])
        self.assertEqual(result["missing_from_right"], ["a"])
        self.assertNotIn("difference", result)

    def test_empty_or_nonfinite_runs_rejected(self):
        self.assertEqual(audit.paired_run_stats({}, {})["status"], "unverified")
        for value in (True, float("nan"), Decimal("Infinity")):
            with self.subTest(value=value), self.assertRaises(audit.AuditInputError):
                audit.paired_run_stats({"s": value}, {"s": 1})


class ValidationTests(FixtureCase):
    def test_zero_findings_valid(self):
        """CFX02: a finding quota must never invent a criticism."""
        result = audit.validate_report({"issues": []}, root=self.root)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["issues"], [])

    def test_confirmed_issue_requires_exact_quote_location(self):
        """CFX15: record validation does not certify the judgment's semantics."""
        result = audit.validate_issue(self.issue(), root=self.root)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["effective_status"], "confirmed")
        self.assertEqual(result["validation_scope"], "record_structure_and_exact_evidence_anchors")
        result = audit.validate_issue(self.issue(evidence={"quote": "Reported accuracy is 99%."}), root=self.root)
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["effective_status"], "unverified")

    def test_missing_evidence_stays_unverified_not_misconduct(self):
        issue = self.issue(evidence={}, severity="minor", claim_type="possible_data_problem")
        result = audit.validate_issue(issue, root=self.root)
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["effective_status"], "unverified")
        self.assertEqual(issue["severity"], "minor")
        self.assertNotIn("misconduct", json.dumps(result))

    def test_self_reported_verified_status_without_root_not_enough(self):
        result = audit.validate_issue(self.issue(evidence={"quote": "Reported accuracy is 80%.", "status": "verified"}))
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["effective_status"], "unverified")

    def test_issue_requires_actionable_fix_acceptance_check_and_id(self):
        for overrides in ({"id": ""}, {"fix": "fix it"}, {"acceptance_check": "looks good"}, {"severity": "fatal"}):
            with self.subTest(overrides=overrides):
                self.assertEqual(audit.validate_issue(self.issue(**overrides), root=self.root)["status"], "invalid")
        bilingual = self.issue(fix="使用提供的两次运行记录重新计算准确率。", acceptance_check="修订后的准确率应等于两次运行均值乘以百分之一百。")
        self.assertEqual(audit.validate_issue(bilingual, root=self.root)["status"], "valid")

    def test_same_model_personas_not_cross_family_independence(self):
        """CFX09: multiple personas do not create independent model families."""
        reviewers = [{"id": "r1", "model": "same-model", "family": "GPT", "persona": "statistician"},
                     {"id": "r2", "model": "same-model", "family": "gpt", "persona": "editor"}]
        report = {"issues": [], "reviewers": reviewers, "independence_claim": "cross_family"}
        self.assertEqual(audit.validate_report(report)["status"], "invalid")
        report["independence_claim"] = "multi_persona"
        self.assertEqual(audit.validate_report(report)["status"], "valid")
        reviewers[1]["family"] = "made-up-different-family"
        report["independence_claim"] = "cross_family"
        self.assertEqual(audit.validate_report(report)["status"], "invalid")

    def test_different_families_allowed_as_declared_not_authenticated(self):
        report = {"issues": [], "independence_claim": "cross_family", "reviewers": [
            {"id": "r1", "model": "model-a", "family": "family-a"},
            {"id": "r2", "model": "model-b", "family": "family-b"}]}
        result = audit.validate_report(report)
        self.assertEqual(result["status"], "valid")
        self.assertIn("not authenticated", " ".join(result["warnings"]))

    def test_acceptance_probability_claims_rejected(self):
        """CFX03: an offline review cannot manufacture acceptance probabilities."""
        for key in ("acceptance_probability", "acceptance-odds", "publication_probability"):
            with self.subTest(key=key):
                self.assertEqual(audit.validate_report({"issues": [], "recommendation": {key: "85%"}})["status"], "invalid")
        self.assertEqual(audit.validate_report({"issues": [], "acceptance_probability": None})["status"], "valid")

    def test_missing_figure_cannot_pass_but_log_plus_artifact_can(self):
        """CFX12: missing visual evidence remains unavailable, never a passed audit."""
        report = {"issues": [], "coverage": {"figures": {"status": "passed", "evidence": []}}}
        self.assertEqual(audit.validate_report(report, root=self.root)["status"], "unverified")
        self.write("figure-review.md", "Figure 1 labels and plotted values were compared with results.csv; all labels are readable.\n")
        area = report["coverage"]["figures"]
        area["evidence"] = [{"path": "figure-review.md", "quote": "Figure 1 labels and plotted values were compared with results.csv; all labels are readable."}]
        # A locatable inspection log still cannot establish that the image was
        # available: visual coverage must declare its source artifact as well.
        self.assertEqual(audit.validate_report(report, root=self.root)["status"], "unverified")
        area["artifacts"] = ["figure.png"]
        self.assertEqual(audit.validate_report(report, root=self.root)["status"], "unverified")
        (self.root / "figure.png").write_bytes(b"fixture artifact; this test does not claim pixel inspection")
        result = audit.validate_report(report, root=self.root)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["coverage"]["figures"]["validation_scope"], "inspection_record_anchors_and_artifact_presence")

    def test_duplicate_issue_id_and_wrong_schemas_rejected(self):
        result = audit.validate_report({"issues": [self.issue(), self.issue()]}, root=self.root)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("duplicate issue id", " ".join(result["errors"]))
        for report in ({}, {"issues": "none"}, {"issues": [], "independence_claim": []},
                       {"issues": [], "coverage": {"figures": {"status": []}}}):
            with self.subTest(report=report):
                self.assertEqual(audit.validate_report(report)["status"], "invalid")
        self.assertEqual(audit.validate_issue(self.issue(severity=[]), root=self.root)["status"], "invalid")


class RecheckTests(FixtureCase):
    def test_author_says_done_and_approval_language_cannot_close(self):
        """CFX16: an approval string is not a recorded substantive check."""
        for method in ("author says done", "author confirmation", "reviewer approved", "looks good", "作者确认"):
            with self.subTest(method=method):
                result = audit.recheck_issue(self.issue(), self.revision(), self.check(method=method), root=self.root)
                self.assertEqual(result["status"], "open")

    def test_missing_or_false_revision_or_check_record_remains_open(self):
        cases = [(None, self.check()), (self.revision(), None),
                 ({"path": "revision.md", "quote": "accuracy is 100%"}, self.check()),
                 (self.revision(), self.check(evidence={"path": "missing-log.md", "quote": "passed"}))]
        for revision, check in cases:
            with self.subTest(revision=revision, check=check):
                self.assertEqual(audit.recheck_issue(self.issue(), revision, check, root=self.root)["status"], "open")

    def test_manual_closure_records_scope_and_requires_observations(self):
        result = audit.recheck_issue(self.issue(), self.revision(), self.check(), root=self.root)
        self.assertEqual(result["status"], "closed")
        self.assertEqual(result["validation"]["closure_check"]["closure_scope"], "recorded_evidence_only")
        check = self.check()
        del check["observations"]
        self.assertEqual(audit.recheck_issue(self.issue(), self.revision(), check, root=self.root)["status"], "open")

    def test_declarative_quote_recomputed(self):
        specification = dict(self.revision(), kind="quote")
        check = self.check(evaluation=specification)
        del check["observations"]
        result = audit.recheck_issue(self.issue(), self.revision(), check, root=self.root)
        self.assertEqual(result["status"], "closed")
        closure = result["validation"]["closure_check"]
        self.assertEqual(closure["closure_scope"], "declarative_check_recomputed")
        self.assertEqual(closure["check_evaluation"]["status"], "verified")
        self.assertEqual(closure["check_evaluation"]["execution_scope"], "builtin_declarative_check_only")

    def test_declarative_number_failure_overrides_passed_claim(self):
        """CFX16: an actual contradictory recomputation defeats status='passed'."""
        check = self.check(evaluation={"kind": "number", "claim": self.claim(reported="90")})
        result = audit.recheck_issue(self.issue(), self.revision(), check, root=self.root)
        self.assertEqual(result["status"], "open")
        closure = result["validation"]["closure_check"]
        self.assertEqual(closure["check_evaluation"]["status"], "mismatch")
        self.assertEqual(result["validation"]["status"], "invalid")

    def test_declarative_number_verified_closes_with_check_scope(self):
        check = self.check(evaluation={"kind": "number", "claim": self.claim()})
        result = audit.recheck_issue(self.issue(), self.revision(), check, root=self.root)
        self.assertEqual(result["status"], "closed")
        self.assertEqual(result["validation"]["closure_check"]["check_evaluation"]["calculated"], "82")
        check["status"] = "failed"
        self.assertEqual(audit.recheck_issue(self.issue(), self.revision(), check, root=self.root)["status"], "open")

    def test_recheck_preserves_original_issue_and_missing_root_unverified(self):
        issue, revision, check = self.issue(), self.revision(), self.check()
        original = copy.deepcopy((issue, revision, check))
        self.assertEqual(audit.recheck_issue(issue, revision, check)["status"], "unverified")
        self.assertEqual((issue, revision, check), original)


if __name__ == "__main__":
    unittest.main()
