#!/usr/bin/env python3
"""Make sure gitmoji-changelog has project info to work with, without ever asking first.

Checks, in order, for files a gitmoji-changelog preset already knows how to read
(package.json, pom.xml, Cargo.toml, Chart.yaml, pyproject.toml/setup.py). If one is
found, there's nothing to do -- just report which --preset flag matches it.

Otherwise, auto-generates a .gitmoji-changelogrc for --preset generic, inferring:
  - name:        the git remote's repo name, else the directory name
  - description: the first real line of README.md, else a generic placeholder
  - version:     the latest git tag (leading "v" stripped), else "0.0.0"

Never overwrites an existing .gitmoji-changelogrc -- a human or a previous run may
have already tuned it.

Usage: python3 ensure_project_config.py [repo_root]   (defaults to cwd)
Prints `preset=<name>` and `reason=...` lines for the caller to relay to the user.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

# Pinned gitmoji-changelog@2.3.0's --preset choices are exactly node/generic/
# maven/cargo/helm -- no python, even though it exists in the upstream repo's
# current source. Passing an unsupported choice fails yargs validation, so
# Python projects fall through to the generic branch below instead.
MANIFEST_PRESETS = {
    "package.json": "node",
    "pom.xml": "maven",
    "Cargo.toml": "cargo",
    "Chart.yaml": "helm",
}


def run_git(repo_root: Path, *args) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args], capture_output=True, text=True, check=True
        )
        return result.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def infer_name(repo_root: Path) -> str:
    remote_url = run_git(repo_root, "remote", "get-url", "origin")
    if remote_url:
        name = remote_url.rstrip("/").rsplit("/", 1)[-1]
        return re.sub(r"\.git$", "", name)
    return repo_root.name


def infer_description(repo_root: Path, name: str) -> str:
    for filename in ("README.md", "README"):
        readme = repo_root / filename
        if readme.exists():
            for raw_line in readme.read_text(errors="ignore").splitlines():
                line = raw_line.strip()
                # skip blanks, headings (the title line, not a description), and
                # badge/image/html lines that aren't prose
                if not line or line.startswith(("#", "[![", "<", "![", "|", "---")):
                    continue
                return line[:200]
    return f"Changelog for {name}."


def infer_version(repo_root: Path) -> str:
    tag = run_git(repo_root, "describe", "--tags", "--abbrev=0")
    if tag:
        return re.sub(r"^v", "", tag)
    return "0.0.0"


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    toplevel = run_git(repo_root, "rev-parse", "--show-toplevel")
    if toplevel:
        repo_root = Path(toplevel)

    for manifest, preset in MANIFEST_PRESETS.items():
        if (repo_root / manifest).exists():
            print(f"preset={preset}")
            print(f"reason=found {manifest}, no .gitmoji-changelogrc needed")
            return 0

    rc_path = repo_root / ".gitmoji-changelogrc"
    if rc_path.exists():
        print("preset=generic")
        print(f"reason={rc_path} already exists, left untouched")
        return 0

    name = infer_name(repo_root)
    description = infer_description(repo_root, name)
    version = infer_version(repo_root)

    rc_path.write_text(
        json.dumps(
            {"project": {"name": name, "description": description, "version": version}},
            indent=2,
        )
        + "\n"
    )

    print("preset=generic")
    print(f"reason=created {rc_path} (name={name!r}, description={description!r}, version={version!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
