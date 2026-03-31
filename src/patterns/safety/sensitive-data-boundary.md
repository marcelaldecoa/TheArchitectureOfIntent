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

## Forces

- **Data necessity vs. protection trade-off**: The agent needs access to sensitive data to perform its job. Locking it down too tightly cripples the agent; allowing free access creates leakage risk.
- **Classification overhead**: Every data element must be tagged and every tool must enforce classification rules. This adds operational burden and complexity.
- **Tool integration friction**: Third-party tools don't know about the agent's data classification scheme. Sanitizing output from external tools is manual and error-prone.
- **Memory paradox**: Long-term memory is valuable for agent continuity, but storing sensitive data violates classification. Rules must define what can be remembered without exposing raw values.

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

**Example:** A financial advisory agent handles customer data:
- **Public**: Customer name, account type, investment goals → logged fully, stored in memory
- **Internal**: Account balance, transaction history → logged in summary ("customer viewed high-volatility portfolio"), never transmitted outside system
- **Confidential**: Social Security number, home address → never logged; accessed only via tools that return redacted results (tool returns "verified" not the SSN itself)
- **Restricted**: Login credentials, 2FA secrets → never logged, never stored in memory; accessed only via credential vault service that returns "authenticated" without exposing the secret

The agent's memory stores: "Customer optimizing for tax efficiency with restricted budget," but not: "Customer SSN 123-45-6789, credit card 4111-1111-1111-1111."

---

## Resulting Context

- **Data exposure is bounded by classification rules.** Logs and memory comply with declared constraints; sensitive data cannot appear in unintended places.
- **Compliance is auditable.** The spec declares handling rules; logs and memory accesses can be audited for compliance.
- **Tool integration is explicit.** Tools that handle sensitive data are declared in the spec; tools that don't need it are never exposed to it.
- **Secret rotation is simplified.** Credentials are never stored in agent memory, so password changes don't require memory scrubbing.

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