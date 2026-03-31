# Feature Spec Template

**Repertoire & Reference**

---

> *Copy this template. Fill in every section marked **[REQUIRED]**. Review conditionals and include those that apply. Delete this instruction block before submitting for approval.*

---

## How to Use This Template

This template is a pre-configured specialization of the [Canonical Spec Template](../../sdd/07-canonical-spec-template.md) for feature development: new functionality, fixes, refactors, or capability extensions built by an Executor agent.

**Mandatory sections:** 1, 2, 3, 5, 6, 8, 11, 12  
**Conditional sections:** 4 (multiple owners), 7 (external systems), 9 (data schema changes), 10 (non-functional requirements apply)  
**Archetype:** Executor  
**Typical oversight model:** A (mature/repeatable task) or B (multi-phase or novel task)

---

## Feature Spec

**Spec ID:** `[REQUIRED: FEAT-YYYY-NNN]`  
**Title:** `[REQUIRED: one-line description]`  
**Template:** `feature-spec-v1.0`  
**Date:** `[REQUIRED]`  
**Author:** `[REQUIRED]`  
**Reviewer / Approver:** `[REQUIRED]`  
**Spec Status:** `Draft` / `Under Review` / `Approved` / `Superseded`

---

### Section 1 — Problem Statement

**[REQUIRED]**

*State the problem this feature solves. One to three sentences. Describe the current state and why it is inadequate. Do not describe the solution here.*

> **Current state:** [What is true today that is insufficient or absent]  
> **Why it matters:** [The consequence of leaving this unchanged]  
> **Scope boundary:** [What related problems are explicitly out of scope for this spec]

---

### Section 2 — Objective

**[REQUIRED]**

*One sentence statement of what this spec will produce. Complete when read in isolation.*

> Build [artifact or capability] so that [who] can [do what], resulting in [measurable outcome or state change].

---

### Section 3 — Archetype & Agency

**[REQUIRED]**

| Dimension | Value |
|-----------|-------|
| Archetype | Executor |
| Agency Level | [2 — multi-step, bounded / 3 — multi-step, some branching] |
| Risk Posture | [Low / Medium — choose and justify if Medium] |
| Oversight Model | [A — spec approval + output review / B — checkpoint-based] |
| Reversibility | [R1 Fully / R2 Recoverable / R3 Partial / R4 Irreversible — list highest consequence action] |

**Justification for deviations from standard Executor profile:** *[Required if any dimension differs from the standard profile in the Archetype Catalog. Delete line if using standard profile.]*

---

### Section 4 — Stakeholders

**[Conditional: include if more than one team or system owner is involved]**

| Role | Name / Team | Responsibility |
|------|-------------|---------------|
| Spec Author | | Writes and owns this spec |
| Technical Reviewer | | Reviews for correctness and completeness |
| Domain Owner | | Approves constraints and scope |
| [Additional] | | |

---

### Section 5 — Scope

**[REQUIRED]**

**In scope:**
- [Specific thing the agent will do]
- [Another specific thing]
- *(be exhaustive — if it is not listed, it is out of scope)*

**Out of scope (explicit):**
- [Adjacent work that might seem related but is not authorized]
- [Refactoring outside the defined change area]
- [Performance optimization beyond the declared requirement]

**Definition of done:**  
*[One sentence: "This spec is complete when [specific, independently verifiable condition]"]*

---

### Section 6 — Success Criteria & Acceptance Tests

**[REQUIRED]**

*Each criterion must be answerable with a definitive yes/no by a reviewer who has only this spec and the output. Copy applicable rows from the [Code Output Validation Template](../05-validation-templates.md).*

| # | Criterion | Test | Pass Condition | Automatable? |
|---|-----------|------|----------------|--------------|
| 1 | [e.g. Unit test coverage] | [e.g. Run test suite] | [e.g. All tests pass; new behaviors have tests] | Yes |
| 2 | [e.g. Naming conventions] | [e.g. Linter] | [e.g. Zero linter violations] | Yes |
| 3 | [e.g. Error paths covered] | [e.g. Manual review] | [e.g. All error conditions in §5 have explicit handling] | No |
| 4 | [Task-specific criterion] | | | |

---

### Section 7 — Dependencies & External Systems

**[Conditional: include if the feature touches or depends on external systems]**

| System | Type | Dependency Nature | Owner |
|--------|------|------------------|-------|
| [System name] | [API / DB / Event / File] | [Required for completion / Informational only] | [Team] |

**Unavailability handling:** *If [system] is unavailable, the agent should [stop and escalate / proceed with mock data for testing / produce partial output and flag].*

---

### Section 8 — Oversight & Escalation

**[REQUIRED]**

**Oversight model:** Model [A / B]

*If Model A:*  
Spec is approved → agent executes → human reviews output against §6 criteria. No confirmation steps during execution.

*If Model B:*  
Phase checkpoints:
- After [phase 1 description]: agent surfaces [deliverable]. Human approves before proceeding.
- After [phase 2 description]: agent surfaces [deliverable]. Human approves before proceeding.

**Escalation triggers:**
- [Trigger 1 — e.g. Target file/record does not exist at expected path]
- [Trigger 2 — e.g. Test suite failure rate exceeds 10%]
- [Trigger 3 — e.g. Spec constraint appears to conflict with discovered codebase state]
- Any action not covered by §5 scope or §12 tool manifest

**Escalation channel:** *[How the agent surfaces an escalation — comment, file, message]*

---

### Section 9 — Data & Schema

**[Conditional: include if this feature changes data structures, schemas, or migrations]**

**Schema changes:**
- [Table/model/type]: [What changes — add field, rename field, change type, etc.]

**Migration requirement:** [Required / Not required]  
**Migration reversibility:** [Fully reversible / Two-phase required — explain]  
**Data impact:** [Affects N rows / No existing data affected / Backfill required]

---

### Section 10 — Non-Functional Requirements

**[Conditional: include if specific performance, security, or reliability requirements apply]**

| Requirement | Target | Measurement Method |
|-------------|--------|--------------------|  
| Response time | [e.g. p95 < 200ms] | [e.g. Load test at 100 rps] |
| Error rate | [e.g. < 0.1% under normal load] | [e.g. Monitor over 24h] |
| [Security] | [e.g. No secrets in output] | [e.g. Automated scan] |

---

### Section 11 — Agent Execution Instructions

**[REQUIRED]**

**Objective restatement (for agent):**  
*[One sentence: what the agent must produce. This is the agent's primary directive.]*

**Skills to load** *(list those that apply; omit section if none apply)*
- `[skill-name]`: [Why relevant to this task]

**Authorized actions:**
- Read: [specific files, modules, tables]
- Write: [specific files, modules, tables]
- Execute: [specific commands, test runners, linters]
- NOT authorized: [anything adjacent that might seem helpful but is out of scope]
- NOT authorized: [external communications]
- NOT authorized: [schema changes beyond those declared in §9]

**Completion signal:**  
*When the objective is achieved and all §6 criteria are satisfied, the agent should [describe how to signal completion — e.g. open a PR, write a summary file, post a status message].*

---

### Section 12 — Tool & Resource Manifest

**[REQUIRED]**

| Tool / Resource | Access Level | Scope Constraint |
|-----------------|-------------|------------------|
| [e.g. `read_file`] | Read | [e.g. `src/` directory only] |
| [e.g. `write_file`] | Write | [e.g. files declared in §5 scope only] |
| [e.g. `run_tests`] | Execute | [e.g. unit tests in `tests/` only] |
| [e.g. `run_linter`] | Execute | [e.g. modified files only] |

**Tools NOT authorized for this task:**  
- [e.g. Email / messaging tools]
- [e.g. Database schema mutation tools]

---

### Spec Approval

| | Name | Date | Notes |
|-|------|------|-------|
| Author sign-off | | | Spec is complete and ready for review |
| Technical review | | | Correctness and completeness verified |
| Approved for execution | | | Agent may proceed |

---

*Back to: [Spec Template Library](../03-spec-template-library.md)*

