# The Idempotent Tool

---

> *"If the network fails and the agent retries, the customer should not be charged twice."*

---

## Context

An agent calls a state-changing tool. The call may succeed but the response may be lost — network timeout, process crash, transient error. The agent doesn't know whether the operation completed. It retries.

---

## Problem

If the tool is not idempotent, the retry produces a duplicate effect: a second charge, a second email, a second record creation. The agent cannot distinguish "the first call failed" from "the first call succeeded but I didn't get the receipt." Non-idempotent tools in agent systems produce duplicate actions at machine speed.

---

## Forces

- **Simplicity vs. safety.** Non-idempotent tools are simpler to build. But they are unsafe in any system where retries are possible — which includes every networked system.
- **Design cost vs. failure cost.** Making tools idempotent requires design effort (idempotency keys, upsert logic, status checks). But the cost of duplicate state changes — double charges, duplicate records, repeated notifications — is higher.
- **Stateless protocol vs. stateful operation.** The tool protocol (HTTP, MCP) is typically stateless. But the operation it performs may require tracking whether a prior call completed. Bridging this gap is the tool designer's responsibility.

---

## The Solution

Design state-changing tools so that **calling them twice with the same inputs produces the same result as calling them once**.

**Techniques:**

1. **Idempotency key.** The caller provides a unique key with each request. The tool checks whether that key has already been processed and returns the original result instead of re-executing.
2. **Check-then-act.** Before performing the operation, the tool checks whether the target state already reflects the desired change. If the record already exists with the expected values, the tool returns success without modifying anything.
3. **Upsert semantics.** Create-or-update: if the record exists, update it; if not, create it. The result is the same regardless of whether the call is the first or a retry.
4. **Status-based progression.** The tool moves the target through a state machine (pending → processing → completed). A retry that finds the state already at "completed" returns success. A retry that finds "processing" waits rather than initiating a parallel operation.

**Spec constraint:** When a spec authorizes a state-changing tool, it should note whether the tool is idempotent. If it is not, the spec must declare the maximum retry count (typically 0 — no retries) and the failure handling behavior.

---

## Resulting Context

- **Retries are safe.** When a tool call times out, the agent can retry without risk of duplicate effects.
- **Partial failure is recoverable.** In a pipeline, if one step fails and is retried, the overall pipeline produces a consistent result.
- **Monitoring is cleaner.** Duplicate detection becomes unnecessary when the tools themselves handle duplicates.

---

## Therefore

> **Design state-changing tools to produce the same result whether called once or twice with the same inputs. Use idempotency keys, check-then-act, or upsert semantics. When a tool cannot be made idempotent, the spec must declare no-retry behavior.**

---

## Connections

- [The State-Changing Tool](state-changing-tool.md) — idempotency is a design requirement for all state-changing tools
- [Retry with Structured Feedback](../coordination/retry-feedback.md) — retries depend on idempotent tools to avoid duplicate effects
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — pipeline reliability depends on idempotent operations at each stage
- [Checkpoint and Resume](../state/checkpoint-resume.md) — resuming from a checkpoint may re-execute the last incomplete step
