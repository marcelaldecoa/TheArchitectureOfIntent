# The Spec Template Library

**Repertoire & Reference**

---

> *"The canonical template is the grammar. The typed templates are the sentences your team actually writes."*

---

## Context

Part IV produced the [Canonical Spec Template](../sdd/07-canonical-spec-template.md) — a 14-section master structure that covers every element a spec might need. It is comprehensive by design. It must be, to serve as the authoritative reference for the framework.

But no practitioner writes from the canonical template every day. It is too comprehensive for routine use — most tasks require seven or eight sections fully, and the other sections partially or not at all. The overhead of deciding which sections to include, which to abbreviate, and which are mandatory for this task type is non-trivial. Multiplied across a team and a year, it is significant.

The Spec Template Library solves this with typed templates: pre-configured specializations of the canonical template, each calibrated for a specific class of work, with the mandatory sections pre-populated, the optional ones scoped, and task-specific guidance already in place.

---

## The Problem

Teams that adopt SDD often cycle through the same frustration: the canonical template is excellent, but starting from it feels slow. The first few times, practitioners read every section carefully to determine applicability. After a few weeks, they start skipping sections they've decided aren't relevant for their usual work. The skipping is often wrong — sections that seemed optional turn out to matter, and the omission shows up in agent output quality.

The second problem is inconsistency. Ten practitioners writing feature specs from the canonical template will produce ten structurally different specs. The sections they include, their level of detail, the formality of their language — all vary. This creates difficulty for reviewers (different spec formats require different mental models to read) and for agents (unpredictable structure means unpredictable parsing).

Typed templates solve both problems: the structure is decided in advance, sections are pre-selected, and the team converges on a recognized format. Reviewing a feature spec looks like reviewing any other feature spec.

---

## Forces

- **Canonical completeness vs. task-specific efficiency.** The canonical 14-section template captures everything. But most tasks only need a subset, and requiring all sections creates overhead.
- **Template proliferation vs. template coherence.** Task-specific templates (feature, integration, agent instruction) reduce overhead. But too many templates create confusion about which to use.
- **Standardization vs. flexibility.** Templates should be consistent enough that reviewers know where to look. Yet tasks differ enough that some sections may be irrelevant.
- **Template quality vs. template availability.** A well-designed template reduces errors. A poorly designed template institutionalizes bad practice.

---

## The Solution

### What a Typed Template Is

A typed template is a pre-configured version of the canonical spec template for a specific class of task. It:

- Marks some sections as **required** (they must be completed for every spec of this type)
- Marks others as **conditional** (complete them if the relevant condition applies)
- Omits sections that are never applicable to this task type
- Pre-populates guidance and examples tailored to the class of task
- Cross-references the relevant archetype profile from the Archetype Catalog

A typed template is not a fill-in-the-blanks form. It is a scaffold. The practitioner still writes the content — the template provides the structure, the guidance, and the starting-point text. The cognitive work the template removes is: figuring out what to include and how to frame it. The cognitive work it preserves: understanding the task well enough to specify it clearly.

### Library Contents

The template library currently contains four templates. Each is fully specified in its dedicated sub-page.

**[Feature Spec Template](templates/feature-spec.md)**  
For new functionality being built by an Executor agent: a feature, a fix, a new capability, or a refactor with defined scope. This is the most frequently used template. Sections: Problem Statement, Scope, Archetype (Executor), Constraints, Success Criteria, Output Format, Oversight (Model A or B), Tools (list), Agent Execution Instructions.

**[Agent Instruction Template](templates/agent-instruction.md)**  
For configuring a standing agent deployment — not a one-time task spec, but the persistent instruction set that defines how an agent operates across many tasks. Used when deploying a new agent persona, configuring an MCP-connected bot, or defining the operational charter of a continuously-running agent. Sections: Agent Identity, Operational Domain, Capability Charter, Constraint Set, Escalation Protocol, Skill Manifest.

**[Integration Spec Template](templates/integration-spec.md)**  
For connecting two or more systems via API, event bus, file exchange, or data pipeline. Captures the integration contract formally enough that an Executor can implement and test it without clarifying questions. Sections: Integration Purpose, Source System, Target System, Data Contract, Volume/Rate Limits, Error Handling, Validation, Rollback Plan.

**[Constraint Library Template](templates/constraint-library.md)**  
Not a task spec — a reusable constraint set that can be referenced by other specs. Used to extract constraints that appear in many specs into a single governed artifact. When a spec says "apply constraints from constraint-library/data-handling-v2.md," that reference pulls in thirty tested constraint clauses from a single reviewed source.

### Growing the Library

The template library is not exhaustive. Organizations will need additional types:

- **Incident postmortem spec** — structured retrospective with defined sections for timeline, root cause, contributing constraints, and remediation actions
- **Data migration spec** — for ETL operations with volume, validation, and rollback requirements
- **Research synthesis spec** — for Synthesizer deployments with source list, output format, and citation requirements

The process for adding a new template type:
1. Identify a class of task for which practitioners have written ≥5 specs
2. Review existing specs of that type to identify which sections are invariant
3. Draft the typed template with section markings (required / conditional / omit)
4. Test it on a real task before adding to the library
5. Add with provenance: task class, derived-from spec IDs, review date

### Template Versioning

Templates change as the framework evolves and the organization learns. Version-control templates the same way as code:

- Semantic versioning: `feature-spec-v2.1.md`
- Specs reference the template version used: `Template: feature-spec-v2.1`
- Major version changes require a migration note explaining what changed and why
- Old versions are archived, not deleted — specs written against them remain valid

---

## Resulting Context

After applying this pattern:

- **Practitioners spend less time on structure, more on content.** Templates handle the format; authors focus on the substance of their specific task.
- **Review efficiency improves.** Reviewers know where to find constraints, success criteria, and oversight declarations in any spec because the template structure is consistent.
- **Template selection guides archetype thinking.** Choosing between feature spec, integration spec, and agent instruction templates forces early consideration of the system's nature.
- **Templates improve through organizational feedback.** When a template section consistently produces gaps, the template is updated to prevent the gap.

---

## Therefore

> **The Spec Template Library provides typed, pre-configured specializations of the canonical template for specific task classes. Typed templates eliminate structural variance, reduce spec authoring time, and direct the practitioner's cognitive effort toward task-specific content rather than structural decisions. The library grows from the organization's accumulated spec history — every class of recurring work is a template candidate, and every template makes the next spec of that type faster and more consistent.**

---

## Connections

**This pattern assumes:**
- [The Organizational Repertoire](01-why-repertoires-matter.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)
- [The Intent Archetype Catalog](02-archetype-catalog.md)

**This pattern enables:**
- [Feature Spec Template](templates/feature-spec.md)
- [Agent Instruction Template](templates/agent-instruction.md)
- [Integration Spec Template](templates/integration-spec.md)
- [Constraint Library Template](templates/constraint-library.md)
- [Standards as Agent Skill Source](04-code-standards.md)

---
