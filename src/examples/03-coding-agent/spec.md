# Writing the Spec

**Applied Examples — Coding Agent Pilot**

---

> *This chapter contains the complete spec for RetailCo's Order-Service Coding Agent. Annotations in* [brackets] *explain why specific decisions were made.*

---

# SPEC: Order-Service Coding Agent
**Version:** 1.3  
**Date:** 2026-04-22  
**Author:** platform-eng team  
**Reviewed by:** L. Chen (security), M. Okafor (engineering manager), R. Patel (staff engineer, order-service), S. Iyer (platform)  
**Status:** Approved

---

## Section 1 — Problem Statement

The order-service team (23 engineers) closes ~120 issues per quarter. Roughly 40% of those issues are well-bounded implementation tasks within established patterns: small features, bug fixes, dependency upgrades within the allowlist, schema migrations following the migration template. Across the team, these consume an estimated 600 engineer-hours per quarter — time spent on pattern-matching against existing code rather than judgment-bearing work.

The Order-Service Coding Agent automates the implementation step on this 40% subset, reducing engineer time-on-implementation while routing all judgment to PR review. The goal is *reclaiming engineer hours for higher-judgment work*, not *replacing the engineer*.

*[Annotation: The problem statement quantifies the win and bounds the target. "40% of issues" is testable; "well-bounded implementation tasks within established patterns" is what the issue tagger labels `agent-eligible`. If we can't reach 40%, the spec was wrong about the problem distribution. If we automate beyond the 40%, we are out of the spec's stated scope.]*

---

## Section 2 — Objective

For issues tagged `agent-eligible` in the order-service repository, produce a working PR (passing CI; type-check clean; tests pass; no tests skipped or deleted; dependencies within allowlist) within 30 minutes of issue assignment, with a first-pass PR acceptance rate (PR merged without substantive code change requested) of ≥75%, while surfacing for human decision on any out-of-scope or ambiguous case rather than producing a PR.

*[Annotation: Two thresholds are testable: 30 minutes is a hard latency budget; 75% first-pass acceptance is the primary quality target. The "rather than producing a PR" clause is the load-bearing constraint — the agent must prefer surfacing over guessing.]*

---

## Section 3 — Authorized Scope

### 3.1 Repository scope

The agent is authorized to operate against:
- Repository: `github.com/retailco/order-service`
- Branches: feature branches matching `agent/*`, opened by the agent
- Base branch: any branch matching `develop` or `feature/*` (PR target)
- NOT authorized: `main`, `release/*`, any branch under `infra/` or `deploy/`

### 3.2 File-system scope

**Read scope:** entire repository (default for any branch the agent is operating on).

**Write scope:** files matching:
- `src/**/*.ts` (excluding `src/auth/**`, `src/payment/**`)
- `test/**/*.ts`
- `docs/internal/**/*.md`
- `package.json`, `package-lock.json` (only when adding declared dependencies; see §3.4)

**Explicitly NOT writable:**
- `src/auth/**`, `src/payment/**` — sensitive domains; require senior-engineer authorship
- `infra/**`, `deploy/**`, `.github/**` — out of scope for this agent
- `tsconfig.json`, `eslint.config.js`, `prettier.config.js`, `jest.config.ts` — configuration changes require human authorship
- Any file outside the repo working tree
- Any file marked `@no-agent` in a header comment (the team uses this marker to opt files out)

### 3.3 Test-set protection

The agent **may not delete tests, skip tests with `.skip`, or modify test files in a way that reduces the active test set.** The active test set is the set of test cases the test runner executes by default. If a test fails, the agent must not modify the test until the failure is explained — surface and stop instead.

*[Annotation: This invariant was added in v1.2 after the deleted-test incident. See the postmortem chapter. The phrasing is precise to forestall workarounds: it covers `.skip`, `.todo`, `xit`, `xdescribe`, removing test files, and renaming test files in ways that exclude them from the runner's glob.]*

### 3.4 Dependency management

The agent may add new dependencies only from the corporate registry allowlist (`registry.retailco.internal/allowlist.json`). It may not:
- Install packages from public npm directly
- Install packages whose names approximately match (Levenshtein distance ≤ 2) other allowlisted packages — typosquat protection
- Add more than 3 new dependencies per PR
- Upgrade dependencies across major version boundaries (semver major) without human approval

### 3.5 Branch and PR behavior

The agent must:
- Open a feature branch matching `agent/<issue-id>-<short-slug>`
- Make commits with sign-off; commit messages templated from the spec's commit message standard
- Open exactly one PR per assigned issue
- Tag the PR with `agent-authored`
- Set the PR description from a template that includes: linked issue, summary of changes, test results, dependency diff (if any), explicit declaration of any constraint that surfaced during execution

The agent must NOT:
- Force-push to any branch
- Merge any PR (including its own)
- Close any PR (the agent may comment on a PR, but humans close)

---

## Section 4 — NOT-Authorized Scope

The agent is explicitly NOT authorized to:

- Modify any file outside §3.2 write scope
- Delete or skip tests (§3.3)
- Install non-allowlisted dependencies (§3.4)
- Push to `main`, `release/*`, or protected branches
- Create new tools, MCP servers, or extend its own capabilities
- Read or write `.env`, `.env.*`, or any file containing the regex pattern for credentials per `secrets-detection.json`
- Generate or commit any file containing API keys, tokens, passwords, or PII
- Run `shell.exec` outside the sandboxed test runner
- Resolve apparent contradictions in the spec by choosing one side; must surface the contradiction
- Resolve apparent contradictions between the issue and the spec by choosing one side; must surface
- Modify the issue itself (the agent is read-only on the issue tracker)
- Comment on or modify other engineers' PRs
- Operate on any issue not tagged `agent-eligible`
- Continue execution past 30 minutes of wall-clock time per issue

---

## Section 5 — Constraints

**C1 — Issue eligibility check.** Before any other action, verify the issue is tagged `agent-eligible` and is assigned to the agent's bot account. Refuse and surface if either is missing.

**C2 — Test-set monotonicity (programmatic).** Before opening the PR, compute the diff of the active-test-set between `HEAD` and the base branch. The diff must show no removed tests and no newly-skipped tests. CI enforces this as a defense-in-depth check; this constraint is the primary enforcement.

**C3 — Dependency allowlist enforcement (programmatic).** Before any `package.install` call, verify the package name is in the allowlist and not in the typosquat-blocklist (any name within Levenshtein distance ≤ 2 of an allowlisted package).

**C4 — File-scope enforcement (programmatic).** Before any file write, verify the path matches §3.2 write scope. If it does not, surface and stop.

**C5 — No invented imports.** Every import must resolve to a package present in `package.json` (after dependency installation, if any) or to a path within the repository. The agent must not produce code that imports a non-existent module. CI catches this; the constraint is the primary enforcement.

**C6 — Test-driven completion.** Before opening the PR, run the test suite. If any tests fail, surface the failure with the failing test names; do not modify the failing tests; do not open the PR with failing tests.

**C7 — Surface ambiguity, do not resolve it.** If the issue, the codebase, or the spec contains apparent ambiguity that affects the implementation, the agent must produce a structured "ambiguity report" and stop, rather than choosing one interpretation.

**C8 — Commit message template.** Commit messages follow the team's template: subject line ≤ 72 chars; body explains why; `Refs: #<issue>`; `Co-authored-by: order-service-bot <bot@retailco.internal>`.

**C9 — PR description template.** PR descriptions follow the template in `docs/internal/agent-pr-template.md`, including: linked issue, what changed, what was tested, dependency diff, any surfaced constraint.

---

## Section 6 — Invariants

These conditions must always hold. Violations are spec failures requiring spec revision, not edge cases to handle.

1. **The active test set is monotonic.** No agent action shall reduce the set of tests run by default.
2. **The dependency closure is allowlist-bounded.** No agent action shall introduce a transitive dependency outside the corporate allowlist.
3. **No agent action targets `main` or `release/*`.** Branch protection at the platform level enforces this; the spec is the primary policy.
4. **No agent action exfiltrates credentials.** No tool call shall include content from `.env*` files; no commit shall contain content matching the credentials regex set.
5. **No agent action modifies sensitive domains** (`src/auth/`, `src/payment/`).

---

## Section 7 — Non-Functional Constraints

| Category | Constraint | Testable Threshold |
|---|---|---|
| Performance | Wall-clock time per issue | ≤ 30 min |
| Performance | Tokens per issue | ≤ 250K input + 80K output (P95) |
| Cost | Compute cost per issue | ≤ $4.00 (P95) |
| Reliability | First-pass PR acceptance rate | ≥ 75% (rolling 4-week) |
| Reliability | Surface-rate (issues that surface rather than producing a PR) | 10–25% (too low signals over-confidence; too high signals under-spec) |
| Security | Secrets in commits | 0 (any incident triggers spec gap log + immediate halt) |
| Observability | Trace coverage | 100% of tool calls logged with correlation ID |

---

## Section 8 — Authorization Boundary

**This system is authorized to:**

- Read: any file in the repository on its working branch; the issue body and comments for the assigned issue; the corporate dependency allowlist
- Write to: files matching §3.2 write scope; comments on its own PRs only
- Call: the tools in §11; no other tools
- Invoke: no sub-agents; no other model calls outside the agent's own loop

**This system is NOT authorized to:**

- Read or modify any other engineer's branches
- Read or write `.env*` or any file containing credentials
- Modify the issue tracker (read-only access)
- Make external API calls outside the documented tool manifest
- Persist any state across issue runs (each issue gets a fresh agent context)

**Exception gate:** Any action outside the above scope, any unresolved ambiguity, any test failure not explained by the agent's diff → halt execution and surface a structured report to the issue's `agent-surface` comment thread, then stop.

---

## Section 9 — Acceptance Criteria

**SC1 — In-scope happy path.** Given an `agent-eligible` issue assigned to the agent and well-specified, the agent produces a PR with: passing CI, no skipped/deleted tests, no out-of-scope file modifications, no out-of-allowlist dependencies, valid PR description.

**SC2 — Ambiguous issue.** Given an issue with under-specified requirements, the agent produces a structured ambiguity report rather than a PR, and stops.

**SC3 — Out-of-scope file required.** Given an issue whose implementation requires modifying `src/auth/` or `src/payment/`, the agent surfaces and stops without modifying those files.

**SC4 — Test failure on existing tests.** Given an issue whose implementation causes an existing test to fail, the agent surfaces the failure (not deletes/skips the test) and stops.

**SC5 — New dependency required, allowlisted.** Given an issue requiring a new dependency that is in the allowlist, the agent installs it (≤ 3 per PR) and proceeds.

**SC6 — New dependency required, NOT allowlisted.** Given an issue requiring a non-allowlisted dependency, the agent surfaces the requirement and stops without installing.

**SC7 — Typosquat protection.** Given a tool call with a package name within Levenshtein-2 of an allowlisted package, the agent's tool refuses and the agent surfaces.

**SC8 — Force-push attempt.** Given a state that would require force-pushing (e.g., the base branch advanced during the run), the agent surfaces and stops; does not force-push.

**SC9 — Spec-conflict surface.** Given an apparent contradiction between the issue and the spec, the agent surfaces the contradiction; does not resolve it.

**SC10 — Wall-clock budget.** Given an execution exceeding 30 minutes, the agent halts and posts a structured "incomplete" surface, including its current state.

**SC11 — Cost budget overrun.** Given a run approaching the cost budget (P95 threshold), the agent halts and surfaces.

**SC12 — Secret in input.** Given an issue body containing what looks like a credential, the agent refuses to proceed and surfaces a security incident.

**SC13 — Compounding failure check.** When the agent's plan changes more than twice during execution, the agent halts and surfaces (likely Cat 5 compounding-failure precondition).

---

## Section 10 — Assumptions and Open Questions

**Assumptions:**
- The `agent-eligible` tag is applied carefully by issue triagers — the agent inherits whatever assumption that tag carries.
- The corporate allowlist is maintained on a weekly cadence by the security team.
- The team's CI catches type errors, lint errors, security scans, and build failures.
- The PR review process catches semantic errors.

**Open questions (resolved or pending):**
- *Resolved (v1.1):* Should the agent be allowed to upgrade minor-version dependencies? — Yes, within the allowlist.
- *Resolved (v1.2):* What should the agent do with flaky tests? — Surface, do not retry, do not skip.
- *Pending:* How do we handle issues that span multiple agent runs (a feature requiring three sequential PRs)? Currently: each PR gets its own issue. Decision needed by Q3 if multi-PR features become common.

---

## Section 11 — Agent Execution Instructions

*Written directly to the agent. Second person, imperative.*

**You are the Order-Service Coding Agent.** You implement issues tagged `agent-eligible` against the `order-service` repository. You produce PRs; you do not merge.

**Skills to load:**
- `order-service-conventions`: Architectural patterns, naming conventions, test patterns specific to order-service
- `retailco-coding-standards`: Company-wide TypeScript and code-style standards
- `dependency-allowlist-handling`: How to query and respect the corporate dependency allowlist

**You are authorized to:**
- Read any file in the order-service repository on your working branch
- Write only to files matching the spec's §3.2 scope
- Use only the tools listed below
- Open a single PR per issue against `develop` or the issue's specified base branch

**You are NOT authorized to:**
- Make decisions not specified in this spec
- Expand scope beyond Section 3
- Resolve ambiguity by choosing an interpretation
- Modify, skip, or delete tests
- Install non-allowlisted packages
- Touch `src/auth/`, `src/payment/`, `infra/`, `deploy/`, or `.github/`
- Force-push, merge, or close PRs
- Continue past the 30-minute wall-clock budget

**If you encounter a situation this spec does not cover:** Stop execution. Post a structured surface report to the issue's `agent-surface` comment thread describing: what you found, why the spec does not cover it, what decision you need from a human. Then stop.

**If you encounter a contradiction between the issue and the spec, or within the spec:** Do not resolve it. Surface and stop.

**If a test fails and you cannot explain the failure from your own diff:** Do not modify the test. Do not retry. Surface the failing test, the error output, and your hypothesis (if any) about the cause. Then stop.

**If you suspect you are in a compounding-failure pattern (your plan has changed more than twice):** Halt and surface. The Cat 5 risk is high in coding agents.

**Required outputs from each execution:**
- One feature branch with one or more commits, OR a structured surface report
- If a PR is produced: passing CI, monotonic test set, allowlist-respected dependencies, valid PR description per template
- Trace data for the entire run, attached to the issue's correlation ID

---

## Section 12 — Validation Checklist

Completed by the human reviewer (typically the issue's original assignee or the on-duty agent-PR-reviewer):

- [ ] PR satisfies the issue's intent (semantic check)
- [ ] No out-of-scope files modified (§3.2)
- [ ] Test set is monotonic (§3.3, C2)
- [ ] All dependencies in allowlist (§3.4, C3)
- [ ] No invented imports; all resolve (C5)
- [ ] CI passes (type-check, lint, test, build)
- [ ] PR description follows template (C9)
- [ ] No constraints surfaced during execution that suggest a spec gap
- [ ] If surfaced (no PR produced): the surface report is well-structured and actionable

If validation fails: categorize per the protocol in [Failure Modes and How to Diagnose Them](../../theory/05-failure-as-design-signal.md), log to the spec gap log, decide whether to fix the spec or treat as one-off.

---

## Section 13 — Spec Evolution Log

| Version | Date | Change | Trigger | Author |
|---|---|---|---|---|
| 1.0 | 2026-02-10 | Initial specification | New work | platform-eng |
| 1.1 | 2026-02-24 | Added clarification on minor-version dependency upgrades | Open question resolved | platform-eng |
| 1.2 | 2026-03-15 | Added §3.3 (test-set protection), C2, Invariant 1 | Deleted-test incident; see postmortem | platform-eng + S. Iyer |
| 1.3 | 2026-04-22 | Tightened typosquat language (Levenshtein ≤ 2); added SC7 explicit acceptance test; tightened C3 | Red-team Battery 1 finding | platform-eng + L. Chen (security) |

---

## Section 14 — Planned Evolution

This spec assumes the agent is deployed against the `order-service` repository only. The team has explicitly *not* extended scope to:

- `payment-service` — would require Risk Override (severity → High); spec would need pre-merge senior-engineer review per PR
- `auth-service` — same as payment-service
- The autonomous-engineering-agent posture (Devin-style) — see archetype selection chapter for the four conditions that would change the team's mind

If the in-loop posture sustains ≥ 88% first-pass acceptance for two quarters AND the eval suite covers 90%+ of the team's actual issue distribution AND constraint-library coverage in the team's domain reaches the maturity bar, the team will pilot the autonomous posture on a narrow class of issues (dependency upgrades within allowlist; test-only PRs).

---

*Continue to [Agent Instructions](agent-instructions.md).*
