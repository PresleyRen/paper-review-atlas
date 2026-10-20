#!/usr/bin/env python3
"""Paper Review Atlas: bounded evidence checks, without network or code execution."""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

from audit_checks import (AuditInputError, paired_run_stats, reconcile_number,
                         recheck_issue, resolve_under_root, validate_report, verify_quote)

from review_extensions import locate, calibrate, policy, export_macros, bibliography

SKILL_ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
MAX_JSON_BYTES = 4 * 1024 * 1024
CORE = ["review-contract.md", "input-output.md"]
ROUTES = {
    "full": ["argument-novelty.md", "experiments-statistics.md", "figures-tables.md", "code-reproducibility.md", "bilingual-writing.md", "citations-venues.md", "formal-theory.md", "adversarial-review.md", "revision-rebuttal.md"],
    "quick": ["argument-novelty.md", "experiments-statistics.md", "adversarial-review.md"],
    "experiments": ["experiments-statistics.md", "code-reproducibility.md"],
    "figures": ["figures-tables.md", "code-reproducibility.md"],
    "writing": ["bilingual-writing.md", "argument-novelty.md"],
    "revise": ["revision-rebuttal.md", "bilingual-writing.md"],
    "rereview": ["revision-rebuttal.md"],
    "rebuttal": ["revision-rebuttal.md", "adversarial-review.md"],
    "guided": ["guided-calibration.md", "argument-novelty.md"],
    "calibration": ["guided-calibration.md", "adversarial-review.md"],
    "submission": ["citations-venues.md", "input-output.md"],
}


def read_json(path: Path):
    if path.stat().st_size > MAX_JSON_BYTES:
        raise AuditInputError("JSON exceeds 4 MiB limit")
    def reject_constant(value):
        raise AuditInputError("Non-finite JSON number: " + value)
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise AuditInputError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal,
                      parse_constant=reject_constant, object_pairs_hook=unique_object)


def object_json(root, relpath):
    data = read_json(resolve_under_root(root, relpath))
    if not isinstance(data, dict):
        raise AuditInputError("Expected a JSON object")
    return data


def list_value(data, key):
    value = data.get(key, [])
    if not isinstance(value, list):
        raise AuditInputError(f"{key} must be an array")
    return value


def plan(mode, language, domain):
    refs = list(dict.fromkeys(CORE + ROUTES[mode]))
    if domain == "agent":
        refs.append("domain-agent.md")
    return {"mode": mode, "language": language, "domain": domain,
            "references": ["references/" + x for x in refs],
            "scope": "Review plan only; no manuscript inspected by this command.",
            "required_outputs": ["scope and evidence ledger", "claim-evidence map", "anchored findings", "actionable revisions", "acceptance checks", "unverified areas"]}


def preflight(root, manifest_path):
    manifest = object_json(root, manifest_path)
    items = list_value(manifest, "artifacts")
    if not items:
        raise AuditInputError("artifacts must contain at least one input")
    out, seen = [], set()
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise AuditInputError("Each artifact needs a string path")
        path = resolve_under_root(root, item["path"], must_exist=False)
        if item["path"] in seen:
            raise AuditInputError("Duplicate artifact path: " + item["path"])
        seen.add(item["path"])
        exists = path.is_file()
        out.append({"path": item["path"], "role": item.get("role", "unspecified"),
                    "available": exists, "status": "available_uninspected" if exists else "unverified",
                    "bytes": path.stat().st_size if exists else None,
                    "format": path.suffix.lower().lstrip(".")})
    return {"status": "ready" if all(x["available"] for x in out) else "unverified",
            "scope": "Declared-file availability only; no scientific or visual verification.",
            "artifacts": out}


def audit(root, spec_path):
    spec = object_json(root, spec_path)
    results = []
    for item in list_value(spec, "quotes"):
        if not isinstance(item, dict) or "path" not in item or "quote" not in item:
            raise AuditInputError("Each quote needs path and quote")
        results.append({"kind": "quote", "id": item.get("id"),
                        **verify_quote(root, item["path"], item["quote"], item.get("line"))})
    for item in list_value(spec, "numeric_claims"):
        if not isinstance(item, dict):
            raise AuditInputError("Each numeric claim must be an object")
        results.append({"kind": "number", "id": item.get("id"), **reconcile_number(root, item)})
    for item in list_value(spec, "paired_runs"):
        if not isinstance(item, dict) or "left" not in item or "right" not in item:
            raise AuditInputError("Each paired summary needs left and right mappings")
        results.append({"kind": "paired_descriptive", "id": item.get("id"),
                        **paired_run_stats(item["left"], item["right"])})
    if not results:
        raise AuditInputError("No checks declared; an empty audit cannot pass")
    statuses = {x.get("status") for x in results}
    status = "mismatch" if statuses & {"mismatch", "invalid"} else "unverified" if "unverified" in statuses else "verified"
    return {"status": status,
            "scope": "Declared anchors and computations only; source selection and scientific validity require review.",
            "results": results}


def verify_install():
    required = ["SKILL.md", "agents/openai.yaml", "scripts/audit_checks.py", "scripts/review_extensions.py"]
    required += ["references/" + x for x in set(CORE + sum(ROUTES.values(), []) + ["domain-agent.md"])]
    required += ["config/" + x + ".json" for x in ("capabilities", "sources", "conflicts", "features", "gaps")]
    missing = [x for x in sorted(required) if not (SKILL_ROOT / x).is_file()]
    return {"status": "invalid" if missing else "valid", "version": VERSION,
            "scope": "Installed files and JSON readability, not scientific review accuracy.",
            "missing": missing,
            "registries": {x: len(read_json(SKILL_ROOT / "config" / (x + ".json")).get(x, [])) for x in ("capabilities", "sources", "conflicts", "features", "gaps") if (SKILL_ROOT / "config" / (x + ".json")).is_file()}}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities", help="Print the capability registry")
    sub.add_parser("verify-install", help="Check the installed footprint")
    find = sub.add_parser("locate", help="Find capability, source feature, gap and repair entry")
    find.add_argument("query")
    route = sub.add_parser("plan", help="List relevant review references")
    route.add_argument("--mode", choices=list(ROUTES), default="full")
    route.add_argument("--language", choices=["auto", "zh", "en"], default="auto")
    route.add_argument("--domain", choices=["general", "agent"], default="general")
    for name, arg in (("preflight", "manifest"), ("audit", "spec"), ("validate-report", "report"), ("recheck", "packet"), ("policy", "packet"), ("calibrate", "packet"), ("export-macros", "packet"), ("bib-audit", "packet")):
        sp = sub.add_parser(name)
        sp.add_argument("--root", required=True, type=Path, help="Authorized evidence directory")
        sp.add_argument("--" + arg, required=True, help="JSON path relative to --root")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "capabilities":
            result = read_json(SKILL_ROOT / "config/capabilities.json")
        elif args.command == "verify-install":
            result = verify_install()
        elif args.command == "locate":
            result = locate(args.query)
        elif args.command == "plan":
            result = plan(args.mode, args.language, args.domain)
        else:
            root = args.root.resolve(strict=True)
            if not root.is_dir():
                raise AuditInputError("--root must be a directory")
            if args.command == "preflight":
                result = preflight(root, args.manifest)
            elif args.command == "audit":
                result = audit(root, args.spec)
            elif args.command == "validate-report":
                result = validate_report(object_json(root, args.report), root=root)
            elif args.command in {"policy", "calibrate", "export-macros", "bib-audit"}:
                packet = object_json(root, args.packet)
                if args.command == "policy":
                    result = policy(packet["rule"], packet["facts"], root)
                    if result.get("check", {}).get("status") in {"mismatch", "invalid", "unverified"}:
                        result["status"] = result["check"]["status"]
                    elif result.get("action") == "open":
                        result["status"] = "mismatch"
                elif args.command == "calibrate":
                    result = calibrate(packet["records"])
                elif args.command == "export-macros":
                    result = export_macros(root, packet["claims"])
                else:
                    result = bibliography(root, packet["bib_path"], packet.get("citations", []), packet.get("query", ""))
            else:
                packet = object_json(root, args.packet)
                for key in ("issue", "revision_evidence", "check"):
                    if not isinstance(packet.get(key), dict):
                        raise AuditInputError("recheck packet needs object: " + key)
                result = recheck_issue(packet["issue"], packet["revision_evidence"], packet["check"], root=root)
        # Numeric computations already emit exact decimal strings. Preserve any
        # decimal metadata without converting it back through binary floats.
        def encode_decimal(value):
            if isinstance(value, Decimal):
                return str(value)
            raise TypeError("Unsupported JSON output type: " + type(value).__name__)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False, default=encode_decimal))
        if args.command == "recheck" and result.get("validation", {}).get("status") == "invalid":
            return 1
        if result.get("status") in ("mismatch", "invalid"):
            return 1
        if result.get("status") == "open":
            return 1 if result.get("validation", {}).get("status") == "invalid" else 3
        if result.get("status") == "unverified":
            return 3
        return 0
    except (AuditInputError, OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
