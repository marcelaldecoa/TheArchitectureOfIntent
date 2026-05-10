# Specify in practice — Coding-agent pipeline

**Part 2 · SPECIFY · Scenario 2 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-E. v1.x source: [examples/02-code-generation-pipeline/spec.md](../../examples/02-code-generation-pipeline/spec.md) and [examples/03-coding-agent/spec.md](../../examples/03-coding-agent/spec.md).

---

## What this chapter will cover

The chapter writes the canonical 12-section spec for a session-scoped coding agent doing PR-shaped work. The spec is meaningfully different from a customer-support spec because the agent's actions are mostly text (code, tests, commit messages) but with structural side effects (a CI run, a PR opened, a branch pushed) that have to be governed.

Highlights:

- **§3 Authorized scope** — touch files matching the task description; create branches; push to non-protected branches; open PRs; run tests.
- **§4 NOT-authorized scope** — push to `main`/`master`; delete or skip existing tests (the canonical Cat 1/Cat 3 hybrid); modify CI workflows; install global dependencies; use unrestricted shell.
- **§4 Composition Declaration (Pattern E — mode-switching)** — Frame, Plan, Implement, Review modes with cross-mode invariants. Mode transitions encoded as agent-emitted markers.
- **§4 Cost Posture sub-block** — model tier per mode (Sonnet for Plan and Review, Haiku candidates for Frame's repo-scan when the codebase is large), per-session token ceiling, what happens when the ceiling is approached.
- **§6 Invariants** — *test-skip set is monotonic non-increasing across the session* (no test deletion). *Branch protection on `main` is not bypassed*. *Tool manifest does not grant unrestricted shell*.
- **§11 Execution instructions** — when to surface ambiguity, how to write a PR description that names the spec it implements, how to flag a Cat 7-adjacent failure (model misread the file).

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)
- [Coding Agents](../../agents/08-coding-agents.md)
- [Composing Archetypes](../../architecture/05-composing-archetypes.md)

## Source material

Two v1.x specs feed this chapter: [examples/02-code-generation-pipeline/spec.md](../../examples/02-code-generation-pipeline/spec.md) (pipeline-scoped) and [examples/03-coding-agent/spec.md](../../examples/03-coding-agent/spec.md) (session-scoped). v2.0.0 unifies them around the session-scoped form and makes the mode-switching declaration explicit.
