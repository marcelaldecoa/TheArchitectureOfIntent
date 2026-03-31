# Summary

[Cover](cover.md)
[Introduction](introduction.md)
[A Note on Pattern Language](preface.md)
[How to Read This Book](how-to-read.md)

---

# Foundations

*Philosophy and theory. Why intent matters, what changed, and the vocabulary for reasoning about it.*

## The Shift

- [Specification as the Primary Artifact](foundations/01-end-of-human-compiler.md)
- [The Orchestrator's Discipline](foundations/02-from-translation-to-orchestration.md)
- [Authorship Follows Intent](foundations/03-authorship-in-software.md)
- [Distributed Agency, Explicit Authority](foundations/04-where-agency-resides.md)
- [Judgment Encoded Before Power](foundations/05-when-power-scales-faster-than-judgment.md)
- [Architecture as Enforceable Law](foundations/06-why-architecture-must-become-law.md)

## The Theory

- [Intent Engineering as a Discipline](theory/01-what-is-intent-engineering.md)
- [The Intent–Implementation Boundary](theory/02-intent-vs-implementation.md)
- [Three Dimensions of Delegation](theory/03-agency-autonomy-responsibility.md)
- [Design for Reversibility](theory/04-reversibility-as-design-dimension.md)
- [Failure as Diagnostic Signal](theory/05-failure-as-design-signal.md)
- [The Moral Weight of Specification](theory/06-why-specs-are-moral-artifacts.md)

---

# The Pattern Language

*Reusable patterns. Each one is self-contained. Navigate by situation, not by sequence.*

## Governance & Architecture

- [Constitutional Archetypes](architecture/01-archetypes-as-constitutional-law.md)
- [The Five Archetypes](architecture/02-canonical-intent-archetypes.md)
  - [The Advisor](architecture/archetypes/advisor.md)
  - [The Executor](architecture/archetypes/executor.md)
  - [The Guardian](architecture/archetypes/guardian.md)
  - [The Synthesizer](architecture/archetypes/synthesizer.md)
  - [The Orchestrator](architecture/archetypes/orchestrator.md)
- [Four Dimensions of Governance](architecture/03-archetype-dimensions.md)
- [The Archetype Selection Tree](architecture/04-decision-tree.md)
- [Archetype Composition](architecture/05-composing-archetypes.md)
- [Governed Archetype Evolution](architecture/06-evolving-archetypes.md)
- [Delegated Definition Authority](operating/03-who-defines-archetypes.md)
- [Proportional Governance](operating/04-governance.md)
- [Intent Review Before Output Review](operating/05-reviewing-intent.md)
- [Four Signal Metrics](operating/06-metrics.md)
- [The Intent-Era Skill Matrix](operating/01-skill-matrix.md)
- [The Intent Architect](operating/02-from-engineer-to-architect.md)

## Specification

- [Spec-Driven Development](sdd/01-what-sdd-means.md)
- [The Spec as Control Surface](sdd/02-specs-as-control-surfaces.md)
- [Five Phases of the Spec](sdd/03-spec-lifecycle.md)
- [SpecKit](sdd/04-speckit.md)
- [Writing for Machine Execution](sdd/05-writing-specs-for-agents.md)
- [The Living Spec](sdd/06-living-specs.md)
- [The Canonical Spec Template](sdd/07-canonical-spec-template.md)

## Agents

- [Agents Defined by Structure](agents/01-what-agents-are.md)
- [Autonomy Without Agency](agents/02-autonomy-vs-agency.md)
- [The Executor Model](agents/03-agents-as-executors.md)
- [Least Capability](agents/04-tools-mcp-capability-boundaries.md)
- [Portable Domain Knowledge](agents/05-agent-skills.md)
- [Proportional Oversight](agents/06-human-oversight-models.md)
- [Six Failure Categories](agents/07-failure-modes.md)

## Knowledge & Context

- [The System Prompt](patterns/capability/system-prompt.md)
- [The Skill File](patterns/capability/skill-file.md)
- [Per-Task Context](patterns/capability/per-task-context.md)
- [Retrieval-Augmented Generation](patterns/capability/rag.md)
- [Long-Term Memory](patterns/capability/long-term-memory.md)
- [Context Window Budget](patterns/capability/context-budget.md)
- [Grounding with Verified Sources](patterns/capability/grounding.md)
- [The Tool Manifest](patterns/capability/tool-manifest.md)

## Integration & Tools

- [The Read-Only Tool](patterns/integration/read-only-tool.md)
- [The State-Changing Tool](patterns/integration/state-changing-tool.md)
- [The Idempotent Tool](patterns/integration/idempotent-tool.md)
- [The MCP Server](patterns/integration/mcp-server.md)
- [Direct Function Calling](patterns/integration/function-calling.md)
- [Code Execution Sandbox](patterns/integration/code-sandbox.md)
- [File System Access](patterns/integration/file-system-access.md)
  - [The Model Context Protocol](agents/mcp/01-what-is-mcp.md)
  - [Designing MCP Tools](agents/mcp/02-designing-mcp-tools.md)
  - [MCP Safety](agents/mcp/03-mcp-safety.md)

## Coordination

- [Sequential Pipeline](patterns/coordination/sequential-pipeline.md)
- [Parallel Fan-Out](patterns/coordination/parallel-fan-out.md)
- [Conditional Routing](patterns/coordination/conditional-routing.md)
- [Human-in-the-Loop Gate](patterns/coordination/human-gate.md)
- [Retry with Structured Feedback](patterns/coordination/retry-feedback.md)
- [Escalation Chain](patterns/coordination/escalation-chain.md)
- [Event-Driven Agent Activation](patterns/coordination/event-driven.md)
- [Supervisor Agent](patterns/coordination/supervisor.md)
- [Agent-to-Agent Contract](patterns/coordination/agent-contract.md)

## State & Memory

- [Session Isolation](patterns/state/session-isolation.md)
- [Shared Context Store](patterns/state/shared-context.md)
- [Checkpoint and Resume](patterns/state/checkpoint-resume.md)
- [Conversation History Management](patterns/state/conversation-history.md)
- [Agent Registry](patterns/state/agent-registry.md)
- [Artifact Store](patterns/state/artifact-store.md)

## Observability

- [Structured Execution Log](patterns/observability/execution-log.md)
- [Distributed Trace](patterns/observability/distributed-trace.md)
- [Anomaly Detection Baseline](patterns/observability/anomaly-baseline.md)
- [Cost Tracking per Spec](patterns/observability/cost-tracking.md)
- [Audit Trail](patterns/observability/audit-trail.md)
- [Health Check and Heartbeat](patterns/observability/health-check.md)

## Safety

- [Prompt Injection Defense](patterns/safety/prompt-injection-defense.md)
- [Output Validation Gate](patterns/safety/output-validation-gate.md)
- [Sensitive Data Boundary](patterns/safety/sensitive-data-boundary.md)
- [Graceful Degradation](patterns/safety/graceful-degradation.md)
- [Rate Limiting and Throttle](patterns/safety/rate-limiting.md)
- [Blast Radius Containment](patterns/safety/blast-radius-containment.md)

## Testing & Validation

- [Spec Conformance Test](patterns/testing/spec-conformance.md)
- [Adversarial Input Test](patterns/testing/adversarial-input.md)
- [Regression on Spec Change](patterns/testing/regression-spec-change.md)
- [Multi-Agent Integration Test](patterns/testing/multi-agent-integration.md)
- [Evaluation by Judge Agent](patterns/testing/judge-agent.md)

## Deployment & Lifecycle

- [Canary Deployment](patterns/deployment/canary.md)
- [Model Upgrade Validation](patterns/deployment/model-upgrade.md)
- [Spec Versioning](patterns/deployment/spec-versioning.md)
- [Rollback on Failure](patterns/deployment/rollback.md)
- [Agent Deprecation Path](patterns/deployment/deprecation.md)

---

# Applied Examples

*Patterns composed in real systems.*

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

# Repertoire & Reference

- [The Organizational Repertoire](repertoires/01-why-repertoires-matter.md)
- [The Intent Archetype Catalog](repertoires/02-archetype-catalog.md)
- [Spec Template Library](repertoires/03-spec-template-library.md)
  - [Feature Spec Template](repertoires/templates/feature-spec.md)
  - [Agent Instruction Template](repertoires/templates/agent-instruction.md)
  - [Integration Spec Template](repertoires/templates/integration-spec.md)
  - [Constraint Library Template](repertoires/templates/constraint-library.md)
- [Standards as Agent Skill Source](repertoires/04-code-standards.md)
  - [Standards for .NET / C#](repertoires/code-standards/dotnet.md)
  - [Standards for TypeScript / Node](repertoires/code-standards/typescript.md)
  - [Standards for Python](repertoires/code-standards/python.md)
  - [Standards for REST APIs](repertoires/code-standards/rest-apis.md)
  - [Standards for Infrastructure as Code](repertoires/code-standards/iac.md)
- [Validation & Acceptance Templates](repertoires/05-validation-templates.md)

---

# Appendices

- [Glossary of Intent Engineering](appendices/glossary.md)
- [The Pattern Index](appendices/pattern-index.md)
- [Reading List & References](appendices/references.md)
- [SpecKit Quick Reference](appendices/speckit-reference.md)
- [Archetype Quick-Select Card](appendices/archetype-card.md)
- [MCP & Agent Skills Quick Reference](appendices/mcp-and-skills-reference.md)
