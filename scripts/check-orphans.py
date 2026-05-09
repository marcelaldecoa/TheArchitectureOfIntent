#!/usr/bin/env python3
"""
Check the book's SUMMARY.md against the file tree.

Reports:
- Orphans: Markdown files in src/ that are not listed in SUMMARY.md
- Missing: SUMMARY.md entries that point at files that do not exist

Usage:
    python3 scripts/check-orphans.py

Exit code: 0 if clean, 1 if any orphans or missing files found.
"""
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC_ROOT = os.path.join(REPO_ROOT, "src")
SUMMARY_PATH = os.path.join(SRC_ROOT, "SUMMARY.md")


def main() -> int:
    all_md: set[str] = set()
    for dirpath, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith(".md") and f != "SUMMARY.md":
                all_md.add(os.path.relpath(os.path.join(dirpath, f), SRC_ROOT))

    summary_text = open(SUMMARY_PATH).read()
    listed: set[str] = set(
        match.group(1) for match in re.finditer(r"\(([^)]+\.md)\)", summary_text)
    )

    orphans = sorted(all_md - listed)
    missing = sorted(listed - all_md)

    print("=== Orphans (file exists but not in SUMMARY) ===")
    for path in orphans:
        print(path)

    print("\n=== Missing (in SUMMARY but file absent) ===")
    for path in missing:
        print(path)

    if orphans or missing:
        print(f"\nFound {len(orphans)} orphans and {len(missing)} missing entries.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
