# Validate in practice — Internal docs Q&A (DevSquad)

**Part 4 · VALIDATE · Scenario 3 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-F. New content for v2.0.0.

---

## What this chapter will cover

The chapter walks the validation phase for the docs Q&A agent and shows the DevSquad team running it through their *Review in an independent context* phase.

Specifically:

- **Pre-launch eval suite.** 200 curated Q-A pairs from docs-team (factual questions with known authoritative-doc answers). Pass threshold ≥ 85%. Held-out 50 out-of-scope questions where the correct answer is *"this isn't in our docs"* — refusal precision matters as much as answer accuracy.
- **Citation-grounding validation.** Every answer must cite at least one doc URL; the validation suite checks that the cited URL contains the claimed information (a Cat 1 fail is a hallucinated citation, the most dangerous Synthesizer failure mode).
- **DevSquad mapping (inline).** The team's `review` agent runs in a fresh sub-agent context — i.e., without the Implement-phase context — and judges answers against the spec's §9 acceptance criteria. The chapter shows the artifacts: review prompts, judgments, the two reviewer-disagreement cases that the team adjudicated.
- **The four signal metrics for a Synthesizer.** Spec-gap rate = questions that triggered a docs amendment (the agent surfaced *real* doc gaps). First-pass-validation = answers the asker accepted. Cost per correct outcome = tokens + reviewer-minutes / accepted answers. Oversight load = reviewer-minutes / 1000 questions.
- **No Cat 7 here either.** Like the other two scenarios, this agent has no perception-action interface. The chapter notes this explicitly to anchor when Cat 7 *does* apply (computer-use, browser-use, robotic agents — not retrieval-and-text).
- **The "doc that doesn't exist yet" signal.** The most valuable diagnostic finding for this scenario is a high spec-gap rate concentrated on a topic — that's an instruction to the docs team about what to write, not a failure of the agent.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. **Validate** | *(this chapter)* |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Failure Modes and How to Diagnose Them](../../theory/05-failure-as-design-signal.md)
- [Four Signal Metrics](../../operating/06-metrics.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operating/12-devsquad-mapping.md) — the *Review in independent context* phase
