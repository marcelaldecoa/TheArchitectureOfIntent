# The Intent Archetype Catalog

**Part VI: Standards & Repertoires** · *2 of 5*

---

> *"A catalog is not a cage. It is a starting point calibrated by everyone who worked in this domain before you."*

---

## Context

Part III introduced the five canonical archetypes — Advisor, Executor, Guardian, Synthesizer, Orchestrator — and the four dimensions that define each: Agency Level, Risk Posture, Oversight Model, and Reversibility. Those archetypes are conceptual vocabulary.

This chapter materializes them as a usable catalog: reference profiles that practitioners consult when specifying a new agent deployment, with enough structure to serve as the starting point for Section 3 of any spec, and enough extensibility to accommodate organizational specializations.

---

## The Problem

The five archetypes work as a conceptual framework. They break down as a daily practice tool when every practitioner must mentally recall the dimensions, determine where their specific deployment falls, and write the spec sections that follow from that determination — from scratch, every time.

The catalog solves this by making the most common archetype profiles decision-ready: look up the closest match, read the dimension values, inspect the standard constraints and oversight configuration, adjust for your specific deployment context. The deliberation is compressed from "what archetype is this?" to "how does this differ from the standard Executor profile?"

---

## Forces

- **Completeness vs. usability.** A catalog that covers every archetype variant is comprehensive but overwhelming. A catalog that covers only the five base archetypes is accessible but insufficient for real deployment.
- **Standardization vs. specialization.** Standard profiles enable consistency. But every organization has domain-specific requirements that standard profiles cannot capture.
- **Catalog proliferation vs. catalog discipline.** Making it easy to add variants encourages growth. Unconstrained growth produces an incoherent catalog.
- **Reference-quality vs. starting-point quality.** Each profile must be good enough to use directly, not just good enough to inspire a custom version.

---

## The Solution

### How to Use This Catalog

**Step 1.** Identify the primary archetype your agent will instantiate. If you're uncertain, use the selection table in Part III ([The Five Archetypes](../architecture/02-canonical-intent-archetypes.md)) and the [Agency Levels and Risk Posture](../architecture/03-archetype-dimensions.md) chapter.

**Step 2.** Find the closest standard profile in the catalog below.

**Step 3.** Copy the dimension values into Section 3 of your spec. Note any deviations from the standard profile and document the rationale.

**Step 4.** Use the standard constraints and oversight configuration as the starting point for Sections 7 and 8 of your spec.

---

### Archetype Profile: Advisor

**Primary function:** Generate analysis, recommendations, and options. The human acts; the agent informs.

| Dimension | Standard Value | Notes |
|-----------|---------------|-------|
| Agency Level | 1 — Minimal | Produces text/analysis only; no direct action |
| Risk Posture | Low | Output is advice; human decision is the gate |
| Oversight Model | A — Pre-authorized, post-review | Review output quality; no mid-execution approvals |
| Reversibility | R1 — Fully reversible | Output is always text; any action is human-initiated |

**Standard constraints:**
- May not take actions on the user's behalf without explicit re-authorization as an Executor
- May not contact external parties
- May not access data outside the defined research scope
- Must surface uncertainty explicitly when confidence is below threshold

**Standard oversight configuration:**
- Spec approval: required before deployment
- Output review: human reads and acts on output; no confirmation step before generation
- Escalation: if asked to take an action, surface the Advisor/Executor distinction and request explicit archetype upgrade

**Typical use cases:** Research synthesis, option generation, decision support, documentation drafting, code review suggestions.

**Variant: Advisor with specialized domain skill**  
Identical profile, plus a designated skill file that encodes domain-specific analysis frameworks. Declare in spec Section 11 (Skills to load).

---

### Archetype Profile: Executor

**Primary function:** Carry out a defined, bounded task with direct system effects.

| Dimension | Standard Value | Notes |
|-----------|---------------|-------|
| Agency Level | 2–3 | Multi-step; limited branching |
| Risk Posture | Medium | Writes, updates, or creates — effects are real |
| Oversight Model | A or B | Model A for mature/repeatable; Model B for novel |
| Reversibility | R2–R3 | Most writes are reversible; some sends are not |

**Standard constraints:**
- Scope is the pre-authorized task and nothing adjacent
- Maximum read-scope is the data explicitly listed in Section 12
- Write operations require all fields to be explicitly declared; no schema discovery and fill
- No external communications without explicit destination list in spec
- NOT authorized: refactoring code outside the defined scope, restructuring data schemas, creating new API endpoints

**Standard oversight configuration:**
- Model A: spec approval required; human reviews output against spec criteria
- Model B: phase checkpoints defined in spec; human approves before phase boundary is crossed
- Escalation triggers: unexpected data format, target resource unavailable, spec appears to conflict with discovered reality

**Typical use cases:** Feature implementation, data transformation, document generation, scheduled report production, migration execution.

**Variant: High-frequency Executor**  
Agency Level 3, Oversight Model C (monitored execution). Suitable for batch operations that execute hundreds of times per day where per-run review is impractical. Requires enhanced audit logging and anomaly detection.

---

### Archetype Profile: Guardian

**Primary function:** Validate, audit, and enforce — flag violations without executing corrections.

| Dimension | Standard Value | Notes |
|-----------|---------------|-------|
| Agency Level | 1–2 | Reads broadly; writes only to audit/flag outputs |
| Risk Posture | Low-Medium | Reading is safe; flagging is advisory |
| Oversight Model | B — Checkpoint-based | Review findings before remediation is triggered |
| Reversibility | R1–R2 | Findings are reversible; triggered remediation is not |

**Standard constraints:**
- May read any resource explicitly listed in Section 12; no write access to source data
- May write to: audit log, findings report, flagging queue
- NOT authorized: auto-remediation, direct correction of violations, escalation to external parties without human approval
- Confidence threshold must be declared; findings below threshold routed to "uncertain" queue, not "violation" queue

**Standard oversight configuration:**
- Human reviews findings before any remediation workflow is triggered
- Findings queue reviewed by designated reviewer within defined SLA
- Escalation: pattern of violations that exceeds threshold triggers human review of whether auto-remediation should be activated (this is an archetype upgrade decision, not an agent decision)

**Typical use cases:** Security compliance scanning, data quality auditing, policy enforcement, code review, cost anomaly detection.

---

### Archetype Profile: Synthesizer

**Primary function:** Aggregate, transform, and compose multi-source information into a unified output.

| Dimension | Standard Value | Notes |
|-----------|---------------|-------|
| Agency Level | 2–3 | Multi-source reads; unified write output |
| Risk Posture | Medium | Output quality is high-consequence; process is read-heavy |
| Oversight Model | B — Checkpoint-based | Review synthesized draft before delivery |
| Reversibility | R2 | Draft output is revisable; distributed output is not |

**Standard constraints:**
- Source list is exhaustive: may not discover and add sources outside Section 12
- Synthesis must preserve source attribution in structured form; no unsourced claims
- Must flag contradictions between sources rather than silently resolving them
- Output must be validated against the success criteria before delivery, not after
- NOT authorized: reaching out to sources for clarification, commissioning new research

**Standard oversight configuration:**
- Draft review required before any distribution
- Human must approve the source list in spec before execution begins
- Escalation: source unavailable, sources materially contradict on a key point, confidence in synthesis is below threshold

**Typical use cases:** Intelligence reporting, research synthesis, document summarization, cross-system status aggregation, competitive analysis.

---

### Archetype Profile: Orchestrator

**Primary function:** Coordinate multiple specialized agents or processes to achieve a compound goal.

| Dimension | Standard Value | Notes |
|-----------|---------------|-------|
| Agency Level | 4–5 | Multi-step, multi-agent, adaptive planning |
| Risk Posture | High | Broad effect surface; coordinates irreversible actions |
| Oversight Model | C or B | Model C for established; Model B for novel workflows |
| Reversibility | R3–R4 | Sub-agent actions may be partially or fully irreversible |

**Standard constraints:**
- Each sub-agent must have its own spec with its own capability boundary; the Orchestrator spec does not override sub-agent specs
- Orchestrator may not grant sub-agents capabilities they were not already spec'd for
- Maximum wall-clock time and maximum cost must be declared as hard limits
- Failure handling must be explicit: what happens when a sub-agent fails, partially fails, or returns unexpected results
- Escalation is mandatory when: any sub-agent reports an unexpected result that would change the plan, combined cost is projected to exceed declared limit, a required sub-agent is unavailable

**Standard oversight configuration:**
- Model B: human approves plan before sub-agent execution begins
- Model C: human reviews logs at defined checkpoints; interrupt capability active
- Each phase that produces an irreversible effect requires checkpoint approval

**Typical use cases:** Multi-stage deployment pipelines, complex document production (multiple specialist agents), parallel research and synthesis, multi-system data migrations.

---

### Extending the Catalog

The five profiles above are starting points, not ceilings. Organizations should extend the catalog with:

**Domain-specific variants.** A "Financial Compliance Executor" is an Executor with elevated constraint specificity, mandatory audit logging, and confirmation requirements for monetary operations. It belongs in the catalog so every financial-system spec author has a proven starting point.

**Composite archetypes.** Some deployments combine archetype characteristics: a Guardian that can initiate remediation when violations are low-risk (Guardian + scoped Executor). Document the combined profile explicitly with clear rules about when the Executor capability activates.

**Organizational capability stamps.** As your agent deployments mature, certain configuration patterns prove reliable in your environment. Document them here: "Our Executor-v2 profile has been running production deployments for 18 months; use it as the default for deployment specs." The catalog becomes a living record of the organization's operational learning.

To add a catalog entry, the pattern is:
1. Deploy an archetype variant in a real task
2. Run it for sufficient time to validate the configuration is stable
3. Extract the profile: dimension values, constraints, oversight configuration
4. Peer-review the profile
5. Add it to the catalog with provenance (team, date, context)

---

## Resulting Context

After applying this pattern:

- **Archetype selection becomes lookup, not invention.** Teams select from pre-built profiles rather than reasoning from first principles each time.
- **Governance is pre-authorized.** Each profile carries its governance requirements. Selecting a profile selects its governance automatically.
- **Extension follows a governed process.** Domain-specific variants extend the catalog through an explicit process rather than ad-hoc modification.
- **Consistency compounds across the organization.** Multiple deployments of the same profile produce predictably similar governance structures.

---

## Therefore

> **The Intent Archetype Catalog materializes the five archetypes as decision-ready profiles — dimension values, standard constraints, and oversight configurations that practitioners copy and adjust rather than derive from scratch. It accelerates spec authoring, reduces dimension-selection variance, and grows as the organization accumulates validated deployment patterns. The catalog is the institutional memory of how archetypes have been applied reliably in this organization's specific context.**

---

## Connections

**This pattern assumes:**
- [The Organizational Repertoire](01-why-repertoires-matter.md)
- [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md)
- [Agency Levels and Risk Posture](../architecture/03-archetype-dimensions.md)
- [Oversight Models and Reversibility](../architecture/03-archetype-dimensions.md)

**This pattern enables:**
- [Spec Template Library](03-spec-template-library.md)
- Org-specific archetype extension

---

*Next: [Spec Template Library](03-spec-template-library.md)*


