#!/usr/bin/env python3
"""Validate a declared review acceptance record, not scientific correctness."""
import argparse
import hashlib
import json
from pathlib import Path

GATES = {f"A{i:02d}" for i in range(1, 19)}
REQUIRED = {"A01", "A03", "A04", "A13", "A18"}
MODES = {"full", "submission", "camera_ready", "published_review"}
STATES = {"passed", "failed", "blocked", "not_applicable"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def safe_file(root, name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError(f"invalid path: {name!r}")
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts or rel.as_posix() != name:
        raise ValueError(f"unsafe/noncanonical path: {name}")
    path = root / rel
    for parent in [path, *path.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError(f"symlink is not allowed: {name}")
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError(f"missing or unsafe file: {name}")
    return path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(root, ledger_name):
    root = Path(root).resolve(strict=True)
    errors, advisories = [], []
    try:
        ledger = read_json(safe_file(root, ledger_name))
        if not isinstance(ledger, dict):
            raise ValueError("ledger must be an object")
        for key in ("paper_id", "version", "manuscript", "report"):
            if not nonempty(ledger.get(key)):
                errors.append(f"missing {key}")
        if ledger.get("mode") not in MODES:
            errors.append("invalid mode")
        artifacts = ledger.get("artifacts")
        if not isinstance(artifacts, dict) or not artifacts:
            raise ValueError("artifacts must be a nonempty object")
        for name, expected in artifacts.items():
            try:
                if name == ledger_name:
                    raise ValueError("ledger cannot hash itself")
                if sha256(safe_file(root, name)) != expected:
                    errors.append(f"stale/invalid hash: {name}")
            except (ValueError, OSError) as exc:
                errors.append(str(exc))
        for key in ("manuscript", "report"):
            if ledger.get(key) not in artifacts:
                errors.append(f"{key} must be in artifacts")
        if ledger.get("manuscript") == ledger.get("report"):
            errors.append("manuscript and report must be separate artifacts")
        report = read_json(safe_file(root, ledger.get("report")))
        if report.get("paper_id") != ledger.get("paper_id"):
            errors.append("report paper_id mismatch")
        issues = {}
        if not isinstance(report.get("issues"), list):
            raise ValueError("report issues must be an array")
        for issue in report["issues"]:
            iid, status, severity = issue.get("id"), issue.get("status"), issue.get("severity")
            if not nonempty(iid) or iid in issues:
                errors.append(f"invalid/duplicate issue: {iid}")
                continue
            issues[iid] = status
            if status not in {"confirmed", "unverified", "closed"} or severity not in {"critical", "major", "minor", "editorial"}:
                errors.append(f"invalid issue state/severity: {iid}")
            elif status != "closed":
                if severity in {"critical", "major"}:
                    errors.append(f"open {severity} issue: {iid}")
                else:
                    advisories.append(f"open {severity} issue: {iid}")
        gates = ledger.get("gates")
        if not isinstance(gates, list):
            raise ValueError("gates must be an array")
        seen = set()
        for gate in gates:
            gid, status = gate.get("id"), gate.get("status")
            if gid not in GATES or gid in seen:
                errors.append(f"unknown/duplicate gate: {gid}")
                continue
            seen.add(gid)
            if status not in STATES:
                errors.append(f"{gid}: invalid status")
            if status not in {"passed", "not_applicable"}:
                errors.append(f"{gid}: not accepted ({status})")
            if status == "not_applicable" and gid in REQUIRED:
                errors.append(f"{gid}: always-required gate cannot be NA")
            for key in ("basis", "check_result"):
                if not nonempty(gate.get(key)):
                    errors.append(f"{gid}: missing {key}")
            evidence = gate.get("evidence")
            if not isinstance(evidence, dict) or (status in {"passed", "not_applicable"} and not evidence):
                errors.append(f"{gid}: missing evidence mapping")
            elif isinstance(evidence, dict):
                for name, expected in evidence.items():
                    if name not in artifacts or artifacts[name] != expected:
                        errors.append(f"{gid}: untracked/mismatched evidence: {name}")
            refs = gate.get("issue_ids")
            if not isinstance(refs, list):
                errors.append(f"{gid}: issue_ids must be an array")
            else:
                for iid in refs:
                    if iid not in issues:
                        errors.append(f"{gid}: unknown issue {iid}")
                    elif status in {"passed", "not_applicable"} and issues[iid] != "closed":
                        errors.append(f"{gid}: unresolved linked issue {iid}")
        for gid in sorted(GATES - seen):
            errors.append(f"missing gate: {gid}")
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        errors.append(f"invalid ledger: {exc}")
    return {"status": "blocked" if errors else "records_current", "errors": errors,
            "advisories": advisories, "limit": "Declared records and hashes only; not scientific validity or venue acceptance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--ledger", required=True, help="JSON ledger path relative to root")
    args = parser.parse_args()
    try:
        result = validate(args.root, args.ledger)
    except (OSError, ValueError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "records_current" else 1


if __name__ == "__main__":
    raise SystemExit(main())
