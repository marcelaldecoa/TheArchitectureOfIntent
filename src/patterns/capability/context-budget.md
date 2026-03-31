# Context Window Budget

---

> *"When context is limited, deciding what the agent forgets is as important as deciding what it knows."*

---

## Context

An agent is about to execute a task. It has a system prompt, skill files, per-task context, retrieved documents, conversation history, and tool descriptions. The context window has a finite size. Not everything fits.

---

## Problem

When context overflows, information is silently truncated — typically from the middle of the window, where the most recent additions displace earlier content. The agent loses information without knowing it lost information. Critical constraints may be truncated while verbose background material remains. The result is an agent that violates constraints it was given but can no longer see.

---

## Forces

- **Completeness vs. capacity.** Every piece of context improves accuracy. But the window is finite, and every addition displaces something else.
- **Constraint safety vs. information richness.** Constraints and invariants must never be truncated. But large constraint sets leave little room for the actual task data.
- **Static allocation vs. dynamic needs.** Different tasks need different amounts of context for skill content, retrieval results, and conversation history. A fixed allocation wastes space on easy tasks and starves complex ones.
- **Explicit management vs. automatic truncation.** Manually managing context is overhead. Automatic truncation is convenient but dangerous — the system decides what to drop, and its priorities may not match yours.

---

## The Solution

Declare a **context priority order** in the spec. When context must be shed, the lowest-priority content is removed first. Constraints are never shed.

**Priority tiers (highest to lowest):**

1. **System prompt + constraints + invariants.** Never truncated. If these don't fit, the context window is too small for this task — fail explicitly.
2. **Task-specific input data.** The actual content the agent needs to work with — the code to review, the document to analyze, the customer record.
3. **Skill file content.** Domain knowledge loaded from skills. If space is limited, load the most relevant skill first.
4. **Retrieved documents.** RAG results, reference material. Shed the lowest-relevance results first.
5. **Conversation history.** Summarize or truncate older turns. Keep the most recent exchanges and any turns that contain authoritative decisions.
6. **Background reference.** Nice-to-have context that improves quality but is not essential. First to be shed.

**Practical rules:**
- Measure context usage before execution. If usage exceeds 80% of the window, shed tier 6. If still over, summarize tier 5. Never shed tiers 1–2.
- When a task consistently exceeds budget, the task is too complex for a single agent execution. Decompose it into subtasks with separate context windows.
- Log what was shed. If post-execution validation reveals that the agent missed something, check whether the relevant context was truncated.

---

## Resulting Context

- **Constraints are never lost.** The priority order guarantees that safety-critical content survives context pressure.
- **Context shedding is deliberate.** Rather than silent truncation, the system knows what was removed and can log it for diagnosis.
- **Complex tasks decompose naturally.** When a task exceeds budget, the constraint forces decomposition into subtasks — a design benefit, not just a limitation.

---

## Therefore

> **Declare a context priority order in the spec. When the context window is full, shed from the bottom tier first. Never shed constraints or invariants. When tasks consistently exceed budget, decompose them rather than truncating critical context.**

---

## Connections

- [The System Prompt](system-prompt.md) — always occupies the highest-priority context tier
- [The Skill File](skill-file.md) — occupies mid-priority; shed by relevance
- [Per-Task Context](per-task-context.md) — high-priority; the actual work data
- [Retrieval-Augmented Generation](rag.md) — retrieval results occupy a middle tier and are shed by relevance
- [Conversation History Management](../state/conversation-history.md) — conversation history is the most common tier to summarize under pressure
