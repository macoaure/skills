#!/usr/bin/env python3
"""Validate a gitmoji + conventional-commit message against the fixed type mapping.

Reads the shortcode -> type table straight out of references/gitmoji-types.md,
so the script and the table the model reads can never drift apart.

Usage:
    python validate_commit.py "MESSAGE"
    python validate_commit.py --file path/to/commit_msg.txt
    echo "MESSAGE" | python validate_commit.py
"""
import argparse
import re
import sys
from pathlib import Path

TABLE_ROW = re.compile(r"^\|\s*`(:[a-z0-9_\-]+:)`\s*\|\s*([a-z0-9\-]+)\s*\|\s*(.*?)\s*\|\s*$")
TYPE_HEADER = re.compile(r"^##\s+(\S+)")
SUBJECT = re.compile(
    r"^(?P<shortcode>:[a-z0-9_\-]+:)\s+"
    r"(?P<type>[a-z]+)"
    r"(?:\((?P<scope>[\w./\-]+)\))?"
    r": (?P<subject>.+)$"
)


def load_gitmoji_table(md_path: Path) -> dict[str, tuple[str, str]]:
    """Returns {shortcode: (type, name-column-two)}."""
    mapping: dict[str, tuple[str, str]] = {}
    current_type = None
    for line in md_path.read_text().splitlines():
        header_match = TYPE_HEADER.match(line)
        if header_match:
            current_type = header_match.group(1)
            continue
        row_match = TABLE_ROW.match(line)
        if row_match and current_type:
            shortcode, name, _description = row_match.groups()
            if shortcode == ":---:" or name.strip("-") == "":
                continue
            mapping[shortcode] = (current_type, name)
    return mapping


def validate(message: str, gitmoji_table: dict[str, tuple[str, str]]) -> list[str]:
    errors = []
    lines = message.splitlines()
    if not lines or not lines[0].strip():
        return ["message is empty"]

    subject_line = lines[0]
    match = SUBJECT.match(subject_line)
    if not match:
        errors.append(
            "first line doesn't match '<shortcode> type(scope): subject', e.g. "
            "':sparkles: feat(auth): add OAuth login support' "
            f"(got: {subject_line!r})"
        )
        return errors

    shortcode = match.group("shortcode")
    commit_type = match.group("type")
    subject = match.group("subject")

    if shortcode not in gitmoji_table:
        errors.append(f"{shortcode!r} is not in the static gitmoji table")
    else:
        expected_type, name = gitmoji_table[shortcode]
        if commit_type != expected_type:
            errors.append(
                f"{shortcode} ({name}) is mapped to type '{expected_type}', "
                f"but the message uses '{commit_type}'"
            )

    if len(subject_line) > 72:
        errors.append(f"first line is {len(subject_line)} chars, keep it to 72 or fewer")

    if subject[:1].isupper():
        errors.append("subject should start lowercase (imperative, e.g. 'add', not 'Add')")

    if subject.endswith("."):
        errors.append("subject should not end with a period")

    if shortcode == ":boom:" and "BREAKING CHANGE:" not in message:
        errors.append(":boom: commits should include a 'BREAKING CHANGE:' footer in the body")

    body = "\n".join(lines[1:]).strip()
    if not body:
        errors.append(
            "message has no body — every commit needs a paragraph explaining why the change "
            "was made, not just the one-line subject"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", nargs="?", help="commit message to validate")
    parser.add_argument("--file", type=Path, help="read the message from a file")
    parser.add_argument(
        "--table",
        type=Path,
        default=Path(__file__).parent.parent / "references" / "gitmoji-types.md",
        help="path to gitmoji-types.md (defaults to the bundled one)",
    )
    args = parser.parse_args()

    if args.file:
        message = args.file.read_text()
    elif args.message:
        message = args.message
    else:
        message = sys.stdin.read()

    gitmoji_table = load_gitmoji_table(args.table)
    if not gitmoji_table:
        print(f"error: could not load any gitmoji rows from {args.table}", file=sys.stderr)
        return 2

    errors = validate(message, gitmoji_table)
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
