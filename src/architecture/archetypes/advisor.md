# The Advisor Archetype

**Part III: Intent Architecture** · *Archetype Deep Dive 1 of 5*

---

> *"The task of the advisor is not to decide. It is to make deciding possible."*

---

## Identity

**Primary Act:** Inform  
**Discretion Scope:** Narrow — chooses *what* information is relevant and *how* to present it; does not choose *what to do*

The Advisor surfaces relevant information, analysis, or recommendations to a human decision-maker. It produces outputs for evaluation. It does not act on those outputs. The human act of accepting, rejecting, or acting on the Advisor's output is a hard boundary between the Advisor and consequences.

---

## The Defining Characteristic

The Advisor's defining characteristic is its **non-actuation rule**: no change to external state, database, service, or system is caused by its output. The Advisor presents; humans execute.

This rule is frequently bent — and every bend is the beginning of misclassification. *"It just sends an email to summarize the meeting"* is not an Advisor if that email changes something. *"It just inserts a draft record"* is not an Advisor if drafts flow automatically to production. *"It just flags the anomaly in the log"* is an Advisor if a human reviews the flag before acting; it is not an Advisor if the flag triggers an automated response.

The test is not the format of the output (a report, a recommendation, a flag, a response). The test is: **between this output and any consequential change, is there a required human act?**

---

## Typical Forms

An Advisor appears as:

- **Retrieval and synthesis**: A query assistant that reads from knowledge bases and surfaces relevant context for a human writing a response.
- **Diagnostic aid**: A system that analyzes error logs and recommends candidate root causes for an engineer to investigate.
- **Recommendation engine (human-gated)**: A system that recommends configuration changes for a human to apply.
- **Document generator (pre-human-edit)**: A system that generates a draft document a human will review and publish.
- **Analysis reporter**: A system that produces a structured report on the state of a system for a human operator to read.
- **Decision support tool**: A system that surfaces options with tradeoffs for a human to choose between.

---

## Agency Profile

| Dimension | Typical Value | Range |
|-----------|:-------------:|-------|
| Agency Level | 1–2 | 1–2 only |
| Risk Posture | Low | Low to Medium |
| Oversight Model | A (Monitoring) | A or B |
| Reversibility | Fully reversible | Always R1 |

**Why Agency Level 1–2 only:** An Advisor at Agency Level 3 or above is a misclassification. Level 3 is "bounded discretion — decides how to accomplish defined tasks within a constrained module scope." If the system is choosing how to accomplish a task with external scope, it is not an Advisor; it is an Executor or Synthesizer in disguise.

**Why always fully reversible:** The output of an Advisor — a text, a report, a recommendation — can always be disregarded. If discarding the output has no effect, the action is reversible in the fullest sense. The moment disregarding the output is harder than acting on it (e.g., the output was automatically forwarded to another system), the system is no longer Advisor-class.

---

## Invariants

These constraints apply to every Advisor-class system and cannot be weakened by local context, performance requirements, or product convenience:

1. **No external writes.** The Advisor writes to no external system — no database, no file system, no API endpoint, no message queue — except to a dedicated output channel (dashboard, UI, log file) that is read by humans before any downstream action.

2. **No automatic forwarding.** The Advisor's output is not automatically consumed by another system that takes action. If the output flows to another system, it must pass through a human confirmation step.

3. **Non-rejection has no effect.** If a human ignores, dismisses, or never reads the Advisor's output, the world is unchanged. The output has no timeout that triggers an action.

4. **Scope declared, not inferred.** The Advisor's information scope — what sources it reads, what data it has access to — is declared in the spec and reviewed. It does not expand autonomously.

5. **Opinion clearly attributed.** Any recommendation, analysis, or conclusion the Advisor produces is clearly labeled as its output — not presented as ground truth. The Advisor presents a perspective; the human makes the determination.

---

## Violation to Watch For: The Soft Executor

The most common way an Advisor fails is by becoming a Soft Executor — a system that accumulates small automatic consequences:

- The summary email is sent to 50 recipients who treat it as authoritative.
- The recommended action is pre-populated in a form that takes two clicks to override.
- The flag appears in a dashboard where the default action is "apply."
- The draft document is automatically submitted unless the reviewer explicitly cancels within 24 hours.

None of these is unambiguously wrong in isolation. Together, they describe a system that has practical agency — its outputs have reliable real-world consequences — even if it was designed as an Advisor.

The diagnostic for this violation: Calculate the compliance rate. If the Advisor's recommendations are accepted more than ~85–90% of the time without substantive modification, ask whether the human review step is a genuine gate or a rubber stamp. This threshold is not arbitrary — it reflects the observation that in functioning advisory relationships (medical second opinions, code review, editorial review), a meaningful fraction of recommendations are modified or rejected by the reviewing human. A compliance rate approaching 100% suggests the human is not exercising independent judgment, which means the system has acquired practical agency without the governance to match. A genuine gate is sometimes rejected. A rubber stamp is an Executor without the governance.

---

## Spec Template Fragment

```markdown
## Archetype

**Classification:** Advisor  
**Agency Level:** 2 — Contextual (selects and synthesizes relevant information; 
                  applies judgment about what is material)  
**Risk Posture:** Low (output is consumed by human before any action; Medium if 
                  output scope includes sensitive personal or financial data)  
**Oversight Model:** A — Monitoring (output quality reviewed via sampling and 
                  user feedback; alert on anomalous output volume or latency)  
**Reversibility:** R1 — Fully reversible (output can be disregarded with no 
                  external consequence)

## Authorization Boundary

This system is authorized to:
- Read: [list data sources]
- Generate: [types of outputs]
- Write to: [output channel only — specify dashboard, log, UI widget, etc.]

This system is NOT authorized to:
- Write to any system other than [output channel]
- Trigger downstream actions
- Represent its output as authoritative without source citation

## Invariants

1. No output of this system causes an external state change without an 
   intervening human act.
2. This system never writes to [list prohibited targets].
3. All recommendations include a confidence signal and source references.
4. Output ignored/dismissed by the user has no timeout consequence.
```

---

## Failure Analysis

| Failure Type | Advisor Manifestation | Response |
|---|---|---|
| Intent Failure | Recommendations systematically miss what the user actually needs | Re-examine information scope and relevance model; spec may have wrong definition of "useful" |
| Context Failure | Reads data that is stale, incomplete, or out of scope | Review data source contracts; add freshness requirements to spec |
| Constraint Violation | Writes to a system beyond the authorized output channel | Immediate scope audit; invariant 1 has been violated |
| Implementation Failure | Surfaces irrelevant information; poor synthesis quality | Implementation-level fix; spec may need tighter output quality criteria |

---

## Connections

**Archetype series:** [Executor →](executor.md)  
**Governing patterns:** [Canonical Intent Archetypes](../02-canonical-intent-archetypes.md) · [Archetype Dimensions](../03-archetype-dimensions.md) · [Decision Tree](../04-decision-tree.md)  
**Composition:** [Composing Archetypes](../05-composing-archetypes.md) — Advisor as the advisory layer in a confirm-then-act Executor pattern  
**SDD:** [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)

