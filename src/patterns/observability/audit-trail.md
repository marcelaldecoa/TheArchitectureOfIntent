# Audit Trail for Compliance

---

> *"The question is not 'what did the agent do?' The question is 'under whose authority did it do it?'"*

---

## Context

An agent system operates in a regulated environment, or handles sensitive data, or takes consequential actions. After the fact, someone — an auditor, an incident responder, a compliance officer — needs to prove what happened and that it was authorized.

---

## Problem

Execution logs capture what happened technically. But they don't answer the governance question: which spec authorized this action? Who approved that spec? What archetype governs this agent? When was the last governance review? Without linking actions to authority, the log is a technical record but not a compliance record.

---

## The Solution

Extend the execution log into an **audit trail** that links every consequential action to its authorization chain.

**Audit trail fields (added to execution log entries):**
- `spec_id` + `spec_version` — which spec authorized this action
- `archetype` — which archetype governs the agent
- `spec_approver` — who approved the spec (name, role, date)
- `tool_authorization` — which manifest entry authorized this tool call
- `human_decision` (if applicable) — the human's decision at a gate, with identity

**The `spec_id` is the critical link.** It connects the technical what-happened to the governance who-authorized-it. From the spec_id, an auditor can trace to the spec, the archetype, the approval chain, and the governance review history.

---

## Therefore

> **Link every consequential agent action to the spec that authorized it, the archetype that governs it, and the human who approved the spec. The audit trail makes governance visible to compliance, incident response, and organizational accountability.**

---

## Connections

- [Structured Execution Log](execution-log.md) — the audit trail extends the execution log with governance fields
- [Delegated Definition Authority](../../operating/03-who-defines-archetypes.md) — the audit trail records who authorized the archetype
- [Human-in-the-Loop Gate](../coordination/human-gate.md) — human decisions at gates become audit trail entries
- [Agent Registry](../state/agent-registry.md) — the registry connects deployed agents to their governance metadata
