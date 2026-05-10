# Evolve in practice — Internal docs Q&A (DevSquad)

**Part 5 · EVOLVE · Scenario 3 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-F. New content for v2.0.0.

---

## What this chapter will cover

The chapter walks the docs-qa agent 90+ days post-launch and shows what the closed-loop discipline looks like for a Synthesizer agent embedded in a DevSquad team's *Refine continuously* phase. The composition with DevSquad is most concrete here, because *Refine continuously* is DevSquad's name for the activity AoI calls *Evolve*.

Specifically:

- **The spec evolution log as a docs-team signal.** This agent's Cat 1 amendments are mostly *"the spec said the agent should answer X but X isn't in the docs."* Those amendments don't change the agent — they get filed against the docs team as authoring tasks. The chapter argues this is the highest-leverage evolution path for a Synthesizer: the agent reveals doc gaps that the docs team didn't know it had.
- **Cost Posture in steady state.** Haiku at scale generates a per-question cost an order of magnitude below the cost of the human time it saves. The chapter shows the cost trajectory and the one tier-shift event that broke even.
- **The 90-day refusal-rate trend.** Refusal rate started at 22% and dropped to 8% over the 90 days as the docs gaps it surfaced got authored. The chapter argues this is the *expected* trajectory — declining refusal rate is the closed loop working — and contrasts it with a degenerate case where refusal rate stays flat (the team isn't authoring, only filing) or drops *too fast* (the agent has stopped refusing when it should be).
- **Composition with DevSquad in steady state.** The team's *Refine continuously* phase uses the four signal metrics directly as backlog inputs for the next sprint. The chapter shows the artifacts: the metrics dashboard, the backlog filing pattern, the docs-team collaboration ritual.
- **Framework versioning in practice.** When [framework v2.1 lands](../07-framework-versioning.md), this team is the first one in the company to upgrade. The chapter walks what that upgrade looks like — what changes in the spec, what changes in the team's working practice, what doesn't change at all.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Framework Versioning](../07-framework-versioning.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operating/12-devsquad-mapping.md) — the *Refine continuously* phase
- [Co-adoption with DevSquad Copilot](../../operating/13-co-adoption-with-devsquad.md)
