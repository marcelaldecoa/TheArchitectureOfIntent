# The System Prompt

---

> *"The system prompt is the agent's constitution — not the law for one case, but the frame for all cases."*

---

## Context

You are deploying an agent that will handle many tasks over time — answering questions, processing requests, producing work products. You need to establish behavioral constraints, identity, and boundaries that apply to every interaction, regardless of what the specific task is.

---

## Problem

Without persistent behavioral instructions, the agent defaults to the behaviors encoded in its training data. It will be helpful, general-purpose, and unconstrained. It will answer questions it shouldn't, attempt tasks outside its scope, adopt whatever tone the user sets, and treat every request as equally authorized. Each conversation starts from an unmarked state.

---

## Forces

- **Persistence vs. per-task flexibility.** Some instructions should never change (identity, safety constraints). Others should vary by task. Mixing both in one place creates confusion about what is permanent and what is negotiable.
- **Comprehensiveness vs. context budget.** A thorough system prompt consumes context window space that could be used for task-specific information. Overly long system prompts crowd out the actual work.
- **Constraint strength vs. override vulnerability.** Instructions in system prompts can be overridden by sufficiently creative user input. Critical constraints should be enforced architecturally, not only through prompt text.
- **Clarity for the agent vs. transparency for the user.** The system prompt is typically hidden from users. Instructions that affect user-facing behavior should be documentable and reviewable, not buried in opaque configuration.

---

## The Solution

Use the system prompt for **deployment-level identity and boundaries** — the instructions that define what this agent is, what it may and may not do, and how it presents itself. These are the instructions that should apply to every task the agent handles.

A well-structured system prompt contains:

1. **Identity declaration.** What the agent is, who it serves, what role it fills. Not a persona — an operational identity. "You are a customer support agent for RetailCo, handling Tier 1 inquiries."
2. **Boundary constraints.** What the agent must never do, regardless of request. "Do not access accounts belonging to other customers. Do not override refund limits. Do not provide legal, medical, or financial advice."
3. **Behavioral defaults.** How the agent responds when the task-specific spec doesn't address a situation. "When uncertain, ask for clarification rather than guessing. When a request is outside scope, say so and offer to escalate."
4. **Output format requirements.** Structural expectations that apply across all tasks. "Always respond in the user's language. Always cite sources when presenting factual claims."

The system prompt does **not** contain:
- Task-specific instructions (those belong in the spec or per-task context)
- Domain knowledge that changes over time (that belongs in skill files)
- Tool invocation details (those belong in the tool manifest)

---

## Resulting Context

- **Every interaction starts from a known baseline.** The agent's identity and boundaries are established before any task-specific context arrives.
- **Task-specific specs can be lighter.** Because the system prompt handles shared constraints, individual specs only need to specify what's unique to this task.
- **Behavioral drift is constrained.** Users who attempt to push the agent outside its role encounter boundaries that persist across conversation turns.
- **Reviewability improves.** The system prompt is a single document that can be reviewed, versioned, and audited independently of task-specific specs.

---

## Therefore

> **Use the system prompt to establish the agent's persistent identity, boundaries, and behavioral defaults — the constitutional layer that applies to every interaction. Keep it focused on what never changes. Move everything that varies by task into specs, skills, or per-task context.**

---

## Connections

- [The Skill File](skill-file.md) — reusable domain knowledge that applies across tasks within a domain, complementing the system prompt's deployment-level scope
- [Per-Task Context](per-task-context.md) — information specific to one task, layered on top of the system prompt
- [Prompt Injection Defense](../safety/prompt-injection-defense.md) — system prompt boundaries are the first line of defense against prompt injection
- [The Tool Manifest](tool-manifest.md) — tool authorization declarations complement the system prompt's behavioral boundaries
- [Constitutional Archetypes](../../architecture/01-archetypes-as-constitutional-law.md) — the system prompt operationalizes the archetype's constraints for a specific deployment
