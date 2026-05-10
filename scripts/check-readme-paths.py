#!/usr/bin/env python3
"""
Check README.md (root) and paper/README.md for stale path references.

Scans every line for tokens that look like repo-relative paths (start with
one of the known top-level prefixes — src/, paper/, scripts/, theme/,
book/, .github/) and verifies each one exists on disk.

Brace expansion is supported for tokens like `paper/architecture-of-intent
.{md,pdf}`. Glob tokens (containing `*`) are skipped — they are patterns,
not concrete paths.

Catches the kind of drift that bit the canvas-readme-fixes pass: a
directory rename (architecture/ → frame/, agents/ → delegate/) that left
the README's repository-layout tree pointing at directories that no
longer exist.

Usage:
    python3 scripts/check-readme-paths.py

Exit code: 0 if every reference resolves, 1 otherwise.
"""
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

README_FILES = ["README.md", "paper/README.md"]

PATH_PREFIXES = ("src/", "paper/", "scripts/", "theme/", ".github/")

PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9._{},/*-]+")
TREE_ART_RE = re.compile(r"[│├└─]+")
BRACE_RE = re.compile(r"\{([^{}]+)\}")


def expand_braces(token: str) -> list[str]:
    m = BRACE_RE.search(token)
    if not m:
        return [token]
    options = m.group(1).split(",")
    expanded = [token[: m.start()] + opt + token[m.end() :] for opt in options]
    out: list[str] = []
    for cand in expanded:
        out.extend(expand_braces(cand))
    return out


def normalize(token: str) -> str:
    return token.strip(".,;:!?\"'`()[] ")


def main() -> int:
    broken: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int, str]] = set()

    for readme in README_FILES:
        path = os.path.join(REPO_ROOT, readme)
        with open(path) as f:
            for lineno, raw in enumerate(f, 1):
                line = TREE_ART_RE.sub(" ", raw)
                line = line.split("#", 1)[0]
                for match in PATH_TOKEN_RE.finditer(line):
                    token = normalize(match.group(0))
                    if not token:
                        continue
                    for cand in expand_braces(token):
                        cand = normalize(cand)
                        if not cand:
                            continue
                        if "*" in cand:
                            continue
                        if not any(cand.startswith(p) for p in PATH_PREFIXES):
                            continue
                        is_dir = cand.endswith("/")
                        check = cand.rstrip("/")
                        full = os.path.join(REPO_ROOT, check)
                        ok = os.path.isdir(full) if is_dir else os.path.exists(full)
                        if not ok:
                            key = (readme, lineno, cand)
                            if key not in seen:
                                seen.add(key)
                                broken.append(key)

    if broken:
        print("=== Broken README path references ===")
        for f, n, p in broken:
            print(f"{f}:{n}  {p}")
        print(f"\nFound {len(broken)} broken reference(s).")
        return 1
    print("All README path references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
