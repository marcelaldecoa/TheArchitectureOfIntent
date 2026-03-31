# The Executor Archetype

**Governance & Architecture**

---

> *"Power without boundary is not capability. It is liability."*

---

## Identity

**Primary Act:** Execute  
**Discretion Scope:** Bounded — decides *how* to accomplish a defined task within an authorized scope; does not decide *whether* the task should be done or *what* system it should act upon

The Executor takes consequential autonomous action on target systems within a pre-authorized scope. It is the workhorse of agent design — the archetype that actually changes things. It also carries the highest frequency of misdesign in practice, because the line between an authorized scope and an overreach is often invisible until it is crossed.

---

## The Defining Characteristic

The Executor's defining characteristic is its **pre-authorization model**: the scope of action is defined before the Executor runs, not discovered at runtime. The Executor decides *how* to execute within a defined space; it does not decide to expand the space.

This is the critical architectural constraint. An Executor that decides at runtime that a particular action is "probably fine" even though it's outside the declared scope has violated the pre-authorization model. This violation is common, locally defensible each time it occurs, and cumulatively catastrophic.

The inverse failure is also real: an Executor whose pre-authorized scope is so tightly bounded that it cannot accomplish its actual purpose will route around its constraints or require constant human intervention. A scope that is too narrow doesn't produce safety — it produces either a blocked system or a system that has learned to frame its overreaches as within-scope.

---

## Typical Forms

- **Code automation**: Refactoring, test generation, PR creation within a specified codebase scope
- **Data pipeline worker**: Reads from source, transforms, writes to defined destination tables
- **Infrastructure provisioner**: Creates/modifies resources within a declared infrastructure scope
- **Ticket resolver**: Applies a predefined resolution pattern to a qualifying support ticket
- **Notification dispatcher**: Sends messages to specified channels under defined trigger conditions
- **Scheduled maintenance agent**: Runs defined cleanup, archival, or rotation tasks on a schedule

---

## Agency Profile

| Dimension | Typical Value | Range |
|-----------|:-------------:|-------|
| Agency Level | 3–4 | 2–4 |
| Risk Posture | Medium | Medium to High |
| Oversight Model | D (Pre-auth scope + exception gate) | C or D |
| Reversibility | Partially reversible | R2–R3 |

**Why Agency Level 3–4:** The Executor decides how to accomplish tasks — selecting specific implementation paths, handling edge cases — but within a bounded scope. Agency Level 5 (fully autonomous goal pursuit) is not Executor territory; it is the Orchestrator or a misclassified system.

**Why Oversight Model D (default):** The pre-authorized scope declaration *is* the oversight mechanism for the Executor. Every action within scope is pre-approved; every action outside scope triggers the exception gate. This is why the scope declaration is the most important sentence in an Executor spec. A vague scope defeats Oversight Model D entirely.

---

## Invariants

1. **Scope is declared, bounded, and specific.** The Executor's authorization boundary is written in the spec as an explicit enumeration of authorized targets, actions, and conditions — not as a general description of intent.

2. **Out-of-scope actions are halted and surfaced, never silently skipped or quietly extended.** When the Executor encounters a situation that its scope doesn't cover, it stops and raises an exception. It does not attempt to handle the situation by reasoning that it's "close enough."

3. **Actions are logged at the point of execution.** Every consequential action is recorded with: what was done, to what target, under what authorization, at what time. This log is not advisory — it is the accountability record.

4. **Irreversible actions require explicit pre-authorization.** Any action in R3 or R4 (partially reversible through significant effort, or irreversible) must be explicitly listed in the scope declaration. A general authorization does not cover irreversible actions by implication.

5. **Scope does not self-expand.** The Executor may not add items to its own authorized scope. Only the governance process for archetype evolution ([Pattern 3.6](../06-evolving-archetypes.md)) may expand scope.

---

## The Scope Declaration

The most consequential artifact for an Executor-class system is its scope declaration. Scope declarations fail in two ways:

**Too vague:** *"The system is authorized to manage the codebase."* This is not a scope — it is an intent. A scope declaration names specific targets, action types, conditions, and exclusions.

**Too focused on happy-path:** *"The system is authorized to create pull requests in the `service-a` repository."* This is better, but: Can it modify any branch? Can it modify `.github`? Can it delete branches? Can it push directly? The scope should describe not only what it can do but what it explicitly cannot.

Canonical scope declaration structure:

```markdown
## Authorization Boundary

**Authorized targets:**
- Repository: `org/service-a`, branches matching `fix/*` and `feat/*`
- No access to: `main`, `release/*`, `.github/`, CI configuration files

**Authorized actions:**
- Create commits on authorized branches
- Open pull requests targeting `main` (not merging)
- Read all files within the repository

**Authorized conditions:**
- Only when triggered by: [specific event type]
- Only when: [precondition]

**Explicitly NOT authorized:**
- Merging pull requests
- Deleting branches
- Modifying workflow files
- Acting on any repository other than `org/service-a`

**Exception gate:** Any action not covered above → halt, log, and surface 
to [designated reviewer] before proceeding.
```

---

## Violation to Watch For: Scope Creep Through Exception Handling

The most common Executor failure is not an explicit scope expansion — it is exception handling that quietly becomes a capability.

An Executor authorized to create PRs encounters a case where the target branch doesn't exist. It could halt and surface this. Instead, it "helpfully" creates the branch — which is not in its authorized scope. The first time this happens, it looks like good behavior. The tenth time, it is an unreviewed capability.

The fix is not more sophisticated exception handling — it is simpler exception handling. The Executor's default behavior for anything outside its scope is halt-and-surface. Always. The exception gate catches everything that the pre-authorization didn't define.

---

## Spec Template Fragment

```markdown
## Archetype

**Classification:** Executor  
**Agency Level:** 3 — Bounded (decides how to accomplish defined tasks within 
                  the declared authorization scope)  
**Risk Posture:** Medium (writes to [target]; [reversibility assessment])  
**Oversight Model:** D — Pre-authorized scope + exception gate  
**Reversibility:** R2 — Largely reversible ([specific recovery mechanism, e.g.,
                  git history, soft delete, backup restore])

## Authorization Boundary

[Scope declaration as above]

## Invariants

1. No action outside the declared authorization boundary without exception gate.
2. All actions logged at time of execution with target, action type, and trigger.
3. Irreversible actions [list] require explicit per-execution authorization.
4. This system never expands its own scope.
```

---

## Failure Analysis

| Failure Type | Executor Manifestation | Response |
|---|---|---|
| Intent Failure | System executes correctly but the authorized actions don't accomplish the actual goal | Scope declaration is wrong; re-examine authorization boundary against actual system purpose |
| Context Failure | System acts on stale or incorrect data, producing correct action on wrong target | Review data freshness requirements; add precondition checks to spec |
| Constraint Violation | Action taken outside the authorization boundary | Immediate audit; scope declaration must be reviewed and exception gate must be strengthened |
| Implementation Failure | Actions within scope are executed incorrectly | Implementation fix; may surface spec ambiguity about how to handle edge cases |

---

## Connections

**Archetype series:** [← Advisor](advisor.md) · [Guardian →](guardian.md)  
**Governing patterns:** [Canonical Intent Archetypes](../02-canonical-intent-archetypes.md) · [Four Dimensions of Governance](../03-archetype-dimensions.md) · [Decision Tree](../04-decision-tree.md)  
**Composition:** [Composing Archetypes](../05-composing-archetypes.md) — Executor as governing archetype in confirm-then-act and Act+Guardian patterns  
**Evolution:** [Governed Archetype Evolution](../06-evolving-archetypes.md) — scope expansion is archetype evolution  
**SDD:** [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)

