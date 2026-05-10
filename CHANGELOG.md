# Changelog

The Architecture of Intent is versioned as a framework. This file records the evolution of the framework's load-bearing commitments: the archetypes, the dimensions, the failure taxonomy, the spec template, the activities, and the practices that bind them.

The version applies to the framework as instantiated by the [book](src/) and the [companion paper](paper/architecture-of-intent.md) *together*. The paper carries its own paper-status version (in the paper's status header) which describes the paper artifact, not the framework.

---

## Versioning convention

Semantic-ish versioning, applied to the framework rather than to a software artifact:

- **MAJOR** version bump — a structural change that breaks existing specs, existing adoption, or the deck/paper sync contract. Examples: adding a sixth archetype; removing an archetype; adding a fifth calibration dimension; changing the cardinality of the failure taxonomy; renaming a load-bearing term that appears in `paper/check-deck-sync.py`.
- **MINOR** version bump — an addition that does not break existing specs. Examples: a new chapter; a new pattern in the pattern index; a new spec-template sub-block; a new composition pattern; a new appendix; a new working-practice ritual.
- **PATCH** version bump — prose clarifications, link fixes, typo corrections, citation additions, figure refinements, new worked examples, deck/paper rebuilds.

The version moves with PR merges to `main`. PR descriptions should name the bump (`v1.0.0 → v1.0.1`, `v1.0.0 → v1.1.0`, etc.) and update this file in the same commit so the changelog stays in lockstep with the published state.

---

## v2.0.0-rc3 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — ships the full prose for the two new Phase-5 conceptual chapters that landed as stubs at rc1: *The Closed Loop: From Failures to Spec Amendments* (5.1) and *Framework Versioning* (5.7). The framework's load-bearing commitments are unchanged from rc2.

### Added

- **`src/evolve/01-closed-loop.md` — full chapter prose.** Replaces the rc1 stub. Names the discipline that opens Part 5: every diagnosed failure produces a structural change (spec, manifest, CI guard, framework version) — never only a prompt patch. Sections: Context (a Friday-afternoon vignette of a closed-loop violation: the on-call engineer reaching for a prompt patch instead of the spec amendment), The problem, Forces, The solution (the loop in detail with a Cat-to-fix-locus table; spec evolution log discipline; the loop at three time-scales — per-incident hours, per-sprint weeks, per-quarter months; what breaks the loop with five named loop-break patterns), Why this chapter opens Part 5 (it positions every other Part-5 chapter as practice that *supports* the loop), and a tour of the loop in operation across the three running scenarios.

- **`src/evolve/07-framework-versioning.md` — full chapter prose.** Replaces the rc1 stub. Elevates the existing repo-level `CHANGELOG.md` discipline to a first-class chapter. Sections: Context (a vignette of a platform team asking *"does our v1.4 spec break against v2.0?"* — naming the question framework versioning is meant to answer), The problem, Forces, The solution (MAJOR · MINOR · PATCH convention with grounded examples from the v1 line; the three-place contract for load-bearing changes — book / paper / sync-check; CHANGELOG as primary record with the v1.4.0 cost-as-fifth-dimension entry as a worked design-record example; what a MAJOR bump looks like in practice using v1 → v2 as the worked example; what downstream teams do with each bump as a table; framework version vs paper status version distinction), and the chapter's place in Part 5 as the longest-time-scale Evolve activity.

### Updated

- Version markers advanced from **v2.0.0-rc2** to **v2.0.0-rc3** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the updated status header.

### Voice

Both new chapters open with a vignette before exposition, per the v2.0.0 commitment to a field-guide voice. The closed-loop chapter opens on a $2,400 unauthorized refund and the engineer's instinct to patch the prompt; the framework-versioning chapter opens on a platform team reading a MAJOR-bump announcement and asking what their existing specs need. The vignettes set the stakes; the rest of each chapter exposits the discipline that addresses them.

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line because the new chapters are foundational to the *Evolve* activity that v2.0.0 introduced as a peer fifth activity. The chapters were stubs at rc1; until they shipped as full prose, the *Evolve* commitment was structural-only (the Part exists, the SUMMARY links resolve) without conceptual ground. rc3 closes that gap. The version stays in the rc-line because the scenario chapters and file-path renames are still pending.

### Deferred (unchanged from rc2's plan)

- File-path renames (`architecture/` → `frame/`, etc.) — purely filesystem cleanup; no reader-facing change
- Three scenarios written in full — PR-C, PR-E, PR-F
- Voice rewrites for the older chapters — PR-G, PR-H, PR-I
- Paper §5 (single canonical scenario) — PR-D
- Reading paths appendix + final v2.0.0 release tag — PR-J
- Light Evolve-framing intros for the 9 existing `operating/*` chapters that now sit in Part 5 — folded into PR-G

### PRs

- **PR-B** (this rc) — closed-loop and framework-versioning chapter prose, version markers, paper PDF rebuild.

---

## v2.0.0-rc2 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — ships the five-row canvas redraw and the teaching-deck activities slide that were deferred from rc1. This rc closes the rc1 prose-vs-figure gap (rc1 said "five activities" but the canvas figure still showed four rows). The framework's load-bearing commitments are unchanged from rc1.

### Added

- **Canvas redraw to five rows.** `paper/figures/architecture-of-intent-canvas.svg` extended from a 1180px-tall, four-activity layout to a 1330px-tall, five-activity layout. New EVOLVE row contains four practice chips (Closed Loop · Spec Evolution Log · Discipline-Health Audit · Framework Versioning) parallel in width and spacing to the SPECIFY row's grid. Loop arrow redrawn to descend from the right-rail metrics into EVOLVE, sweep beneath EVOLVE, and ascend the left spine back to FRAME — preserving the "metrics → next intent" semantic while making EVOLVE a first-class waypoint instead of an implicit feedback. Right-rail title softened from "CLOSED LOOP" to "SIGNALS" with the strap "drive the EVOLVE loop," reflecting that the metrics are now the *input* to a named activity rather than a self-contained closing loop. Bottom caption updated from "FRAME · CALIBRATE · SPECIFY · DELEGATE · VALIDATE" to "FRAME · SPECIFY · DELEGATE · VALIDATE · EVOLVE — the five activities of the Architecture of Intent."
- **Canvas PNG regenerated** at 1600×1330 (was 1600×1180) and mirrored to `src/images/architecture-of-intent-canvas.png` for mdBook.
- **Deck activities slide.** `paper/presentation_content.py` gains a new slide at position 6 (`kind=table`, `section="02 · ACTIVITIES"`, title *"Five activities, one canvas"*) showing the five activities with the load-bearing list each binds and the artifact each produces. Existing "Four load-bearing elements" cards4 slide retitled to *"Four load-bearing elements bound to the spine"* to clarify the activities-as-spine framing. Both PPTX and HTML decks rebuilt; deck count goes from 19 → 20 slides.
- **Deck-side phase check.** `paper/check-deck-sync.py`'s `check_phases()` previously checked the paper only at rc1; it now checks both the paper *and* the deck's activities table (mirrors `check_archetypes()`'s deck-side enforcement). The five-activity cardinality is now sync-locked across both artifacts.

### Updated

- **`src/introduction.md`** — image alt-text rewritten to describe the new five-row canvas; the rc1 deferral annotation paragraph removed.
- **`paper/architecture-of-intent.md`** — figure caption rewritten to describe the new five-row layout; the rc1 deferral language removed; status header advances to **v2.0.0-rc2** with the rc2-shipped notation.
- **`paper/architecture-of-intent.pdf`** — recompiled with the new figure caption; PDF size grows from ~982KB to ~1.16MB to accommodate the taller figure.
- **Version markers advanced from `v2.0.0-rc1` to `v2.0.0-rc2`** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md` (Framework version section), and `README.md` (Framework version section). The README's "four activities" enumeration also gets corrected to "five activities" — this was a v1.4.0-era leftover that PR #53 missed.

### Deferred to subsequent rcs (unchanged from rc1's plan)

- File-path renames (`architecture/` → `frame/` etc.) — purely filesystem cleanup; no reader-facing change.
- Phase-5 chapter prose (PR-B).
- Three scenarios written in full (PR-C, PR-E, PR-F).
- Voice rewrites (PR-G, PR-H, PR-I).
- Paper §5 — single canonical scenario walked end-to-end (PR-D).
- Reading paths appendix (PR-J).

### Trade-offs

The rc2 canvas redraw extends the SVG height by 150px and adds a 105px-tall row of four chips. The chips deliberately mirror SPECIFY's four-column grid for visual consistency with the rest of the canvas. The right-rail metrics column intentionally does NOT move into the EVOLVE row — keeping it on the right rail preserves the existing visual conceit that signals are continuous (always emitting) while the activity rows are sequential (each happens at a particular phase of the work).

### Why MAJOR-rc

This rc continues the v2.0.0 MAJOR line because the deck-side phases check goes from non-existent to enforcing five activities — a net new sync constraint. Decks or papers that had been authored against v1.x's four-activity assumption fail this check; that's the intended behavior. The version number stays in the rc-line until the prose work and the file-path renames land; v2.0.0 final ships when the rc series stabilizes.

### PRs

- **PR-A2** (this rc) — canvas redraw, deck activities slide, deck-side phase check, version markers, paper PDF rebuild.

---

## v2.0.0-rc1 — 2026-05-10

**MAJOR (release candidate)** — promotes *Evolve* from a closing-Validate sub-discipline to a peer fifth activity, introduces three running scenarios across the five activities, and reorganizes the book around the activity spine. This is the structural commit of the v2.0.0 line; the prose work for the Phase-5 chapters and the 15 scenario chapters lands in subsequent rcs (PR-B through PR-F per the rollout plan in PR-A's description). The canvas redraw to a five-row layout, the teaching-deck refresh, and any file-path renames are deferred to PR-A2 / PR-A3 within the v2.0.0-rc line.

### Why MAJOR

The cardinality of the framework's *activities* changes from four to five. Specs and deck/paper sync slides that hardcoded "four activities" become incorrect. The book's organizational spine changes from "Decisions / Spec / Agent / Oversight / Ship / Pilots / Patterns / Repertoires / Appendices" (nine Parts of mixed grain) to "Frame / Specify / Delegate / Validate / Evolve / Reference" (six Parts, one per activity plus the catalog). Per the versioning convention in the *How to use this file* section below, both changes are MAJOR-bump triggers.

### What did **not** change (the load-bearing commitments survived)

- Five archetypes: Advisor, Executor, Guardian, Synthesizer, Orchestrator.
- Four orthogonal calibration dimensions: Agency, Autonomy, Responsibility, Reversibility.
- Twelve canonical spec sections (with the Composition Declaration and Cost Posture sub-blocks in §4 introduced in v1.x).
- Seven fix-locus failure categories (Cat 1 Spec through Cat 7 Perceptual, with four sub-categories).
- Four oversight models.
- Four signal metrics.
- Eight pattern categories (~50 patterns).
- Composition as a first-class design surface (Patterns A–E).
- The Intent Design Session, the Discipline-Health Audit, and the honest accounting (3 novel / 4 not-claimed).

The framework's vocabulary and load-bearing commitments are unchanged; only the *spine* changed. v2.0.0 is a structural reshape, not a vocabulary breaking change. Existing v1.x specs remain valid; their references to "the four activities" become references to "the five activities" with *Evolve* added as the activity that closes the loop.

### Added

- **`SUMMARY.md` reshaped** around the five-activity spine. New Parts: Part 1 — FRAME, Part 2 — SPECIFY, Part 3 — DELEGATE, Part 4 — VALIDATE, Part 5 — EVOLVE, Part 6 — REFERENCE. Each of Parts 1–5 ends with three *in practice* chapters per phase (15 total), one for each running scenario. The legacy worked pilots in `examples/*` are kept under Part 6 — REFERENCE as superseded reference material; the running scenarios are the primary path.
- **15 scenario chapter stubs** under `src/{frame,specify,delegate,validate,evolve}/scenarios/{customer-support,coding-pipeline,docs-qa}.md`. Each stub names what the chapter will cover, links to its conceptual source chapters, links to the same scenario across all five phases, and points at the v1.x source material. Prose lands in PR-C (S1 customer-support), PR-E (S2 coding-pipeline), PR-F (S3 docs-qa).
- **2 new Phase-5 conceptual chapter stubs**: `src/evolve/01-closed-loop.md` (the discipline that opens Part 5) and `src/evolve/07-framework-versioning.md` (elevating the CHANGELOG discipline to a first-class chapter). Prose lands in PR-B.
- **`paper/check-deck-sync.py` `CANONICAL_PHASES`** added with the five activity names and a paper-side `check_phases` function. Deck-side check activates when an activities slide lands in the deck.
- **`introduction.md`** updated: five-activity bullet list (Evolve added), revised "what you will have at the end" list (now seven artifacts, with the closed-loop discipline as item 7), revised "How to use it" table with running-scenario entry points.
- **`appendices/glossary.md`** updated: the *Architecture of Intent* entry and the *Framework Version* entry both reference five activities; the version number on the *Framework Version* entry advances to **v2.0.0-rc1**.
- **`paper/architecture-of-intent.md`** status header advances to **v2.0.0-rc1** with the structural-change note; §3 figure caption acknowledges the canvas figure currently shows the v1.x four-activity layout pending the rc2 redraw.

### Deferred to a later v2.0.0-rc

- **Canvas redraw** (4 rows → 5 rows) — the SVG and PNG redraws to add an *Evolve* row. Deferred because the redraw is design-sensitive (rsvg-convert mismeasures Georgia bold; the existing canvas layout fits 1180px tightly) and warrants its own PR. Until then, the canvas figure shows the v1.x four-activity layout with prose annotations naming the gap.
- **Teaching-deck refresh** — the deck has no activities slide currently; when one is added, mirror it on the paper.
- **File-path renames** (e.g., `architecture/` → `frame/`) — the SUMMARY structure is filesystem-agnostic, so the path renames are pure filesystem-cleanup. Deferred because cross-reference updates across ~120 files are high-risk for the reader-facing improvement they produce (none — URLs change, but the reader experience is identical).
- **Phase-5 chapter prose** (rewriting `operating/*` chapters into the Evolve frame) — PR-B.
- **Three scenarios written in full** — PR-C, PR-E, PR-F.
- **Voice rewrites** for Parts 0–5 (vignette-before-exposition openings) — PR-G, PR-H, PR-I.
- **Paper §5** (single canonical scenario walked end-to-end) — PR-D, after PR-C lands.
- **Reading paths appendix** — PR-J.

### Trade-offs

The phased rollout means rc1 ships with the new *shape* visible (TOC, activity vocabulary, scenario-chapter scaffolding, version markers) but the new *prose* still pending. Readers who land on a scenario chapter at rc1 see a stub with a clear pointer to the v1.x worked pilot. This is intentional: the structural commit is large enough to merit its own diff, and gating it behind the prose work would couple two failure modes.

### PRs

- **PR-A** (this rc) — structural reshape, scenario stubs, sync-check phases, version markers.
- **PR-A2** (planned) — canvas redraw + deck refresh.
- **PR-B**–**PR-J** (planned) — Phase-5 prose, three scenarios, paper §5, voice passes, reading paths.

---

## v1.4.0 — 2026-05-10

**MINOR** — adds the *Cost Posture* sub-block to §4 of the canonical spec template, plus the structural framing that explains *why* cost is a §4 sub-block and not a fifth calibration dimension. No load-bearing commitment changed.

### Added

- **§4 Cost Posture sub-block** in [`src/sdd/07-canonical-spec-template.md`](src/sdd/07-canonical-spec-template.md), parallel to the existing Composition Declaration. Five fields: model-tier commitment per step, latency budget (p50/p95/p99 + behavior on breach), prompt-stability invariant, per-call cost ceiling (with breach behavior), cost-incident escalation. Required for systems running in production at any scale; omittable only at the [MVP-AoI](src/operating/16-minimum-viable-aoi.md) floor.
- **"Cost is not a fifth dimension" framing sub-section** in [`src/theory/03-agency-autonomy-responsibility.md`](src/theory/03-agency-autonomy-responsibility.md) that explains the working position with three structural reasons (cost is partially derived from the four dimensions; cost is a *resource* commitment whereas A/A/R/R are *behavioral* commitments; the lineage is thin — neither SAE J3016 nor Shavit & Agarwal treat cost as a dimension).
- **Paper §3.3 paragraph** giving the same structural rationale at paper grain.
- **Cost Posture** glossary entry under C (in proper alphabetical position between Context Provision and Delegation), naming the five fields and the resource-vs-behavioral distinction.
- New **Cost Posture sub-block** entry at the top of the Pattern Index *"My agent program's cost or latency isn't penciling"* By-Problem entry, with the framing-sub-section as the second link. Practitioners reaching for that By-Problem entry now see the upstream spec surface before the operational chapters.
- Light cross-references added from [Cost and Latency Engineering](src/operating/09-cost-and-latency.md) and [Cacheable Prompt Architecture](src/operating/14-cacheable-prompt-architecture.md) to the new §4 sub-block.

### Why this is MINOR, not MAJOR

The sub-block extends §4 alongside the existing Composition Declaration without changing any load-bearing commitment: the five archetypes, **four** dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are all unchanged. The four-dimension cardinality the deck/paper sync check enforces is unaffected. The orthogonality argument in paper §3.3 stands. The honest accounting in paper §1.3 ("3 novel / 4 not claimed") is unchanged because Cost Posture is presented as a *structural surface* on top of existing operational treatments (Cost & Latency Engineering, Cacheable Prompt Architecture), not as a novel claim.

### Why a §4 sub-block instead of a fifth dimension

The candidate alternative — promoting cost to a fifth calibration dimension alongside A/A/R/R — would have been a MAJOR bump (v1.3.0 → v2.0.0). It was rejected for three reasons documented in the new framing sub-section: (1) cost is partly *derived* from the four behavioral dimensions, conflating dial with derived quantity; (2) cost is a *resource* commitment whereas A/A/R/R are *behavioral* commitments — different category; (3) the lineage is thin — neither SAE J3016 nor Shavit & Agarwal treat cost as a dimension, so promoting it would require either a weak novelty claim or a manufactured citation. The §4 sub-block does the work the recommendation actually wanted done — give cost a structural upstream seat in the spec — without overclaiming. The Composition Declaration sub-block established the precedent: §4 can absorb structural commitments that aren't dimensions.

### PRs

- **#52** — Add Cost Posture sub-block to spec template §4; framing sub-section in theory/03 and paper §3.3

---

## v1.3.0 — 2026-05-10

**MINOR** — adds the *Minimum Viable Architecture of Intent* chapter (operating/16) without changing any load-bearing commitment.

### Added

- **[Minimum Viable Architecture of Intent](src/operating/16-minimum-viable-aoi.md)** — a new Operating Practice chapter at the end of the *Adoption* sub-section of Part 5, naming the floor of the discipline for systems too small to warrant the full Intent Design Session. The MVP is one page of structured text — archetype, scope (in and out), oversight commitment, one signal, escalation trigger — written in ~15 minutes. Applicable when the system is small across all five of audience, stakes (R1–R2), cohesion (one person), scale (bounded), and diagnosability (failures visible in real time). Five graduation triggers signal when the MVP should upgrade to the full IDS.
- New **Minimum Viable Architecture of Intent (MVP-AoI)** entry in the glossary under M.
- New *"My system is too small for the full framework"* By-Problem entry in the Pattern Index, distinguishing the MVP from the Miniature Pilot (which is the full canvas applied to small-but-production-bound systems).

### Why this is MINOR, not MAJOR

The chapter scales the discipline *down* without changing any load-bearing commitment: the five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are unchanged. The MVP is a *deliberately compressed* form of the discipline, not a separate framework. The deck/paper sync check is unaffected. No paper changes (the paper does not currently address the MVP angle; that may become a future paper-side addition).

### Distinction worth naming

The MVP-AoI is *not* a substitute for the [Miniature Pilot](src/miniature-pilot.md). The miniature pilot is the *full canvas* applied to a small but production-bound system; the MVP-AoI is a *deliberately compressed* discipline for systems below that production threshold. Both shapes are correct for their respective scopes; the distinction is named explicitly in both files.

### PRs

- **#51** — Add *Minimum Viable Architecture of Intent* chapter (operating/16)

---

## v1.2.0 — 2026-05-10

**MINOR** — adds the *What Changes for the Senior Engineer* chapter (theory/08) without changing any load-bearing commitment.

### Added

- **[What Changes for the Senior Engineer](src/theory/08-what-changes-for-senior-engineers.md)** — a new Foundations chapter at the end of Part 1 that responds to the question the [Prologue](src/prologue.md) raises but never resolves: *if late-judgment compensation was the senior engineer's value-add, what is the value-add now?* The chapter names where the judgment goes (Frame, Specify, Bind Patterns, Skeptic, Validate); names what is honestly lost (the flow state of late-judgment debugging, tribal knowledge as a moat, pure-implementation seniority, the practitioners who will not make the transition); names what is gained (authorship that compounds, durable artifacts, leverage across teams, a different kind of seniority); and names the career-ladder gap explicitly.
- New *"I'm a senior engineer wondering what this all means for me"* By-Problem entry in the Pattern Index, pointing at the Prologue, the new chapter, the IDS, and the RACI Card.

### Why this is MINOR, not MAJOR

The chapter extends the framework's vocabulary about *practitioner experience* without changing any load-bearing commitment: the five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are unchanged. The deck/paper sync check is unaffected. No paper changes (the paper does not currently address the senior-engineer angle; that may become a future paper-side addition).

### PRs

- **#50** — Add *What Changes for the Senior Engineer* chapter (theory/08)

---

## v1.1.0 — 2026-05-10

**MINOR** — adds the Roles & Responsibilities (RACI) Card appendix without changing any load-bearing commitment.

### Added

- **[Roles & Responsibilities (RACI) Card](src/appendices/raci-card.md)** — a one-page reference appendix that maps the seven canonical roles (domain owner, spec author, architect, builder, operator, reviewer, skeptic) against the six operational activities (Frame · Specify · Build · Oversee · Ship · Evolve). Standard RACI shorthand: R does the work, A owns the outcome (exactly one per activity), C is consulted before action, I is informed after. Five common patterns and five anti-patterns documented.
- New **RACI** entry in the glossary; new *RACI Card* row added to the *Roles & Responsibilities* governance entry of the Pattern Index.
- Light cross-references added from the [Intent Design Session](src/theory/07-intent-design-session.md) chapter (the IDS is where the RACI is *enacted* for one specific system; the card is the matrix the team enacts against), [Proportional Governance](src/operating/04-governance.md), and the [Adoption Playbook](src/operating/11-adoption-playbook.md).

### Why this is MINOR, not MAJOR

The card extends operational vocabulary without changing any load-bearing commitment: the five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are unchanged. The RACI's *six activities* are a finer-grained decomposition of the canvas's *four activities* for ownership-assignment purposes; both vocabularies remain correct for their respective purposes. The deck/paper sync check is unaffected.

### PRs

- **#49** — Add Roles & Responsibilities (RACI) Card

---

## v1.0.0 — 2026-05-10

The first stable release of the framework as documented in this book and its companion paper. Captures the framework's load-bearing commitments after the post-canvas review series.

### Load-bearing commitments

- **5 archetypes**: Advisor, Executor, Guardian, Synthesizer, Orchestrator.
- **4 orthogonal calibration dimensions**: Agency, Autonomy, Responsibility, Reversibility.
- **12 canonical spec sections** (with optional Composition Declaration sub-block in §4 for systems with embedded components or mode-switching).
- **7 fix-locus failure categories**: Cat 1 Spec, Cat 2 Capability, Cat 3 Scope Creep, Cat 4 Oversight, Cat 5 Compounding, Cat 6 Model-level, Cat 7 Perceptual (with four sub-categories: misidentification, missed element, hallucinated element, state miscount).
- **4 oversight models**: Monitoring, Periodic, Output Gate, Pre-authorized.
- **4 signal metrics**: spec-gap rate, first-pass validation, cost per correct outcome, oversight load.
- **8 pattern categories** (~50 patterns total): capability, integration, coordination, safety, observability, testing, state, deployment.
- **4 activities**: Frame, Specify, Delegate, Validate.
- **Composition as a first-class design surface**: Patterns A–E (Confirm-then-Act, Executor + Guardian, Orchestrator with typed sub-agents, Compose-then-Publish, Mode-switching for the 2026 pressure-point classes).

### Working practices

- **The Intent Design Session** — 7 phases, 5 required roles, 3–4 hours per system.
- **The Discipline-Health Audit** — 11 anti-patterns, 60 minutes per system per quarter.

### Honest accounting (from paper §1.3)

- **3 contributions claimed novel:**
  - Operationalization of agency vs. autonomy as orthogonal axes (extending Shavit & Agarwal 2023).
  - Fix-locus framing of the failure taxonomy (complementing Cemri et al.'s MAST symptom-locus partition).
  - Cat 7 (Perceptual Failure) for perceiving-then-acting agents (computer-use, browser-use, robotic).
- **4 contributions explicitly not claimed novel:**
  - SDD as a discipline (lineage from spec-kit and DevSquad).
  - Archetypes as a concept (lineage from Anthropic's *Building Effective Agents*).
  - The four dimensions individually (lineage from SAE J3016 and Shavit & Agarwal).
  - Cat 1–6 as categories (synthesis from common practice).

### What landed in the v1.0 line (the post-canvas review series)

| PR | Pass |
|---|---|
| #42 | The framework canvas — *Figure 1* of paper §3 and *The framework on one page* in the book Introduction |
| #43 | The one-page definition of *Architecture of Intent* at the front of the book Introduction |
| #44 | The Intent Design Session chapter (`theory/07`) — the 7-phase ritual that turns the framework from a vocabulary into a discipline |
| #45 | The opening miniature pilot (`miniature-pilot.md`) — the canvas applied to one concrete system in one screen |
| #46 | Composition first-class (Pattern E mode-switching + Composition Declaration sub-template) — the structural answer to the taxonomy-pressure question, with no sixth archetype |
| #47 | The anti-patterns chapter (`operating/15`) — Signs Your Architecture of Intent Is Degrading; the 11-anti-pattern catalog and the quarterly Discipline-Health Audit |

### Pre-v1.0 history

The book and paper accumulated incrementally through 2024–2025 across the prior 41 PRs. The canonical archetype framework, spec template, oversight models, and Cat 1–6 partition stabilized over that period; the Cat 7 (Perceptual) category, the canvas, and the working-practice chapters (Intent Design Session, anti-patterns) landed in the post-canvas series above.

Pre-v1.0 work is not version-tagged in this file; the git history is the record of that period.

---

## How to use this file

When opening a PR that touches load-bearing framework commitments:

1. Decide the bump (MAJOR / MINOR / PATCH).
2. Add an entry above this section under the new version.
3. Name what changed in one or two lines per item.
4. Tie the bump to the PR number.
5. Update the version mention in `README.md` and `paper/architecture-of-intent.md` if applicable.

Cosmetic changes (typo fixes, dead-link replacements, individual prose smoothing) can be batched into a single PATCH bump rather than each getting their own.
