# The Pattern Index

**Appendices** · *Appendix B*

---

> *"A pattern language is only useful if you can navigate it. This index is the navigation layer."*

---

This index organizes every chapter and pattern in the book by part, by theme, and by the problems they address. Use it to:

- Find a chapter you half-remember
- Discover all chapters that address a particular problem (cross-reference tables at the end)
- Navigate by archetype or by phase of the practice

---

## Part I: Foundations

*The slow, deliberate opening. These chapters earn the intellectual debt the rest of the book spends.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 1.1 | [The End of the Human Compiler](../foundations/01-end-of-human-compiler.md) | What changed about the developer's role when agents can write code? |
| 1.2 | [From Translation to Orchestration](../foundations/02-from-translation-to-orchestration.md) | If we no longer translate intent into code manually, what do we do instead? |
| 1.3 | [Authorship in Software](../foundations/03-authorship-in-software.md) | When an agent writes code, who is its author? |
| 1.4 | [Where Agency Resides](../foundations/04-where-agency-resides.md) | Where does decision-making authority actually live in an agent-augmented system? |
| 1.5 | [When Power Scales Faster Than Judgment](../foundations/05-when-power-scales-faster-than-judgment.md) | What is the structural risk when capability outpaces governance? |
| 1.6 | [Why Architecture Must Become Law](../foundations/06-why-architecture-must-become-law.md) | Why do architectural decisions need to be encoded, not assumed? |

---

## Part II: Theory of Intent Engineering

*The naming and formalizing. These chapters define the vocabulary everything else uses.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 2.1 | [What Is Intent Engineering](../theory/01-what-is-intent-engineering.md) | What is the discipline, and what makes it distinct from software engineering? |
| 2.2 | [Intent vs. Implementation](../theory/02-intent-vs-implementation.md) | Why is the distinction between what we want and how we build it load-bearing? |
| 2.3 | [Agency, Autonomy, and Responsibility](../theory/03-agency-autonomy-responsibility.md) | How do agency and responsibility relate when agents act? |
| 2.4 | [Reversibility as a Design Dimension](../theory/04-reversibility-as-design-dimension.md) | Why is reversibility a first-class design variable, not a quality concern? |
| 2.5 | [Failure as a Design Signal](../theory/05-failure-as-design-signal.md) | How do failure modes inform good architecture rather than just indicating bad luck? |
| 2.6 | [Why Specs Are Moral Artifacts](../theory/06-why-specs-are-moral-artifacts.md) | What does it mean that a spec is an ethical commitment, not just a technical document? |

---

## Part III: Intent Architecture

*The constitutional design. These chapters define the pre-commitments every system makes.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 3.1 | [Archetypes as Constitutional Law](../architecture/01-archetypes-as-constitutional-law.md) | Why are archetypes pre-commitments rather than post-hoc descriptions? |
| 3.2 | [The Canonical Intent Archetypes](../architecture/02-canonical-intent-archetypes.md) | What are the five archetypes and how are they distinguished? |
| — | [The Advisor Archetype](../architecture/archetypes/advisor.md) | Full specification of the information-surfacing archetype |
| — | [The Executor Archetype](../architecture/archetypes/executor.md) | Full specification of the bounded-action archetype |
| — | [The Guardian Archetype](../architecture/archetypes/guardian.md) | Full specification of the constraint-enforcement archetype |
| — | [The Synthesizer Archetype](../architecture/archetypes/synthesizer.md) | Full specification of the composite-output archetype |
| — | [The Orchestrator Archetype](../architecture/archetypes/orchestrator.md) | Full specification of the multi-agent coordination archetype |
| 3.3 | [Archetype Dimensions](../architecture/03-archetype-dimensions.md) | How do the four dimensions (agency, risk, oversight, reversibility) interact? |
| 3.4 | [Decision Tree for Archetype Selection](../architecture/04-decision-tree.md) | How do you choose the right archetype for a system? |
| 3.5 | [Composing Archetypes in Real Systems](../architecture/05-composing-archetypes.md) | How do multiple archetypes work together in a single deployment? |
| 3.6 | [Evolving Archetypes Without Dogma](../architecture/06-evolving-archetypes.md) | How do you update your archetype catalog as the technology and your domain change? |

---

## Part IV: Spec-Driven Development

*Method. These chapters turn philosophy into a repeatable practice.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 4.1 | [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md) | What is SDD and how is it different from requirements writing? |
| 4.2 | [Specs as Control Surfaces](../sdd/02-specs-as-control-surfaces.md) | How does a spec actually control what an agent does? |
| 4.3 | [The Spec Lifecycle](../sdd/03-spec-lifecycle.md) | What are the phases a spec moves through from intent to validation? |
| 4.4 | [SpecKit in the Architecture of Intent](../sdd/04-speckit.md) | How does the SpecKit toolchain support spec-driven development? |
| 4.5 | [Writing Specs for Agents, Not Humans](../sdd/05-writing-specs-for-agents.md) | What makes an agent-executable spec different from a human-readable one? |
| 4.6 | [Living Specs and Feedback Loops](../sdd/06-living-specs.md) | How do specs evolve after execution, and how do they capture learning? |
| 4.7 | [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) | What does a complete spec look like? (The reference template) |

---

## Part V: Agents & Execution

*Delegation mechanics. These chapters clarify how to use agents safely.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 5.1 | [What Agents Are (and Are Not)](../agents/01-what-agents-are.md) | What precisely is an agent, and what are its operational limits? |
| 5.2 | [Operational Autonomy vs. Genuine Agency](../agents/02-autonomy-vs-agency.md) | Why does the autonomy/agency distinction matter in practice? |
| 5.3 | [Agents as Executors of Intent](../agents/03-agents-as-executors.md) | How do agents relate to the intent encoded in specs? |
| 5.4 | [Tools, MCP, and Capability Boundaries](../agents/04-tools-mcp-capability-boundaries.md) | How do tool manifests and MCP define what an agent can reach? |
| — | [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md) | What is MCP and why does it matter for agent safety? |
| — | [Designing MCP Tools for Intent](../agents/mcp/02-designing-mcp-tools.md) | How do you design tools that enforce intent rather than expose raw capability? |
| — | [MCP Tool Safety and Constraints](../agents/mcp/03-mcp-safety.md) | What safety patterns apply to MCP tool design? |
| 5.5 | [Agent Skills: Packaging Domain Knowledge](../agents/05-agent-skills.md) | What are SKILL.md files and how do they carry domain context? |
| 5.6 | [Human Oversight Models](../agents/06-human-oversight-models.md) | What are the four oversight models and when does each apply? |
| 5.7 | [Failure Modes in Agent Systems](../agents/07-failure-modes.md) | What are the canonical failure modes in agent systems and how are they diagnosed? |

---

## Part VI: Standards & Repertoires

*Institutional acceleration. These chapters build the infrastructure that makes teams fast.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 6.1 | [Why Repertoires Matter](../repertoires/01-why-repertoires-matter.md) | What is a repertoire and why does investing in it compound? |
| 6.2 | [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) | What does a decision-ready archetype catalog entry look like? |
| 6.3 | [Spec Template Library](../repertoires/03-spec-template-library.md) | How are spec templates organized and maintained? |
| — | [Feature Spec Template](../repertoires/templates/feature-spec.md) | Template for feature-development agent tasks |
| — | [Agent Instruction Template](../repertoires/templates/agent-instruction.md) | Template for agent system-prompt instructions |
| — | [Integration Spec Template](../repertoires/templates/integration-spec.md) | Template for integration and API agent tasks |
| — | [Constraint Library Template](../repertoires/templates/constraint-library.md) | Template for capturing reusable constraint sets |
| 6.4 | [Code Standards for Agent-Generated Systems](../repertoires/04-code-standards.md) | How are code standards structured for agent validation? |
| — | [Standards for .NET / C#](../repertoires/code-standards/dotnet.md) | .NET platform constraints, patterns, and validation rules |
| — | [Standards for TypeScript / Node](../repertoires/code-standards/typescript.md) | TypeScript platform constraints, patterns, and validation rules |
| — | [Standards for Python](../repertoires/code-standards/python.md) | Python platform constraints, patterns, and validation rules |
| — | [Standards for REST APIs](../repertoires/code-standards/rest-apis.md) | REST API design constraints and OpenAPI requirements |
| — | [Standards for Infrastructure as Code](../repertoires/code-standards/iac.md) | IaC constraints for Bicep, Terraform, and YAML manifests |
| 6.5 | [Validation & Acceptance Templates](../repertoires/05-validation-templates.md) | What does a reusable acceptance test template look like? |

---

## Part VII: Operating the System

*People, skills, and governance. These chapters address organizational transformation.*

| # | Title | Key question addressed |
|---|-------|----------------------|
| 7.1 | [The Modern Engineering Skill Matrix](../operating/01-skill-matrix.md) | How do value-producing skills shift in an agent-augmented practice? |
| 7.2 | [From Senior Engineer to Intent Architect](../operating/02-from-engineer-to-architect.md) | What is the identity and role transition for experienced engineers? |
| 7.3 | [Who Is Allowed to Define Archetypes](../operating/03-who-defines-archetypes.md) | How is authority over the archetype catalog governed? |
| 7.4 | [Governance Without Bureaucracy](../operating/04-governance.md) | What is the lightest governance structure that prevents both chaos and bureaucracy? |
| 7.5 | [Reviewing Intent, Not Code](../operating/05-reviewing-intent.md) | How does spec review work as a practice, and how does it differ from code review? |
| 7.6 | [Metrics That Actually Matter](../operating/06-metrics.md) | What should be measured in an agent-augmented practice, and what should not? |

---

## Part VIII: Applied Examples

*The patterns in action. Use these to calibrate your own system designs.*

| Title | What it demonstrates |
|-------|---------------------|
| [How to Use These Examples](../examples/00-how-to-use.md) | Reading guide for Part VIII |
| [Designing an AI Customer Support System](../examples/01-ai-customer-support/README.md) | Multi-agent Orchestrator + Executor + Guardian + Advisor in a live customer system |
| → [Selecting the Archetypes](../examples/01-ai-customer-support/archetypes.md) | Full five-archetype evaluation for the customer support scenario |
| → [Writing the Spec](../examples/01-ai-customer-support/spec.md) | Complete annotated SDD spec for the Account Executor |
| → [Agent Instructions](../examples/01-ai-customer-support/agent-instructions.md) | Full operational instructions derived from the spec |
| → [Validating Outcomes](../examples/01-ai-customer-support/validation.md) | 14-test acceptance suite with one instruction gap found |
| → [Post-mortem Through Intent](../examples/01-ai-customer-support/postmortem.md) | $0.00 refund incident — spec gap traced and closed |
| [A Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md) | Synthesizer-Executor-Guardian pipeline with no live human |
| → [Selecting the Archetypes](../examples/02-code-generation-pipeline/archetypes.md) | Orchestrator rejected; Synthesizer as primary coordinator |
| → [Writing the Spec](../examples/02-code-generation-pipeline/spec.md) | Complete annotated spec for the Scaffold Synthesizer |
| → [Agent Instructions](../examples/02-code-generation-pipeline/agent-instructions.md) | Operational (non-conversational) instructions for all three pipeline agents |
| → [Validating Outcomes](../examples/02-code-generation-pipeline/validation.md) | 9-test pipeline acceptance suite; cross-component consistency testing |

---

## Cross-Reference: By Problem

*Find patterns by the problem you are trying to solve.*

### "I don't know which archetype to use"
- [Decision Tree for Archetype Selection](../architecture/04-decision-tree.md) — 3.4
- [Archetype Quick-Select Card](archetype-card.md) — Appendix E
- [Selecting the Archetypes (Example 1)](../examples/01-ai-customer-support/archetypes.md)
- [Selecting the Archetypes (Example 2)](../examples/02-code-generation-pipeline/archetypes.md)

### "I don't know how to write a good spec"
- [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md) — 4.1
- [Specs as Control Surfaces](../sdd/02-specs-as-control-surfaces.md) — 4.2
- [Writing Specs for Agents, Not Humans](../sdd/05-writing-specs-for-agents.md) — 4.5
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — 4.7
- [Writing the Spec (Example 1)](../examples/01-ai-customer-support/spec.md) — annotated real spec
- [SpecKit Quick Reference](speckit-reference.md) — Appendix D

### "I don't know what constraints to include"
- [Specs as Control Surfaces](../sdd/02-specs-as-control-surfaces.md) — 4.2
- [Constraint Library Template](../repertoires/templates/constraint-library.md)
- [Writing the Spec — NOT-authorized section](../examples/01-ai-customer-support/spec.md) — §4 annotated

### "Something went wrong and I need to diagnose it"
- [Failure Modes in Agent Systems](../agents/07-failure-modes.md) — 5.7
- [Failure as a Design Signal](../theory/05-failure-as-design-signal.md) — 2.5
- [Post-mortem Through Intent](../examples/01-ai-customer-support/postmortem.md) — worked example
- [The Spec Gap Log](../sdd/06-living-specs.md) — 4.6

### "I need to set up governance"
- [Who Is Allowed to Define Archetypes](../operating/03-who-defines-archetypes.md) — 7.3
- [Governance Without Bureaucracy](../operating/04-governance.md) — 7.4
- [Reviewing Intent, Not Code](../operating/05-reviewing-intent.md) — 7.5

### "I need to measure and report on the practice"
- [Metrics That Actually Matter](../operating/06-metrics.md) — 7.6
- [Living Specs and Feedback Loops](../sdd/06-living-specs.md) — 4.6

### "I need to design a multi-agent system"
- [Composing Archetypes in Real Systems](../architecture/05-composing-archetypes.md) — 3.5
- [Orchestrator Archetype](../architecture/archetypes/orchestrator.md)
- [Designing an AI Customer Support System](../examples/01-ai-customer-support/README.md) — Example 1
- [A Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md) — Example 2

### "I need to build or expand a team repertoire"
- [Why Repertoires Matter](../repertoires/01-why-repertoires-matter.md) — 6.1
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) — 6.2
- [Spec Template Library](../repertoires/03-spec-template-library.md) — 6.3
- [Validation & Acceptance Templates](../repertoires/05-validation-templates.md) — 6.5

### "I need to help my team understand what changes"
- [From Translation to Orchestration](../foundations/02-from-translation-to-orchestration.md) — 1.2
- [The Modern Engineering Skill Matrix](../operating/01-skill-matrix.md) — 7.1
- [From Senior Engineer to Intent Architect](../operating/02-from-engineer-to-architect.md) — 7.2

### "I need to design safe agent tools"
- [Tools, MCP, and Capability Boundaries](../agents/04-tools-mcp-capability-boundaries.md) — 5.4
- [Designing MCP Tools for Intent](../agents/mcp/02-designing-mcp-tools.md)
- [MCP Tool Safety and Constraints](../agents/mcp/03-mcp-safety.md)
- [Human Oversight Models](../agents/06-human-oversight-models.md) — 5.6

---

## Cross-Reference: By Archetype

*Find all chapters relevant to a specific archetype.*

| Archetype | Definitional chapter | Used in example | Governance | Constraints |
|-----------|---------------------|----------------|-----------|-------------|
| Advisor | [3.2 / advisor.md](../architecture/archetypes/advisor.md) | Example 1 (Policy Advisor) | [7.3](../operating/03-who-defines-archetypes.md) | [6.3 templates](../repertoires/03-spec-template-library.md) |
| Executor | [3.2 / executor.md](../architecture/archetypes/executor.md) | Example 1 (Account Executor) | [7.3](../operating/03-who-defines-archetypes.md) | [6.5](../repertoires/05-validation-templates.md) |
| Guardian | [3.2 / guardian.md](../architecture/archetypes/guardian.md) | Example 1 (Compliance Guardian), Example 2 (Standards Guardian) | [7.3](../operating/03-who-defines-archetypes.md) | [5.4](../agents/04-tools-mcp-capability-boundaries.md) |
| Synthesizer | [3.2 / synthesizer.md](../architecture/archetypes/synthesizer.md) | Example 2 (Scaffold Synthesizer) | [7.3](../operating/03-who-defines-archetypes.md) | [6.3 templates](../repertoires/03-spec-template-library.md) |
| Orchestrator | [3.2 / orchestrator.md](../architecture/archetypes/orchestrator.md) | Example 1 (Inquiry Orchestrator) | [7.3](../operating/03-who-defines-archetypes.md) | [5.6](../agents/06-human-oversight-models.md) |


