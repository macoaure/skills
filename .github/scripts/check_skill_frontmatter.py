#!/usr/bin/env python3
"""Fail CI if any skills/*/SKILL.md is missing required frontmatter fields.

Usage: python3 check_skill_frontmatter.py skills/*/SKILL.md
"""
import re
import sys

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REQUIRED_FIELDS = ("name:", "description:")


def check(path: str) -> bool:
    text = open(path, encoding="utf-8").read()
    match = FRONTMATTER.match(text)
    if not match:
        print(f"::error file={path}::missing YAML frontmatter")
        return False

    frontmatter = match.group(1)
    ok = True
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            print(f"::error file={path}::missing required field '{field}'")
            ok = False
    return ok


def main() -> int:
    paths = sys.argv[1:]
    if not paths:
        print("usage: check_skill_frontmatter.py <SKILL.md ...>", file=sys.stderr)
        return 2

    results = [check(path) for path in paths]
    for path, ok in zip(paths, results):
        print(f"{'OK  ' if ok else 'FAIL'}  {path}")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
