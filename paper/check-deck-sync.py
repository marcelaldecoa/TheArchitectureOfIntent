#!/usr/bin/env python3
"""
Verify that load-bearing facts in the deck match the paper.

This script extracts the small set of structured facts that BOTH the paper
(paper/architecture-of-intent.md) and the teaching deck source
(paper/presentation_content.py) must agree on, and exits non-zero if they
diverge. It is conservative: it only checks named facts that appear in both
sources; it does NOT try to enforce prose alignment.

Drift surface (intentionally small):
  - Five archetype names
  - Seven failure category names (Cat 1..Cat 7)
  - Four Cat 7 sub-category names
  - Eight DevSquad phase names (paper only — the deck condenses some)
  - "3 novel / 4 not-claimed" honest-accounting counts
  - Five framework activities (paper only at v2.0.0-rc1; deck-side check
    activates when an activities slide lands)

If you intentionally rename or add to any of these, update all THREE places:
  1. paper/architecture-of-intent.md
  2. paper/presentation_content.py
  3. The CANONICAL_* lists below

Usage:
    python3 paper/check-deck-sync.py

Exit code: 0 if synchronized, 1 if drift detected.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER_PATH = HERE / "architecture-of-intent.md"
DECK_PATH = HERE / "presentation_content.py"


# ============================================================================
# Canonical lists — the contract.
# Update these (and both sources below them) when names intentionally change.
# ============================================================================

CANONICAL_ARCHETYPES = [
    "Advisor", "Executor", "Guardian", "Synthesizer", "Orchestrator",
]

# Cat number -> Cat name (the human-facing label, not the long description).
CANONICAL_CATEGORIES = [
    ("Cat 1", "Spec"),
    ("Cat 2", "Capability"),
    ("Cat 3", "Scope creep"),
    ("Cat 4", "Oversight"),
    ("Cat 5", "Compounding"),
    ("Cat 6", "Model-level"),
    ("Cat 7", "Perceptual"),
]

CANONICAL_CAT7_SUBS = [
    "Misidentification",
    "Missed element",
    "Hallucinated element",
    "State miscount",
]

CANONICAL_DEVSQUAD_PHASES = [
    "envisioning phase",
    "Spec the next slice",
    "Plan only what the current slice needs",
    "Decompose that slice",
    "Implement with TDD discipline",
    "Learn in the open",
    "Review in an independent context",
    "Refine continuously",
]

# Honest-accounting cardinality.
# Paper claims THREE explicit novel contributions; deck mirrors that.
CANONICAL_NOVEL_COUNT = 3
CANONICAL_NOT_CLAIMED_COUNT = 4

# Five framework activities — promoted to a load-bearing list in v2.0.0
# (Evolve was elevated from a closing-Validate sub-discipline to a peer
# fifth activity). Both paper and deck checked from rc2 onward.
CANONICAL_PHASES = [
    "Frame",
    "Specify",
    "Delegate",
    "Validate",
    "Evolve",
]


# ============================================================================
# Helpers
# ============================================================================

def load_deck_module():
    spec = importlib.util.spec_from_file_location("presentation_content", DECK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_slide(slides, kind, section_substr=None):
    """Return the first slide of given kind whose section contains substring."""
    for s in slides:
        if s.get("kind") != kind:
            continue
        if section_substr and section_substr.lower() not in s.get("section", "").lower():
            continue
        return s
    return None


def report(failures):
    print()
    if failures:
        print(f"  {len(failures)} drift(s) detected:")
        for f in failures:
            print(f"    ✖ {f}")
        print()
        print("  Update the diverging source(s), or update CANONICAL_* in this script if")
        print("  the change is intentional.")
        return 1
    print("  Deck and paper are in sync on all load-bearing named facts.")
    return 0


# ============================================================================
# Checks
# ============================================================================

def check_archetypes(paper_text, deck):
    """All 5 canonical archetype names must appear in both sources."""
    failures = []
    for name in CANONICAL_ARCHETYPES:
        if not re.search(rf"\b{re.escape(name)}\b", paper_text):
            failures.append(f"archetype '{name}' missing from paper")

    # Find the deck's archetypes table.
    slide = find_slide(deck.SLIDES, "table", section_substr="ARCHETYPES")
    if slide is None:
        failures.append("deck has no archetypes table slide (kind=table, section contains 'ARCHETYPES')")
    else:
        deck_names = [row[0] for row in slide["rows"]]
        if deck_names != CANONICAL_ARCHETYPES:
            failures.append(
                f"deck archetypes table is {deck_names}, expected {CANONICAL_ARCHETYPES}"
            )
    return failures


def check_categories(paper_text, deck):
    """All 7 Cat names appear in paper. Deck taxonomy slide has the same 7 in order."""
    failures = []
    for cat_id, name in CANONICAL_CATEGORIES:
        if cat_id not in paper_text:
            failures.append(f"category id '{cat_id}' missing from paper")
        if not re.search(rf"\b{re.escape(name)}\b", paper_text):
            failures.append(f"category name '{name}' missing from paper")

    slide = find_slide(deck.SLIDES, "taxonomy")
    if slide is None:
        failures.append("deck has no taxonomy slide (kind=taxonomy)")
    else:
        deck_pairs = [(row[0], row[1]) for row in slide["rows"]]
        if deck_pairs != CANONICAL_CATEGORIES:
            failures.append(
                f"deck taxonomy is {deck_pairs}, expected {CANONICAL_CATEGORIES}"
            )
    return failures


def check_cat7_subs(paper_text, deck):
    """All 4 Cat 7 sub-category names appear in both sources, deck in same order."""
    failures = []
    for name in CANONICAL_CAT7_SUBS:
        if name not in paper_text:
            failures.append(f"Cat 7 sub-category '{name}' missing from paper")

    slide = find_slide(deck.SLIDES, "cat7")
    if slide is None:
        failures.append("deck has no Cat 7 slide (kind=cat7)")
    else:
        deck_subs = [pair[0] for pair in slide["subs"]]
        if deck_subs != CANONICAL_CAT7_SUBS:
            failures.append(
                f"deck Cat 7 sub-categories are {deck_subs}, expected {CANONICAL_CAT7_SUBS}"
            )
    return failures


def check_devsquad_phases(paper_text):
    """All 8 DevSquad phase names appear verbatim in the paper.

    The deck condenses some phases into combined rows (phases 1+2 merged),
    so deck-side enforcement isn't useful here. Paper alone is checked.
    """
    failures = []
    for phase in CANONICAL_DEVSQUAD_PHASES:
        if phase not in paper_text:
            failures.append(f"DevSquad phase '{phase}' missing from paper")
    return failures


def check_phases(paper_text, deck):
    """All 5 framework activity names appear in both paper and deck.

    Paper side: capitalized phase names appear as standalone words.
    Deck side: there is a `kind=table` slide whose section contains
    'ACTIVITIES' and whose first column matches CANONICAL_PHASES in order.

    Match is verbatim and case-sensitive on the capitalized phase names
    (Frame, Specify, Delegate, Validate, Evolve) — the activity names
    are the load-bearing form; lowercase mentions in prose don't count.
    """
    failures = []
    for phase in CANONICAL_PHASES:
        if not re.search(rf"\b{re.escape(phase)}\b", paper_text):
            failures.append(f"framework activity '{phase}' missing from paper")

    slide = find_slide(deck.SLIDES, "table", section_substr="ACTIVITIES")
    if slide is None:
        failures.append("deck has no activities table slide (kind=table, section contains 'ACTIVITIES')")
    else:
        deck_phases = [row[0] for row in slide["rows"]]
        if deck_phases != CANONICAL_PHASES:
            failures.append(
                f"deck activities table is {deck_phases}, expected {CANONICAL_PHASES}"
            )
    return failures


def check_honest_accounting(deck):
    """Deck's compare slide for honest accounting must have the right cardinality."""
    failures = []
    slide = find_slide(deck.SLIDES, "compare", section_substr="HONEST")
    if slide is None:
        failures.append("deck has no honest-accounting compare slide (kind=compare, section contains 'HONEST')")
        return failures
    novel = len(slide["left"]["items"])
    borrowed = len(slide["right"]["items"])
    if novel != CANONICAL_NOVEL_COUNT:
        failures.append(
            f"deck claims {novel} novel contributions, canonical is {CANONICAL_NOVEL_COUNT}"
        )
    if borrowed != CANONICAL_NOT_CLAIMED_COUNT:
        failures.append(
            f"deck lists {borrowed} not-claimed items, canonical is {CANONICAL_NOT_CLAIMED_COUNT}"
        )
    return failures


# ============================================================================
# Main
# ============================================================================

def main():
    paper_text = PAPER_PATH.read_text()
    deck = load_deck_module()

    failures = []
    print("Checking deck/paper sync...")
    print()
    print(f"  paper:  {PAPER_PATH.relative_to(HERE.parent)}")
    print(f"  deck:   {DECK_PATH.relative_to(HERE.parent)}")
    print()

    for label, fn in [
        ("Archetypes (5)",          lambda: check_archetypes(paper_text, deck)),
        ("Failure categories (7)",  lambda: check_categories(paper_text, deck)),
        ("Cat 7 sub-categories (4)", lambda: check_cat7_subs(paper_text, deck)),
        ("DevSquad phases (8)",     lambda: check_devsquad_phases(paper_text)),
        ("Framework activities (5)", lambda: check_phases(paper_text, deck)),
        ("Honest-accounting cardinality (3 / 4)", lambda: check_honest_accounting(deck)),
    ]:
        f = fn()
        status = "OK" if not f else "DRIFT"
        print(f"  [{status:5s}] {label}")
        failures.extend(f)

    return report(failures)


if __name__ == "__main__":
    sys.exit(main())
