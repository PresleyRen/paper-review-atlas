#!/usr/bin/env python3
"""Validate the Atlas registries and render their human-readable coverage map.

No network, model calls, third-party libraries, or manuscript data are required.
Registry structure and generated-artifact freshness are tested here; review
quality and the truth of a scientific claim are deliberately not inferred.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

REGISTRY_PATH = Path("skills/paper-review-atlas/config")
SKILL_PATH = Path("skills/paper-review-atlas")
GENERATED_FILES = (
    "docs/CAPABILITY_MAP.md",
    "docs/SOURCES.md",
    "docs/CONFLICTS.md",
    "docs/coverage.svg",
    "docs/coverage.mmd",
)


def load_registry(repo_root: Path) -> dict:
    """Load the three source registries without altering any files."""
    return {
        name: json.loads((repo_root / REGISTRY_PATH / f"{name}.json").read_text(encoding="utf-8"))
        for name in ("capabilities", "sources", "conflicts")
    }


def _duplicates(items: list[str]) -> list[str]:
    return sorted(k for k, count in Counter(items).items() if count > 1)


def _safe_relative_path(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _evidence_errors(evidence: object, repo_root: Path, context: str) -> list[str]:
    """Check concrete evidence references, including optional Python test names.

    Accepted forms: "path/to/file" or "path/to/test.py::Class::test_name", or
    {"path": "...", "test_id": "Class::test_name"}. This checks existence, not
    whether the referenced check passed; actual run results must be recorded.
    """
    errors = []
    if not isinstance(evidence, list):
        return [f"{context}: verification.evidence must be a list"]
    for reference in evidence:
        if isinstance(reference, str):
            bits = reference.split("::")
            value, test_ids = bits[0], bits[1:]
        elif isinstance(reference, dict):
            value = reference.get("path", "")
            test_ids = str(reference.get("test_id", "")).split("::") if reference.get("test_id") else []
        else:
            errors.append(f"{context}: unsupported evidence reference")
            continue
        if not isinstance(value, str) or not _safe_relative_path(value):
            errors.append(f"{context}: unsafe evidence path {value!r}")
            continue
        path = repo_root / value
        try:
            path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            errors.append(f"{context}: evidence escapes repository: {value}")
            continue
        if not path.is_file():
            errors.append(f"{context}: missing evidence file: {value}")
            continue
        if test_ids:
            if path.suffix != ".py":
                errors.append(f"{context}: test_id requires a Python source file: {value}")
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeError) as exc:
                errors.append(f"{context}: cannot parse evidence source {value}: {exc}")
                continue
            nodes = list(tree.body)
            for test_id in test_ids:
                found = next((n for n in nodes if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == test_id), None)
                if found is None:
                    errors.append(f"{context}: missing test symbol {test_id!r} in {value}")
                    break
                nodes = list(found.body)
    return errors


def validate_registry(registry: dict, repo_root: Path, require_protocols: bool = True) -> list[str]:
    """Return actionable consistency errors. Empty does not mean review-valid."""
    errors: list[str] = []
    for name in ("capabilities", "sources", "conflicts"):
        if not isinstance(registry.get(name), dict) or registry[name].get("schema_version") != 1:
            errors.append(f"{name}: expected registry schema_version 1")
    if errors:
        return errors
    cap_doc, source_doc, conflict_doc = (registry[n] for n in ("capabilities", "sources", "conflicts"))
    caps, sources, conflicts = cap_doc.get("capabilities", []), source_doc.get("sources", []), conflict_doc.get("conflicts", [])
    groups = cap_doc.get("groups", [])
    for name, entries in (("capabilities", caps), ("sources", sources), ("conflicts", conflicts), ("groups", groups)):
        if not isinstance(entries, list) or not entries or any(not isinstance(e, dict) for e in entries):
            errors.append(f"{name}: expected a nonempty object list")
            return errors
        identifiers = [e.get("id", "") for e in entries]
        if any(not isinstance(v, str) or not v for v in identifiers):
            errors.append(f"{name}: every entry needs a string id")
            return errors
        for duplicate in _duplicates(identifiers):
            errors.append(f"{name}: duplicate id {duplicate}")
    cap_ids, source_ids, conflict_ids, group_ids = ({e["id"] for e in entries} for entries in (caps, sources, conflicts, groups))
    source_map = {s["id"]: s for s in sources}
    cap_map = {c["id"]: c for c in caps}
    source_capabilities: dict[str, set[str]] = {}
    for source in sources:
        sid = source["id"]
        if source.get("relationship") != "conceptual_reference_only":
            errors.append(f"{sid}: upstream reuse requires a separately reviewed policy")
        if source.get("copied_code") is not False or source.get("copied_instruction_text") is not False:
            errors.append(f"{sid}: source-copy declarations must be explicit false")
        for key in ("title", "repository", "url", "consulted_on", "inspection_level", "license_note"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"{sid}: missing {key}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source.get("consulted_on", "")):
            errors.append(f"{sid}: consulted_on must be ISO date")
        if not source.get("url", "").startswith("https://github.com/"):
            errors.append(f"{sid}: require a primary upstream repository URL")
        modules = source.get("skills", [])
        if not isinstance(modules, list) or not modules:
            errors.append(f"{sid}: missing module inventory")
            continue
        source_capabilities[sid] = set()
        names = [m.get("name", "") for m in modules]
        if _duplicates(names):
            errors.append(f"{sid}: duplicate module names")
        for module in modules:
            label = f"{sid}/{module.get('name', '?')}"
            if module.get("inspection_level") not in ("skill_body_reviewed", "catalog_or_cross_reference_only"):
                errors.append(f"{label}: unknown inspection level")
            if not module.get("url", "").startswith(source.get("url", "") + "/"):
                errors.append(f"{label}: module URL does not belong to repository")
            if not module.get("treatment"):
                errors.append(f"{label}: missing synthesis treatment")
            mapped = module.get("capabilities", [])
            if not isinstance(mapped, list) or not mapped:
                errors.append(f"{label}: module needs an explicit capability mapping")
                continue
            unknown = set(mapped) - cap_ids
            if unknown:
                errors.append(f"{label}: unknown capabilities {sorted(unknown)}")
            source_capabilities[sid].update(mapped)
    for cap in caps:
        cid = cap["id"]
        if not re.fullmatch(r"C\d{2,}", cid):
            errors.append(f"{cid}: invalid capability id")
        for key in ("title_en", "title_zh", "limitations"):
            if not isinstance(cap.get(key), str) or not cap[key].strip():
                errors.append(f"{cid}: missing {key}")
        if cap.get("group") not in group_ids:
            errors.append(f"{cid}: unknown group")
        protocol = cap.get("protocol", "")
        if not isinstance(protocol, str) or not _safe_relative_path(protocol) or not protocol.startswith("references/"):
            errors.append(f"{cid}: unsafe or missing protocol path")
        elif require_protocols:
            protocol_path = repo_root / SKILL_PATH / protocol
            try:
                protocol_path.resolve().relative_to((repo_root / SKILL_PATH).resolve())
                if not protocol_path.is_file():
                    errors.append(f"{cid}: missing protocol {protocol}")
            except ValueError:
                errors.append(f"{cid}: protocol escapes skill root")
        if cap.get("status") not in ("implemented_workflow", "partial_adapter", "planned"):
            errors.append(f"{cid}: unknown implementation status")
        implementation = cap.get("implementation", {})
        if not isinstance(implementation.get("workflow"), bool):
            errors.append(f"{cid}: implementation.workflow must be Boolean")
        for kind in ("deterministic", "adapter"):
            if not isinstance(implementation.get(kind), list) or any(not isinstance(x, str) or not x.strip() for x in implementation.get(kind, [])):
                errors.append(f"{cid}: implementation.{kind} must be a string list")
        if cap.get("status") == "partial_adapter" and not implementation.get("adapter"):
            errors.append(f"{cid}: partial_adapter must state required adapters")
        mapped_sources = cap.get("sources", [])
        if not isinstance(mapped_sources, list):
            errors.append(f"{cid}: sources must be a list")
            mapped_sources = []
        for sid in mapped_sources:
            if sid not in source_ids:
                errors.append(f"{cid}: unknown source {sid}")
            elif cid not in source_capabilities.get(sid, set()):
                errors.append(f"{cid}: {sid} has no module mapped back to this capability")
        verification = cap.get("verification", {})
        if verification.get("state") not in {"not_measured", "planned", "partial", "passed", "failed", "not_run"}:
            errors.append(f"{cid}: unknown verification state")
        if verification.get("state") in {"partial", "passed", "failed"} and not verification.get("evidence"):
            errors.append(f"{cid}: executed verification needs concrete evidence")
        if verification.get("state") == "not_measured" and not verification.get("annotation"):
            errors.append(f"{cid}: unmeasured verification needs a scope annotation")
        unknown_cases = set(verification.get("planned_cases", [])) - conflict_ids
        if unknown_cases:
            errors.append(f"{cid}: unknown planned cases {sorted(unknown_cases)}")
        errors.extend(_evidence_errors(verification.get("evidence", []), repo_root, cid))
    for sid, mapped in source_capabilities.items():
        for cid in mapped & cap_ids:
            if sid not in cap_map[cid].get("sources", []):
                errors.append(f"{sid}: capability {cid} does not map back to this source")
    for conflict in conflicts:
        fid = conflict["id"]
        if not re.fullmatch(r"CFX\d{2,}", fid):
            errors.append(f"{fid}: invalid conflict id")
        for key in ("topic", "topic_zh", "policy", "why"):
            if not conflict.get(key):
                errors.append(f"{fid}: missing {key}")
        if not isinstance(conflict.get("options"), list) or len(conflict.get("options", [])) < 2:
            errors.append(f"{fid}: at least two alternatives are required")
        if conflict.get("test_kind") not in ("deterministic", "forward", "manual"):
            errors.append(f"{fid}: unknown test kind")
        unknown = set(conflict.get("capabilities", [])) - cap_ids
        if unknown:
            errors.append(f"{fid}: unknown capabilities {sorted(unknown)}")
        verification = conflict.get("verification", {})
        if verification.get("case_key") != fid:
            errors.append(f"{fid}: case_key must match stable conflict id")
        if not verification.get("expectation"):
            errors.append(f"{fid}: missing test expectation")
        if verification.get("state") not in ("planned", "passed", "failed", "partial", "not_run"):
            errors.append(f"{fid}: unknown verification state")
        if verification.get("state") in ("passed", "failed", "partial") and not verification.get("evidence"):
            errors.append(f"{fid}: executed verification needs concrete evidence")
        errors.extend(_evidence_errors(verification.get("evidence", []), repo_root, fid))
        for cid in set(conflict.get("capabilities", [])) & cap_ids:
            if fid not in cap_map[cid].get("verification", {}).get("planned_cases", []):
                errors.append(f"{fid}: capability {cid} lacks a reciprocal case mapping")
    for group in groups:
        if not any(cap.get("group") == group["id"] for cap in caps):
            errors.append(f"{group['id']}: empty group")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", group.get("color", "")):
            errors.append(f"{group['id']}: color must be a six-digit hex value")
    return errors


def _md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _link_protocol(path: str) -> str:
    return f"../skills/paper-review-atlas/{path}"


def _scope(cap: dict) -> str:
    labels = ["W" if cap["implementation"]["workflow"] else "planned"]
    if cap["implementation"]["deterministic"]:
        labels.append("D")
    if cap["implementation"]["adapter"]:
        labels.append("A")
    return " / ".join(labels)


def render_capability_markdown(registry: dict) -> str:
    data = registry["capabilities"]
    caps = data["capabilities"]
    lines = [
        "<!-- Generated by scripts/build_coverage.py. Edit config registries, then regenerate. -->",
        "# Capability map / 能力地图", "",
        f"As of {data['as_of']}. {data['coverage_claim']}", "",
        "![Paper Review Atlas coverage](coverage.svg)", "",
        "## Reading this map / 如何阅读", "",
        "- **W — review workflow / 审查协议**: original written instructions are present. This is not an empirical accuracy score.",
        "- **D — deterministic helper / 确定性辅助**: named local checks cover narrow structured inputs; they do not establish semantic correctness.",
        "- **A — external adapter / 外部适配要求**: the review can use the listed evidence/tool when available. The adapter is not bundled or automatically accessible.",
        "- **implemented_workflow** describes written implementation; **partial_adapter** means the format route additionally depends on unbundled parsing/rendering tools. Neither status means all tests passed.",
        "", "能力覆盖数统计的是已登记审查流程，不代表语义审稿正确率。缺失图像、原始数据、外部检索、运行环境或格式工具时，报告必须说明未评估的范围。", "",
        "## Registry / 能力索引", "",
        "| ID | Capability / 能力 | Scope | Protocol | Source families | Verification |",
        "|---|---|---|---|---|---|",
    ]
    for group in data["groups"]:
        for cap in (c for c in caps if c["group"] == group["id"]):
            sources = ", ".join(f"[{sid}](SOURCES.md#{sid.lower()})" for sid in cap["sources"]) or "Original Atlas infrastructure"
            lines.append(f"| {cap['id']} | {_md(cap['title_en'])} / {_md(cap['title_zh'])} | {_scope(cap)} | [{Path(cap['protocol']).stem}]({_link_protocol(cap['protocol'])}) | {sources} | {_md(cap['verification']['state'])} |")
    lines += ["", "## Capability boundaries / 每项能力的边界", ""]
    for cap in caps:
        helpers = ", ".join(f"`{x}`" for x in cap["implementation"]["deterministic"]) or "None; model/human review protocol."
        adapters = "; ".join(cap["implementation"]["adapter"]) or "No additional adapter requirement specified."
        cases = ", ".join(cap["verification"]["planned_cases"]) or "Registry consistency and generation checks."
        lines += [f"### {cap['id']} — {cap['title_en']} / {cap['title_zh']}", "", cap["limitations"], "", f"**Local helpers:** {helpers}", "", f"**External requirements:** {adapters}", "", f"**Conflict cases:** {cases}", "", f"**Verification scope:** {cap['verification']['annotation']}", ""]
        for ref in cap["verification"].get("evidence", []):
            path = ref.split("::")[0] if isinstance(ref, str) else ref["path"]
            label = ref if isinstance(ref, str) else path
            lines.append(f"- [{label}](../{path})")
        if cap["verification"].get("evidence"):
            lines.append("")
    lines += [
        "## Extending the map / 扩展步骤", "",
        "1. Add or extend a protocol under `skills/paper-review-atlas/references/`. State the input evidence, review method, output, limits, and a realistic failure case.",
        "2. Add a stable capability ID to `config/capabilities.json`; do not renumber existing IDs. Choose a group, bilingual titles, protocol path, actual helpers, required adapters and honest verification scope.",
        "3. Map conceptual sources at module level in `config/sources.json`, recording consultation date, inspection depth and license uncertainty. Update reciprocal capability mappings. New original capabilities may have an empty sources list.",
        "4. Add a policy conflict and regression case where behavior could conflict with an existing rule. Record a planned test before execution; attach concrete evidence only after running the test.",
        "5. Run `python scripts/build_coverage.py`, then `python scripts/build_coverage.py --check` and the repository test suite. Commit registries and generated outputs together.",
        "6. Describe remaining blind spots in the README and test report. Record model/version, prompts, inputs and grading method for behavioral evaluations; do not upgrade a workflow to measured effectiveness on a structural test alone.",
        "", "## Open coverage gaps / 明确保留的扩展位置", "",
        "- Validated domain adapters for clinical trials, qualitative studies, geophysics, formal verification and other specialist fields.",
        "- Real PDF/OCR/DOCX/LaTeX/Typst adapters, visual inspection logs and source-data reconciliation.",
        "- Blind bilingual benchmarks with expert-labeled false positives and false negatives; broader languages and discipline-specific terminology.",
        "- Reproducible execution environments, trustworthy independent-review provenance and external bibliographic verification.",
        "- Calibrated review-quality measures across real papers; no claim is made that the current scope guarantees completeness or acceptance.", "",
        "See [source inventory](SOURCES.md), [conflict decisions](CONFLICTS.md), and the machine-readable registries for the exact scope.", "",
    ]
    return "\n".join(lines)


def render_sources_markdown(registry: dict) -> str:
    data = registry["sources"]
    sources = data["sources"]
    total = sum(len(s["skills"]) for s in sources)
    inspected = sum(m["inspection_level"] == "skill_body_reviewed" for s in sources for m in s["skills"])
    lines = [
        "<!-- Generated by scripts/build_coverage.py. Edit sources.json, then regenerate. -->",
        "# Source inventory / 来源与整合范围", "", data["reuse_policy"], "",
        f"**Inventory:** {len(sources)} repositories, {total} named modules. {inspected} module bodies were reviewed; {total - inspected} entries are catalog/cross-reference inventory. Consultation date: {data['as_of']}.", "",
        data.get("inspection_scope", ""), "",
        "本清单记录本次研究范围，不能代表全网所有技能。目录级参考不等于完整读取、移植或测试。Atlas 提供独立编写的能力融合流程；任何上游许可限制不会因本项目的原创实现而改变。", "",
        "The project does not inherit source benchmark scores, calibration, runtime dependencies, model independence or effectiveness claims. URLs identify mutable upstream pages; pin a commit before any future code reuse or license-dependent port.", "",
    ]
    for source in sources:
        lines += [f"## {source['id']}", "", f"### {source['title']}", "", f"**Repository:** [{source['repository']}]({source['url']})", "", f"**License handling:** {source['license_note']}", "", f"**Consulted:** {source['consulted_on']} · **Relationship:** conceptual reference only · **Copied code/instruction text:** no.", "", source.get("review_notes", ""), ""]
        if source.get("related_distribution"):
            lines += [f"Related distribution: {source['related_distribution']}", ""]
        if source.get("additional_inspected_urls"):
            lines += ["Additional inspected reference: " + ", ".join(f"[reference {i + 1}]({url})" for i, url in enumerate(source["additional_inspected_urls"])), ""]
        lines += ["| Module | Inspection depth | Atlas capabilities | Retrieved blob, when recorded | Integration treatment |", "|---|---|---|---|---|"]
        for module in source["skills"]:
            depth = "Body reviewed / 正文已审阅" if module["inspection_level"] == "skill_body_reviewed" else "Catalog/reference only / 仅目录或交叉引用"
            blob = module.get("reviewed_blob_sha", "Not recorded")
            lines.append(f"| [{module['name']}]({module['url']}) | {depth} | {', '.join(module['capabilities'])} | {blob} | {_md(module['treatment'])} |")
        lines.append("")
    return "\n".join(lines)


def render_conflicts_markdown(registry: dict) -> str:
    data = registry["conflicts"]
    lines = [
        "<!-- Generated by scripts/build_coverage.py. Edit conflicts.json, then regenerate. -->",
        "# Conflict resolutions / 冲突裁决与验证", "", data["testing_policy"], "",
        "这里记录的是冲突规则的明确取舍；测试状态以证据条目为准。结构检查、前向合成案例和真实论文盲测不能互相替代。", "",
        "| ID | Conflict | Resolution | Test kind | State |", "|---|---|---|---|---|",
    ]
    for c in data["conflicts"]:
        lines.append(f"| {c['id']} | {_md(c['topic_zh'])} | {_md(c['policy'])} | {c['test_kind']} | {c['verification']['state']} |")
    lines.append("")
    for c in data["conflicts"]:
        v = c["verification"]
        lines += [f"## {c['id']} — {c['topic_zh']}", "", c["topic"], "", "**Alternatives considered:**", ""]
        lines.extend(f"- {option}" for option in c["options"])
        lines += ["", f"**Chosen policy:** {c['policy']}", "", f"**Reason:** {c['why']}", "", f"**Capability links:** {', '.join(c['capabilities'])}", "", f"**Test design ({c['test_kind']}):** {v['expectation']}", "", f"**Verification:** {v['state']}. Stable case key: `{v['case_key']}`.", ""]
        if v.get("evidence"):
            lines += ["**Recorded evidence:**", ""]
            for ref in v["evidence"]:
                if isinstance(ref, str):
                    path = ref.split("::")[0]
                    label = ref
                else:
                    path = ref["path"]
                    label = path + ("::" + ref["test_id"] if ref.get("test_id") else "")
                lines.append(f"- [{label}](../{path})")
            lines.append("")
        else:
            lines += ["No executed-test evidence has been attached to this registry entry yet.", ""]
        if v.get("note"):
            lines += [v["note"], ""]
    return "\n".join(lines)


def render_mermaid(registry: dict) -> str:
    """A three-column coverage grid; no invented scientific dependency arrows."""
    groups = registry["capabilities"]["groups"]
    caps = registry["capabilities"]["capabilities"]
    lines = ["block-beta", "  columns 3"]
    for group in groups:
        ids = ", ".join(c["id"] for c in caps if c["group"] == group["id"])
        label = f"{group['title_en']}: {ids}".replace('"', "'")
        lines.append(f'  {group["id"]}["{label}"]')
    for group in groups:
        lines.append(f"  style {group['id']} fill:#ffffff,stroke:{group['color']},color:#172b43")
    lines.append("")
    return "\n".join(lines)


def render_svg(registry: dict) -> str:
    """Render an exact, expandable grid, not an illustrative generated bitmap."""
    data = registry["capabilities"]
    groups, caps = data["groups"], data["capabilities"]
    sources = registry["sources"]["sources"]
    total_modules = sum(len(s["skills"]) for s in sources)
    width, margin, gap, cols = 1600, 44, 24, 3
    card_width = (width - 2 * margin - (cols - 1) * gap) / cols
    rows = (len(groups) + cols - 1) // cols
    largest_group = max(sum(c["group"] == g["id"] for c in caps) for g in groups)
    card_height = 80 + 45 * largest_group
    start_y, footer = 194, 180
    height = start_y + rows * (card_height + gap) - gap + footer
    esc = lambda value: html.escape(str(value), quote=True)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Paper Review Atlas — capability coverage / 论文审查能力地图</title>',
        f'<desc id="desc">{len(caps)} documented capabilities across {len(groups)} groups, based on a transparent inventory of {len(sources)} repositories and {total_modules} modules. W means written workflow, D means narrow deterministic helper, A means external adapter requirement. Coverage is not measured review accuracy.</desc>',
        '<defs><linearGradient id="header" x1="0" x2="1"><stop offset="0" stop-color="#14243b"/><stop offset="1" stop-color="#243c5c"/></linearGradient></defs>',
        '<style>text{font-family:Inter,"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif}.cap{font-size:17px;font-weight:600;fill:#172b43}.en{font-size:13px;fill:#536379}.badge{font-size:11px;font-weight:700;letter-spacing:.6px}.small{font-size:15px;fill:#52647a}</style>',
        f'<rect width="{width}" height="{height}" fill="#f2f5f9"/>',
        f'<rect width="{width}" height="156" fill="url(#header)"/>',
        '<text x="44" y="51" fill="#a5c9ee" font-size="14" font-weight="700" letter-spacing="3">EVIDENCE · CRITIQUE · REVISION</text>',
        '<text x="44" y="99" fill="#ffffff" font-size="40" font-weight="750">Paper Review Atlas</text>',
        '<text x="484" y="98" fill="#d6e5f5" font-size="27">Capability coverage</text>',
        f'<text x="44" y="132" fill="#d6e5f5" font-size="17">{len(caps)} documented capabilities · {len(groups)} domains · {len(sources)} source repositories · {total_modules} inventoried modules</text>',
        '<text x="44" y="179" class="small">W  Written review workflow     D  Narrow deterministic checks     A  External adapter or evidence required</text>',
    ]
    for index, group in enumerate(groups):
        x = margin + (index % cols) * (card_width + gap)
        y = start_y + (index // cols) * (card_height + gap)
        color = group["color"]
        lines += [f'<rect x="{x:g}" y="{y:g}" width="{card_width:g}" height="{card_height:g}" rx="15" fill="#ffffff" stroke="#dce4ef"/>', f'<rect x="{x:g}" y="{y:g}" width="7" height="{card_height:g}" rx="3" fill="{color}"/>', f'<text x="{x+24:g}" y="{y+32:g}" font-size="21" font-weight="700" fill="{color}">{esc(group["title_en"])}</text>', f'<text x="{x+24:g}" y="{y+54:g}" font-size="14" fill="#62738a">{esc(group["title_zh"])}</text>']
        group_caps = [c for c in caps if c["group"] == group["id"]]
        for item_index, cap in enumerate(group_caps):
            cy = y + 86 + item_index * 45
            lines.append(f'<text x="{x+24:g}" y="{cy:g}" class="cap"><tspan fill="{color}">{cap["id"]}</tspan><tspan dx="10">{esc(cap["title_en"])}</tspan></text>')
            lines.append(f'<text x="{x+67:g}" y="{cy+18:g}" class="en">{esc(cap["title_zh"])}</text>')
            scope = _scope(cap).replace(" / ", " ")
            lines.append(f'<text x="{x+card_width-22:g}" y="{cy:g}" text-anchor="end" class="badge" fill="#536d88">{esc(scope)}</text>')
            state = cap["verification"]["state"]
            state_color = "#9a6700" if state == "partial" else "#64748b"
            lines.append(f'<text x="{x+card_width-22:g}" y="{cy+18:g}" text-anchor="end" font-size="10" fill="{state_color}">{esc(state)}</text>')
    fy = height - footer + 42
    lines += [
        f'<text x="44" y="{fy:g}" font-size="18" font-weight="700" fill="#20364f">Documented review scope, not a measured scientific-review accuracy score.</text>',
        f'<text x="44" y="{fy+28:g}" class="small">Format parsers, visual access, literature search and experimental execution depend on available adapters and evidence.</text>',
        f'<text x="44" y="{fy+55:g}" class="small">Expand: protocol → capability registry → source mapping → conflict case → tests → regenerate this map.</text>',
        f'<text x="44" y="{fy+82:g}" class="small">partial: exercised on limited cases · not_measured: protocol present, behavioral effectiveness not measured.</text>',
        f'<text x="44" y="{fy+109:g}" font-size="13" fill="#708399">Generated from config/capabilities.json, sources.json and conflicts.json · {esc(data["as_of"])} · Source inventory ≠ copied implementations</text>',
        '</svg>', '',
    ]
    return "\n".join(lines)


def render_all(registry: dict) -> dict[str, str]:
    """Return all generated paths and UTF-8 content without writing anything."""
    return {
        "docs/CAPABILITY_MAP.md": render_capability_markdown(registry),
        "docs/SOURCES.md": render_sources_markdown(registry),
        "docs/CONFLICTS.md": render_conflicts_markdown(registry),
        "docs/coverage.svg": render_svg(registry),
        "docs/coverage.mmd": render_mermaid(registry),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="Check freshness without modifying files")
    parser.add_argument("--allow-missing-protocols", action="store_true", help="Bootstrap generation only; never use for release validation")
    args = parser.parse_args(argv)
    try:
        registry = load_registry(args.root)
        errors = validate_registry(registry, args.root, require_protocols=not args.allow_missing_protocols)
    except (OSError, ValueError) as exc:
        print(f"Registry load failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("Registry validation failed:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    rendered = render_all(registry)
    stale = []
    for relative, content in rendered.items():
        target = args.root / relative
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != content:
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    if stale:
        print("Generated coverage files are stale:\n" + "\n".join(f"- {path}" for path in stale), file=sys.stderr)
        return 1
    verb = "Verified" if args.check else "Generated"
    print(f"{verb} {len(rendered)} coverage artifacts. Structural consistency only; no semantic review-effectiveness claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
