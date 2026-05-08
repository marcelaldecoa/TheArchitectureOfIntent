# Mapping the Framework to the DevSquad 8-Phase Cadence

**Part 5 — Ship**

---

> *"This book is process-agnostic by design. If your team runs the DevSquad Copilot 8-phase cadence — and many do — here is exactly where the framework's artifacts and disciplines live in your week."*

---

## Context

Microsoft's [DevSquad Copilot](https://github.com/microsoft/devsquad-copilot) is a delivery framework that integrates Copilot with specialized agents into an explicit 8-phase iterative cycle: envisioning → spec thin slices → plan with ADRs → decompose → TDD-first implement → learn openly → independent review → continuous refinement. The framework converges with this book on the load-bearing concepts (living specs, risk-tiered human-in-the-loop, principle of least privilege, context isolation, spec-first response to failure) but is more *operationally prescriptive*: it gives a team a delivery cadence rather than a design vocabulary.

If your team already runs DevSquad's cadence, this chapter shows where each phase consumes and produces the book's artifacts. The two frameworks compose cleanly. This chapter is the bridge.

If your team does not run DevSquad's cadence, skip this chapter. The book's discipline is not dependent on it.

---

## The Problem

Two failure modes recur when teams try to combine the two frameworks without an explicit mapping:

**1. Artifact mismatch.** The team writes specs in DevSquad's "thin-slice" form, then tries to apply the book's canonical spec template, then finds that some sections (Section 4 — Authorization Boundary, Section 11 — Agent Execution Instructions) don't map cleanly onto DevSquad's notion of "what a spec contains." The team either bloats the spec to include both, or picks one and loses the discipline the other was providing.

**2. Phase-discipline mismatch.** The team adopts the book's eval suite but doesn't know which DevSquad phase it runs in. They adopt the book's archetype declaration but don't know whether it's a phase-2 (spec) or phase-3 (plan) artifact. The disciplines exist; their place in the cadence does not.

The mapping below resolves both.

---

## The Solution

### The 8-phase mapping

For each DevSquad phase, the artifacts the book contributes and the disciplines that apply.

#### Phase 1 — Envisioning

**DevSquad activity:** Surface pain points and success criteria. The team identifies what they are trying to build and why.

**Book artifacts produced:** Sections 1 (Problem Statement) and 2 (Objective) of the [Canonical Spec Template](../sdd/07-canonical-spec-template.md). Sometimes the [Archetype declaration](../architecture/02-canonical-intent-archetypes.md) is provisional at this phase — "this is going to be an Executor with a Guardian gate" — pending refinement.

**Book disciplines that apply:** The risk-override check from [The Archetype Selection Tree](../architecture/04-decision-tree.md). If the envisioned system is going to be Critical risk, name that early and let it shape the rest of the cadence.

**Output of this phase:** Sections 1–2 of the spec, plus a provisional archetype hypothesis.

#### Phase 2 — Spec thin slices

**DevSquad activity:** Write prioritized user stories capturing what/why, never how. Specs are thin and incrementally refined.

**Book artifacts produced:** Sections 3 (Authorized Scope) and 4 (NOT-Authorized Scope) of the spec, narrowed to the thin slice. The archetype declaration (Section 4) is firmed up. Initial reversibility assessment per [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md).

**Book disciplines that apply:** Surface, don't resolve. Where a thin slice has ambiguity that affects the archetype or the authorization boundary, name it as an open question rather than over-specifying.

**Connection to DevSquad's "spec thin slices":** The book's canonical template is *cumulative across slices*. A thin slice in DevSquad terms is a slice of Sections 1–3; the rest of the template (oversight model, eval criteria, tool manifest) accumulates as the slice gains substance and as ADRs from Phase 3 get integrated.

#### Phase 3 — Plan with ADRs

**DevSquad activity:** Record architectural decisions against ranked priorities. ADRs are durable; they survive the slice they were written for.

**Book artifacts produced:** Section 6 (Invariants) of the spec — every ADR that produces a non-negotiable rule becomes an entry in Section 6. Section 8 (Authorization Boundary) — every ADR that constrains tool access becomes a clause in Section 8. The [Architectural Decision Records](../sdd/08-architectural-decision-records.md) chapter explains the relationship between ADRs and spec sections in detail.

**Book disciplines that apply:** ADRs that conflict with each other surface as Cat 1 (Spec Failure) precursors — surface, don't resolve at the agent layer. The book's [Composing Archetypes](../architecture/05-composing-archetypes.md) spec-conflict resolution rules apply when ADRs from different team members propose contradictory invariants.

**Connection to DevSquad's "Plan with ADRs":** ADRs map to the book's invariants and authorization-boundary clauses. They are the durable record of *why* the spec says what it says. The spec evolution log (Section 13 of the canonical template) and the team's ADR archive are the two sides of the same artifact: the spec captures the *what*, ADRs capture the *why*.

#### Phase 4 — Decompose

**DevSquad activity:** Break the slice into granular tasks — single-session implementation units.

**Book artifacts produced:** Section 9 (Acceptance Criteria) per task, in Given/When/Then form. Section 11 (Agent Execution Instructions) refined for each agent that will participate.

**Book disciplines that apply:** [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) — each task receives only the tools it needs from Section 7's tool manifest, not the whole manifest. Capability minimalism per task is what makes [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) actually structural.

**Output of this phase:** A task-level spec for each decomposed unit, derived from the slice spec.

#### Phase 5 — Implement TDD-first

**DevSquad activity:** Test-before-code discipline. Implementation follows from the test.

**Book artifacts produced:** Level 2 of the [Evals and Benchmarks](07-evals-and-benchmarks.md) eval stack — the spec acceptance suite. Each Section 9 acceptance criterion becomes one or more automated tests. The TDD red-green loop is the book's spec-acceptance suite running.

**Book disciplines that apply:** The eval suite is *not optional* and *gates deployment*. TDD-first as practiced in DevSquad maps onto the book's Level 2 eval discipline. If the spec acceptance suite cannot be written (because the spec is too vague), that is a Cat 1 spec failure surfaced before code is written — the right response is to refine the spec, not to skip the suite.

**Connection to DevSquad's "TDD-first":** The book's eval suite *is* the TDD discipline applied at the spec layer rather than the unit-test layer. The two are compatible and reinforcing — unit tests cover the implementation, the spec acceptance suite covers the intent.

#### Phase 6 — Learn openly

**DevSquad activity:** Amend specs when implementation reveals new constraints. Failures are surfaced and the spec evolves.

**Book artifacts produced:** Spec Gap Log entries per [The Living Spec](../sdd/06-living-specs.md). Constraint library updates per [The Organizational Repertoire](../repertoires/01-why-repertoires-matter.md).

**Book disciplines that apply:** The diagnostic protocol from [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md). Every learning is categorized (Cat 1–6) and traced to the artifact that needs to change. When the change is structural enough to warrant a new ADR, this phase produces a back-flow into Phase 3.

**Connection to DevSquad's "Learn openly":** DevSquad's amendment process is the book's spec evolution discipline. The book adds the categorization protocol — *which kind of learning is this, and what artifact does it change?*

#### Phase 7 — Independent review

**DevSquad activity:** Validate against specifications and ADRs. Independent reviewer (not the implementer).

**Book artifacts produced:** [Intent Review Before Output Review](05-reviewing-intent.md) artifacts — the review is structured around the spec and the ADRs, not around the diff. Production sampling per Level 4 of the eval stack.

**Book disciplines that apply:** Output review answers *"did the agent follow the spec?"* not *"do I agree with this output?"* The first has an objective answer; the second restarts the design work that should have happened in Phase 3.

**Connection to DevSquad's "Independent review":** Same discipline, same purpose. The book's contribution is the framing that distinguishes spec-conformance review from preference-based review.

#### Phase 8 — Continuous refinement

**DevSquad activity:** Backlog maintenance between sprints. Artifacts are updated; the team prepares for the next slice.

**Book artifacts produced:** Updates to the constraint library; updates to the archetype catalog if the team's work surfaced a new variant; eval regression baseline updates per [Evals and Benchmarks](07-evals-and-benchmarks.md) Level 3.

**Book disciplines that apply:** The four signal metrics ([Four Signal Metrics](06-metrics.md)) are reviewed in this phase. Trends, not single-data-points. Cost-per-correct-output trends and spec-gap-rate trends drive the priorities for the next sprint's spec work.

**Connection to DevSquad's "Continuous refinement":** The book contributes the *measurement* layer that makes refinement signal-driven rather than vibes-driven. The four signal metrics are what tell you *which* refinements compound and which were one-off.

---

### Where ADRs and the spec touch

This is the question DevSquad fans ask first: where do ADRs and the canonical spec interact?

**ADRs are about architecture; the spec is about behavior.** An ADR records the decision to use the Authentication service A rather than service B; the spec records the constraint that all authenticated calls must pass through Service A. They are different artifacts at different lifetimes. ADRs change rarely (architectural decisions are stable); specs evolve with every learning event.

**Mapping rules:**

| ADR type | Maps onto spec section |
|---|---|
| Architectural choice (which library / service / pattern) | Section 6 (Invariants) — "the system uses X, may not use Y" |
| Authorization decision (what the agent may access) | Section 8 (Authorization Boundary) |
| Capability decision (what tools exist) | Section 7 (Tool Manifest) |
| Risk-tier decision (oversight model) | Section 4 (Archetype Declaration's oversight model) |
| Process decision (review cadence, escalation policy) | Section 12 (Validation Checklist) |

The book's [Architectural Decision Records](../sdd/08-architectural-decision-records.md) chapter goes deeper on the relationship and the format.

---

### What this mapping does NOT solve

Three places where the two frameworks pull in different directions, and the team has to choose:

**1. Ownership of the spec.** DevSquad assumes a multi-developer team where the spec is shared property and ADRs are how cross-team decisions are recorded. The book is more individual-author-shaped — a single owner per spec, with reviewers. Teams that want to combine them need to decide: is the spec owned by one author and reviewed by the team, or shared property edited by the team? Both work; pick one and be consistent.

**2. Sprint cadence vs. agent task cadence.** DevSquad assumes sprints; the book's task cadence is per-agent-run, which is often shorter. A team running both will have *two cadences* — the sprint cadence for human work and refinement, the per-agent cadence for individual agent runs. The metrics in the book ([Four Signal Metrics](06-metrics.md)) operate on the per-agent cadence; the DevSquad reviews operate on the sprint cadence. Don't try to collapse them.

**3. ADR-as-decision vs. spec-as-control.** DevSquad's ADRs are decisions the team made. The book's spec is the control surface the agent runs against. Sometimes a team will want to record an ADR that the spec doesn't enforce — "we considered X and rejected it." That ADR has no spec section. It still has value as institutional memory. The mapping table above is the rule for ADRs that do have spec consequences; ADRs without spec consequences live in the team's ADR archive and don't generate spec changes.

---

## Resulting Context

After applying this mapping:

- **Each DevSquad phase has named book artifacts.** No phase produces nothing the book recognizes; no book artifact lacks a phase to live in.
- **ADRs and specs are explicitly related, not duplicative.** ADRs record the *why*; specs encode the *what*; the mapping table above says how they connect.
- **The eval suite has a phase home.** Level 2 acceptance evals live in Phase 5 (TDD-first); Level 3 regression and Level 4 production sampling live in Phase 7 (review) and Phase 8 (refinement).
- **The diagnostic protocol fits the learn-openly phase.** Categorization (Cat 1–6) is what gives Phase 6 its rigor.

---

## Therefore

> **The book's design vocabulary and DevSquad's delivery cadence compose cleanly when the mapping is explicit. Each of DevSquad's 8 phases produces or consumes book artifacts: envisioning produces Sections 1–2 of the spec; spec thin slices produce Sections 3–4; ADRs map to invariants and authorization clauses; decomposition produces task-level acceptance criteria; TDD-first IS the spec acceptance suite; learn openly is the spec gap log discipline; independent review is intent review before output review; continuous refinement is metric-driven prioritization. Run the cadence; apply the artifacts; let the disciplines compound.**

---

## References

- Microsoft. (2024–2025). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot.
- Nygard, M. (2011). *Documenting Architecture Decisions.* — The original ADR format that DevSquad and this book both inherit from.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)
- [Architectural Decision Records](../sdd/08-architectural-decision-records.md)
- [Co-adoption with DevSquad](13-co-adoption-with-devsquad.md) — the strategy chapter for combining the two

**This pattern enables:**
- [Adoption Playbook](11-adoption-playbook.md) — adoption guidance for teams not already on DevSquad
- All of Part 5 (Ship) — every chapter applies within DevSquad's cadence at the phase identified above

---
