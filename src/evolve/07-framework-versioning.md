# Framework Versioning

**Part 5 · EVOLVE**

---

> **v2.0.0-rc1 stub.** This chapter elevates the existing repo-level [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) discipline to a first-class chapter of the book. Full prose lands in PR-B.

---

## What this chapter will cover

The chapter names *the framework itself* as a versioned artifact and walks the practice for evolving it without breaking the systems that adopted earlier versions.

Specifically:

- **Why the framework needs versioning.** A team's specs reference framework concepts (archetypes, dimensions, Cats, phases). When the framework changes those concepts, the team's specs become stale unless the framework signals the change clearly. Without versioning, the framework either freezes (and goes stale itself) or evolves silently (and produces unfindable inconsistency).
- **The MAJOR · MINOR · PATCH convention.** MAJOR: structural change that breaks specs or sync contracts (e.g., adding/removing an archetype or a calibration dimension; renaming a load-bearing term). MINOR: addition that doesn't break adoption (e.g., a new chapter, a new pattern, a new sub-block). PATCH: clarification, link fix, prose smoothing, deck/paper rebuild.
- **The three-place contract.** When a load-bearing named fact changes, three places update together: the book source, the paper source, and `paper/check-deck-sync.py`'s `CANONICAL_*` lists. The sync check enforces this; the chapter explains why the check is part of the discipline, not a CI tax.
- **The CHANGELOG as the primary record.** Every PR that bumps the version updates the CHANGELOG in the same commit. The CHANGELOG names what changed, why it's MAJOR/MINOR/PATCH, and which PR.
- **What MAJOR bumps look like.** The chapter walks v1 → v2 (the bump that introduced Phase 5 — Evolve — as a peer activity, three running scenarios, and the field-guide-with-scenarios shape) as the worked example. It names what the v2 bump did *not* change (5 archetypes, 4 dimensions, 7 Cats, 4 oversight models, 4 metrics, composition first-class) — the load-bearing commitments survived; the *spine* changed.
- **What downstream teams do with a bump.** PATCH: nothing. MINOR: read the CHANGELOG, optionally adopt new chapters/patterns. MAJOR: walk the spec evolution log to identify which sections need re-grounding against the new framework.
- **The relationship between framework version and paper status.** The paper has its own status header version (descriptive of the paper artifact); the framework version applies to book and paper *together*. The chapter names the distinction.

## Where this chapter sits in the Part

This is **5.7**, sitting near the end of Part 5 — Evolve, after the cost and anti-pattern chapters and before the DevSquad mapping. It's positioned here because framework versioning is the longest-time-scale evolve activity (per-quarter and per-year), and the chapters that precede it cover progressively shorter time-scales.

## Conceptual chapters this binds to

- [The Living Spec](../sdd/06-living-specs.md) — the per-system analog of framework versioning
- [Spec Versioning](../patterns/deployment/spec-versioning.md) — the deployment pattern
- [Co-adoption with DevSquad Copilot](../operating/13-co-adoption-with-devsquad.md) — composition is one of the things that has to be re-validated on a MAJOR bump

## Repo-level reference

The canonical record of framework version history lives in [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) at the repo root, not in the book itself — the book describes the *practice*; the CHANGELOG is the *log*.
