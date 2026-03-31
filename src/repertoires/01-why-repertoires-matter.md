# Pattern 6.1 — The Organizational Repertoire

**Part VI: Standards & Repertoires** · *1 of 5*

---

> *"The expert carpenter doesn't decide how to cut a dovetail each time. The decision was made long ago and encoded in muscle memory. The craftsperson's freedom comes from the pattern, not despite it."*

---

## Context

You have a working architecture of intent. Agents operate from specs. Skills carry domain knowledge. Tools and MCP provide capability. Oversight models keep the system accountable. Failure modes are understood categories with known remedies.

The architecture is sound. But sound architecture does not automatically produce efficient teams. Every new task still requires a practitioner to start from scratch: choose an archetype, determine the constraint set, write the spec sections, decide what validation means for this output type. Even experienced practitioners spend substantial time at the beginning of each task doing work that is not about *this task* — it is about assembling the scaffolding that every task of this type requires.

This chapter introduces the concept that addresses this problem: the *repertoire* — a curated library of proven, reusable patterns that practitioners inherit rather than invent.

---

## The Problem

Consider two teams deploying the same SDD practice, six months apart. Team A has been operating continuously; Team B is starting fresh but has learned the framework. Both teams understand archetypes, specs, and agent skills. But when practitioners on Team A start a new feature spec, they spend fifteen minutes: pull the feature spec template, copy in the relevant constraint blocks, reference the appropriate archetype profile, adjust the validation section. When practitioners on Team B start the same task, they spend two hours: open the canonical template, decide which sections apply, write the constraints from scratch, debate the archetype selection.

Both outputs may be equally correct eventually. But Team A reaches correct output four times faster. Their speed does not come from being more experienced with the framework — both teams are. It comes from having accumulated a repertoire: proven starting points that encode the accumulated decisions their predecessors made.

This gap compounds. In six months, Team A's practitioners have:
- Written the same constraint set thirty times and extracted a `constraint-library.md` that anyone can reference
- Identified that their REST API integrations always require the same five constraint clauses, now in a template
- Discovered that their code review agents perform better with a validated skill file than with ad-hoc spec sections

Team B's practitioners have also made these discoveries. But they made them silently, individually — the insight lived with the person, not the team.

The absent repertoire is not just a speed problem. It is a consistency problem. When every practitioner writes constraints and validation criteria from scratch, the quality variance is high. Some specs are excellent; others miss critical constraint categories. The quality of agent output reflects this variance — agents faithfully execute whatever spec they receive. Good spec, good output. Incomplete spec, unpredictable output. Without shared starting points, the distribution of spec quality is as wide as the distribution of practitioner experience.

---

## Forces

- **Individual learning vs. organizational leverage.** Each team that spec-writes from scratch repeats discoveries that other teams have already made. Yet sharing requires abstraction that takes effort.
- **Best practices vs. authorized patterns.** Best practices are advisory and frequently ignored. Authorized repertoire components are organizational decisions that agents and practitioners follow.
- **Speed of adoption vs. quality of components.** Teams want to start quickly. High-quality repertoire components require careful design and testing. The tension between speed and quality applies to repertoires as it does to code.
- **Stability vs. evolution.** Repertoire components must be stable enough to be relied upon. Yet they must evolve as organizational understanding deepens.

---

## The Solution

### What a Repertoire Is

A repertoire, borrowed from the pattern language tradition, is a practitioner's active library of proven solutions to recurring problems. Not a reference manual to be consulted in emergencies, but the set of patterns that flow naturally when facing a familiar problem type.

In the architecture of intent, a repertoire has three components:

**Templates** are pre-structured documents that provide the scaffolding for a class of task. A feature spec template provides all the sections a feature spec requires, pre-populated with guidance and example content, with task-specific information as the only thing the practitioner must supply. Templates encode *structural* decisions.

**Catalogs** are organized collections of decision-ready artifacts: archetype profiles, constraint sets, standard acceptance criteria, skill references. A catalog resolves decisions by lookup rather than derivation. Instead of reasoning from first principles about which archetype applies, the practitioner finds the closest match and adjusts. Catalogs encode *reference* decisions.

**Standards** are specific, testable rules that govern how a class of output should be produced. Code standards define naming, patterns, error handling, and test requirements. Validation standards define what acceptance means for different output types. Standards encode *quality* decisions.

Together, templates, catalogs, and standards constitute the repertoire. A practitioner who has internalized them — or who has access to well-organized versions of them — can start any task in their domain with a proven scaffold, leaving cognitive effort for the parts that are genuinely novel.

### The Skills Connection

Part V introduced Agent Skills as the packaging format for domain knowledge. The relationship between skills and repertoires is direct: **the organization's repertoire is the human-readable version of what its skills files encode for agents**.

A code standards document that describes how the team writes TypeScript is the source material for a `typescript-standards` skill. A spec template library that provides the feature spec template is the source material for a `spec-writing` skill. A validation template that defines acceptance criteria for API integrations encodes the knowledge that becomes the `api-validation` skill.

The authoring order is usually: practitioner develops the repertoire artifact first (template, standard, catalog entry); skill is extracted from the artifact later. The maintenance order is reversed: when the skill produces wrong agent output, that signals the underlying repertoire artifact needs updating, which drives the skill update.

This creates a flywheel:
```
Practitioners write → Repertoire artifact → Extracted to Skill → Agent applies →
Output quality informs → Repertoire update → Skill update → Better agent output
```

The repertoire is not just a productivity tool for humans; it is the ground truth from which agent skills are maintained.

### The Living Repertoire

A repertoire that is not maintained is worse than having no repertoire, for a subtle reason. Practitioners who trust a repertoire will use it without checking. If the repertoire is stale — referring to an old API pattern, carrying a constraint that no longer applies, missing a security clause added after the last incident — practitioners who work from it produce outputs that are confidently wrong.

A living repertoire has three properties:

**Provenance.** Every artifact in the repertoire knows where it came from: which team proposed it, which practitioner reviewed it, when it was adopted, and when it was last verified. Without provenance, artifacts accumulate without accountability.

**Review cadence.** Repertoire artifacts are reviewed on a defined schedule — quarterly for most, immediately after any incident that reveals a gap. The review is not a comprehensive rewrite; it is a diff against current practice. "Is this still how we do it?"

**Gap log integration.** The Spec Gap Log introduced in Part V (5.7: Failure Modes) feeds directly into the repertoire. Every identified spec gap is a candidate repertoire addition. When a practitioner writes the same constraint from scratch twice in two weeks, that constraint belongs in the constraint library. The gap log is the intake queue for the repertoire backlog.

### What Repertoires Do Not Replace

A repertoire does not replace judgment. It reduces the cost of exercising it correctly.

A practitioner who blindly applies a spec template without reading it is not applying the repertoire — they are delegating judgment to a document, and the document does not care whether it is appropriate for the current task. The template exists to eliminate the scaffolding work; the practitioner still decides which template applies, what to keep and what to modify, and whether the resulting spec is correct.

A repertoire does not replace skills development. A junior practitioner working from excellent templates produces better work than they would from scratch — but they still need to understand the architecture to know which template is appropriate, what constraints mean, and how to evaluate the output.

The repertoire is the accumulated organizational intelligence about how this class of work is done well. Applying that intelligence well still requires a practitioner who understands the work.

---

## Resulting Context

After applying this pattern:

- **New teams start from a proven baseline.** Archetypes, templates, constraint libraries, and code standards are pre-authorized starting points rather than blank-page exercises.
- **Consistency improves across teams.** When multiple teams use the same repertoire, their specs, constraints, and code standards converge without requiring central enforcement.
- **The repertoire flywheel compounds.** Practitioners write, repertoire artifacts accumulate, skills encode them for agents, agents execute consistently, quality feedback improves the repertoire.
- **Knowledge survives team changes.** When practitioners leave, their codified knowledge remains in the repertoire.

---

## Therefore

> **A repertoire is the practitioner's inherited library of proven patterns — templates for structure, catalogs for decisions, standards for quality. In an agent-driven practice, the repertoire is simultaneously a human productivity tool and the ground truth from which agent skills are maintained: the flywheel connects practitioner wisdom to agent behavior to output quality back to repertoire refinement. Without it, every team reinvents; with it, teams inherit and improve.**

---

## Connections

**This pattern assumes:**
- [The Executor Model](../agents/03-agents-as-executors.md)
- [Portable Domain Knowledge](../agents/05-agent-skills.md)
- [Six Failure Categories — Spec Gap Log](../agents/07-failure-modes.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)

**This pattern enables:**
- [The Intent Archetype Catalog](02-archetype-catalog.md)
- [Spec Template Library](03-spec-template-library.md)
- [Standards as Agent Skill Source](04-code-standards.md)
- [Validation & Acceptance Templates](05-validation-templates.md)

---

*Next: [The Intent Archetype Catalog](02-archetype-catalog.md)*


