# Adoption Playbook

**Part 5 — Evolve & Operate**

---

> *"The framework that adopts cleanly is the framework that survived adoption. Most don't. The ones that do follow a recognizable pattern: small scope, fast feedback, the discipline applied to one thing before it's applied to many."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 5 — Evolve & Operate**. The Adoption Playbook is what keeps the [closed loop](../evolve/01-closed-loop.md) going as the team grows and as the framework spreads to other teams. Cross-team adoption is itself the closed loop at organizational scale — the coding-pipeline and docs-qa Evolve scenarios both demonstrate the pattern, with the team that explains the framework to others deepening its own discipline through the explanation.*

---

## Context

You have read the framework — archetypes, spec template, oversight models, evals, telemetry, the diagnostic protocol. You think it would help your team. The remaining question is *operational*: how do you actually introduce this practice without (a) burning credibility through over-investment, (b) producing specs nobody reads, or (c) being the person who slowed the team down by demanding governance before the first agent shipped?

This chapter is the chapter the rest of the book leaves implicit. It is not an org-redesign manifesto — the book deliberately cut those. It is a short, opinionated guide to introducing SDD discipline into an existing team without producing the predictable failures.

If you are starting from scratch — a new team, a new product, agent-native from day one — much of this chapter still applies, but the friction is lower. This chapter is most useful for the harder case: introducing the framework to a team that has been shipping software for years and is now adding agents.

---

## The Problem

Three adoption failure modes recur, and they account for most cases where teams that *should* benefit from this framework end up not.

**1. Big-bang rollout.** A staff engineer reads the framework, finds it convincing, writes a 30-page proposal to adopt it across all teams, all systems, all agent deployments, retrofit the existing systems with specs and archetypes, mandate spec review for all agent-touching code. The proposal lands in a leadership meeting. It is correctly judged as too big. It dies. The framework is now associated with "the proposal that didn't happen" and adoption is harder later than it would have been if the engineer had quietly applied it to one project.

**2. Spec theater.** A team adopts the canonical spec template for a new agent. The spec is written. The agent ships. The spec is never updated. A year later, the spec describes a system that no longer exists; the team has stopped reading it; new engineers don't know where the "real" spec lives. The framework's *form* was adopted — sections, templates, archetype declarations — without its *discipline* — the gap log, the spec-first response to failure, the constraint library that compounds learning. Theater specs are worse than no specs because they create the false impression that the discipline is in place.

**3. Governance over-investment.** A team takes the framework seriously and goes deep on governance: spec review boards, quarterly archetype audits, formal oversight committees, multi-stakeholder approval for new agents. The governance overhead becomes the limiting factor on the team's velocity. Senior engineers who could be writing specs are sitting in archetype-classification meetings. The team's leadership concludes — correctly, given the visible cost — that the framework slows them down. The discipline gets stripped back to the minimum, often beyond it.

A successful adoption avoids all three. The pattern that consistently works is *small scope, demonstrable benefit, then expand* — applied to a single agent with a single team and a narrow set of behaviors before it's expanded to the rest of the organization.

---

## Forces

- **Demonstration vs. mandate.** Frameworks introduced by mandate (top-down, all-at-once) face every team's resistance simultaneously and have no working examples to point at. Frameworks introduced by demonstration (one team's pilot succeeds, others adopt voluntarily) build credibility before they request bandwidth.
- **Discipline burden vs. immediate value.** Spec writing, gap logging, and archetype declarations have an upfront cost. The compounding benefits are real but delayed. If the first week of adoption is more cost than benefit, the team won't reach week four.
- **Standardization vs. local adaptation.** A framework rigidly applied is brittle. A framework freely interpreted is incoherent. The right adoption posture is rigid on the load-bearing parts (the spec template, the archetype categories, the diagnostic protocol) and flexible on everything else.
- **Champion bandwidth vs. organic adoption.** A single engineer who deeply understands the framework can shepherd one or two adoptions personally. Beyond that, the framework has to teach itself — through templates, examples, and the gap log culture — or it stops scaling.

---

## The Solution

### Week 1 — Pick one agent, one spec, one gap log

Adoption begins with a single agent. Not "an agent strategy." Not "a platform initiative." One agent, one team, one spec.

**The setup:**

- Pick an agent your team is about to build, or has just shipped, or is about to revise. Bias toward "about to build" — the spec is most valuable before code exists.
- Read [The Canonical Spec Template](../specify/07-canonical-spec-template.md) and write the spec. Allow yourself one to three days. The first spec is always slow.
- Walk the [Archetype Selection Tree](../frame/04-decision-tree.md). Declare the archetype in Section 4. Decide the oversight model.
- Set up a Spec Gap Log. A spreadsheet with the columns from [The Living Spec](../specify/06-living-specs.md) is sufficient for week 1. Tooling can come later.
- Ship the agent.

**What you are learning in week 1:**

- Whether the spec template fits your domain. (It will need adaptation. That's expected.)
- Where your existing implicit constraints live, and how much pain it is to make them explicit.
- Whether the archetype framework gives you a useful classification or feels forced. (If forced for one specific case, often the case is at a real boundary; if forced consistently, the framework may not fit your domain — see "When to retreat" below.)

What you are *not* doing in week 1: convincing other teams, writing process documents, building tooling, designing governance.

---

### Month 1 — One spec becomes a gap log becomes a constraint library entry

After week 1, the agent is running. Things will go wrong. The discipline that distinguishes a real adoption from spec theater is what you do when they go wrong:

- Each failure: walk the diagnostic protocol from [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md). Categorize. Identify the artifact to change.
- Each Cat 1 (Spec Failure): update the spec, log the gap. The log entry has to include *which spec section was affected* and *why intent review didn't catch it*.
- Each pattern that recurs: ask "is this a constraint that belongs in a constraint library, not just in this spec?" If yes, it goes in a shared place — a folder, a Notion page, a repo — that future specs can reference.

By month 1, you will have:
- A spec that has been revised three to ten times, each revision tied to a logged gap
- A small set of constraint-library entries — typically 3–8 — that are now reusable
- A working answer to the question "is the discipline producing benefit?"

If yes, expand. If no, retreat (see below).

---

### Quarter 1 — Second team adopts, voluntarily, by example

Adoption from one team to a second team is the test of whether the framework will scale in your organization. The pattern that consistently works:

- The first team's adoption is *visible* — the spec is open, the gap log is shared, the constraint library is referenced
- A second team has a similar agent project incoming
- The second team asks "can we use what you did?"
- The first team's spec, archetype declaration, and constraint library entries are *copied* — not by mandate, by request

If this pattern doesn't happen organically by quarter 1, the framework is not doing the work yet. Don't push it. The right next move is going deeper on the first team's adoption — better evals, more constraint-library entries, a worked postmortem — until the demonstrated benefit is unambiguous. Then re-test whether other teams ask.

---

### Year 1 — The constraint library is the asset

By the end of year 1, if adoption is working, the team's accumulated artifacts are:

- 5–20 specs, each tied to specific agents, all using the same template
- 30–100 constraint-library entries, organized by domain (PII, auth, data integrity, output formatting, dependency management, ...)
- A spec gap log with hundreds of entries showing the team's accumulated learning
- Two or three archetypes that have been refined or specialized for the team's domain
- Evals tied to the canonical spec template's Section 9 across all major agents

The constraint library is the asset that compounds. New agents inherit constraints they didn't have to discover. New engineers learn the team's accumulated wisdom by reading constraint entries. Failures that recur once are addressed; failures that recur a third time are themselves a Cat 1 spec failure of the *team's adoption discipline*, not of the original spec.

This is the steady state. From here, the work is maintenance, evolution, and selective deepening (a coding-agent program, a multi-agent system, a red-team protocol). The framework does not have an end-state where it is "fully adopted" — like any operational discipline, it is a practice, not a milestone.

---

### Who needs to be on board

The minimum coalition for a successful single-team adoption:

- **One staff or principal engineer** with the bandwidth to write the first spec and shepherd the first month. This person is the framework's interpreter for the team — translating the framework's language into the team's language.
- **The engineering manager** of the team, who needs to understand that the upfront cost is real and the benefit is delayed but compounding. They don't need to become a spec author themselves; they need to defend the discipline against pressure to skip it.
- **The product owner or PM**, who needs to know that "spec review" is a step that happens before implementation and may surface clarification requests.

Notable absences from this list: the CTO, the platform team, an org-wide governance committee, a security review board. None is needed for a single-team adoption. They become relevant when adoption expands to more teams, or when the team's domain has regulatory requirements that demand them. Don't seek their approval before week 1; you will be asking too early.

---

### Handling skeptics

Three forms of skepticism recur. Each has a productive response.

**"This is just bureaucracy."** The honest answer: it *can* be, if implemented as theater. The way to refute it is to show the gap log entry that prevented a recurring failure, or the constraint-library entry that the next agent inherited for free. Bureaucracy doesn't compound; this discipline does. The skeptic isn't wrong about the failure mode; they're wrong that you're walking into it.

**"We don't have time."** The honest answer: the upfront cost is real; the quarter-1 cost-per-correct-output should be measurably better than the pre-adoption baseline. Until you can show that, you're asking the team to take the discipline on faith, which is a fair thing for a skeptic to refuse. The right response is to do the work, measure it, and bring data. If the data doesn't support the claim, the skeptic is right.

**"The framework feels academic."** The honest answer: large parts of it *are* drawn from older, more academic disciplines (requirements engineering, systems thinking, responsibility analysis). The framework is honest about this in its references appendix. The right response is to focus on the parts that are clearly operational — the canonical spec template, the diagnostic protocol, the four signal metrics — and let the academic parts stay in the background. Most teams don't need the philosophical material to do the work.

---

### Three anti-patterns to avoid

- **Mandating adoption before demonstrating benefit.** No team adopts a discipline they were told to adopt before they've seen it work. Pilot first; expand by request.
- **Writing the spec after the agent is built.** Specs written retrospectively are documentation, not control surfaces. They reduce to a description of whatever the code happens to do, which is what the team had before. The discipline is *spec first*, even if iteratively refined; specs added at the end miss the entire point.
- **Confusing the framework with its templates.** The canonical spec template is a tool; the discipline is a practice. A team that uses the templates without the gap log, the diagnostic protocol, and the constraint library culture is producing artifacts without the underlying mechanism that makes them valuable. Watch for "we adopted the template" without "we adopted the practice."

---

### When to retreat

Adoption sometimes fails for good reasons. The framework does not fit every team or every domain. The signs that retreat is the right move:

- After three months, the team's first-pass acceptance rate has not improved, the gap log is sparse or unused, and engineers describe the discipline as overhead rather than support
- The domain's failures are dominated by Category 6 (model-level) failures that no spec quality can address — the framework is offering tools that don't fit the problem
- The team's bandwidth to maintain the discipline at the threshold required is structurally absent (small team, high task heterogeneity, no role with explicit ownership)

In these cases, the productive move is to keep the *vocabulary* and the *diagnostic protocol* — these are useful even without the full discipline — and let the rest go. A team that says "we use the archetype categories and the failure taxonomy in our postmortems but we don't run the full SDD" is using the framework correctly for their context. There is no failure in selective adoption.

What is a failure: continuing to insist on the full discipline when the team is not getting the benefit, because a champion has a personal investment in the framework. That produces theater, then resentment, then nothing.

---

### Wiring into CI/CD

The disciplines this book describes — eval suite, spec gap log, red-team protocol, prompt-stability constraint — only become operational when they are wired into the team's existing CI/CD pipeline. The framework is process-agnostic about *which* CI/CD system; the wiring pattern is the same.

The three-tier model:

| Tier | What it does | What blocks a merge / deploy |
|---|---|---|
| **Hard gate** | Fails the build. Cannot be merged or deployed without resolution or explicit override with sign-off. | Level 1 unit asserts on tool I/O; Level 2 spec acceptance suite; secret-pattern hits in trace; broken internal links in spec |
| **Soft gate** | Fails the build but can be overridden with reviewer approval and a recorded reason. | Level 3 regression on the golden set (some regressions are acceptable trade-offs); cache-hit-rate target violation for new prompt; first-pass acceptance rate drop > 5pp on the eval canary |
| **Observe** | Does not block. Records the signal for trend monitoring. | Level 4 production sampling; cost-per-task drift; per-step latency drift; spec gap log entry rate |

Each artifact maps to a tier:

- **Eval suite (Level 1, 2)** — hard gate on PR, before merge. CI installs the agent harness, runs the spec acceptance suite, blocks merge on failure.
- **Eval suite (Level 3)** — soft gate on PR. Regression delta is reported in the PR; reviewer judges whether the regression is intentional.
- **Eval suite (Level 4)** — observe in production. Drift triggers an alert, not a deploy block.
- **Spec PR review** — hard gate. A spec change requires explicit sign-off by the spec owner. Use the [Intent Review Before Output Review](../validate/05-reviewing-intent.md) discipline as the review checklist.
- **Red-team finding (critical/high)** — hard gate. New deploys cannot proceed until the finding has a Spec Gap Log entry and an eval test case. Lower-severity findings are soft-gated against the next release window.
- **Cache hit rate** — soft gate on prompt PRs. Below 50% in the first 1,000 production calls after deploy → reviewer must justify or roll back. See [Cacheable Prompt Architecture](14-cacheable-prompt-architecture.md).
- **Cost per correct outcome** — observe. Drift is a [Four Signal Metrics](../validate/06-metrics.md) signal, not a deploy block.

**A minimal GitHub Actions / Azure DevOps sketch** (the same shape works in either):

```yaml
on: [pull_request]
jobs:
  spec-conformance:                   # HARD GATE
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/run-eval-level-1.sh    # tool I/O asserts
      - run: ./scripts/run-eval-level-2.sh    # spec acceptance suite
  regression:                          # SOFT GATE
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/run-eval-level-3.sh --report-only
      - run: ./scripts/post-regression-comment.sh
  red-team-delta:                      # HARD GATE on critical/high
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/red-team-delta.sh --severity-threshold high
```

The principle: **make the gate match the consequence**. A spec acceptance failure is non-negotiable; a 1pp regression on a niche golden-set scenario is a judgment call. Hard-gating everything produces deployment paralysis; soft-gating everything produces deployment theatre.

For teams on DevSquad cadence, the wiring slots into Phase 5 (TDD-first, hard gate on Level 1+2), Phase 7 (independent review, hard gate on red-team and spec PR), and Phase 8 (continuous refinement, observe layer feeding the next sprint's priorities). The [DevSquad Mapping](12-devsquad-mapping.md) chapter has the full phase-by-phase artifact table.

---

### Connection to the rest of the framework

The adoption playbook is the practical entry-point to the rest of the operational chapters:

- [Proportional Governance](04-governance.md) — what governance you actually need at the team's adoption stage
- [Intent Review Before Output Review](../validate/05-reviewing-intent.md) — the review practice that the adoption playbook calls for in week 1
- [Four Signal Metrics](../validate/06-metrics.md) — the metrics that tell you whether adoption is working at month 3
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — the eval discipline that the adoption playbook treats as the lifeline
- [Cost and Latency Engineering](09-cost-and-latency.md) — once adoption is working, this is where the team grows next
- [Production Telemetry](10-production-telemetry.md) — the observability layer that the gap log culture depends on for input

A team that has adopted the framework well will read these chapters not as an introduction but as a reference for the disciplines they are already running.

---

## Resulting Context

After applying this pattern:

- **Adoption begins small.** One agent, one team, one spec, one gap log. The team can demonstrate benefit in 30 days or accept that the framework doesn't fit.
- **The discipline compounds.** Each gap-log entry becomes a constraint library candidate; each constraint-library entry inherits to future specs; each new spec is faster and tighter than the one before.
- **Expansion is by request.** Other teams adopt because they have seen it work, not because they were told to. The framework's spread is voluntary and earned.
- **Retreat is allowed and named.** Teams whose domain doesn't fit the framework can keep the useful parts — vocabulary, diagnostic protocol — without the full discipline, and that is a successful outcome.

---

## Therefore

> **Adopt by demonstration, not mandate. Pick one agent, write one spec, log one set of gaps, build one set of constraint-library entries. Show the result before asking for organizational bandwidth. The discipline is the practice (gap log, diagnostic protocol, constraint library that compounds) — not the templates. Expand only when other teams ask. If after three months the framework is producing more cost than benefit, retreat to selective adoption: keep the vocabulary and the diagnostic protocol, let the rest go. The most common failure is not skipping the framework; it is adopting too much of it too fast.**

---

## References

- Kotter, J. P. (1996). *Leading Change.* Harvard Business Review Press. — The eight-step model for organizational change; specifically the "establish a sense of urgency / form a guiding coalition / generate short-term wins" sequence applied here as week-1 / month-1 / quarter-1.
- Westrum, R. (2004). *A typology of organisational cultures.* — Pathological / bureaucratic / generative organizational typology; predicts which adoption postures fit which org culture.
- Forsgren, N., Humble, J., Kim, G. (2018). *Accelerate.* — Empirical study of high-performing engineering organizations; the four key metrics framework that informed this book's signal-metric design and the iterative adoption pattern.
- Meadows, D. H. (2008). *Thinking in Systems.* Chelsea Green. — Leverage points for changing systems; the "small change with feedback" model that this chapter applies to organizational adoption.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The "start with the simplest pattern" guidance applied at the organizational level: start with the simplest adoption.
- Microsoft. (2026). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot. — A parallel framework that gives a more prescriptive 8-phase delivery cadence — *envisioning phase → Spec the next slice → Plan only what the current slice needs → Decompose that slice → Implement with TDD discipline → Learn in the open → Review in an independent context → Refine continuously* — compatible with this book's design vocabulary. A team that wants a turnkey process to wrap around this book's discipline could reasonably adopt DevSquad's cadence and ADR practice while applying the book's archetype framework, failure taxonomy, and security/eval/telemetry stacks. The two are complementary, not competitive.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — what week 1 produces
- [The Living Spec](../specify/06-living-specs.md) — the gap log discipline
- [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md) — the diagnostic protocol that month 1 depends on

**This pattern enables:**
- [Proportional Governance](04-governance.md) — at quarter 1+, governance becomes relevant
- [Four Signal Metrics](../validate/06-metrics.md) — at month 3, the metrics tell you whether adoption is working
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — the eval suite the team builds in month 2-3
- [Roles & Responsibilities (RACI) Card](../appendices/raci-card.md) — the canonical role-to-activity matrix the team grows into; introduce roles incrementally, not all at once
- The worked examples ([Customer Support](../examples/01-ai-customer-support/README.md), [Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md), [Coding Agent](../examples/03-coding-agent/README.md)) — what mature adoptions look like

---

*This concludes the operational chapters of Part 5. From here, the book becomes reference material — the worked examples, the pattern reference, and the appendices.*
