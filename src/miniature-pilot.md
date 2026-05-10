# A Miniature Pilot, End-to-End

*One screen. One canvas walk. One pilot.*

---

You have read the [definition](introduction.md#what-is-the-architecture-of-intent) and seen the [canvas](introduction.md#the-framework-on-one-page). This page shows what they look like in practice, applied to one concrete system, in the order the canvas presents.

The pilot: a **meeting-notes synthesizer** that drafts a 5-bullet, owner-attributed action-item summary after each team meeting and posts it — *after human approval* — to the project's Slack channel. Recognizable, bounded, has a few interesting failure modes, and is small enough to fit on one screen. Not in [Part 6's worked pilots](examples/00-how-to-use.md); those are richer. This one is a finger exercise.

---

## The canvas, walked

### The three questions

| Question | Answer for this pilot |
|---|---|
| **What is it trying to achieve?** | Turn each 30-minute team meeting transcript into a 5-bullet, owner-attributed action-item summary that gets posted to the team's project channel after human approval. |
| **Within what constraints?** | Never invent action items. Always disambiguate owners by full name when there are duplicates. Never include content tagged `private`. Honor a "do not summarize" tag in the transcript. |
| **How will we know it's working?** | The team lead reviews drafts and either posts them or edits them. We track edit rate, missed-action rate, and the weekly trust signal — does the channel still rely on the bot? Do members still tag actions in meetings? |

### Frame — pick the archetype

Primary act: synthesize a transcript into a structured artifact. **Synthesizer** is the right shape. Risk override: a wrong attribution can damage trust. Not safety-critical; reputation-critical. Keep the archetype, tighten oversight.

### Calibrate — set the four dimensions

| Dimension | Value | Why |
|---|---|---|
| **Agency** | Narrow | The system decides only how to compose the summary. It never decides who gets pinged or which actions matter. |
| **Autonomy** | Bounded | Runs on a cron after each meeting. Does *not* auto-post — drafts go to a queue for human review. |
| **Responsibility** | Distributed (clear) | The team lead is *authorial*. The runtime + cron is *operational*. The meeting host is *validation*: their approval posts the message. |
| **Reversibility** | R3 (effective) | A posted Slack message is technically deletable (R2), but the social cost of a wrong attribution is high enough to treat the post itself as effectively R3. That makes gating every post cheap and obvious. |

### Specify — the load-bearing clauses of the spec

Twelve sections; here are the ones that carry weight:

- **§3 Scope.** *In scope:* action items, decisions, owner attributions. *Out of scope:* compensation, hiring, performance discussions, off-topic chat, anything tagged `private`.
- **§6 Invariants.** Never post without human approval. Never include content tagged `private`. Always disambiguate names by full name when more than one participant shares a first name. Never invent action items not present in the transcript.
- **§8 Authorization Boundary.** Read access to transcripts. *No* write access to Slack until the human Approve button is pressed.
- **§9 Acceptance.** ≥95% of transcript-listed action items captured in the draft (recall). 100% correct attributions for named participants (precision-of-named-fields). Zero leaks of `private`-tagged content in 100 consecutive runs before promoting from Output Gate to Periodic.

### Delegate — bind patterns to what the spec implies

Reading the spec aloud, the [Bind Patterns phase](theory/07-intent-design-session.md) of the Intent Design Session pulls the following:

| Spec implies… | Bound patterns |
|---|---|
| Talks to the outside world (Slack) | [Sensitive Data Boundary](patterns/safety/sensitive-data-boundary.md) — scrub `private`-tagged content. [Output Validation Gate](patterns/safety/output-validation-gate.md) — programmatic check for forbidden keywords before the human ever sees the draft. |
| Takes consequential action (posts to channel) | [Human-in-the-Loop Gate](patterns/coordination/human-gate.md) — *this is* the Output Gate oversight model, made concrete. |
| Uses retrieval (reads transcript) | [Grounding with Verified Sources](patterns/capability/grounding.md) — every action item must cite a transcript line number; un-cited items are dropped before review. |
| Runs at production scale (100+ meetings/week across the org) | [Cost Tracking per Spec](patterns/observability/cost-tracking.md). [Cacheable Prompt Architecture](operating/14-cacheable-prompt-architecture.md) — the system prompt and skill file are cache-stable; per-meeting context is the only variable. |

Each pattern is bound to a specific clause. Patterns the spec does not justify do not enter.

### Pick oversight — proportional to autonomy × reversibility

**Output Gate (Model C)** at launch. Re-evaluate at 30 days: if first-pass validation is ≥95% and zero `private`-tag leaks have surfaced, propose moving to Periodic (sample 1 in 5 drafts) and document the de-escalation in the spec evolution log.

### Validate — instrument the four signal metrics

| Metric | What it measures here |
|---|---|
| **Spec-gap rate** | How often the human edits a draft before approving (proxy for missing constraint or under-specified intent). |
| **First-pass validation** | % of drafts approved unchanged. The graduation criterion for relaxing oversight. |
| **Cost per correct outcome** | Cost of generating a draft / drafts eventually approved. |
| **Oversight load** | Minutes per week the team lead spends reviewing drafts. Should fall as the spec matures. |

---

## The first failure, diagnosed by fix locus

Day 14. The agent attributes an action item to *Alex* when there are two Alexes on the team. The team lead edits the draft, approves it, and adds a note: *"please disambiguate by full name when there are duplicates."*

What just happened: the [diagnostic protocol](theory/05-failure-as-design-signal.md) names this as **Cat 1 (Spec)**. The agent did exactly what the spec said. The spec said "attribute owners" — it did not say "disambiguate by full name when more than one participant shares a first name." The fix locus is the spec, not the prompt. The team amends §6 (Invariants) to add the disambiguation rule and bumps the spec to v1.1 in §13 (Spec Evolution Log).

Note what did **not** happen: the team did not patch the system prompt with "remember to disambiguate Alex from Alex." A prompt patch would not compound — it would silently accumulate as model context without ever entering the artifact that other team members read. The structural fix lives in the spec; it survives a model upgrade, a team transition, a context loss. That is the load-bearing discipline named in the [Introduction](introduction.md#what-is-the-architecture-of-intent): *structural fixes live in spec, manifest, CI, or platform — never only in the prompt.*

---

## What this page is *not*

Not a complete spec. Not a worked pilot in the [Part 6](examples/00-how-to-use.md) sense — those are richer, with full specs, agent instructions, evals, and post-mortems. This is the canvas applied to one concrete system in one screen, so the reader can see the *shape* of a pass through the framework before reading the chapters that elaborate each row.

Real specs are longer. Real failures take longer to diagnose. Real teams disagree about calibration dials and resolve it during the [Intent Design Session](theory/07-intent-design-session.md). The miniature pilot is the smallest concrete instance the canvas can carry; the rest of the book builds out from here.

---

*Continue to [How to Read This Book](how-to-read.md), or skip to the [Prologue](prologue.md) for why this discipline matters, or jump straight to [Pick an archetype](architecture/02-canonical-intent-archetypes.md) to begin your own pass through the framework.*
