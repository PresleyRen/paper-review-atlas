#!/usr/bin/env python3
"""Recompute a real published table and run the priority CLI, without network."""
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/paper-review-atlas/scripts/atlas.py'

def run():
    path=ROOT/'tests/fixtures/real_react/table1.csv'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    expected=json.loads((path.parent/'source.json').read_text())['transcriptions_sha256']['table1.csv']
    if digest != expected: raise ValueError('Published table transcription drift')
    with path.open(encoding='utf-8') as f: rows={r['method']:r for r in csv.DictReader(f)}
    delta={metric:str(Decimal(rows['ReAct'][metric])-Decimal(rows['CoT'][metric]))
           for metric in ('hotpot_em','fever_accuracy')}
    invocations=[]
    def command(args):
        proc=subprocess.run([sys.executable,str(CLI),*args],capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(proc.stderr or proc.stdout)
        output=json.loads(proc.stdout)
        invocations.append({'arguments':args,'exit_code':proc.returncode,'output':output})
        return output
    command(['plan','--mode','priorities','--domain','agent','--language','zh'])
    with tempfile.TemporaryDirectory() as directory:
        for name,rule,facts in [
            ('non-sota','CFX20',{'objection_basis':'sota_rank','prior_result_verified':False}),
            ('missing-video','CFX22',{'source_access':'unavailable','conflicts_with_verified_policy':False,'advice_scope':'general'}),
            ('soundness-venue','CFX17',{'profile':'soundness_only','policy_verified':True,'criterion':'importance'})]:
            filename=name+'.json'
            (Path(directory)/filename).write_text(json.dumps({'rule':rule,'facts':facts}))
            command(['policy','--root',directory,'--packet',filename])
        # Temporary roots are normalized, not used as long-lived evidence paths.
        for item in invocations:
            item['arguments']=[v.replace(directory,'<temporary evidence root>') for v in item['arguments']]
    return {'source':'https://arxiv.org/pdf/2210.03629v3','printed_pages_reinspected':[5,6],
            'table_transcription_sha256':digest,'data_origin':'published aggregate table; not raw experimental runs',
            'react_minus_cot_percentage_points':delta,
            'synthetic_probe':{'text':'ReAct is universally superior to CoT across all tasks.',
                               'authored_by_paper':False,'contradicted_by_hotpot_table':Decimal(delta['hotpot_em'])<0},
            'actual_paper_control':'Section 3.3 explicitly discusses the mixed outcome; retain that discussion.',
            'cli_executions':invocations,'original_model_experiments_rerun':False}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
