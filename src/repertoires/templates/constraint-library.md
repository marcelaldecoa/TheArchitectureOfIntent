# Constraint Library Template

**Part VI: Spec Template Library** · *Template 4*

---

> *A constraint library file is a reusable, reviewed set of constraints that specs can reference by name instead of repeating. This template defines the format. The actual library files for your organization live in `repertoires/constraint-libraries/`.*

---

## What a Constraint Library Is

A constraint library file is a named collection of constraints that apply to a class of agent work. When a spec references a constraint library, the agent treats all constraints in that file as binding for the task — identical to constraints written directly in the spec.

**The value:** Instead of writing the same twelve data-handling constraints in every spec that touches customer data, write them once in `constraint-libraries/customer-data-v2.md`, review and approve that file, and reference it with one line:

```
**Constraints (from library):** constraint-libraries/customer-data-v2.md
```

When the data handling policy changes, update the library file, bump its version, and all specs that reference the new version inherit the updated constraints.

**Versioning is critical.** Constraint libraries use semantic versioning. Specs reference a specific version (`customer-data-v2.md`), not just a name. This prevents a constraint library update from silently changing the constraints of an approved spec. When a library is updated, spec authors decide whether to upgrade their reference.

---

## Constraint Library File Format

```markdown
---
library-id: [REQUIRED: unique identifier, e.g. CLB-004]
name: [REQUIRED: human-readable name, e.g. customer-data]
version: [REQUIRED: v2.0]
effective-date: [REQUIRED: YYYY-MM-DD]
owner: [REQUIRED: team or individual]
reviewed-by: [REQUIRED: reviewer name]
next-review: [REQUIRED: YYYY-MM-DD]
description: >
  [One to three sentences: what class of work these constraints govern,
  and when a spec should reference this library.]
---

# [Library Name] Constraints — v[version]

## Scope

These constraints apply to any agent task that [describe the class of work].
Reference this library in your spec's Section 7 or Section 11 (Agent Execution Instructions).

## Invariants

*These constraints are absolute. No task spec may override them.*

- [Constraint statement — precise, testable, unambiguous]
- [e.g. PII fields (defined as: name, email, phone, address, government ID) must not appear in log output]
- [e.g. All writes to [system] must include an audit_user field set to the authenticated agent identity]

## Required Constraints

*All task specs that reference this library must satisfy these constraints.*

- [e.g. Data accessed for this task must be scoped to the requesting user's organization]
- [e.g. No bulk exports of more than 1,000 records without an explicit export authorization in the spec]
- [e.g. Deleted records must be soft-deleted; hard deletes require separate authorization]

## Conditional Constraints

*Apply these when the indicated condition is true.*

- **If writing to external storage:** All files must be encrypted at rest using [standard]
- **If sending to third parties:** Recipients must be in the approved vendor list at [location]
- **If processing financial data:** Transaction amounts must be validated against source; no rounding without explicit rounding rule in spec

## Anti-Patterns

*Patterns the agent must not use, even if they would work.*

- [e.g. Do not use wildcard selects (`SELECT *`) on tables with PII columns]
- [e.g. Do not cache authentication tokens across task boundaries]

## Changelog

| Version | Date | Changed By | Summary |
|---------|------|------------|--------|
| v2.0 | [date] | [name] | [What changed from v1] |
| v1.0 | [date] | [name] | Initial version |
```

---

## Organization Constraint Library Index

*Maintain this index as new libraries are added. It is the discovery mechanism for spec authors.*

| Library File | Name | Version | Governs | Owner |
|-------------|------|---------|---------|-------|
| `constraint-libraries/customer-data-v2.md` | customer-data | v2.0 | Any task that reads or writes customer PII | Data team |
| `constraint-libraries/financial-ops-v1.md` | financial-ops | v1.0 | Tasks that initiate or process financial transactions | Finance platform |
| `constraint-libraries/external-comms-v1.md` | external-comms | v1.0 | Tasks that send email, Slack, or notifications to external recipients | Comms team |
| `constraint-libraries/code-review-v3.md` | code-review | v3.0 | Executor tasks producing code for this codebase | Engineering |
| *[add as libraries are created]* | | | | |

---

## Referencing a Constraint Library in a Spec

In Section 7 (Constraints) of any spec:

```markdown
### Section 7 — Constraints

**Constraints from library:**
- `constraint-libraries/customer-data-v2.md` — this task reads customer records
- `constraint-libraries/external-comms-v1.md` — this task sends a notification email

**Additional task-specific constraints:**
- [Constraint not covered by any library]
- [Task-specific edge case handling]
```

The agent treats referenced library constraints as fully expanded into the spec. The agent is responsible for knowing both sets.

---

## Governance Process for New Libraries

1. **Identify the pattern.** When the same constraint block appears in ≥3 specs, it is a library candidate.
2. **Draft the library.** Use the format above. Write invariants, required, and conditional separately.
3. **Peer review.** At least one reviewer from the domain team who will use it.
4. **Register.** Add to the index above with owner and review date.
5. **Announce.** Notify teams that write specs in this domain.
6. **Maintain.** Owner is responsible for updates; old versions are never deleted.

---

*Back to: [Spec Template Library](../03-spec-template-library.md)*

