# Session Isolation

---

> *"User A's conversation is invisible to User B. Always."*

---

## Context

Multiple users or conversations share an agent deployment. Each user provides personal data, makes requests, and expects responses based on their own context. The agent handles all of them.

---

## Problem

Without isolation, state from one session leaks into another. User A's data appears in User B's response. Decisions made for one customer affect another. The agent's context accumulates across sessions, producing responses that reference conversations the current user never had.

**Concrete scenario:** A customer support agent deployed for a SaaS company. User A (Acme Corp) reports a billing issue on March 15. The agent reviews Acme's account, notes a specific pricing anomaly, records it in context memory. User B (Beta Industries) logs in on March 16. The agent, reusing context, begins: "As we discussed with Acme Corp, you have the same pricing issue..." Beta Industries has never had that conversation. Their billing works fine. The agent is confusing two accounts, both using the agent, but separate sessions.

---

## Forces

- **Need shared agent infrastructure** (cost-effective) vs. **total isolation per session** (per-session resource overhead)
- **Need long-term memory across sessions** (remember customer preferences) vs. **need current-session privacy** (can't leak between sessions)
- **Need cache efficiency** (reuse computed results) vs. **session isolation** (each session computes independently)
- **Need to prevent data leakage** vs. **debugging difficulty** (tracing an error requires looking across isolated sessions)

---

## The Solution

Each session operates under its own **isolated context instance**. No cross-session state sharing.

1. **Session-scoped context.** Each session has its own system prompt instance, per-task context, and conversation history. Nothing from Session A is visible in Session B.
2. **Session-scoped tool results.** Tool calls in one session do not affect the context of another session. A customer record retrieved for User A is not cached for User B.
3. **Session-scoped memory.** If long-term memory is enabled, memories are scoped to the user, not shared across users.
4. **Session termination clears ephemeral state.** When a session ends, its conversation history and per-task context are discarded (long-term memory persists per its own retention rules).
5. **Isolation is a constraint, not a feature.** The spec declares session isolation as an invariant. It is not traded for performance or convenience.

**Example:** The support agent above. The spec declares:
```
session:
  isolation: "strict"
  context_scope: "per_session"
  memory:
    embedding_cache: "session_scoped"
    long_term: "user_scoped_only"
  cleanup_on_termination:
    - "conversation_history"
    - "per_task_context"
    - "tool_result_cache"
```
When User A (account_id: acme-123) starts a session, a new context instance is created with tag `session:acme-123-mar15-14:22`. The agent retrieves Acme's account data, notes the pricing anomaly, stores it in `session:acme-123-mar15-14:22/pricing_issue`. When the session ends, the instance is discarded. User B (account_id: beta-456) starts a fresh session with tag `session:beta-456-mar16-09:10`. The pricing anomaly is invisible. User B's context contains only their data, their history, their decisions.

---

## Resulting Context

- **User data is completely isolated** — no cross-user leakage, no shared conversation history
- **Long-term memory remains user-scoped** — preferences and patterns are remembered, but not confused across users
- **Debugging is clear** — failures are traced within a single session, not across contaminated sessions
- **Compliance is simpler** — session isolation is a default guarantee, not something that needs to be verified per-feature

---

## Therefore

> **Each session operates in an isolated context instance. No cross-session state, no shared conversation history, no leaked tool results. Session isolation is an invariant, not a preference.**

---

## Connections

- [Per-Task Context](../capability/per-task-context.md) — context is injected per session, not shared
- [Long-Term Memory](../capability/long-term-memory.md) — memory is scoped to the user, not the session
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — session isolation prevents cross-user data exposure
- [Shared Context Store](shared-context.md) — the explicit alternative when agents DO need to share state (within a pipeline, not across users)