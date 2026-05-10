# Delegate in practice — Coding-agent pipeline

**Part 3 · DELEGATE · Scenario 2 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-E. v1.x source: [examples/02-code-generation-pipeline/agent-instructions.md](../../examples/02-code-generation-pipeline/agent-instructions.md), [examples/03-coding-agent/agent-instructions.md](../../examples/03-coding-agent/agent-instructions.md).

---

## What this chapter will cover

The chapter binds patterns to the coding-agent spec written in [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md), names the oversight model, and walks through the build of a session-scoped coding agent with mode-switching composition (Pattern E).

Specifically:

- **System prompt as an authored stance.** The system prompt isn't a prompt-engineering exercise; it's the operationalization of the four-dimension calibration committed in Frame. It encodes the agent's NOT-authorized clauses, the mode markers (`<frame>`, `<plan>`, `<implement>`, `<review>`), and the spec-amendment escalation path.
- **Tool manifest by mode.** Frame mode: `read_file`, `list_dir`, `grep`. Plan mode: same plus `ask_user_question`. Implement mode: adds `edit_file`, `write_file`, `run_tests`, `run_linter`, `git_commit`. Review mode: adds `git_diff`, `git_push_non_protected`, `gh_pr_create`. **No mode** gets `unrestricted_shell` or `git_push_protected`.
- **Patterns bound from Part 4.** Spec Conformance Testing in CI (the spec's §9 acceptance criteria run on every PR). Test-skip-set monotonicity check as a CI guard. Distributed trace for the entire session. Per-session token ceiling enforced by the harness.
- **Oversight model.** **Pre-authorized scope with exception escalation** — the agent runs end-to-end without per-step gates, escalating only on (a) ambiguity in the spec, (b) attempt to touch a NOT-authorized file class, (c) test failure that cannot be diagnosed in N retries, (d) the per-session token ceiling.
- **Composition mechanics.** How mode transitions surface to the human in the loop (e.g., the PR description names which mode emitted which commit, the trace shows mode-switch events). Cross-mode invariants enforced as CI guards, not as prompt rules.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [Coding Agents](../../agents/08-coding-agents.md)
- [Composing Archetypes](../../architecture/05-composing-archetypes.md) — Pattern E (mode-switching)
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — the pre-authorized model
- [The Tool Manifest](../../patterns/capability/tool-manifest.md)
