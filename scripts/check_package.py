#!/usr/bin/env python3
"""Portable package checks; no claim of semantic review effectiveness."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/paper-review-atlas"


def check():
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    front = text.split("---", 2)
    if len(front) != 3:
        errors.append("Missing frontmatter")
    else:
        keys = re.findall(r"^(\w+):", front[1], re.M)
        if keys != ["name", "description"]:
            errors.append("Frontmatter must contain only name and description")
        if "name: paper-review-atlas" not in front[1]:
            errors.append("Skill name mismatch")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines")
    for file in SKILL.rglob("*.md"):
        body = file.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            path = (file.parent / target.split("#")[0]).resolve()
            if not path.is_relative_to(SKILL.resolve()) or not path.exists():
                errors.append(f"Broken or external package link: {file.relative_to(SKILL)} -> {target}")
    for name in ("capabilities", "sources", "conflicts", "features", "gaps"):
        data = json.loads((SKILL / "config" / (name + ".json")).read_text(encoding="utf-8"))
        if not isinstance(data.get(name), list) or not data[name]:
            errors.append("Empty registry: " + name)
    yaml = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(r'^  ' + key + r': "(.*)"$', yaml, re.M)
        if not match:
            errors.append("Missing quoted interface key: " + key)
        elif key == "short_description" and not 25 <= len(match[1]) <= 64:
            errors.append("Interface short description length")
    if "$paper-review-atlas" not in yaml:
        errors.append("Interface prompt must invoke the skill")
    return errors


if __name__ == "__main__":
    problems = check()
    print(json.dumps({"status": "invalid" if problems else "valid", "errors": problems}, indent=2))
    sys.exit(bool(problems))
