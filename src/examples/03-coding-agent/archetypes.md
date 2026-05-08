# Selecting the Archetypes

**Applied Examples — Coding Agent Pilot**

---

This chapter walks through the archetype selection for RetailCo's Order-Service Coding Agent, including the decision tree application, the dimension assessment, and the explicit rejection of alternatives.

---

## The system in one paragraph

An in-loop coding agent that reads issues from the team's tracker, drafts branches, implements changes, runs the test suite, and opens PRs. It does not merge. It does not deploy. It surfaces for human decision when scope is unclear or when constraints conflict.

---

## Walking the decision tree

From [The Archetype Selection Tree](../../architecture/04-decision-tree.md):

**Q1: Does this system take any consequential action without a human between its output and the consequence?**

*Yes.* The agent writes files, commits, pushes branches, and creates PRs without per-action human gating. The PR review is downstream of the agent's actions — the actions themselves (writes, commits, branch pushes) have already happened by the time a human reviews.

This rules out Advisor.

**Q2: Is the system's primary purpose to protect a boundary or prevent a violation?**

*No.* The agent's purpose is to ship features, not to enforce constraints. Guardian behavior is present (it must refuse to delete tests, refuse to install non-allowlisted packages) but it's a constraint on the Executor, not the primary act.

**Q3: Does this system fundamentally direct work across other agents?**

*No.* Single-agent deployment. The team explicitly chose against multi-agent. (See "Why not Orchestrator-over-self" below.)

**Q4: Is the primary output a synthesized artifact rather than action on a target system?**

*Mixed.* The agent produces a structured artifact (the diff, the PR description) AND takes actions on a target system (file writes, commits, pushes). This is the mode-mixing characteristic of coding agents called out in [Coding Agents](../../agents/08-coding-agents.md).

The dominant primary act here is *act* — the diff exists in the repo as state, not as a draft for review. So **Executor with Synthesizer composition**, not Synthesizer alone.

---

## Final classification

**Primary archetype:** Executor (in-loop coding agent posture per [Coding Agents](../../agents/08-coding-agents.md))

**Composition:** Synthesizer for diff-and-PR-description generation

**Agency Level:** 3 — Bounded. The agent decides *how* to implement within an authorized scope (file paths, allowed tools, approved dependencies), but the *what* is constrained by the issue and the spec. It does not set its own goals.

**Risk Posture:** Medium.
- Impact scope: narrow (one repo, one team's code) — but production code that ships to customers eventually
- Severity: medium (a bad PR wastes review time; a merged bad PR could ship a bug; the PR-gate is the primary defense)
- Detectability: fast (CI catches structural issues; reviewers catch semantic issues; test failures are immediate)

**Oversight Model:** D — Pre-authorized Scope + Exception Gate. The spec defines exactly what files, tools, branches, and dependencies the agent may touch. Anything outside scope surfaces for human decision. PR review is the post-hoc validation layer, not a per-step gate.

**Reversibility:**
- File writes → fully reversible (git)
- Commits → fully reversible (git revert)
- Branch pushes → reversible but visible to others (someone may have pulled)
- PR creation → reversible (close PR) but creates noise
- Merges to main → not in scope; PR-only. If a merge happens, that's a control failure (Cat 4 Oversight Failure), not an agent action.

Reversibility classification: **R2 (Largely reversible)** for the agent's authorized actions. Mostly recoverable through standard git operations; some social cost from noise.

---

## Why not Orchestrator-over-self (Devin-style)

The team considered an autonomous-engineering-agent posture: file an issue, get a PR with no human-in-loop until review. They chose against it for four reasons, all worth recording explicitly:

**1. Consequence and reliability are not yet matched.** The team's tolerable rate of bad PRs is roughly 5%. Internal benchmarking on a held-out set of 50 historical issues showed the autonomous architecture producing acceptable PRs ~70% of the time, vs. the in-loop architecture at ~88%. The 18-percentage-point gap is the cost of compounding failure across the planner→implementer→reviewer sub-agent loop in a system whose sub-agents share a model.

**2. Debuggability does not yet exist.** Compounding failures in the autonomous architecture were hard to attribute. The team's observability stack (LangSmith) traces the calls, but post-mortem analysis on the failed PRs took 3–4× longer than for the in-loop architecture, because the failure had to be traced backward through multiple sub-agent contexts.

**3. The team's bandwidth budget assumes the in-loop posture.** The team allocated ~2 hours per engineer per week for agent oversight (PR reviews of agent PRs, plus spec maintenance). The autonomous posture would need ~4 hours per engineer per week for the same throughput, due to the higher rate of bad PRs requiring spec revision and the harder debugging.

**4. The team has not yet developed the spec-and-eval discipline that an autonomous posture requires.** This is the team's first agent deployment. The spec-gap-log culture, the eval coverage, and the constraint library all need to mature before the team trusts itself to specify an autonomous agent's exception conditions exhaustively.

**Conditions under which the team will revisit:** if the in-loop posture is producing >88% acceptable PRs sustainably for two quarters, if the eval suite covers the team's actual issue distribution, and if the team has bandwidth to maintain a more elaborate spec, the team will pilot a hybrid: autonomous on a narrow class of issues (dependency upgrades within the allowlist, test-only PRs) while keeping the in-loop posture for everything else.

This explicit "we are not doing this, and here is what would change our minds" record is part of the spec evolution log and should be revisited at each quarterly review per [Governed Archetype Evolution](../../architecture/06-evolving-archetypes.md).

---

## What's NOT this archetype's job

Naming what the agent is not authorized to do is part of the archetype classification:

- The agent is **not** an Orchestrator. It does not delegate work to other agents. If a task requires more than one agent (rare for the team's current issue mix), the human files separate issues for separate agent runs.
- The agent is **not** a Guardian over the codebase. Code-quality enforcement (linting, formatting, type-checking, security scanning) is handled by CI tools, not by the coding agent. The coding agent must satisfy them, but is not their guardian.
- The agent is **not** an Advisor. It does not produce suggestions for engineers to apply manually. If an engineer wants advice without action, they use the team's pair-programming Copilot deployment, which is a different system with a different spec.

---

## Risk Override check

From [The Archetype Selection Tree — Risk Override](../../architecture/04-decision-tree.md):

> *If the system's consequence-of-failure is Critical (broad impact, high severity, or slow detectability), document that explicitly and escalate the governance tier.*

For this system:
- Impact scope: narrow (one repo)
- Severity: medium (PR-gated)
- Detectability: fast (CI + review)

No override triggered. The Executor + Model D oversight stays as the minimum.

The team noted that *if* this agent's scope expanded to repos with broader blast radius (the payment service, the auth service), the override would trigger and the governance tier would escalate to mandatory pre-merge review by a senior engineer per PR. This is recorded in the spec's Section 14 (Planned Evolution).

---

*Continue to [Writing the Spec](spec.md).*
