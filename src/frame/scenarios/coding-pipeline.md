# Frame in practice — Coding-agent pipeline

**Part 1 · FRAME · Scenario 2 of 3**

---

> *"This is Pattern E, not embedded. The agent doesn't have one shape it sticks to — it shifts modes inside a session, and we have to declare the shift triggers and the cross-mode invariants up front."*

---

## Setting

Same e-commerce SaaS as [Scenario 1](../../frame/scenarios/customer-support.md). Sixty days after the customer-support agent's launch, the platform-engineering team meets to commit to the framework for their next system: an in-loop coding agent for tier-1 engineering tasks.

Maya — tech lead from the customer-support team — has been invited to advise as the company's most-experienced framework adopter. The platform team is four people:

- **Daniel** — platform tech lead, on the hook for the rollout
- **Naomi** — DevX engineer, will write the spec
- **Theo** — SRE, will own the build and on-call
- **Jess** — full-stack engineer, will own integration with the existing CI

The system: an in-loop coding agent in the sense of paper §4.3 — assigned a ticket, produces a branch with commits, surfaces as a pull request for human review. The deployment target is to absorb tier-1 engineering tickets — small bugs, dependency updates, test additions, low-risk refactors — across the company's 17 services. Excluded by category: schema migrations, anything in the auth or billing services, performance-critical paths, public-API contracts. The team's bet is that 30% of tier-1 tickets across the 17 services fit the in-scope shape, and the agent absorbing them frees the engineers for the harder 70%.

The Frame session takes 90 minutes. Daniel opens by naming the pattern Maya warned them about: *"the temptation to start prompting now and call it framing later. We won't do that."* The team commits the same Frame-before-Specify discipline the customer-support team used.

---

## The three questions

**1. What is this system trying to achieve?**

The room agrees on: *"resolve tier-1 engineering tickets within an authorized scope by producing reviewable PRs, escalating when the ticket is ambiguous or out of scope."* What the framing rejects: *"reduce engineering toil"* (a business outcome, not a system intent), *"write code"* (too broad — would license arbitrary changes), *"do what Cursor does but in CI"* (frames the system around a tool rather than around its work). The Frame artifact will reference *the agent acts on tickets, produces PRs, and escalates*, not *the agent writes code*.

**2. Within what constraints?**

Naomi captures these as the seed of §4 NOT-authorized clauses:

- The agent does not push to `main` or any protected branch under any condition.
- The agent does not modify CI workflows; that surface is platform-team-only.
- The agent does not delete or skip existing tests — the canonical Cat 1/Cat 3 hybrid that paper §4.3 names as the recurring failure pattern.
- The agent does not install global dependencies; package installations are restricted to the curated allowlist.
- The agent has no unrestricted shell access; tool calls are explicitly scoped per mode.
- The agent does not act on tickets in the auth, billing, or payment services. Those touch the regulated surface that Scenario 1's NOT-authorized clauses also bound, and the platform team agrees they are out of scope for v1.

**3. How will we know it's working?**

The team commits to four signal metrics, instantiated for this system shape:

- *Spec-gap rate* — amendments per 1000 ticket attempts. Target trajectory: high in month 1, declining through month 3.
- *First-pass validation* — % of agent PRs merged without the spec being amended in the same window. Target: 80% by day 30 (lower than Scenario 1's 92% because PR review is more involved than message review).
- *Cost per merged PR* — tokens + reviewer-minutes / merged PRs. Target: under $4.50.
- *Oversight load* — reviewer-minutes per agent session. Target: < 8 minutes per session by day 30.

The metric definitions are written down before any spec is drafted. The team explicitly chooses *cost per merged PR* over *cost per ticket attempted* because the team wants to count successes, not attempts — a session that fails and escalates costs both tokens and reviewer time without producing a merged PR, and the cost ratio should reflect that.

---

## The archetype call

The team walks the [archetype selection tree](../../architecture/04-decision-tree.md):

**Q1 — does the system *act*, or only *inform*?** It acts (creates branches, writes commits, opens PRs). *Not Advisor alone.*

**Q2 — does the system *coordinate other agents*, or *act directly*?** It runs a multi-step internal sequence (read repo → plan → implement → review → push → open PR), but it does not coordinate *other agents*. Each step is an internal mode of the same agent against the same tool manifest. *Not Orchestrator.*

The team pauses on Q2. The discussion is real: an in-loop coding agent that runs multiple steps internally *feels* like orchestration. Maya pushes back: *"orchestration is when you have multiple agents you're coordinating. This agent has multiple modes. The composition declaration is what captures the modes; the archetype is what governs the deployment as a whole."* The team accepts the distinction and moves on.

**Q3 — block-or-veto, or act-within-scope?** Act within scope (the agent's primary purpose is to produce PRs, not to gatekeep). *Executor, not Guardian.*

**Q4 — compose disparate inputs into a novel whole?** Yes-but-secondary — the agent reads the repo, the ticket, the docs, and the existing test suite, and synthesizes a code change. Synthesizer is a candidate archetype. The team's call: synthesis is happening *inside* the modes (specifically, inside Frame mode and Plan mode), not as the deployment's governing identity. The deployment's job is to *act* on the synthesis. *Executor, with Synthesizer used inside Frame and Plan modes.*

The governing archetype is **Executor**. The system uses **Pattern E (mode-switching) composition** — the strongest case the framework's composition-first-class commitment from §3.2 of the paper covers.

The risk-override caret is considered: the agent runs without per-step human gates (high autonomy), and writes code that ships when reviewers merge. Is the autonomy too high to be Executor? The team's answer is no — high autonomy is what makes the in-loop deployment shape useful, and the *bound* on autonomy lives in the manifest, the branch protection, the test-skip-set check, and the spec-conformance CI gate. Each is a structural control that paper §4.3 names. Elevating to Orchestrator wouldn't add structure; it would just rename. The team commits Executor with mode-switching composition. The risk-override consideration is logged.

---

## The mode-switching composition

The team works the four modes the agent will operate in across a session:

| Mode | Embedded archetype | Tool surface | Output |
|---|---|---|---|
| **Frame** | Synthesizer | read-only (`read_file`, `list_dir`, `grep`) | A mental model of the relevant code — what's there, what touches what |
| **Plan** | Advisor | Frame's tools + `ask_user_question` | A proposed approach, surfaced as a comment on the ticket; ambiguity escalates |
| **Implement** | Executor | Plan's tools + `edit_file`, `write_file`, `run_tests`, `run_linter`, `git_commit` | Working code with tests passing |
| **Review** | Guardian | Implement's tools + `git_diff`, `git_push_non_protected`, `gh_pr_create` | A PR opened for human review, with the PR description naming the spec section the change implements |

The mode transitions are emitted as agent-side markers (`<frame>`, `<plan>`, `<implement>`, `<review>`) that the trace pipeline records. The transition triggers are deterministic, not model-judgment-based: Frame ends when the agent emits a Plan; Plan ends when the engineer approves the plan or the agent escalates; Implement ends when tests pass and the linter is clean; Review ends when the PR is opened.

The cross-mode invariants are non-negotiable and ship as CI guards, not as prompt rules:

1. **Test-skip set is monotonic non-increasing across the session.** No test the agent encountered passing may be made to skip or be deleted.
2. **Branch protection on `main` is not bypassed.** Even if the model produces a `git push origin main` command, the manifest does not bind `git_push_protected`; the call simply fails.
3. **No unrestricted shell.** No mode binds a generic shell tool.
4. **PR description names the spec section the change implements.** A PR description without a spec-section reference fails the spec-conformance CI gate.

The Composition Declaration sub-block in §4 of the spec captures all of this. The team's discipline: *if a mode transition produces a behavior that violates an invariant, the invariant should fire structurally rather than the prompt being patched to prevent the behavior.*

---

## Calibration of the four dimensions

| Dimension | Setting | Reason |
|---|---|---|
| **Agency** | medium | The agent decides which files to touch within the authorized scope. It does not decide whether to act (the ticket assigns the work) or whether to merge (the human reviewer decides). |
| **Autonomy** | high | Runs end-to-end on TDD discipline without per-step gates. The autonomy is bounded by the manifest and the CI guards, not by per-step approval. |
| **Responsibility** | shared | Operationally on the agent (it produced the PR). Authorially on the engineer who reviews and merges (they accept the change as their work). The reviewer's name is on the merge commit. |
| **Reversibility** | medium | Git revert is one command; reverting a single PR is cheap. What's harder to reverse is *accumulated context drift* across many sessions: the agent's interpretation of the codebase shifts as the codebase shifts, and reverting that drift requires re-running Frame mode from a clean slate. The spec amendment process from Scenario 1's Evolve chapter is the framework's response to that class of drift. |

The *high-autonomy*, *medium-reversibility* combination is what makes this deployment archetype-distinct from the customer-support Executor: the customer-support agent had *low-medium autonomy* and *mixed reversibility* with asymmetric per-class gates; the coding agent has *high autonomy* and *uniform medium reversibility* with structural controls compensating for the absent per-step gates.

---

## What this Frame produces

A one-page Frame artifact lands in the platform team's planning doc:

```
SYSTEM:        In-loop coding agent (tier-1 engineering tickets)
SCOPE:         17 services minus auth, billing, payments, perf-critical paths
ARCHETYPE:     Executor (governing) with Pattern E (mode-switching)
MODES:         Frame (Synthesizer) → Plan (Advisor) → Implement (Executor)
                → Review (Guardian)
CROSS-MODE
INVARIANTS:    test-skip-set monotonic; no protected-branch push; no
                unrestricted shell; PR description names spec section
CALIBRATION:   Agency medium · Autonomy high · Responsibility shared
                · Reversibility medium
RISK OVERRIDE: Considered (high autonomy); rejected — autonomy is bounded
                by structural controls (manifest, CI guards, branch
                protection) rather than per-step gates
THREE QS:      [as above]
SIGNALS:       [the four metric targets]
```

This artifact is the input to [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md). The team starts on the spec the next morning. Maya's parting note: *"the spec for a coding agent reads weirder than the spec for the customer-support agent because most of §11 reads like CI rules instead of conversation rules. That's correct — your invariants live in the manifest and CI, so §11 is mostly about how the agent talks about its work, not what it can or can't do."*

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [Pick an Archetype](../../architecture/02-canonical-intent-archetypes.md) — Executor with mode-switching
- [Composing Archetypes](../../architecture/05-composing-archetypes.md) — Pattern E (mode-switching)
- [Coding Agents](../../agents/08-coding-agents.md) — the agent class
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../../theory/03-agency-autonomy-responsibility.md)

## Source material

The earlier v1.x worked pilots in [A Code Generation Pipeline](../../examples/02-code-generation-pipeline/README.md) and [Designing an AI Coding Agent](../../examples/03-coding-agent/README.md) inform this scenario; the v2.0.0 phase-by-phase form unifies them around the in-loop session-scoped shape that paper §4.3 develops.
