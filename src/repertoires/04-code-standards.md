# Pattern 6.4 — Standards as Agent Skill Source

**Part VI: Standards & Repertoires** · *4 of 5*

---

> *"The agent writes what it infers. When it has no standard to infer from, it averages everything it was ever trained on. The result is technically correct and organizationally incoherent."*

---

## Context

When agents generate code, they draw on a distribution: billions of examples across countless codebases, styles, conventions, and eras. Without an explicit standard to follow, an agent will synthesize code that is statistically representative of that distribution — competent by average, coherent by none of your team's specific conventions.

The result is code that usually compiles, often passes tests, and consistently requires reformatting, renaming, restructuring, and style alignment before it can be merged. The agent's technical output is correct; its organizational fit is poor. Code review becomes an exercise in explaining implicit norms to a system that cannot read minds.

Code standards for agent-generated systems solve this by externalizing what was previously implicit — making the conventions your team holds available to the agent as explicit instructions it can apply during generation.

---

## The Problem

Two failure modes emerge when code standards are absent from an agent practice:

**Style incoherence.** The agent writes C# using `camelCase` property names in one file, `PascalCase` in another, a mix of both in a third — because all three appear in its training data. It uses `var` liberally in some methods and explicit types in others. It handles errors with exceptions in some functions and return types in others. The code passes review but requires constant nit-corrections that slow review cycles and train reviewers to focus on style rather than logic.

**Pattern divergence.** The agent generates a service class with constructor injection in one feature, static factories in another, and service locators in a third — all patterns it has seen used, none of them your pattern. It writes async code that correctly awaits but doesn't use your team's standard cancellation token handling. The code is correct in isolation; it does not fit the codebase.

Both failures share the same root cause: the agent is inferring your standards from incomplete evidence. It sees some of your code in its context window and some of its training data, and it blends them. The blend is poor.

---

## Forces

- **Agent training distribution vs. organizational standards.** Agents write code based on training averages. Without explicit standards, agent output varies in style and quality.
- **Standard overhead vs. consistency benefit.** Maintaining code standards documents requires ongoing effort. But the cost of inconsistent agent-generated code compounds in maintenance and review.
- **Human-oriented vs. agent-oriented standards.** Traditional standards assume human readers who can interpret guidelines. Agent-oriented standards must be precise enough to function as skill source material.
- **Adoption friction vs. quality improvement.** Integrating standards into the development workflow requires tool changes. But once integrated, every agent execution benefits.

---

## The Solution

### Code Standards as Agent Skills

Code standards in an agent-driven practice are not primarily review checklists. They are **the source material for code-related agent skills**. The standards document for TypeScript is the basis for the `typescript-standards` skill. The REST API standards document is the basis for the `api-design` skill.

When an agent is generating code, it loads the relevant skill, and the skill's instructions carry your organization's actual conventions — not the statistical average of the internet's. The output quality improvement is measurable and immediate.

This changes how standards documents should be written. A traditional code style guide is written for the human reviewer: comprehensive, organized, with rationale and examples of correct and incorrect patterns. An agent-ready standards document adds precision that the human might infer: explicit enumerations (not "use clear names" but "use `PascalCase` for types, `camelCase` for methods and fields, `SCREAMING_SNAKE_CASE` for constants"), explicit negatives ("don't use `dynamic`"), and decision rules for ambiguous cases ("when a class exceeds 300 lines, split along logical boundaries — prefer splitting by domain concept, not by access-level grouping").

### The Five Standard Pages

Each language and platform has its own standards document in the library. The current set covers the platforms most commonly used with agent-generated code. Each document follows the same structure:

1. **Naming conventions** — comprehensive, with explicit rules for every identifier type
2. **Code organization** — file layout, namespace/module structure, class organization
3. **Patterns and anti-patterns** — canonical patterns to use; explicit list of patterns to avoid
4. **Error handling** — the single approved approach; no alternatives to "use judgment"
5. **Async conventions** — how async/sync boundaries are managed
6. **Testing** — test organization, test naming, what must be tested, what need not be
7. **Performance invariants** — rules the agent must not violate regardless of what seems clever

The full standards for each platform are in their respective sections:

- [Standards for .NET / C#](code-standards/dotnet.md)
- [Standards for TypeScript / Node](code-standards/typescript.md)
- [Standards for Python](code-standards/python.md)
- [Standards for REST APIs](code-standards/rest-apis.md)
- [Standards for Infrastructure as Code](code-standards/iac.md)

### Using Standards in Specs

The spec's Section 11 (Agent Execution Instructions) should reference the applicable standards explicitly:

```
**Skills to load**
- `typescript-standards`: This task generates TypeScript service classes. Apply naming,
  async, and error handling conventions.
- `rest-api-standards`: New endpoints are being added. Apply naming, versioning, and
  error response conventions.
```

For code generation tasks, the applicable skills are almost always the most important Section 11 declaration. An Executor agent writing code without a standards skill is working without your codebase's conventions — its output will be generically correct and specifically inconsistent.

### Maintenance Discipline

Code standards drift when maintained inconsistently. Some specific risks:

**New pattern adoption without standard update.** Your team adopts a new approach — say, switching from a `Result<T>` type to thrown application exceptions. Specs for the first three months after the change may carry the old pattern (from practitioner habit) or the new pattern (for practitioners who know). The agent, reading both, will be inconsistent. Standards must be updated at the moment of pattern adoption, not retrospectively.

**Adding without pruning.** Standards grow through incident response — "add a rule to prevent this" — but rarely shrink. After a few years, some rules are obsolete (they applied to a library you no longer use) and others are contradicted by newer rules. Quarterly review should remove obsolete rules, not just add new ones.

**Standard/codebase divergence.** The standard says one thing; most of the existing code does another. The agent reads both and averages them. Decide: update the codebase to match the standard, or update the standard to match the codebase. Never leave the divergence unresolved — it is a permanent source of inconsistent agent output.

---

## Resulting Context

After applying this pattern:

- **Agent output is consistent and reviewable.** When agents load code standards as skills, their output converges on the organization's expectations.
- **Standards become agent skill source material.** Code standards documents feed directly into agent skills, closing the loop between human guidance and agent execution.
- **Review burden decreases over time.** As agents consistently follow standards, code review can focus on logic and intent rather than style and convention.
- **New pattern adoption flows through standards.** When the organization adopts a new pattern, updating the standard propagates the change to all future agent output.

---

## Therefore

> **Code standards for agent-generated systems are not review checklists — they are the source material for code-related agent skills. Written with explicit rules, enumerated conventions, and decision trees for ambiguous cases, they give agents the organizational context needed to produce code that is not just technically correct but fits your codebase. They must be maintained in sync with codebase evolution; a drifted standard is worse than no standard because it produces confidently inconsistent output.**

---

## Connections

**This pattern assumes:**
- [The Organizational Repertoire](01-why-repertoires-matter.md)
- [Portable Domain Knowledge](../agents/05-agent-skills.md)
- [The Canonical Spec Template — Section 11](../sdd/07-canonical-spec-template.md)

**This pattern enables:**
- [Standards for .NET / C#](code-standards/dotnet.md)
- [Standards for TypeScript / Node](code-standards/typescript.md)
- [Standards for Python](code-standards/python.md)
- [Standards for REST APIs](code-standards/rest-apis.md)
- [Standards for Infrastructure as Code](code-standards/iac.md)
- [Validation & Acceptance Templates](05-validation-templates.md)

---

*Next: [Standards for .NET / C# →](code-standards/dotnet.md)*


