import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from acceptance_gate import GATES, validate


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.write("paper.md", "Synthetic paper fixture; not real research.")
        self.write("report.json", json.dumps({"paper_id": "fixture", "issues": []}))
        self.artifacts = {n: self.digest(n) for n in ("paper.md", "report.json")}
        self.ledger = {"paper_id": "fixture", "version": "v1", "mode": "full", "manuscript": "paper.md", "report": "report.json", "artifacts": self.artifacts, "gates": [
            {"id": gid, "status": "passed", "basis": "synthetic fixture", "check_result": "synthetic record", "evidence": {"paper.md": self.artifacts["paper.md"]}, "issue_ids": []} for gid in sorted(GATES)]}

    def write(self, name, text):
        (self.root / name).write_text(text, encoding="utf-8")

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def result(self):
        self.write("acceptance.json", json.dumps(self.ledger))
        return validate(self.root, "acceptance.json")

    def blocked(self):
        self.assertEqual(self.result()["status"], "blocked")

    def issue(self, status="confirmed", severity="major"):
        self.write("report.json", json.dumps({"paper_id": "fixture", "issues": [{"id": "PRA-001", "status": status, "severity": severity}]}))
        self.artifacts["report.json"] = self.digest("report.json")

    def test_complete(self):
        self.assertEqual(self.result()["status"], "records_current")

    def test_missing_lane(self):
        self.ledger["gates"].pop()
        self.blocked()

    def test_duplicate_lane(self):
        self.ledger["gates"].append(self.ledger["gates"][0])
        self.blocked()

    def test_stale_manuscript(self):
        self.write("paper.md", "edited after review")
        self.blocked()

    def test_missing_evidence(self):
        self.ledger["gates"][0]["evidence"] = {}
        self.blocked()

    def test_unknown_evidence(self):
        self.ledger["gates"][0]["evidence"] = {"fake.md": "unknown"}
        self.blocked()

    def test_blocked_lane(self):
        self.ledger["gates"][0]["status"] = "blocked"
        self.blocked()

    def test_always_required_na(self):
        self.ledger["gates"][0]["status"] = "not_applicable"
        self.blocked()

    def test_other_na(self):
        self.ledger["gates"][9]["status"] = "not_applicable"
        self.assertEqual(self.result()["status"], "records_current")

    def test_unlinked_major_issue(self):
        self.issue()
        self.blocked()

    def test_linked_minor_issue(self):
        self.issue(severity="minor")
        self.ledger["gates"][0]["issue_ids"] = ["PRA-001"]
        self.blocked()

    def test_closed_linked_issue(self):
        self.issue(status="closed")
        self.ledger["gates"][0]["issue_ids"] = ["PRA-001"]
        self.assertEqual(self.result()["status"], "records_current")

    def test_minor_advisory(self):
        self.issue(severity="minor")
        self.assertTrue(self.result()["advisories"])
        self.assertEqual(self.result()["status"], "records_current")

    def test_traversal(self):
        self.artifacts["../escape"] = "bad"
        self.blocked()

    def test_symlink(self):
        (self.root / "alias.md").symlink_to(self.root / "paper.md")
        self.artifacts["alias.md"] = self.artifacts["paper.md"]
        self.blocked()

    def test_duplicate_json_key(self):
        self.write("acceptance.json", '{"paper_id":"a","paper_id":"b"}')
        self.assertEqual(validate(self.root, "acceptance.json")["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
