# Checkpoint and Resume

---

> *"When a long pipeline fails at step 7, don't restart from step 1."*

---

## Context

A multi-stage pipeline processes a task that takes significant time or resources. If it fails midway, re-executing from the beginning wastes the work already completed and may be non-deterministic (producing different intermediate results the second time).

---

## Problem

Without checkpoints, pipeline failure is all-or-nothing. Every transient error — a timeout, a rate limit, a temporary service unavailability — requires full re-execution. The cost of failure is proportional to total pipeline length, not to the failed stage.

---

## The Solution

Persist pipeline state at **declared checkpoints** so execution can resume from the last successful stage.

1. **Checkpoint after each stage completes validation.** Only validated output is checkpointed — incomplete or invalid intermediate results are not.
2. **Checkpoint includes the shared context store** plus metadata: which stage completed, when, with what spec version.
3. **Resume loads the checkpoint** and begins execution at the next stage. Prior stages are not re-executed.
4. **Checkpoint storage is declared in the spec.** File system, object store, database — the location is explicit, not defaulted.
5. **Checkpoint expiration is declared.** Stale checkpoints from abandoned executions are cleaned up. A checkpoint from three weeks ago is unlikely to be valid for resumption.

---

## Therefore

> **Persist validated intermediate results at declared checkpoints. When a pipeline fails, resume from the last checkpoint instead of restarting. Declare checkpoint storage, expiration, and the conditions under which a checkpoint is valid for resumption.**

---

## Connections

- [Sequential Pipeline](../coordination/sequential-pipeline.md) — checkpoints are placed between pipeline stages
- [Shared Context Store](shared-context.md) — the checkpoint persists the store's contents
- [The Idempotent Tool](../integration/idempotent-tool.md) — resuming from a checkpoint may re-execute the failed stage; the tools must be idempotent
- [Artifact Store](artifact-store.md) — completed pipeline outputs are stored as artifacts, not checkpoints
