# The Guardian Archetype

**Part III: Intent Architecture** · *Archetype Deep Dive 3 of 5*

---

> *"The value of a fence is not in the wood. It is in the boundary it marks. Remove the fence and the boundary may persist — or it may not. Build the boundary into the system, and it cannot be removed without a decision."*

---

## Identity

**Primary Act:** Enforce  
**Discretion Scope:** Narrow on enforcement, none on exception — the Guardian enforces declared constraints; it does not grant exceptions to itself

The Guardian's purpose is to protect a boundary. It watches for violations of declared invariants — policy boundaries, safety conditions, compliance rules — and acts when those invariants are in danger of being breached. Its action is fundamentally negative: it blocks, halts, or reverses. It does not initiate positive action toward a goal.

This negative-first design is the Guardian's essential characteristic and the source of its trustworthiness.

---

## The Defining Characteristic

The Guardian is distinguished by the asymmetry of its action authority: **it has strong authority to prevent or halt; it has no authority to create, modify, or initiate.**

An Executor that also validates its own outputs before acting has a Guardian component — but it is still an Executor as the governing archetype. A system whose *only* autonomous action is to block or halt when a condition is violated is a Guardian.

The test: if the Guardian were removed from the system, positive actions would continue to happen. The Guardian's removal means boundaries are no longer enforced, not that work stops.

---

## Typical Forms

- **Policy enforcement layer**: Checks that content, actions, or outputs comply with declared organizational policy before they proceed.
- **Rate limiter / circuit breaker**: Enforces usage or error-rate thresholds; halts when limits are exceeded.
- **Compliance validator**: Checks that data, code, or configurations meet regulatory or security requirements; blocks non-compliant items.
- **Safety check pre-executor**: Evaluates a proposed action against declared safety invariants before the Executor is permitted to proceed.
- **Access control enforcer**: Validates that the requesting agent has authorization for the requested action; denies what isn't authorized.
- **Drift detector**: Monitors system behavior for deviation from spec; alerts or halts when drift exceeds threshold.

---

## Agency Profile

| Dimension | Typical Value | Range |
|-----------|:-------------:|-------|
| Agency Level | 2 | 2–3 |
| Risk Posture | Medium | Low to High |
| Oversight Model | A + alert | A with alert or B |
| Reversibility | Fully reversible (blocks/halts) | R1 for blocks; R2–R3 if it takes remediation actions |

**Why Agency Level 2:** The Guardian applies declared rules; it does not make judgment calls about *whether* the rules are right. If a Guardian is regularly making discretionary exceptions, it has drifted to Agency Level 3 and is no longer operating as a Guardian — it is acting as an Executor with enforcement capability.

**Why Oversight Model A + alert:** The Guardian's operation is visible by design — every block or halt it generates is an event that should be logged and monitored. Oversight consists of reviewing: (1) that violations are being caught as expected, (2) that the false-positive rate is acceptable, and (3) that the Guardian hasn't been bypassed.

---

## Invariants

1. **Constraints are declared, not inferred.** The Guardian enforces what the spec says it enforces. It does not block based on its own assessment of what seems like a violation — it applies the declared rule.

2. **The Guardian cannot grant exceptions to itself.** If a violation is detected, the Guardian halts and surfaces. It does not decide that the violation is acceptable in this particular case. Exception granting is a separate human process.

3. **Blocks are logged at the point of enforcement.** Every block includes: what was blocked, which invariant was triggered, what the actual observed value was, and when it occurred. Silent blocks are not permitted — they are invisible and unauditable.

4. **The Guardian cannot be bypassed by the systems it governs.** The Guardian sits in the execution path, not alongside it. An architecture that allows the Executor to route around the Guardian when the Guardian would block it is not a Guardian architecture — it is theater.

5. **False positives are surfaced as policy feedback.** When a Guardian blocks something that turns out to be legitimate, that event is a policy feedback signal — the declared constraint may be wrong. The resolution is to update the constraint, not to train the Guardian to be more lenient.

---

## The Bypass Problem

The most dangerous Guardian failure is not a false negative (missing a real violation). It is being architects out of the execution path.

Common bypass mechanisms:
- Performance pressure: the Guardian adds latency, so an exception is added for "time-sensitive" operations
- Urgency exceptions: a flag that bypasses the Guardian for high-priority cases, initially intended for emergencies, becomes standard practice
- Environment exemptions: the Guardian is skipped in staging "for convenience," and staging gradually becomes the path for certain production actions
- Interface shortcuts: a new API endpoint is added that doesn't route through the Guardian's check

Each of these seems individually reasonable. Together, they describe a Guardian that exists in the architecture diagram but not in the actual execution path.

The design principle: a Guardian must be in the execution path with no lateral bypass. If bypassing the Guardian is ever the right answer, the constraint the Guardian enforces is wrong — and the resolution is to fix the constraint, not to add a bypass.

---

## Violation to Watch For: The Punitive Guardian

A Guardian that is technically correct but systematically wrong about which things matter will be circumvented — by users, by other systems, and eventually by architectural decisions.

A Guardian that blocks 20% of otherwise valid operations because its declared constraints are too strict is not protecting the system. It is creating pressure for the bypass mechanisms listed above.

The calibration check: Over a rolling period, what percentage of Guardian blocks are overturned by the human exception process? If the answer is high (>10%), the Guardian's constraints are miscalibrated. This threshold is a heuristic, not a universal constant — the principle is that a Guardian whose blocks are routinely overridden is not enforcing the organization's actual intent. The right threshold for your context depends on domain: a safety-critical Guardian might warrant investigation at >2%, while a content-formatting Guardian might tolerate >15%. The diagnostic question remains the same: are the constraints the right constraints? The spec needs to be fixed, not the Guardian's strictness. The Guardian is supposed to enforce what the spec says; if the spec says the wrong things, that is a spec problem.

---

## Spec Template Fragment

```markdown
## Archetype

**Classification:** Guardian  
**Agency Level:** 2 — Declarative enforcement (applies specified rules; 
                  does not make discretionary exceptions)  
**Risk Posture:** Medium (enforces [specific constraints]; false positives 
                  impact [volume/type of legitimate operations])  
**Oversight Model:** A — Monitoring with alert (every block logged; alert 
                  on block rate >X% or on zero-block periods exceeding Y days)  
**Reversibility:** R1 — Fully reversible (blocks/halts only; no state mutation)

## Enforcement Boundary

**Enforced invariants:**
1. [Specific constraint with specific threshold or condition]
2. [Specific constraint]

**Enforcement action on violation:**
- Block: [what is stopped]
- Log: [what is recorded]
- Surface: [where the block notification goes, and to whom]

**Explicitly NOT within enforcement scope:**
- [What the Guardian does not check or enforce]

**Exception process:**
- Who can override a Guardian block: [role/process]
- Override requires: [documentation / approval]
- Override is logged: [yes — all overrides recorded with reason]
```

---

## Failure Analysis

| Failure Type | Guardian Manifestation | Response |
|---|---|---|
| Intent Failure | Guardian enforces the declared constraints but the constraints don't actually protect the intended boundary | Constraint declaration is wrong; re-examine what the Guardian is protecting and why |
| Context Failure | Guardian does not have accurate visibility into the state it is protecting | Review data access; Guardian needs fresher or broader context for accurate enforcement |
| Constraint Violation | Guardian has been bypassed; blocks are not in the execution path | Architecture audit; bypass mechanisms must be removed or formally documented as intentional scope changes |
| Implementation Failure | Guardian blocks incorrectly (wrong false positive/negative rate) | May be implementation issue or miscalibrated constraint thresholds — test against known cases |

---

## Connections

**Archetype series:** [← Executor](executor.md) · [Synthesizer →](synthesizer.md)  
**Governing patterns:** [Canonical Intent Archetypes](../02-canonical-intent-archetypes.md) · [Archetype Dimensions](../03-archetype-dimensions.md) · [Decision Tree](../04-decision-tree.md)  
**Composition:** [Composing Archetypes](../05-composing-archetypes.md) — Guardian as embedded enforcement layer in Executor systems  
**SDD:** [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)

