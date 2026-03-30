# Pattern 5.5 — Agent Skills: Packaging Domain Knowledge

**Part V: Agents & Execution** · *5 of 7*

---

> *"An expert does not need to be instructed from first principles every time. They arrive knowing how we work here. Skills are how that knowledge travels."*

---

## Context

We have tools: callable capabilities that let agents act in the world. We have specs: structured intent documents that tell agents what to do for a given task. There is a third layer that has been conspicuously absent from this picture.

Every serious organization that deploys agents eventually discovers the same gap: there is knowledge that belongs in neither tools nor specs. It is domain knowledge — how we approach this class of problem, what our style requires, what our approval process looks like, how we handle exceptions in this domain, what our naming conventions are. It is organizational knowledge — what we have learned from running this workflow before, what assumptions we carry, what invariants must not be violated. It lives in senior engineers' heads, in onboarding documents, in the accumulated judgment of people who have been doing this work for years.

When that knowledge is absent from an agent system, the agent reproduces it from its training distribution — which is general, not your-organization-specific. When it is present only in specs, it must be re-included in every spec, which creates maintenance burden, silent drift, and repetition cost. This chapter introduces the mechanism that solves this problem: **Agent Skills**.

---

## The Problem

Consider a team that uses an agent for code review. They have discovered that good reviews in their codebase require: knowing the naming conventions for their domain objects, understanding that all database migrations must be reversible, following the pattern guide that documents approved ways to handle async errors, and applying the security checklist for any code that handles authentication flows. These are not tool capabilities — the agent already has the ability to *read* and *analyze* code. They are *knowledge about how to analyze code in this specific context*.

The team has three options, and each produces a different failure mode:

**Option 1: Embed knowledge in every code review spec.** Maintainable until it isn't. When the security checklist changes, every code review spec is out of date. When someone writes a spec and forgets the naming convention section, the output is wrong in a way that is hard to trace to the omission.

**Option 2: Assume the agent "knows" from general training.** The agent has seen millions of code review examples. But it has not seen your codebase's specific conventions. It will apply general best practice, not your practice. The gap is often invisible until it matters.

**Option 3: Pack all context into the system prompt.** Teams that discover options 1 and 2 are insufficient often stuff everything into an enormous system prompt. This produces agents that are expensive to run, slow to respond, constrained in the context they have available for the actual task, and dependent on context-length limits. The knowledge is also unversioned, ungoverned, and shared across all tasks regardless of relevance.

None of these options separates the concerns appropriately. What is needed is a way to package domain knowledge as a first-class artifact that agents can load when relevant, that teams can version and govern, and that travels across platforms without being reimplemented everywhere.

---

## Forces

- **Per-spec knowledge vs. reusable domain knowledge.** Specs encode per-task requirements. Skills encode domain knowledge that applies across many tasks. Without skills, every spec must re-specify shared knowledge.
- **Agent training distribution vs. organizational context.** Agents carry general knowledge from training. Organizations have specific conventions, standards, and practices that differ from general knowledge.
- **Knowledge portability vs. platform lock-in.** Skills should work across multiple agent platforms. Yet platform-specific features may tempt platform-specific skill formats.
- **Organizational consistency vs. individual preference.** Organizational skills enforce consistency. Personal skills encode individual workflows. The two scopes must coexist without conflict.

---

## The Solution

### What Agent Skills Are

An Agent Skill is a package of domain-specific procedural knowledge that an agent loads before or during execution to enhance its capability in a particular domain. A skill is not a tool (it doesn't give the agent a new capability to call) and not a spec (it doesn't define what to do for this specific task). A skill is *how to approach a class of work* — procedural and contextual knowledge that improves the quality of execution across any task in that domain.

Skills are defined in files named `SKILL.md`. A skill has:

**A YAML frontmatter header** that provides identity and discoverability:
```yaml
---
name: database-migrations
description: "Guidelines for writing safe, reversible database migrations in this codebase. Load when working on any task that creates or modifies database schema or migration files."
---
```

**The skill body**: Markdown instructions that the agent follows when the skill is active. This is the knowledge itself — procedures, conventions, constraints, examples. It is written to be read and applied by an agent, not by a human reader.

A complete skill might look like:

```markdown
---
name: database-migrations
description: "Guidelines for writing safe, reversible database migrations. Load when creating or modifying schema migration files."
---

# Database Migration Guidelines

## Invariants
- ALL migrations must be reversible. Every `up()` migration must have a matching `down()`.
- Never drop a column without a two-phase migration: deprecate in one release, remove in the next.
- Migration files are named: `YYYYMMDDHHMMSS_description_in_snake_case.sql`

## Performance Safety
- No migration may lock a table that receives more than 100 requests/second without an async migration plan.
- Index creation must use CONCURRENTLY for tables > 10k rows.

## Validation
- Every migration must be tested against a copy of the production database schema before merge.
- Migration PRs require sign-off from a database administrator.

## What to Watch For
- Adding NOT NULL columns to existing tables without a default value will fail on populated tables.
- Foreign key constraints add index lookups — document the performance impact for tables > 1M rows.
```

This skill contains no tools and no task-specific instructions. It contains the accumulated knowledge that makes a good database migration in this codebase. Loaded by an agent working on a migration task, it changes the quality of every decision the agent makes.

### The Open Standard

Agent Skills are an open standard, originated by Anthropic and formalized at [agentskills.io](https://agentskills.io). The standard is deliberately minimal — a `SKILL.md` file with YAML frontmatter is all that is required. This simplicity is intentional: the standard spreads because any team can adopt it without tooling investment.

As of early 2026, the standard is supported by a growing ecosystem. Specific platform support evolves rapidly; verify current capabilities against each platform's documentation:

| Platform | Skills Location | Status |
|---------|----------------|--------|
| GitHub Copilot | `.github/skills/` | Supported |
| Claude / Claude Code | `.claude/skills/` | Supported |
| VS Code Copilot | `.vscode/skills/` | Supported |
| Gemini CLI | `.gemini/skills/` | Supported |
| Spring AI | `.agents/skills/` | Community adoption |
| Snowflake Cortex | `.cortex/skills/` | Community adoption |
| Generic (project-level) | `.agents/skills/` | Convention |

Cross-platform portability is a first-order property of the standard. A skill written once can be used by any agent framework that supports the standard. Organizations that operate multiple agent tools — which is almost everyone operating at any scale — get the same knowledge applied consistently, without reimplementing for each platform.

### Three Scopes of Skills

**Project-level skills** live in the repository alongside the code or documents the agent operates on. They encode knowledge specific to this codebase, document corpus, or workflow. Everyone working on this project — human or agent — operates in the context of these skills. Examples: code style guide, domain model conventions, API design patterns for this service.

**Personal skills** live in the user's home directory (e.g., `~/.copilot/skills`). They encode individual preferences, personal workflows, and habits the individual wants applied consistently. Examples: preferred code organization style, personal documentation templates, languages the individual works in most.

**Organizational skills** are emerging — the next layer above project, for skills that should apply across all repositories and projects in an organization. Examples: security compliance checklist, corporate communication style, data handling policies. Platform tooling for organizational skills is actively developing; teams that need org-level consistency today often implement it via shared repository templates or CI-enforced skill injection.

### Skills vs. Tools vs. Specs

The three layers serve different purposes:

| Layer | Answers | Scope | Persistence |
|-------|---------|-------|-------------|
| Tools (MCP) | *What can I do?* | Task execution | Platform/server |
| Skills | *How should I approach this class of work?* | Domain expertise | Repository/user |
| Spec (SDD) | *What exactly should I do right now?* | This task | Task instance |

A skill is not invoked — it is loaded. When an agent loads a skill, it incorporates the skill's instructions into its working context for the duration of the task. The skill informs every decision the agent makes, without being a specific instruction about any particular decision.

A tool call produces a discrete result: the agent called the tool, received data, and acts on it. A loaded skill influences the entire texture of execution: every code block the agent writes, every recommendation it makes, every edge case it handles.

### What Skills Enable

**Domain expertise encapsulation.** The knowledge that lives in your most experienced engineers' heads can be written down as skills. When those engineers are unavailable, the agent still has access to their procedural knowledge. This is not a replacement for expertise; it is a durability mechanism.

**Repeatable workflows.** Complex multi-step processes that must be followed exactly — security reviews, incident post-mortems, deployment checklists — can be encoded as skills. The agent follows the process consistently, without the drift that comes from relying on human memory.

**Organizational knowledge capture.** Skills are a forcing function for externalizing knowledge that would otherwise remain tacit. The process of writing a skill requires making implicit knowledge explicit. Over time, a skills library becomes a machine-readable representation of organizational expertise.

**Cross-platform consistency.** An organization that uses GitHub Copilot for development, Claude Code for refactoring, and a custom agent for deployment gets the same domain knowledge applied consistently — because all three load from the same skill files.

### Writing Good Skills

A skill that is too general provides no value. "Write good code" is not a skill. A skill that is too specific becomes a spec fragment. There is a practical test:

*A good skill applies to every instance of a class of task, not to one specific task.*

If you find yourself writing "on this particular task, do X," you are writing spec content, not skill content.

Practical guidance for authoring skills:

- **Name concisely**: the name is the primary discovery signal. `database-migrations` is better than `guidelines-for-working-with-database-migration-files-in-this-project`.
- **Write the description to answer "when should I load this?"**: the agent's runtime infrastructure often uses descriptions to determine skill relevance. Make the loading condition explicit.
- **Lead with invariants**: what must always be true takes precedence. Put it first so the agent encounters the hard constraints before the soft guidelines.
- **Use examples for non-obvious conventions**: "use snake_case for field names" is clear. "Mirror the pattern used in `UserRecord` when adding new record types" is not — include a brief example.
- **Review skills like code**: skills should go through the same review pipeline as any other team artifact. Stale skills produce stale agent behavior.

### Skills in the Spec

The canonical spec template's Section 11 (Agent Execution Instructions) includes a "Skills to load" field for exactly this purpose. When writing a spec for a task that has relevant skills, the spec author lists the skill names and a brief note on why each applies:

```markdown
**Skills to load**
- `database-migrations`: This task involves adding two new columns. Apply migration safety guidelines.
- `api-design-patterns`: New REST endpoints are being added. Apply the API naming and versioning conventions.
```

This declaration serves two purposes. First, it gives the agent's runtime infrastructure the information to load the correct skills. Second, it makes the knowledge context for the task visible in the spec itself — a reviewer reading the spec can understand what organizational context the agent is expected to apply.

---

## Resulting Context

After applying this pattern:

- **Domain knowledge becomes portable and persistent.** Skills encode organizational knowledge that persists across team changes and applies across platforms.
- **Agent output quality improves without per-spec overhead.** Shared knowledge loaded from skills reduces the specification burden on individual tasks.
- **Cross-platform consistency becomes achievable.** The same skill applies regardless of which agent platform executes it.
- **Three scopes enable layered knowledge governance.** Project, personal, and organizational skills give appropriate authority levels to different knowledge types.

---

## Therefore

> **Agent Skills are packages of domain-specific procedural knowledge — written in `SKILL.md` files, governed as a cross-platform open standard — that agents load to apply domain and organizational expertise consistently across any task in that class. Skills solve the problem that tools can't (tools are capabilities, not knowledge) and specs shouldn't (specs are per-task, not per-domain). A skills library is an organization's machine-readable institutional memory, applied at the moment of agent execution.**

---

## Connections

**This pattern assumes:**
- [Agents as Executors of Intent](03-agents-as-executors.md)
- [Tools, MCP, and Capability Boundaries](04-tools-mcp-capability-boundaries.md)
- [The Canonical Spec Template — Section 11](../sdd/07-canonical-spec-template.md)

**This pattern enables:**
- [Human Oversight Models](06-human-oversight-models.md)
- Standards and Repertoires *(Part VI)*
- The organizational skills library as a governance artifact

---

*Next: [Human Oversight Models](06-human-oversight-models.md)*

