# Parallel Fan-Out

---

> *"When the tasks don't depend on each other, don't make them wait for each other."*

---

## Context

You have multiple subtasks that can be executed independently — analyzing five documents simultaneously, generating code for three independent modules, running validation checks against different criteria. No subtask depends on another's output.

---

## Problem

Running independent tasks sequentially wastes time. The total duration is the sum of all task durations instead of the maximum. But parallel execution introduces new failure modes: partial completion (three of five subtasks succeed), result merging (how independent results become a coherent whole), and resource contention (all subtasks hitting the same API simultaneously).

---

## Forces

- **Speed vs. coordination complexity.** Parallel execution is faster. But coordinating results, handling partial failure, and managing shared resources adds complexity that sequential execution avoids.
- **Independence assumption vs. hidden dependencies.** Tasks appear independent but may share resources (database connections, API rate limits, file system paths). Unrecognized dependencies produce concurrency bugs.
- **All-or-nothing vs. best-effort.** Should the overall task fail if one subtask fails? All-or-nothing is safer but wasteful when most subtasks succeed. Best-effort is more aligned with the cost of reprocessing, but uneven results can be hard to merge.
- **Merge determinism vs. merge flexibility.** Results from parallel tasks must be combined. A deterministic merge (concatenate in order) is simple but may not fit all cases. A flexible merge (synthesize across results) requires another agent but handles complex combinations.

---

## The Solution

Dispatch independent subtasks in parallel with a **declared merge strategy and explicit partial failure handling**.

**Fan-out structure:**

1. **Declare subtask independence.** The pipeline spec explicitly states that these tasks have no data dependencies. If they do, use Sequential Pipeline instead.
2. **Each subtask has its own spec.** Each parallel branch operates under its own spec with its own constraints, tool manifest, and success criteria.
3. **Declare the merge strategy.** How results are combined:
   - **Concatenate** — results are appended in a declared order. Simplest.
   - **Key-merge** — results are merged by a shared key (e.g., each subtask produces results for a different entity).
   - **Synthesis** — a Synthesizer agent combines results into a coherent whole.
4. **Declare partial failure policy.** What happens when some subtasks succeed and others fail:
   - **All-or-nothing** — if any subtask fails, the entire fan-out fails. Use for tasks where partial results are meaningless.
   - **Best-effort with flagging** — return successful results and flag failed subtasks. Use when partial results are useful and failed subtasks can be retried independently.
5. **Respect shared resource limits.** If subtasks share a rate-limited API, declare a concurrency limit. Do not assume the API can handle all subtasks simultaneously.

---

## Resulting Context

- **Total execution time drops to the duration of the slowest subtask.** Instead of summing all durations, parallel execution takes the maximum.
- **Partial failure is handled explicitly.** The merge strategy and failure policy are declared, not discovered at runtime.
- **Subtasks are independently retryable.** A failed subtask can be retried without re-executing successful ones.

---

## Therefore

> **When subtasks are independent, dispatch them in parallel with a declared merge strategy and explicit failure policy. Each subtask runs under its own spec. Declare concurrency limits for shared resources.**

---

## Connections

- [Sequential Pipeline](sequential-pipeline.md) — use when tasks have dependencies; combine with fan-out for mixed topologies
- [Agent-to-Agent Contract](agent-contract.md) — each subtask's output must conform to the merge contract
- [Rate Limiting](../safety/rate-limiting.md) — parallel subtasks may overwhelm shared resources without throttling
- [Supervisor Agent](supervisor.md) — a supervisor can monitor parallel workers and intervene on coordination failures
