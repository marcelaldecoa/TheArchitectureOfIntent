# Retry with Structured Feedback

---

> *"The first attempt failed. Tell the agent exactly what went wrong before asking it to try again."*

---

## Context

An agent produced output that failed validation. The output is not catastrophically wrong — it missed a constraint, had a formatting error, or omitted a required section. A second attempt with guidance about what specifically was wrong has a reasonable chance of succeeding.

---

## Problem

Blind retries — re-executing the same spec without providing the failure report — tend to produce the same failure. The agent doesn't know what went wrong. Conversely, unlimited retries create loops where the agent burns tokens and time without converging on a correct output.

---

## Forces

- **Retry cost vs. restart cost.** A retry that succeeds saves the cost of restarting the full pipeline. A retry that fails wastes additional time. The expected value determines whether retry is worthwhile.
- **Guidance quality vs. guidance overhead.** Detailed failure reports help the agent correct its output. But producing a detailed failure report requires validation logic that may be complex.
- **Convergence vs. oscillation.** Some failures are correctable with feedback (missing section, wrong format). Others oscillate — the agent fixes one thing and breaks another. The retry limit prevents infinite oscillation.

---

## The Solution

When output fails validation, **re-execute with the validation failure report as additional context** — subject to a declared retry limit.

**Retry structure:**

1. **Validate output** against the spec's success criteria. Produce a structured failure report: which criteria failed, what was expected, what was received.
2. **Re-invoke the agent** with the original spec plus the failure report. The failure report is injected as additional context: "Your previous output failed the following criteria: [structured list]. Revise your output to address these specific issues."
3. **Validate again.** If the second attempt passes, proceed. If it fails, **halt** — do not retry again.
4. **Maximum retry count is declared in the spec.** Typically 1 (one retry after initial failure). Rarely more than 2. Never unlimited.
5. **Both failure reports are preserved** for diagnosis. The pair (attempt 1 failure, attempt 2 failure) is diagnostic data for improving the spec.

**When retry is appropriate:**
- Formatting errors, missing sections, violated structural constraints
- Outputs that are partially correct but missed specific criteria

**When retry is not appropriate:**
- The spec itself is flawed (retry produces the same failure — fix the spec instead)
- The failure is model-level (hallucination, confidence miscalibration — retry won't help)
- The task exceeds the agent's capability (no amount of feedback will produce a correct output)

---

## Resulting Context

- **Simple failures are self-correcting.** Formatting issues and minor omissions are resolved without human intervention.
- **The retry limit prevents waste.** Two failures signal that the problem is not correctable by feedback — it requires spec review or human intervention.
- **Failure reports improve the spec.** Patterns in retry failures reveal where the spec is systematically ambiguous.

---

## Therefore

> **When output fails validation, re-execute with the structured failure report as additional context. Limit retries to 1-2 attempts. If the second attempt fails, halt and surface both failure reports for diagnosis. Never retry blindly.**

---

## Connections

- [Sequential Pipeline](sequential-pipeline.md) — retry is a per-stage behavior within a pipeline
- [Output Validation Gate](../safety/output-validation-gate.md) — validation produces the failure report that feeds the retry
- [The Idempotent Tool](../integration/idempotent-tool.md) — retries require idempotent tools to prevent duplicate side effects
- [Six Failure Categories](../../agents/07-failure-modes.md) — retry is appropriate for spec failures and capability failures, not for model-level failures
- [The Living Spec](../../sdd/06-living-specs.md) — repeated retry failures are signals to update the spec
