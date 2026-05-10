# Frame in practice — Internal docs Q&A (DevSquad)

**Part 1 · FRAME · Scenario 3 of 3**

---

> **v2.0.0-rc1 stub.** This chapter is the structural placeholder for Scenario 3's *Frame* walkthrough in v2.0.0. The full prose lands in PR-F of the v2.0.0 rollout (see [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md)). Unlike Scenarios 1 and 2, this scenario is **new for v2.0.0** — it has no v1.x source material. It is the DevSquad-flavored worked example that lets the book demonstrate composition with Microsoft DevSquad Copilot's working cadence at scenario grain rather than only at vocabulary grain.

---

## What this chapter will cover

The chapter walks a small platform team through the *Frame* activity for an **internal docs Q&A agent** — an agent that retrieves and summarizes from the company's engineering documentation, deployed for ~200 internal engineers. It is the first of five chapters that follow the same scenario across the five activities, and the running scenario throughout the book that demonstrates how the Architecture of Intent composes with DevSquad's eight-phase cadence.

Specifically, the chapter will name:

- **The archetype call.** **Synthesizer** (compose information from sources into a structured answer), with **Advisor** mode embedded for the "I don't know — here's where to look" path when retrieval grounds nothing useful. The team rejects **Executor** because the agent doesn't take actions; it produces text that humans act on.
- **The four-dimension calibration.** Agency: low — answers grounded in retrieved docs only. Autonomy: high — runs end-to-end without per-question approval. Responsibility: distributed — the docs author owns the source-of-truth, the platform team owns the retrieval boundary, the asker owns the decision they make from the answer. Reversibility: high — bad answers cost ~minutes of one engineer's time.
- **DevSquad activity mapping (inline).** Frame happens during DevSquad's *envisioning phase* and the *kickoff* ceremony. The framework's three questions feed the team's envision document; the archetype call lands in the kickoff ADR. The chapter shows the artifacts side-by-side.
- **Composition Declaration.** Synthesizer is the governing archetype; Advisor is an embedded mode for the no-confident-answer path. Pattern A (Confirm-then-Act) does **not** apply — there's no act. Cross-mode invariant: every answer cites a doc, or names that it can't.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Pick an Archetype](../../architecture/02-canonical-intent-archetypes.md) — the Synthesizer entry
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operating/12-devsquad-mapping.md)
- [Co-adoption with DevSquad Copilot](../../operating/13-co-adoption-with-devsquad.md)

## Why a third scenario at all

S1 (customer-support) is the canonical Executor with embedded Guardian; S2 (coding pipeline) is the canonical mode-switching composition. S3 fills two gaps: a **Synthesizer** primary archetype (the other two are Executor-flavored) and a **DevSquad-native team** as the building org (the other two are framework-only). Without S3, the book demonstrates DevSquad composition only at vocabulary grain in Part 5; with S3, the demonstration runs the full five activities.
