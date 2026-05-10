# Evolve in practice — Coding-agent pipeline

**Part 5 · EVOLVE · Scenario 2 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-E. v1.x source: [examples/03-coding-agent/postmortem.md](../../examples/03-coding-agent/postmortem.md).

---

## What this chapter will cover

The chapter walks the coding-agent pipeline 90+ days post-launch and shows what the closed-loop discipline looks like for an agent that emits PRs. Most of the *Evolve* work for this scenario is structural rather than conversational — every Cat 1 amendment ships as a CI-guard change, a tool-manifest tightening, or a NOT-authorized clause refinement.

Specifically:

- **Spec evolution log structured for code.** Each amendment names which CI guard or manifest field it changed. The log is co-located with the spec itself, in the repo. The chapter argues this is the form the spec evolution log has to take for a coding agent — a parallel doc disconnected from the code is the failure mode.
- **The deleted-tests failure, post-mortem.** The canonical Cat 1 / Cat 3 hybrid that compounded across multiple sessions before the structural fix landed. The chapter shows the fix landing in CI as a test-skip monotonicity check and as a §4 NOT-authorized clause; both fixes ship together because either alone is fragile.
- **Per-mode evolution.** Because the agent uses mode-switching composition, the chapter shows which modes generated the most amendments. Frame mode generated almost none (it's all read-only); Plan mode generated several (this is where ambiguity surfaces); Implement mode generated the most by raw count but the lowest-stakes amendments; Review mode generated the *highest-stakes* amendments because those are the ones that caught structural drift.
- **The model-tier rotation.** What happened when Sonnet 4.7 became available — the chapter walks the model-upgrade validation pattern in the team's CI, shows the spec amendments triggered by capability differences, and argues why Cost Posture had to be re-baselined.
- **Discipline-Health Audit.** The 11-anti-pattern audit at the 90-day mark. The chapter shows where this team's score differed from S1's — a Synthesizer-flavored docs agent fails differently from an Executor-flavored coding agent, and both fail differently from a Synthesizer-flavored Q&A agent.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Coding Agents](../../agents/08-coding-agents.md)
- [Model Upgrade Validation](../../patterns/deployment/model-upgrade.md)
- [Signs Your Architecture of Intent Is Degrading](../../operating/15-anti-patterns.md)
