# Architectural Decision Records

**Part 2 — Specify**

---

> *"The spec records what the system does. The ADR records why the team decided it should do that. They are different artifacts with different lifetimes. Conflating them produces specs that are too long and decisions that are forgotten."*

---

## Context

You have a spec, written against the canonical template. You have a team. Decisions are made — about which service to call, which library to standardize on, which architectural pattern to apply, which trade-off to accept. Some of those decisions become invariants in the spec. Most of them don't, but they still need to be recorded.

This chapter introduces ADRs (Architectural Decision Records) as a first-class durable artifact alongside the spec, the spec gap log, and the constraint library. ADRs are well-established in software engineering — Michael Nygard's 2011 essay is the canonical reference — and they have become a load-bearing artifact in modern AI-augmented delivery frameworks like Microsoft's [DevSquad Copilot](https://github.com/microsoft/devsquad-copilot).

The earlier versions of this book did not treat ADRs explicitly. That was an omission. This chapter closes it.

---

## The Problem

Three failure modes recur in teams that have specs but not ADRs:

**1. Specs become rationale dumps.** A spec that says "the system uses Authentication Service A" leaves the next reader (or the next agent) wondering *why*. So the spec author adds a paragraph: "We chose Service A because it supports SAML and Service B requires LDAP; the security review in Q1 mandated SAML; the cost differential was acceptable; the migration risk from B to A was deemed lower than the inverse." The spec is now half-rationale. A year later, the rationale is stale (the security review is forgotten; SAML may have been deprecated), but the spec still says it. The decision and its constraint have been welded together in a way that makes neither maintainable.

**2. Decisions are forgotten.** A team makes a careful decision in a meeting. The decision is captured in the meeting notes. Three months later, an engineer joins and asks "why are we using Service A?" Nobody remembers the rationale. The decision gets re-litigated, often badly, often arriving at a different answer than the original.

**3. ADRs are written but disconnected.** A team adopts the ADR practice but never connects ADRs to specs. The ADRs live in `docs/adr/`; the specs live in `specs/`; agents read the specs and not the ADRs; the rationale is documented but ineffectual.

The discipline this chapter teaches is: **ADRs and specs are different artifacts with explicit relationships. Both are durable. Each has a job. Neither can do the other's job.**

---

## Forces

- **Decision durability vs. spec readability.** Specs are read more often than ADRs and need to be tight. ADRs are read less often but need to be discoverable when relevant. Bundling them serves neither.
- **Decision permanence vs. spec evolution.** A spec evolves with every gap learning; an ADR rarely changes after it's written. Different lifetime profiles need different artifacts.
- **Spec authority vs. team consensus.** The spec is authoritative for the agent at runtime; the ADR is the team's recorded reasoning. The agent runs on the spec, not the ADR.
- **Local decision vs. organizational decision.** Some ADRs apply only to one system; some apply to a class of systems and become repertoire-level. The artifact format must accommodate both.

---

## The Solution

### What an ADR is

An ADR records, in a stable format, **a decision the team made, the context that produced it, the alternatives considered, and the consequences accepted.**

A canonical ADR has six sections (adapted from Nygard's original):

```
ADR-NNN: Short title

Status: Proposed | Accepted | Superseded by ADR-NNN | Deprecated

Context
  What the team faced when this decision was needed.
  What constraints were in play.
  What information was available (and what wasn't).

Decision
  What the team chose. One paragraph, declarative.

Alternatives Considered
  What else was on the table.
  Why each was rejected.

Consequences
  What this decision enables.
  What this decision constrains.
  What new problems this creates.

Spec Mapping
  Which spec section(s) this decision touches.
  Which invariants it produces (if any).
```

The "Spec Mapping" section is the book's addition to the standard ADR format. It is the explicit bridge between an architectural decision and the spec sections it constrains.

---

### When to write an ADR

Three triggers:

**1. A decision affects how an agent (or a class of agents) is authorized to act.** "The Authentication Service handles all session validation." "All payment-related agents go through the Payment Guardian." "Coding agents may install only from the corporate registry." Each of these is an ADR-worthy decision because it shapes the spec's Authorization Boundary or Tool Manifest.

**2. A decision that future engineers will not understand without context.** "We use HTTP polling instead of WebSockets." "We never compute aggregate refund amounts in the agent — we always call the billing service." Each is the kind of decision an engineer joining the team would otherwise re-litigate.

**3. A decision that was contested and the team picked a side.** Decisions that came after debate are decisions worth recording. Decisions that were obvious to everyone usually don't need an ADR.

What does NOT need an ADR: routine implementation choices (variable naming, file organization), product decisions that don't constrain architecture, decisions that the spec already captures completely (the spec's Authorization Boundary already says everything that needs to be said about the decision).

---

### Where ADRs and specs touch

ADRs are about *why*. Specs are about *what*. The mapping rules:

| ADR records a decision about... | ...which produces a spec change in: |
|---|---|
| Architecture choice (library, service, pattern) | Section 6 (Invariants) — "the system uses X, may not use Y" |
| Authorization decision (what the agent may access) | Section 8 (Authorization Boundary) |
| Capability decision (what tools exist, what's allowlisted) | Section 7 (Tool Manifest) |
| Risk-tier decision (oversight intensity) | Section 4 (Archetype declaration's oversight model) |
| Process decision (review cadence, escalation policy) | Section 12 (Validation Checklist) |
| Failure-handling decision (what to do on Cat N failure) | Section 11 (Agent Execution Instructions); also the spec gap log's resolution column |

The mapping table above is the rule for ADRs that *do* have spec consequences. Some ADRs don't — they record decisions that were made but never had to be enforced at the spec layer (e.g., "we considered switching to a different model provider and decided not to"). Those ADRs live in the team's ADR archive and don't generate spec changes. They still have institutional memory value.

---

### Worked example: an ADR for the order-service coding agent

The team described in [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) faced the typosquat decision: should the dependency-installation tool refuse packages within Levenshtein distance 2 of allowlisted packages? The decision became ADR-007:

```
ADR-007: Typosquat protection at the tool layer

Status: Accepted (2026-04-22)

Context
  Q1 2026 red-team Battery 1 found that the agent could be coaxed
  into installing typosquatted packages by an issue body that
  named a misspelled but plausible-looking package. The agent's
  prompt-level instruction "use only allowlisted packages" did
  not catch this — the model selected the misspelled name as
  plausible, and the package.install tool's check was a literal
  allowlist match (exact string), so the misspelled name was
  rejected as not-allowlisted but the agent then fell back to
  shell.exec("npm install <misspelled>") which had no allowlist
  enforcement.

Decision
  Implement Levenshtein-distance-2 typosquat protection at the
  package.install tool layer (refuses any name within edit
  distance 2 of an allowlisted name). Concurrently remove the
  general-purpose shell.exec from the tool manifest; replace
  with specific test.run, typecheck.run, lint.run actions that
  cannot be used to install packages.

Alternatives Considered
  - Levenshtein distance 1 only: too narrow; misses common
    typosquats with 2-character substitutions.
  - Token-similarity (token2vec): catches more but produces
    false positives for legitimate packages with similar names
    in unrelated namespaces. Not worth the false-positive cost.
  - Manual allowlist of known-typosquat names: doesn't scale;
    new typosquats appear faster than maintenance can keep up.

Consequences
  Enables: structural typosquat protection that is independent
  of the agent's prompt-level instructions. Closes the OWASP
  LLM03 supply-chain attack vector for this agent.

  Constrains: legitimate packages within Levenshtein 2 of any
  allowlisted package cannot be installed. As of 2026-04, this
  affects 4 known cases in the team's ecosystem; manual
  exceptions are recorded in allowlist.json's exceptions array.

  New problems: the allowlist.json exceptions array is a new
  surface that needs review. Added to security team's quarterly
  review cadence.

Spec Mapping
  Order-Service Coding Agent spec v1.3:
    §3.4 (Dependency management) — explicit Levenshtein-2 clause
    §5 C3 (Dependency allowlist enforcement) — programmatic check
    §7 (Tool Manifest) — package.install enforced_constraints
    §7 (Tool Manifest) — shell.exec removed; test.run, typecheck.run,
                        lint.run as replacements
    §6 Invariant 2 — dependency closure is allowlist-bounded
```

The decision is recorded. The spec is the runtime control surface. The ADR is the answer to "why does the spec say this?" — durable, discoverable, and decoupled from the spec's per-version evolution.

---

### ADR governance

A team running ADRs needs a few light governance practices:

- **One file per ADR**, named `ADR-NNN-short-title.md`, in a known location (typically `docs/adr/` in the team's repository or platform).
- **Sequential numbering** that never restarts. ADRs are immutable once Accepted; superseded ADRs are kept in place with status changed and a forward-link to the superseding ADR.
- **A reviewer who is not the author**. ADRs are decisions; one author and one reviewer is the minimum for a decision to count as a team decision.
- **Periodic review** (quarterly or per-release) to identify ADRs that should be marked Superseded or Deprecated. Stale ADRs that contradict current reality are worse than no ADRs.

ADRs do not need a heavyweight governance process. They are deliberately lightweight artifacts. Adding ceremony defeats the purpose.

---

### What ADRs are NOT

Three anti-patterns to avoid:

**1. ADRs as design documents.** An ADR is not the place to design a system. It records a decision that was made, with enough context to understand it. If you find yourself writing an ADR with multi-page architecture diagrams, you are designing in the wrong artifact. Design lives in design docs (or in the spec itself, depending on team norms); ADRs record the discrete decisions that fall out of design work.

**2. ADRs as documentation of obvious choices.** An ADR for "we use TypeScript" is theater unless TypeScript was contested at the time the decision was made. ADRs cover decisions that *could have gone differently*. A decision that nobody considered alternatives for is not an ADR-worthy decision; it's just a fact.

**3. ADRs that the spec ignores.** An ADR that the spec doesn't reflect is institutional memory only — useful, but not load-bearing. The mapping table is the rule. If the ADR is supposed to constrain agent behavior, the spec must encode it. If the spec doesn't, either the spec is incomplete or the ADR was advisory rather than binding; clarify which.

---

### Connection to the rest of the framework

ADRs interact with several other book artifacts:

- **Spec Gap Log** ([The Living Spec](06-living-specs.md)). When a gap log entry surfaces a learning that requires an architectural decision, the gap log entry should reference (or trigger the creation of) an ADR. Not every gap is ADR-worthy; the test is "does this require team-level decision-making, or just a spec-section update?"
- **Constraint Library** ([Constraint Library Template](../repertoires/templates/constraint-library.md)). Constraints inherited across multiple specs may have an originating ADR. The constraint library entry should reference the ADR that established it.
- **Composing Archetypes** ([Composing Archetypes](../frame/05-composing-archetypes.md)). Spec-conflict resolution rules are ADR-worthy at the team or organization level — they say how the team handles a class of conflicts, not just one instance.
- **DevSquad Mapping** ([Mapping the Framework to the DevSquad 8-Phase Cadence](../evolve/12-devsquad-mapping.md)). DevSquad's Phase 3 is "Plan with ADRs"; that phase is where most ADRs are produced.

---

## Resulting Context

After applying this pattern:

- **Specs are tight.** Rationale lives in ADRs, not in the spec body. Specs say *what*; ADRs say *why*.
- **Decisions are durable.** Three months later, six months later, three years later, the decision and its context are still discoverable.
- **Specs and ADRs are explicitly related.** The Spec Mapping section of every ADR names the spec sections it constrains. The team can trace from any spec clause back to the ADR that established it.
- **New engineers can self-onboard.** ADRs answer the questions a new engineer asks ("why do we do it this way?") without re-litigating settled decisions.

---

## Therefore

> **ADRs and specs are different artifacts. The spec records what the system does and is the control surface the agent runs against. The ADR records why the team decided the system should do it that way and is institutional memory for the next reader. Use the canonical ADR format (Nygard's, plus a Spec Mapping section). Write an ADR when a decision affects authorization, capability, risk tier, or process — or when a future engineer would not understand the decision without the rationale. Do not bundle rationale into specs; do not write ADRs that the spec doesn't reflect; do not write ADRs for obvious choices. Both artifacts are durable. Each has a job. Neither can do the other's.**

---

## References

- Nygard, M. (2011). *Documenting Architecture Decisions.* cognitect.com/blog/2011/11/15/documenting-architecture-decisions. — The original essay defining the ADR format. The canonical reference.
- ADR Tools and Templates. (ongoing). adr.github.io. — Community resources for ADR format variations.
- Microsoft. (2026). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot. — ADRs as a first-class artifact in modern AI-augmented delivery; DevSquad's Phase 3 is centered on ADR production.
- Fowler, M. (2002). *Patterns of Enterprise Application Architecture.* — Foundational discipline of recording architectural patterns and the decisions behind them.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](07-canonical-spec-template.md) — ADRs map onto specific spec sections per the table above
- [The Living Spec](06-living-specs.md) — gap log entries can trigger ADRs for team-level decisions

**This pattern enables:**
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../evolve/12-devsquad-mapping.md) — DevSquad Phase 3 is where ADRs live in that cadence
- [Co-adoption with DevSquad](../evolve/13-co-adoption-with-devsquad.md) — the bridge chapter for teams running both frameworks
- [Composing Archetypes](../frame/05-composing-archetypes.md) — system-level spec-conflict resolution rules are typically ADR-worthy

---
