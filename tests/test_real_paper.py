"""Published ReAct table calculations; hypothetical error probe is explicitly labeled."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'tests/fixtures/real_react'
sys.path.insert(0,str(ROOT/'skills/paper-review-atlas/scripts'))
from audit_checks import reconcile_number
from review_extensions import export_macros
CLAIMS=json.loads((D/'verified-spec.json').read_text())['numeric_claims']

class RealPaperCalculations(unittest.TestCase):
    def test_transcription_hashes(self):
        source=json.loads((D/'source.json').read_text())
        for path,digest in source['transcriptions_sha256'].items():self.assertEqual(hashlib.sha256((D/path).read_bytes()).hexdigest(),digest)
    def test_invented_relative_percent_error_detected(self):
        c=json.loads((D/'intentional-error-spec.json').read_text())['numeric_claims'][0]
        r=reconcile_number(D,c);self.assertEqual(r['status'],'mismatch');self.assertEqual(r['rounded_calculated'],'32.9')
    def test_corrected_units_export_to_safe_macro(self):
        claim=next(c for c in CLAIMS if c['id']=='webshop-react-vs-act')
        r=export_macros(D,[{'name':'WebShopGainPP','claim':claim}]);self.assertEqual(r['status'],'verified');self.assertIn('{9.9}',r['tex'])
    def test_different_cohorts_not_silently_compared(self):
        source=json.loads((D/'source.json').read_text())
        self.assertTrue(any(x['page']==14 and '500' in x['observation'] for x in source['inspected_objects']))
        # Cohort equivalence is semantic review, so no cross-table mismatch claim is emitted.
        self.assertFalse(any(c['source']['path']=='table5.csv' and 'comparison' in c for c in CLAIMS))
    def test_actual_cli_exit_codes(self):
        cli=ROOT/'skills/paper-review-atlas/scripts/atlas.py'
        for spec,code in [('verified-spec.json',0),('intentional-error-spec.json',1)]:
            r=subprocess.run([sys.executable,str(cli),'audit','--root',str(D),'--spec',spec],capture_output=True,text=True)
            self.assertEqual(r.returncode,code,r.stderr)

def check_claim(c):
    def test(self):
        r=reconcile_number(D,c);self.assertEqual(r['status'],'verified');self.assertEqual(float(r['calculated']),float(c['reported']))
    return test
for c in CLAIMS:setattr(RealPaperCalculations,'test_'+c['id'].replace('-','_'),check_claim(c))
