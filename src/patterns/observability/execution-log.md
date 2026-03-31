# Structured Execution Log

---

> *"If you can't see what the agent did, you can't fix what the agent did wrong."*

---

## Context

An agent executed a task. The output may be correct or incorrect. You need to understand what happened: what tools were called, with what inputs, producing what outputs, in what order, and how long each step took.

---

## Problem

Without structured logs, debugging agent behavior requires reproducing the failure from scratch — re-running the same spec and hoping the same behavior recurs. Conversation logs capture the human-agent interaction but not the tool calls, retrieval queries, or internal reasoning that produced the output.

---

## The Solution

Log every agent action as a **structured event** with standardized fields.

**Required fields per log entry:**
- `timestamp` — when the action occurred
- `spec_id` — which spec authorized this execution
- `action_type` — tool_call, retrieval_query, output_generation, escalation
- `tool_name` — which tool was invoked (if applicable)
- `input_summary` — what was sent (redacted for sensitive fields)
- `output_summary` — what was received
- `duration_ms` — how long the action took
- `status` — success, failure, timeout

Logs are **structured (JSON), append-only, and immutable.** They are not free-text debug messages.

---

## Therefore

> **Log every agent action as a structured event with spec_id, tool_name, input/output summaries, and timing. Logs are structured, append-only, and immutable. They are the diagnostic foundation for everything else in observability.**

---

## Connections

- [Distributed Trace](distributed-trace.md) — traces correlate logs across multiple agents in a pipeline
- [Audit Trail](audit-trail.md) — the audit trail is a compliance view of the execution log
- [Anomaly Detection Baseline](anomaly-baseline.md) — baselines are computed from aggregated execution logs
- [Cost Tracking](cost-tracking.md) — cost is derived from log data (token counts, durations, tool calls)
