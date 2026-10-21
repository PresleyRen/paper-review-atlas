"""Apply the reviewed 1.2 source files and registries to the inspected 1.1 base."""
import hashlib,json,subprocess,sys
from pathlib import Path
R=Path.cwd();S=R/'skills/paper-review-atlas';DATE='2026-10-21'
def read(p):return (R/p).read_text(encoding='utf-8')
def write(p,t):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def load(n):return json.loads((S/'config'/f'{n}.json').read_text())
def save(n,d):write('skills/paper-review-atlas/config/'+n+'.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def replace(p,a,b):
 t=read(p)
 if a not in t:raise ValueError('Missing base text: '+p+' '+a[:40])
 write(p,t.replace(a,b))
if 'VERSION = "1.1.0"' not in read('skills/paper-review-atlas/scripts/atlas.py'):raise ValueError('Expected 1.1.0')
for dst in ['docs/validation/real-react-priorities.md','docs/validation/reviewer-priorities-validation.md','scripts/compare_reviewer_priorities.py','scripts/run_priority_demo.py','skills/paper-review-atlas/assets/priority-report.template.md','skills/paper-review-atlas/references/reviewer-priorities.md','skills/paper-review-atlas/scripts/reviewer_priorities.py','tests/test_reviewer_priorities.py']:
 write(dst,read('.audit/payload/'+Path(dst).name))
replace('skills/paper-review-atlas/scripts/atlas.py','VERSION = "1.1.0"','VERSION = "1.2.0"')
for mode in ('full','quick'):replace('skills/paper-review-atlas/scripts/atlas.py','"'+mode+'": ["argument-novelty.md"','"'+mode+'": ["reviewer-priorities.md", "argument-novelty.md"')
replace('skills/paper-review-atlas/scripts/atlas.py','    "guided": [','    "priorities": ["reviewer-priorities.md", "argument-novelty.md", "experiments-statistics.md", "adversarial-review.md", "citations-venues.md"],\n    "guided": [')
replace('skills/paper-review-atlas/scripts/atlas.py','"scripts/review_extensions.py"]','"scripts/review_extensions.py", "scripts/reviewer_priorities.py", "config/reviewer-advice.json"]')
replace('skills/paper-review-atlas/scripts/review_extensions.py',"    if not re.fullmatch(r'CFX(?:0[1-9]|1[0-6])', rule):","    from reviewer_priorities import RULES, policy as priority_policy\n    if isinstance(rule, str) and rule in RULES:\n        return priority_policy(rule, facts)\n    if not isinstance(rule, str) or not re.fullmatch(r'CFX(?:0[1-9]|1[0-6])', rule):")
cases=[]
def case(n,f,e,a):cases.append(dict(id=f'RP{len(cases)+1:03d}',rule='CFX'+str(n),facts=f,expected=e,alternative=a))
for p,v,c,a in [('soundness_only',True,'importance','no_importance_veto'),('importance_selective',True,'importance','assess_venue_fit'),('unknown',False,'importance','retrieve_venue_policy'),('soundness_only',False,'importance','retrieve_venue_policy'),('unknown',True,'importance','retrieve_venue_policy'),('soundness_only',True,'validity','assess_validity'),('importance_selective',True,'validity','assess_validity')]:case(17,dict(profile=p,policy_verified=v,criterion=c),a,'assess_venue_fit' if c=='importance' else 'assess_validity')
for c,e,d,a in [('performance',True,False,'retain_measured_effect'),('mechanism',True,False,'test_mechanism_or_narrow_claim'),('mechanism',True,True,'assess_mechanism_support'),('performance',False,True,'request_effect_evidence'),('mechanism',False,False,'request_effect_evidence'),('performance',True,True,'retain_measured_effect')]:case(18,dict(claim_type=c,effect_supported=e,discriminating_evidence=d),a,'retain_measured_effect' if e else 'request_effect_evidence')
for p,n,a in [('current_claim',False,'minimum_sufficient_test'),('current_claim',True,'test_or_narrow_claim'),('new_scope',False,'optional_extension'),('already_resolved',True,'close_resolved_request'),('unspecified',False,'specify_evidence_gap')]:case(19,dict(request_purpose=p,supported_narrower_claim=n),a,'minimum_sufficient_test')
for b,v,a in [('module_count',False,'build_contribution_map'),('method_name',False,'build_contribution_map'),('sota_rank',False,'build_contribution_map'),('located_prior_result',True,'assess_incremental_contribution'),('located_prior_result',False,'verify_prior_result')]:case(20,dict(objection_basis=b,prior_result_verified=v),a,'novelty_rejection')
for f,i,s,o,c,a in [(False,True,False,'reviewer',2,'freeze_before_synthesis'),(True,True,False,'audit',0,'separate_audit_finding'),(True,False,False,'reviewer',3,'label_shared_context_views'),(True,True,True,'reviewer',3,'label_shared_context_views'),(True,True,False,'reviewer',2,'record_convergent_reports'),(True,True,False,'reviewer',1,'record_nonconsensus_finding'),(True,True,False,'reviewer',0,'record_nonconsensus_finding')]:case(21,dict(reports_frozen=f,contexts_isolated=i,shared_concerns_before_freeze=s,finding_origin=o,reports_raising_concern=c),a,'record_convergent_reports')
for a,c,s,e in [('unavailable',False,'general','pending_source_no_attribution'),('title_only',False,'general','pending_source_no_attribution'),('full_text',True,'venue_specific','use_verified_policy'),('transcript',False,'style_preference','optional_style'),('full_text',False,'general','conditional_review_rule'),('transcript',False,'venue_specific','conditional_review_rule')]:case(22,dict(source_access=a,conflicts_with_verified_policy=c,advice_scope=s),e,'conditional_review_rule')
write('tests/fixtures/reviewer-priorities-cases.json',json.dumps({'scope':'Fixed structured facts, not upstream skill execution or blind LLM evaluation','cases':cases},ensure_ascii=False,indent=2)+'\n')
advice=[
 dict(id='ADV00',title='SCI审稿人自述：我最关注的几个生死点',author='爱玩鱼龟的真叫兽（用户分享署名）',url='https://v.douyin.com/A4JwDjhX-9A/',status='pending',access='user-supplied title; shortlink fetch unsuccessful; transcript unavailable',attributed_claims=[],adoption='No speaker-specific rule added. Obtain transcript/video and timestamp each claim.',gap='G13'),
 dict(id='ADV01',title='How to peer review',author='Matt Might',url='https://matt.might.net/articles/how-to-peer-review/',status='read',access='primary author webpage',adopted=['Record first-pass confusion and revisit later clarification','Give specific, actionable repair rather than only a negative judgment'],not_adopted=['Personal punctuation or scheduling preferences as scientific gates']),
 dict(id='ADV02',title='Review anti-patterns',author='Prem Devanbu',url='https://homes.cs.washington.edu/~mernst/advice/review-antipatterns-devanbu.txt',status='read',access='authored advice reproduced on university site',adopted=['Locate the exact prior result behind a novelty objection','Explain the flaw and what evidence or change would resolve it'],not_adopted=['Treat hosted advice as journal policy']),
 dict(id='ADV03',title='How to write a report',author='Nature',url='https://www.nature.com/nature/for-referees/how-to-write-a-report',status='excerpt_verified',access='primary-site search-index excerpt; full-page open redirected unsuccessfully',adopted=['Validity and significance are distinct assessments','Use technical evidence, methods and appropriate additional tests'],not_adopted=['Generalize Nature importance and readership criteria to all journals']),
 dict(id='ADV04',title='Guide to referees',author='Scientific Reports',url='https://www.nature.com/srep/guide-to-referees',status='excerpt_verified',access='primary-site search-index excerpt; full-page open redirected unsuccessfully',adopted=['Technical validity rather than perceived importance as a selection criterion'],not_adopted=['Drop ethics, originality or validity because the venue is soundness-focused']),
 dict(id='ADV05',title='Guidelines for Reviewers',author='PLOS ONE',url='https://journals.plos.org/plosone/s/reviewer-guidelines',status='read',access='official full webpage',adopted=['Review rigor and supported conclusions rather than perceived importance','Use article-stage criteria for protocols and registered reports'],not_adopted=['Require final results from a study-protocol manuscript'])]
for a in advice:a['checked_on']=DATE
save('reviewer-advice',dict(schema_version=1,as_of=DATE,sources=advice,source_skills=['SRC14','SRC15']))
new_sources=[
 ('SRC14','Yuan1z0825/nature-skills','nature-reviewer','main/skills/nature-reviewer/SKILL.md','04938b9c002d929365a84ddcedff577a39713178',['C02','C04','C18','C27','C28','C36'],['期刊标准分层','重大意见与核心阻断分离','冻结事实包与独立上下文','先冻结后汇总','数值审计与共识分离','保留真实分歧'],'Fixed reviewer counts and punctuation bans omitted; conditional criteria and frozen-report procedure reimplemented.'),
 ('SRC15','M1n-n9/paper-lifecycle','review-revision','master/review-revision/SKILL.md','f871152c34388cb51d4c750057cdb90dbd82b559',['C03','C04','C05','C06','C07','C08','C09','C23','C28'],['贡献类型对应评审','去掉命名后检查增量','问题与可控变量','方法到可检验预测','核心主张对应实验','最小修改与反证'],'No automatic rejection from module count, multiple contributions or non-SOTA results. Reference framework lines 1–150 additionally read; later sections not inspected.')]
sources=load('sources');features=load('features');caps=load('capabilities');walk=json.loads(read('tests/fixtures/feature-walkthrough.json'))
texts=[('三份同上下文审稿没有提出数值矛盾。随后审计发现均值标错，汇总应把该错误写成三位审稿人的共同意见。','将数值矛盾作为审计新增问题，提供重算位置。保留原有报告；同上下文意见按多视角记录，不把后续发现写成既有共识。','汇总分别列出原始审稿意见与审计发现；均值重算可追溯且冻结报告保持不变。'),('该方法用了五个模块，并且一项指标没有达到SOTA，所以没有创新，必须全部重做。','删除按模块数量和单项排名否定创新的结论。先按贡献类型对照最接近工作，定位主张、设置、证据与可保留增量，再提出针对性的实验或表述修订。','每条创新性质疑对应具体已有结果及本文差异；所要求实验解决现有主张的确切证据缺口。')]
for i,(sid,repo,module,path,sha,ids,facets,treatment) in enumerate(new_sources,62):
 url=f'https://github.com/{repo}/blob/{path}';fid=f'F{i:03d}';fc=f'FC{i:03d}'
 sources['sources'].append(dict(id=sid,title=module,repository=repo,url='https://github.com/'+repo,consulted_on=DATE,inspection_level='listed_skill_bodies_reviewed',license_note='License not independently established. Original synthesis only; no upstream prose or code redistributed.',relationship='conceptual_reference_only',copied_code=False,copied_instruction_text=False,skills=[dict(name=module,url=url,inspection_level='skill_body_reviewed',capabilities=ids,treatment=treatment,reviewed_blob_sha=sha,reviewed_on=DATE)],notes=treatment))
 features['features'].append(dict(id=fid,source=sid,module=module,source_url=url,source_blob_sha=sha,facets=facets,capabilities=ids,implementation_locations=['references/reviewer-priorities.md','scripts/reviewer_priorities.py'],complements=[dict(capability='C18',reason='用可追溯数字核对支持科学判断，而不把数值正确等同于结论成立。'),dict(capability='C28',reason='把关键质疑连接到最小修改与实际复核。')],review_case=fc,contract_test='tests/test_feature_contracts.py::FeatureContracts::test_'+fid,verification=dict(mapping='checked',semantic_evaluation='reviewer_walkthrough',independent_benchmark=False),executable_helpers=['policy CFX17–CFX22']))
 t,response,acceptance=texts[i-62];inp=f'tests/fixtures/feature_walkthrough/{fc}.txt';write(inp,t+'\n')
 walk['cases'].append(dict(id=fc,feature=fid,module=module,classification='synthetic_micro_case',input_path=inp,input_sha256=hashlib.sha256((t+'\n').encode()).hexdigest(),review_output=dict(decision='revise',quote=t,line=1,response=response,acceptance_check=acceptance),provenance=dict(reviewer='authoring assistant applying Atlas protocols',context='same development conversation',blind=False)))
 for c in caps['capabilities']:
  if c['id'] in ids:c['sources'].append(sid)
sources['as_of']=DATE;caps['as_of']=DATE;caps['package_version']='1.2.0'
walk['scope']='63 representative same-context cases; deterministic tests verify anchors and routing, not independent semantic accuracy.'
save('sources',sources);save('features',features);write('tests/fixtures/feature-walkthrough.json',json.dumps(walk,ensure_ascii=False,indent=2)+'\n')
rows=[
 (17,'Venue importance versus universal SCI gates','期刊重要性标准与通用SCI门槛',['Apply importance gate to every venue','Use the verified destination criterion'],'Keep scientific validity separate from venue-specific importance; retrieve missing policies.',['C02','C27','C30']),
 (18,'Mechanism identification versus empirical effect','机制识别与经验效果',['A positive score proves the mechanism','Tie evidence demand to the actual claim'],'Retain a measured effect; demand discriminating evidence or narrowing for a mechanism claim.',['C04','C07','C09']),
 (19,'Essential repair versus scope expansion','必要修复与扩展新课题',['Require every proposed experiment','Request the minimum evidence for the current claim'],'Separate required tests, supported narrowing, optional extension and already resolved requests.',['C07','C28','C29']),
 (20,'Novelty evidence versus superficial proxies','创新证据与命名模块排名代理',['Reject from module count or one rank','Compare contribution with located prior results'],'Establish what is new by contribution type and prior-work evidence, not module count, names or rank.',['C03','C05','C06']),
 (21,'Frozen reviews versus manufactured consensus','冻结审稿与事后制造共识',['Rewrite reports after seeing audit','Freeze reports and label origin'],'Keep audit discoveries separate, label shared contexts and preserve genuine disagreement.',['C18','C27','C36']),
 (22,'Accessible advice versus inferred video views','可核验建议与猜测视频观点',['Infer speaker views from the title','Require accessible content before attribution'],'Keep unavailable sources pending; prefer verified applicable policies to conflicting personal advice.',['C01','C02','C36'])]
conflicts=load('conflicts')
for n,en,zh,opts,pol,cs in rows:
 cid=f'CFX{n}';ids=[c['id'] for c in cases if c['rule']==cid]
 conflicts['conflicts'].append(dict(id=cid,topic=en,topic_zh=zh,options=opts,policy=pol,why='The remedy must follow the inspected claim, available evidence and applicable criterion.',capabilities=cs,test_kind='deterministic',verification=dict(state='partial',case_key=cid,expectation='Conditional action must match each fixed correct, adverse and missing-information case.',evidence=['tests/test_reviewer_priorities.py','docs/validation/reviewer-priorities-comparison.json'],note='Executed structured rule tests; scientific adequacy of input facts is reviewed by the host, not authenticated by this helper.',structured_regression=dict(state='passed',cases=ids,report='docs/validation/reviewer-priorities-comparison.json'))))
 for c in caps['capabilities']:
  if c['id'] in cs:
   c['verification']['planned_cases'].append(cid);c['verification']['evidence'].append('docs/validation/reviewer-priorities-validation.md')
   if c['verification']['state']=='not_measured':c['verification'].update(state='partial',annotation='Conditional reviewer-priority rules exercised; complete semantic capability remains unmeasured.')
conflicts['as_of']=DATE;save('conflicts',conflicts);save('capabilities',caps)
gaps=load('gaps');gaps['gaps'].append(dict(id='G13',title='用户分享视频的逐观点核验',status='open',capabilities=['C01','C02','C27','C36'],edit_location='references/reviewer-priorities.md',remedy='取得指定抖音视频或字幕，按时间戳核对原话、适用研究类型和已有规则，补充冲突正反例。',test_command='python -m unittest discover -s tests -p test_reviewer_priorities.py -v',acceptance_check='ADV00包含可读原文或字幕及时间戳；每条归因均有证据并映射至协议、测试与采用状态。'));save('gaps',gaps)
replace('skills/paper-review-atlas/SKILL.md','all 61 inventoried modules to 227 specific facets','all 63 inventoried modules to 239 specific facets')
replace('skills/paper-review-atlas/SKILL.md','| `full` |','| `priorities` | Central case, destination criteria, decisive evidence and minimum sufficient repairs | reviewer-priorities; argument-novelty; experiments-statistics; adversarial-review; citations-venues |\n| `full` |')
replace('skills/paper-review-atlas/SKILL.md','### Capability-specific references','For `full` and `quick`, read [reviewer-priorities.md](references/reviewer-priorities.md) before forming a verdict. Keep scientific support, contribution, venue fit and presentation distinct.\n\n### Capability-specific references')
replace('skills/paper-review-atlas/SKILL.md','- [argument-novelty.md]','- [reviewer-priorities.md](references/reviewer-priorities.md): reviewer decision questions, venue profiles, minimal repairs, first-pass correction and frozen-review synthesis. Advice provenance: [reviewer-advice.json](config/reviewer-advice.json).\n- [argument-novelty.md]')
replace('scripts/build_feature_docs.py',"'The 61 rows account for the declared source inventory;","f'The {len(features)} rows account for the declared source inventory;")
source_doc=['# Reviewer advice and integration / 审稿经验来源','','| ID | Source | Access | Adopted behavior |','|---|---|---|---|']
for a in advice:source_doc.append(f"| {a['id']} | [{a['author']}: {a['title']}]({a['url']}) | {a['access']} | {'; '.join(a.get('adopted',[])) or a['adoption']} |")
source_doc+=['','The two added skill modules are F062 (`nature-reviewer`) and F063 (`review-revision`). Their exact body hashes and capability mappings are in [the feature matrix](FEATURE_MATRIX.md).','','Advice becomes a conditional check only after scope, evidence and a conflict case have been identified. Full official policy takes precedence over personal preferences. ADV00 is not an attribution source until its actual content is available.']
write('docs/REVIEWER_ADVICE.md','\n'.join(source_doc)+'\n')
zh='''## 审稿人关键问题与修改优先级

新增 `priorities` 模式，先找影响论文核心结论的证据缺口，再处理局部表达。全文审查和快速审查会自动加载这一流程。

```text
研究问题 → 实际贡献 → 方法与预测 → 决定性证据
                                 ↓
                        反例、替代解释与成本
                                 ↓
                 科学有效性 / 期刊适配 / 表达清晰度
                                 ↓
                    最小充分修改 → 明确验收条件
```

| 审稿关注点 | 实际作用 |
|---|---|
| 期刊标准 | 区分关注重要性的期刊和侧重科学可靠性的期刊，按目标期刊核验要求 |
| 创新与机制 | 去掉名称看具体贡献；将方法操作、变量、预测与实验连起来 |
| 决定性实验 | 区分效果提升与机制识别，检查预算、基线和替代解释 |
| 修改优先级 | 标出阻碍核心结论的问题，给出重分析、补证据或收窄主张的最小方案 |
| 阅读与图表 | 阅读附录后复核初步质疑，定位主图主表与结论的对应关系 |
| 多视角审查 | 先冻结报告再汇总，将后续数字审计与既有审稿共识分开 |

```text
使用 $paper-review-atlas，priorities 模式审查当前论文。
围绕核心结论列出重要问题、支持和反对证据、最小修改及验收条件。
分别判断科学有效性、贡献增量、期刊适配和表达问题。
```

本轮融合 Matt Might、Prem Devanbu 的审稿经验、期刊官方规则，以及 `nature-reviewer`、`review-revision` 的适用能力。[来源与采用方式](docs/REVIEWER_ADVICE.md) · [真实 ReAct 重点审查示例](docs/validation/real-react-priorities.md)

'''
en='''## Reviewer priorities and minimum sufficient repairs

The new `priorities` mode identifies evidence gaps affecting the central case before polishing local prose. Full and quick reviews load it automatically.

```text
Problem -> contribution -> operation and prediction -> decisive evidence
                                              |
                                  alternatives and quality-cost tradeoffs
                                              |
                         validity / contribution / venue fit / presentation
                                              |
                                minimum repair -> acceptance condition
```

The pass selects verified venue criteria, compares contributions without branding or module-count shortcuts, separates measured effects from mechanism claims, revisits initial concerns after reading supporting material, and produces a claim-specific repair plan. Optional isolated reviews are frozen before synthesis; later numerical audit findings retain their separate provenance.

```text
Use $paper-review-atlas in priorities mode.
Identify central-case concerns, supporting and opposing evidence,
the minimum sufficient repair and an observable acceptance condition.
Separate validity, contribution, venue fit and presentation.
```

The synthesis uses Matt Might and Prem Devanbu's reviewer advice, official journal criteria, and selected `nature-reviewer` and `review-revision` capabilities. [Sources and adoption](docs/REVIEWER_ADVICE.md) · [Real ReAct exercise](docs/validation/real-react-priorities.md)

'''
for lang,section in [('zh',zh),('en',en)]:
 p='docs/templates/README.'+lang+'.md';t=read(p);marker='## 11 种工作模式' if lang=='zh' else '## 11 modes';t=t.replace(marker,section+marker.replace('11','12'))
 if lang=='zh':
  t=t.replace('| `full` / `quick` |','| `priorities` | 核心贡献、决定性证据、期刊标准与最小充分修改 |\n| `full` / `quick` |')
  t=t.replace('16项冲突规则包含舍入、问题配额、统计单位、格式偏好、证据缺失、跨语言保真、多角色来源和修改验收。58个固定输入案例对比两类明确规则：所选规则58项符合预期，对照规则13项符合预期。输入、规则实现和输出都在[测试记录](docs/validation/v1.1-audit.md)中。','22项冲突规则覆盖原有数值、统计、图表、翻译和返修检查，并增加期刊标准、机制证据、最小修复、创新判断、冻结审稿与来源归因。原有58个案例与新增36个案例均有可执行输入和输出，见[本轮测试记录](docs/validation/reviewer-priorities-validation.md)。')
 else:
  t=t.replace('| `full`, `quick` |','| `priorities` | Central case, decisive evidence, venue criteria and minimum repairs |\n| `full`, `quick` |')
  t=t.replace('Sixteen conflicts cover rounding, issue quotas, sampling units, style/format, evidence access, bilingual preservation, reviewer provenance and closure. On 58 fixed structured cases, the selected policies match 58 expected decisions; the explicitly implemented alternatives match 13. Inputs, policy code, comparison method and outputs are in the [audit record](docs/validation/v1.1-audit.md).','Twenty-two conflict policies cover numeric checks, sampling units, evidence access, bilingual preservation, revision closure and the new reviewer-priority decisions. The original 58 fixed cases and 36 new cases have executable inputs and recorded results in the [validation record](docs/validation/reviewer-priorities-validation.md).')
 t=t.replace('CFX01–CFX16','CFX01–CFX22').replace('12个具体后续方向','13个具体后续方向').replace('12 concrete','13 concrete').replace('(docs/validation/v1.1-audit.md)','(docs/validation/reviewer-priorities-validation.md)')
 write(p,t)
write('docs/CLI_REFERENCE.md',read('docs/CLI_REFERENCE.md')+'\n## Reviewer priorities (1.2)\n\n`plan --mode priorities --domain agent --language zh` selects the new pass. Full/quick automatically include it. `policy` now accepts CFX17–CFX22 with the fact schemas demonstrated in `tests/fixtures/reviewer-priorities-cases.json`. `locate F062`, `locate F063` and `locate G13` navigate the two new source integrations and video-source repair task.\n\nReproduce decisions with `python scripts/compare_reviewer_priorities.py`. Policy exit 0 means the input was valid and an action was returned, not that the paper passed review.\n')
write('CHANGELOG.md',read('CHANGELOG.md').replace('# Changelog','# Changelog\n\n## 1.2.0 — 2026-10-21\n\n- Add reviewer priorities to full/quick and a dedicated mode.\n- Integrate two source modules, 12 facets, 6 conflict policies and 36 structured cases.\n- Separate venue fit from validity, effects from mechanisms, and essential repair from scope expansion.\n- Preserve frozen-review provenance and pending attribution for inaccessible advice.\n- Add real ReAct mixed-result review, portable tests and bilingual documentation.'))
ci=read('.github/workflows/ci.yml');ci=ci.replace('      - name: Verify installed runtime footprint','      - name: Replay reviewer-priority policies\n        run: python scripts/compare_reviewer_priorities.py > /tmp/atlas-priorities.json\n      - name: Run public-table priority demo\n        run: python scripts/run_priority_demo.py > /tmp/atlas-priority-demo.json\n      - name: Verify installed runtime footprint');write('.github/workflows/ci.yml',ci)
for script,target in [('compare_reviewer_priorities.py','reviewer-priorities-comparison.json'),('run_priority_demo.py','real-react-priorities-output.json')]:
 out=subprocess.run([sys.executable,'scripts/'+script],capture_output=True,text=True,check=True);write('docs/validation/'+target,out.stdout)
for script in ('build_coverage.py','build_feature_docs.py'):subprocess.run([sys.executable,'scripts/'+script],check=True)
