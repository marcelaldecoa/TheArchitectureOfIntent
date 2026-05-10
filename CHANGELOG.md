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
