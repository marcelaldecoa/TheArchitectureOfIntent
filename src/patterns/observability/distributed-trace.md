# Distributed Trace Across Agents

---

> *"A request that flows through five agents needs one trace ID, not five separate logs."*

---

## Context

A request flows through multiple agents in a pipeline — a classifier routes it, a specialist processes it, a guardian validates it, an executor acts on it. Each agent produces its own execution log. You need to see the full journey as one unit.

---

## Problem

Without a trace ID propagated across agents, correlating logs requires manual timestamp matching and educated guessing. When something goes wrong, determining which agent's step caused the downstream failure requires reconstructing the flow from fragmented logs across different systems.

---

## The Solution

Propagate a **trace ID** through every agent in the pipeline. Each agent includes the trace ID in its execution log entries.

1. **Generate a trace ID at the pipeline entry point.** The first agent (or the pipeline orchestrator) creates a unique trace ID.
2. **Pass the trace ID through agent-to-agent handoffs.** It is part of the shared context, not a tool parameter.
3. **Each agent includes the trace ID in every log entry.** Query all logs by trace ID to see the full journey.
4. **Add span IDs for per-agent segments.** The trace ID identifies the pipeline execution; span IDs identify each agent's contribution within it.

---

## Therefore

> **Propagate a trace ID through every agent in a multi-agent pipeline. Each agent logs with that trace ID. Query by trace ID to see the full request journey across all agents.**

---

## Connections

- [Structured Execution Log](execution-log.md) — each agent's log includes the trace ID
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — the trace follows the pipeline stages
- [Agent-to-Agent Contract](../coordination/agent-contract.md) — the trace ID is part of the handoff contract
- [Cost Tracking](cost-tracking.md) — per-trace cost aggregation shows the total cost of a multi-agent request
