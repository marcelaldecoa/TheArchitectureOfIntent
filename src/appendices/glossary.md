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

**Constraint**
A non-negotiable rule embedded in a specification. Constraints define what an agent *cannot* do or *must* do. They are distinct from guidelines (advisory) and preferences (soft). See [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md).

**Context Provision**
The act of making institutional knowledge, architectural decisions, and domain-specific rules explicit in a specification so that agents can act reliably without guessing. A core responsibility of the orchestrator role.

---

## D

**Delegation**
The act of transferring execution authority to an agent or automated system while retaining authorship and accountability. Delegation without constraints is abandonment. See [The Executor Model](../agents/03-agents-as-executors.md).

---

## E

**Executor Archetype**
One of the five canonical intent archetypes. Characterizes systems that act autonomously to produce outcomes within defined boundaries. High agency, structured constraints, moderate oversight. See [The Executor Archetype](../architecture/archetypes/executor.md).

---

## F

**Failure Mode**
A predictable way in which a system, agent, or spec produces wrong outcomes. Cataloging known failure modes is a core activity of intent engineering — because failure modes are design signals, not surprises. See [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md).

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
A time-boxed working ritual (typically 3–4 hours, run once per system or per major spec revision) that walks a team through the four activities of the framework in seven concrete phases — Frame, Categorize, Calibrate, Populate Spec, Bind Patterns, Oversight & Metrics, Stage Rollout. Five required roles in the room (spec author, architect, operator, domain owner, skeptic). Produces a draft spec, a bound pattern set, an oversight model commitment, and a rollout plan with a scheduled retrospective. The ritual is what turns the framework from a vocabulary into a discipline. See [The Intent Design Session](../theory/07-intent-design-session.md).

**Architecture of Intent**
The discipline of designing intent — what a delegated system is supposed to do, what it must never do, and how we will know it is working — so that a non-human executor can act on it reliably and a human can validate the action accurately. Organized around three questions every delegated system must answer (*what is this system trying to achieve, within what constraints, and how will we know it is working?*) and four recurring activities: **Frame**, **Specify**, **Delegate**, **Validate**. Three properties make it *architectural* rather than artisanal: intent is a designed artifact distinct from implementation; fixes live in structure (spec, manifest, CI, platform) rather than in prompts; and calibration along agency, autonomy, responsibility, and reversibility is deliberate. Defined in [Introduction — What is the Architecture of Intent?](../introduction.md#what-is-the-architecture-of-intent); summarized visually in [Introduction — The framework on one page](../introduction.md#the-framework-on-one-page); elaborated chapter by chapter through the rest of the book.

---

## L

**Living Spec**
A specification that is versioned, evolves with the system, and is updated when agent behavior diverges from intent — rather than patching the code. The primary artifact of a spec-driven development practice. See [The Living Spec](../sdd/06-living-specs.md).

---

## M

**MCP (Model Context Protocol)**
An open protocol that standardizes how AI models interact with tools, data sources, and external systems. In intent engineering, MCP tools are the mechanism by which capability boundaries are enforced. See [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md).

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

