# Conversation History Management

---

> *"Not every turn in the conversation deserves a permanent seat in the context window."*

---

## Context

An agent operates in a multi-turn conversation. Each turn adds to the history. The history accumulates until it exceeds the context window budget, at which point information is silently truncated.

---

## Problem

Unmanaged conversation history grows until it displaces system prompt, skills, or per-task context — the very information the agent needs most. The agent forgets its constraints before it forgets the user's first question. Alternatively, aggressive truncation removes turns that contained authoritative decisions, causing the agent to re-ask resolved questions.

---

## The Solution

Manage history with a **summarize-and-prioritize strategy**.

1. **Keep the most recent N turns in full.** Typically the last 3-5 turns, enough for conversational coherence.
2. **Summarize older turns.** Compress earlier conversation into a structured summary: key decisions made, constraints established, questions resolved.
3. **Preserve authoritative decisions.** Any turn where the user made a consequential decision (approved a plan, set a constraint, resolved an ambiguity) is flagged as authoritative and never summarized away.
4. **Let the context budget govern the history allocation.** History is a lower-priority tier than constraints and task data in the context budget. When budget is tight, history is the first to be summarized.

---

## Therefore

> **Manage conversation history actively: keep recent turns in full, summarize older turns, and flag authoritative decisions for preservation. History is the most expendable tier in the context budget — never sacrifice constraints or task data to keep old conversation turns.**

---

## Connections

- [Context Window Budget](../capability/context-budget.md) — history is allocated from the budget's lower-priority tiers
- [Long-Term Memory](../capability/long-term-memory.md) — important decisions from conversation can be persisted to long-term memory
- [Session Isolation](session-isolation.md) — one conversation's history never appears in another session
