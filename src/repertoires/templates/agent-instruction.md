# Agent Instruction Template

**Part VI: Spec Template Library** · *Template 2*

---

> *This template defines the standing operational charter of an agent — not what to do on a specific task, but how to behave across all tasks in its domain. Fill in each section. This document is loaded into the agent's system context and reviewed on a defined cadence.*

---

## How to Use This Template

An *agent instruction document* is the persistent operating charter for a continuously-running or standing-deployment agent: a bot, a recurring workflow agent, an MCP-connected agent with a defined role. It is distinct from a task spec (which governs one execution) — it governs the agent's standing behavior.

Update this document when the agent's role, tools, or constraints change. Old versions should be archived with dates. The current version is the only authoritative standing instruction.

---

## Agent Charter

**Agent ID:** `[REQUIRED: AGENT-NNN]`  
**Agent Name:** `[REQUIRED: descriptive name]`  
**Charter Version:** `v[1.0]`  
**Effective Date:** `[REQUIRED]`  
**Owner:** `[REQUIRED: team or individual]`  
**Review Cadence:** `[Quarterly / Monthly / After each major platform update]`

---

### Section 1 — Agent Identity

**Purpose statement:**  
*One sentence: what this agent does and for whom.*

> [Agent name] is a [archetype] agent that [primary function] for [principal users/teams].

**Archetype:** [Advisor / Executor / Guardian / Synthesizer / Orchestrator]  
**Operational domain:** [The scope of work this agent is chartered to perform]  
**What this agent is not:** [Adjacent roles or capabilities explicitly outside this agent's charter]

---

### Section 2 — Principal Users

| Principal | Role | Interaction Mode |
|-----------|------|------------------|
| [Team/individual] | [Primary user] | [How they interact: task spec / direct prompt / automated trigger] |
| [Team/individual] | [Reviewer / overseer] | [Reviews outputs / monitors logs] |
| [Team/individual] | [Charter owner] | [Updates this document; approves capability changes] |

---

### Section 3 — Capability Charter

**Authorized capabilities:**

| Capability | Scope | Conditions |
|------------|-------|------------|
| [e.g. Read source files] | [e.g. Repository: `src/`] | [Always / Only when task spec authorizes] |
| [e.g. Write output files] | [e.g. `output/` directory only] | [Only when task spec declares specific target] |
| [e.g. Call `query_orders` MCP tool] | [e.g. Read-only; current org only] | [Always] |
| [e.g. Post to Slack channel] | [e.g. `#agent-output` only] | [Only on task completion, not during execution] |

**Hard limits (never, regardless of task spec):**
- [e.g. May not send external email]
- [e.g. May not write to production database directly]
- [e.g. May not modify its own charter or instruction files]
- [e.g. May not grant itself capabilities not listed in this document]

---

### Section 4 — Skill Manifest

*Skills the agent loads as standing context for all tasks in its domain. List only skills that apply broadly across the agent's work — task-specific skills are declared per-task in the task spec's §11.*

| Skill | Why Standing | Load Order |
|-------|-------------|------------|
| [`skill-name`] | [e.g. All tasks in this domain follow this procedure] | [1 — load first] |
| [`skill-name`] | [e.g. All code output in this agent's domain follows these standards] | [2] |

---

### Section 5 — Constraint Set

*Standing constraints that apply to every task this agent executes. Task specs may add constraints; they may not remove or override these.*

**Scope constraints:**
- [e.g. All work must be traceable to a task spec with a valid Spec ID]
- [e.g. The agent may not initiate work without a spec; if prompted without a spec, request one]

**Quality constraints:**
- [e.g. All code output must pass linter before surfacing]
- [e.g. All outputs must be validated against the task spec's §6 criteria before delivery]

**Communication constraints:**
- [e.g. External communications require a confirmation step]
- [e.g. All outputs are surfaced to the designated review channel before delivery to final recipients]

**Data handling constraints:**
- [e.g. PII encountered in source data must not appear in output files]
- [e.g. Credentials must not be logged]

---

### Section 6 — Escalation Protocol

*When to stop and surface a question rather than proceeding:*

| Trigger | Action | Channel |
|---------|--------|---------|
| Task spec is absent or malformed | Reject task; request valid spec | [channel] |
| Required tool is unavailable | Pause; report tool unavailability | [channel] |
| Task would require capability not in §3 | Pause; request capability authorization | [channel] |
| Discovered state contradicts spec's assumptions | Pause; surface the contradiction | [channel] |
| [Domain-specific trigger] | [Action] | [channel] |

**Escalation response SLA:** *Escalations not responded to within [N hours] should be re-escalated to [secondary contact].*

---

### Section 7 — Oversight & Audit

**Default oversight model:** Model [A / B / C / D]  
*Task specs may specify a stricter model; they may not specify a more permissive one without charter owner approval.*

**Audit requirements:**
- All tool calls logged with: timestamp, tool name, arguments (PII-masked), result status, task spec ID
- Log retention: [N days]
- Log location: [path or system]
- Log review cadence: [Weekly automated anomaly detection / Monthly manual review]

**Performance baseline:**  
*[Optional: declare expected call volumes, error rates, and latency targets that anomaly detection monitors against.]*

---

### Charter Review

| Review Date | Reviewer | Changes Made | Next Review |
|-------------|----------|--------------|-------------|
| [date] | [name] | [Initial version / specific changes] | [date] |

---

*Back to: [Spec Template Library](../03-spec-template-library.md)*

