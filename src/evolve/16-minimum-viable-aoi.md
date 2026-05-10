# Minimum Viable Architecture of Intent

**Part 5 — Evolve**

---

> *"The smallest version of the discipline that still does work. Below this floor is not adoption; it is just deployment."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 5 — Evolve**. MVP-AoI is the [closed loop](../evolve/01-closed-loop.md) in compressed form for systems too small for the full discipline; the discipline travels down-scale, not just across-scale. The MVP applies when the system is small across all five of audience, stakes, cohesion, scale, and diagnosability, and graduates to the full discipline when any of the five graduation triggers fire.*

---

## Context

The full framework — a 3-to-4-hour [Intent Design Session](../theory/07-intent-design-session.md), a 12-section spec, four-dimension calibration, ~50 patterns to bind from, four oversight models, four signal metrics, a 12-anti-pattern audit, a 7×6 RACI — is calibrated for systems that *deserve* it. A non-trivial pilot, a team of more than one, a deployment with reversibility cost, a regulated domain.

Some systems do not deserve that treatment. A solo prototype. A weekend agent. An internal one-week pilot the team will throw away. A side-project assistant that talks only to its author. For these, the framework as written is more expensive than the system is worth, and applying it produces *spec theater* — the form of discipline without the function — which is worse than skipping the discipline honestly.

This chapter names the **floor** of the discipline. Below the floor is not Architecture of Intent; it is just deploying an agent and hoping. At the floor, you have the smallest set of artifacts that still does structural work. Above the floor, the rest of the book takes over.

This pattern assumes [What is the Architecture of Intent?](../introduction.md#what-is-the-architecture-of-intent), [The Intent Design Session](../theory/07-intent-design-session.md), and [Adoption Playbook](11-adoption-playbook.md).

---

## The Problem

Practitioners face a real choice when starting a small system:

- **Apply the full framework** (a few hours of IDS, a 12-section spec, a bound pattern set) and produce a spec longer than the system's code.
- **Skip the framework entirely** and accept that you have no shared mental model, no scoped boundary, no oversight commitment, no escalation trigger.
- **Apply something in between** — but "something in between" is unspecified, so different practitioners draw the line differently and the framework has no stance on what counts.

The third option is the honest one. The framework should have a stance. Without one, every practitioner who is not running a production pilot ends up either over-investing or under-investing, and the over-investors quietly stop applying the framework because it costs more than it returns.

The MVP names the floor explicitly. It is *not* a license to skip discipline. It is the discipline scaled to the smallest deployment for which discipline still earns its keep.

---

## Forces

- **Discipline cost vs. system worth.** A spec that takes longer to write than the agent takes to build is poorly calibrated. The MVP fits the discipline to the system, not the other way around.
- **Structural floor vs. nothing.** Below some floor, the agent has no shared model, no boundary, no oversight, no signal. That floor exists; the question is where.
- **Honest scaling vs. graduation drift.** A system that grows past the MVP threshold should graduate to the full discipline. Graduation cannot happen if no one ever names that the threshold was crossed.

---

## The Solution

### When to use the MVP

Apply the MVP when the system is small *across all five* of these dimensions simultaneously. If any one of them is borderline, treat the system as warranting the full framework.

| Dimension | MVP threshold |
|---|---|
| **Audience** | Just you, or a small known group; not external users. |
| **Stakes** | Reversible (R1–R2): mistakes are recoverable with effort, no irreversible state changes, no regulated data, no safety-critical control. |
| **Cohesion** | One person works on it. Nobody else has to read the spec to understand the system. |
| **Scale** | Bounded: a few dozen runs at most before you next reconsider. Not running continuously in production. |
| **Diagnosability** | Failures are visible to you in real time. You'd notice a problem within one or two runs, not one or two months. |

If your system meets all five, the MVP applies. If it crosses any threshold — production scale, external users, irreversible state, multi-person work, latent failures — graduate to the full framework before going further.

### The MVP itself

The MVP is one page of structured text. Five elements, each one or two sentences. No pattern format, no 12 sections, no calibration table. Just the floor.

```markdown
# [Project name] — MVP Architecture of Intent

**1. Archetype**
[One of: Advisor / Executor / Guardian / Synthesizer / Orchestrator]
[One sentence: what the system's primary act is, in plain language.]

**2. Scope**
*In scope:*
- [Behavior 1]
- [Behavior 2]
- [Behavior 3]

*Not in scope:*
- [Forbidden behavior 1 — the things you'd be embarrassed if it did]
- [Forbidden behavior 2]
- [Forbidden behavior 3]

**3. Oversight commitment**
[One of: I review every output before acting on it / I sample one in N
outputs / I let it run with rollback ready / I run it once and check.]
[One sentence: how the review actually happens.]

**4. One signal**
[One observable thing: what tells me this is working? "First-pass useful
rate," or "no embarrassing outputs in 20 runs," or "I stop reaching for
the manual fallback." Whatever your one observable is.]

**5. Escalation trigger**
[One condition: what makes me stop and reconsider? "Two failures in a
row," or "any output in the not-in-scope list," or "the system surprises
me twice." Whatever your tripwire is.]
```

That is the entire artifact. It fits on one printable page. It can be written in 15 minutes. It does the structural work.

### What the MVP guarantees

Even at the floor, four things are explicit:

1. **A shared mental model** — even if you are the only person, the archetype line is the model you can return to when the system surprises you.
2. **A boundary** — the *not in scope* list is the load-bearing element of the spec. Most "the agent did something I didn't want" failures are crossings of an unstated *not in scope* clause.
3. **An oversight commitment** — even if the commitment is "I review every output," it is *named*. Drift from named oversight to unnamed oversight is what produces the [oversight kabuki](15-anti-patterns.md) anti-pattern; an MVP names the commitment so drift is visible.
4. **A tripwire** — the escalation trigger is the equivalent of [§13 Spec Evolution Log](../specify/07-canonical-spec-template.md) at MVP scale. It is what tells you the system has crossed into needing more than the MVP.

### What the MVP deliberately omits

- **The 4-dimension calibration.** Implicit in the archetype choice. If you find yourself wanting to calibrate Agency or Autonomy explicitly, that is itself a graduation signal.
- **The bound pattern set.** Pick patterns reactively as failures surface. If you find yourself wanting to bind patterns proactively (because the failures are starting to compound), graduate.
- **The 4 oversight models.** Pick whatever fits — usually "I review every output" for the smallest systems. If the system grows past your ability to review every output, you have hit a graduation trigger.
- **The 4 signal metrics.** One signal is enough at this scale. If you start needing to break "is this working?" into multiple signals, graduate.
- **The Composition Declaration.** If your MVP is a composition (which is rare at this scale), you are probably already past the MVP threshold. Graduate.
- **The RACI.** It is just you. The roles collapse.
- **The Discipline-Health Audit.** Irrelevant for a system operated by one person who can hold the whole picture in their head.

The MVP omits these *deliberately*, not as a checklist of "things you don't have to do." The omission is what makes the MVP cheap enough to actually use. Adding any of them back without crossing a graduation threshold is a sign the practitioner is over-investing — which is *spec theater for the MVP itself*, the most-meta form of [the spec-theater anti-pattern](15-anti-patterns.md).

### Graduation triggers

The MVP graduates to the full framework when *any one* of these crosses:

| Trigger | The graduation signal |
|---|---|
| **Audience expands** | The system gains a second user. Anyone other than you depending on it. |
| **Stakes increase** | A new feature touches irreversible state, regulated data, or safety-critical control. Reversibility moves from R1–R2 to R3+. |
| **Cohesion breaks** | A second person starts working on the system. They need a spec to disagree against; the artifact in your head is no longer enough. |
| **Scale crosses ~100 runs/day** | Cost, latency, and oversight load become first-class concerns. The four signal metrics start mattering. |
| **A failure recurs and you cannot diagnose why** | The MVP's missing artifacts (the spec gap log, the four signal metrics, the failure taxonomy) start earning their keep. The same failure repeating is the strongest possible signal that you have crossed the floor. |

Graduation is not a one-time event; it is a transition that takes a session. Run the [Intent Design Session](../theory/07-intent-design-session.md) on the now-larger system, with the MVP as the starting artifact. Phase 5 (Bind Patterns) will be the most-changed; the patterns the MVP let you skip are now the patterns the spec needs.

### A worked example, end to end

A solo developer builds a personal note-cleanup agent that takes their daily journal entries and produces a tagged, indexed archive. It runs locally. Only they use it. The output goes only to their personal notes vault.

**MVP:**

```markdown
# Journal-Cleanup Agent — MVP AoI

**1. Archetype**
Synthesizer. Composes a tagged, indexed version of my journal entries
into a personal archive.

**2. Scope**
*In scope:*
- Add tags from a fixed allowlist of 20 tags
- Produce a one-line summary per entry
- Index by date and topic

*Not in scope:*
- Modify the original journal text
- Add tags outside the allowlist
- Send any content outside my local machine

**3. Oversight commitment**
I review the archive at the end of each week before letting it overwrite
last week's archive. The agent never auto-overwrites.

**4. One signal**
The weekly review takes me less than 10 minutes and I find no entries
needing manual correction.

**5. Escalation trigger**
Two consecutive weeks where I find any entry tagged outside the allowlist,
or any modification to the original journal text.
```

That is the entire spec. Took 15 minutes. The agent runs for a year on this. Then the developer's partner asks to use the agent for their journal too. *Audience expanded* — graduation trigger fires. The developer runs an IDS, produces a 12-section spec, picks an oversight model explicitly, instruments a metric. The MVP was the right shape for the year-of-solo-use; the IDS is the right shape for the now-shared deployment.

### What the MVP is not

**Not a license to skip discipline.** Practitioners who use the MVP without acknowledging the graduation triggers are running a system without a discipline. The framework's anti-pattern catalog applies in full to MVPs that should have graduated.

**Not a stable end-state for production systems.** A system in continuous production, with real users, that has stayed at the MVP shape for more than a quarter is almost certainly over-due for graduation. The MVP is a starting shape, not a permanent shape.

**Not a substitute for the [Miniature Pilot](../miniature-pilot.md).** The miniature pilot in the front of the book is a *worked example* of the *full canvas* applied to a small but production-bound system. The MVP here is a *deliberately compressed* discipline for systems below that production threshold. Both are correct shapes for their respective scopes.

---

## Resulting Context

After this pattern is in place:

- **The framework has an honest floor.** Practitioners can apply Architecture of Intent to systems too small for the full IDS without either over-investing or skipping the discipline altogether.
- **Graduation is visible.** The five graduation triggers tell a practitioner *when* to upgrade, not just *that* they should think about upgrading. The trigger is concrete; the response (run an IDS) is concrete.
- **Spec theater for small systems is named.** Adding the full 12-section spec to a system that meets all five MVP thresholds is over-investment, and the framework now says so explicitly.
- **The MVP is a starting shape, not an end state.** Practitioners are warned in advance that staying at the MVP for too long, on a system that has crossed a graduation threshold, is itself a discipline anti-pattern.

---

## Therefore

> **The Minimum Viable Architecture of Intent is one page of structured text — archetype, scope (in and out), oversight commitment, one signal, escalation trigger — written in 15 minutes, applicable to systems that are small across all five of audience, stakes, cohesion, scale, and diagnosability. It is the floor of the discipline, not a license to skip it. Five graduation triggers (audience expanding, stakes increasing, cohesion breaking, scale crossing ~100 runs/day, a recurring undiagnosable failure) signal when the MVP has earned its keep and should be upgraded to the full Intent Design Session. Below the MVP floor is not adoption; it is just deployment.**

---

## Connections

**This pattern assumes:**
- [What is the Architecture of Intent?](../introduction.md#what-is-the-architecture-of-intent) — the discipline this chapter scales down
- [The Intent Design Session](../theory/07-intent-design-session.md) — the full ritual the MVP graduates to
- [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — the 12-section spec the MVP omits most of

**This pattern enables:**
- [Adoption Playbook](11-adoption-playbook.md) — for teams introducing the framework, the MVP is the smallest unit of practice they can demonstrate before committing to the full IDS
- [A Miniature Pilot, End-to-End](../miniature-pilot.md) — the contrast case: a small but production-bound system that still warrants the full canvas
- [Signs Your Architecture of Intent Is Degrading](15-anti-patterns.md) — the audit to run when an MVP system grows past graduation thresholds without graduating

---
