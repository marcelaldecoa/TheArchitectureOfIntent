# Summary

[Introduction](introduction.md)
[A Note on Pattern Language](preface.md)
[How to Read This Book](how-to-read.md)

---

# Part I: Foundations

*Why this exists at all. This section is intentionally slow and reflective. It earns the right to exist.*

- [The End of the Human Compiler](foundations/01-end-of-human-compiler.md)
- [From Translation to Orchestration](foundations/02-from-translation-to-orchestration.md)
- [Authorship in Software](foundations/03-authorship-in-software.md)
- [Where Agency Resides](foundations/04-where-agency-resides.md)
- [When Power Scales Faster Than Judgment](foundations/05-when-power-scales-faster-than-judgment.md)
- [Why Architecture Must Become Law](foundations/06-why-architecture-must-become-law.md)

---

# Part II: Theory of Intent Engineering

*Naming the discipline. Here we formalize what was implicit.*

- [What Is Intent Engineering](theory/01-what-is-intent-engineering.md)
- [Intent vs. Implementation](theory/02-intent-vs-implementation.md)
- [Agency, Autonomy, and Responsibility](theory/03-agency-autonomy-responsibility.md)
- [Reversibility as a Design Dimension](theory/04-reversibility-as-design-dimension.md)
- [Failure as a Design Signal](theory/05-failure-as-design-signal.md)
- [Why Specs Are Moral Artifacts](theory/06-why-specs-are-moral-artifacts.md)

---

# Part III: Intent Architecture

*Constitutional design. The load-bearing section of the entire book.*

- [Archetypes as Constitutional Law](architecture/01-archetypes-as-constitutional-law.md)
- [The Canonical Intent Archetypes](architecture/02-canonical-intent-archetypes.md)
  - [The Advisor Archetype](architecture/archetypes/advisor.md)
  - [The Executor Archetype](architecture/archetypes/executor.md)
  - [The Guardian Archetype](architecture/archetypes/guardian.md)
  - [The Synthesizer Archetype](architecture/archetypes/synthesizer.md)
  - [The Orchestrator Archetype](architecture/archetypes/orchestrator.md)
- [Archetype Dimensions](architecture/03-archetype-dimensions.md)
- [Decision Tree for Archetype Selection](architecture/04-decision-tree.md)
- [Composing Archetypes in Real Systems](architecture/05-composing-archetypes.md)
- [Evolving Archetypes Without Dogma](architecture/06-evolving-archetypes.md)

---

# Part IV: Spec-Driven Development

*Turning intent into executable form. Now philosophy turns into method.*

- [What Spec-Driven Development Really Means](sdd/01-what-sdd-means.md)
- [Specs as Control Surfaces](sdd/02-specs-as-control-surfaces.md)
- [The Spec Lifecycle: From Intent to Validation](sdd/03-spec-lifecycle.md)
- [SpecKit in the Architecture of Intent](sdd/04-speckit.md)
- [Writing Specs for Agents, Not Humans](sdd/05-writing-specs-for-agents.md)
- [Living Specs and Feedback Loops](sdd/06-living-specs.md)
- [The Canonical Spec Template](sdd/07-canonical-spec-template.md)

---

# Part V: Agents & Execution

*Delegating labor safely. This is where modern tooling fits without dominating the narrative.*

- [What Agents Are (and Are Not)](agents/01-what-agents-are.md)
- [Operational Autonomy vs. Genuine Agency](agents/02-autonomy-vs-agency.md)
- [Agents as Executors of Intent](agents/03-agents-as-executors.md)
- [Tools, MCP, and Capability Boundaries](agents/04-tools-mcp-capability-boundaries.md)
  - [The Model Context Protocol](agents/mcp/01-what-is-mcp.md)
  - [Designing MCP Tools for Intent](agents/mcp/02-designing-mcp-tools.md)
  - [MCP Tool Safety and Constraints](agents/mcp/03-mcp-safety.md)
- [Agent Skills: Packaging Domain Knowledge](agents/05-agent-skills.md)
- [Human Oversight Models](agents/06-human-oversight-models.md)
- [Failure Modes in Agent Systems](agents/07-failure-modes.md)

---

# Part VI: Standards & Repertoires

*Caching wisdom. The section that accelerates teams.*

- [Why Repertoires Matter](repertoires/01-why-repertoires-matter.md)
- [The Intent Archetype Catalog](repertoires/02-archetype-catalog.md)
- [Spec Template Library](repertoires/03-spec-template-library.md)
  - [Feature Spec Template](repertoires/templates/feature-spec.md)
  - [Agent Instruction Template](repertoires/templates/agent-instruction.md)
  - [Integration Spec Template](repertoires/templates/integration-spec.md)
  - [Constraint Library Template](repertoires/templates/constraint-library.md)
- [Code Standards for Agent-Generated Systems](repertoires/04-code-standards.md)
  - [Standards for .NET / C#](repertoires/code-standards/dotnet.md)
  - [Standards for TypeScript / Node](repertoires/code-standards/typescript.md)
  - [Standards for Python](repertoires/code-standards/python.md)
  - [Standards for REST APIs](repertoires/code-standards/rest-apis.md)
  - [Standards for Infrastructure as Code](repertoires/code-standards/iac.md)
- [Validation & Acceptance Templates](repertoires/05-validation-templates.md)

---

# Part VII: Operating the System

*People, skills, governance. Where transformation becomes real.*

- [The Modern Engineering Skill Matrix](operating/01-skill-matrix.md)
- [From Senior Engineer to Intent Architect](operating/02-from-engineer-to-architect.md)
- [Who Is Allowed to Define Archetypes](operating/03-who-defines-archetypes.md)
- [Governance Without Bureaucracy](operating/04-governance.md)
- [Reviewing Intent, Not Code](operating/05-reviewing-intent.md)
- [Metrics That Actually Matter](operating/06-metrics.md)

---

# Part VIII: Applied Examples

*Proof through reality. This is where everything converges.*

- [How to Use These Examples](examples/00-how-to-use.md)
- [Designing an AI Customer Support System](examples/01-ai-customer-support/README.md)
  - [Selecting the Archetypes](examples/01-ai-customer-support/archetypes.md)
  - [Writing the Spec](examples/01-ai-customer-support/spec.md)
  - [Agent Instructions](examples/01-ai-customer-support/agent-instructions.md)
  - [Validating Outcomes](examples/01-ai-customer-support/validation.md)
  - [Post-mortem Through Intent](examples/01-ai-customer-support/postmortem.md)
- [A Code Generation Pipeline](examples/02-code-generation-pipeline/README.md)
  - [Selecting the Archetypes](examples/02-code-generation-pipeline/archetypes.md)
  - [Writing the Spec](examples/02-code-generation-pipeline/spec.md)
  - [Agent Instructions](examples/02-code-generation-pipeline/agent-instructions.md)
  - [Validating Outcomes](examples/02-code-generation-pipeline/validation.md)

---

# Appendices

- [Glossary of Intent Engineering](appendices/glossary.md)
- [The Pattern Index](appendices/pattern-index.md)
- [Reading List & References](appendices/references.md)
- [SpecKit Quick Reference](appendices/speckit-reference.md)
- [Archetype Quick-Select Card](appendices/archetype-card.md)
- [MCP & Agent Skills Quick Reference](appendices/mcp-and-skills-reference.md)
