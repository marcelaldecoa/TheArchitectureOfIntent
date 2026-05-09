# Mapping the Framework to the DevSquad 8-Phase Cadence

**Part 5 — Ship**

---

> *"This book is process-agnostic by design. If your team runs the DevSquad Copilot 8-phase cadence — and many do — here is exactly where the framework's artifacts live in your week."*

---

## Context

Microsoft's [DevSquad Copilot](https://github.com/microsoft/devsquad-copilot) is a delivery framework that integrates Copilot with specialized agents into an explicit 8-phase iterative cycle. It converges with this book on the load-bearing concepts (living specs, risk-tiered human-in-the-loop, principle of least privilege, context isolation, spec-first response to failure) but is more *operationally prescriptive*: it gives a team a delivery cadence rather than a design vocabulary.

This chapter is the bridge for teams running both. If your team does not run DevSquad's cadence, skip the table and read [Co-adoption with DevSquad Copilot](13-co-adoption-with-devsquad.md) instead.

---

## The 8-phase artifact map

| DevSquad phase | Activity | Book artifact produced | Book discipline that applies |
|---|---|---|---|
| **1. Envisioning** | Surface pain points and success criteria | Spec §1 (Problem) and §2 (Objective); provisional [archetype](../architecture/02-canonical-intent-archetypes.md) hypothesis | Risk-override check from [The Archetype Selection Tree](../architecture/04-decision-tree.md) — name Critical risk early |
| **2. Spec thin slices** | What/why per slice, never how | Spec §3 (Authorized Scope), §4 (NOT-authorized), firmed-up archetype, initial reversibility assessment per [Calibrate ARRR](../theory/03-agency-autonomy-responsibility.md) | Surface ambiguity, don't resolve. The canonical template is **cumulative across slices** — later sections accumulate as slices mature |
| **3. Plan with ADRs** | Architectural decisions against ranked priorities | Spec §6 (Invariants); §8 (Authorization Boundary); per [ADRs](../sdd/08-architectural-decision-records.md) | Conflicting ADRs are Cat 1 precursors — surface, don't resolve at the agent layer. Use [Composing Archetypes](../architecture/05-composing-archetypes.md) conflict rules |
| **4. Decompose** | Break slice into single-session tasks | Spec §9 (Acceptance Criteria) per task in Given/When/Then; §11 (Agent Execution Instructions) per agent | [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) — each task receives only the tools it needs from §7's manifest |
| **5. Implement TDD-first** | Test-before-code | Level 2 of the [eval stack](07-evals-and-benchmarks.md) — the spec acceptance suite; each §9 criterion becomes a test | The eval suite gates deployment. If the suite cannot be written, that is a Cat 1 spec failure surfaced before code |
| **6. Learn openly** | Amend specs when implementation reveals new constraints | [Spec Gap Log](../sdd/06-living-specs.md) entries; constraint library updates | The diagnostic protocol from [Failure Modes](../theory/05-failure-as-design-signal.md) — categorize every learning (Cat 1–6+7), trace to the artifact that needs to change. Structural learnings flow back into Phase 3 |
| **7. Independent review** | Validate against specs and ADRs (not the implementer) | [Intent Review Before Output Review](05-reviewing-intent.md) artifacts; Level 4 production sampling | Output review answers *"did the agent follow the spec?"* — not *"do I agree with this output?"* |
| **8. Continuous refinement** | Backlog maintenance between sprints | Constraint-library updates; archetype-catalog updates if a new variant surfaced; Level 3 regression baseline updates | The [Four Signal Metrics](06-metrics.md) — trends, not single data points — drive the next sprint's spec priorities |

---

## Where ADRs and the spec touch

ADRs are about architecture; the spec is about behavior. ADRs change rarely; specs evolve with every learning event.

| ADR type | Maps onto spec section |
|---|---|
| Architectural choice (which library / service / pattern) | §6 (Invariants) — *"the system uses X, may not use Y"* |
| Authorization decision (what the agent may access) | §8 (Authorization Boundary) |
| Capability decision (what tools exist) | §7 (Tool Manifest) |
| Risk-tier decision (oversight model) | §4 (Archetype Declaration's oversight model) |
| Process decision (review cadence, escalation policy) | §12 (Validation Checklist) |

Some ADRs have no spec consequence ("we considered X and rejected it"). They still belong in the team's ADR archive as institutional memory; they just don't generate spec changes.

The book's [Architectural Decision Records](../sdd/08-architectural-decision-records.md) chapter goes deeper on the format and the relationship.

---

## What this mapping does NOT solve

Three places where the two frameworks pull in different directions:

1. **Ownership of the spec.** DevSquad assumes shared team property; the book is closer to single-author + reviewers. Pick one and be consistent.
2. **Sprint cadence vs. agent task cadence.** DevSquad's sprint is the human cadence; the book's metrics operate on the per-agent-run cadence. Run both; don't try to collapse them.
3. **ADR-as-decision vs. spec-as-control.** ADRs are decisions the team made; specs are the control surface the agent runs against. Some ADRs intentionally have no spec section — that's fine.

---

## Therefore

> **The book's design vocabulary and DevSquad's delivery cadence compose cleanly when the artifact mapping is explicit. Run the cadence; produce the artifacts at the named phases; let the disciplines compound. The mapping table above is the contract; the rest of Part 5 is the detail per discipline.**

---

## References

- Microsoft. (2026). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot.
- Nygard, M. (2011). *Documenting Architecture Decisions.* — The original ADR format both frameworks inherit from.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)
- [Architectural Decision Records](../sdd/08-architectural-decision-records.md)
- [Co-adoption with DevSquad](13-co-adoption-with-devsquad.md) — the strategy chapter for combining the two

**This pattern enables:**
- [Adoption Playbook](11-adoption-playbook.md) — adoption guidance for teams not on DevSquad
- All of Part 5 (Ship) — every chapter applies within DevSquad's cadence at the phase identified above

---
