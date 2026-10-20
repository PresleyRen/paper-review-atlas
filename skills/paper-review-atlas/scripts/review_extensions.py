"""Source-feature navigation, calibration, and explicit review-policy decisions.

A policy decision checks supplied evidence records. Semantic facts must be
extracted and justified by the reviewer; the function is not a prose classifier.
"""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
from audit_checks import AuditInputError, reconcile_number, recheck_issue, verify_quote

SKILL = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((SKILL / 'config' / (name + '.json')).read_text(encoding='utf-8'))


def locate(query: str) -> dict:
    """Resolve exact IDs first, then search descriptions without recursive fan-out."""
    if not isinstance(query, str) or not query.strip():
        raise AuditInputError('locate needs a nonempty ID or search term')
    q = query.strip().casefold()
    caps = load('capabilities')['capabilities']
    features = load('features')['features']
    gaps = load('gaps')['gaps']
    exact_caps = [c for c in caps if c['id'].casefold() == q]
    exact_features = [f for f in features if f['id'].casefold() == q or f['module'].casefold() == q]
    exact_gaps = [g for g in gaps if g['id'].casefold() == q]
    if exact_caps:
        ids = {c['id'] for c in exact_caps}
        found_features = [f for f in features if set(f['capabilities']) & ids]
        found_gaps = [g for g in gaps if set(g['capabilities']) & ids]
    elif exact_features:
        found_features = exact_features
        ids = {x for f in exact_features for x in f['capabilities']}
        found_gaps = [g for g in gaps if set(g['capabilities']) & ids]
    elif exact_gaps:
        found_gaps = exact_gaps
        ids = {x for g in exact_gaps for x in g['capabilities']}
        found_features = [f for f in features if set(f['capabilities']) & ids]
    else:
        direct = [c for c in caps if q in json.dumps(c, ensure_ascii=False).casefold()]
        found_features = [f for f in features if q in json.dumps(f, ensure_ascii=False).casefold()]
        found_gaps = [g for g in gaps if q in json.dumps(g, ensure_ascii=False).casefold()]
        ids = {c['id'] for c in direct} | {x for f in found_features for x in f['capabilities']} | {x for g in found_gaps for x in g['capabilities']}
    return {'query': query, 'capabilities': [c for c in caps if c['id'] in ids],
            'features': found_features, 'gaps': found_gaps}


def calibrate(records: list[dict]) -> dict:
    """Exact confusion counts on explicitly labeled, uniquely identified items."""
    if not isinstance(records, list) or not records:
        raise AuditInputError('calibration requires labeled records')
    counts = Counter(TP=0, FP=0, TN=0, FN=0)
    seen = set()
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip():
            raise AuditInputError('each calibration record needs a nonempty string id')
        if row['id'] in seen:
            raise AuditInputError('duplicate calibration item: ' + row['id'])
        seen.add(row['id'])
        if type(row.get('gold')) is not bool or type(row.get('predicted')) is not bool:
            raise AuditInputError('gold and predicted must be booleans')
        counts[('T' if row['gold'] == row['predicted'] else 'F') + ('P' if row['predicted'] else 'N')] += 1
    def ratio(a, b):
        return a / b if b else None
    tp, fp, tn, fn = (counts[k] for k in ('TP', 'FP', 'TN', 'FN'))
    return {'n': len(records), **dict(counts), 'precision': ratio(tp, tp+fp),
            'recall': ratio(tp, tp+fn), 'false_positive_rate': ratio(fp, fp+tn),
            'false_negative_rate': ratio(fn, fn+tp), 'unit': 'supplied labeled item'}


def _require(facts, fields):
    if not isinstance(facts, dict):
        raise AuditInputError('policy facts must be an object')
    missing = [x for x in fields if x not in facts]
    if missing:
        raise AuditInputError('missing facts: ' + ', '.join(missing))


def _flag(facts, key):
    value = facts.get(key)
    if type(value) is not bool:
        raise AuditInputError(key + ' must be a boolean')
    return value


def _choice(facts, key, choices):
    value = facts.get(key)
    if not isinstance(value, str) or value not in choices:
        raise AuditInputError(key + ' must be one of ' + ', '.join(sorted(choices)))
    return value


def policy(rule: str, facts: dict, root: Path | None = None) -> dict:
    """Adjudicate one named conflict; fail closed on unspecified decision inputs."""
    if not re.fullmatch(r'CFX(?:0[1-9]|1[0-6])', rule):
        raise AuditInputError('unknown conflict ID')
    if not isinstance(facts, dict):
        raise AuditInputError('facts must be an object')
    result = {'rule': rule, 'basis': 'supplied facts; record check unless an executable check is attached'}
    def decision(action, **extra):
        return {**result, 'action': action, **extra}
    if rule == 'CFX01':
        _require(facts, ['claim'])
        if root is None:
            raise AuditInputError('numeric policy requires --root')
        check = reconcile_number(root, facts['claim'])
        return decision({'verified': 'retain', 'mismatch': 'correct', 'unverified': 'request_source'}[check['status']], check=check)
    if rule == 'CFX02':
        _require(facts, ['supported_issues'])
        items = facts['supported_issues']
        if not isinstance(items, list) or any(not isinstance(i, str) or not i.strip() for i in items):
            raise AuditInputError('supported_issues must be an array of nonempty IDs')
        return decision('report', issue_ids=list(dict.fromkeys(items)))
    if rule == 'CFX03':
        return decision('qualitative_assessment', acceptance_probability=None)
    if rule == 'CFX04':
        _require(facts, ['unit_ids', 'independence_justified'])
        ids = facts['unit_ids']
        if not isinstance(ids, list) or not ids or any(not isinstance(x, str) or not x.strip() for x in ids):
            raise AuditInputError('unit_ids must be nonempty string IDs')
        justified = _flag(facts, 'independence_justified')
        action = 'independent_analysis' if justified and len(set(ids)) == len(ids) else 'group_or_justify'
        return decision(action, observations=len(ids), distinct_units=len(set(ids)))
    if rule == 'CFX05':
        impact = _choice(facts, 'impact', {'scientific', 'meaning', 'style', 'none'})
        mandatory = _flag(facts, 'verified_venue_requirement')
        action = 'scientific_review' if impact == 'scientific' else 'clarify' if impact == 'meaning' else 'format_fix' if mandatory else 'optional_style' if impact == 'style' else 'retain'
        return decision(action)
    if rule == 'CFX06':
        _choice(facts, 'format', {'raster', 'vector'})
        readable = _flag(facts, 'readable')
        compatible = _flag(facts, 'meets_verified_requirement')
        return decision('retain' if readable and compatible else 'repair_readability' if not readable else 'repair_format')
    if rule in {'CFX07', 'CFX14'}:
        _require(facts, ['before', 'after'])
        keys = {'quantities', 'polarity', 'modality', 'causality', 'scope', 'entities', 'comparators'}
        for key in ('before', 'after'):
            if not isinstance(facts[key], dict) or set(facts[key]) != keys:
                raise AuditInputError(key + ' requires all seven semantic inventory fields')
        changed = sorted(k for k in keys if facts['before'][k] != facts['after'][k])
        return decision('retain' if not changed else 'review_scientific_change', changed_fields=changed)
    if rule == 'CFX08':
        study = _choice(facts, 'study', {'clinical_trial', 'observational', 'systematic_review', 'ml_benchmark', 'qualitative', 'theory', 'systems'})
        _require(facts, ['applicable_to'])
        targets = facts['applicable_to']
        if not isinstance(targets, list) or not targets or any(x not in {'clinical_trial', 'observational', 'systematic_review', 'ml_benchmark', 'qualitative', 'theory', 'systems'} if isinstance(x, str) else True for x in targets):
            raise AuditInputError('applicable_to must be nonempty study-type strings')
        return decision('apply' if study in targets else 'not_applicable')
    if rule == 'CFX09':
        _require(facts, ['model_families'])
        families = facts['model_families']
        if not isinstance(families, list) or not families or any(not isinstance(x, str) or not x.strip() for x in families):
            raise AuditInputError('model_families must be nonempty strings')
        families = [x.strip().casefold() for x in families]
        return decision('same_family_views' if len(set(families)) == 1 else 'reported_cross_family_views', independent_error_processes=False)
    if rule == 'CFX10':
        basis = _choice(facts, 'basis', {'missing', 'observed_omission', 'observed_contradiction', 'inference'})
        return decision('request_evidence' if basis in {'missing', 'inference'} else 'report_located_issue', misconduct_established=False)
    if rule == 'CFX11':
        mode = _choice(facts, 'mode', {'review', 'revise', 'submit'})
        if mode == 'submit':
            return decision('submit' if _flag(facts, 'submission_authorized') else 'prepare_only')
        return decision('tracked_edit' if mode == 'revise' else 'suggest_only')
    if rule == 'CFX12':
        viewed = _flag(facts, 'image_viewed')
        data = _flag(facts, 'data_recomputed')
        return decision('visual_record_available' if viewed else 'visual_unassessed', numeric_record='recomputed' if data else 'not_recomputed')
    if rule == 'CFX13':
        level = _choice(facts, 'activity', {'planned', 'static_inspection', 'recomputed', 'reproduced'})
        if level in {'recomputed', 'reproduced'}:
            _require(facts, ['command', 'exit_code', 'output_sha256'])
            if not isinstance(facts['command'], str) or not facts['command'].strip() or type(facts['exit_code']) is not int:
                raise AuditInputError('execution needs a command and integer exit_code')
            if not re.fullmatch(r'[0-9a-f]{64}', str(facts['output_sha256'])):
                raise AuditInputError('execution needs SHA-256 of its output')
            if facts['exit_code'] != 0:
                return decision('execution_failed')
        return decision(level)
    if rule == 'CFX15':
        support = _choice(facts, 'objection_support', {'supported', 'unknown', 'contradicted'})
        response = _choice(facts, 'counterevidence', {'resolves', 'partial', 'none', 'unknown'})
        if support == 'contradicted' or response == 'resolves':
            return decision('withdraw')
        if support == 'unknown' or response == 'unknown':
            return decision('investigate')
        return decision('narrow' if response == 'partial' else 'retain')
    _require(facts, ['issue', 'revision_evidence', 'check'])
    if root is None:
        raise AuditInputError('closure policy requires --root and real artifacts')
    check = recheck_issue(facts['issue'], facts['revision_evidence'], facts['check'], root=root)
    return decision(check['status'], check=check)


def export_macros(root: Path, claims: list[dict]) -> dict:
    """Emit safe LaTeX number macros only after source computations agree."""
    from decimal import Decimal, InvalidOperation
    if not isinstance(claims, list) or not claims:
        raise AuditInputError('macros needs a nonempty claims list')
    lines, checks, seen = [], [], set()
    for item in claims:
        if not isinstance(item, dict) or set(item) != {'name', 'claim'}:
            raise AuditInputError('each macro requires name and claim')
        name = item['name']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z]{1,64}', name) or name in seen:
            raise AuditInputError('macro names must be unique ASCII letters, at most 64')
        # TeX primitives and common control names cannot be replaced.
        if name.lower() in {'input', 'include', 'write', 'read', 'catcode', 'def', 'let', 'newcommand', 'renewcommand', 'end', 'begin', 'csname', 'usepackage', 'documentclass'}:
            raise AuditInputError('reserved macro name')
        seen.add(name)
        check = reconcile_number(root, item['claim'])
        checks.append({'name': name, **check})
        if check['status'] != 'verified':
            continue
        text = str(check.get('rounded_calculated', check['calculated']))
        try:
            number = Decimal(text)
        except InvalidOperation as exc:
            raise AuditInputError('invalid computed number') from exc
        if not number.is_finite() or abs(number.adjusted()) > 1000:
            raise AuditInputError('computed number exceeds export range')
        suffix = r'\%' if check.get('reported_unit') == 'percent' else ''
        lines.append('\\newcommand{\\' + name + '}{' + format(number, 'f') + suffix + '}')
    states = {c['status'] for c in checks}
    status = 'mismatch' if states & {'mismatch', 'invalid'} else 'unverified' if 'unverified' in states else 'verified'
    return {'status': status, 'tex': '\n'.join(lines) + '\n' if status == 'verified' else None,
            'checks': checks, 'scope': 'Computed macros; no manuscript modified'}


def bibliography(root: Path, bib_path: str, citations: list[str], query: str = '') -> dict:
    """Read bounded BibTeX, preserve exact entries and flag missing/duplicate keys.

    This scanner balances delimiters and quoted strings. It does not expand
    @string macros, interpret TeX, resolve crossref, or query a DOI service.
    """
    from audit_checks import resolve_under_root
    path = resolve_under_root(root, bib_path)
    if path.stat().st_size > 5 * 1024 * 1024:
        raise AuditInputError('bibliography exceeds 5 MiB')
    if not isinstance(citations, list) or any(not isinstance(k, str) or not k.strip() for k in citations):
        raise AuditInputError('citations must be string keys')
    if not isinstance(query, str):
        raise AuditInputError('query must be text')
    text = path.read_text(encoding='utf-8')
    entries, i = [], 0
    while i < len(text):
        if text[i] == '%':
            j = text.find('\n', i); i = len(text) if j < 0 else j + 1; continue
        if text[i] != '@':
            i += 1; continue
        match = re.match(r'@([A-Za-z]+)\s*([({])', text[i:])
        if match is None:
            raise AuditInputError('malformed BibTeX entry at offset ' + str(i))
        start = i; typ = match.group(1).lower(); opening = match.group(2)
        endchar = '}' if opening == '{' else ')'
        j = i + match.end(); content_start = j; braces = 0; quoted = False; escaped = False
        while j < len(text):
            char = text[j]
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"' and braces == 0:
                quoted = not quoted
            elif not quoted:
                if char == '{':
                    braces += 1
                elif char == '}' and braces > 0:
                    braces -= 1
                elif char == endchar and braces == 0:
                    break
            j += 1
        if j >= len(text) or quoted:
            raise AuditInputError('unclosed BibTeX entry at offset ' + str(start))
        raw = text[start:j+1]; body = text[content_start:j]
        if typ not in {'comment', 'preamble', 'string'}:
            key, sep, _ = body.partition(',')
            key = key.strip()
            if not sep or not key or re.search(r'\s|[{}(),@]', key):
                raise AuditInputError('invalid citation key at offset ' + str(start))
            entries.append({'key': key, 'type': typ, 'raw': raw, 'line': text.count('\n', 0, start)+1})
        i = j + 1
    counts = Counter(e['key'] for e in entries)
    duplicates = sorted(k for k, n in counts.items() if n > 1)
    missing = sorted(set(citations) - set(counts))
    selected = [e for e in entries if not query or query.casefold() in e['raw'].casefold()]
    return {'status': 'mismatch' if duplicates or missing else 'verified', 'entries': selected,
            'duplicate_keys': duplicates, 'undefined_citations': missing,
            'uncited_keys': sorted(set(counts) - set(citations)),
            'scope': 'Local entry/key checks; uncited shared-library entries are informational'}
