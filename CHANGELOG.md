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

## v2.4.0 — 2026-05-10

**MINOR** — a focus-and-structure pass addressing five reviewer findings (focus drift in Part 5, the procedural shape of the Adoption Playbook, the ambiguous status of `foundations/08`, the Intent Design Session not anchored as the Foundations exit, and the absence of a §-by-§ pattern justification audit).

No load-bearing commitment moves. The deck/paper sync check remains green on all six named-fact families: 5 archetypes, 7 Cats, 4 Cat 7 sub-categories, 8 DevSquad phases, **5** activities, 3-novel/4-not-claimed honest accounting.

### Structural — Part 5 → Parts 5 + 6

The v2.3.0 rename to "EVOLVE & OPERATE" acknowledged that Operations sat inside Evolve but did not separate them. The agent-review pass found that Operations chapters (8 chapters, ~1,500 lines) outweighed core Evolve (3 chapters, ~800 lines) and diluted the activity-spine focus.

v2.4.0 splits them:

- **Part 5 — EVOLVE** keeps the closed-loop core:
  - `evolve/01-closed-loop.md`
  - `evolve/15-anti-patterns.md`
  - `evolve/07-framework-versioning.md`
  - `evolve/16-minimum-viable-aoi.md`
  - the 5 deployment patterns in `patterns/deployment/`
  - the 3 Evolve-phase running-scenario chapters in `evolve/scenarios/`
- **Part 6 — OPERATIONS** (new) collects the sustaining-ops chapters:
  - `operate/01-governance.md` (moved from `evolve/04-governance.md`)
  - `operate/02-cost-and-latency.md` (from `evolve/09-cost-and-latency.md`)
  - `operate/03-cacheable-prompt-architecture.md` (from `evolve/14-cacheable-prompt-architecture.md`)
  - `operate/04-production-telemetry.md` (from `evolve/10-production-telemetry.md`)
  - `operate/05-adoption-playbook.md` (from `evolve/11-adoption-playbook.md`)
  - `operate/06-devsquad-mapping.md` (from `evolve/12-devsquad-mapping.md`)
  - `operate/07-co-adoption-with-devsquad.md` (from `evolve/13-co-adoption-with-devsquad.md`)
- **Part 6 — REFERENCE** is renumbered **Part 7 — REFERENCE**.

Part 6 is explicitly *not* a sixth activity. The framework still commits to five activities; the new Part is the sustaining-ops layer that runs alongside them. The framing in the Introduction, the how-to-read table, and the Part 6 opener (`operate/01-governance.md`) all carry this commitment.

### Anchored — Intent Design Session as the Foundations exit

`foundations/07-intent-design-session.md` gains a "Why this is the Foundations exit" section above the existing Context block. The IDS is now framed explicitly as the ritual that turns Foundations vocabulary into work, with each subsequent Part elaborating one phase of the IDS.

Back-references added from each Part's opening chapter (Part 1 frame/02; Part 2 specify/01; Part 3 delegate/01; Part 4 validate/05; Part 5 evolve/01; Part 6 operate/01), using a consistent *Where this sits in the work:* prose pattern so readers recognize the navigational signal.

### Rewrote — Adoption Playbook leads with principles

`operate/05-adoption-playbook.md` gains a "Principles before the playbook" section between Forces and the procedural walkthrough. The four principles: (1) adoption compounds when focus is tight (one agent, one spec, one gap log); (2) demonstration beats mandate; (3) load-bearing parts (5 archetypes, 4 dimensions, 7 Cats, 4 oversight models, 12 spec sections, MVP-AoI) stay rigid; (4) the discipline is what survives the champion leaving. The "The Solution" header becomes "A concrete rhythm" so readers see the calendar walkthrough as one worked example, not the only valid form.

No content removed; the procedural sections still anchor a reader who needs something concrete to run on Monday.

### Clarified — `foundations/08` audience

`foundations/08-what-changes-for-senior-engineers.md` gains a "Who this chapter is for" section that names the asymmetry honestly: this is the one Foundations chapter with an audience-specific scope (a *career* question rather than a *system-design* question). Readers not personally navigating the transition can skip it on first read. The `how-to-read.md` Parts table gets a one-clause note on the same point.

### Added — Pattern Justification Map

`appendices/pattern-index.md` gains a new section titled "Pattern Justification Map" that audits all ~50 patterns against the canonical 12-section spec template plus §4's Composition Declaration sub-block. For each pattern, the map names the spec section(s) that *pull* it, and a one-line justification.

Audit result: all 50 patterns map cleanly. None are unjustified inventory. The density concentrates in §11 (Agent Execution Instructions), §8 (Authorization Boundary), and §6 (Invariants). §1 and §2 (framing sections) pull no patterns, which is correct.

Closing note in the map establishes the workflow for future contributors: write the justification row first; if you cannot name the spec section that pulls a new pattern, the pattern does not belong in the book.

### Wayfinding updates

- `src/SUMMARY.md` — Part 5/6/7 reorganization with new Part 6 — OPERATIONS section.
- `src/how-to-read.md` — the stale "Six Parts" v1.x table is replaced with an eight-Parts table reflecting the v2.4 structure.
- `src/introduction.md` — Part-by-Part paragraph rewritten for the new spine.
- `README.md` — "How it's organized" table updated; repository-layout tree adds `src/operate/`.
- `CLAUDE.md` — repo-structure tree updated; "Recent meaningful decisions" gains the v2.4.0 entry.
- `paper/architecture-of-intent.md` — Appendix B's DevSquad citations now point at `operate/` paths; the paper's status header is updated to v2.4.0 with a MINOR-bump explanation.

### Verification

- `python3 scripts/check-internal-links.py` — 0 broken
- `python3 scripts/check-orphans.py` — 0 orphans, 0 missing
- `python3 scripts/check-readme-paths.py` — clean
- `python3 paper/check-deck-sync.py` — all 6 checks pass (activities count = 5)

### Why MINOR, not MAJOR

No load-bearing commitment moves. The five activities, five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, composition first-class — all unchanged. Part 6 is an *addition* (a sustaining-ops layer that previously sat inside Part 5); the activity count it sits alongside is unchanged. The deck/paper sync check confirms this.

The chapter files moved on disk but every existing inbound link was rewritten; readers with bookmarks to chapter URLs (e.g., `evolve/04-governance.md`) will get 404s on those specific URLs. SUMMARY-anchor bookmarks to `#evolve--operate-*` will also break. These are presentational moves, not commitment moves.

---

## v2.3.1 — 2026-05-10

**PATCH** — collapses the legacy v1.x worked-pilots multi-chapter listing in Part 6 — Reference into a single *Legacy v1.x Worked Pilots Archive* appendix entry. Removes the "(legacy — superseded by phase scenarios in Parts 1–5)" parenthetical from the published TOC, which read as visible technical debt. The example files themselves are preserved; only the SUMMARY footprint shrinks.

### Added

- **`src/appendices/legacy-pilots.md`** — new archive appendix that introduces the three v1.x pilots (Customer Support, Code Generation Pipeline, Coding Agent), names what each pilot covers, links to every chapter of every pilot, names which v2.0.0 *in practice* scenario supersedes each one, and gives reading guidance ("don't start here unless you are evaluating how the framework matured between v1.x and v2.0").

### Removed from SUMMARY.md

- The flat-listed `## Worked Pilots (legacy — superseded by phase scenarios in Parts 1–5)` section with 17 chapter bullets is removed from Part 6 — Reference.
- Replaced by a single bullet *Legacy v1.x Worked Pilots Archive* under `## Appendices`, between *The Companion Paper* and *Reading List & References*.

### Preserved on disk

- `src/examples/00-how-to-use.md`
- `src/examples/01-ai-customer-support/` (6 files)
- `src/examples/02-code-generation-pipeline/` (5 files)
- `src/examples/03-coding-agent/` (6 files)

All 17 files are reachable from:

- The new `src/appendices/legacy-pilots.md` archive appendix (every chapter linked)
- `src/appendices/pattern-index.md` worked-examples table and by-problem section
- `src/appendices/references.md` citation table
- `src/frame/scenarios/customer-support.md` and `src/frame/scenarios/coding-pipeline.md` — both explicitly cite their v1.x predecessor for v1.x → v2.0 comparison
- `src/miniature-pilot.md`, `src/evolve/11-adoption-playbook.md`, `src/appendices/speckit-reference.md`, `src/appendices/companion-paper.md` — supplementary references

### Updated — orphan-check script

`scripts/check-orphans.py` now whitelists `examples/` as intentionally-not-in-SUMMARY. The script's purpose is to catch *forgotten* orphans; intentionally-archived files reachable through the appendix should not trigger an error. The whitelist is documented in a comment naming the archive intent.

### Updated — wayfinding

- `src/introduction.md` — the "Looking at a v1.x worked pilot (legacy)" row of the *Where to start* table now points at the archive appendix rather than directly at one specific pilot.
- `src/how-to-read.md` — the "Looking at a real example" row reordered to recommend the v2.0.0 running scenarios first, with the v1.x archive as the secondary option.

### Verification

- `python3 scripts/check-internal-links.py` — 0 broken
- `python3 scripts/check-orphans.py` — 0 orphans, 0 missing (with `examples/` whitelisted)
- `python3 paper/check-deck-sync.py` — all 6 checks pass

### Updated — version markers

Version markers advanced from **v2.3.0** to **v2.3.1** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).

### Why PATCH, not MINOR

The change is a navigation refinement. No new chapters; no removed content; no load-bearing commitment moves. The 17 example files keep their paths so all inbound links (~40 of them across pattern-index, references, scenarios, and supplementary chapters) continue to resolve. The reader's experience changes only at the SUMMARY level — Part 6 is shorter and the "(legacy — superseded by…)" mid-renovation parenthetical is gone — and the change is reversible by restoring the SUMMARY entries.

### Trade-off honesty

External readers who bookmarked the SUMMARY anchor *#worked-pilots-legacy-superseded-by-phase-scenarios-in-parts-15* will get a 404 on that anchor; the chapter URLs themselves are unchanged. The new appendix anchor *#legacy-v1x-worked-pilots-archive* is the replacement.

---

## v2.3.0 — 2026-05-10

**MINOR** — renames book Part 5 from "EVOLVE" to "EVOLVE & OPERATE" and reorganizes its 11 chapters plus Deployment Patterns into three reader-facing sub-sections. Closes the "Part 5 is doing two jobs" critique by acknowledging the dual scope in the Part name and grouping the chapters by which job they serve. The framework retains its five activities; the rename is a *book navigation* change, not a *framework commitment* change.

### Renamed

- **Part 5 — EVOLVE** → **Part 5 — EVOLVE & OPERATE**

### Restructured — SUMMARY.md

The 11 Part 5 chapters and 5 deployment patterns were reorganized from a flat list into three sub-sections by the time-scale and concern they serve:

**Evolution** — what changes about the system over time (per-incident through per-year):
- The Closed Loop: From Failures to Spec Amendments
- Signs Your Architecture of Intent Is Degrading
- Framework Versioning

**Deployment Patterns** — the patterns that make changes safe (between Evolution and Operations because each pattern enables a structural change):
- Canary Deployment
- Rollback on Failure
- Spec Versioning
- Model Upgrade Validation
- Agent Deprecation Path

**Operations** — what runs the system day to day:
- Proportional Governance
- Cost and Latency Engineering
- Cacheable Prompt Architecture
- Production Telemetry
- Adoption Playbook
- Minimum Viable Architecture of Intent
- Mapping the Framework to the DevSquad 8-Phase Cadence
- Co-adoption with DevSquad Copilot

The scenario sub-section is renamed **Evolve & Operate in practice** for symmetry with other Parts' *<Part> in practice* convention.

### Updated — chapter subtitles and prose

- All 11 Part 5 chapter subtitles updated from `**Part 5 — Evolve**` to `**Part 5 — Evolve & Operate**`. The 11 *Where this sits in v2.0.0* callout block-quotes updated similarly.
- Three Evolve scenario chapter subtitles updated from `**Part 5 · EVOLVE · Scenario N of 3**` to `**Part 5 · EVOLVE & OPERATE · Scenario N of 3**`. Three Evolve scenario H1 titles updated from `# Evolve in practice — ...` to `# Evolve & Operate in practice — ...`.
- Twelve scenario reading-path tables across Parts 1–5 updated their bottom-row link text from "Evolve in practice — …" to "Evolve & Operate in practice — …" while keeping the column label "5. Evolve" (the activity name is unchanged in the framework).
- `src/evolve/07-framework-versioning.md` "Where this chapter sits in Part 5" prose rewritten to reflect the new sub-section ordering: framework versioning now closes the Evolution sub-section rather than sitting "near the end of Part 5", and its time-scale-gradient claim is relocalized to the Evolution sub-section ordering.
- `src/introduction.md` Part 5 description rewritten to introduce the Evolution / Operations sub-section split and to name explicitly that the framework retains five activities while the book Part covers two adjacent jobs.
- `src/appendices/reading-paths.md` four references to "Part 5 — EVOLVE" updated; "Evolve in practice" italics updated to "Evolve & Operate in practice".

### Verification

- `python3 scripts/check-internal-links.py` — 0 broken
- `python3 scripts/check-orphans.py` — 0 orphans, 0 missing
- `python3 paper/check-deck-sync.py` — all 6 checks pass; the framework activity count remains 5 (Frame, Specify, Delegate, Validate, Evolve)

### Why MINOR, not PATCH or MAJOR

- Not PATCH because the change is structural, not prose-only — it adds new SUMMARY sub-section structure inside Part 5 and renames the Part itself.
- Not MAJOR because no load-bearing commitment changes: the five activities remain five (Operate is treated as a slice of Evolve, not promoted to a peer activity); the deck/paper sync contract is unaffected; existing specs and existing adoption are unbroken; the canvas figure's five-row spine is unchanged. The change is a book-navigation refinement, not a framework-commitment change.

### Why "Evolve & Operate" rather than promoting Operate to a sixth activity

Promoting Operate to a peer activity would be a MAJOR change: it would re-cardinalize the activity count from five to six, force a redesign of the canvas figure, change the deck/paper sync contract, and break every existing spec that names "the five activities". The honest read is that ongoing operations *are* part of evolving a deployed system — there is no clean line between "the team is operating today" and "the team is evolving today" because the same closed loop runs continuously. The Part rename acknowledges the dual scope without forcing the framework to grow a sixth peer.

### Trade-off honesty

External readers who bookmarked the URL of the **Part 5 — EVOLVE** SUMMARY anchor may experience confusion when the rendered HTML now reads **Part 5 — EVOLVE & OPERATE**. Chapter URLs are unchanged (no file moves; no path renames). Internal links resolve identically.

---

## v2.2.3 — 2026-05-10

**PATCH** — closes the filesystem cleanup begun in v2.2.2 by renaming `src/theory/` → `src/foundations/` so the Part 0 directory matches its Part label. After v2.2.2, the five Part-aligned directories (`frame/`, `specify/`, `delegate/`, `validate/`, `evolve/`) already matched their Part labels; Part 0's `theory/` was the one outlier explicitly deferred at v2.2.2. v2.2.3 closes that gap. No load-bearing commitments change; no impact on the paper's structure.

### Renamed

| v2.2.2 path | v2.2.3 path | Rationale |
|---|---|---|
| `src/theory/` | `src/foundations/` | Directory name now matches the Part 0 — Foundations label |

The six chapters keep their stems (`01-what-is-aoi.md`, `02-intent-vs-implementation.md`, `03-agency-autonomy-responsibility.md`, `05-failure-as-design-signal.md`, `07-intent-design-session.md`, `08-what-changes-for-senior-engineers.md`); only the directory changed.

### Cross-reference updates

**~170 cross-references updated** across the book and CLAUDE.md via `sed` for the path-prefix replacement. 57 files touched: SUMMARY.md, the six moved chapters themselves, 49 other book chapters that link into Part 0, four appendices, README, CHANGELOG (v2.2.2 retrospective entry preserved historically — see below), and CLAUDE.md.

The paper has no `theory/` references (it cites the book by repository URL, not by source-tree path), so the paper Markdown source is unchanged except for the framework-version header bump.

### Verification

- `python3 scripts/check-internal-links.py` — 0 broken
- `python3 scripts/check-orphans.py` — 0 orphans, 0 missing

### Updated — version markers

Version markers advanced from **v2.2.2** to **v2.2.3** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).

### Updated — CLAUDE.md repo-structure tree

The repo-structure tree in CLAUDE.md was stale beyond just `theory/` — it still listed `src/architecture/`, `src/sdd/`, `src/agents/`, `src/operating/`, all of which were absorbed into the phase-aligned directories at v2.2.2. v2.2.3 brings the tree current: each Part directory is shown with its scenarios subdirectory and a brief description; legacy worked-pilot status is named explicitly. The file-numbering note's example was also refreshed (`foundations/` and `evolve/` gaps documented).

### Why PATCH, not MINOR

Same reasoning as v2.2.2: this is purely cosmetic at the filesystem layer. The book's content is unchanged; the SUMMARY structure is unchanged; the rendered HTML structure is identical except for URL paths. Per the versioning convention, PATCH is the right shape.

### Trade-off honesty

Existing deep links to `src/theory/...` paths break with this release. There are no redirects (same v2.2.2 reasoning: mdBook doesn't support native redirects, and the v2.2.x line has not committed to a redirect-management strategy). External readers who bookmarked Part 0 chapter URLs at v1.x or v2.0–v2.2.2 will see 404s and need to re-navigate from the SUMMARY.

### Note on historical CHANGELOG entries

The path-rename `sed` swept the entire repo, including older CHANGELOG entries that referenced `src/theory/...` historically. Two structurally important lines in the v2.2.2 entry — where v2.2.2 explicitly stated it was *not* renaming `src/theory/` — have been restored to their historical wording with a forward-pointer to v2.2.3. Other historical mentions of `theory/...` paths in v2.0.0 / v2.1.0 / v2.2.0 entries have been left as-is at the new path; the file references still resolve to current files, and recovering the precise wording of older entries adds noise without adding signal. The v2.2.2 entry's unique value was its statement that the rename was deferred — that needed preserving.

---

## v2.2.2 — 2026-05-10

**PATCH** — filesystem cleanup. Chapter directories renamed to match the v2.0+ Part placement, closing the file-path-rename item that has been deferred since rc1. No reader-facing change beyond URL stability for deep links; SUMMARY-driven navigation is identical. No load-bearing commitments change; no impact on the paper's structure.

### Renamed — directory structure

| v1.x / v2.x path | v2.2.2 path | Rationale |
|---|---|---|
| `src/architecture/` | `src/frame/` | All chapters live in Part 1 — FRAME |
| `src/sdd/` | `src/specify/` | All chapters live in Part 2 — SPECIFY |
| `src/agents/` | `src/delegate/` | All chapters live in Part 3 — DELEGATE |
| `src/operating/05–08` | `src/validate/05–08` | Intent Review / Signal Metrics / Evals / Red-Team — Part 4 — VALIDATE |
| `src/operating/04, 09–16` | `src/evolve/04, 09–16` | Governance / Cost / Telemetry / Adoption / DevSquad / Anti-patterns / MVP-AoI — Part 5 — EVOLVE |

The directory names now match their Part labels. The chapter file numbering is preserved across all moves: `architecture/02-canonical-intent-archetypes.md` becomes `frame/02-canonical-intent-archetypes.md` (same stem, new directory).

### Subdirectories preserved

- `src/frame/archetypes/` retains the five archetype subchapters (advisor, executor, guardian, synthesizer, orchestrator) that were `src/architecture/archetypes/`
- `src/delegate/mcp/` retains the three MCP subchapters that were `src/agents/mcp/`
- `src/frame/scenarios/`, `src/specify/scenarios/`, `src/delegate/scenarios/`, `src/validate/scenarios/`, `src/evolve/scenarios/` were already present from PR-A; the directory rename merges existing scenario chapters with the relocated conceptual chapters into the same Part directory

### Unchanged

- `src/theory/` retains the Part 0 — Foundations chapters (intentionally for v2.2.2; theory/ is a reasonable name for foundations material, and Part 0 is the one Part where the directory name doesn't perfectly match the Part label — that's a deferrable polish, not a v2.2.2 target). *(Renamed to `src/foundations/` in v2.2.3.)*
- `src/repertoires/`, `src/patterns/`, `src/examples/`, `src/appendices/`, `src/images/`, top-level `cover.md` / `introduction.md` / `miniature-pilot.md` / `how-to-read.md` / `prologue.md` / `SUMMARY.md` — unchanged, all referenced from across multiple Parts and not phase-specific

### Cross-reference updates

**~580 cross-references updated** across the book and paper via `git mv` for file moves and `sed` for path-prefix replacement. Two passes required:

1. **First pass** — replace `architecture/` → `frame/`, `sdd/` → `specify/`, `agents/` → `delegate/` plus per-file replacements for the 13 `operating/*.md` files that split between `validate/` and `evolve/`.
2. **Second pass** — fix bare-relative links that were intra-`operating/` (e.g., `evolve/11-adoption-playbook.md` linking to `06-metrics.md`, which moved to `validate/06-metrics.md`). 33 such bare-relative links became cross-directory after the operating split and required `../validate/` or `../evolve/` prefixes.

### Verification

- `python3 scripts/check-internal-links.py` — 0 broken (after both sed passes)
- `python3 scripts/check-orphans.py` — 0 orphans, 0 missing
- `python3 paper/check-deck-sync.py` — all 6 checks pass

### Updated — version markers

Version markers advanced from **v2.2.1** to **v2.2.2** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header). `paper/architecture-of-intent.pdf` recompiled.

### Why PATCH, not MINOR

This is purely cosmetic at the filesystem layer. The book's content is unchanged; the SUMMARY structure is unchanged; the rendered HTML structure is identical. What changes is which directory each chapter file lives in. Per the versioning convention, PATCH is the right shape.

### Trade-off honesty

Existing deep links to `architecture/`, `sdd/`, `agents/`, `operating/` paths break with this release. There are no redirects (mdBook doesn't support native redirects, and the v2.2.x line has not committed to a redirect-management strategy). External readers who bookmarked specific chapter URLs at v1.x or v2.0–v2.2.1 will see 404s and need to re-navigate from the SUMMARY. This is the trade-off that justified deferring the rename for 8 release candidates plus three stable releases; the cost is taken now to align the filesystem with the Part vocabulary going forward.

### Deferred (and possibly indefinite)

- Renaming `src/theory/` → `src/foundations/` to match Part 0's label. *(Resolved in v2.2.3.)*
- Adding redirects from old paths to new paths via an mdBook preprocessor. Possibly v2.2.3 if reader feedback indicates the link rot is meaningful.

---

## v2.2.1 — 2026-05-10

**PATCH** — three small refinements on top of v2.2.0 stable: paper ↔ book cross-references, voice pass on the five archetype subchapters, and a sharpening of paper §1.1–1.2's empirical-claim prose. No load-bearing commitments change.

### Added — paper ↔ book cross-references

Paper §4.3 (*Coding agents*) and book Scenario 2 (the worked coding-pipeline walkthrough) didn't previously reference each other directly. Both are about the same agent class, at different grain — §4.3 is paper-grade analysis at vocabulary level, S2 is book-grade walkthrough at scenario level — and a reader landing on either should be able to find the other. Fixed:

- **`paper/architecture-of-intent.md` §4.3** — new closing subsection *"Worked instantiation"* that points readers at S2 in the companion book for the end-to-end walkthrough, and notes that §5 of the paper itself condenses S1 (customer-support) at paper grain.
- The book's S2 chapters already reference *"paper §4.3"* in their Frame chapter; this rc completes the bidirectional link.

### Added — vignettes on the five archetype subchapters

The five archetype subchapters (`src/architecture/archetypes/{advisor,executor,guardian,synthesizer,orchestrator}.md`) are the most-cited reference chapters in the book — readers land on them from the [Pick an Archetype](src/architecture/02-canonical-intent-archetypes.md) decision tree, from scenario chapters, from the glossary, and from cross-references throughout. Until v2.2.1 they had definition-style openings (Identity / Defining Characteristic) without scene-setting. This rc adds vignette-before-exposition openings to all five, in the same shape as the rc8 / v2.0.1 voice passes:

- **Advisor** — opens on a Frame review where the team can't agree whether *"summarizes the meeting and emails the summary"* is an Advisor or an Executor; the answer is whichever the spec commits to in §3.
- **Executor** — opens on **archetype drift in action**: an agent's authorized scope expands silently as the team's *interpretation* of the rules grows, until a new engineer notices the cross-repo edit two months later. Cross-references S1 and S2 as worked Executor instantiations.
- **Guardian** — opens on the day-51 customer-support incident where the Guardian fired correctly but the failure was downstream in the review-and-action handoff. Cross-references S1's Evolve chapter for the resolution.
- **Synthesizer** — opens on **citation theater**: a docs Q&A agent's confident summary with technically-grounded citations that, read in full context, complicate rather than support the answer. Cross-references the [Discipline-Health Audit](src/operating/15-anti-patterns.md) and S3.
- **Orchestrator** — opens on the *"is this an Orchestrator coordinating four sub-agents, or an Executor with mode-switching?"* debate that recurs for coding agents. Cross-references S2's Frame chapter, where the team explicitly considers and rejects the Orchestrator framing.

Subtitles updated from the v1.x *"Governance & Architecture"* to **`Part 1 — Frame`** to match the v2.0+ Part placement.

### Updated — paper §1.1–1.2 honest-citation pass

The paper's §1.1–1.2 previously claimed *"Emerging 2026 evaluations of help-seeking behavior in agents... find that frontier models perform well on fully specified tasks but collapse on tasks that should trigger clarification"* — a placeholder gesture toward an empirical literature without specific benchmark citations. Sharpened in this rc:

- **The structural argument leads.** Reordered prose so the RLHF-reward-shape argument (completion is rewarded; pausing is ambiguously rewarded; one-shotting becomes the high-probability default) is the paper's primary claim. The paper's structural commitment doesn't require empirical backfill to stand.
- **The empirical claim is softened to *"consistent with practitioner observations across deployments"*** — accurate, and doesn't overclaim.
- **The citation gap is named explicitly.** New sentence: *"We have chosen not to ground this empirical claim in specific benchmark citations because the help-seeking-behavior evaluation literature is still emerging in 2026 and we are not aware of an established benchmark we can defensibly cite without overclaiming. The structural argument from the reward shape is what the paper rests on; benchmark-citation backfill remains a deferred refinement when the literature stabilizes."*
- **No fabricated citations added.** Specific benchmark names (*HiL-Bench*-class, etc.) are deliberately *not* invented. Honest accounting holds.

### Updated — version markers

Version markers advanced from **v2.2.0** to **v2.2.1** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header). `paper/architecture-of-intent.pdf` recompiled.

### Why PATCH

All three changes are prose-and-cross-reference refinements. No structural changes; no load-bearing list changes; no spec-template changes. Existing v2.2.x deployments continue to validate against the same vocabulary.

### Open follow-up

The benchmark-citation backfill in paper §1.1–1.2 remains an open task. If a future contributor (or the maintainer) nominates verified sources for the help-seeking-behavior empirical claim — peer-reviewed papers, established benchmarks with published evaluation results, or named practitioner reports — the paper can cite them directly and remove the *"deferred refinement"* acknowledgment. Until then, the structural argument carries the section.

---

## v2.2.0 — 2026-05-10

**MINOR** — restores **Part 0 — Foundations** as a six-chapter conceptual preface. Closes the one structural delta between the original v2.0.0 proposal and what shipped: Part 0 was dissolved during rc1 planning to avoid front-loading definitions before the first scenario; v2.2.0 brings it back as an explicit Part for readers who want the foundations co-located. No load-bearing commitments change; no impact on the paper's structure.

### Why MINOR, not MAJOR

Adding a Part is a *navigation addition*. Existing v2.1.x specs continue to validate; no spec hardcodes the Part structure. The chapters that move into Part 0 keep their file paths (only their SUMMARY placement and chapter subtitles change), so existing deep links continue to resolve. Per the versioning convention, MINOR is the right shape.

### Added

- **`src/foundations/01-what-is-aoi.md`** — new chapter *What is the Architecture of Intent?*, extracted from the *What is AoI?* section that previously lived inside the Introduction. Re-cast as a standalone chapter with a Part 0 subtitle, an epigraph, and a *Where to go next* closing section that lists the rest of Part 0 in order plus pointers to the canvas, the IDS, the miniature pilot, and the Reading Paths appendix.

### Updated — SUMMARY structure

`src/SUMMARY.md` reshaped to add **Part 0 — FOUNDATIONS** between the Foreword and Part 1. The new Part lists six chapters:

1. [What is the Architecture of Intent?](src/foundations/01-what-is-aoi.md) *(new)*
2. [Intent vs. Implementation](src/foundations/02-intent-vs-implementation.md) *(was Part 1)*
3. [Calibrate Agency, Autonomy, Responsibility, Reversibility](src/foundations/03-agency-autonomy-responsibility.md) *(was Part 1)*
4. [Failure Modes and How to Diagnose Them](src/foundations/05-failure-as-design-signal.md) *(was Part 4 opener)*
5. [What Changes for the Senior Engineer](src/foundations/08-what-changes-for-senior-engineers.md) *(was Foreword)*
6. [The Intent Design Session](src/foundations/07-intent-design-session.md) *(was Part 2)*

Removed from their previous Parts:
- Foreword: now contains only the Prologue (Senior Engineer relocated to Part 0).
- Part 1 — FRAME: Intent vs. Implementation and Calibrate A/A/R/R relocated to Part 0. Part 1 now opens with [Pick an Archetype](src/architecture/02-canonical-intent-archetypes.md), which is appropriate for the Frame Part (the chapter is about *picking the shape*).
- Part 2 — SPECIFY: The Intent Design Session relocated to Part 0. The IDS is the bridge between framework vocabulary and per-system spec; it sits more naturally in Foundations than in Specify.
- Part 4 — VALIDATE: Failure Modes relocated to Part 0. Part 4 now opens with [Intent Review Before Output Review](src/operating/05-reviewing-intent.md). Part 4's Part-italic intro now notes that the Cat 1–7 taxonomy itself lives in Part 0 since it's referenced from every Part; Part 4 is about applying it in operation.

### Updated — chapter subtitles and Part-framing prose

- Subtitles in the five moved chapters updated to **`**Part 0 — Foundations**`**: foundations/02, 03, 05, 07, 08.
- `foundations/05`'s Part-framing intro paragraph (added in rc8 / v2.0.1) updated to reflect the Part 0 placement: *"This chapter sits in Part 0 — Foundations because the seven-category fix-locus taxonomy is referenced from every Part."*

### Updated — Introduction

The Introduction's *What is the Architecture of Intent?* section (~25 lines of definition-style content) is removed; the intro now points readers at [Part 0's *What is AoI?* chapter](src/foundations/01-what-is-aoi.md) for the canonical definition. The Introduction keeps its *Why this book exists*, *The framework on one page* (canvas), *What you will have at the end*, *Who this is for*, *How to use it*, *What the book does not promise*, *Honest scope*, and *A note on style* sections.

### Updated — Reading Paths appendix

- The *linear field-guide read* path now lists Part 0 as step 3 (after Foreword and Introduction) before Parts 1–5.
- The *conceptual-only read* path simplifies to *"read all of Part 0 in order, plus a few additional binding chapters"* — Part 0's existence makes the path much shorter to describe.

### Updated — version markers

Version markers advanced from **v2.1.0** to **v2.2.0** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header). `paper/architecture-of-intent.pdf` recompiled.

### What did *not* change

- **No file paths changed.** The five moved chapters keep their `src/foundations/0N-*.md` paths; only their SUMMARY placement and chapter subtitle changed. All deep links to those chapters from elsewhere in the book continue to resolve.
- **No load-bearing commitments changed.** Five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, five activities, twelve spec sections, eight pattern categories, twelve anti-patterns, composition first-class — all unchanged.
- **No impact on the paper.** The paper's structure (sections 1–8, plus appendices) is unchanged; only the status-header version updated.

### Reader-experience trade-off, named

The original argument for dissolving Part 0 (rc1, 2026-05-10) was *first-encounter experience over reference utility* — opening with ~30 pages of definitions before the first scenario was the "lecture before story" pattern the field-guide voice was trying to escape. v2.2.0 restores Part 0 with the trade-off acknowledged: linear readers now encounter Foundations chapters before the first *Frame in practice* scenario, but the [Reading Paths appendix](src/appendices/reading-paths.md) provides scenario-first paths for readers who want the operational color first. The trade-off is now *named in both directions* rather than chosen one way silently.

### Deferred (unchanged from v2.1.0's plan)

- File-path renames (`architecture/` → `frame/`, etc.)
- Vignettes on the remaining v1.x chapters

---

## v2.1.0 — 2026-05-10

**MINOR** — elevates *citation theater* from a team-proposed addition to the framework's Discipline-Health Audit catalog as anti-pattern #6 in cluster 1 (*form without function*). The proposal originated in [Scenario 3's Evolve chapter](src/evolve/scenarios/docs-qa.md) at the docs-platform team's day-90 audit. Adopting it as a framework-level anti-pattern is the **closed loop running at framework grain** — the same discipline that takes per-system Cat 1s back to spec, taking team-proposed catalog additions back to the framework. No other load-bearing commitments change.

### Why MINOR, not MAJOR

Adding a catalog entry is an *addition*. It does not break existing v2.0.x specs because no spec hardcodes the anti-pattern count. The audit's existing 11 entries continue to produce the same verdicts on existing systems; the new 12th entry simply records *not applicable* for non-Synthesizer-flavored systems. Per the versioning convention, MINOR is the right shape.

### Added

- **`src/operating/15-anti-patterns.md`** — new anti-pattern entry **6. Citation theater** in cluster 1 (*form without function*), placed after *Calibration without commitment*. The entry follows the existing format (*The shape*, *The signs*, *The fix*) plus a closing *Applies primarily to* note that scopes the anti-pattern to Synthesizer-flavored systems and cross-references its origin in S3.
  
  Existing anti-patterns in the chapter renumbered to accommodate the insertion: 6→7, 7→8, 8→9, 9→10, 10→11, 11→12. Cluster headings (cluster 2 — drift, cluster 3 — process degradation) unchanged; only the within-catalog numbering shifted.

### Updated

- **Catalog cardinality references** updated from "11 anti-patterns" / "eleven anti-patterns" to "12 anti-patterns" / "twelve anti-patterns" across the book and paper, in:
  - `src/operating/15-anti-patterns.md` — the *Where this sits in v2.0.0* intro paragraph and the *Running a discipline-health audit* closing section
  - `src/appendices/pattern-index.md` — two cross-reference rows
  - `src/evolve/01-closed-loop.md` — the per-quarter time-scale paragraph
  - `src/operating/16-minimum-viable-aoi.md` — the *full framework* enumeration
  - `paper/architecture-of-intent.md` — the §5.5 audit-walkthrough sentence
  - `paper/figures/architecture-of-intent-canvas.svg` — the *Discipline-Health Audit* practice chip in the EVOLVE row
- **Canvas PNG regenerated** at 1600×1330 from the updated SVG, mirrored to `src/images/architecture-of-intent-canvas.png`.
- **Three running scenarios' audit tables** updated to use the v2.1 catalog numbering:
  - **`src/evolve/scenarios/customer-support.md`** — added row #6 *Citation theater* with verdict *Not applicable* (Executor archetype); existing rows 6–11 renumbered to 7–12. Intro paragraph notes the catalog-state expectation.
  - **`src/evolve/scenarios/coding-pipeline.md`** — same shape as S1 (Executor with mode-switching; citation theater is N/A).
  - **`src/evolve/scenarios/docs-qa.md`** — the *(NEW)* row that previously sat outside the numbered table is now row #6 in the catalog with verdict *Early signs* and notes preserved verbatim. Closing prose updated: the team's proposal is named as having *been adopted in v2.1.0* rather than as still pending.
- **Glossary's Discipline-Health Audit entry** updated: citation theater inserted into the comma-separated anti-pattern list with a *(Synthesizer-specific; added at v2.1.0)* parenthetical, and the verdict vocabulary expanded from *not present / early signs / active* to include *not applicable* for catalog entries that don't apply to a system's archetype.

### Updated — version markers

Version markers advanced from **v2.0.1** to **v2.1.0** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header). `paper/architecture-of-intent.pdf` recompiled.

### The closed loop at framework grain

This release demonstrates a discipline the framework names but had not previously executed at the framework's own level: **the closed loop applied to the framework itself.** The S3 docs-qa team ran their day-90 Discipline-Health Audit, found a pattern the existing 11-anti-pattern catalog didn't cover, proposed it back to the framework via repository discussion, and the framework adopted it. The same loop — diagnose → categorize → trace to fix locus → amend the structural artifact → record in the evolution log — runs at the per-system level (the spec evolution log) and at the framework level (this CHANGELOG). v2.1.0 is the framework's own *Cat 1 fix* in operation, with the spec evolution log being the CHANGELOG and the prior text being the v2.0 catalog of 11 anti-patterns.

### Deferred (unchanged from v2.0.1's plan)

- File-path renames (`architecture/` → `frame/`, etc.)
- Vignettes on the remaining v1.x chapters (~6 conceptual chapters across `sdd/01–06`, `agents/01–05`, `architecture/03/04/06/07` could still benefit)

---

## v2.0.1 — 2026-05-10

**PATCH** — voice-pass round 2 and Part-framing-intro completion on top of v2.0.0 stable. Adds vignette-before-exposition openings to four high-prominence conceptual chapters that didn't get the v2.0.0 voice pass, and Part-framing intros to eight operating chapters that didn't get them in v2.0.0. No load-bearing framework changes.

### Added — vignettes

Four conceptual chapters get a short scene before the existing Context section:

- **`src/foundations/05-failure-as-design-signal.md`** — opens on a Wednesday-morning post-incident review where the team's first reaction is *"the model hallucinated"* and the on-call engineer reframes: *"the model didn't hallucinate. The trace shows the model emitted the right tool call. The Guardian wrap wasn't bound on this code path."* Also fixes the chapter's outdated *"This chapter sits in Decisions"* note (now correctly Part 4 — Validate).
- **`src/foundations/07-intent-design-session.md`** — opens on 9 AM Monday, the team about to skip the IDS and start typing the spec, the tech lead stopping them: *"We're skipping a step. Read the framework, write the spec — that's the failure pattern Part 1 named. We need the session in between."*
- **`src/sdd/07-canonical-spec-template.md`** — opens on a team finishing Frame, the cursor sitting at §1 of an empty 12-section template, the question *"where do I start?"* The chapter then names the structural-commitments-first answer.
- **`src/agents/06-human-oversight-models.md`** — opens on a team in Frame disputing autonomy, until they realize the autonomy debate is actually an oversight debate — and oversight has four named models, not a sliding scale.

### Added — Part-framing intros

Eight operating chapters get a short *Where this sits in v2.0.0* paragraph after the epigraph, anchoring them in their activity:

**Part 4 — Validate:**
- **`src/operating/05-reviewing-intent.md`** — intent review as the upstream complement to the closed loop
- **`src/operating/06-metrics.md`** — the four signal metrics across three time-scales
- **`src/operating/07-evals-and-benchmarks.md`** — evals as the spec-conformance discipline; cross-references the running scenarios
- **`src/operating/08-red-team-protocol.md`** — red-team as the validation surface the eval suite doesn't cover

**Part 5 — Evolve:**
- **`src/operating/10-production-telemetry.md`** — telemetry as the trace surface the closed loop requires
- **`src/operating/12-devsquad-mapping.md`** — vocabulary-grain version of the AoI ↔ DevSquad mapping; cross-references Scenario 3
- **`src/operating/13-co-adoption-with-devsquad.md`** — co-adoption recommendation; cross-references Scenario 3
- **`src/operating/14-cacheable-prompt-architecture.md`** — caching as the prompt-stability invariant for §4 Cost Posture; cross-references Scenario 1's day-47 incident

### Updated

- Version markers advanced from **v2.0.0** to **v2.0.1** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the v2.0.1 status header.

### Why PATCH, not MINOR

This is a prose-and-orientation refinement: vignettes and Part-framing intros that surface what's already in the chapters more legibly. The framework's load-bearing commitments are unchanged; existing v2.0.0 specs continue to validate against the same vocabulary. PATCH is the right shape per the versioning convention.

### Deferred (unchanged from v2.0.0's plan)

- File-path renames (`architecture/` → `frame/`, etc.)
- Vignettes on the remaining v1.x chapters (~6 conceptual chapters across `sdd/01–06`, `agents/01–05`, `architecture/03/04/06/07` could still benefit; this rc covered the highest-prominence remaining 4)
- Elevating S3's team-proposed *citation theater* anti-pattern to the framework's catalog as a 12th anti-pattern — would be a v2.1 MINOR addition; queued as the next release after v2.0.1

---

## v2.0.0 — 2026-05-10

**MAJOR (stable)** — graduates the v2.0.0 release-candidate series (rc1–rc8) to stable. Adds the *Reading Paths* appendix as the navigation aid for readers picking their entry point, and bumps version markers from `v2.0.0-rc8` to `v2.0.0`. No load-bearing framework changes from rc8; this is the publication of the v2.0 line.

### Added

- **`src/appendices/reading-paths.md` — new navigation appendix.** Eight reader entry points, each with the chapter sequence and the time estimate: (1) the linear field-guide read, (2/3/4) the three scenario reads end-to-end, (5) the conceptual-only read for evaluators, (6) the minimum-90-minute read, (7) per-role reads (tech lead / ML engineer / SRE / engineering manager / product manager), (8) problem-driven entry points indexed against the most-common questions. The appendix closes with a *note on re-entry* that frames the book as a field guide structured to be re-entered rather than finished.
- The new appendix is added to `src/SUMMARY.md` under *Appendices* between *The Pattern Index* and *The Companion Paper*.

### Updated

- Version markers advanced from **v2.0.0-rc8** to **v2.0.0** (stable) in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the v2.0.0 status header.

### What v2.0.0 contains, in summary

The complete v2.0.0 release as it stabilized through rc1–rc8:

**Load-bearing commitments (unchanged from v1.x's five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, composition first-class):**
- Five archetypes: Advisor, Executor, Guardian, Synthesizer, Orchestrator
- Four orthogonal calibration dimensions: Agency, Autonomy, Responsibility, Reversibility
- Seven fix-locus failure categories (Cat 1 Spec through Cat 7 Perceptual, with four sub-categories)
- Four oversight models: Monitoring, Periodic, Output Gate, Pre-authorized
- Four signal metrics: spec-gap rate, first-pass validation, cost per correct outcome, oversight load
- 12 canonical spec sections (with the v1.x Composition Declaration and Cost Posture sub-blocks)
- Eight pattern categories (~50 patterns)
- Composition as a first-class design surface (Patterns A–E)

**v2.0.0's structural changes:**
- *Evolve* promoted from a closing-Validate sub-discipline to a **peer fifth activity** (the cardinality change that made v2.0.0 a MAJOR bump)
- Book reorganized from nine mixed-grain Parts into six phase-aligned Parts: **FRAME / SPECIFY / DELEGATE / VALIDATE / EVOLVE / REFERENCE**
- Framework canvas redrawn from a four-row layout (1180px) to a five-row layout (1330px) with the EVOLVE row's four practice chips (Closed Loop · Spec Evolution Log · Discipline-Health Audit · Framework Versioning)

**v2.0.0's new prose (~50K words across 21 chapters and one paper section):**
- 2 new conceptual Phase-5 chapters: [The Closed Loop](src/evolve/01-closed-loop.md) and [Framework Versioning](src/evolve/07-framework-versioning.md)
- 15 new scenario chapters across the three running scenarios (5 phases × 3 scenarios), each scenario walking a 4–5 person team through its 90-day operating window
- Paper §5: the customer-support pilot condensed into ~4K words of paper-grade prose
- The Reading Paths appendix (this rc)

**v2.0.0's voice commitment:** vignette-before-exposition openings on all new chapters and on the highest-impact v1.x conceptual chapters (rc8's voice pass). Specifics carry through the prose: named team roles, concrete numbers, operational details, decisions documented with reasoning.

**v2.0.0's narrative spine:** three scenarios at the same e-commerce SaaS, with the cross-team adoption arc Maya (S1, customer-support) → Daniel (S2, platform-engineering) → Logan (S3, docs-platform) showing the framework's vocabulary spreading across teams as a working discipline.

**v2.0.0's deck and sync:** the teaching deck got an activities slide and the deck/paper sync check enforces the five-activity cardinality across both artifacts.

### What v2.0.0 explicitly did not change

- The framework's vocabulary (5 archetypes, 4 dimensions, 7 Cats, etc. — listed above) survived intact. v2.0.0 was a *spine* change, not a vocabulary change.
- Existing v1.x specs that referenced the four activities by name need a one-section re-grounding to reflect *Evolve* as a peer fifth activity; all other spec content remains valid.
- The paper's §1.3 honest accounting (3 novel contributions / 4 explicitly-not-claimed) is unchanged.

### Deferred to v2.0.x or v2.1.x (not blocking v2.0.0 stable)

- File-path renames (`architecture/` → `frame/`, etc.) — purely filesystem cleanup; no reader-facing change. The SUMMARY drives navigation regardless of file paths.
- Vignettes on the remaining v1.x chapters (rc8 covered the highest-impact 4 Frame chapters; ~10 more conceptual chapters across `sdd/`, `agents/`, `operating/` could benefit from the same pass).
- Light Evolve-framing intros for the 4 remaining `operating/*` chapters in Part 5 (operating/10, 12, 13, 14) that didn't get them in rc8.
- Elevating S3's team-proposed *citation theater* anti-pattern to the framework's catalog as a 12th anti-pattern — pending repository discussion. If accepted, this would be a v2.1 MINOR addition, not a MAJOR change.

### The eight release candidates (chronological summary)

- **rc1** — structural reshape: SUMMARY reorganized to six Parts, 17 scenario stub files created, deck/paper sync acquires `CANONICAL_PHASES`, version markers seeded.
- **rc2** — five-row canvas redraw and PNG mirror, deck activities slide added, deck-side phases check activated.
- **rc3** — full prose for the two new Phase-5 conceptual chapters (the Closed Loop and Framework Versioning).
- **rc4** — Scenario 1 (customer-support agent) end-to-end across all five activities (~10K words across 5 chapters).
- **rc5** — paper §5 (the customer-support pilot condensed for the paper).
- **rc6** — Scenario 2 (coding-agent pipeline) end-to-end with Pattern E mode-switching composition concrete.
- **rc7** — Scenario 3 (internal docs Q&A, DevSquad-built) end-to-end, completing the three-scenario commitment.
- **rc8** — voice pass on v1.x conceptual chapters; chapter-subtitle alignment to the v2.0.0 Part placement across ~25 chapters.

### PRs

- **PR-J** (this release) — Reading Paths appendix; version graduation rc8 → 2.0.0; CHANGELOG summary of the rc cycle; paper PDF rebuild.

After this release lands on `main`, a **`v2.0.0` git tag** can be created against the merge commit. The tag creation is intentionally not part of the PR; it is a step the maintainer takes after merge so the tag points at the canonical merged state on `main`.

---

## v2.0.0-rc8 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — voice pass and chapter-subtitle alignment for v1.x book chapters that hadn't been touched in v2.0.0. No load-bearing framework changes; this is the editorial cleanup pass that brings the older conceptual chapters into the field-guide voice the new (rc3–rc7) chapters established. Framework load-bearing commitments unchanged from rc7.

### Added — vignettes (vignette-before-exposition openings)

Four highest-impact Frame conceptual chapters get a short vignette before the existing Context section, in the same shape as the rc3 closed-loop chapter and the scenario chapters:

- **`src/foundations/02-intent-vs-implementation.md`** — opens on a sprint-review moment where the agent's PR-merge-without-amendment rate dropped, the team investigates the agent's recent commits, and one engineer says *"the code is fine. The agent is doing exactly what the spec says. The spec is wrong about how cross-service refactors should be planned."* That moment is the chapter's load-bearing distinction.
- **`src/architecture/02-canonical-intent-archetypes.md`** — opens on a team in a Frame session 30 minutes in, the PM impatient to start naming features, the tech lead writing one word on the board: ARCHETYPE.
- **`src/foundations/03-agency-autonomy-responsibility.md`** — opens on a team debating *"high autonomy"* vs *"medium autonomy"* in circles, until the tech lead splits the four dimensions out as four separate decisions.
- **`src/architecture/05-composing-archetypes.md`** — opens on a spec review where the reviewer asks *"this part where the agent checks its own output before sending — that's a Guardian behavior. And §10's escalation flow looks like an Advisor handoff. Are we doing composition by accident, or composition by design?"*

### Added — Evolve-framing intros

Four operating chapters that now sit in **Part 5 — Evolve** get a short *Where this sits in v2.0.0* intro paragraph after the epigraph, anchoring them in the Evolve activity and naming their relationship to the closed loop:

- **`src/operating/04-governance.md`** — names governance as the role-and-responsibility frame that makes the closed loop survive contact with a real organization.
- **`src/operating/15-anti-patterns.md`** — names the Discipline-Health Audit as the per-quarter cadence that catches loop decay; cross-references the three running scenarios.
- **`src/operating/16-minimum-viable-aoi.md`** — names MVP-AoI as the closed loop in compressed form; the discipline travels down-scale.
- **`src/operating/09-cost-and-latency.md`** — names cost incidents as a particular Cat 4 class that requires its own escalation pattern; cross-references the customer-support and coding-pipeline Cost Posture incidents.
- **`src/operating/11-adoption-playbook.md`** — names the playbook as what keeps the loop going as the team grows; cross-references the cross-team adoption arc that runs through scenarios 1–3.

### Updated — chapter-subtitle alignment to v2.0.0 Part placement

Approximately **25 chapter subtitles** updated to match the v2.0.0 SUMMARY structure rather than the v1.x Part naming. The SUMMARY itself defines the Part placement; the chapter-level subtitles were lagging. This rc closes the gap.

| Old subtitle | New subtitle | Files |
|---|---|---|
| `**Part 5 — Ship**` | `**Part 4 — Validate**` | operating/07, 08 |
| `**Part 5 — Ship**` | `**Part 5 — Evolve**` | operating/09, 10, 11, 12, 13, 14 |
| `**Governance & Architecture**` | `**Part 4 — Validate**` | operating/05, 06 |
| `**Governance & Architecture**` | `**Part 5 — Evolve**` | operating/04 |
| `**Governance & Architecture**` | `**Part 1 — Frame**` | architecture/03, 04, 05, 06 |
| `**Operating Practice**` | `**Part 5 — Evolve**` | operating/15, 16 |
| `**Part 1 — Decisions**` | `**Part 1 — Frame**` | architecture/02, 07; foundations/03 |
| `**Part 1 — Decisions**` | `**Part 4 — Validate**` | foundations/05 |
| `**Foundations**` | `**Part 1 — Frame**` | foundations/02 |
| `**Foundations**` | `**Foreword**` | foundations/08 |
| `**Working Practice**` | `**Part 2 — Specify**` | foundations/07 |
| `**Specification**` | `**Part 2 — Specify**` | sdd/01–07 (7 chapters) |
| `**Part 2 — The Spec**` | `**Part 2 — Specify**` | sdd/08 |
| `**Agents**` | `**Part 3 — Delegate**` | agents/01–06 (6 chapters) |
| `**Part 3 — The Agent**` | `**Part 3 — Delegate**` | agents/08, 09 |

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line. The voice pass is the v2.0.0 commitment that addressed the most-cited reader complaint about v1.x — *"boring, declarative not narrative"* — by introducing vignette-before-exposition openings on new chapters. rc8 retroactively applies the same voice to the older chapters that hadn't had the pass. The chapter-subtitle alignment is also v2.0.0-structural — it brings the in-chapter Part markers into agreement with the SUMMARY structure that v2.0.0 reshaped. The version stays in the rc-line because the file-path renames and the reading-paths appendix are still pending.

### Deferred (unchanged from rc7's plan, plus one more)

- File-path renames (`architecture/` → `frame/`, etc.)
- Vignettes on the remaining v1.x chapters (PR-G covered the highest-impact 4; ~10 more conceptual chapters could benefit from the same pass) — folded into PR-H if needed
- Light Evolve-framing intros for the 4 remaining operating/* chapters in Part 5 (10, 12, 13, 14) — same comment
- Reading paths appendix + final v2.0.0 release tag — PR-J
- (Possibly) elevating the team-proposed *citation theater* anti-pattern from S3's Evolve chapter to the framework's catalog as a 12th anti-pattern — pending repository discussion

### PRs

- **PR-G** (this rc) — vignettes on 4 Frame conceptual chapters, Evolve-framing intros on 5 Part 5 operating chapters, ~25 chapter-subtitle alignments, version markers, paper PDF rebuild.

---

## v2.0.0-rc7 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — ships **Scenario 3 (internal docs Q&A, DevSquad-built) end-to-end** across all five activities, completing the three-scenario commitment v2.0.0 introduced at rc1. Five chapters (~10K words total). Framework load-bearing commitments unchanged from rc6.

### Added

- **`src/frame/scenarios/docs-qa.md` — full chapter prose.** Logan's docs-platform team — the third adopter at the same e-commerce SaaS as Scenarios 1 and 2 — frames an internal docs Q&A agent for ~200 internal engineers using DevSquad Copilot's eight-phase iterative cycle. Walks the three questions, the archetype call (**Synthesizer governing with Advisor mode embedded for the low-confidence path**), and the team's most-important framing decision: committing to *docs-gap-finding rate as a positive signal* — the agent's most-valuable accidental product is revealing real coverage gaps in the docs. Frame happens during DevSquad's *envisioning phase* + *kickoff* ceremony.
- **`src/specify/scenarios/docs-qa.md` — full chapter prose.** Walks the canonical 12-section spec written as a DevSquad **slice spec (P1 priority)** during DevSquad's *Spec the next slice* phase. The framework's 12-section template lives alongside DevSquad's slice spec format; the slice spec is the *current state* of the canonical spec, growing as slices land. Shows the AoI ↔ DevSquad mapping inline.
- **`src/delegate/scenarios/docs-qa.md` — full chapter prose.** The build is decomposed by DevSquad's `decompose` agent into per-task scopes with curated tool subsets — the framework's **Least Capability** discipline expressed at the *build* layer. The 5-tool manifest is the smallest of the three running scenarios (`retrieve_docs`, `rerank_docs`, `compose_answer`, `verify_citation`, `emit_docs_gap_candidate`); the **citation-grounding check** is the most load-bearing tool implementation, structurally enforcing the citation discipline that paper §5 names as the worst Synthesizer failure mode.
- **`src/validate/scenarios/docs-qa.md` — full chapter prose.** Pre-launch eval suite (200 known-good + 50 out-of-scope; first run **78% / 84%**, post-amendment **88% / 92%**), DevSquad's `review` agent running in independent context surfacing two findings the team's manual review missed, launch gate decision (5% canary → 25% → 75% → 100%), 30 days of metrics with all four standard metrics on target plus the **docs-gap-finding rate** stabilizing as the docs team keeps up, and the first month's 12 categorized failures tagged by both Cat *and* DevSquad phase.
- **`src/evolve/scenarios/docs-qa.md` — full chapter prose.** The 90-day operating window: 44 spec amendments distributed 28 Cat 1 / 8 Cat 2 / 6 Cat 4 / 0 Cat 6 / 0 Cat 7, **plus 142 *docs amendments triggered by the agent*** in the docs team's authoring history (the agent's most operationally significant output, captured outside the agent's spec evolution log). The refusal-rate trajectory falls from 24% to 8% over 90 days as the docs team keeps up with the docs-gap-candidate feed. The §11 structural rewrite at days 45–52. A new corpus-growth-aware Cost Posture amendment at day 74. The **Discipline-Health Audit at day 90** is the cleanest among the three scenarios — zero *active* anti-patterns, one *early signs* on a team-proposed new anti-pattern (**citation theater**, specific to Synthesizer-flavored systems), and a framework-repository discussion about whether to elevate it to the framework's catalog.

### Continuity

- Scenario 3 closes the cross-team adoption arc named in Scenarios 1 and 2: customer-support team (Maya, S1) → platform-engineering team (Daniel, S2) → docs-platform team (Logan, S3). By the end of Scenario 3, the framework's vocabulary is operating across three teams as a working discipline, with two more teams in flight. Cross-team adoption is itself the closed loop at organizational scale.
- The five chapters cross-link both ways via the *Reading path* table at the end of each.
- Scenario 3's Evolve chapter proposes a new **citation theater** anti-pattern back to the framework via repository discussion — the framework's living-document discipline at work, modeled within the scenario itself.

### Voice

All five chapters open vignette-before-exposition. Specifics carry through: the team's commitment to *docs-gap-finding rate as a positive signal*; Maya's note that *"the docs-gap-finding metric is what makes this scenario interesting"*; the team's reflection at day 30 that *"the spec evolution log under-represents the agent's value because most of the agent's value lands in the docs team's history, not ours"*; the day-74 corpus-growth lesson that *"Cost Posture sub-blocks should consider corpus growth as a default — for any retrieval-augmented system, the corpus is part of the cost surface"*. The DevSquad mapping inline at every phase keeps both vocabularies alive in the prose.

### Updated

- Version markers advanced from **v2.0.0-rc6** to **v2.0.0-rc7** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the updated status header.

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line because Scenario 3 is the third of the three running scenarios v2.0.0 introduced as load-bearing. The Synthesizer-flavored deployment shape and the DevSquad-native team practice are both v2.0.0 commitments that had been stubs from rc1 to rc6. rc7 makes both concrete in book-grade prose. The version stays in the rc-line until the file-path renames and the voice rewrites for older book chapters are complete; v2.0.0 stable lands when the rc series stabilizes.

### Deferred

- File-path renames (`architecture/` → `frame/`, etc.)
- Voice rewrites for older book chapters — PR-G, PR-H, PR-I
- Light Evolve-framing intros for the 9 existing `operating/*` chapters in Part 5 — folded into PR-G
- Reading paths appendix + final v2.0.0 release tag — PR-J
- (Possibly) elevating the team-proposed *citation theater* anti-pattern to the framework's catalog as a 12th anti-pattern — pending repository discussion

### PRs

- **PR-F** (this rc) — five docs-qa scenario chapters with DevSquad mapping inline at every phase, version markers, paper PDF rebuild.

---

## v2.0.0-rc6 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — ships **Scenario 2 (the coding-agent pipeline) end-to-end** across all five activities. Five chapters (~10K words total) replace the rc1 stubs with full prose. Framework load-bearing commitments unchanged from rc5.

### Added

- **`src/frame/scenarios/coding-pipeline.md` — full chapter prose.** A second team at the same e-commerce SaaS as Scenario 1 (Daniel/Naomi/Theo/Jess from platform-engineering, with Maya from S1 advising) frames an in-loop coding agent for tier-1 engineering tickets across 17 services. Walks the three questions, the archetype call (Executor with **Pattern E mode-switching composition** — Frame/Plan/Implement/Review), the high-autonomy / medium-reversibility calibration, the four cross-mode invariants (test-skip-set monotonic, no protected-branch push, no unrestricted shell, PR description names spec section), and the deliberate decision to elevate or not (rejected — the structural controls compensate for high autonomy).
- **`src/specify/scenarios/coding-pipeline.md` — full chapter prose.** Walks the canonical 12-section spec for a system whose load-bearing constraint lives in the manifest and CI rather than in the prose. Detailed §3/§4/§5 with the per-mode tool manifest (the strongest case of mode-scoped tool binding in the framework's body of examples), the Composition Declaration sub-block (Pattern E with explicit transition triggers), the Cost Posture sub-block ($4.50 per-merged-PR ceiling), the four §6 invariants as CI guards.
- **`src/delegate/scenarios/coding-pipeline.md` — full chapter prose.** The build phase: a 2-paragraph system prompt (even shorter than Scenario 1's 3-paragraph one because the manifest carries more load), per-mode tool manifest with deliberate exclusions enumerated and `git_push_protected` / `gh_pr_merge` explicitly absent, the four CI guards (test-skip monotonicity, branch-protection at the platform layer, manifest-scope check, spec-conformance gate) shown with shell snippets, oversight wiring for **Pre-authorized scope with exception escalation** (not Output Gate — the PR review process is itself the validation gate), the launch readiness checklist.
- **`src/validate/scenarios/coding-pipeline.md` — full chapter prose.** Pre-launch eval suite (60 known-good ticket scenarios + 15 adversarial; first run lands at 71%, post-amendment at 82%), red-team protocol four attack surfaces with two findings (a Cat 7-adjacent file-misidentification pattern in Frame mode; a Cat 4 escalation routing dropping tickets when reviewers are on PTO), launch gate decision (all gates pass; 4-service pilot expansion), 30 days of metrics with FPV short of target at 78%, the first month's 22 categorized failures distributed across modes (Plan dominates, as expected and as the discipline intends).
- **`src/evolve/scenarios/coding-pipeline.md` — full chapter prose.** The 90-day operating window: 22 amendments distributed 17 Cat 1 / 1 Cat 2 / 4 Cat 4 / 0 Cat 6, two structural rewrites of §11 (the operationally-thin section was the under-specified surface), the model-tier rotation event at day 60 (Sonnet 4.7 lands; the framework's model-upgrade-validation pattern fires; eval re-runs at 89% with a $4.10 cost baseline), the cross-team adoption pattern (two other teams ask for help; one-hour Frame consultations rather than full IDS; the platform team's discipline deepens through teaching), the Discipline-Health Audit at day 90 catching **active prompt-patch drift, active pattern inventory, and early signs of composition by accident** with corrective actions, and the post-90 disposition with the **Anomaly Baseline pattern de-bound** as net-unused.

### Continuity

- Scenario 2 introduces **named characters who carry forward into Scenario 3**: Daniel, Naomi, Theo, Jess on the platform-engineering team; Maya from Scenario 1 advising as the first-adopter. The narrative continuity reinforces the company-level adoption arc: customer-support team adopts the framework in Scenario 1; their 90-day success leads the platform team to adopt in Scenario 2; the platform team's adoption is itself a vector for cross-team adoption (two other teams in Scenario 2's Evolve chapter; Scenario 3 will show the third).
- The five chapters cross-link via the *Reading path* table at the end of each.
- Scenario 2's Evolve chapter mentions a *service overlay* construct that emerged from operating across 17 services — a per-service file naming dev-dependency allowlist additions, test-runner config, and ticket-template hints. The construct is named in this rc as worked development; if it generalizes to a framework-level concept, that elevation will land in a subsequent rc with the appropriate cardinality update to `paper/check-deck-sync.py`.

### Voice

All five chapters open vignette-before-exposition, per the v2.0.0 commitment. Specifics carry through: Daniel's *"the temptation to start prompting now and call it framing later"* warning at the Frame session opening; Maya's parting note that *"the spec for a coding agent reads weirder"*; Naomi's *"§11 was the under-specified section"* per-sprint roll-up call; the *"the model bump did some of the work that incremental amendments would have done"* observation from the day-60 model-tier rotation; Naomi's *"explaining the §11 rewrite to the product-engineering team forced me to articulate why we wrote it that way"* reflection on cross-team adoption.

### Updated

- Version markers advanced from **v2.0.0-rc5** to **v2.0.0-rc6** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the updated status header.

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line because Scenario 2 is the second of the three running scenarios v2.0.0 introduced as load-bearing. The mode-switching composition (Pattern E) is the v2.0.0 canonical demonstration case — the strongest case of the framework's composition-first-class commitment — and it had been a stub from rc1 to rc5. rc6 makes Pattern E concrete in book-grade prose. The version stays in the rc-line because Scenario 3, the file-path renames, and the voice rewrites are still pending.

### Deferred (unchanged from rc5's plan)

- File-path renames (`architecture/` → `frame/`, etc.)
- Scenario 3 (internal docs Q&A, DevSquad-built) end-to-end — PR-F
- Voice rewrites for older chapters — PR-G, PR-H, PR-I
- Light Evolve-framing intros for the 9 existing `operating/*` chapters in Part 5 — folded into PR-G
- Reading paths appendix + final v2.0.0 release tag — PR-J

### PRs

- **PR-E** (this rc) — five coding-pipeline scenario chapters, version markers, paper PDF rebuild.

---

## v2.0.0-rc5 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — adds **paper §5**, a paper-grade end-to-end walkthrough of the customer-support pilot drawing on the rc4 book material, plus the section renumbering it requires. Closes the rc1 commitment that the paper acquires its own worked walkthrough as a complement to §4's agent-class deep-dives. Framework load-bearing commitments are unchanged from rc4.

### Added

- **Paper §5: Walking a pilot end-to-end: the customer-support agent.** Six subsections — 5.1 Frame, 5.2 Specify, 5.3 Delegate, 5.4 Validate, 5.5 Evolve, 5.6 What the walkthrough demonstrates. Roughly 4,000 words; condenses the ~10,000-word rc4 book scenario into a paper-grade narrative without losing the structural specifics (asymmetric Reversibility commitment, Composition Declaration sub-block, Cost Posture sub-block with the Sonnet 4.6→4.7 cost incident at day 47, Cat-by-Cat distribution of the 11 amendments, Output Gate→Periodic transition at day 44, Discipline-Health Audit findings at day 90, Haiku-fallback deprecation decision based on operational evidence). Voice is paper-academic — anonymous team roles rather than named individuals — while preserving the load-bearing operational details.

### Changed (renumbering)

The new §5 inserts after the existing §4 (Worked application: AI agent systems), shifting downstream sections:
- Old §5 Discussion → **new §6 Discussion**
- Old §6 Limitations → **new §7 Limitations**
- Old §7 Conclusion → **new §8 Conclusion**

Cross-references updated throughout the paper:
- §1.3 (Contribution) — now refers to §7 for limitations enumeration; mentions §5 as the existence-proof walkthrough
- §1.4 (Paper structure) — fully rewritten to describe §5 + the renumbered §6/§7/§8
- §2.4 (MAST relation) — `§5.3` → `§6.3`
- §3.5 (closing summary of §3) — fully rewritten to mention §5/§6/§7
- §6.5 (What this paper does not claim) — `§6 enumerates` → `§7 enumerates`
- §7 (Limitations) — `§5.4` reference → `§6.4`; the *no-empirical-validation* bullet rewritten to acknowledge that paper §5 walks one of the three book scenarios as an existence proof
- §8 (Conclusion) — closing paragraph rewritten to mention §5 alongside §4 and §6.4
- Appendix A (Mapping to the book) — new row added for §5 (pointing at the five book "in practice — Customer-support agent" chapters and the Closed Loop chapter); existing rows for §6 Discussion and §7 Limitations renumbered

### Updated

- Version markers advanced from **v2.0.0-rc4** to **v2.0.0-rc5** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the new §5 and the renumbering. The PDF page count grows by ~6 pages (paper word count from ~16,100 to ~20,200).

### Voice

§5 opens directly with the operational setting (the e-commerce SaaS, the volume, the team shape, the deployment target) without the book's vignette form — the paper voice is more academic. The structural specifics are preserved verbatim: the asymmetric Reversibility argument, the Guardian wrapper logic, the day-47 Cost Posture incident's measurement-based decision, the day-51 review-handoff failure with the *"approve message"* misinterpretation, the day-90 Discipline-Health Audit findings (active prompt-patch drift, early signs of metrics theater). The paper makes the case that one worked pilot is an existence proof of the discipline, not a statistical validation; quantitative validation across many independent deployments remains future work (§7).

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line because §5 is structural to the paper — it changes the section count, the cross-reference graph, and the limitations bullet that previously said *"the book provides three worked examples; the paper provides none."* External readers of v2.0.0-rc4 paper PDFs would find the rc5 paper substantially different (one entire new section, six subsections, ~4K new words). The version stays in the rc-line because Scenarios 2 and 3 are still pending, the file-path renames are still pending, and the voice rewrites for older book chapters are still pending.

### Deferred (unchanged from rc4's plan)

- File-path renames (`architecture/` → `frame/`, etc.)
- Scenario 2 (coding-agent pipeline) end-to-end — PR-E
- Scenario 3 (internal docs Q&A, DevSquad) end-to-end — PR-F
- Voice rewrites for older chapters — PR-G, PR-H, PR-I
- Light Evolve-framing intros for the 9 existing `operating/*` chapters in Part 5 — folded into PR-G
- Reading paths appendix + final v2.0.0 release tag — PR-J

### PRs

- **PR-D** (this rc) — paper §5, section renumbering, cross-reference updates, version markers, paper PDF rebuild.

---

## v2.0.0-rc4 — 2026-05-10

**MAJOR (release candidate, continues v2.0.0 line)** — ships **Scenario 1 (the customer-support agent) end-to-end** across all five activities. Five chapters (~10K words total) replace the rc1 stubs with full prose; the running-scenario tour at the end of `evolve/01-closed-loop.md` now resolves to substantive content rather than placeholders. Framework load-bearing commitments unchanged from rc3.

### Added

- **`src/frame/scenarios/customer-support.md` — full chapter prose.** Walks Maya, Ari, Sam, Jordan, and Priya through a 90-minute Frame session. Names the three questions, the archetype call (Executor with embedded Advisor and Guardian), the explicit risk-override consideration and rejection, the Composition Declaration, and the four-dimension calibration with an asymmetric Reversibility commitment. Produces a one-page Frame artifact that flows into Specify.
- **`src/specify/scenarios/customer-support.md` — full chapter prose.** Walks the team through writing the canonical 12-section spec. Spends the most ink on §3 / §4 (with concrete clauses), §4 Composition Declaration, §4 Cost Posture (Haiku/Sonnet routing, p95/p99 latency budget, $0.04 ceiling), §6 invariants, and §11 escalation triggers. Produces a complete spec in 8 hours.
- **`src/delegate/scenarios/customer-support.md` — full chapter prose.** Walks the build through five layers — system prompt (3 paragraphs), tool manifest (5 tools with deliberate exclusions enumerated), patterns bound from Part 4, oversight wiring, and the launch readiness checklist. Names the *"three paragraphs"* discipline for system prompts and shows the Guardian wrap on `issue_refund_within_cap` as code.
- **`src/validate/scenarios/customer-support.md` — full chapter prose.** Walks pre-launch eval suite (150 known-good + 30 adversarial; first run lands at 84%, post-amendment at 91%), red-team protocol with four attack surfaces, the launch gate decision (all gates pass; 10% canary → 50% → 100%), the first 30 days of signal metrics with FPV short of target at 89%, and the eight Cat 1–7 categorized failures from the first month with their fix-locus amendments.
- **`src/evolve/scenarios/customer-support.md` — full chapter prose.** Opens with the $2,400-unauthorized-refund vignette from `evolve/01-closed-loop.md`, then resolves it: the Guardian did its job, the failure was Cat 4 in the review-and-action handoff, and the fix lives in §10 and Priya's runbook (not the prompt). Walks 90 days of operation: the full 11-amendment spec evolution log, the Output Gate → Periodic transition (held at day 30, executed at day 44), the Cost Posture incident at day 47, the Discipline-Health Audit at day 90 (which catches *active* prompt-patch drift and *early signs* of metrics theater), and the post-90 disposition including the deprecation of the Haiku fallback path as net-negative.

### Continuity

The five chapters cross-link both ways through the *Reading path through this scenario* table at the end of each. The closed-loop chapter's running-scenario tour at `evolve/01-closed-loop.md` now points to substantive prose rather than the rc1 stubs. The $2,400-refund vignette in `evolve/01-closed-loop.md` (rc3) and `evolve/scenarios/customer-support.md` (rc4) are now narratively connected — the Evolve scenario chapter is the resolution of the closed-loop chapter's opening scene.

### Voice

All five chapters open vignette-before-exposition, per the v2.0.0 commitment. Specifics carry through: a five-person team with named roles (Maya / Ari / Sam / Jordan / Priya); concrete numbers (~3,000 chats/day, ~50K customers, $500 cap, $0.04 ceiling, 92% FPV target); operational details (the model-tier rotation at day 47; the contractor reviewer's interpretation of "approve message" at day 51); and explicit decisions documented with their reasoning.

### Updated

- Version markers advanced from **v2.0.0-rc3** to **v2.0.0-rc4** in `src/appendices/glossary.md` (Framework Version entry), `src/appendices/companion-paper.md`, `README.md`, and `paper/architecture-of-intent.md` (status header).
- `paper/architecture-of-intent.pdf` recompiled with the updated status header.

### Why MAJOR-rc

Continues the v2.0.0 MAJOR line because Scenario 1 is one of the three running scenarios v2.0.0 introduced as load-bearing — the v2.0.0 commitment to *running scenarios across the five activities* was structural at rc1 (the SUMMARY links resolved to stubs) but not yet substantive. rc4 makes the commitment substantive for one of the three scenarios. The version stays in the rc-line because Scenarios 2 and 3, paper §5, the file-path renames, and the voice rewrites are still pending.

### Deferred (unchanged from rc3's plan)

- File-path renames (`architecture/` → `frame/`, etc.) — purely filesystem cleanup
- Scenario 2 (coding-agent pipeline) end-to-end — PR-E
- Scenario 3 (internal docs Q&A, DevSquad) end-to-end — PR-F
- Voice rewrites for older chapters — PR-G, PR-H, PR-I
- Light Evolve-framing intros for the 9 existing `operating/*` chapters in Part 5 — folded into PR-G
- Paper §5 (single canonical scenario, drawing on the rc4 customer-support material) — PR-D
- Reading paths appendix + final v2.0.0 release tag — PR-J

### PRs

- **PR-C** (this rc) — five customer-support scenario chapters, version markers, paper PDF rebuild.

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
- **"Cost is not a fifth dimension" framing sub-section** in [`src/foundations/03-agency-autonomy-responsibility.md`](src/foundations/03-agency-autonomy-responsibility.md) that explains the working position with three structural reasons (cost is partially derived from the four dimensions; cost is a *resource* commitment whereas A/A/R/R are *behavioral* commitments; the lineage is thin — neither SAE J3016 nor Shavit & Agarwal treat cost as a dimension).
- **Paper §3.3 paragraph** giving the same structural rationale at paper grain.
- **Cost Posture** glossary entry under C (in proper alphabetical position between Context Provision and Delegation), naming the five fields and the resource-vs-behavioral distinction.
- New **Cost Posture sub-block** entry at the top of the Pattern Index *"My agent program's cost or latency isn't penciling"* By-Problem entry, with the framing-sub-section as the second link. Practitioners reaching for that By-Problem entry now see the upstream spec surface before the operational chapters.
- Light cross-references added from [Cost and Latency Engineering](src/operating/09-cost-and-latency.md) and [Cacheable Prompt Architecture](src/operating/14-cacheable-prompt-architecture.md) to the new §4 sub-block.

### Why this is MINOR, not MAJOR

The sub-block extends §4 alongside the existing Composition Declaration without changing any load-bearing commitment: the five archetypes, **four** dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are all unchanged. The four-dimension cardinality the deck/paper sync check enforces is unaffected. The orthogonality argument in paper §3.3 stands. The honest accounting in paper §1.3 ("3 novel / 4 not claimed") is unchanged because Cost Posture is presented as a *structural surface* on top of existing operational treatments (Cost & Latency Engineering, Cacheable Prompt Architecture), not as a novel claim.

### Why a §4 sub-block instead of a fifth dimension

The candidate alternative — promoting cost to a fifth calibration dimension alongside A/A/R/R — would have been a MAJOR bump (v1.3.0 → v2.0.0). It was rejected for three reasons documented in the new framing sub-section: (1) cost is partly *derived* from the four behavioral dimensions, conflating dial with derived quantity; (2) cost is a *resource* commitment whereas A/A/R/R are *behavioral* commitments — different category; (3) the lineage is thin — neither SAE J3016 nor Shavit & Agarwal treat cost as a dimension, so promoting it would require either a weak novelty claim or a manufactured citation. The §4 sub-block does the work the recommendation actually wanted done — give cost a structural upstream seat in the spec — without overclaiming. The Composition Declaration sub-block established the precedent: §4 can absorb structural commitments that aren't dimensions.

### PRs

- **#52** — Add Cost Posture sub-block to spec template §4; framing sub-section in foundations/03 and paper §3.3

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

**MINOR** — adds the *What Changes for the Senior Engineer* chapter (foundations/08) without changing any load-bearing commitment.

### Added

- **[What Changes for the Senior Engineer](src/foundations/08-what-changes-for-senior-engineers.md)** — a new Foundations chapter at the end of Part 1 that responds to the question the [Prologue](src/prologue.md) raises but never resolves: *if late-judgment compensation was the senior engineer's value-add, what is the value-add now?* The chapter names where the judgment goes (Frame, Specify, Bind Patterns, Skeptic, Validate); names what is honestly lost (the flow state of late-judgment debugging, tribal knowledge as a moat, pure-implementation seniority, the practitioners who will not make the transition); names what is gained (authorship that compounds, durable artifacts, leverage across teams, a different kind of seniority); and names the career-ladder gap explicitly.
- New *"I'm a senior engineer wondering what this all means for me"* By-Problem entry in the Pattern Index, pointing at the Prologue, the new chapter, the IDS, and the RACI Card.

### Why this is MINOR, not MAJOR

The chapter extends the framework's vocabulary about *practitioner experience* without changing any load-bearing commitment: the five archetypes, four dimensions, seven Cats, four oversight models, four signal metrics, four canvas activities, and composition-first-class are unchanged. The deck/paper sync check is unaffected. No paper changes (the paper does not currently address the senior-engineer angle; that may become a future paper-side addition).

### PRs

- **#50** — Add *What Changes for the Senior Engineer* chapter (foundations/08)

---

## v1.1.0 — 2026-05-10

**MINOR** — adds the Roles & Responsibilities (RACI) Card appendix without changing any load-bearing commitment.

### Added

- **[Roles & Responsibilities (RACI) Card](src/appendices/raci-card.md)** — a one-page reference appendix that maps the seven canonical roles (domain owner, spec author, architect, builder, operator, reviewer, skeptic) against the six operational activities (Frame · Specify · Build · Oversee · Ship · Evolve). Standard RACI shorthand: R does the work, A owns the outcome (exactly one per activity), C is consulted before action, I is informed after. Five common patterns and five anti-patterns documented.
- New **RACI** entry in the glossary; new *RACI Card* row added to the *Roles & Responsibilities* governance entry of the Pattern Index.
- Light cross-references added from the [Intent Design Session](src/foundations/07-intent-design-session.md) chapter (the IDS is where the RACI is *enacted* for one specific system; the card is the matrix the team enacts against), [Proportional Governance](src/operating/04-governance.md), and the [Adoption Playbook](src/operating/11-adoption-playbook.md).

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
| #44 | The Intent Design Session chapter (`foundations/07`) — the 7-phase ritual that turns the framework from a vocabulary into a discipline |
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
