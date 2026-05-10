# Roles & Responsibilities (RACI) Card

**Appendices**

---

A one-page reference for who owns what across the framework's six operational activities. Use it during the [Intent Design Session](../theory/07-intent-design-session.md) (phases 3 and 6 in particular), in [Proportional Governance](../operating/04-governance.md) reviews, and in onboarding new team members to a system that is already running.

---

## RACI legend

The standard responsibility-assignment shorthand:

| Letter | Meaning | Cardinality |
|---|---|---|
| **R — Responsible** | Does the work. | One or more per activity. |
| **A — Accountable** | Owns the outcome; signs off on completion. | **Exactly one** per activity. |
| **C — Consulted** | Provides input *before* the work happens. Two-way communication. | Zero or more. |
| **I — Informed** | Receives the result *after* the work happens. One-way communication. | Zero or more. |

The framework's discipline is broken when **A** is unclear ("we're all accountable" = no one is) or when **A** is held by someone with no operational authority over the activity. Both failures are common; both produce the *diffuse responsibility* failure mode named in [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) §"Responsibility."

---

## The seven roles

The framework assumes seven roles. Two people may share a role; one person should not hold more than one role on the same system unless the system is small enough that a one-person practice is honest. The five roles required to run an [Intent Design Session](../theory/07-intent-design-session.md) (spec author, architect, operator, domain owner, skeptic) are a subset of these seven.

| Role | Responsibility |
|---|---|
| **Domain owner** | Knows what the system is being built for, in the domain language of the people it serves. Owns the framing — *what* the system is supposed to achieve. |
| **Spec author** | Owns the spec as a living artifact. Writes it during [phase 4 of the IDS](../theory/07-intent-design-session.md); amends it after every incident; maintains §13 (Spec Evolution Log). |
| **Architect / tech lead** | Owns the archetype commitment and the dimensional calibration. Has authority to say "that crosses the archetype's invariant." |
| **Builder** | The engineer or engineering team that implements the agent — system prompt, skill files, tool manifests, capability boundaries. Often plural; Accountability is on the team lead. |
| **Operator** | The person on the production pager. Owns the oversight model, the canary plan, the rollback trigger, the metrics instrumentation. |
| **Reviewer** | The human who validates outputs against the spec at the oversight gate. May be the operator, may be the spec author, may be a separate role for high-touch systems. |
| **Skeptic / security** | The role whose explicit job is to ask "what could go wrong?" Surfaces failure modes during [phase 5 of the IDS](../theory/07-intent-design-session.md), red-team protocols, and discipline-health audits. Often a security or platform person; sometimes a Cat 7 specialist for computer-use deployments. |

Two roles intentionally absent from this matrix: *executive sponsor* (who funds the work and is Informed at major milestones — they show up in the project's parent governance, not in the per-system RACI) and *end user* (whose voice belongs in framing via the domain owner, not as a separate RACI row, because end users do not typically have operational authority over framework activities).

---

## The six activities

Six operational activities, finer-grained than the four canvas activities. The mapping:

| Canvas activity | RACI activity | What happens |
|---|---|---|
| Frame | **Frame** | Define the problem, pick the archetype, calibrate the four dimensions. |
| Specify | **Specify** | Write the canonical spec (12 sections); Composition Declaration in §4 if applicable. |
| Delegate | **Build** | Implement the agent: system prompt, skills, tool manifest, capability boundaries, bound patterns. |
| Delegate | **Oversee** | Run the oversight model — review outputs, fire gates, respond to escalations. |
| Validate | **Ship** | Canary, rollback, spec versioning, deployment governance. |
| Validate | **Evolve** | Post-launch retrospectives, spec amendments, model-upgrade re-validation, framework-version bumps. |

The canvas's four activities are the *spine* of the discipline; the RACI's six are the *ownership-assignment grain*. Both vocabularies are correct for their purpose.

---

## The matrix

| Activity | Domain owner | Spec author | Architect | Builder | Operator | Reviewer | Skeptic |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Frame** | **A** | R | R | I | C | I | C |
| **Specify** | C | **A**, R | C | C | C | I | C |
| **Build** | I | C | C | **A**, R | C | I | C |
| **Oversee** | C | C | C | I | **A**, R | R | C |
| **Ship** | I | C | C | C | **A**, R | R | C |
| **Evolve** | C | **A**, R | C | C | C | C | C |

**A** = accountable (one per activity); **R** = responsible (does the work); **C** = consulted; **I** = informed.

Read across each row to find who does what for that activity. Read down each column to find a single person's responsibilities across the system's lifecycle.

---

## How to read each row

**Frame.** Domain owner is accountable — the goal is theirs. Spec author and architect both *do the work*: the spec author captures the framing in §1–§2, the architect drives the archetype commitment and the dimensional calibration. Operator is consulted (operational implications); skeptic is consulted (failure modes that should be designed against, not against). Builder is informed; they will implement later.

**Specify.** Spec author is both accountable and responsible — they own the artifact. Architect, builder, operator, domain owner are all consulted because the spec encodes everyone's commitments. Reviewer is informed (will validate against this spec later). Skeptic is consulted on §6 invariants and §10 open questions.

**Build.** Builder is accountable for the implementation matching the spec; their team is responsible. Spec author is consulted whenever ambiguity surfaces (which should trigger a §10 entry, not a guess). Architect is consulted on adherence to the archetype's invariants. Operator is consulted on operational requirements (what the runtime needs from the implementation).

**Oversee.** Operator is accountable for the oversight model running. Reviewer is responsible for actually doing reviews when the gate fires. Spec author is consulted when reviewer judgment surfaces ambiguity in the spec — this is the input that drives spec evolution. Skeptic is consulted for periodic red-team passes.

**Ship.** Operator is accountable for the deployment surface — canary, rollback, versioning. Builder and reviewer are responsible for the mechanical execution. Spec author is consulted to confirm the deployment matches the spec version. Skeptic is consulted on go/no-go for high-stakes shipments.

**Evolve.** Spec author is accountable — spec evolution is theirs. Everyone is consulted because amendments may touch any role's commitments. Reviewer's findings during oversight are the primary input for evolution; skeptic's audits surface drift.

---

## Common patterns

**Two-Rs-and-an-A is normal.** Most activities have one A and several Rs. RACI doesn't forbid this; it forbids *no* A or *multiple* As.

**The same role can be A across multiple activities.** Operator is A for Oversee and Ship. Spec author is A for Specify and Evolve. This is fine — it's the same human owning a coherent slice of lifecycle. What's not fine is changing A across activities without explicit handoffs.

**Skeptic is C, never A.** The skeptic's value comes from *not* having operational ownership. Making the skeptic A turns them into an operator with a contrarian's job description, which is structurally weaker than a non-owning critic with periodic review authority.

**Domain owner accountability stops at Frame.** After Frame, domain owner is C or I. The framework's discipline is that the domain owner *commits to* the goal during Frame and then defers operational decisions to the architect, builder, operator, and reviewer. Domain owners who try to stay A through Build or Oversee end up micromanaging implementation.

---

## Anti-patterns

**Everyone is A.** "We're all accountable for shipping safely." This is the diffuse-responsibility failure mode named in the [Calibration](../theory/03-agency-autonomy-responsibility.md) chapter. Diagnose by asking "if the system causes an incident at 3am, who gets paged?" The answer is the operator; that is the A for Oversee and Ship.

**No one is consulted before action.** Activities run with zero Cs — the work happens, then everyone is Informed. This is the *retrofit* anti-pattern from the [discipline-health audit](../operating/15-anti-patterns.md): consultation surfaces disagreement *before* the work, which is when disagreement is cheapest to resolve.

**Reviewer is informed, not responsible.** A common drift in *oversight kabuki*: the reviewer is listed in §11 of the spec as the human at the gate, but in the RACI they're shown as I. That contradiction means the gate is firing without anyone responsible for the judgment. Either promote the reviewer to R (with the time and authority to do real review) or downgrade the gate (move from Output Gate to Periodic).

**Skeptic absent from the RACI entirely.** Some teams forget to include a skeptic role at all. Their first incident reveals the failure mode the skeptic would have asked about during Frame. The skeptic's column in this matrix is mostly C — that is the role's correct shape, and it has to exist.

**Sponsor as A.** "The VP is accountable for this system." Operationally, the VP cannot be paged at 3am, cannot review the next spec amendment, cannot fire the oversight gate. They are *informed* of major milestones, not accountable for daily operation. If a sponsor wants accountability, they need to designate an operator and a spec author and accept that the operational A sits with them.

---

## Connections

- [The Intent Design Session](../theory/07-intent-design-session.md) — the IDS is where the RACI is *enacted*. Phase 1 establishes domain-owner accountability; phases 2–3 establish architect responsibility; phase 6 establishes operator accountability for oversight.
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) — *Responsibility* as a calibration dimension is what this card operationalizes; the dimension names *authorial / operational / validation* sub-loci, and this RACI maps them to actual roles.
- [Proportional Governance](../operating/04-governance.md) — the governance practice that runs against this RACI.
- [Adoption Playbook](../operating/11-adoption-playbook.md) — the adoption practice that introduces these roles to a team progressively, rather than all at once.
- [Signs Your Architecture of Intent Is Degrading](../operating/15-anti-patterns.md) — the audit that catches RACI drift, particularly the *oversight kabuki* and *diffuse-responsibility* anti-patterns.

---

*This card is intentionally short. If your team needs a finer-grained ownership matrix per system — for example, separating reviewer-of-Cat-1-failures from reviewer-of-Cat-2-failures — extend the matrix in your team's repertoire. The card here is the canonical baseline, not the only acceptable shape.*
