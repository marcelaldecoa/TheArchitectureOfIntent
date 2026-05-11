# Multi-Tenant Fleet Governance

**Part 6 — Operations**

---

> *"Governing one agent is system design. Governing fifty agents across twelve teams sharing one platform is something else. The structure that worked for one does not extend by repetition."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 6 — Operations**. It addresses the gap the [Introduction's honest-scope section](../introduction.md#honest-scope-what-this-book-is-and-what-it-isnt) names — the framework, as written through v2.3.x, governed one system at a time. v2.4.0 adds this chapter to extend the discipline to *fleets*: many systems, many tenant teams, shared platform infrastructure, where single-system governance does not compose by repetition. The chapter develops the four structural moves a fleet needs (constraint inheritance, cross-tenant isolation, fleet-level telemetry partitioning, platform-tier failure-locus) and how those compose with the per-system discipline the rest of the book teaches.*

> *Where this sits in the work:* this chapter elaborates the *platform-team* counterpart of [Proportional Governance](01-governance.md). Proportional Governance answers *who reviews what, on what cadence* for a single system; this chapter answers *how those reviews compose across many systems sharing the same platform*. The [Intent Design Session](../foundations/07-intent-design-session.md) runs per system; fleet governance is what holds the shape of the discipline as the number of IDS-run systems grows from one to twelve to fifty.

---

## Context

A platform team operates an internal AI agent platform for the rest of the company. Twelve product teams have built agents against it. Each agent has its own spec, its own oversight model, its own constraint library entries. The platform team's job is not to write any individual spec — it is to keep the *fleet* coherent: shared infrastructure works, shared invariants hold, cross-team failures stay scoped, and the framework's discipline does not erode as the number of agents grows from one to fifty to a hundred.

Single-system governance — the four layers in [Proportional Governance](01-governance.md), the per-system Discipline-Health Audit, the per-spec review template — was designed for the team that owns the system. None of it scales linearly when ten teams are building against shared MCP servers, shared model providers, shared safety classifiers, and shared cost budgets. A platform team that runs ten independent instantiations of the per-system discipline is doing ten times the work of one team and producing ten times the duplicated artifacts; a platform team that runs only one centralized instantiation produces governance theater that tenant teams route around.

The structural question of this chapter: *what does governance look like when the unit of governance is the fleet, not the system?*

The answer is not a sixth activity or a new archetype. The five activities still apply per system; the seven failure categories still apply per incident; the spec template still applies per agent. What changes is the *scope* of certain governance moves — the constraint library, the oversight calendar, the telemetry partitioning, the failure-locus diagnosis — when many systems share infrastructure and tenant-level invariants need to hold across the fleet.

This chapter assumes the rest of Part 6 (the per-system Operations chapters: [Governance](01-governance.md), [Cost and Latency](02-cost-and-latency.md), [Telemetry](04-production-telemetry.md), [Adoption Playbook](05-adoption-playbook.md)). It is most useful for **platform teams**, **central architecture functions**, and **CIO/CTO-tier owners of internal AI infrastructure** — not for tenant teams operating a single agent, who can mostly stay in the per-system Operations chapters.

---

## The Problem

Three failure modes recur in fleets that try to extend single-system governance by repetition.

**1. Constraint duplication and drift.** Team A discovers that an indirect prompt-injection vector can exfiltrate session tokens through a particular tool. They add an invariant to their spec and a Cat 3 entry to their constraint library. Six weeks later Team B hits the same vector, having not seen Team A's discovery. They add the same constraint, slightly differently worded. By month six the fleet has twelve near-identical NOT-authorized clauses, three of which have drifted in meaning, and no one knows which clause is the canonical version. The fleet is *less* safe than a single shared constraint library would make it, because the version of the constraint that catches the attack lives in three teams' specs out of twelve.

**2. Cross-tenant blast radius.** A failure in Team A's agent — a Cat 4 oversight gap that lets the agent over-act — corrupts shared state in the platform's vector store or generates an unbounded billing event against the platform's account. The blast radius of Team A's incident extends to Team B, who has not changed anything but now finds their agent reading from a corrupted index, and to the platform team, who absorbs the cost overrun. The single-system blast-radius pattern, where the agent's authorization boundary is the unit of containment, doesn't capture this: the boundary that mattered was *between* tenants, not *within* one tenant's authorization scope.

**3. Platform-tier failure locus.** The team-level closed loop says: *every failure produces a structural change to the spec or the manifest or a CI guard or the framework version*. At fleet scale, certain failure patterns recur across many teams with the same root cause — typically platform-level. A shared MCP server has a permission-checking bug; a shared system-prompt template has a vulnerability; a model upgrade introduces a regression that affects every Synthesizer in the fleet simultaneously. The per-team closed loop produces twelve correct but uncoordinated spec amendments when the right fix is one platform-level change. The fix-locus framing breaks down because the *fix locus* is "the platform," not "any one team's spec."

A successful fleet governance regime addresses all three. It does so by adding four structural moves to the per-system discipline, not by replacing the per-system discipline.

---

## Forces

- **Per-tenant autonomy vs. platform-level coherence.** Tenant teams need authorial autonomy over their own specs — they own the problem space, they own the on-call. Platform teams need fleet-level coherence — they own the shared infrastructure, they absorb shared failures. Heavy platform mandates create the same avoidance behavior heavy governance creates anywhere. Heavy per-tenant autonomy produces drift.
- **Constraint inheritance vs. constraint duplication.** Shared invariants should be authored once and inherited; team-specific invariants should stay local. The mechanism that distinguishes them has to be visible in the spec, or teams cannot tell which clauses they own and which they inherit.
- **Centralized telemetry vs. tenant privacy.** The platform team needs cross-tenant telemetry to diagnose fleet-wide patterns. Tenant teams need their telemetry partitioned so a debugging session does not leak their domain context to other tenants or to the platform team's general audit dashboards.
- **Standard oversight cadence vs. per-tenant risk profile.** A standard oversight calendar applies uniformly to the fleet. But Team A's compliance agent has different risk than Team B's docs-search agent, and applying the same cadence either over-controls Team B or under-controls Team A.
- **Platform-tier fix vs. distributed-spec fix.** When a failure has a platform-level root cause, the fix locus is centralized — but the platform team needs the tenant teams' visibility to diagnose it, and the tenant teams need to know whether they should amend their specs in the meantime or wait for the platform fix.

---

## The Solution

Fleet governance is the per-system discipline plus four structural moves: a *constraint inheritance hierarchy*, a *cross-tenant isolation contract*, a *fleet-partitioned telemetry layer*, and a *platform-tier failure-locus rule*. Each move is small; together they make the per-system discipline composable across many systems.

### Move 1: Constraint inheritance hierarchy

The single most leveraged fleet move is to formalize a **shared constraint library** that every tenant spec inherits from. The library has three tiers:

- **Tier 1 — Fleet-wide invariants.** Clauses that hold for every agent in the fleet, regardless of tenant team or archetype. Examples: *no exfiltration of session tokens*; *all tool calls audited to the central log*; *cost ceiling per call enforced by platform middleware*; *system-prompt extraction defenses enabled by default*. Authored and maintained by the platform team; tenant teams cannot disable them but can request additions through the platform-team backlog.
- **Tier 2 — Archetype-wide invariants.** Clauses that hold for every agent of a given archetype across the fleet. Examples: *every Executor must declare its NOT-authorized scope in §3*; *every Guardian must emit a structured veto reason*; *every Orchestrator must declare its component archetypes per the Composition Declaration*. Authored once per archetype; inherited automatically when a spec declares its archetype in §4.
- **Tier 3 — Per-tenant additions.** Clauses specific to one tenant's domain. Authored and owned by the tenant team. Free to add; cannot weaken Tier 1 or Tier 2.

The spec template's §6 (Invariants), §7 (Non-Functional Constraints), and §8 (Authorization Boundary) each gain an explicit *inherited from* annotation per clause:

```markdown
## §6 Invariants

- (Fleet, T1) No exfiltration of session tokens across tool calls.
- (Fleet, T1) All tool calls audited to the central log within 5s of the call.
- (Archetype: Executor, T2) NOT-authorized scope declared in §3 is enforced
  by the tool-manifest layer, not only the spec.
- (Tenant, T3) For ride-share fraud detection: no agent action may resolve
  before the rider has had at least one charged trip in the last 90 days.
```

The hierarchy is *visible* in every spec because the spec is the audit surface. The platform team's job is to keep Tier 1 and Tier 2 small, sharp, and load-bearing. A Tier 1 clause that exists "because someone proposed it" rather than "because a real cross-tenant failure demonstrated the need" is constraint inflation — the fleet equivalent of governance theater.

The constraint library lives in a single platform-owned repository (typically `constraints/` in the platform's monorepo or a dedicated `intent-constraints` repo). Tenant specs reference it by version. When a Tier 1 clause changes, every spec inheriting it gets an automatic *spec-amendment-required* signal at its next CI build.

### Move 2: Cross-tenant isolation contract

A fleet sharing infrastructure has cross-tenant blast-radius surfaces the single-system pattern doesn't address. The platform layer carries a **cross-tenant isolation contract** that names, for each shared resource, what guarantees it makes across tenants:

| Shared resource | Cross-tenant guarantee | Mechanism |
|---|---|---|
| Vector store | Per-tenant namespace isolation; no cross-tenant retrieval | Per-tenant collection prefix; query filter enforced at SDK layer |
| MCP server fleet | Per-tenant capability scope; auth tokens never crossed | Per-tenant OAuth scope; server rejects calls without matching scope |
| Model provider account | Per-tenant cost attribution; budget caps enforced before model call | Per-tenant API key wrapper; per-call cost check against tenant's budget |
| Audit log | Per-tenant query partition; aggregate cross-tenant only for platform team | Tenant ID indexed on every record; query layer enforces partition |
| Skill files / skill registry | Tenant-published skills isolated from other tenants by default | Skill manifest declares visibility (private / cross-tenant-readable / fleet-wide) |

The contract is the platform team's deliverable. Tenants can read it but cannot weaken it; tenants can request additions if they discover a cross-tenant surface the contract missed. The contract is versioned like the constraint library; when a clause changes, every tenant gets a notification and the platform team carries the cost of migration.

Cross-tenant isolation failures are typically **Cat 4 (Oversight) at the platform tier** — the gate that should have prevented one tenant's call from affecting another tenant's state failed to fire. The fix locus is the platform middleware, not any individual spec; *but every affected tenant spec should declare the cross-tenant invariant it depends on* (in Tier 2 of the inheritance hierarchy), so when the platform middleware fails, the audit log can attribute the failure precisely.

### Move 3: Fleet-partitioned telemetry layer

The single-system telemetry pattern in [Production Telemetry](04-production-telemetry.md) assumes one team reads one stream. A fleet needs telemetry that is **simultaneously per-tenant-private and platform-team-aggregable** — a structural commitment, not an analytics feature.

The pattern:

- **Every span carries a tenant ID** as a first-class attribute (OpenTelemetry resource attribute is the right home).
- **Every query layer enforces the partition**: tenant queries restrict to their own ID; platform queries can aggregate across tenants but cannot reveal another tenant's domain context (the prompt body, the tool input/output payloads) without explicit cross-tenant audit authorization.
- **Two telemetry products are kept distinct**: the per-tenant operational dashboard (the tenant team owns this; covers spec-gap rate, first-pass validation, cost per correct outcome, oversight load for *their* agents) and the platform fleet dashboard (the platform team owns this; covers cross-tenant patterns like model upgrade impact, MCP server error rates, fleet-wide cost trends, fleet-wide Cat distribution).
- **The four signal metrics from [Validate](../validate/06-metrics.md) split into two views**: the per-tenant view (each team's own metrics) and the fleet view (distribution of each metric across tenants). The fleet view surfaces patterns no single tenant sees — *e.g., a 30% rise in spec-gap rate across 8 of 12 tenants over 14 days suggests a platform-tier change*.
- **Audit log retention is per-tenant**, but **incident-replay capability is fleet-wide**: the platform team can request access to a specific span tree across tenants when investigating a cross-tenant incident, with the request logged and visible to the affected tenant teams.

The partition is enforced at the platform layer (SDK, query layer, dashboard ACLs) because tenant teams cannot reliably enforce isolation in their own client code. The platform team's deliverable is the *substrate* that makes isolation default; tenant teams' deliverable is the per-tenant telemetry their dashboards consume.

### Move 4: Platform-tier failure-locus rule

The per-system fix-locus rule says: *every failure produces a structural change at the artifact named by the diagnosed Cat*. The fleet extension adds one rule:

> **If the same Cat recurs across three or more tenants within a 14-day window with the same root cause, the fix locus moves up to the platform tier, regardless of where the incident first surfaced.**

The rule prevents the failure mode where twelve teams each amend their spec for the same underlying bug. Once the third recurrence is detected (typically by the platform fleet dashboard surfacing the pattern), an *incident is opened against the platform tier* — a constraint library amendment, an MCP server patch, a CI guard update, a system-prompt template revision, or a framework version bump.

Tenant teams continue to operate within their own closed loop in the meantime; once the platform fix lands, the constraint library version bumps and tenant specs that inherit the affected clause get the *spec-amendment-required* signal at next CI. The platform team owns the migration cost.

The rule's threshold (three tenants in 14 days) is opinionated. It is calibrated against the failure mode it prevents: a lower threshold (one or two) generates too many false platform escalations; a higher threshold (five or more) lets fleet-wide patterns recur long enough to do real damage. Teams should adapt the threshold to their fleet's size and risk profile — but they should commit to *some* threshold, in writing, and the platform team should be accountable to it.

### Composing the four moves

The four moves compose with the per-system discipline; they do not replace it. A tenant team running an agent in the fleet:

1. Runs the [Intent Design Session](../foundations/07-intent-design-session.md) for their agent.
2. Writes a spec using the canonical template, with §6/§7/§8 clauses annotated for which tier they inherit from (Move 1).
3. Declares which shared platform resources their agent depends on, picking up the corresponding cross-tenant invariants from the isolation contract (Move 2).
4. Emits telemetry with the platform's tenant ID attribute; consumes the per-tenant dashboard for the four signal metrics; the platform team consumes the fleet view (Move 3).
5. Runs the per-system closed loop on incidents; escalates to platform-tier when the recurrence threshold is crossed (Move 4).

A platform team operating the fleet:

1. Owns and maintains the constraint library (Tier 1 + Tier 2), the cross-tenant isolation contract, the telemetry substrate, and the platform-tier incident response.
2. Runs the Adoption Playbook from [operate/05](05-adoption-playbook.md) at the *fleet* level — the first tenant team's pilot demonstrates the platform; subsequent tenants onboard against an established platform rather than a new one. The champion-led-rollout cost amortizes across the fleet.
3. Runs a quarterly *fleet* Discipline-Health Audit alongside the per-system audits — checking whether the constraint library is staying small, whether the isolation contract is still complete, whether the telemetry partition is holding, whether the platform-tier failure-locus rule is firing correctly.

### When the fleet model isn't right yet

Fleet governance is the right shape when:

- Multiple tenant teams (≥3) operate agents against shared platform infrastructure;
- At least one cross-tenant resource exists (shared model account, shared MCP server, shared vector store, shared audit log);
- Spec evolution at one tenant has surfaced an invariant that should hold for others, and the team is about to copy it.

It is *not* the right shape when:

- One team operates one agent, even at high scale. The per-system discipline is sufficient; adding fleet machinery is governance theater.
- Multiple teams operate agents but on fully separate stacks (no shared platform). The constraint library is still useful as an organizational artifact; the other three moves are over-investment.
- The platform team does not yet have one tenant team's pilot working well. Build one well-functioning tenant on the platform first; do not roll fleet machinery before any tenant has demonstrated success.

The cost of premature fleet governance is the same as the cost of premature any-governance — the framework's *form* gets adopted (constraint library, isolation contract, partitioned telemetry, escalation rule) without its *discipline* (the cross-tenant patterns that justify those structures). The result is platform theater at fleet scale.

---

## Therefore

**Fleet governance is the per-system Architecture of Intent plus four structural moves — constraint inheritance, cross-tenant isolation, partitioned telemetry, and a platform-tier failure-locus rule — owned by the platform team and inherited by tenant specs.** The five activities stay five. The seven failure categories stay seven. What changes is the *scope* of certain artifacts (the constraint library, the audit log, the failure-locus rule), so single-system discipline composes across many systems without producing twelve drifting copies of the same invariant.

---

## Resulting Context

A platform team operating the fleet now has:

- A versioned constraint library (Tier 1 + Tier 2) authored once and inherited by every tenant spec, visible in every spec's §6/§7/§8.
- A cross-tenant isolation contract enumerating every shared resource and its per-tenant guarantee.
- A telemetry substrate that is per-tenant-private at the dashboard layer and platform-team-aggregable at the fleet-view layer, with the four signal metrics split into per-tenant and fleet views.
- A platform-tier failure-locus rule with an opinionated threshold (e.g., three tenants in 14 days) that prevents constraint duplication.
- A quarterly fleet Discipline-Health Audit alongside the per-system audits.

Tenant teams operating agents in the fleet retain authorial autonomy over their per-tenant specs, oversight cadences, and constraint additions; they inherit the fleet-wide invariants by reference rather than by copy. The framework's per-system discipline runs unchanged inside the fleet boundary.

---

## Connections

**Assumes:**

- [Proportional Governance](01-governance.md) — the per-system governance layers this chapter composes with at the fleet level.
- [Production Telemetry](04-production-telemetry.md) — the single-system telemetry pattern this chapter partitions across tenants.
- [Adoption Playbook](05-adoption-playbook.md) — the per-team adoption rhythm; fleet adoption is the playbook applied once per tenant against an established platform.
- [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — the spec sections (§6 Invariants, §7 Non-Functional Constraints, §8 Authorization Boundary) where the inheritance annotations land.
- [Cost and Latency Engineering](02-cost-and-latency.md) — the per-tenant cost attribution machinery that the cross-tenant isolation contract enforces.

**Enables:**

- A platform team can grow the tenant fleet from one to twelve to fifty without doing N times the per-system governance work.
- Cross-tenant failures get diagnosed at the platform tier rather than recurring across N tenants.
- The constraint library compounds across the fleet — the discovery one tenant team makes becomes a fleet-wide invariant within one constraint-library version bump.

**Cross-references:**

- The [framework's honest-scope statement](../introduction.md#honest-scope-what-this-book-is-and-what-it-isnt) named multi-tenant fleet governance as a gap through v2.3.x; v2.4.0 closes that gap with this chapter.
- The [Pattern Justification Map](../appendices/pattern-index.md#pattern-justification-map) treats the four moves as fleet-scope amendments to existing spec sections, not as new pattern categories — the constraint inheritance hierarchy operationalizes §6/§7/§8 at fleet scale; the isolation contract is a §8 extension at the platform tier; the partitioned telemetry is a §12 extension at the platform tier; the platform-tier failure-locus rule is an extension of the closed-loop discipline in [evolve/01](../evolve/01-closed-loop.md).

---

## References

- The four moves are synthesized from common practice across cloud-platform multi-tenancy literature; nothing in this chapter is original infrastructure design. The contribution is the *spec-side* commitment — that every spec in the fleet declares its inheritance, its isolation dependencies, its telemetry tenancy, and its escalation threshold *in writing*, so the audit surface stays coherent as the fleet grows.
- Related single-tenant patterns: [Blast Radius Containment](../patterns/safety/blast-radius-containment.md), [Sensitive Data Boundary](../patterns/safety/sensitive-data-boundary.md), [Session Isolation](../patterns/state/session-isolation.md), [Agent Registry](../patterns/state/agent-registry.md).
- The framework's commitment to *structural fixes live in spec / manifest / CI / platform — never only in the prompt* extends naturally to fleet scale: the *platform* slot in that list is where many fleet-scale fixes land. This chapter is the explicit treatment.
