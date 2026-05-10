# Framework Versioning

**Part 5 — Evolve**

---

> *"A framework that cannot version is a framework that has either frozen or quietly broken its adopters."*

---

## Context

Three months after a v1.4 release, a platform team that adopted the framework reads the v2.0.0 announcement and asks: *"does our customer-support spec break?"* The team has eight specs in production written against v1.4. The question is real — a MAJOR version bump means *something* the spec depends on changed cardinality, name, or structural meaning. The team needs to know what.

The answer they need is not "yes" or "no." It's: *here is exactly what changed, here is which sections of your specs are affected, here is what re-grounding looks like, and here is what does not need to change.* That answer is what framework versioning makes possible. Without it, the framework either (a) freezes and goes stale itself, or (b) evolves silently and produces unfindable inconsistency at scale.

Framework versioning is the longest-time-scale Evolve activity. The [closed loop](01-closed-loop.md) operates per-incident; the spec evolution log rolls up per-sprint; the Discipline-Health Audit is per-quarter; framework versioning is per-quarter to per-year. Each time-scale serves the same discipline — turn what you learned into a structural artifact — at a different layer of the system.

---

## The problem

The framework is three things at once: a vocabulary (archetypes, dimensions, Cats, activities), a set of structural commitments (the canonical spec template, oversight models, signal metrics), and a discipline (the IDS, the closed loop, the Discipline-Health Audit). Teams' specs reference all three. Spec sections cite archetypes (*"this system is a Synthesizer with embedded Advisor"*), dimensions (*"agency: low; autonomy: medium"*), failure categories (*"Cat 1 amendment: §4 NOT-authorized scope"*), and activities (*"the Validate phase signal metrics drove this change"*).

When the framework changes those references silently, every team's spec becomes stale in a way the team can't see. A new archetype appears in the appendix, but specs written against five archetypes don't recognize it. A category gets renamed, and the spec evolution log's "Cat 5" entries no longer cleanly map to the current Cat 5 definition. An activity gets promoted from a sub-discipline to a peer activity, and spec templates that hardcoded the prior cardinality break.

The opposite failure is just as real: a framework that freezes to avoid breaking adopters becomes inadequate as the deployment surface evolves. Cat 7 was added when computer-use agents arrived; Composition First-Class was promoted when the 2026 pressure-point classes pushed against the five-archetype taxonomy. Framework versioning is what lets the framework evolve *visibly* — adopters know what changed, why, and what they need to do about it.

---

## Forces

- **Stability for adopters vs. capacity to evolve.** The framework wants to stay stable so adopters' specs keep referencing it correctly. It also has to evolve as practice surfaces gaps. Versioning is how these two pressures coexist instead of fighting.

- **Lineage transparency vs. apparent novelty.** The framework draws lineage from prior work — SAE J3016, Shavit & Agarwal, the Cemri et al. MAST taxonomy, Anthropic's *Building Effective Agents*, the spec-kit and DevSquad heritage of Spec-Driven Development. When the framework evolves, the version log makes clear what is the framework's own evolution versus what is incorporation of new lineage. Teams reading the log understand whether the change is "the framework did something new" or "the framework caught up with literature."

- **Per-system spec evolution vs. framework evolution.** Each system has its own spec evolution log (per-system, per-incident). The framework also has a CHANGELOG (cross-system, per-release). The two are independent vocabularies. A framework MAJOR bump *might* trigger amendments across many specs; per-system spec evolution does not affect the framework version. Conflating the two is a category error that produces either an unmanageable framework changelog or version churn driven by individual systems' incidents.

- **MAJOR bump cost vs. accumulated half-fixes.** A MAJOR bump asks adopters to do work. Avoiding MAJOR bumps to spare adopters is tempting and produces accumulated half-fixes — a list of things the framework "should change at some point" that never coalesce into a release. Versioning honesty requires shipping MAJOR bumps when warranted, with the trade-offs visible.

---

## The solution

### MAJOR · MINOR · PATCH

**MAJOR.** A structural change that breaks existing specs or the deck/paper sync contract. Examples that have happened: v1 → v2 promoted *Evolve* from a sub-discipline to a peer fifth activity, changing activity cardinality from 4 to 5 and reorganizing the book's spine. Examples that would qualify but haven't: adding a sixth archetype, removing a calibration dimension, renaming a load-bearing term that appears in `paper/check-deck-sync.py`'s `CANONICAL_*` lists.

**MINOR.** An addition that does not break adoption. Examples from the v1 line: a new chapter (the senior-engineer chapter, MVP-AoI), a new spec sub-block (Composition Declaration in §4 at v1.0.0; Cost Posture in §4 at v1.4.0), a new pattern in the catalog, a new appendix card (the RACI Card at v1.1.0). Adopters can ignore MINOR additions safely; their specs still validate against the prior framework version.

**PATCH.** Prose clarifications, link fixes, citation additions, figure refinements, deck/paper rebuilds. No adopter has to do anything in response, but the version number advances so the artifact's release record is precise. PATCH bumps can be batched; MAJOR and MINOR each get their own CHANGELOG entry.

The version moves with PR merges to `main`. Each PR description names the bump (`v1.0.0 → v1.0.1`, `v1.0.0 → v1.1.0`, etc.) and updates `CHANGELOG.md` in the same commit so the changelog stays in lockstep with the published state.

### The three-place contract

A change to a load-bearing named fact requires three coordinated updates in the same PR:

1. **The book** — `src/...` Markdown sources, glossary, `SUMMARY.md` if structure is affected.
2. **The paper** — `paper/architecture-of-intent.md`, including the figure caption if the canvas figure is affected.
3. **`paper/check-deck-sync.py`** — the `CANONICAL_*` lists at the top of the script.

The sync check enforces this. It runs in `.github/workflows/build-paper.yml` *before* any build steps, so a PR that touches the paper or deck without updating all three places fails before artifacts get rebuilt. The check is part of the discipline, not a CI tax — it makes drift between the book and paper into a hard error rather than a slow accumulation.

The check is intentionally conservative. It enforces only named-fact alignment: 5 archetypes, 7 Cats, 4 Cat 7 sub-categories, 8 DevSquad phases, 5 activities, 3 novel / 4 not-claimed counts. Freeform prose between the book and paper can differ; the load-bearing structures cannot.

When the check needs to be extended — when a new load-bearing list is promoted — the extension itself is part of the MAJOR bump that introduced the list. The v2.0.0 bump added `CANONICAL_PHASES` and the corresponding paper-and-deck check; future bumps that introduce new lists will follow the same pattern.

### CHANGELOG as the primary record

`CHANGELOG.md` at the repo root is the canonical version history. Each entry names what changed in one or two lines per item, ties the bump to the PR number, and explains *why* it's MAJOR/MINOR/PATCH. The CHANGELOG is intentionally verbose. Reviewers reading it should be able to understand not just what shipped but the trade-offs the change considered and rejected.

The v1.4.0 entry is the canonical example. It documents not just the addition (Cost Posture sub-block in §4) but the candidate alternative considered and rejected (cost as a fifth calibration dimension), with three structural reasons for the rejection. That kind of explicit accounting is what makes the version history useful as a *design record*, not just a release log.

The CHANGELOG also documents what *did not* change at each bump. The v2.0.0-rc1 entry, for instance, lists the load-bearing commitments that survived the MAJOR bump (5 archetypes, 4 dimensions, 7 Cats, 4 oversight models, 4 signal metrics, 8 pattern categories, composition first-class, IDS, Discipline-Health Audit, honest accounting) — making clear that the bump reshaped the spine but preserved the vocabulary. Adopters reading the entry know what they have to re-ground (the activity-spine assumption) and what they don't (everything else).

### What a MAJOR bump looks like in practice

The v1 → v2 bump is the worked example currently visible in the repository. The change:

- **What changed.** Activity cardinality went from 4 to 5 — *Evolve* was promoted from a closing-Validate sub-discipline to a peer activity. The book's organizational spine reshaped from 9 mixed-grain Parts (*Decisions / Spec / Agent / Oversight / Ship / Pilots / Patterns / Repertoires / Appendices*) to 6 phase-aligned Parts (*Frame / Specify / Delegate / Validate / Evolve / Reference*). The deck and paper sync check now enforce the new cardinality.

- **What did *not* change.** 5 archetypes, 4 dimensions, 7 Cats, 4 oversight models, 4 signal metrics, 8 pattern categories, composition first-class, the IDS, the Discipline-Health Audit, the honest accounting (3 novel / 4 not-claimed). The framework's vocabulary survived; only the spine changed.

- **What downstream teams have to do.** Read the CHANGELOG entries for v2.0.0-rc1 onward. Identify which sections of their specs reference "the four activities" — most don't, since most specs reference individual activities rather than the cardinality. Update any spec template or organizational documentation that hardcoded the four-activity assumption.

The bump shipped as a release-candidate (rc) line because the structural commit was large enough to merit incremental visibility. rc1 shipped the SUMMARY reshape and scenario stubs. rc2 shipped the canvas redraw and deck activities slide. Subsequent rcs ship the prose work for the new chapters and scenarios. v2.0.0 stable ships when the rc series stabilizes — the rc line lets adopters track the framework's progress toward stability rather than waiting for a single all-or-nothing release.

### What downstream teams do with each bump

| Bump | Adopter response |
|---|---|
| **PATCH** | Nothing. Behavior unchanged; framework artifacts referenced are sharper. |
| **MINOR** | Read the CHANGELOG entry. Optionally adopt new chapters, patterns, or sub-blocks. Existing specs continue to validate against the prior version's expectations; the new material is purely additive. |
| **MAJOR** | Walk the spec evolution log to identify which sections need re-grounding. The work is bounded by the size of the load-bearing change — most MAJOR bumps affect 1–2 spec sections, not the whole template. Re-grounding produces a set of spec amendments, all attributable in the system's own spec evolution log to the framework version bump (e.g., *"amended §3 scope language to reflect framework v2.0.0's activity-spine vocabulary"*). |

The asymmetry is intentional. PATCH and MINOR bumps put no work on adopters; MAJOR bumps put bounded, well-described work on adopters. The framework can evolve in all three modes, and adopters know in advance what each mode costs them.

### Framework version vs. paper status version

The framework version applies to the book and paper *together*. A v2.0.0 framework means the book and the paper both reflect v2.0.0's structural commitments.

The paper additionally carries its own *paper status version* in the status header (e.g., *"Paper status: Skeleton draft (paper v0.1)"*). The paper status version describes the *paper artifact* — its draft maturity, its target venue, its expected revision cycle — and is independent of the framework version. A paper at status v0.3 against framework v2.0.0 means: the framework's structural commitments are at v2.0.0, the paper's draft maturity is v0.3.

The book does not carry a separate book version. The framework version *is* the book version, because the book is the framework's primary instantiation; a change in the book that touches a load-bearing commitment bumps the framework version.

---

## Where this chapter sits in Part 5

This is **5.7**, near the end of Part 5 — Evolve, after the cost and anti-pattern chapters and before the DevSquad mapping. Framework versioning is the longest-time-scale Evolve activity (per-quarter and per-year), and the chapters that precede it cover progressively shorter time-scales: the [closed loop](01-closed-loop.md) is per-incident; the spec evolution log is per-sprint; the [Discipline-Health Audit](../evolve/15-anti-patterns.md) is per-quarter; framework versioning is per-quarter to per-year. Reading Part 5 in order reveals the time-scale gradient.

---

## Related material

- [The Living Spec](../specify/06-living-specs.md) — the per-system analog of framework versioning
- [Spec Versioning](../patterns/deployment/spec-versioning.md) — the deployment pattern for amended specs
- [The Closed Loop](01-closed-loop.md) — the per-incident discipline that rolls up to framework-level versioning at the longest time-scale
- [Co-adoption with DevSquad Copilot](../evolve/13-co-adoption-with-devsquad.md) — composition is one of the things that has to be re-validated on a MAJOR bump
- [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) — the canonical record at the repo root
