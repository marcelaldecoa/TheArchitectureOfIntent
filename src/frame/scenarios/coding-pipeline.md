# Frame in practice — Coding-agent pipeline

**Part 1 · FRAME · Scenario 2 of 3**

---

> **v2.0.0-rc1 stub.** This chapter is the structural placeholder for Scenario 2's *Frame* walkthrough in v2.0.0. The full prose lands in PR-E of the v2.0.0 rollout (see [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md)). The existing worked pilots in [A Code Generation Pipeline](../../examples/02-code-generation-pipeline/README.md) and [Designing an AI Coding Agent](../../examples/03-coding-agent/README.md) are the v1.x source material this chapter will rework into the phase-by-phase form.

---

## What this chapter will cover

The chapter walks a working team through the *Frame* activity for a coding-agent pipeline: an Anthropic-Claude-Code-class or Cursor-class agent doing PR-shaped work on an established service repository. It is the first of five chapters that follow the same scenario across the five activities of the Architecture of Intent.

Specifically, the chapter will name:

- **The archetype call.** **Executor** as the governing archetype, with the team rejecting **Orchestrator** as overkill for a session-scoped agent. The discussion explicitly considers the 2026 pressure-point case for "coding agent as a sixth archetype" and rejects it in favor of the [composition first-class](../../architecture/05-composing-archetypes.md) framing — the agent uses Advisor, Executor, Synthesizer, and Guardian modes within a single session.
- **The four-dimension calibration.** Agency: medium — the agent decides which files to touch within an authorized scope. Autonomy: high — runs end-to-end on TDD discipline without per-step gates. Responsibility: shared with the reviewer — operational on the agent, authorial on the engineer. Reversibility: medium — git revert is cheap, but accumulated context across many sessions becomes harder to undo.
- **Composition Declaration (Pattern E — mode-switching).** Frame mode → Synthesizer (read repo, build mental model). Plan mode → Advisor (propose approach, surface ambiguity). Implement mode → Executor (TDD loop). Review mode → Guardian (check invariants before push). Cross-mode invariants documented inline.
- **The pre-spec hand-off.** Frame's output — archetype, dimensions, mode-switching declaration — flows into [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md).

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [Coding Agents](../../agents/08-coding-agents.md)
- [Composing Archetypes](../../architecture/05-composing-archetypes.md)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../../theory/03-agency-autonomy-responsibility.md)

## Source material

Two existing worked pilots inform this scenario: [A Code Generation Pipeline](../../examples/02-code-generation-pipeline/README.md) (the multi-stage pipeline view) and [Designing an AI Coding Agent](../../examples/03-coding-agent/README.md) (the single-session agent view). v2.0.0 keeps both as legacy reference while the phase-by-phase scenario chapters supersede them.
