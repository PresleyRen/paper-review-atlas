#!/usr/bin/env python3
"""Generate bilingual capability text maps, source-feature matrix and gap routes."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/paper-review-atlas'

def read(name):return json.loads((SKILL/'config'/f'{name}.json').read_text(encoding='utf-8'))

def validate():
    caps=read('capabilities')['capabilities']; features=read('features')['features'];gaps=read('gaps')['gaps']
    capids={x['id'] for x in caps}
    sources={(s['id'],m['name']):m for s in read('sources')['sources'] for m in s['skills']}
    seen=set();ids=set();errors=[]
    cases={c['id']:c for c in json.loads((ROOT/'tests/fixtures/feature-walkthrough.json').read_text())['cases']}
    for f in features:
        pair=(f['source'],f['module']);fid=f['id']
        if pair not in sources or pair in seen:errors.append(fid+': unknown/duplicate source module')
        if fid in ids or not re.fullmatch(r'F\d{3,}',fid):errors.append(fid+': invalid/duplicate ID')
        seen.add(pair);ids.add(fid)
        if not set(f['capabilities'])<=capids:errors.append(fid+': unknown capability')
        if not f.get('facets') or len(set(f['facets']))!=len(f['facets']):errors.append(fid+': missing/duplicate facets')
        if not re.fullmatch(r'[0-9a-f]{40}',f['source_blob_sha']):errors.append(fid+': missing source identity')
        for path in f['implementation_locations']:
            resolved=(SKILL/path).resolve()
            if not resolved.is_relative_to(SKILL.resolve()) or not resolved.is_file():errors.append(fid+': invalid implementation path '+path)
        if not f['complements']:errors.append(fid+': missing complementary lane')
        for link in f['complements']:
            if link['capability'] not in capids or not link.get('reason'):errors.append(fid+': incomplete complement')
        c=cases.get(f['review_case'])
        if c is None or c['feature']!=fid:errors.append(fid+': missing representative case')
        else:
            p=(ROOT/c['input_path']).resolve()
            if not p.is_relative_to(ROOT.resolve()) or not p.is_file():errors.append(fid+': missing case input')
            elif hashlib.sha256(p.read_bytes()).hexdigest()!=c['input_sha256']:errors.append(fid+': input hash drift')
        if not (ROOT/f['contract_test'].split('::')[0]).is_file():errors.append(fid+': missing contract test')
    if seen!=set(sources):errors.append('Source inventory and feature matrix differ')
    if set(cases)!={f['review_case'] for f in features}:errors.append('Case and feature ID sets differ')
    if {x['id'] for x in read('guide')['capabilities']}!=capids:errors.append('README guide misses capability IDs')
    for gap in gaps:
        if not set(gap['capabilities'])<=capids:errors.append(gap['id']+': invalid capability')
        if not gap['remedy'] or not gap['acceptance_check'] or not (SKILL/gap['edit_location']).is_file():errors.append(gap['id']+': incomplete repair route')
    return errors

def text_tree(lang='zh'):
    registry=read('capabilities');lines=['Paper Review Atlas']
    for gi,g in enumerate(registry['groups']):
        final=gi==len(registry['groups'])-1;lines.append(('└── ' if final else '├── ')+g['title_'+lang])
        cs=[c for c in registry['capabilities'] if c['group']==g['id']]
        for i,c in enumerate(cs):lines.append(('    ' if final else '│   ')+('└── ' if i==len(cs)-1 else '├── ')+c['id']+' '+c['title_'+lang])
    return '\n'.join(lines)

def table(lang):
    guide={g['id']:g for g in read('guide')['capabilities']};rows=[]
    for c in read('capabilities')['capabilities']:
        link='skills/paper-review-atlas/'+c['protocol']
        rows.append(f"| [{c['id']}]({link}) | {c['title_'+lang]} | {guide[c['id']]['effect_'+lang]} |")
    return '\n'.join(rows)

def outputs():
    features=read('features')['features'];caps={c['id']:c for c in read('capabilities')['capabilities']};gaps=read('gaps')['gaps']
    sources=read('sources')['sources'];facets=sum(len(f['facets']) for f in features)
    outputs={}
    matrix=['# Source-feature integration / 来源特色与互补矩阵','',f'{len(features)} inventoried modules; {facets} named facets. Each row links a source-specific feature to implementation, a representative review case, complementary lanes and development gaps.','',
      'The micro-cases are a same-context developer walkthrough. Regression tests verify their evidence anchors, hashes and routing. They are not an independent measurement of semantic review accuracy. Executable conflict and real-paper arithmetic tests are recorded separately in [the audit report](validation/v1.1-audit.md).','',
      '| ID / Source module | Distinctive facets / 特色 | Implementation | Complement / 弥补点 | Case / test | Open gaps |','|---|---|---|---|---|---|']
    for f in features:
        implementation='<br>'.join(f'[{p.split("/")[-1]}](../skills/paper-review-atlas/{p})' for p in f['implementation_locations'])
        complement='<br>'.join(x['capability']+': '+x['reason'] for x in f['complements'])
        missing=', '.join(g['id'] for g in gaps if set(g['capabilities'])&set(f['capabilities'])) or '—'
        matrix.append(f"| {f['id']} · [{f['module']}]({f['source_url']}) | {'；'.join(f['facets'])} | {implementation} | {complement} | [{f['review_case']}](FEATURE_WALKTHROUGH.md#{f['review_case'].lower()}) / [test](../{f['contract_test'].split('::')[0]}) | {missing} |")
    matrix+=['','## Integration decisions','',
       'Preserve the useful review behavior and author intent; implement workflow equivalents rather than redistribute upstream instructions. Source-specific model backends, scoring engines, external retrieval, renderers and compilers are adapter work identified below. Fixed fault quotas, automatic rejection for punctuation/raster images, invented acceptance odds and provider-required promotional citations are not adopted. All source snapshots have content hashes in the feature register.','',
       f'The {len(features)} rows account for the declared source inventory; they do not claim every optional upstream script was ported. Use the facets, linked protocols and open gaps to identify the next concrete extension.']
    outputs['docs/FEATURE_MATRIX.md']='\n'.join(matrix)+'\n'
    walk=['# Representative source-feature walkthrough / 逐技能特色案例','',
          'Inputs are deliberately small synthetic excerpts. The authoring assistant applied Atlas protocols in the same development conversation and recorded the following decisions. These records preserve concrete reasoning and fixes; tests replay their anchors and route checks, not an independent LLM evaluation.','']
    cases=json.loads((ROOT/'tests/fixtures/feature-walkthrough.json').read_text())['cases']
    for c in cases:
        o=c['review_output'];walk += [f"## {c['id']}",f"**{c['feature']} · {c['module']}**",'',f"Input: `{o['quote']}`",'',f"Decision: **{o['decision']}**",'',o['response'],'','验收 / acceptance: '+o['acceptance_check'],'',f"[Frozen input](../{c['input_path']}) · SHA-256 `{c['input_sha256']}`",'']
    outputs['docs/FEATURE_WALKTHROUGH.md']='\n'.join(walk)+'\n'
    index=['# Extension index / 缺口定位与补强','',
      'Search by capability, module name, feature ID or gap ID. Each open task identifies the actual protocol, the missing implementation, a test entry and a closure criterion.','',
      '```bash','python skills/paper-review-atlas/scripts/atlas.py locate C19','python skills/paper-review-atlas/scripts/atlas.py locate F030','python skills/paper-review-atlas/scripts/atlas.py locate G03','```','',
      '| Gap | Capability IDs | Edit here | Add / implement | Test entry | Close when |','|---|---|---|---|---|---|']
    for g in gaps:index.append(f"| {g['id']} {g['title']} | {', '.join(g['capabilities'])} | [{g['edit_location']}](../skills/paper-review-atlas/{g['edit_location']}) | {g['remedy']} | `{g['test_command']}` | {g['acceptance_check']} |")
    index+=['','## Maintenance sequence','',
       '1. Locate Cxx/Fxxx/Gxx; retain existing IDs. Add a new ID only for a genuinely new capability or source module.','2. Implement the missing protocol/helper/adapter, update the feature facets and reciprocal source mappings.','3. Add an erroneous example, a similar correct control and a missing-evidence case. Exercise actual code or save an actual semantic review, labeling the execution type.','4. Record disagreements and the rule used to resolve them in the conflict register.','5. Run all tests, regenerate both sets of documentation, and commit the inputs and generated outputs together.','',
       '```bash','python scripts/build_coverage.py','python scripts/build_feature_docs.py','python -m unittest discover -s tests -v','python scripts/build_coverage.py --check','python scripts/build_feature_docs.py --check','python scripts/check_package.py','```']
    outputs['docs/EXTENSION_INDEX.md']='\n'.join(index)+'\n'
    outputs['docs/coverage.txt']=text_tree('zh')+'\n\n'+text_tree('en')+'\n'
    for lang,file in [('zh','README.md'),('en','README.en.md')]:
        template=(ROOT/'docs/templates'/('README.'+lang+'.md')).read_text(encoding='utf-8')
        family_rows=[]
        for source in sources:
            family_rows.append(f"| {source['id']} · [{source['repository']}]({source['url']}) | {len(source['skills'])} |")
        for key,val in {'TREE':text_tree(lang),'CAPABILITIES':table(lang),'FAMILIES':'\n'.join(family_rows),'FEATURE_COUNT':str(len(features)),'FACET_COUNT':str(facets),'CAP_COUNT':str(len(caps))}.items():template=template.replace('{{'+key+'}}',val)
        outputs[file]=template
    return outputs

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    problems=validate()
    if problems:
        print('\n'.join(problems));return 1
    stale=[]
    for rel,content in outputs().items():
        path=ROOT/rel
        if a.check:
            if not path.is_file() or path.read_text(encoding='utf-8')!=content:stale.append(rel)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
    if stale:print('Generated feature documentation is stale: '+', '.join(stale));return 1
    print('Feature inventory, repair routes and bilingual text maps: OK');return 0
if __name__=='__main__':raise SystemExit(main())
