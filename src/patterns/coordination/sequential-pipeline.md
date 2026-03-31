# Sequential Pipeline

---

> *"When B needs A's output, there is no parallelism to find — only a dependency to honor."*

---

## Context

You are building a multi-step agent workflow where each step depends on the output of the previous step. A code generation pipeline produces a repository scaffold, then generates controllers, then generates tests, then validates against standards — each step consuming the prior step's output.

---

## Problem

Without explicit pipeline structure, multi-step workflows are implemented as one long agent conversation. The agent is asked to do everything in one pass. Intermediate results are not validated, checkpoints don't exist, and when something fails at step 7, the entire conversation must be restarted. Debugging is difficult because there is no clear stage at which the failure occurred.

---

## Forces

- **Single-pass simplicity vs. checkpoint recoverability.** One long conversation is simple to set up. But when it fails, there is no way to resume from a known-good intermediate state.
- **Tight coupling vs. stage independence.** Stages that share the same conversation context are tightly coupled — one stage's side effects affect all subsequent stages. Independent stages can be retried, replaced, or re-ordered.
- **Validation at the end vs. validation at each stage.** End-to-end validation catches the final result. Stage-level validation catches errors early, before they compound through downstream stages.
- **Latency vs. quality assurance.** Adding validation between stages increases total execution time. But the time saved by catching errors early outweighs the checkpoint overhead.

---

## The Solution

Structure the workflow as a **declared sequence of stages**, each with its own spec, input/output contract, and validation step.

**Pipeline structure:**

1. **Declare the stage order.** The pipeline spec lists stages in dependency order. Each stage names: the agent or executor, its archetype, its input contract (what it receives), and its output contract (what it produces).
2. **Define inter-stage contracts.** Agent A's output schema must match Agent B's input schema. This contract is declared and validated at the handoff — not assumed.
3. **Validate between stages.** After each stage completes, validate the output against the spec's success criteria for that stage. A failed validation halts the pipeline at that stage, not at the end.
4. **Store intermediate results.** Each stage's output is persisted. If Stage 4 fails, stages 1–3 don't need to be re-executed. The pipeline resumes from the last successful checkpoint.
5. **Handle stage failure explicitly.** The pipeline spec declares what happens when a stage fails: retry (with the Retry with Structured Feedback pattern), escalate, or halt. No silent failure propagation.

**Example pipeline declaration:**
```
Stage 1: Schema Parser (Advisor) → parsed schema
Stage 2: Controller Generator (Executor) → controller files
Stage 3: Test Generator (Executor) → test files
Stage 4: Standards Validator (Guardian) → validation report
Stage 5: Assembly (Synthesizer) → complete scaffold

Failure at any stage: halt, return stage output + validation report
Retry policy: max 1 retry per stage with failure report as additional input
```

---

## Resulting Context

- **Errors are caught at the stage they occur.** A constraint violation in Stage 2 is caught before Stage 3 builds on incorrect output.
- **Recovery is partial, not total.** When a stage fails, only that stage and its downstream dependents are re-executed.
- **Each stage is independently testable.** Stage 2 can be tested with representative inputs without running Stages 1, 3, 4, and 5.
- **Pipeline evolution is modular.** A new stage can be inserted, a stage can be replaced with a better agent, or a stage can be split — without rewriting the entire workflow.

---

## Therefore

> **Structure multi-step agent workflows as declared sequential pipelines with explicit stage order, inter-stage contracts, checkpoint validation, and stored intermediate results. Each stage has its own spec and can be tested, retried, or replaced independently.**

---

## Connections

- [Agent-to-Agent Contract](agent-contract.md) — inter-stage contracts define what one agent sends and what the next agent expects
- [Retry with Structured Feedback](retry-feedback.md) — how a failed stage is re-attempted with the failure report as additional input
- [Checkpoint and Resume](../state/checkpoint-resume.md) — how pipeline state is persisted for recovery
- [The Idempotent Tool](../integration/idempotent-tool.md) — stage retries require idempotent operations
- [Parallel Fan-Out](parallel-fan-out.md) — when stages don't have dependencies, they can run in parallel instead
- [Output Validation Gate](../safety/output-validation-gate.md) — inter-stage validation catches errors before they compound
