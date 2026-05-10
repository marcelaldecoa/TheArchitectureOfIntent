# Glossary

**Appendices** · *Appendix A*

---

This glossary defines the core vocabulary of the Architecture of Intent. Every term defined here appears in at least one spec, archetype, or template elsewhere in this book. This is intentional — terms without referents are decoration.

*Terms are listed alphabetically. Each entry includes the pattern where the concept originates.*

---

## A

**Agency**
The capacity to act with discretion in pursuit of a goal. In system design, agency is distributed across instructors (spec authors), executors (agents, tools), and oversight functions. Distinguished from *operational autonomy*. See [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md).

**Archetype**
A pre-committed behavioral frame for a class of system. Archetypes define identity, agency level, oversight model, reversibility posture, and invariants in advance — before any specific system is designed. See [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md).

**Authorship**
The act of originating the intent that a system expresses and accepting accountability for its consequences. Authorship does not require proximity to code generation — the author of a specification is the author of the system that executes it. See [Prologue](../prologue.md).

---

## B

**Blast Radius**
The scope of consequence if a decision or action is incorrect. A key calibration factor when deciding how much oversight to require for a given operation. High blast radius + low reversibility = require maximum oversight.

**Boundary**
A limit on what a system or agent is permitted to do. Boundaries are encoded in specs as constraints and in archetypes as invariants. Distinguished from guidelines (which can be ignored) by their non-negotiable nature.

---

## C

**Capability Boundary**
The limit of what a tool or agent is permitted to access or affect. Defined in agent specifications and enforced through MCP tool design and authorization structures. See [Least Capability](../agents/04-tools-mcp-capability-boundaries.md).

**Companion Paper**
The arXiv-format distillation of this book — *The Architecture of Intent: A Framework for Designing Delegated Systems* — at `paper/architecture-of-intent.pdf` in the repository, with the editable Markdown source at `paper/architecture-of-intent.md`. ~15,000 words, structured for a reader evaluating the framework rather than adopting it. Both the paper and the book reflect the same Framework Version. See [The Companion Paper](companion-paper.md) for the section-by-section mapping.

**Constraint**
A non-negotiable rule embedded in a specification. Constraints define what an agent *cannot* do or *must* do. They are distinct from guidelines (advisory) and preferences (soft). See [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md).

**Context Provision**
The act of making institutional knowledge, architectural decisions, and domain-specific rules explicit in a specification so that agents can act reliably without guessing. A core responsibility of the orchestrator role.

**Cost Posture**
A structural sub-block of §4 of the canonical spec template, parallel to the Composition Declaration, that captures a system's *resource* commitment: model-tier commitment per step, latency budget, prompt-stability invariant, per-call cost ceiling, and cost-incident escalation. Distinguished from the four calibration dimensions (Agency, Autonomy, Responsibility, Reversibility), which are *behavioral* commitments about what the system does; Cost Posture is the *resource* commitment about what the system consumes. The framework's working position is that cost is **not** a fifth calibration dimension — see [Calibrate Agency, Autonomy, Responsibility, Reversibility — Cost is not a fifth dimension](../theory/03-agency-autonomy-responsibility.md#cost-is-not-a-fifth-dimension) for the structural rationale, and [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) §4 for the sub-block fields. The operational target this calibration serves is the *cost-per-correct-outcome* signal metric.

---

## D

**Delegation**
The act of transferring execution authority to an agent or automated system while retaining authorship and accountability. Delegation without constraints is abandonment. See [The Executor Model](../agents/03-agents-as-executors.md).

**Discipline-Health Audit**
A 60-minute, per-system, quarterly review that walks an opinionated catalog of *discipline anti-patterns* — spec theater, oversight kabuki, metrics theater, pattern inventory, calibration without commitment, citation theater (Synthesizer-specific; added at v2.1.0), prompt-patch drift, archetype drift, glossary by import, composition by accident, the retrofit IDS, the Adoption Playbook problem — and writes a one-paragraph verdict per anti-pattern (*not present*, *early signs*, *active*, or *not applicable* for catalog entries that don't apply to the system's archetype). Distinguished from system-level failure diagnosis (the Cat 1–7 fix-locus taxonomy in [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md)): the audit catalogs failure modes of the *discipline*, not of the systems built with it. See [Signs Your Architecture of Intent Is Degrading](../operating/15-anti-patterns.md).

---

## E

**Executor Archetype**
One of the five canonical intent archetypes. Characterizes systems that act autonomously to produce outcomes within defined boundaries. High agency, structured constraints, moderate oversight. See [The Executor Archetype](../architecture/archetypes/executor.md).

---

## F

**Failure Mode**
A predictable way in which a system, agent, or spec produces wrong outcomes. Cataloging known failure modes is a core activity of intent engineering — because failure modes are design signals, not surprises. See [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md).

**Framework Version**
A semantic-ish version number for the Architecture of Intent as a whole. The version applies to the framework's load-bearing commitments — the five archetypes, the four dimensions, the seven failure categories, the four oversight models, the four signal metrics, the **five** activities, composition as a first-class design surface — as instantiated by the book and the companion paper *together*. **MAJOR** bumps mark structural changes that break existing specs (a sixth archetype, a removed Cat, promoting a sub-activity to a peer activity); **MINOR** bumps mark additions that don't (a new chapter, a new pattern, a new spec sub-block); **PATCH** bumps mark prose, link, and figure refinements. Current version: **v2.2.1** (2026-05-10) — PATCH on top of v2.2.0. Three small refinements: (1) cross-references between paper §4.3 (Coding agents) and book Scenario 2 (the worked coding-pipeline walkthrough) — paper §4.3 now points readers at S2 for the end-to-end instantiation; (2) vignette-before-exposition openings on the five archetype subchapters (advisor, executor, guardian, synthesizer, orchestrator) — these are the most-cited reference chapters and previously had definition-style openings without scene-setting; (3) paper §1.1–1.2 prose sharpened to lead with the structural RLHF-completion-bias argument and to honestly acknowledge that benchmark-citation backfill remains deferred (no fabricated citations). No load-bearing commitments change. See [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) at the repository root.

**Framing**
The act of defining the problem space precisely enough that delegation can be both safe and productive. Framing determines what the agent is trying to do, what counts as success, and what must not happen. The foundation of every good spec.

---

## G

**Guardian Archetype**
One of the five canonical intent archetypes. Characterizes systems whose primary function is to protect invariants, enforce constraints, or prevent failure modes. Low agency, maximum constraint enforcement, high oversight. See [The Guardian Archetype](../architecture/archetypes/guardian.md).

---

## H

**Human Compiler** *(historical)*
The role of the software developer as the bridge between ambiguous business intent and literal machine execution. The concept whose obsolescence is the starting point of this book. See [Prologue](../prologue.md).

---

## I

**Invariant**
A condition that must always hold, regardless of what the system does. Invariants are the hardest constraints — they cannot be traded for performance, convenience, or edge-case handling. Defining invariants is a primary function of the oversight role.

**Intent**
The human purpose that a system is meant to serve. Distinct from *implementation* (how the purpose is achieved). Intent is what specs encode. Implementation is what agents produce. See [The Intent-Implementation Boundary](../theory/02-intent-vs-implementation.md).

**Intent Design Session**
A time-boxed working ritual (typically 3–4 hours, run once per system or per major spec revision) that walks a team through the five activities of the framework in seven concrete phases — Frame, Categorize, Calibrate, Populate Spec, Bind Patterns, Oversight & Metrics, Stage Rollout. Five required roles in the room (spec author, architect, operator, domain owner, skeptic). Produces a draft spec, a bound pattern set, an oversight model commitment, and a rollout plan with a scheduled retrospective. The ritual is what turns the framework from a vocabulary into a discipline. See [The Intent Design Session](../theory/07-intent-design-session.md).

**Architecture of Intent**
The discipline of designing intent — what a delegated system is supposed to do, what it must never do, and how we will know it is working — so that a non-human executor can act on it reliably and a human can validate the action accurately. Organized around three questions every delegated system must answer (*what is this system trying to achieve, within what constraints, and how will we know it is working?*) and **five** recurring activities: **Frame**, **Specify**, **Delegate**, **Validate**, **Evolve**. Three properties make it *architectural* rather than artisanal: intent is a designed artifact distinct from implementation; fixes live in structure (spec, manifest, CI, platform) rather than in prompts; and calibration along agency, autonomy, responsibility, and reversibility is deliberate. Defined in [Introduction — What is the Architecture of Intent?](../introduction.md#what-is-the-architecture-of-intent); summarized visually in [Introduction — The framework on one page](../introduction.md#the-framework-on-one-page); elaborated chapter by chapter through the rest of the book. The fifth activity, **Evolve**, was promoted from a closing-Validate sub-discipline to a peer activity in framework v2.0.0; see [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md).

---

## L

**Living Spec**
A specification that is versioned, evolves with the system, and is updated when agent behavior diverges from intent — rather than patching the code. The primary artifact of a spec-driven development practice. See [The Living Spec](../sdd/06-living-specs.md).

---

## M

**MCP (Model Context Protocol)**
An open protocol that standardizes how AI models interact with tools, data sources, and external systems. In intent engineering, MCP tools are the mechanism by which capability boundaries are enforced. See [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md).

**Minimum Viable Architecture of Intent (MVP-AoI)**
The one-page floor of the discipline for systems too small to warrant the full Intent Design Session: archetype, scope (in and out), oversight commitment, one signal, escalation trigger. ~15 minutes to write. Applicable when the system is small across all five of audience (just you or a small known group), stakes (R1–R2 reversibility), cohesion (one person), scale (bounded; not continuous production), and diagnosability (failures visible in real time). Five graduation triggers — audience expansion, stakes increase, cohesion break, ~100 runs/day scale, recurring undiagnosable failure — signal when the MVP has earned its keep and should upgrade to the full framework. See [Minimum Viable Architecture of Intent](../operating/16-minimum-viable-aoi.md). Distinguished from the [Miniature Pilot](../miniature-pilot.md), which is the *full canvas* applied to a small but production-bound system.

---

## O

**Operational Autonomy**
The ability to execute a pre-defined process without human intervention at each step. Distinguished from *genuine agency*, which involves discretion in novel situations. See [Autonomy Without Agency](../agents/02-autonomy-vs-agency.md).

**Orchestration**
The act of arranging agents, tools, and human oversight so that each does what they are best suited for, in service of a clearly specified goal. See [Prologue](../prologue.md).

**Orchestrator Archetype**
One of the five canonical intent archetypes. Characterizes systems that coordinate multiple agents or services toward a goal. Moderate agency, structured delegation, active oversight with escalation paths. See [The Orchestrator Archetype](../architecture/archetypes/orchestrator.md).

**Oversight**
The human function that validates agent outputs against intent, catches divergence before it becomes irreversible, and maintains accountability for system behavior. A first-class design concern, not a quality assurance afterthought. See [Proportional Oversight](../agents/06-human-oversight-models.md).

**Oversight Model**
One of four structured approaches to human oversight of agent systems: (A) Monitoring — observe and intervene; (B) Periodic — checkpoint-based review; (C) Output Gate — human approval before delivery; (D) Pre-authorized scope with exception escalation. The appropriate model is determined by the agent's archetype, risk posture, and reversibility. See [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) and [Proportional Oversight](../agents/06-human-oversight-models.md).

---

## R

**RACI**
A standard responsibility-assignment shorthand: **R**esponsible (does the work — one or more per activity), **A**ccountable (owns the outcome — exactly one per activity), **C**onsulted (provides input *before* the work happens), **I**nformed (receives the result *after* the work happens). The framework's [RACI Card](raci-card.md) maps the seven canonical roles (domain owner, spec author, architect, builder, operator, reviewer, skeptic) against the six operational activities (Frame, Specify, Build, Oversee, Ship, Evolve). The discipline breaks when **A** is unclear ("we're all accountable" = no one is) — a specific instance of the *diffuse responsibility* failure mode named in [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md).

**Repertoire**
A pre-authorized collection of archetypes, templates, constraints, and code standards that teams can use to accelerate spec-driven development without starting from scratch. Distinguished from "best practices" by their explicit authorization status. See [The Organizational Repertoire](../repertoires/01-why-repertoires-matter.md).

**Reversibility**
The degree to which an action can be undone or corrected after the fact. A primary design dimension for any system involving agents. High-agency systems acting on irreversible states require maximum oversight. See [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md).

**Reversibility Class**
A classification of an action's reversibility posture, ranging from fully reversible (R1 — soft delete, undo available) through partially reversible (R2–R3 — correctable with effort or within a time window) to irreversible (R4 — cannot be undone once executed). The reversibility class of an agent's highest-consequence action determines the minimum oversight and design requirements. See [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) and [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md).

---

## S

**SDD (Spec-Driven Development)**
An operating model where specifications become the primary artifact, the control surface for agent behavior, and the locus of quality assurance. See [Spec-Driven Development](../sdd/01-what-sdd-means.md).

**Spec**
Short for *specification*. In this book: a structured document that encodes intent, constraints, success criteria, and context in a form that agents can act on reliably. Not a requirements document for humans. Not a design document for developers. An operating instruction for machines. See [The Canonical Spec Template](../sdd/07-canonical-spec-template.md).

**Spec Gap Log**
A maintained record of every instance where agent output diverged from intent due to an incomplete, ambiguous, or incorrect specification. Each entry captures the gap type, which spec section was affected, and how the spec was updated. The primary instrument for organizational learning in a spec-driven practice. See [The Living Spec](../sdd/06-living-specs.md) and [Four Signal Metrics](../operating/06-metrics.md).

**SpecKit**
An open-source toolkit for spec-driven development, providing slash commands, templates, and structured workflows for creating and managing agent-executable specifications. See [SpecKit](../sdd/04-speckit.md).

**Synthesizer Archetype**
One of the five canonical intent archetypes. Characterizes systems that aggregate, distill, or compose information from multiple sources to produce structured outputs. Moderate agency, strong output constraints, human review of high-stakes outputs. See [The Synthesizer Archetype](../architecture/archetypes/synthesizer.md).

---

## T

**Translation** *(historical)*
The old paradigm for software development: converting ambiguous human intent into deterministic machine instructions. The task performed by the human compiler. Contrasted with the new paradigm of *orchestration*. See [Prologue](../prologue.md).

---

## V

**Validation**
The process of evaluating agent outputs against the intent expressed in a specification. Performed by humans. Cannot be fully delegated to agents without circular reasoning. See [The Spec Lifecycle](../sdd/03-spec-lifecycle.md).

---

*This glossary will grow as the book is developed. All terms will remain cross-referenced to their source patterns.*

