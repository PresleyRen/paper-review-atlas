"""Integration tests for honest CLI outcomes and a portable project install."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/paper-review-atlas"
CLI = SKILL / "scripts/atlas.py"
spec = importlib.util.spec_from_file_location("atlas_installer", ROOT / "scripts/install_skill.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class CliIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "paper.md").write_text("Mean accuracy is 84.0%.\n", encoding="utf-8")
        (self.root / "runs.csv").write_text("model,accuracy\na,0.80\na,0.84\na,0.88\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return name

    def run_cli(self, *args, cli=CLI):
        r = subprocess.run([sys.executable, str(cli), *map(str,args)], text=True, capture_output=True)
        payload = json.loads(r.stdout or r.stderr)
        return r.returncode, payload

    def number(self, reported="84.0"):
        return {"source":{"path":"runs.csv","format":"csv","where":{"model":"a"}},
                "operation":"mean","field":"accuracy","source_unit":"fraction",
                "reported_unit":"percent","reported":reported,"rounding":{"places":1,"mode":"half_even"}}

    def test_rounding_and_aggregation_cli_success(self):
        self.write("audit.json", {"numeric_claims":[self.number()]})
        code, out = self.run_cli("audit", "--root",self.root,"--spec","audit.json")
        self.assertEqual((code,out["status"]),(0,"verified"))

    def test_mismatch_has_failing_exit(self):
        self.write("audit.json", {"numeric_claims":[self.number("88.0")]})
        code,out = self.run_cli("audit","--root",self.root,"--spec","audit.json")
        self.assertEqual((code,out["status"]),(1,"mismatch"))

    def test_missing_source_has_distinct_exit(self):
        claim = self.number(); claim["source"]["path"]="absent.csv"
        self.write("audit.json", {"numeric_claims":[claim]})
        code,out = self.run_cli("audit","--root",self.root,"--spec","audit.json")
        self.assertEqual((code,out["status"]),(3,"unverified"))

    def test_empty_audit_cannot_silently_pass(self):
        self.write("audit.json", {})
        code,out = self.run_cli("audit","--root",self.root,"--spec","audit.json")
        self.assertEqual((code,out["status"]),(2,"invalid_input"))

    def test_malformed_json_returns_error_record(self):
        (self.root/"broken.json").write_text("{",encoding="utf-8")
        code,out = self.run_cli("audit","--root",self.root,"--spec","broken.json")
        self.assertEqual((code,out["status"]),(2,"invalid_input"))

    def test_nonfinite_json_is_rejected(self):
        (self.root/"nan.json").write_text('{"quotes":[],"x":NaN}',encoding="utf-8")
        code,_ = self.run_cli("audit","--root",self.root,"--spec","nan.json")
        self.assertEqual(code,2)

    def test_duplicate_json_keys_cannot_override_evidence(self):
        (self.root/"duplicate.json").write_text('{"issues":[{}],"issues":[]}',encoding="utf-8")
        code,out = self.run_cli("validate-report","--root",self.root,"--report","duplicate.json")
        self.assertEqual(code,2)
        self.assertIn("Duplicate JSON key",out["error"])

    def test_decimal_literals_preserve_paired_difference(self):
        # Do not json.dumps a Python float: that would lose the digit before the CLI.
        (self.root/"exact.json").write_text('{"paired_runs":[{"left":{"a":9007199254740992.0,"b":9007199254740992.0},"right":{"a":9007199254740993.0,"b":9007199254740993.0}}]}',encoding="utf-8")
        code,out = self.run_cli("audit","--root",self.root,"--spec","exact.json")
        self.assertEqual(code,0)
        self.assertEqual(out["results"][0]["difference"]["mean"],"1")

    def test_reported_decimal_literal_is_not_silently_rounded(self):
        (self.root/"values.json").write_text('[{"value":0.1}]',encoding="utf-8")
        (self.root/"exact.json").write_text('{"numeric_claims":[{"source":{"path":"values.json","format":"json"},"operation":"value","field":"value","reported":0.10000000000000001,"source_unit":"number","reported_unit":"number"}]}',encoding="utf-8")
        code,out = self.run_cli("audit","--root",self.root,"--spec","exact.json")
        self.assertEqual((code,out["status"]),(1,"mismatch"))
        self.assertEqual(out["results"][0]["reported"],"0.10000000000000001")

    def test_manifest_does_not_claim_review(self):
        self.write("manifest.json",{"artifacts":[{"path":"paper.md","role":"manuscript"}]})
        code,out = self.run_cli("preflight","--root",self.root,"--manifest","manifest.json")
        self.assertEqual(code,0)
        self.assertEqual(out["artifacts"][0]["status"],"available_uninspected")

    def test_missing_manifest_artifact_not_passed(self):
        self.write("manifest.json",{"artifacts":[{"path":"figure.png"}]})
        code,out = self.run_cli("preflight","--root",self.root,"--manifest","manifest.json")
        self.assertEqual((code,out["status"]),(3,"unverified"))

    def test_duplicate_manifest_artifacts_rejected(self):
        self.write("manifest.json",{"artifacts":[{"path":"paper.md"},{"path":"paper.md"}]})
        code,_ = self.run_cli("preflight","--root",self.root,"--manifest","manifest.json")
        self.assertEqual(code,2)

    def test_manifest_cannot_escape_root(self):
        self.write("manifest.json",{"artifacts":[{"path":"../outside.txt"}]})
        code,_ = self.run_cli("preflight","--root",self.root,"--manifest","manifest.json")
        self.assertEqual(code,2)

    def test_exact_chinese_quote_is_supported(self):
        (self.root/"中文.md").write_text("结果提高了 4 个百分点。",encoding="utf-8")
        self.write("audit.json",{"quotes":[{"path":"中文.md","quote":"提高了 4 个百分点"}]})
        code,_=self.run_cli("audit","--root",self.root,"--spec","audit.json")
        self.assertEqual(code,0)

    def test_empty_findings_is_valid(self):
        self.write("review.json",{"issues":[],"independence_claim":"none"})
        code,out=self.run_cli("validate-report","--root",self.root,"--report","review.json")
        self.assertEqual((code,out["status"]),(0,"valid"))

    def test_plan_routes_agent_work(self):
        code,out=self.run_cli("plan","--mode","experiments","--language","zh","--domain","agent")
        self.assertEqual(code,0)
        self.assertIn("references/domain-agent.md",out["references"])
        self.assertNotIn("references/bilingual-writing.md",out["references"])

    def test_recheck_open_cannot_return_success(self):
        issue={"id":"PRA-1","status":"confirmed","severity":"major","location":{"path":"paper.md"},
               "evidence":{"quote":"Mean accuracy is 84.0%."},"fix":"Correct mean","acceptance_check":"Recompute from all runs"}
        self.write("packet.json",{"issue":issue,"revision_evidence":{"path":"absent.md","quote":"Corrected"},
                                   "check":{"status":"passed","method":"looks good"}})
        code,out=self.run_cli("recheck","--root",self.root,"--packet","packet.json")
        self.assertNotEqual(code,0)
        self.assertNotEqual(out["status"],"closed")

    def test_recheck_invalid_original_anchor_is_failure_not_missing_evidence(self):
        issue={"id":"PRA-1","status":"confirmed","severity":"major","location":{"path":"paper.md"},
               "evidence":{"quote":"A fabricated original quote."},"fix":"Correct mean","acceptance_check":"Recompute from all runs"}
        self.write("packet.json",{"issue":issue,"revision_evidence":{"path":"paper.md","quote":"Mean accuracy is 84.0%."},
                                   "check":{"status":"passed","method":"looks good"}})
        code,out=self.run_cli("recheck","--root",self.root,"--packet","packet.json")
        self.assertEqual(code,1)
        self.assertEqual(out["validation"]["status"],"invalid")


class InstallerIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.project=self.root/"paper"; self.project.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_installed_skill_self_contained(self):
        result=installer.install(self.project)
        dest=Path(result["path"])
        r=subprocess.run([sys.executable,str(dest/"scripts/atlas.py"),"verify-install"],text=True,capture_output=True,cwd=self.project)
        self.assertEqual(r.returncode,0,r.stderr+r.stdout)
        self.assertEqual(json.loads(r.stdout)["missing"],[])
        self.assertTrue((dest/"assets/review-report.template.md").is_file())

    def test_existing_skill_is_preserved(self):
        result=installer.install(self.project); target=Path(result["path"])
        marker=target/"personal-note.txt"; marker.write_text("keep",encoding="utf-8")
        with self.assertRaises(FileExistsError): installer.install(self.project)
        self.assertEqual(marker.read_text(),"keep")

    def test_replace_creates_backup(self):
        first=installer.install(self.project); old=Path(first["path"])
        (old/"personal-note.txt").write_text("keep",encoding="utf-8")
        result=installer.install(self.project,replace=True)
        self.assertEqual((Path(result["backup"])/"personal-note.txt").read_text(),"keep")
        self.assertFalse((Path(result["path"])/"personal-note.txt").exists())

    def test_backup_is_not_an_active_skill_definition(self):
        installer.install(self.project)
        result=installer.install(self.project,replace=True)
        definitions=list((self.project/".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(definitions),1)
        self.assertFalse(Path(result["backup"]).is_relative_to(self.project/".agents"))

    def test_backup_directory_escape_preserves_active_skill(self):
        result=installer.install(self.project)
        outside=self.root/"outside";outside.mkdir()
        (self.project/".paper-review-atlas-backups").symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError): installer.install(self.project,replace=True)
        self.assertTrue((Path(result["path"])/"SKILL.md").is_file())
        self.assertEqual(list(outside.iterdir()),[])

    def test_install_rejects_escaping_project_directory(self):
        outside=self.root/"outside"; outside.mkdir()
        (self.project/".agents").symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError): installer.install(self.project)
        self.assertEqual(list(outside.iterdir()),[])

    def test_install_rejects_symlink_destination(self):
        target=self.project/".agents/skills"; target.mkdir(parents=True)
        (target/"paper-review-atlas").symlink_to(self.root/"missing",target_is_directory=True)
        with self.assertRaises(ValueError): installer.install(self.project,replace=True)

    def test_install_rejects_source_symlinks(self):
        source=self.root/"source"; source.mkdir()
        (source/"SKILL.md").write_text("test",encoding="utf-8")
        (source/"outside").symlink_to(self.root/"missing")
        with self.assertRaises(ValueError): installer.install(self.project,source=source)

    def test_install_rejects_destination_inside_source(self):
        source=self.root/"source"; source.mkdir()
        (source/"SKILL.md").write_text("test",encoding="utf-8")
        with self.assertRaises(ValueError): installer.install(source,source=source)
        self.assertFalse((source/".agents").exists())


if __name__ == "__main__":
    unittest.main()
