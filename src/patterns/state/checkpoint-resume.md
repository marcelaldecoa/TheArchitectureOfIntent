# Checkpoint and Resume

---

> *"When a long pipeline fails at step 7, don't restart from step 1."*

---

## Context

A multi-stage pipeline processes a task that takes significant time or resources. If it fails midway, re-executing from the beginning wastes the work already completed and may be non-deterministic (producing different intermediate results the second time).

---

## Problem

Without checkpoints, pipeline failure is all-or-nothing. Every transient error — a timeout, a rate limit, a temporary service unavailability — requires full re-execution. The cost of failure is proportional to total pipeline length, not to the failed stage.

**Concrete scenario:** A data processing pipeline with 8 stages: fetch data (slow), validate schema, deduplicate, enrich with external APIs, transform, aggregate, generate report, notify stakeholders. At stage 6 (aggregate), an external API becomes temporarily unavailable. The pipeline fails. Re-running restarts from stage 1, re-fetching all data, re-validating, re-deduplicating — all already-completed work. The fetch stage takes 45 minutes; the aggregate stage takes 2 minutes. A transient 2-minute API error costs 47 minutes of re-execution.

---

## Forces

- **Need resumption to save time** (don't redo completed work) vs. **complexity of managing intermediate state** (checkpoint format, validity checks)
- **Need checkpoints to be small and fast** vs. **need them to capture enough state** (incomplete checkpoints aren't useful for resumption)
- **Need automatic checkpoint validation** vs. **need human oversight** (invalid checkpoints will silently produce wrong results)
- **Need checkpoints to be retained** vs. **storage and cleanup costs** (stale checkpoints accumulate)

---

## The Solution

Persist pipeline state at **declared checkpoints** so execution can resume from the last successful stage.

1. **Checkpoint after each stage completes validation.** Only validated output is checkpointed — incomplete or invalid intermediate results are not.
2. **Checkpoint includes the shared context store** plus metadata: which stage completed, when, with what spec version.
3. **Resume loads the checkpoint** and begins execution at the next stage. Prior stages are not re-executed.
4. **Checkpoint storage is declared in the spec.** File system, object store, database — the location is explicit, not defaulted.
5. **Checkpoint expiration is declared.** Stale checkpoints from abandoned executions are cleaned up. A checkpoint from three weeks ago is unlikely to be valid for resumption.

**Example:** The data-processing pipeline above. The spec declares:
```
checkpoints:
  store: "s3://pipeline-checkpoints/data-processing/"
  expiration_hours: 72
  stages:
    - name: "fetch"
      checkpoint_on: "success"
      store_key: "data_fetched"
    - name: "validate"
      checkpoint_on: "success"
      store_key: "data_validated"
    - name: "aggregate"
      checkpoint_on: "success"
      store_key: "data_aggregated"
```
First run: fetch completes, checkpoint saved. Validate completes, checkpoint saved. At aggregate, the API fails. Checkpoint file exists at `s3://pipeline-checkpoints/data-processing/run-abc123/stage-aggregate.json`.

Re-run: Pipeline loads the aggregate stage's checkpoint, finds it's 45 minutes old, spec version matches, data is intact. Resume from stage aggregate+1 (transform). No re-fetch, no re-validate. Total time: 4 minutes instead of 47.

---

## Resulting Context

- **Failed pipelines resume in minutes instead of hours**, proportional to the remaining stages, not the total pipeline
- **Intermediate results are preserved and auditable**, not re-derived non-deterministically
- **Resource waste is minimized** for transient failures
- **Checkpoint validity is explicit**, based on spec version matching and metadata validation

---

## Therefore

> **Persist validated intermediate results at declared checkpoints. When a pipeline fails, resume from the last checkpoint instead of restarting. Declare checkpoint storage, expiration, and the conditions under which a checkpoint is valid for resumption.**

---

## Connections

- [Sequential Pipeline](../coordination/sequential-pipeline.md) — checkpoints are placed between pipeline stages
- [Shared Context Store](shared-context.md) — the checkpoint persists the store's contents
- [The Idempotent Tool](../integration/idempotent-tool.md) — resuming from a checkpoint may re-execute the failed stage; the tools must be idempotent
- [Artifact Store](artifact-store.md) — completed pipeline outputs are stored as artifacts, not checkpoints