# Delegated Definition Authority

**Governance & Architecture**

---

> *"The power to define what kind of thing an agent is determines everything that follows: what it can do, who can stop it, and who is accountable when it doesn't."*

---

## Context

The archetype definition is the highest-leverage point in the entire architecture of intent. An archetype definition establishes the Agency Level, Risk Posture, Oversight Model, and Reversibility class for every deployment of that pattern. Specs written against that archetype inherit its constraints and oversight configuration. Skills written for that domain encode its conventions. The downstream effect of an archetype definition is large and long-lasting.

The question of who should be allowed to make that definition is therefore not administrative. It is a governance design question with real consequences for organizational risk.

---

## The Problem

Organizations that deploy agents at scale typically develop one of two dysfunctional governance patterns:

**Centralized bottleneck.** A central AI governance team must approve every archetype definition. They have good intentions and appropriate caution. They also have no domain knowledge, are unfamiliar with the specific workflow, and are asked to review dozens of requests across a wide range of domains. The result is approvals that are slow, generic, and unable to catch domain-specific risk — "looks fine" signed by people who don't know what could actually go wrong.

**Diffuse proliferation.** Every team defines its own archetypes without review or coordination. An "Executor" in the payments team has different Agency Levels, different constraint sets, and different oversight expectations than an "Executor" in the content team. The word "archetype" stops meaning anything consistent. When something goes wrong, accountability is unclear and remediation is inconsistent.

Between these extremes, there is a model that achieves appropriate rigor without becoming a bottleneck: **delegated authority with mandatory review composition**.

---

## Forces

- **Central control vs. diffuse proliferation.** If everyone can define archetypes, the catalog becomes incoherent. If only central authority can define them, the process becomes a bottleneck.
- **Domain knowledge vs. architectural authority.** The person who best understands the domain may lack architectural expertise. The architect may lack domain knowledge.
- **Speed of deployment vs. governance rigor.** Every authorization step adds latency. Yet deploying systems under the wrong archetype creates risk that is invisible until failure.
- **Vendor claims vs. organizational assessment.** AI product vendors may assert that their system operates at a particular capability level. These claims cannot substitute for organizational assessment.

---

## The Solution

### The Three Principles

**Principle 1: Domain knowledge is required.**

No one should approve an archetype definition for a domain they don't understand. An archetype definition for a payment processing agent must involve someone who understands payment processing risk. An archetype definition for a code deployment agent must involve someone who understands deployment failure modes. The governance body that approves an archetype must include at minimum one person with operational knowledge of the specific domain.

This sounds obvious and is routinely violated. The remedy is explicit review composition requirements: the archetype definition approval checklist specifies which roles must be present in the approval, not just that "approval is required."

**Principle 2: Risk level determines authority level.**

Not all archetypes require the same governance depth. A low-Agency-Level, fully-reversible Advisor archetype in a narrow domain requires less governance investment than a high-Agency-Level Orchestrator with irreversible effect scope.

The authority level required to approve an archetype definition should scale with the risk profile of the archetype:

| Agency Level | Risk Posture | Reversibility | Minimum Approval Authority |
|--|--|--|--|
| 1–2 | Low | R1–R2 | Team tech lead + domain owner |
| 2–3 | Medium | R2–R3 | Staff engineer + domain owner + security review |
| 3–4 | High | R3 | Principal engineer + domain owner + security + data governance |
| 4–5 | High–Critical | R3–R4 | VP or equivalent + legal review + security + domain owner |

This is a minimum requirement. Organizations with their own governance frameworks should layer their requirements on top, not instead of, this baseline.

**Principle 3: Definitions are organizational artifacts, not individual decisions.**

An archetype definition affects every practitioner who will write specs in that domain. It affects every agent that will execute in the domain. It lives in the catalog and is referenced by future work that doesn't exist yet. It should be version-controlled, have a formal owner, and require a documented change process for updates.

Archetype definitions that live in one person's head, in a chat message, or in a comment on a PR are not real definitions. They are informal agreements that will be interpreted inconsistently, forgotten, and violated — not through negligence but because institutional knowledge that isn't written down doesn't survive personnel changes.

### The Definition Process

A properly governed archetype definition goes through five stages:

**1. Draft.** An intent architect or senior engineer familiar with the domain writes a proposed archetype profile using the catalog format from Part VI. The draft includes: proposed dimension values (Agency Level, Risk Posture, Oversight Model, Reversibility), rationale for each dimension, standard constraints, standard oversight configuration, and examples of tasks this archetype would govern.

**2. Domain review.** Subject matter experts in the domain review the draft for accuracy. They are not reviewing governance; they are reviewing whether the description of what the agent will do is correct and whether the constraints reflect the real risks of that domain. A payments SME catching that a proposed constraint doesn't handle chargeback scenarios is exactly the domain review's job.

**3. Risk review.** Security, data governance, and/or legal review the proposed dimension values and constraint set for organizational risk alignment. This review asks: are the oversight requirements sufficient? Are the NOT-authorized constraints comprehensive? Does the reversibility classification reflect the true cost of failure?

**4. Authority approval.** Based on the risk profile matrix above, the appropriate authority level signs off. For high-risk profiles, this may involve executive approval. For low-risk profiles, it may be the tech lead. The approval is documented with the approver's name, role, date, and the version of the profile approved.

**5. Catalog publication.** The approved archetype profile is added to the Intent Archetype Catalog (Part VI) with full provenance. It is version-controlled and announced to teams that will be writing specs in that domain.

### Who Cannot Define Archetypes

Certain roles are explicitly excluded from unilateral archetype definition:

**AI product vendors.** A vendor who sells an "autonomous AI agent" product cannot define the archetype that governs how their product is deployed in your organization. The vendor defines the product's capabilities; the organization defines the authorized archetype and constrains the deployment accordingly. Vendor sales materials that say "our agent is a Level 4 Orchestrator" are describing a capability claim, not granting an archetype definition.

**Individual engineers without domain authority.** An engineer can propose a new archeype profile. They cannot approve it, even for their own work. Self-approval on archetype definitions is not permitted. This is not a lack of trust in the individual; it is recognition that the downstream effect of an archetype definition is too broad to be a single-person decision.

**Autonomous agents themselves.** Agents may not modify their own archetype definitions, constraint sets, or capability boundaries. This is a hard system constraint, not a reviewable policy. An agent that executes a spec does not have authorization to upgrade its own Agency Level or remove a constraint that is inconvenient. The architecture of intent is governed by humans; it is not subject to agent negotiation.

### The Living Catalog and Change Control

Once published, an archetype definition is not frozen. Domains evolve, risks change, failure modes are discovered. The catalog must be maintained.

**Minor updates** (adding a variant, adding an example, correcting a description) follow the standard PR process with the domain owner's approval.

**Breaking changes** (changing a dimension value, tightening a constraint set, changing the oversight model) require a full re-approval through the original authority chain. All specs that reference the changed archetype must be reviewed for continued compliance.

**Deprecation** (removing an archetype profile from active use) requires communication to all teams with active specs that reference it, a migration path to an approved alternative, and an archive period before removal.

---

## Resulting Context

After applying this pattern:

- **Authority is proportional to risk.** Low-risk systems can be classified by team leads. High-risk systems require VP-level approval with security and legal review.
- **Exclusions are explicit.** Vendors, individual engineers acting alone, and agents themselves cannot unilaterally define archetypes.
- **The catalog remains coherent.** With clear authority, archetype definitions maintain consistent quality and governance standards.
- **Accountability is traceable.** Every archetype definition has a named authority who approved it.

---

## Therefore

> **Archetype definitions are high-leverage organizational governance artifacts: they set the authority scope for every agent deployment in a domain, and their quality is determined by the quality of the review that produced them. Governance authority scales with risk profile; domain knowledge is required at every level; and definitions are organizational artifacts version-controlled with formal ownership and change processes. Vendors, individual engineers, and agents themselves are explicitly excluded from unilateral definition authority.**

---

## Connections

**This pattern assumes:**
- [The Intent Architect](02-from-engineer-to-architect.md)
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md)
- [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md)

**This pattern enables:**
- [Proportional Governance](04-governance.md)
- Organizational authority framework for AI deployment

---
