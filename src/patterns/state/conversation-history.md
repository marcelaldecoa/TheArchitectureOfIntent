# Conversation History Management

---

> *"Not every turn in the conversation deserves a permanent seat in the context window."*

---

## Context

An agent operates in a multi-turn conversation. Each turn adds to the history. The history accumulates until it exceeds the context window budget, at which point information is silently truncated.

---

## Problem

Unmanaged conversation history grows until it displaces system prompt, skills, or per-task context — the very information the agent needs most. The agent forgets its constraints before it forgets the user's first question. Alternatively, aggressive truncation removes turns that contained authoritative decisions, causing the agent to re-ask resolved questions.

**Concrete scenario:** A code generation agent on a 25-turn architectural refactoring task. At turn 5, the user specifies: "All database calls must use prepared statements. This is non-negotiable." At turn 18, when the agent generates the DAL layer, the system prompt about security constraints has been truncated from the context window, and the agent bypasses prepared statements. The user must re-establish the constraint at turn 19.

---

## Forces

- **Need conversational coherence** (recent context) vs. **limited context window** (only so much space available)
- **Need to preserve authoritative decisions** (they don't change) vs. **uncertainty about which turns are authoritative** (requires manual review or flag-on-write)
- **Need to summarize older turns for space** vs. **loss of detail when summarizing** (summaries omit nuance)
- **Need fast history recall** (don't recompute summaries on every turn) vs. **staleness of pre-computed summaries** (context may have shifted)

---

## The Solution

Manage history with a **summarize-and-prioritize strategy**.

1. **Keep the most recent N turns in full.** Typically the last 3-5 turns, enough for conversational coherence.
2. **Summarize older turns.** Compress earlier conversation into a structured summary: key decisions made, constraints established, questions resolved.
3. **Preserve authoritative decisions.** Any turn where the user made a consequential decision (approved a plan, set a constraint, resolved an ambiguity) is flagged as authoritative and never summarized away.
4. **Let the context budget govern the history allocation.** History is a lower-priority tier than constraints and task data in the context budget. When budget is tight, history is the first to be summarized.

**Example:** A data analysis agent working on a quarterly reporting pipeline. Turn 1 establishes three constraints: "Use only approved data sources, round percentages to 1 decimal, include 2020-2024 data only." These are tagged as *authoritative*. Turns 2-14 are exploratory (data source evaluation, drafts). At turn 15, the agent is asked to produce the final report. The context window includes: system prompt + authoritative constraints (turn 1, in full) + turns 13-15 in full + a summary of turns 2-12 (what was explored, what was ruled out). The agent produces the final report without re-asking about constraints.

---

## Resulting Context

- **Authoritative decisions persist** across long conversations without being re-asked
- **Recent conversational context remains vivid**, enabling the agent to reference recent turns directly
- **Context budget is stable**, allocated predictably between constraints, task data, and conversation
- **Older exploratory turns are summarized but not lost**, recoverable if edge cases arise

---

## Therefore

> **Manage conversation history actively: keep recent turns in full, summarize older turns, and flag authoritative decisions for preservation. History is the most expendable tier in the context budget — never sacrifice constraints or task data to keep old conversation turns.**

---

## Connections

- [Context Window Budget](../capability/context-budget.md) — history is allocated from the budget's lower-priority tiers
- [Long-Term Memory](../capability/long-term-memory.md) — important decisions from conversation can be persisted to long-term memory
- [Session Isolation](session-isolation.md) — one conversation's history never appears in another session