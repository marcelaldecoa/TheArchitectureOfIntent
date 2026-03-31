# Long-Term Memory

---

> *"A session ends. The knowledge shouldn't."*

---

## Context

An agent interacts with users or systems over time — across sessions, days, or months. It learns things during one session that would be valuable in the next: user preferences, prior decisions, accumulated project context, resolved ambiguities. But each new session starts from zero.

---

## Problem

Without persistent memory, every interaction is a first encounter. The agent re-asks questions it has already resolved. It re-discovers preferences the user has already stated. It cannot build on prior work — each session is a standalone event rather than a continuation. Users compensate by re-providing context manually, which is tedious and error-prone.

---

## Forces

- **Continuity vs. staleness.** Remembered information improves user experience. But remembered information decays — preferences change, contexts shift, prior decisions become irrelevant. Memory without expiration creates noise.
- **Personalization vs. privacy.** Storing user-specific information enables better service. It also creates privacy obligations — what is stored, for how long, who can access it, how it is deleted.
- **Explicit vs. implicit memory.** Some things should be explicitly saved (user preferences, project notes). Others are implicitly inferred (this user prefers brief answers). Implicit memory is powerful but opaque and hard to audit.
- **Agent memory vs. system of record.** When the agent remembers something that conflicts with the database, which is authoritative? Agent memory must never override system-of-record data.

---

## The Solution

Implement long-term memory as a **declared, scoped, auditable store** — not as an opaque model feature.

**Memory architecture:**

1. **Explicit storage, not implicit inference.** The agent writes to memory through a declared memory tool, not by internally accumulating hidden state. Each memory entry has a timestamp, source, and category.
2. **Scoped by entity.** User-scoped memories are tied to a user ID. Project-scoped memories are tied to a project ID. Organization-scoped memories are shared. Scopes prevent cross-contamination.
3. **Human-readable and editable.** Users can view what the agent remembers about them and delete entries. This is not optional — it is a trust and compliance requirement.
4. **Authority is subordinate to systems of record.** If the agent remembers "this customer's subscription is Gold" but the database says "Silver," the database wins. Memory augments authoritative data; it does not override it.
5. **Expiration and relevance decay.** Memories have a declared TTL or are reviewed periodically. A preference stated 18 months ago may no longer apply. Stale memories are worse than no memories.
6. **Spec-governed write conditions.** The spec declares what the agent is authorized to remember. "You may remember stated user preferences and project conventions. You may not store personal health information, financial details, or authentication credentials."

---

## Resulting Context

- **Interactions improve over time.** The agent builds on prior context rather than starting from zero each session.
- **Memory is auditable.** Because storage is explicit and scoped, administrators can review what agents remember and compliance teams can verify data handling.
- **Users retain control.** The ability to view and delete memories preserves trust and satisfies privacy requirements.
- **Systems of record remain authoritative.** Memory supplements — it never overrides — the organization's canonical data sources.

---

## Therefore

> **Implement agent memory as a declared, scoped store with explicit write conditions, human-readable entries, and a clear subordination to systems of record. Users must be able to view and delete what the agent remembers. Memory entries decay over time and are governed by the same spec that governs the agent's other behaviors.**

---

## Connections

- [Session Isolation](../state/session-isolation.md) — within a session, state is ephemeral; long-term memory persists across sessions
- [Per-Task Context](per-task-context.md) — per-task context is injected fresh each time; memory is retrieved from the persistent store
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — memory storage must respect data classification constraints
- [The State-Changing Tool](../integration/state-changing-tool.md) — writing to memory is a state-changing operation and should be authorized as such
- [Audit Trail](../observability/audit-trail.md) — memory writes are auditable events
