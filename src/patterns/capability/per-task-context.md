# Per-Task Context

---

> *"The system prompt says who you are. The skill says what you know. The context says what you're looking at right now."*

---

## Context

An agent is about to execute a task. It has its system prompt (identity and boundaries) and its skill files (domain knowledge). But this specific task requires information that is unique to this moment — a customer record, an error log, a pull request diff, a set of requirements. This information is relevant only to this task and should not persist into future tasks.

---

## Problem

Without explicit per-task context injection, the agent works from its general knowledge plus whatever the user types into the prompt. Critical information is either missing (the agent hallucinates or asks questions) or buried in a long conversation thread where the agent may lose track of it. The agent cannot distinguish between authoritative context (the actual customer record) and casual context (the user's description of the record from memory).

---

## Forces

- **Specificity vs. context budget.** More context makes the agent more accurate. But context has a finite budget. Including everything relevant may crowd out the system prompt or skill files that provide structural guidance.
- **Authoritative data vs. user narrative.** A customer record retrieved from the database is authoritative. A user saying "the customer joined in 2020" is narrative. The agent needs to know which to trust when they conflict.
- **Freshness vs. availability.** The best context is live data retrieved at execution time. But live retrieval adds latency and may fail. Stale cached data is fast but may be wrong.
- **Injection safety vs. content richness.** Per-task context often includes user-provided data. This data may contain prompt injection attempts. Rich context is valuable; untrusted context is dangerous.

---

## The Solution

Inject per-task context as a **structured, labeled block** that is distinct from the system prompt, skill files, and user conversation. The agent should know explicitly what the context is, where it came from, and how authoritative it is.

**Context injection structure:**
```
## Task Context
**Source:** Order Management System (live query, retrieved 2026-03-30T14:22:00Z)
**Authoritative fields:** order_id, status, total_value, customer_id
**Non-authoritative fields:** customer_notes (user-provided text, may contain errors)

[structured data or document content]
```

**Rules for per-task context:**

1. **Label the source.** The agent should know whether this came from a database, an API, a user upload, or a conversation summary.
2. **Mark authority levels.** System-of-record fields take precedence over user claims. The agent should never override authoritative data with user assertions.
3. **Scope it to the task.** Context injected for Task A should not leak into Task B. Each task execution starts with fresh context injection.
4. **Declare freshness.** Include a timestamp. If the agent is making decisions based on data that could have changed, it should know when the data was retrieved.

---

## Resulting Context

- **Agents work with real data rather than assumptions.** The relevant records, documents, and artifacts are present in context, reducing hallucination and increasing accuracy.
- **Authority is explicit.** When user claims conflict with system data, the agent knows which to trust because authority levels are declared.
- **Task isolation is maintained.** Each task gets its own context. Previous task context doesn't contaminate current task execution.
- **Context injection becomes auditable.** Because context is structured and labeled, post-execution review can verify that the agent had the right information.

---

## Therefore

> **Inject task-specific information as a structured, labeled context block — distinct from the system prompt and skills. Declare the source, authority level, and freshness of each data element so the agent can reason about what to trust.**

---

## Connections

- [The System Prompt](system-prompt.md) — persistent identity; per-task context is ephemeral information layered on top
- [The Skill File](skill-file.md) — stable domain knowledge; per-task context is task-specific data
- [Context Window Budget](context-budget.md) — per-task context competes for space; the budget determines how much fits
- [Retrieval-Augmented Generation](rag.md) — when per-task context is too large to inject directly, RAG retrieves relevant subsets
- [Session Isolation](../state/session-isolation.md) — ensuring per-task context doesn't leak across sessions or users
- [Prompt Injection Defense](../safety/prompt-injection-defense.md) — user-provided context is untrusted input and must be handled as such
