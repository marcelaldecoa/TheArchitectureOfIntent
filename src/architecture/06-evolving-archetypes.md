# Pattern 3.6 — Governed Archetype Evolution

**Part III: Intent Architecture** · *6 of 6*

---

> *"A building is not a building. It is a process — a process which, over time, unfolds. And the quality of the process determines the quality of the result."*  
> — Christopher Alexander, *The Nature of Order*

---

## Context

You have classified a system, specced it, and shipped it. Three months later, a stakeholder wants to expand what it does. Or six months later, the system has quietly accumulated capabilities it was never formally authorized to have. Or a year later, you inherit a system and have no record of why it was classified the way it was.

Archetypes are not permanent — but changing them must be a deliberate act, not an accumulation of small decisions.

This pattern assumes all of [Intent Architecture](01-archetypes-as-constitutional-law.md), and is the closing pattern for Part III.

---

## The Problem

The hardest archetype problem is not classification — it is drift.

A system begins as an Executor within a tight pre-authorized scope. Over time, individual decisions expand the scope slightly: *this API call is basically the same as the authorized ones*, *this additional write is necessary for the feature to work*, *the exception gate is too slow for this case, let's skip it just this once*. No single decision is dramatic. Each is locally defensible.

Six months later, the system is taking consequential actions across a much broader domain with less oversight than was originally designed. It is still technically classified as an Executor, but it is now functioning as an uncontrolled Orchestrator. The archetype became a fiction.

This is archetype drift — and it is more dangerous than a wrong initial classification, because at least a wrong initial classification can be discovered and corrected. Drift is invisible until a consequential failure reveals it.

The inverse problem also occurs: a system is over-constrained for its actual risk. An Advisor that was given Guardian-class oversight because someone was nervous during initial design never gets simplified. Friction accumulates, engineers route around it, and eventually the oversight process exists on paper while real oversight happens not at all.

Archetypes need to evolve — but evolution must be governed differently from initial classification.

---

## Forces

- **Archetype permanence vs. operational reality.** Systems change in scope and capability over months and years; treating archetypes as immutable produces governance models increasingly divorced from actual behavior.
- **Drift invisibility vs. explicit evolution.** Small incremental decisions that expand scope are invisible until a failure reveals them; formal review processes are heavyweight but catch drift that informal change control misses.
- **Speed vs. governance.** Formal reclassification takes time. Systems are under deadline pressure. The process cannot be so heavy that teams route around it, yet cannot be so light that drift happens invisibly.
- **Accountability vs. flexibility.** When an archetype changes, someone made that decision. There must be a record of who and why. Yet expecting formal notification of every scope expansion may create incentives to classify loosely from the start.

---

## The Solution

### The Distinction Between Evolution and Drift

**Drift** is when a system's actual behavior diverges from its archetype classification because of accumulated, unreviewed decisions.

**Evolution** is when a system's archetype classification is formally updated to match a deliberate, reviewed change in scope or capability.

The mechanisms that distinguish them:

| | Drift | Evolution |
|---|---|---|
| **How it happens** | Small incremental decisions, no review | Explicit proposal, formal review |
| **Who knows it happened** | Often no one | The team + reviewers |
| **Is the spec updated?** | No | Yes, before deployment |
| **Are invariants reviewed?** | No | Yes |
| **Is the change reversible?** | Often not | By design |
| **Risk posture re-evaluated?** | No | Yes |

The spec is the primary instrument for distinguishing drift from evolution. If the spec was not updated before the behavior changed, the change was drift.

---

### Triggers for Archetype Review

A formal archetype review should be triggered when any of the following occur:

**Capability expansion triggers:**
- The system can now write to a new target system it couldn't before
- The system can now make decisions it previously surfaced to humans
- The system's action scope has expanded beyond what the pre-authorized scope declaration describes
- The system now routes work to or from other agents it didn't interact with at time of classification

**Risk change triggers:**
- The system now processes data it didn't before (especially personal, financial, or safety-critical data)
- The potential impact scope has grown (more users, more downstream systems affected)
- A failure mode has been identified that wasn't considered in the original Risk Posture

**Oversight degradation triggers:**
- The agreed oversight process is being routinely bypassed or skipped
- The exception gate is generating so many exceptions that it has become nominal
- Human reviewers in the oversight chain are no longer making substantive reviews

**Third-party trigger:**
- Any security audit or incident post-mortem that references the system
- A significant change to any external system the agent integrates with
- Regulatory or policy change that affects the data or actions the system handles

---

### The Archetype Review Process

An archetype review is not a re-evaluation starting from scratch. It is a comparison of the current behavior against the current spec, against the original archetype declaration.

**Step 1 — Behavior audit.** Without looking at the spec, describe what the system actually does today. What data does it read? What actions does it take? What decisions does it make autonomously? What does it escalate? This description should come from logs, code, and team knowledge — not the spec.

**Step 2 — Spec gap identification.** Compare the behavior audit against the current spec. Document every discrepancy. There will always be some. The question is whether they are structural (affecting archetype, dimensions, or invariants) or peripheral (affecting implementation detail).

**Step 3 — Re-run the decision tree.** Apply [Pattern 3.4](04-decision-tree.md) to the system as described by the behavior audit. Does the result match the current archetype classification?

If yes: Update the spec to close the peripheral gaps. The archetype stands.

If no: proceed to Step 4.

**Step 4 — Reclassification proposal.** Document: what the current archetype is, what the correct archetype appears to be, what changed, and who authorized or permitted those changes. This is an accountability document, not a blame document. Its purpose is to ensure that reclassification is owned.

**Step 5 — Dimension and invariant review.** If the archetype changes, all four dimensions must be re-evaluated from scratch. The prior dimensions are not inputs to the new evaluation — they are a comparison check after the new evaluation is complete. Invariants from the old archetype must be audited: do they still apply? Are they sufficient? Are any of them now wrong?

**Step 6 — Spec update and redeployment.** Update the spec before deploying any new behavior. The spec must describe the system as it will be, not as it was.

### Integrating Archetype Reviews Into CI/CD

In continuous deployment environments, archetype evolution must be integrated into the delivery pipeline rather than treated as an offline governance exercise:

- **Spec-as-code.** Store specs alongside application code in the repository. Spec changes follow the same pull request and review process as code changes. Archetype reclassification is a PR that requires explicit approval from the authority level defined in [Delegated Definition Authority](../operating/03-who-defines-archetypes.md).
- **Automated drift detection.** CI checks can validate that the system's declared capabilities (tool manifest, API surface, data access) are consistent with its archetype's authorized scope. A new tool added to the manifest that exceeds the current archetype's boundaries should fail the pipeline and trigger a review.
- **Gated promotion for archetype changes.** When an archetype is reclassified, the deployment requires a manual gate — the spec reviewer signs off before the pipeline proceeds. This is not bureaucracy; it is the minimum governance for a change that alters oversight requirements, risk posture, and invariants.
- **Feature flags for planned evolution.** Planned transitions (Advisor → Executor) can be gated behind feature flags that are enabled only after transition criteria are met and the spec is updated. The flag flip is a logged event, not a silent change.

---

### Planned Evolution

Some archetype evolution is anticipated from the beginning. A system built to validate content may be planned to take enforcement action in future phases. An Advisor may be planned to become an Executor once trust is established.

Planned evolution should be documented in the initial spec, not as a commitment but as a declared transition path:

```markdown
## Planned Evolution

**Current classification:** Advisor (Agency Level 2)  
**Target classification (Phase 2):** Executor (Agency Level 3)  
**Transition criteria:**  
  - 90-day operational record with <0.1% false positive rate  
  - Formal sponsor review and approval  
  - Spec updated before any autonomous action is enabled  
**What will NOT change at transition:** The Guardian layer invariants apply in 
Phase 2 as they do in Phase 1.
```

This declaration serves two purposes. First, it makes the future intent visible so that teams operating the Phase 1 system know what the goal is. Second, it creates a formal threshold — the transition criteria — that must be met before the archetype changes. The transition becomes an event, not a drift.

---

### The Hardest Case: Downgrading an Archetype

Systems almost always expand in scope. Downgrading — reducing from Executor to Advisor, or from Orchestrator to Executor — is rare and requires the same formal review as upgrading.

A common reason for downgrading: a system was over-built for its actual risk, and the overhead of its governance model is disproportionate. The correct response is a formal reclassification, not a quiet relaxation of the oversight model while keeping the archetype label.

The reclassification removes the liability of governing a system by the wrong model — including the liability of having a governance model that nobody follows.

---

### The Constitutional Record

Every archetype classification, review, and reclassification should be recorded in the spec's version history. Not just "updated classification" — the actual record:

- Date
- Previous classification
- New classification  
- Reason for change
- Reviewer(s)
- Transition criteria (if applicable)

This record is the constitutional history of the system. It is the document a future engineer reaches for when they need to understand why the system is the way it is. It is the document an auditor reaches for when accountability matters.

Write it with that reader in mind.

---

## Resulting Context

After applying this pattern:

- **Drift becomes detectable.** With a defined separation between drift and evolution, audit can identify when a system has drifted and require remediation. The archetype is no longer fiction.
- **Transitions are loadbearing.** Planned evolution is now a named transition with explicit criteria. The transition itself is a checkable event.
- **Constitutional history becomes auditable.** With version history recorded in the spec, any reviewer can see what the system was classified as, when it changed, and why.
- **Reclassification authority is aligned.** The authority to reclassify a system is the same as the authority to originally classify it, preserving the constitutional principle.

---

## Therefore

> **Archetype drift occurs when small decisions accumulate without review, producing a system whose actual behavior no longer matches its governance model. Evolution is when the classification is formally updated to reflect a deliberate change — with a behavior audit, the decision tree re-applied, dimensions re-evaluated, and the spec updated before deployment. Planned transitions should be declared upfront with explicit criteria. Every reclassification should be recorded in the spec's constitutional history.**

---

## Connections

**This pattern assumes:**
- [Constitutional Archetypes](01-archetypes-as-constitutional-law.md)
- [Four Dimensions of Governance](03-archetype-dimensions.md)
- [The Archetype Selection Tree](04-decision-tree.md)
- [Archetype Composition](05-composing-archetypes.md)

**This pattern enables:**
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the spec version history section
- [Living Specs](../sdd/06-living-specs.md) — how specs evolve over time
- Part VII (Operating Intent Systems) — governance cadences in production

---

*Part III is complete. Continue to [Part IV: Spec-Driven Development](../sdd/01-what-sdd-means.md), or to the archetype deep dives: [Advisor](archetypes/advisor.md) · [Executor](archetypes/executor.md) · [Guardian](archetypes/guardian.md) · [Synthesizer](archetypes/synthesizer.md) · [Orchestrator](archetypes/orchestrator.md)*

