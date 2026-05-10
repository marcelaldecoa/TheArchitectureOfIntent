# Delegate in practice — Internal docs Q&A (DevSquad)

**Part 3 · DELEGATE · Scenario 3 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-F. New content for v2.0.0.

---

## What this chapter will cover

The chapter binds patterns to the docs-qa spec written in [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) and walks through the build with DevSquad activity mapping inline — i.e., showing where DevSquad's `decompose` and `implement` agents do work that the framework's *Delegate* activity governs.

Specifically:

- **System prompt for a Synthesizer governing archetype.** Different shape from an Executor's prompt — emphasizes citation discipline and refusal patterns rather than action gates.
- **Tool manifest.** `retrieve_docs` (RAG; vector + lexical), `cite` (formatting), `escalate_to_advisor_mode` (when no doc grounds the question with confidence ≥ threshold). **No** action tools — the agent doesn't act on the docs, only synthesizes from them.
- **Patterns bound.** RAG with grounding (Capability category). Sensitive Data Boundary on the retrieval index (don't index unindexed-private docs). Output Validation Gate that blocks responses lacking a citation. Cost Tracking per Spec to surface the per-question ceiling to the platform team.
- **Oversight model.** **Monitoring** — the team observes a trace stream and the four signal metrics dashboard, intervening when first-pass-validation drops below 75% in any 4-hour window or oversight load spikes (which would indicate the agent is escalating questions it should be answering).
- **DevSquad mapping (inline).** Build happens during DevSquad's *Decompose that slice* and *Implement with TDD discipline* phases. The framework's tool manifest lives in DevSquad's `decompose` artifacts; the spec acceptance suite gates each commit per DevSquad's *Implement* phase definition. The chapter shows the artifacts side-by-side.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Retrieval-Augmented Generation](../../patterns/capability/rag.md)
- [Grounding with Verified Sources](../../patterns/capability/grounding.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operating/12-devsquad-mapping.md) — the *Decompose* + *Implement* phases
