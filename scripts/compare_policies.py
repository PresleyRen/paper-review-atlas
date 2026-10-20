#!/usr/bin/env python3
"""Run declared conflict alternatives on the same fixed evidence records."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/paper-review-atlas/scripts'))
from review_extensions import policy

def baseline(case):
    """Explicit operationalizations of rejected rules, not upstream model runs."""
    rule,f=case['rule'],case['facts']
    if rule=='CFX01':
        # Candidate: treat any raw-vs-display difference as an error.
        from audit_checks import reconcile_number
        c=dict(f['claim']);c.pop('rounding',None)
        r=reconcile_number(ROOT/'tests/fixtures/conflicts',c)
        return {'verified':'retain','mismatch':'correct','unverified':'request_source'}[r['status']]
    return {'CFX02':'fill_quota','CFX03':'numerical_probability','CFX04':'independent_analysis',
            'CFX05':'major_style_error','CFX06':'repair_format' if f.get('format')=='raster' else 'retain',
            'CFX07':'retain','CFX08':'apply','CFX09':'independent_review',
            'CFX10':'confirmed_misconduct','CFX11':'tracked_edit',
            'CFX12':'visual_record_available','CFX13':'reproduced',
            'CFX14':'retain','CFX15':'retain','CFX16':'closed'}[rule]

def run():
    root=ROOT/'tests/fixtures/conflicts'
    cases=json.loads((root/'cases.json').read_text())['cases']
    results=[]
    for c in cases:
        selected=policy(c['rule'],c['facts'],root)
        before=baseline(c)
        results.append({'id':c['id'],'expected':c['expected'],'alternative':before,
                        'selected':selected,'alternative_matches':before==c['expected'],
                        'selected_matches':selected['action']==c['expected']})
    return {'kind':'deterministic policy comparison on supplied facts',
            'upstream_models_executed':False,'cases':len(results),
            'alternative_matches':sum(x['alternative_matches'] for x in results),
            'selected_matches':sum(x['selected_matches'] for x in results),'results':results}

if __name__=='__main__':
    r=run();print(json.dumps(r,ensure_ascii=False,indent=2))
    raise SystemExit(0 if r['selected_matches']==r['cases'] else 1)
