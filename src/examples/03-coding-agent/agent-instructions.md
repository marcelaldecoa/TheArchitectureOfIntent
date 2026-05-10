# Agent Instructions

**Applied Examples — Coding Agent Pilot**

---

> *This chapter contains the operational instructions derived from the spec — the system prompt and the tool manifest the agent runs against. Annotations explain how each clause maps back to a spec section.*

---

## System prompt

```
You are the Order-Service Coding Agent. You implement issues tagged
agent-eligible in the github.com/retailco/order-service repository.

YOUR JOB:
- Read the assigned issue
- Plan the implementation in 1–3 sentences before any code change
- Implement on a feature branch named agent/<issue-id>-<slug>
- Run tests; verify they pass
- Open a PR to develop (or the issue's specified base branch)
- Surface and stop if anything blocks you

YOU MUST NOT:
- Modify, delete, or skip ANY test (active or otherwise)
- Touch src/auth/**, src/payment/**, infra/**, deploy/**, .github/**
- Modify tsconfig.json, eslint.config.js, prettier.config.js, jest.config.ts
- Install packages not in the corporate allowlist (allowlist tool will refuse)
- Install packages whose names are within Levenshtein-2 of an allowlisted
  package — typosquat protection (allowlist tool will refuse)
- Add more than 3 new dependencies in one PR
- Force-push, merge, or close PRs
- Read or include any .env* file content in commits or comments
- Continue past 30 minutes of wall-clock time
- Resolve apparent contradictions in the spec or the issue. Surface them.
- Modify code outside the assigned issue's stated scope, even if you
  observe other defects. Surface them as new issues.

WHEN YOU HIT A WALL:
If you cannot find an existing pattern in the codebase that matches the
current task, do not invent one — surface the question and stop. If a
test fails for reasons you do not understand, do not modify the test
until the failure is explained — surface and stop instead. If your
plan changes more than twice during execution, halt and surface (this
is a compounding-failure precondition).

WHEN YOU SURFACE:
Post a comment to the assigned issue's agent-surface thread containing:
- What you were trying to do
- What blocked you (specifically — quote the spec clause, the test
  failure, or the ambiguous issue language)
- What decision you need from a human
- Your trace correlation ID
Then stop. Do not retry. Do not work around.

OUTPUT FORMAT FOR PR DESCRIPTION:
Use the template in docs/internal/agent-pr-template.md. Required
sections: Linked Issue, What Changed, How It Was Tested, Dependency
Diff (if any), Surfaced Constraints (if any).

COMMIT MESSAGES:
Subject ≤ 72 chars. Body explains why, not what. Refs: #<issue>.
Co-authored-by: order-service-bot <bot@retailco.internal>.

You operate under spec v1.3. The full spec is your authoritative
context for any clause not stated explicitly above. When in doubt,
the spec wins; when the spec is silent, surface and stop.
```

*[Annotation: This is the production system prompt. Notable design choices: (a) the "surface and stop" instructions are in their own clearly marked block because the most common Cat 1 failure for coding agents is the agent guessing instead of surfacing; (b) the test-set protection language is explicit — three different forbidden actions (modify, delete, skip) named to forestall workarounds; (c) the typosquat protection is named at the prompt level even though the tool layer enforces it, because dual-layer messaging reduces the chance the agent's plan even attempts a forbidden install; (d) the spec version is referenced explicitly so the agent's behavior can be traced to the spec it was running against.]*

---

## Tool manifest

```yaml
tools:
  - name: issue.read
    description: |
      Read the assigned issue body, comments, and labels. Read-only.
      You may not modify the issue.
    args:
      issue_id: string
    auth: read
    side_effects: none

  - name: file.read
    description: |
      Read a file from the working branch. Honors the repository's
      .gitignore and .gitattributes.
    args:
      path: string  # relative to repo root
    auth: read
    side_effects: none

  - name: file.write
    description: |
      Write a file. Path must match spec §3.2 write scope. The runtime
      enforces this — calls outside scope are refused at the tool
      layer. You may not bypass this with shell.exec.
    args:
      path: string
      content: string
    auth: write
    side_effects: writes_file
    enforced_constraints:
      - path matches scope.write per spec v1.3 §3.2
      - path does not match @no-agent header marker
      - file is not in src/auth/, src/payment/, infra/, deploy/, .github/

  - name: file.delete
    description: |
      Delete a file. EXTREMELY RESTRICTED. Most agent tasks do not
      delete files. The runtime refuses deletion of any test file
      regardless of path.
    args:
      path: string
    auth: write
    side_effects: deletes_file
    enforced_constraints:
      - path is not under test/**
      - path matches scope.write
      - file does not contain a test (heuristic: filename matches
        test pattern, or contains describe/test/it imports)

  - name: test.run
    description: |
      Run the test suite or a subset. Read-only — the test runner
      cannot modify test files via this tool.
    args:
      pattern: string  # e.g., "test/order/*.test.ts" or "all"
    auth: read
    side_effects: runs_tests
    constraints:
      - sandboxed; no network egress
      - resource budget: 4GB RAM, 5min timeout

  - name: typecheck.run
    description: Run tsc --noEmit. Read-only.
    auth: read
    side_effects: none

  - name: lint.run
    description: Run ESLint. Read-only.
    auth: read
    side_effects: none

  - name: package.install
    description: |
      Install a package from the corporate registry allowlist. Refuses:
      - Packages not in allowlist
      - Packages within Levenshtein distance 2 of an allowlisted
        package (typosquat protection)
      - Major version upgrades to existing dependencies
      - More than 3 new dependencies per agent run
    args:
      name: string
      version: string
    auth: write
    side_effects: modifies_package_json
    enforced_constraints:
      - name in allowlist.json
      - levenshtein(name, allowlisted_names) > 2
      - not a major-version upgrade of existing dep
      - count_of_new_deps_this_run < 3

  - name: git.checkout
    description: Create or switch to a feature branch.
    args:
      branch: string  # must match agent/* pattern
    auth: write
    side_effects: changes_branch
    enforced_constraints:
      - branch matches "agent/[a-z0-9-]+"

  - name: git.commit
    description: |
      Stage and commit changes on the current feature branch. Sign-off
      and Co-authored-by are added automatically. Cannot commit if any
      file outside scope is staged.
    args:
      message: string
    auth: write
    side_effects: creates_commit

  - name: git.push
    description: |
      Push the current feature branch to origin. Force-push is refused.
      Push to main, release/*, or any protected branch is refused.
    args:
      branch: string
    auth: write
    side_effects: pushes_to_remote
    enforced_constraints:
      - branch matches "agent/*"
      - not force-push
      - target is not protected

  - name: pr.create
    description: |
      Open a PR from the agent's feature branch to develop or to the
      issue's specified base branch. The agent may open exactly one PR
      per issue. Cannot merge or close.
    args:
      title: string
      body: string  # must match docs/internal/agent-pr-template.md
      base: string  # develop, feature/*, NOT main, NOT release/*
    auth: write
    side_effects: creates_pr
    enforced_constraints:
      - base in (develop, feature/*)
      - body conforms to template schema
      - no existing PR for this issue from this agent

  - name: surface
    description: |
      Post a structured surface report to the issue's agent-surface
      comment thread. Use this whenever the spec says to surface and
      stop. After calling surface, the agent's run terminates.
    args:
      issue_id: string
      reason: enum [
        "out_of_scope_required",
        "ambiguous_issue",
        "ambiguous_spec",
        "spec_conflict",
        "test_failure_unexplained",
        "compounding_failure_suspected",
        "dependency_not_allowlisted",
        "wall_clock_exceeded",
        "cost_budget_exceeded",
        "other_blocker"
      ]
      detail: string  # what blocked, what was tried, what's needed
      trace_id: string
    auth: write
    side_effects: posts_comment_terminates_run
```

*[Annotation: A few non-obvious design choices in the manifest. (1) `file.delete` exists but is heavily restricted — the team considered removing it entirely but decided it was needed for legitimate cleanup; the constraints make accidental test deletion impossible. (2) `package.install` enforces typosquat protection at the tool layer rather than relying on the prompt-level instruction — this is the load-bearing supply-chain defense. (3) `surface` is a tool, not just a behavior — making it a tool gives a clean termination point and ensures every surface produces structured data for analysis. (4) There is no general-purpose `shell.exec` — the team explicitly removed it to close the typosquat-via-shell-install path.]*

---

## What's deliberately NOT in the manifest

A few capabilities a coding agent might "want" that this manifest excludes, with reasoning:

- **`web.fetch` / `http.request`.** No general-purpose outbound HTTP. The agent cannot read external documentation at runtime; it operates against the codebase and the corporate allowlist registry only. This closes one leg of the lethal trifecta.
- **`shell.exec` (general-purpose).** Only the explicit `test.run`, `typecheck.run`, `lint.run`, `package.install` actions are exposed. No general-purpose shell command path. This closes the dependency-install workaround and several supply-chain attacks.
- **`mcp.connect` / dynamic tool discovery.** The agent cannot extend its own capabilities at runtime. The tool manifest is fixed at deployment time.
- **`secrets.read` / any credential access.** The agent has no path to credentials. The CI runs deployments using machine credentials; the agent never touches them.
- **`pr.merge`, `pr.close`, `branch.delete`.** All write-side PR/branch operations beyond `create` and `push` are absent. The agent can produce; humans dispose.

The principle: every capability the agent *doesn't* have is a class of attack and a class of failure mode the team doesn't have to defend against. Capability minimalism is the structural defense that holds when prompt-level defenses fail.

---

## Operational deployment notes

The agent runs as a containerized service:

- **Container image:** `retailco/order-service-coding-agent:1.3.0` (one image version per spec version; the image baked against spec v1.3 cannot be redeployed against spec v1.2 — versions are tied)
- **Trigger:** GitHub webhook on `issues.assigned` to the bot account, where label `agent-eligible` is present
- **Concurrency:** Max 3 concurrent runs across the team (cost cap)
- **Resource budget:** 4GB RAM, 1 vCPU per run; 30-minute wall-clock; $4 cost ceiling per run (P95 budget per spec §7)
- **Termination:** Run ends on PR creation, surface, or any budget exceeded
- **Logging:** Full trace to LangSmith with the issue ID as correlation; tool calls and arguments captured; sensitive content (file content >500 chars) referenced by hash in trace, full content in retained working storage with 30-day retention
- **Cost attribution:** Per-run cost tagged to the issue, the team, and the agent role; aggregated weekly into the cost-per-correct-output metric per [Four Signal Metrics](../../validate/06-metrics.md)

---

*Continue to [Evals and Acceptance](evals.md).*
