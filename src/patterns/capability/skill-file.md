# The Skill File

---

> *"A skill is not a prompt. It is the codified judgment of someone who has done this work before — packaged so that every agent benefits from it."*

---

## Context

You have agents working in a specific domain — a codebase, a business process, a documentation corpus. The agents need domain-specific knowledge: coding conventions, naming standards, workflow rules, domain terminology, quality criteria. This knowledge applies to many tasks, not just one. It doesn't change from task to task; it changes when the domain evolves.

---

## Problem

Without shared domain knowledge, every spec must re-teach the agent what the organization already knows. Each spec author includes their own version of the conventions, with their own completeness and their own biases. Agent output quality varies not because the agents differ, but because the knowledge they receive differs. When conventions change, every spec that embedded the old convention must be found and updated individually.

---

## Forces

- **Centralized knowledge vs. distributed authorship.** Domain knowledge should be maintained in one place. But different people own different parts of the domain. A single monolithic knowledge file becomes a bottleneck.
- **Stability vs. evolution.** Skills should be stable enough to rely on. But domains evolve — new patterns are adopted, old patterns are deprecated. A skill that can't be updated is a liability.
- **Portability vs. platform specificity.** Organizations use multiple agent platforms. Skills should work across all of them. But platform-specific features may tempt platform-specific skill formats.
- **Machine readability vs. human authorship.** Skills are consumed by agents, but they are written and maintained by humans. The format must serve both audiences.

---

## The Solution

Create a **SKILL.md file** — a markdown document with YAML frontmatter that packages domain-specific procedural knowledge for agent use. The file contains knowledge that is true for the domain, not for a specific task.

**What belongs in a skill file:**
- Coding conventions and naming standards for a project
- Domain model definitions and entity relationships
- Workflow rules and process constraints
- Quality criteria specific to the domain
- Known pitfalls and how to avoid them

**What does not belong in a skill file:**
- Task-specific instructions (those belong in the spec)
- Agent identity and safety constraints (those belong in the system prompt)
- Ephemeral context like a specific customer's data (per-task context)

**Skill file structure:**
```yaml
---
title: "TypeScript API Standards"
description: "Coding standards for agent-generated TypeScript code in this project"
applyWhen: "The agent is generating or modifying TypeScript code"
---

[Domain knowledge in natural language, organized by topic]
```

**Three scopes of skills:**

1. **Project-level** — lives in the repository. Applies to all work in this codebase. Example: `.github/skills/typescript-standards.md`
2. **Personal** — lives in the user's home directory. Applies to individual preferences. Example: `~/.copilot/skills/code-review-style.md`
3. **Organizational** — applies across all projects in the organization. Example: security compliance standards, data handling policies.

The `applyWhen` field is critical — it tells the agent **when** to load this skill, preventing context pollution from irrelevant knowledge.

---

## Resulting Context

- **Agent output converges on organizational standards.** When every agent loads the same skill file, output quality becomes consistent regardless of which spec author wrote the task.
- **Domain knowledge survives personnel changes.** When an expert leaves, their codified knowledge remains in the skill file for every future agent and practitioner to use.
- **Skill files become the source of truth for standards.** Instead of standards documents that agents may or may not follow, skill files are directly consumed by agents — closing the gap between documented convention and actual practice.
- **Cross-platform consistency becomes achievable.** A skill file written once works across any agent platform that supports the standard.

---

## Therefore

> **Package reusable domain knowledge into SKILL.md files with clear loading conditions. Skills encode what the organization knows — coding standards, domain rules, quality criteria — so that every agent and every task benefits from accumulated expertise without every spec re-teaching it.**

---

## Connections

- [The System Prompt](system-prompt.md) — the system prompt establishes deployment identity; skills provide domain knowledge within that identity
- [Per-Task Context](per-task-context.md) — skills provide stable domain knowledge; per-task context provides task-specific information
- [Standards as Agent Skill Source](../../repertoires/04-code-standards.md) — code standards documents are natural skill file source material
- [Context Window Budget](context-budget.md) — skills compete for context space; the budget pattern determines priority
- [Portable Domain Knowledge](../../agents/05-agent-skills.md) — the full treatment of skills in agent architecture
