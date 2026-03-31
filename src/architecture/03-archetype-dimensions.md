# Four Dimensions of Governance

**Governance & Architecture**

---

> *"A compass gives you four directions. Navigation gives you precision. Dimensions give you the ability to place any system on the map — not just name its rough category."*

---

## Context

You know the five archetypes. Now you need to characterize them precisely — and more importantly, to characterize any real system in a way that reveals its design requirements clearly.

This pattern introduces the four formal dimensions along which archetypes (and systems) are described: **Agency**, **Risk**, **Oversight**, and **Reversibility**. Together these four dimensions form the governance profile of any agent system.

This pattern is the conceptual bridge between archetype identity (Pattern 3.2) and the practical decision tools (Pattern 3.4). It is also the vocabulary used in every individual archetype specification and in the [Archetype Catalog](../repertoires/02-archetype-catalog.md).

---

## The Problem

Naming an archetype is necessary but not sufficient for design. "This is an Executor" tells you the category. It does not tell you:
- How much autonomous discretion this particular Executor should have
- What the oversight cadence should be
- How to calibrate the spec's constraint section
- Whether a human approval gate is required before certain actions

Two systems are both Executors: a CI/CD pipeline that runs tests and a financial transaction processing agent. The category is the same. The governance requirements are radically different. The dimensions are the tool for expressing that difference precisely.

---

## Forces

- **Category vs. detail.** The archetype names the kind of system, but two systems of the same type can differ drastically in their oversight requirements. Yet specifying every system from first principles recreates the classification problem at every decision point.
- **Standardization vs. customization.** Systems need enough behavioral similarity that the archetype label carries meaning. Yet every real system differs in risk, scope, and consequence.
- **Expressiveness vs. learnability.** Four dimensions can express the nuance needed to distinguish one Executor from another. Adding more multiplies complexity; removing dimensions loses important distinctions.
- **Metric-driven vs. judgment-based.** Dimensions should be assessable by analyzing the system itself. Yet some dimensions require subjective assessment. The framework must accommodate both.

---

## The Solution

### The Four Dimensions

---

#### Dimension 1: Agency Level

**Definition:** The degree of discretion the system is authorized to exercise — the range of decisions it can make without human input.

Agency is described on a five-point scale:

| Level | Label | Meaning | Example |
|-------|-------|---------|---------|
| 1 | **None** | System surfaces information; all decisions and actions are human | Read-only dashboard |
| 2 | **Minimal** | System chooses among pre-enumerated options; no open-ended decisions | Classifier routing to defined categories |
| 3 | **Bounded** | System decides *how* to accomplish a defined task within a constrained space | Code refactoring within a module, with defined patterns |
| 4 | **Substantial** | System decides *what* to do and *how* within a broad requirement, with escalation for true edge cases | Feature implementation agent given an outcome goal |
| 5 | **Full** | System sets its own sub-goals and decides how to achieve the stated top-level goal with minimal constraint | Long-horizon autonomous research or planning agent |

Most production systems should operate at levels 2–4. Level 5 requires exceptional governance. Level 1 is appropriate for pure advisors.

**Design implication:** Each increment in agency level upward should be matched with a corresponding increment in constraint specificity and oversight investment. Agency level and constraint density must grow together.

---

#### Dimension 2: Risk Posture

**Definition:** The potential for system outcomes to cause harm — to users, to the organization, to third parties, or to data integrity — if the system fails, errs, or is misused.

Risk is assessed across three factors:

**Impact scope:** How many people or systems are affected if the system produces a wrong output?
- *Narrow* — affects one user or one isolated process
- *Broad* — affects many users, critical data, or inter-system state

**Severity:** How bad is the worst plausible bad outcome?
- *Low* — incorrect output that can be ignored or corrected easily
- *High* — output that causes financial, reputational, legal, or safety harm

**Detectability:** How quickly will a problem be noticed?
- *Fast* — problem surfaces in seconds or minutes (test failure, UI error, metric alert)
- *Slow* — problem surfaces over days or weeks (subtle bias, gradual data degradation)

**Composite risk label used in archetype profiles:**
- **Low** — Narrow + Low + Fast
- **Medium** — Mixed profile; requires explicit assessment
- **High** — Broad or High severity or Slow detectability present
- **Critical** — Broad + High + Slow; full governance tier required

---

#### Dimension 3: Oversight Model

**Definition:** The required structure of human involvement in reviewing, correcting, or authorizing the system's behavior.

Four oversight models cover the space of practical agent systems:

**Model A — Monitoring**
Human attention is triggered by anomalies or metrics, not by every output. The system runs continuously; humans review exceptions. Appropriate for: low-risk, high-reversibility systems with automated failure detection.

*Requirements:* Defined alert thresholds, automated anomaly detection, clear escalation path, designated reviewer.

**Model B — Periodic Review**
Human reviews a sample of outputs on a scheduled cadence. Not real-time. Appropriate for: medium-risk systems with medium reversibility where continuous monitoring would be overwhelming but some regular human eyes are needed.

*Requirements:* Defined sample size and sampling method, review schedule, review log, owner responsible for each scheduled review.

**Model C — Output Gate**
Human reviews and approves (or rejects) before any output is released or acted upon. Real-time review. Appropriate for: high-risk systems, irreversible outputs, or systems with broad impact.

*Requirements:* Review queue, defined reviewer, maximum review latency, clear approve/reject criteria, escalation for ambiguous cases.

**Model D — Pre-authorized Scope + Exception Gate**
Human defines the authorized scope in advance (the spec's constraint section). The system acts within scope without per-output review. Except: any action outside the pre-authorized scope must surface for human decision before executing.

*Requirements:* Precise scope definition in spec, reliable boundary detection, exception escalation path, logs of all scope-boundary events for review.

Model D is the most powerful production model — it enables high-velocity autonomous execution while preserving human authority at the boundaries. It is also the model that fails most expensively when scope definition is imprecise.

---

#### Dimension 4: Reversibility Posture

**Definition:** The inherent reversibility profile of this class of system's actions, and the minimum design requirements that follow.

Building on the reversibility spectrum from [Pattern 2.4](../theory/04-reversibility-as-design-dimension.md), each archetype carries a default reversibility posture:

| Reversibility Posture | Minimum Design Requirement |
|-----------------------|---------------------------|
| **Fully reversible** | Basic rollback / discard capability sufficient |
| **Largely reversible** | Staging / preview step recommended; rollback documented |
| **Partially reversible** | Dry-run mode required; confirmation step before side-effect actions |
| **Irreversible** | Human approval gate required; audit log mandatory; cannot be waived |

The reversibility posture of a specific system may differ from the archetype's default if the implementation makes otherwise-irreversible actions reversible (e.g., through soft deletes, draft queues, or paper-journal patterns).

---

### The Canonical Dimension Profiles

Applying all four dimensions to the five archetypes produces their canonical governance profiles:

| Archetype | Agency | Risk | Oversight | Reversibility |
|-----------|--------|------|-----------|---------------|
| **Advisor** | 1–2 | Low | Monitoring | Fully reversible |
| **Executor** | 3–4 | Medium–High | Model D (scope gate) | Partially–Irreversible |
| **Guardian** | 2 (veto only) | Low (when operating) | Monitoring + alert | Depends on what it guards |

**A note on the Guardian's agency level.** The Guardian shares a numeric agency level (2) with an Advisor at level 2, but the *kind* of discretion is qualitatively different. An Advisor at level 2 chooses among pre-enumerated presentation options — its discretion is compositional. A Guardian at level 2 exercises *veto discretion*: the authority to block, halt, or reject actions that violate constraints. Veto power is a categorically different capability from selection among options, even though both sit at level 2 on the numeric scale. The label "veto only" is essential — it signals that the Guardian's agency is directionally negative (it prevents, rather than initiates) and narrower than a general level-2 system.
| **Synthesizer** | 3 | Low–Medium | Periodic review or Output gate | Largely reversible |
| **Orchestrator** | 4–5 | High | Model C or D + escalation | Irreversible (coordinates irreversible agents) |

These are minimums. A specific implementation may require stronger governance than the canonical profile if its risk posture, impact scope, or reversibility profile is elevated above the archetype default.

---

### Using Dimensions to Validate Spec Design

The four dimensions are not just descriptive — they are diagnostic. When reviewing a spec, use the dimensions as a checklist:

**Agency check:** Is the agency level claimed in the spec consistent with the archetype? A system claiming Executor designation but with Agency Level 5 has miscategorized itself.

**Risk check:** Have all three risk factors (impact scope, severity, detectability) been explicitly assessed? An unassessed risk is an accepted risk — often unknowingly.

**Oversight check:** Does the oversight model described in the spec match the minimum requirement for this archetype and risk level? "The team will review occasionally" is not a Model B — it is the absence of an oversight model.

**Reversibility check:** For each action the system can take, has the reversibility been assessed? For irreversible actions: is there a human approval gate explicitly in the spec?

A spec that fails any of these checks is not ready for agent execution.

---

## Resulting Context

After applying this pattern:

- **Governance profiles become diagnostic.** The four dimensions make it visible when a system is under-governed or over-governed. Mismatch becomes discussable because the dimensions are explicit.
- **Constraints flow from structure.** Once a system's dimensions are established, the required constraints follow. The spec's constraint density can be calibrated to the dimensions.
- **Risk is owned explicitly.** By assessing all four dimensions, the organization can no longer ignore risk quietly.
- **Evolution becomes checkable.** When a system's dimensions change, the change is visible and auditable.

---

## Therefore

> **The four archetype dimensions — Agency Level, Risk Posture, Oversight Model, and Reversibility Posture — together form the governance profile of any agent system. They transform archetype names from categories into design specifications: they tell you what the spec must contain, what the oversight structure must look like, and what design requirements cannot be waived. Every serious spec review should evaluate all four.**

---

## Connections

**This pattern assumes:**
- [The Five Archetypes](02-canonical-intent-archetypes.md)
- [Design for Reversibility](../theory/04-reversibility-as-design-dimension.md)
- [Three Dimensions of Delegation](../theory/03-agency-autonomy-responsibility.md)

**This pattern enables:**
- [The Archetype Selection Tree](04-decision-tree.md) — putting the dimensions to practical use
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the oversight and constraint sections
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) — full dimension profiles per archetype
- [Proportional Oversight](../agents/06-human-oversight-models.md) — implementing the four oversight models

---
