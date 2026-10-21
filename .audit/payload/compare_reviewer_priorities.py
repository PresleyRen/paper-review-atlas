#!/usr/bin/env python3
"""Replay explicit reviewer-priority alternatives against the same fixed cases."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/paper-review-atlas/scripts'))
from review_extensions import policy

def run():
    cases=json.loads((ROOT/'tests/fixtures/reviewer-priorities-cases.json').read_text())['cases']
    if not cases: raise ValueError('No cases')
    results=[]
    for c in cases:
        actual=policy(c['rule'],c['facts'])
        results.append({**c,'selected':actual,'selected_matches':actual['action']==c['expected'],
                        'alternative_matches':c['alternative']==c['expected']})
    return {'kind':'structured policy regression; author-defined cases and comparator',
            'upstream_models_executed':False,'cases':len(results),
            'selected_matches':sum(r['selected_matches'] for r in results),
            'alternative_matches':sum(r['alternative_matches'] for r in results),'results':results}
if __name__=='__main__':
    result=run();print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['selected_matches']==result['cases'] else 1)
