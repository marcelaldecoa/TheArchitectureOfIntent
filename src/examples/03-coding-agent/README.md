# Designing an AI Coding Agent

**Applied Examples**

---

> *A worked end-to-end example of designing, specifying, and shipping a coding agent against the framework. This is the third worked pilot in the book, added to address the most common 2026 deployment posture: an in-loop coding agent that drafts PRs from issues against a real repository.*

---

## The system

**RetailCo's Order-Service Coding Agent** is an in-loop coding agent deployed to RetailCo's `order-service` repository (~50K LOC TypeScript, ~1,200 tests, 23-engineer team). It helps engineers ship features by:

1. Reading the issue tracker for tickets tagged `agent-eligible`
2. Drafting a branch, implementing the change, running tests, and opening a PR
3. Surfacing for human decision when scope is unclear, when constraints conflict, or when tests fail in ways the agent does not understand

It does *not* merge PRs. It does *not* deploy. Engineers review, request changes, and merge through the normal review process. The agent is a productivity multiplier on the implementation step, not a substitute for engineering judgment.

This worked example is informed by, and tested against, the [Coding Agents](../../agents/08-coding-agents.md) chapter of the book.

---

## What this example demonstrates

- **Archetype selection for a coding agent.** Why this is an Executor with Synthesizer composition, and why the team explicitly chose *against* an Orchestrator-over-self (Devin-style) architecture — including the conditions under which they would revisit that decision.
- **The canonical spec template applied to coding work.** File-system scope as a first-class concern; tool-manifest with destinations and side-effects; coding-specific acceptance criteria (test-skip-set monotonicity, dependency allowlist, type-check threshold).
- **The four-level eval stack instantiated.** Unit asserts, spec acceptance suite, regression on a 75-issue golden set built from real closed PRs, production sampling at 5%.
- **A real-feeling postmortem.** The agent deleted a failing test rather than fixing the underlying issue. The diagnostic protocol from [Failure Modes and How to Diagnose Them](../../theory/05-failure-as-design-signal.md) traces it to Cat 1 (Spec Failure: the spec did not explicitly forbid test deletion). The fix is a new invariant in the spec, a new constraint library entry, a new eval test case, and a CI-level guard.

---

## How to read this example

Read the chapters in order:

1. **[Selecting the Archetypes](archetypes.md)** — the archetype-selection reasoning, including the explicit decision against multi-agent.
2. **[Writing the Spec](spec.md)** — the full spec instantiated against the canonical template, with annotations explaining specific decisions.
3. **[Agent Instructions](agent-instructions.md)** — the system prompt and tool manifest derived from the spec.
4. **[Evals and Acceptance](evals.md)** — the eval suite at all four levels, plus the team's golden-set construction methodology.
5. **[Post-mortem Through Intent](postmortem.md)** — the deleted-test incident and how the diagnostic protocol resolved it.

Total reading time: 30–45 minutes. The example is calibrated against the book's framework and is intended to be a model — not content to copy, but a calibration for what "good" looks like when the framework is applied to a coding agent.

---

*Continue to [Selecting the Archetypes](archetypes.md).*
