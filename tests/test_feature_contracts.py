"""Module-by-module traceability checks, not a semantic review benchmark."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/paper-review-atlas'
sys.path.insert(0,str(SKILL/'scripts'))
from audit_checks import verify_quote,validate_issue
spec=importlib.util.spec_from_file_location('feature_docs',ROOT/'scripts/build_feature_docs.py')
DOC=importlib.util.module_from_spec(spec);spec.loader.exec_module(DOC)
FEATURES=json.loads((SKILL/'config/features.json').read_text())['features']
CASES={c['id']:c for c in json.loads((ROOT/'tests/fixtures/feature-walkthrough.json').read_text())['cases']}

class FeatureContracts(unittest.TestCase):
    def test_source_inventory_exactly_matches_features(self):
        self.assertEqual(DOC.validate(),[])
        src=json.loads((SKILL/'config/sources.json').read_text())['sources']
        self.assertEqual({(s['id'],m['name']) for s in src for m in s['skills']},{(f['source'],f['module']) for f in FEATURES})
    def test_generated_docs_current(self):
        for name,expected in DOC.outputs().items():
            self.assertEqual((ROOT/name).read_text(encoding='utf-8'),expected,name)
    def test_bilingual_readmes_include_every_capability(self):
        caps=DOC.read('capabilities')['capabilities']
        for lang,path in [('zh','README.md'),('en','README.en.md')]:
            text=(ROOT/path).read_text()
            for c in caps:
                self.assertIn(c['id']+' '+c['title_'+lang],text)
                self.assertIn('['+c['id']+'](',text)
            self.assertIn('```text',text);self.assertIn('locate G03',text)
    def test_new_capability_propagates_without_diagram_template_edit(self):
        original=DOC.read
        registry=copy.deepcopy(original('capabilities'))
        c=copy.deepcopy(registry['capabilities'][-1]);c.update(id='C37',title_zh='新能力',title_en='New capability')
        registry['capabilities'].append(c)
        def custom(name):return registry if name=='capabilities' else original(name)
        with patch.object(DOC,'read',side_effect=custom):
            self.assertIn('C37 新能力',DOC.text_tree('zh'));self.assertIn('C37 New capability',DOC.text_tree('en'))
    def test_gap_routes_have_test_files_and_closure(self):
        for g in DOC.read('gaps')['gaps']:
            self.assertTrue((SKILL/g['edit_location']).is_file())
            self.assertGreater(len(g['acceptance_check']),10)
            filename=g['test_command'].split('-p ')[1].split()[0]
            self.assertTrue((ROOT/'tests'/filename).is_file())
    def test_missing_or_duplicate_feature_mapping_is_detected(self):
        original=DOC.read
        for mode in ['missing','duplicate']:
            features=copy.deepcopy(original('features'))
            if mode=='missing':features['features'].pop()
            else:features['features'].append(features['features'][0])
            with patch.object(DOC,'read',side_effect=lambda name:features if name=='features' else original(name)):
                self.assertTrue(DOC.validate())
    def test_unrecognized_implementation_path_is_detected(self):
        original=DOC.read;features=copy.deepcopy(original('features'));features['features'][0]['implementation_locations']=['../outside.md']
        with patch.object(DOC,'read',side_effect=lambda name:features if name=='features' else original(name)):
            self.assertTrue(any('invalid implementation path' in e for e in DOC.validate()))

def feature_test(feature):
    def test(self):
        c=CASES[feature['review_case']];o=c['review_output'];p=ROOT/c['input_path']
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),c['input_sha256'])
        self.assertEqual(verify_quote(ROOT,c['input_path'],o['quote'],o['line'])['status'],'verified')
        self.assertFalse(c['provenance']['blind'])
        self.assertTrue(feature['complements'])
        if o['decision']=='revise':
            issue={'id':c['id'],'status':'confirmed','severity':'minor',
                   'location':{'path':c['input_path'],'line':1},'evidence':{'quote':o['quote']},
                   'fix':o['response'],'acceptance_check':o['acceptance_check']}
            self.assertEqual(validate_issue(issue,ROOT)['status'],'valid')
        self.assertGreater(len(o['response']),10)
        self.assertGreater(len(o['acceptance_check']),10)
    return test
for f in FEATURES:setattr(FeatureContracts,'test_'+f['id'],feature_test(f))
