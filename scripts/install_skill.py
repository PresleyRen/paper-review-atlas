#!/usr/bin/env python3
"""Install this self-contained skill into one explicitly chosen project."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1] / "skills/paper-review-atlas"


def install(project: Path, replace=False, source=SOURCE):
    project = project.resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    source = source.resolve(strict=True)
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source does not contain SKILL.md")
    for item in source.rglob("*"):
        if item.is_symlink():
            raise ValueError("Install source must not contain symbolic links")
    parent = project / ".agents/skills"
    if not parent.resolve().is_relative_to(project):
        raise ValueError("Project skill directory escapes the project through a symlink")
    target = parent / "paper-review-atlas"
    if target.is_symlink():
        raise ValueError("Refusing to replace a symlink destination")
    if source.is_relative_to(target.resolve()) or target.resolve().is_relative_to(source):
        raise ValueError("Source overlaps destination")
    if target.exists() and not replace:
        raise FileExistsError("Skill already exists; use --replace to preserve a backup and update it")
    parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if target.exists():
        if not target.is_dir():
            raise ValueError("Destination exists but is not a directory")
        # Keep old SKILL.md files outside active skill discovery directories.
        backup_parent = project / ".paper-review-atlas-backups"
        if backup_parent.is_symlink() or not backup_parent.resolve().is_relative_to(project):
            raise ValueError("Backup directory must stay inside the project without a symlink")
        backup_parent.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = backup_parent / ("paper-review-atlas-" + stamp)
        target.rename(backup)
    try:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    except Exception:
        if target.exists():
            shutil.rmtree(target)
        if backup:
            backup.rename(target)
        raise
    return {"status": "installed", "path": str(target), "backup": str(backup) if backup else None,
            "activation": "Skill discovery depends on the host application. Reload its skill list if needed."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--replace", action="store_true", help="Back up an existing skill before replacing it")
    args = p.parse_args()
    try:
        print(json.dumps(install(args.project, args.replace), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
