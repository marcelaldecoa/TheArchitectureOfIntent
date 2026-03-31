# Structured Execution Log

---

> *"If you can't see what the agent did, you can't fix what the agent did wrong. If you can't trace who authorized it, you can't govern it."*

---

## Context

An agent executed a task. The output may be correct or incorrect. You need to understand what happened: what tools were called, with what inputs, producing what outputs, in what order, and how long each step took. In regulated environments or with consequential actions, you also need to prove what happened and that it was authorized — which spec, which archetype, which human approved it.

---

## Problem

Without structured logs, debugging agent behavior requires reproducing the failure from scratch — re-running the same spec and hoping the same behavior recurs. Conversation logs capture the human-agent interaction but not the tool calls, retrieval queries, or internal reasoning that produced the output.

Without governance linkage, the log answers "what happened" but not "under whose authority." An auditor, incident responder, or compliance officer needs both. A log entry that says "refund.initiate called with amount $47.50" is operationally useful. A log entry that also says "authorized by spec CS-2024-031 v1.2, approved by J. Chen, governed by Executor archetype" is compliance-ready.

---

## Forces

- **Completeness vs. volume.** Logging everything produces massive volume. But logging too little leaves gaps that make post-incident diagnosis impossible. The tradeoff is logging categorized events with summaries, not raw payloads.
- **Structured data vs. free text.** Free-text logs are easy to write but impossible to query at scale. Structured logs (JSON) are queryable but require schema discipline.
- **Operational visibility vs. privacy.** Logs should capture what the agent did. But inputs and outputs may contain sensitive data. Redaction must happen at write time, not after the fact.
- **Technical record vs. governance record.** Development teams want operational logs. Compliance teams want authorization chains. The same log infrastructure should serve both audiences through layered fields.

---

## The Solution

Log every agent action as a **structured event** with standardized fields, organized in two layers: an operational layer for debugging and a governance layer for compliance. The key design principle is that a single log infrastructure serves both the development team (who needs to debug failures) and the governance function (who needs to demonstrate accountability).

### Two Layers, One Event

Each log entry carries two layers of information:

**The operational layer** answers *what happened*: timestamp, trace and span identifiers for correlation, which spec authorized the execution, what action was taken (tool call, retrieval, output generation, escalation, validation), what was sent and received (redacted and summarized), how long it took, and whether it succeeded.

**The governance layer** answers *under whose authority*: which spec version authorized the action, which archetype governs the agent, who approved the spec, which manifest entry authorized the tool call, what effect class the action belongs to (read, write, delete, transmit), and any human decisions made at gates.

The operational layer is required for all log entries. The governance layer is required for consequential actions — state changes, escalations, and human decisions.

### Implementation Principles

1. **Structured, not free-text.** Every log entry is JSON with a consistent schema. Unstructured logs are easy to write but impossible to query at scale.
2. **Append-only and immutable.** Log entries are written once and never modified. Tampering with logs is a governance violation.
3. **Redaction at write time.** Sensitive fields (PII, credentials, financial data) are redacted before the entry is written. The raw data is never in the log.
4. **Retention is declared.** The spec or organizational policy declares how long logs are retained. Compliance requirements may mandate minimum retention periods.
5. **Queryable by trace_id and spec_id.** At minimum, the logging system supports querying all entries for a given pipeline execution (trace_id) and all entries authorized by a given spec (spec_id). These two query paths serve operational debugging and governance auditing respectively.

### The spec_id as Governance Link

The critical design decision in the structured execution log is the `spec_id` field — the link between the technical record of what happened and the governance chain of who authorized it. Without `spec_id`, the log answers "what did the agent do?" but not "was it authorized to do it?" With `spec_id`, every log entry is traceable to a spec, which is traceable to an archetype, which is traceable to an approval authority. This chain is what makes agent systems auditable.

---

## Resulting Context

- **Debugging moves from reproduction to analysis.** When an agent fails, the log shows exactly what happened — no need to re-run the task and hope the failure recurs.
- **Governance is built into the operational log.** Compliance teams and incident responders use the same log infrastructure, querying different fields.
- **Anomaly detection has a data source.** Aggregated log data feeds baseline computation: average durations, tool call frequencies, error rates.
- **Cost tracking is derivable.** Token counts, tool call counts, and durations in the log enable cost-per-execution and cost-per-correct-output calculations.
- **Cross-agent traces are possible.** The trace_id links entries from multiple agents in a pipeline, enabling end-to-end journey analysis.

---

## Therefore

> **Log every agent action as a structured event with standardized operational fields (what happened, when, how long) and governance fields (who authorized it, under what spec, with what archetype). Logs are structured JSON, append-only, immutable, and redacted at write time. The spec_id is the critical link between the technical record and the governance chain.**

---

## Connections

- [Distributed Trace](distributed-trace.md) — traces correlate log entries across multiple agents using the shared trace_id
- [Anomaly Detection Baseline](anomaly-baseline.md) — baselines are computed from aggregated execution log data
- [Cost Tracking](cost-tracking.md) — cost is derived from token counts, durations, and tool calls in the log
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — log entries respect data classification through redaction
- [Delegated Definition Authority](../../operating/03-who-defines-archetypes.md) — the governance layer records who authorized the archetype
- [Human-in-the-Loop Gate](../coordination/human-gate.md) — human decisions at gates become log entries with the governance layer
- [Agent Registry](../state/agent-registry.md) — the registry connects deployed agents to their governance metadata visible in the log
