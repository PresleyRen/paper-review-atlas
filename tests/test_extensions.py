"""Executable rules and helper behavior; semantic labels are supplied, not inferred."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'skills/paper-review-atlas/scripts'
sys.path.insert(0,str(SCRIPTS))
import review_extensions as ext
from audit_checks import AuditInputError
CASES=json.loads((ROOT/'tests/fixtures/conflicts/cases.json').read_text())['cases']

class ConflictCases(unittest.TestCase):
    def test_all_sixteen_rules_have_positive_and_negative_cases(self):
        self.assertEqual({c['rule'] for c in CASES},{f'CFX{i:02d}' for i in range(1,17)})
        for rule in {c['rule'] for c in CASES}:
            self.assertGreaterEqual(sum(c['rule']==rule for c in CASES),3)
    def test_same_family_case_and_whitespace_not_independent(self):
        self.assertEqual(ext.policy('CFX09',{'model_families':[' family-A ','family-a']})['action'],'same_family_views')
    def test_invalid_policy_facts_rejected(self):
        for rule,facts in [('CFX04',{'unit_ids':[],'independence_justified':True}),('CFX04',{'unit_ids':['x'],'independence_justified':'yes'}),('CFX05',{'impact':[],'verified_venue_requirement':False}),('CFX08',{'study':'ml_benchmark','applicable_to':['invalid']}),('CFX09',{'model_families':[]}),('CFX13',{'activity':'reproduced'}),('CFX07',{'before':{},'after':{}}),('CFX99',{})]:
            with self.subTest(rule=rule),self.assertRaises(AuditInputError): ext.policy(rule,facts)
    def test_comparison_replays_distinct_rules_not_upstream_models(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from compare_policies import run
        result=run()
        self.assertFalse(result['upstream_models_executed'])
        self.assertEqual(result['selected_matches'],len(CASES))
        self.assertLess(result['alternative_matches'],result['selected_matches'])

# Each policy fixture is an individual test with its rule ID in the test name.
def policy_case(case):
    def test(self):
        facts=copy.deepcopy(case['facts'])
        result=ext.policy(case['rule'],facts,ROOT/'tests/fixtures/conflicts')
        self.assertEqual(result['action'],case['expected'],case['rationale'])
        self.assertEqual(facts,case['facts'])
        if case['rule']=='CFX02': self.assertEqual(result['issue_ids'],list(dict.fromkeys(facts['supported_issues'])))
        if case['rule']=='CFX09': self.assertFalse(result['independent_error_processes'])
        if case['rule']=='CFX10': self.assertFalse(result['misconduct_established'])
        if case['rule']=='CFX12': self.assertEqual(result['numeric_record'],'recomputed' if facts['data_recomputed'] else 'not_recomputed')
    return test
for c in CASES: setattr(ConflictCases,'test_'+c['id'].replace('-','_'),policy_case(c))

class NewHelpers(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def write(self,name,text):
        (self.root/name).write_text(text,encoding='utf-8');return name
    def test_calibration_counts(self):
        rows=[{'id':str(i),'gold':g,'predicted':p} for i,(g,p) in enumerate([(True,True),(True,False),(False,True),(False,False)])]
        r=ext.calibrate(rows); self.assertEqual([r[k] for k in ['TP','FN','FP','TN']],[1,1,1,1]);self.assertEqual(r['precision'],.5);self.assertEqual(r['recall'],.5)
    def test_calibration_zero_denominators(self):
        r=ext.calibrate([{'id':'a','gold':False,'predicted':False}]);self.assertIsNone(r['recall']);self.assertIsNone(r['precision']);self.assertEqual(r['false_positive_rate'],0)
    def test_calibration_duplicate_and_nonboolean_rejected(self):
        for rows in [[],[{'id':'x','gold':1,'predicted':True}],[{'id':'x','gold':True,'predicted':True}]*2]:
            with self.assertRaises(AuditInputError):ext.calibrate(rows)
    def test_locate_capability_and_feature(self):
        for query in ['C19','F030','academic-paper-reviewer','图表']:
            r=ext.locate(query);self.assertTrue(r['capabilities']);self.assertTrue(r['features'])
        self.assertEqual([c['id'] for c in ext.locate('C19')['capabilities']], ['C19'])
        self.assertEqual([f['id'] for f in ext.locate('F030')['features']], ['F030'])
        self.assertEqual([f['module'] for f in ext.locate('academic-paper-reviewer')['features']], ['academic-paper-reviewer'])
        self.assertEqual([g['id'] for g in ext.locate('G03')['gaps']], ['G03'])
    def test_locate_gap_returns_repair_and_capabilities(self):
        r=ext.locate('G03');self.assertIn('G03',[g['id'] for g in r['gaps']]);self.assertIn('C11',[c['id'] for c in r['capabilities']])
    def test_locate_empty_rejected_and_unknown_not_invented(self):
        with self.assertRaises(AuditInputError):ext.locate(' ')
        r=ext.locate('definitely-absent-xyz');self.assertEqual(r['capabilities'],[]);self.assertEqual(r['gaps'],[])
    def macro_claim(self,reported='84'):
        self.write('runs.csv','value\n0.80\n0.84\n0.88\n')
        return {'source':{'path':'runs.csv','format':'csv'},'operation':'mean','field':'value','reported':reported,'source_unit':'fraction','reported_unit':'percent'}
    def test_macro_computed_mean_not_best_seed(self):
        r=ext.export_macros(self.root,[{'name':'MeanScore','claim':self.macro_claim()}]);self.assertEqual(r['status'],'verified');self.assertEqual(r['tex'],'\\newcommand{\\MeanScore}{84\\%}\n')
    def test_macro_failure_suppresses_all_output(self):
        good={'name':'A','claim':self.macro_claim()};bad={'name':'B','claim':self.macro_claim('88')}
        r=ext.export_macros(self.root,[good,bad]);self.assertEqual(r['status'],'mismatch');self.assertIsNone(r['tex'])
    def test_macro_injection_and_duplicate_rejected(self):
        for name in ['input','x}\\input{secret}','A1','中']:
            with self.subTest(name=name),self.assertRaises(AuditInputError):ext.export_macros(self.root,[{'name':name,'claim':self.macro_claim()}])
        item={'name':'Safe','claim':self.macro_claim()}
        with self.assertRaises(AuditInputError):ext.export_macros(self.root,[item,item])
    def test_macro_missing_source_unverified(self):
        c=self.macro_claim();c['source']['path']='missing.csv'
        self.assertEqual(ext.export_macros(self.root,[{'name':'A','claim':c}])['status'],'unverified')
    def test_bib_nested_braces_and_raw_preservation(self):
        raw='@article{a, title={{Agent {Memory}}}, author={X}, year={2024}}'
        self.write('x.bib',raw+'\n@book{b, title="Shared library"}\n')
        r=ext.bibliography(self.root,'x.bib',['a'],'memory');self.assertEqual(r['status'],'verified');self.assertEqual(r['entries'][0]['raw'],raw);self.assertEqual(r['uncited_keys'],['b'])
    def test_bib_quoted_delimiters_and_parentheses(self):
        raw='@article(a, title="literal } ) { and \\"quote\\"", year={2024})'
        self.write('x.bib',raw);r=ext.bibliography(self.root,'x.bib',['a']);self.assertEqual(r['entries'][0]['raw'],raw)
    def test_bib_comments_and_macros_not_entries(self):
        self.write('x.bib','% @article{fake, title={X}}\n@string{v="venue"}\n@preamble{"x"}\n@comment{ignored}\n@article{real,title={Hello},journal=v}')
        r=ext.bibliography(self.root,'x.bib',['real']);self.assertEqual([e['key'] for e in r['entries']],['real'])
    def test_bib_duplicate_and_undefined_are_errors(self):
        self.write('x.bib','@article{a,title={One}}\n@book{a,title={Two}}')
        r=ext.bibliography(self.root,'x.bib',['missing']);self.assertEqual(r['status'],'mismatch');self.assertEqual(r['duplicate_keys'],['a']);self.assertEqual(r['undefined_citations'],['missing'])
    def test_bib_malformed_not_silently_skipped(self):
        for text in ['@article{a,title={unfinished}','@article{oops}','@?{x}']:
            self.write('x.bib',text)
            with self.subTest(text=text),self.assertRaises(AuditInputError):ext.bibliography(self.root,'x.bib',[])
    def test_bib_root_boundary(self):
        with self.assertRaises(AuditInputError):ext.bibliography(self.root,'../outside.bib',[])
    def test_installed_commands_actual_subprocess(self):
        self.write('cal.json',json.dumps({'records':[{'id':'1','gold':False,'predicted':False}]}))
        commands=[['plan','--mode','guided'],['plan','--mode','calibration'],['locate','G03'],['calibrate','--root',str(self.root),'--packet','cal.json']]
        for command in commands:
            r=subprocess.run([sys.executable,str(SCRIPTS/'atlas.py'),*command],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr);self.assertIsInstance(json.loads(r.stdout),dict)
    def test_cli_policy_missing_input_rejected(self):
        self.write('policy.json',json.dumps({'rule':'CFX12','facts':{}}))
        r=subprocess.run([sys.executable,str(SCRIPTS/'atlas.py'),'policy','--root',str(self.root),'--packet','policy.json'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
    def test_cli_macros_and_bib_real_files(self):
        self.write('macro.json',json.dumps({'claims':[{'name':'Mean','claim':self.macro_claim()}]}))
        self.write('x.bib','@article{a,title={Agent}}');self.write('bib.json',json.dumps({'bib_path':'x.bib','citations':['a']}))
        for cmd,packet in [('export-macros','macro.json'),('bib-audit','bib.json')]:
            r=subprocess.run([sys.executable,str(SCRIPTS/'atlas.py'),cmd,'--root',str(self.root),'--packet',packet],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['status'],'verified')

if __name__=='__main__':unittest.main()
