# Specify in practice — Internal docs Q&A (DevSquad)

**Part 2 · SPECIFY · Scenario 3 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-F. **New for v2.0.0** — no v1.x source material.

---

## What this chapter will cover

The chapter writes the canonical 12-section spec for the internal docs Q&A agent framed in [Part 1's docs-qa scenario](../../frame/scenarios/docs-qa.md), and shows the spec being authored *during* DevSquad Copilot's *Spec the next slice* phase. The DevSquad activity mapping is shown inline — the framework's §1–§12 sections fill the same places in the team's slice spec that DevSquad's `specify` agent prompts for.

Highlights:

- **§1 Problem statement** — engineers waste ~12 minutes per "where is X documented?" question; we want sub-30-second answers grounded in the docs.
- **§2 Desired outcome** — observable success: *answers cite at least one doc URL or refuse cleanly; ≥80% first-answer satisfaction in 30-day rolling window*.
- **§3 Authorized scope** — answer factual questions about engineering docs; cite sources; refuse outside-domain questions.
- **§4 NOT-authorized scope** — code generation, decisions on behalf of teams, anything requiring HR or legal grounding.
- **§4 Composition Declaration** — Synthesizer (governing) with Advisor mode for the "I don't have a confident answer" path. Cross-mode invariant: every output names whether it's a synthesis or an "I don't know."
- **§4 Cost Posture** — Haiku tier with retrieval-augmented context; per-question ceiling that triggers fallback to Advisor mode if exceeded.
- **§6 Invariants** — *no answer without a citation*; *no claim of certainty without grounding*; *no leakage of unindexed-private docs*.
- **§9 Acceptance criteria** — eval set of 200 known-good Q-A pairs from docs-team curation; pass threshold ≥85%.
- **DevSquad mapping (inline).** §1, §2 → DevSquad envision document. §3, §4, §6 → DevSquad's slice plan. §11 → DevSquad's `implement` agent prompt. §9, §12 → DevSquad's `review` agent context.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)
- [The Intent Design Session](../../theory/07-intent-design-session.md) — the IDS happens here, but compressed to fit DevSquad's *Spec the next slice* time-box
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operating/12-devsquad-mapping.md)
