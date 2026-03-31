# Distributed Trace Across Agents

---

> *"A request that flows through five agents needs one trace ID, not five separate logs."*

---

## Context

A request flows through multiple agents in a pipeline — a classifier routes it, a specialist processes it, a guardian validates it, an executor acts on it. Each agent produces its own execution log. You need to see the full journey as one unit.

---

## Problem

Without a trace ID propagated across agents, correlating logs requires manual timestamp matching and educated guessing. When something goes wrong, determining which agent's step caused the downstream failure requires reconstructing the flow from fragmented logs across different systems.

**Concrete scenario:** A fraud detection pipeline processes a transaction:
1. Classifier (Agent A) scores risk level
2. Specialist (Agent B) analyzes the account history if risk > 0.7
3. Guardian (Agent C) determines if the transaction should be blocked
4. Executor (Agent D) applies the decision (allow or block)

Transaction at 2026-03-15 14:22:00 fails. Four separate logs exist: Agent A's log (no errors, scored 0.75). Agent B's log (timeout connecting to account-history-db). Agent C's log (missing data, defaults to "block"). Agent D's log (blocked transaction). You have to manually correlate by timestamp and infer that Agent B's timeout cascaded. With dozens of transactions per minute, manual correlation is impossible.

---

## Forces

- **Need end-to-end visibility** (see the full path) vs. **log system performance** (adding trace IDs to every log entry adds overhead)
- **Need fine-grained per-agent span IDs** vs. **keeping the schema simple** (too many IDs becomes noise)
- **Need the trace to survive handoffs** vs. **need agents to not know about each other's trace format** (minimal coupling)
- **Need logs to be retrievable by trace ID** vs. **log storage and indexing costs** (indexing all traces is expensive)

---

## The Solution

Propagate a **trace ID** through every agent in the pipeline. Each agent includes the trace ID in its execution log entries.

1. **Generate a trace ID at the pipeline entry point.** The first agent (or the pipeline orchestrator) creates a unique trace ID.
2. **Pass the trace ID through agent-to-agent handoffs.** It is part of the shared context, not a tool parameter.
3. **Each agent includes the trace ID in every log entry.** Query all logs by trace ID to see the full journey.
4. **Add span IDs for per-agent segments.** The trace ID identifies the pipeline execution; span IDs identify each agent's contribution within it.

**Example:** The fraud detection pipeline. The spec declares:
```
observability:
  tracing:
    enabled: true
    propagate_trace_id: true
    shared_context_key: "trace_id"
```
Request arrives at 2026-03-15 14:22:00 UTC for transaction tx-98765. The pipeline orchestrator generates trace_id `trace:fraud-detection:20260315142200-xyz789` and stores it in shared context.

Agent A (Classifier) executes, logs: `{"trace_id": "trace:fraud-detection:20260315142200-xyz789", "span_id": "span:a-001", "message": "Scored risk=0.75"}`. 

Agent B (Specialist) reads shared context, finds trace_id, logs: `{"trace_id": "trace:fraud-detection:20260315142200-xyz789", "span_id": "span:b-001", "message": "Timeout connecting to account-history-db at 14:22:04"}`.

Agent C and D do the same. Later, query logs by `trace_id = "trace:fraud-detection:20260315142200-xyz789"` and the full journey appears: A outputs → B timeout → C defaults to block → D blocks. One query, one trace, not four logs to painstakingly correlate.

---

## Resulting Context

- **Full request journeys are visible in one query**, traced from entry to exit
- **Failure points are immediately clear** — which agent failed or timed out
- **Per-agent performance is measurable** — span IDs show how long each agent took
- **Root cause analysis is straightforward** — follow the trace to the failure, don't guess

---

## Therefore

> **Propagate a trace ID through every agent in a multi-agent pipeline. Each agent logs with that trace ID. Query by trace ID to see the full request journey across all agents.**

---

## Connections

- [Structured Execution Log](execution-log.md) — each agent's log includes the trace ID
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — the trace follows the pipeline stages
- [Agent-to-Agent Contract](../coordination/agent-contract.md) — the trace ID is part of the handoff contract
- [Cost Tracking](cost-tracking.md) — per-trace cost aggregation shows the total cost of a multi-agent request