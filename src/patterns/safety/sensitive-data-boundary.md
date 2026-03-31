# Sensitive Data Boundary

---

> *"Classify the data. Then design the boundary around the classification, not the convenience."*

---

## Context

An agent handles data that includes PII, financial records, credentials, health information, or other sensitive categories. The agent needs some of this data to do its job. But the data must not leak into logs, be stored in unauthorized locations, or cross system boundaries without authorization.

---

## Problem

Without declared data boundaries, agents treat all data uniformly. A customer's name appears in the execution log. A credit card number is passed to a tool that doesn't need it. A password is included in a conversation summary that persists to long-term memory. The agent doesn't intentionally leak data — it simply doesn't know which data is sensitive.

---

## The Solution

Declare **data classification in the spec** and enforce handling rules per classification level.

1. **Classify data in the spec.** Each data element the agent handles is tagged: public, internal, confidential, restricted.
2. **Handling rules per classification:**
   - **Public** — no restrictions on logging, storage, or transmission.
   - **Internal** — may be logged in summary form. May not be transmitted outside the system boundary.
   - **Confidential (PII, financial)** — never logged in full. Transmitted only to authorized tools. Redacted in conversation summaries and long-term memory.
   - **Restricted (credentials, health)** — never logged. Never stored in agent memory. Accessed only through authorized tools with minimal exposure.
3. **Tool-level enforcement.** Tools that handle sensitive data enforce classification: they accept classified fields, process them, and return results without exposing raw values.
4. **Memory exclusion.** Long-term memory storage respects classification. The agent may remember "the customer has a refund history" but not the specific credit card number used.

---

## Therefore

> **Declare data classification in the spec. Enforce per-classification handling rules: what can be logged, stored, transmitted, and remembered. Never log restricted data. Never store credentials in agent memory. The data boundary is a spec constraint, not a tooling decision.**

---

## Connections

- [Long-Term Memory](../capability/long-term-memory.md) — memory writes respect classification boundaries
- [Structured Execution Log](../observability/execution-log.md) — log entries redact classified fields
- [Session Isolation](../state/session-isolation.md) — cross-session leakage would violate data classification
- [Audit Trail](../observability/audit-trail.md) — audit entries reference classified data without exposing it
- [File System Access](../integration/file-system-access.md) — credential files are excluded from file access by default
