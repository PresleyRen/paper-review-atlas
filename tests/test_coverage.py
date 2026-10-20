"""Registry correctness and exact generated coverage, not semantic review quality."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_coverage", ROOT / "scripts/build_coverage.py")
assert SPEC and SPEC.loader
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


class CoverageRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = coverage.load_registry(ROOT)

    def test_release_registry_and_protocol_paths_are_consistent(self):
        self.assertEqual([], coverage.validate_registry(self.registry, ROOT))

    def test_requested_core_is_present_without_preventing_extension(self):
        ids = {c["id"] for c in self.registry["capabilities"]["capabilities"]}
        self.assertTrue({f"C{i:02d}" for i in range(1, 37)} <= ids)
        conflicts = {c["id"] for c in self.registry["conflicts"]["conflicts"]}
        self.assertTrue({f"CFX{i:02d}" for i in range(1, 17)} <= conflicts)
        august = next(s for s in self.registry["sources"]["sources"] if s["id"] == "SRC01")
        self.assertEqual(29, len(august["skills"]))

    def test_generated_artifacts_match_single_source_registries(self):
        rendered = coverage.render_all(self.registry)
        self.assertEqual(set(coverage.GENERATED_FILES), set(rendered))
        for relative, expected in rendered.items():
            with self.subTest(path=relative):
                self.assertEqual(expected, (ROOT / relative).read_text(encoding="utf-8"))

    def test_source_inventory_records_scope_without_claiming_copied_ports(self):
        for source in self.registry["sources"]["sources"]:
            with self.subTest(source=source["id"]):
                self.assertEqual("conceptual_reference_only", source["relationship"])
                self.assertFalse(source["copied_code"])
                self.assertFalse(source["copied_instruction_text"])
                self.assertTrue(source["license_note"])
                for module in source["skills"]:
                    self.assertTrue(module["capabilities"])
                    self.assertIn(module["inspection_level"], {"skill_body_reviewed", "catalog_or_cross_reference_only"})
        restricted = next(s for s in self.registry["sources"]["sources"] if s["id"] == "SRC03")
        self.assertIn("Academic Use Only", restricted["license_note"])

    def test_duplicate_ids_and_unknown_sources_are_rejected(self):
        changed = copy.deepcopy(self.registry)
        changed["capabilities"]["capabilities"].append(copy.deepcopy(changed["capabilities"]["capabilities"][0]))
        changed["capabilities"]["capabilities"][1]["sources"].append("UNSEEN_SOURCE")
        errors = coverage.validate_registry(changed, ROOT)
        self.assertTrue(any("duplicate id C01" in e for e in errors))
        self.assertTrue(any("unknown source UNSEEN_SOURCE" in e for e in errors))

    def test_every_source_mapping_is_reciprocal(self):
        changed = copy.deepcopy(self.registry)
        first = changed["sources"]["sources"][0]
        cid = first["skills"][0]["capabilities"][0]
        cap = next(c for c in changed["capabilities"]["capabilities"] if c["id"] == cid)
        cap["sources"].remove(first["id"])
        errors = coverage.validate_registry(changed, ROOT)
        self.assertTrue(any(f"capability {cid} does not map back" in e for e in errors))

    def test_source_module_cannot_map_to_an_invented_capability(self):
        changed = copy.deepcopy(self.registry)
        changed["sources"]["sources"][0]["skills"][0]["capabilities"].append("C999")
        self.assertTrue(any("unknown capabilities ['C999']" in e for e in coverage.validate_registry(changed, ROOT)))

    def test_protocol_path_cannot_escape_skill(self):
        changed = copy.deepcopy(self.registry)
        changed["capabilities"]["capabilities"][0]["protocol"] = "references/../../../../sensitive.md"
        self.assertTrue(any("unsafe or missing protocol path" in e for e in coverage.validate_registry(changed, ROOT)))

    def test_unknown_conflict_reference_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        changed["capabilities"]["capabilities"][0]["verification"]["planned_cases"].append("CFX999")
        self.assertTrue(any("unknown planned cases ['CFX999']" in e for e in coverage.validate_registry(changed, ROOT)))

    def test_executed_test_status_requires_concrete_evidence(self):
        changed = copy.deepcopy(self.registry)
        verification = changed["conflicts"]["conflicts"][0]["verification"]
        verification["state"] = "passed"
        verification["evidence"] = []
        self.assertTrue(any("executed verification needs concrete evidence" in e for e in coverage.validate_registry(changed, ROOT)))
        changed = copy.deepcopy(self.registry)
        verification = changed["capabilities"]["capabilities"][0]["verification"]
        verification["state"] = "passed"
        verification["evidence"] = []
        self.assertTrue(any("C01: executed verification needs concrete evidence" in e for e in coverage.validate_registry(changed, ROOT)))

    def test_stale_missing_test_name_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        v = changed["conflicts"]["conflicts"][0]["verification"]
        v["state"] = "passed"
        v["evidence"] = ["tests/test_coverage.py::CoverageRegistryTests::test_no_such_assertion"]
        self.assertTrue(any("missing test symbol 'test_no_such_assertion'" in e for e in coverage.validate_registry(changed, ROOT)))

    def test_real_nested_test_reference_resolves(self):
        errors = coverage._evidence_errors(
            ["tests/test_coverage.py::CoverageRegistryTests::test_requested_core_is_present_without_preventing_extension"],
            ROOT,
            "structural-reference-test",
        )
        self.assertEqual([], errors)

    def test_evidence_reference_cannot_escape_repository(self):
        self.assertTrue(coverage._evidence_errors(["../outside.json"], ROOT, "test"))
        self.assertTrue(coverage._evidence_errors(["/etc/passwd"], ROOT, "test"))

    def test_evidence_symlink_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as outer:
            parent = Path(outer)
            project = parent / "project"
            project.mkdir()
            secret = parent / "outside.txt"
            secret.write_text("outside", encoding="utf-8")
            (project / "inside.txt").symlink_to(secret)
            errors = coverage._evidence_errors(["inside.txt"], project, "test")
            self.assertTrue(any("escapes repository" in e for e in errors))

    def test_svg_is_valid_xml_and_represents_every_capability_once(self):
        svg = coverage.render_svg(self.registry)
        element = ET.fromstring(svg)
        texts = [node.text for node in element.iter() if node.text]
        for cap in self.registry["capabilities"]["capabilities"]:
            self.assertEqual(1, texts.count(cap["id"]), cap["id"])
        self.assertIn("Coverage is not measured review accuracy", "".join(texts))

    def test_xml_escaping_and_registry_extension_need_no_template_edit(self):
        changed = copy.deepcopy(self.registry)
        new = copy.deepcopy(changed["capabilities"]["capabilities"][-1])
        new.update(id="C37", title_en='A & B <C> "D"', title_zh="新增 & 领域", sources=[])
        new["verification"]["planned_cases"] = []
        new["verification"]["evidence"] = []
        new["verification"]["state"] = "not_measured"
        changed["capabilities"]["capabilities"].append(new)
        self.assertEqual([], coverage.validate_registry(changed, ROOT))
        svg = coverage.render_svg(changed)
        root = ET.fromstring(svg)
        self.assertIn(new["title_en"], "".join(root.itertext()))
        self.assertIn("C37", coverage.render_capability_markdown(changed))
        self.assertIn("37 documented capabilities", svg)

    def test_cli_check_detects_drift_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry_path = root / coverage.REGISTRY_PATH
            registry_path.mkdir(parents=True)
            for name, data in self.registry.items():
                (registry_path / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
            # No evidence references in this isolated fixture; do not fabricate
            # real test results or copy the manuscript/protocol dependencies.
            fixture = coverage.load_registry(root)
            for conflict in fixture["conflicts"]["conflicts"]:
                conflict["verification"]["state"] = "planned"
                conflict["verification"]["evidence"] = []
            for cap in fixture["capabilities"]["capabilities"]:
                cap["verification"]["state"] = "not_measured"
                cap["verification"]["evidence"] = []
            for name, data in fixture.items():
                (registry_path / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(0, coverage.main(["--root", str(root), "--allow-missing-protocols"]))
            target = root / "docs/coverage.svg"
            original = target.read_text(encoding="utf-8")
            target.write_text(original + "\n<!-- stale -->\n", encoding="utf-8")
            self.assertEqual(1, coverage.main(["--root", str(root), "--check", "--allow-missing-protocols"]))
            self.assertTrue(target.read_text(encoding="utf-8").endswith("<!-- stale -->\n"))


if __name__ == "__main__":
    unittest.main()
