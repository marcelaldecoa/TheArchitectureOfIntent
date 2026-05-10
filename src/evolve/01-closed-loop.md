# The Closed Loop: From Failures to Spec Amendments

**Part 5 · EVOLVE**

---

> **v2.0.0-rc1 stub.** This is the opening conceptual chapter of Part 5. The full prose lands in PR-B of the v2.0.0 rollout (see [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md)). New content for v2.0.0; some of the source material is distributed across [Intent Review Before Output Review](../operating/05-reviewing-intent.md), [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md), and [The Living Spec](../sdd/06-living-specs.md).

---

## What this chapter will cover

The chapter names the discipline that makes an Architecture of Intent practice survive the team that built it: every diagnosed failure produces either a spec amendment, a manifest tightening, a CI guard, or a [framework versioning](07-framework-versioning.md) bump — never only a prompt patch. The chapter argues that this loop is the *core distinguishing claim* of the framework as a working practice.

Specifically:

- **Why the loop has to be structural.** A prompt patch fixes one instance. A §4 NOT-authorized clause fixes the class. A CI guard fixes every future instance. A framework version bump fixes every future *system* in the org. The compounding is the value.
- **The loop in detail.** Production trace → categorize Cat 1–7 → trace to fix-locus → write the amendment → ship the structural change → record in the spec evolution log → roll forward.
- **Spec evolution log discipline.** Every amendment names which §, which Cat triggered it, what the prior text was, what the new text is, who reviewed. The log is the durable record; the agent's behavior at any point in time is derivable from the log plus the spec.
- **What the loop looks like at three time-scales.** Per-incident (hours): trace, categorize, file. Per-sprint (weeks): roll up the spec evolution log, find the systemic patterns, schedule structural amendments. Per-quarter (months): the [Discipline-Health Audit](../operating/15-anti-patterns.md) and the framework-version reassessment.
- **What breaks the loop.** Prompt-only patches that don't migrate to the spec. Tribal-knowledge fixes that live in someone's head. Cat 6 (Model-level) attribution being used as a license to skip the diagnostic work. Anti-patterns 1–11 from the operating chapter, mapped to which loop step they break.
- **Why this chapter opens Part 5 and not Part 4.** Validate is *learning in production*; Evolve is *what you do with what you learned*. The two are inseparable in practice, but the discipline of structural amendment is the Evolve commitment, not the Validate commitment.

## Where this chapter sits in the Part

This is **5.1**, the opener for Part 5 — Evolve. It frames the Part by naming the discipline; subsequent chapters (Adoption Playbook, MVP-AoI, Governance, Cost incident response, Anti-patterns, Framework versioning, DevSquad mapping, Co-adoption) elaborate the working practices that make the loop survive contact with a real organization.

## Conceptual chapters this binds to

- [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) — the seven categories
- [The Living Spec](../sdd/06-living-specs.md) — the artifact the loop updates
- [Intent Review Before Output Review](../operating/05-reviewing-intent.md) — the review discipline that surfaces Cat 1s
- [Spec Versioning](../patterns/deployment/spec-versioning.md) — how amended specs ship without breaking running agents
