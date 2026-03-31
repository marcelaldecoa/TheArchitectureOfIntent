# Session Isolation

---

> *"User A's conversation is invisible to User B. Always."*

---

## Context

Multiple users or conversations share an agent deployment. Each user provides personal data, makes requests, and expects responses based on their own context. The agent handles all of them.

---

## Problem

Without isolation, state from one session leaks into another. User A's data appears in User B's response. Decisions made for one customer affect another. The agent's context accumulates across sessions, producing responses that reference conversations the current user never had.

---

## The Solution

Each session operates under its own **isolated context instance**. No cross-session state sharing.

1. **Session-scoped context.** Each session has its own system prompt instance, per-task context, and conversation history. Nothing from Session A is visible in Session B.
2. **Session-scoped tool results.** Tool calls in one session do not affect the context of another session. A customer record retrieved for User A is not cached for User B.
3. **Session-scoped memory.** If long-term memory is enabled, memories are scoped to the user, not shared across users.
4. **Session termination clears ephemeral state.** When a session ends, its conversation history and per-task context are discarded (long-term memory persists per its own retention rules).
5. **Isolation is a constraint, not a feature.** The spec declares session isolation as an invariant. It is not traded for performance or convenience.

---

## Therefore

> **Each session operates in an isolated context instance. No cross-session state, no shared conversation history, no leaked tool results. Session isolation is an invariant, not a preference.**

---

## Connections

- [Per-Task Context](../capability/per-task-context.md) — context is injected per session, not shared
- [Long-Term Memory](../capability/long-term-memory.md) — memory is scoped to the user, not the session
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — session isolation prevents cross-user data exposure
- [Shared Context Store](shared-context.md) — the explicit alternative when agents DO need to share state (within a pipeline, not across users)
