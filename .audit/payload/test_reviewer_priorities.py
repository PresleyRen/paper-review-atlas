"""Actual conditional-policy, package, routing and real-table regression tests."""
import csv
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/paper-review-atlas'
sys.path.insert(0,str(SKILL/'scripts'))
from audit_checks import AuditInputError
from review_extensions import policy, locate
import atlas
CASES=json.loads((ROOT/'tests/fixtures/reviewer-priorities-cases.json').read_text())['cases']

class ReviewerPriorities(unittest.TestCase):
    def test_all_six_new_rules_and_distinct_controls(self):
        self.assertEqual({c['rule'] for c in CASES},{f'CFX{i}' for i in range(17,23)})
        self.assertEqual(len({c['id'] for c in CASES}),len(CASES))
        for rule in {c['rule'] for c in CASES}:
            self.assertGreaterEqual(len({c['expected'] for c in CASES if c['rule']==rule}),2)
    def test_every_required_field_checked(self):
        for case in CASES:
            for key in case['facts']:
                f=dict(case['facts']);f.pop(key)
                with self.subTest(case=case['id'],key=key):
                    with self.assertRaises(AuditInputError):policy(case['rule'],f)
    def test_wrong_types_do_not_become_truthy_evidence(self):
        for case in CASES:
            for key,val in case['facts'].items():
                f=dict(case['facts']);f[key]='true' if type(val) is bool else ([] if type(val) is str else True)
                with self.subTest(case=case['id'],key=key):
                    with self.assertRaises(AuditInputError):policy(case['rule'],f)
    def test_report_count_bounds(self):
        facts=next(c['facts'] for c in CASES if c['rule']=='CFX21')
        for count in (-1,1001,1.5,None):
            with self.assertRaises(AuditInputError):policy('CFX21',{**facts,'reports_raising_concern':count})
    def test_unknown_rule_and_nonobject(self):
        for rule,facts in [(None,{}),('CFX23',{}),('CFX17',[]),('CFX22',None)]:
            with self.assertRaises(AuditInputError):policy(rule,facts)
    def test_full_quick_and_priorities_really_load_protocol(self):
        for mode in ('full','quick','priorities'):
            p=atlas.plan(mode,'zh','agent')
            self.assertIn('references/reviewer-priorities.md',p['references'])
            self.assertIn('references/domain-agent.md',p['references'])
    def test_new_features_and_pending_video_are_locatable(self):
        for query in ('F062','F063','G13'):
            self.assertIn(query,json.dumps(locate(query),ensure_ascii=False))
    def test_no_attribution_to_unread_video(self):
        data=json.loads((SKILL/'config/reviewer-advice.json').read_text())
        video=next(s for s in data['sources'] if s['id']=='ADV00')
        self.assertEqual(video['status'],'pending')
        self.assertEqual(video['attributed_claims'],[])
        self.assertIn('A4JwDjhX-9A',video['url'])
    def test_cli_plan_and_policy_execute(self):
        cli=SKILL/'scripts/atlas.py'
        p=subprocess.run([sys.executable,str(cli),'plan','--mode','priorities'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('reviewer-priorities.md',p.stdout)
        with tempfile.TemporaryDirectory() as d:
            packet=Path(d)/'p.json';packet.write_text(json.dumps({'rule':'CFX17','facts':CASES[0]['facts']}))
            p=subprocess.run([sys.executable,str(cli),'policy','--root',d,'--packet','p.json'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout)['action'],'no_importance_veto')
    def test_portable_install_contains_new_workflow_and_helper(self):
        with tempfile.TemporaryDirectory() as d:
            p=subprocess.run([sys.executable,str(ROOT/'scripts/install_skill.py'),'--project',d],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            installed=Path(d)/'.agents/skills/paper-review-atlas'
            self.assertTrue((installed/'scripts/reviewer_priorities.py').is_file())
            p=subprocess.run([sys.executable,str(installed/'scripts/atlas.py'),'verify-install'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout)['version'],'1.2.0')
    def test_public_react_mixed_result_preserved(self):
        with (ROOT/'tests/fixtures/real_react/table1.csv').open() as f:
            rows={r['method']:r for r in csv.DictReader(f)}
        self.assertEqual(Decimal(rows['ReAct']['hotpot_em'])-Decimal(rows['CoT']['hotpot_em']),Decimal('-2.0'))
        self.assertEqual(Decimal(rows['ReAct']['fever_accuracy'])-Decimal(rows['CoT']['fever_accuracy']),Decimal('4.6'))
        action=policy('CFX20',{'objection_basis':'sota_rank','prior_result_verified':False})['action']
        self.assertEqual(action,'build_contribution_map')
    def test_real_paper_demo_executes_cli_and_records_provenance(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/run_priority_demo.py')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        output=json.loads(p.stdout)
        self.assertEqual(output['react_minus_cot_percentage_points'],{'hotpot_em':'-2.0','fever_accuracy':'4.6'})
        self.assertTrue(output['synthetic_probe']['contradicted_by_hotpot_table'])
        self.assertFalse(output['synthetic_probe']['authored_by_paper'])
        self.assertFalse(output['original_model_experiments_rerun'])
        self.assertEqual(len(output['cli_executions']),4)
    def test_priority_template_has_usable_repair_fields(self):
        template=(SKILL/'assets/priority-report.template.md').read_text()
        for field in ('Evidence pointer','Blocking?','Counterevidence','Minimum repair','Sufficient when'):
            self.assertIn(field,template)
    def test_fixed_comparison_script_runs(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/compare_reviewer_priorities.py')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        result=json.loads(p.stdout)
        self.assertEqual(result['cases'],len(CASES))
        self.assertEqual(result['selected_matches'],len(CASES))
        self.assertFalse(result['upstream_models_executed'])

def make_case(case):
    def test(self):
        result=policy(case['rule'],case['facts'])
        self.assertEqual(result['action'],case['expected'])
        self.assertIn('conditional routing',result['basis'])
        if case['rule']=='CFX21':self.assertFalse(result['statistical_independence_established'])
    return test
for c in CASES:setattr(ReviewerPriorities,'test_'+c['id'],make_case(c))
