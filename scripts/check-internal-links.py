#!/usr/bin/env python3
"""
Check internal Markdown links in the book source (src/).

A link is broken if a relative `[text](path.md)` reference resolves to a file
that does not exist on disk.

Usage:
    python3 scripts/check-internal-links.py

Exit code: 0 if clean, 1 if any broken links found.
"""
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC_ROOT = os.path.join(REPO_ROOT, "src")

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    existing: set[str] = set()
    for dirpath, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith(".md"):
                existing.add(os.path.relpath(os.path.join(dirpath, f), SRC_ROOT))

    broken: list[tuple[str, int, str, str]] = []

    for dirpath, _, files in os.walk(SRC_ROOT):
        for f in files:
            if not f.endswith(".md"):
                continue
            full = os.path.join(dirpath, f)
            rel_dir = os.path.dirname(os.path.relpath(full, SRC_ROOT))
            with open(full) as fh:
                for lineno, line in enumerate(fh, 1):
                    for match in LINK_RE.finditer(line):
                        target = match.group(1).strip()
                        if (
                            target.startswith("http")
                            or target.startswith("mailto:")
                            or target.startswith("#")
                        ):
                            continue
                        target_clean = target.split("#")[0].split("?")[0]
                        if not target_clean.endswith(".md"):
                            continue
                        if target_clean.startswith("/"):
                            resolved = os.path.normpath(target_clean.lstrip("/"))
                        else:
                            resolved = os.path.normpath(os.path.join(rel_dir, target_clean))
                        if resolved not in existing:
                            broken.append(
                                (os.path.relpath(full, SRC_ROOT), lineno, target, resolved)
                            )

    for path, line, target, resolved in broken:
        print(f"{path}:{line} → {target}  (resolved: {resolved})")

    print(f"\nTotal broken: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
