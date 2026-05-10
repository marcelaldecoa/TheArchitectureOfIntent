# The Pattern Index

**Appendices** · *Appendix B*

---

> *"A field guide is only useful if you can navigate it. This index is the navigation layer."*

---

This index lists every chapter and pattern in the book by part, by category, and by the problem they address. Use it to:

- Find a chapter you half-remember
- Discover all chapters relevant to a particular problem
- Navigate by archetype or by phase of the practice

---

## Part 1 — Decisions

*The decisions you commit to before you start.*

| Title | Key question |
|-------|-------------|
| [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md) | What kind of system is this — Advisor, Executor, Guardian, Synthesizer, or Orchestrator? |
| [The Advisor](../architecture/archetypes/advisor.md) | Information-surfacing archetype: full specification |
| [The Executor](../architecture/archetypes/executor.md) | Bounded-action archetype: full specification |
| [The Guardian](../architecture/archetypes/guardian.md) | Constraint-enforcement archetype: full specification |
| [The Synthesizer](../architecture/archetypes/synthesizer.md) | Composite-output archetype: full specification |
| [The Orchestrator](../architecture/archetypes/orchestrator.md) | Multi-agent coordination archetype: full specification |
| [Calibrate the Four Dimensions](../theory/03-agency-autonomy-responsibility.md) | How much autonomy, agency, responsibility, and reversibility does this system get? |
| [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) | How do agency, risk, oversight, and reversibility interact in formal governance terms? |
| [The Archetype Selection Tree](../architecture/04-decision-tree.md) | How do you choose the right archetype when the answer isn't obvious? |
| [Composing Archetypes](../architecture/05-composing-archetypes.md) | How do multiple archetypes work together in a single deployment? |
| [Governed Archetype Evolution](../architecture/06-evolving-archetypes.md) | How do you update the archetype catalog as the technology and your domain change? |
| [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) | How do you govern an N-agent system as a system, not as N individually-specified components? |
| [Intent vs. Implementation](../theory/02-intent-vs-implementation.md) | When something goes wrong, was the spec wrong, or did the agent fail to execute it? |
| [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) | What are the seven failure categories, and how do you diagnose them? |
| [The Intent Design Session](../theory/07-intent-design-session.md) | What is the time-boxed working ritual that turns the framework into a session a team can run? |

---

## Part 2 — The Spec

*How to write the artifact the agent executes against.*

| Title | Key question |
|-------|-------------|
| [Spec-Driven Development](../sdd/01-what-sdd-means.md) | What is SDD and how is it different from requirements writing? |
| [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md) | How does a spec actually control what an agent does? |
| [The Spec Lifecycle](../sdd/03-spec-lifecycle.md) | What phases does a spec move through from intent to validation? |
| [Writing for Machine Execution](../sdd/05-writing-specs-for-agents.md) | What makes an agent-executable spec different from a human-readable one? |
| [The Living Spec](../sdd/06-living-specs.md) | How do specs evolve after execution and capture learning? |
| [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) | What does a complete spec look like? |
| [Architectural Decision Records](../sdd/08-architectural-decision-records.md) | How do ADRs and specs relate; when to write each; the canonical ADR format with Spec Mapping section |
| [SpecKit](../sdd/04-speckit.md) | How does the SpecKit toolchain support spec-driven development? |

---

## Part 3 — The Agent

*What agents are structurally, what capabilities they need, how to bound them.*

| Title | Key question |
|-------|-------------|
| [What Agents Are](../agents/01-what-agents-are.md) | What precisely is an agent, and what are its operational limits? |
| [Autonomy Without Agency](../agents/02-autonomy-vs-agency.md) | Why does the autonomy/agency distinction matter in practice? |
| [The Executor Model](../agents/03-agents-as-executors.md) | How do agents relate to the intent encoded in specs? |
| [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) | How do tool manifests and MCP define what an agent can reach? |
| [Portable Domain Knowledge](../agents/05-agent-skills.md) | What are SKILL.md files and how do they carry domain context? |
| [Coding Agents](../agents/08-coding-agents.md) | How do the framework's archetypes, spec, and oversight apply to the most-deployed agent class (Cursor, Cline, Devin, Claude Code)? |
| [Computer-Use Agents](../agents/09-computer-use-agents.md) | How do the framework's disciplines apply to GUI-acting agents (Claude Computer Use, OpenAI Operator, Gemini computer use); the new Cat 7 Perceptual Failure category |

### Knowledge & Context

| Title | Purpose |
|-------|---------|
| [The System Prompt](../patterns/capability/system-prompt.md) | The agent's constitution at runtime |
| [The Skill File](../patterns/capability/skill-file.md) | Encoding domain knowledge the agent can reference |
| [The Tool Manifest](../patterns/capability/tool-manifest.md) | Declaring what tools the agent can access |
| [Per-Task Context](../patterns/capability/per-task-context.md) | Task-scoped context provision |
| [Retrieval-Augmented Generation](../patterns/capability/rag.md) | Grounding outputs in retrieved content |
| [Long-Term Memory](../patterns/capability/long-term-memory.md) | Cross-session memory patterns |
| [Context Window Budget](../patterns/capability/context-budget.md) | Managing context window allocation |
| [Grounding with Verified Sources](../patterns/capability/grounding.md) | Constraining outputs to verified facts |

### Tools and MCP

| Title | Purpose |
|-------|---------|
| [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md) | Protocol overview |
| [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md) | Designing tools that enforce intent rather than expose raw capability |
| [MCP Safety](../agents/mcp/03-mcp-safety.md) | Safety considerations for MCP tool design |
| [The Read-Only Tool](../patterns/integration/read-only-tool.md) | Boundary pattern for read-only access |
| [The State-Changing Tool](../patterns/integration/state-changing-tool.md) | Pattern for stateful operations |
| [The Idempotent Tool](../patterns/integration/idempotent-tool.md) | Idempotency guarantee pattern |
| [The MCP Server](../patterns/integration/mcp-server.md) | Standard MCP server design |
| [Direct Function Calling](../patterns/integration/function-calling.md) | Tool calling protocol |
| [Code Execution Sandbox](../patterns/integration/code-sandbox.md) | Safe code execution boundary |
| [File System Access](../patterns/integration/file-system-access.md) | File I/O patterns |

---

## Part 4 — Oversight, Safety & Operations

| Title | Purpose |
|-------|---------|
| [Proportional Oversight](../agents/06-human-oversight-models.md) | The four oversight models (Monitoring / Periodic / Output Gate / Pre-authorized) |
| [Human-in-the-Loop Gate](../patterns/coordination/human-gate.md) | Structured decision gate before consequential actions |
| [Retry with Structured Feedback](../patterns/coordination/retry-feedback.md) | Structured retry that improves first-pass execution |
| [Escalation Chain](../patterns/coordination/escalation-chain.md) | Escalation hierarchy design |

### Safety

| Title | Purpose |
|-------|---------|
| [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | Multi-layer defense for any externally-facing agent |
| [Output Validation Gate](../patterns/safety/output-validation-gate.md) | Tiered validation (programmatic → Guardian → human) |
| [Sensitive Data Boundary](../patterns/safety/sensitive-data-boundary.md) | PII/secret handling pattern |
| [Graceful Degradation](../patterns/safety/graceful-degradation.md) | Partial-failure handling |
| [Rate Limiting and Throttle](../patterns/safety/rate-limiting.md) | Preventing runaway execution |
| [Blast Radius Containment](../patterns/safety/blast-radius-containment.md) | Limiting the consequence of a single failure |

### Observability

| Title | Purpose |
|-------|---------|
| [Structured Execution Log](../patterns/observability/execution-log.md) | Auditable execution trace |
| [Cost Tracking per Spec](../patterns/observability/cost-tracking.md) | Cost attribution per agent and spec |
| [Distributed Trace](../patterns/observability/distributed-trace.md) | Tracing multi-agent flows |
| [Health Check and Heartbeat](../patterns/observability/health-check.md) | Agent health monitoring |
| [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md) | Anomaly detection setup |

### Testing & Validation

| Title | Purpose |
|-------|---------|
| [Spec Conformance Testing](../patterns/testing/spec-conformance.md) | Making spec constraints testable and verifiable |
| [Adversarial Input Test](../patterns/testing/adversarial-input.md) | Robustness testing |
| [Multi-Agent Integration Test](../patterns/testing/multi-agent-integration.md) | Testing agent coordination |
| [Evaluation by Judge Agent](../patterns/testing/judge-agent.md) | Using an agent to validate another agent's output |

---

## Part 5 — Ship

| Title | Purpose |
|-------|---------|
| [Canary Deployment](../patterns/deployment/canary.md) | Safe spec rollout |
| [Rollback on Failure](../patterns/deployment/rollback.md) | Reverting a broken spec |
| [Spec Versioning](../patterns/deployment/spec-versioning.md) | Managing spec versions |
| [Model Upgrade Validation](../patterns/deployment/model-upgrade.md) | Re-validating when the underlying model changes |
| [Agent Deprecation Path](../patterns/deployment/deprecation.md) | Sunsetting old agents and specs |
| [Proportional Governance](../operating/04-governance.md) | The lightest governance structure that prevents both chaos and bureaucracy |
| [Intent Review Before Output Review](../operating/05-reviewing-intent.md) | Spec review as a practice |
| [Four Signal Metrics](../operating/06-metrics.md) | What to measure, what not to |
| [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) | The four-level eval stack: unit asserts, spec acceptance, regression, production sampling |
| [Red-Team Protocol](../operating/08-red-team-protocol.md) | Four red-team batteries (pre-launch, per-release, monthly regression, quarterly fresh-attacks) feeding the spec gap log |
| [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Model-tier selection, prompt caching strategy, latency budget decomposition, anti-patterns |
| [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md) | Prompt caching as architecture, not optimization: layered prompt structure, cache breakpoints, prompt-stability spec constraint, eval-time pre-warm, `cache_hit_rate` as first-class telemetry |
| [Production Telemetry](../operating/10-production-telemetry.md) | The integrated telemetry stack: what to instrument, what to retain, alerts vs monitors, OpenTelemetry GenAI semantic conventions |
| [Adoption Playbook](../operating/11-adoption-playbook.md) | How to introduce SDD discipline to a team without big-bang rollout, spec theater, or governance over-investment; CI/CD wiring with hard-gate / soft-gate / observe tiers |
| [Mapping the Framework to the DevSquad 8-Phase Cadence](../operating/12-devsquad-mapping.md) | Phase-by-phase mapping of the book's artifacts and disciplines into Microsoft DevSquad Copilot's 8-phase iterative cycle |
| [Co-adoption with DevSquad Copilot](../operating/13-co-adoption-with-devsquad.md) | The minimum additions from this book that give a DevSquad team the most leverage; vocabulary translation; 30-day co-adoption plan |

---

## Part 6 — Worked Pilots

| Title | Demonstrates |
|-------|-------------|
| [How to Use These Examples](../examples/00-how-to-use.md) | Reading guide |
| [Designing an AI Customer Support System](../examples/01-ai-customer-support/README.md) | Multi-agent Orchestrator + Executor + Guardian + Advisor |
| [Selecting the Archetypes (Example 1)](../examples/01-ai-customer-support/archetypes.md) | Five-archetype evaluation worked through |
| [Writing the Spec (Example 1)](../examples/01-ai-customer-support/spec.md) | Annotated SDD spec for the Account Executor |
| [Agent Instructions (Example 1)](../examples/01-ai-customer-support/agent-instructions.md) | Operational instructions derived from spec |
| [Validating Outcomes (Example 1)](../examples/01-ai-customer-support/validation.md) | 14-test acceptance suite |
| [Post-mortem Through Intent (Example 1)](../examples/01-ai-customer-support/postmortem.md) | $0.00 refund incident — spec gap traced and closed |
| [A Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md) | Synthesizer-Executor-Guardian pipeline with no live human |
| [Selecting the Archetypes (Example 2)](../examples/02-code-generation-pipeline/archetypes.md) | Orchestrator rejected; Synthesizer as primary coordinator |
| [Writing the Spec (Example 2)](../examples/02-code-generation-pipeline/spec.md) | Annotated spec for the Scaffold Synthesizer |
| [Agent Instructions (Example 2)](../examples/02-code-generation-pipeline/agent-instructions.md) | Non-conversational instructions for all three agents |
| [Validating Outcomes (Example 2)](../examples/02-code-generation-pipeline/validation.md) | 9-test pipeline acceptance suite |
| [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) | In-loop coding agent for an internal repo; Executor with Synthesizer composition; explicit decision against Devin-style autonomy |
| [Selecting the Archetypes (Example 3)](../examples/03-coding-agent/archetypes.md) | Decision-tree walk for a coding agent; the "why not Orchestrator-over-self" decision recorded explicitly |
| [Writing the Spec (Example 3)](../examples/03-coding-agent/spec.md) | Full canonical spec with coding-agent specifics: file-system scope, dependency allowlist, test-set protection |
| [Agent Instructions (Example 3)](../examples/03-coding-agent/agent-instructions.md) | System prompt + tool manifest with capability minimalism (no general shell, no web fetch, no merge/close) |
| [Evals and Acceptance (Example 3)](../examples/03-coding-agent/evals.md) | The four-level eval stack instantiated; 75-issue golden set construction methodology |
| [Post-mortem Through Intent (Example 3)](../examples/03-coding-agent/postmortem.md) | The deleted-test incident; spec v1.1 → v1.2 change with constraint-library entry |

---

## Cross-Cutting Patterns

*Coordination and state patterns to consult once your pilot is running. Most patterns in the book live inside Parts 3–5 alongside their parent chapters; this section gathers the cross-cutting ones.*

### Coordination

| Title | Purpose |
|-------|---------|
| [Sequential Pipeline](../patterns/coordination/sequential-pipeline.md) | Linear pipeline pattern |
| [Parallel Fan-Out](../patterns/coordination/parallel-fan-out.md) | Parallel execution pattern |
| [Conditional Routing](../patterns/coordination/conditional-routing.md) | Decision-based routing |
| [Event-Driven Agent Activation](../patterns/coordination/event-driven.md) | Event-based coordination |
| [Supervisor Agent](../patterns/coordination/supervisor.md) | Supervisor agent pattern |
| [Agent-to-Agent Contract](../patterns/coordination/agent-contract.md) | Contracted agent-to-agent interaction |

### State & Memory

| Title | Purpose |
|-------|---------|
| [Session Isolation](../patterns/state/session-isolation.md) | Multi-user isolation |
| [Shared Context Store](../patterns/state/shared-context.md) | Context sharing between agents |
| [Checkpoint and Resume](../patterns/state/checkpoint-resume.md) | Long-running execution pattern |
| [Conversation History Management](../patterns/state/conversation-history.md) | Storing conversation state |
| [Agent Registry](../patterns/state/agent-registry.md) | Registry of agent capabilities |
| [Artifact Store](../patterns/state/artifact-store.md) | Storing agent-produced artifacts |

### Repertoire

| Title | Purpose |
|-------|---------|
| [The Organizational Repertoire](../repertoires/01-why-repertoires-matter.md) | Why repertoires exist and how they compound |
| [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) | Decision-ready archetype catalog entries |
| [Spec Template Library](../repertoires/03-spec-template-library.md) | Organized spec templates |
| [Feature Spec Template](../repertoires/templates/feature-spec.md) | Template for feature-development tasks |
| [Agent Instruction Template](../repertoires/templates/agent-instruction.md) | Template for system-prompt instructions |
| [Integration Spec Template](../repertoires/templates/integration-spec.md) | Template for integration and API tasks |
| [Constraint Library Template](../repertoires/templates/constraint-library.md) | Template for reusable constraint sets |
| [Validation & Acceptance Templates](../repertoires/05-validation-templates.md) | Reusable acceptance test templates |

### Code Standards

| Title | Purpose |
|-------|---------|
| [Standards as Agent Skill Source](../repertoires/04-code-standards.md) | How code standards are structured for agent validation |
| [Standards for .NET / C#](../repertoires/code-standards/dotnet.md) | .NET constraints, patterns, and validation rules |
| [Standards for TypeScript / Node](../repertoires/code-standards/typescript.md) | TypeScript constraints and patterns |
| [Standards for Python](../repertoires/code-standards/python.md) | Python constraints and patterns |
| [Standards for REST APIs](../repertoires/code-standards/rest-apis.md) | REST API design constraints |
| [Standards for Infrastructure as Code](../repertoires/code-standards/iac.md) | IaC constraints for Bicep, Terraform, YAML |

---

## Cross-Reference: By Problem

*Find patterns by the problem you're trying to solve.*

### "I don't know which archetype to use"
- [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md)
- [The Archetype Selection Tree](../architecture/04-decision-tree.md)
- [Archetype Quick-Select Card](archetype-card.md)
- [Selecting the Archetypes (Example 1)](../examples/01-ai-customer-support/archetypes.md)
- [Selecting the Archetypes (Example 2)](../examples/02-code-generation-pipeline/archetypes.md)

### "I don't know how to write a good spec"
- [Spec-Driven Development](../sdd/01-what-sdd-means.md)
- [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md)
- [Writing for Machine Execution](../sdd/05-writing-specs-for-agents.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)
- [Writing the Spec (Example 1)](../examples/01-ai-customer-support/spec.md)
- [SpecKit Quick Reference](speckit-reference.md)

### "I don't know what constraints to include"
- [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md)
- [Constraint Library Template](../repertoires/templates/constraint-library.md)
- [Writing the Spec — NOT-authorized section](../examples/01-ai-customer-support/spec.md)

### "I'm trying to calibrate how much autonomy to give"
- [Calibrate the Four Dimensions](../theory/03-agency-autonomy-responsibility.md)
- [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md)
- [Proportional Oversight](../agents/06-human-oversight-models.md)

### "Something went wrong and I need to diagnose it"
- [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md)
- [Intent vs. Implementation](../theory/02-intent-vs-implementation.md)
- [Post-mortem Through Intent](../examples/01-ai-customer-support/postmortem.md)
- [The Living Spec](../sdd/06-living-specs.md)

### "I need to design oversight for this agent"
- [Proportional Oversight](../agents/06-human-oversight-models.md)
- [Human-in-the-Loop Gate](../patterns/coordination/human-gate.md)
- [Escalation Chain](../patterns/coordination/escalation-chain.md)
- [Output Validation Gate](../patterns/safety/output-validation-gate.md)

### "I need to set up safety controls"
- [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md)
- [Output Validation Gate](../patterns/safety/output-validation-gate.md)
- [Blast Radius Containment](../patterns/safety/blast-radius-containment.md)
- [Sensitive Data Boundary](../patterns/safety/sensitive-data-boundary.md)

### "I need to set up governance"
- [Proportional Governance](../operating/04-governance.md)
- [Intent Review Before Output Review](../operating/05-reviewing-intent.md)
- [Four Signal Metrics](../operating/06-metrics.md)

### "I need to measure and report on the practice"
- [Four Signal Metrics](../operating/06-metrics.md)
- [The Living Spec](../sdd/06-living-specs.md)
- [Cost Tracking per Spec](../patterns/observability/cost-tracking.md)

### "I need to design a multi-agent system"
- [Multi-Agent Governance](../architecture/07-multi-agent-governance.md)
- [Composing Archetypes](../architecture/05-composing-archetypes.md)
- [Orchestrator Archetype](../architecture/archetypes/orchestrator.md)
- [Designing an AI Customer Support System](../examples/01-ai-customer-support/README.md)
- [A Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md)

### "I'm building a coding agent (Cursor / Cline / Devin / Claude Code style)"
- [Coding Agents](../agents/08-coding-agents.md)
- [Designing an AI Coding Agent](../examples/03-coding-agent/README.md)
- [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) (if going Devin-style)

### "I need to red-team my system"
- [Red-Team Protocol](../operating/08-red-team-protocol.md)
- [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md)
- [Adversarial Input Test](../patterns/testing/adversarial-input.md)
- [Output Validation Gate](../patterns/safety/output-validation-gate.md)

### "My agent program's cost or latency isn't penciling"
- [Model-Tier Quick-Select Card](model-tier-card.md) — start here: per-step decision matrix and step-to-tier defaults
- [Cost and Latency Engineering](../operating/09-cost-and-latency.md) — full treatment with vendor pricing and a worked case study
- [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md) — caching as architecture, not optimization; the largest single lever for systems running 100+ tasks/day
- [Four Signal Metrics](../operating/06-metrics.md) — cost-per-correct-output is the metric this work moves
- [Context Window Budget](../patterns/capability/context-budget.md)

### "I need real production observability for my agents"
- [Production Telemetry](../operating/10-production-telemetry.md)
- [Structured Execution Log](../patterns/observability/execution-log.md)
- [Distributed Trace](../patterns/observability/distributed-trace.md)
- [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md)

### "I'm trying to introduce this framework to my team"
- [A Miniature Pilot, End-to-End](../miniature-pilot.md) — start here; show the framework on one screen before asking anyone to read three parts of a book
- [The Intent Design Session](../theory/07-intent-design-session.md) — the working ritual; run this for the first system that matters
- [Adoption Playbook](../operating/11-adoption-playbook.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)
- [The Living Spec](../sdd/06-living-specs.md)
- The worked examples ([Customer Support](../examples/01-ai-customer-support/README.md), [Code Gen Pipeline](../examples/02-code-generation-pipeline/README.md), [Coding Agent](../examples/03-coding-agent/README.md))

### "My team already uses Microsoft DevSquad Copilot"
- [Co-adoption with DevSquad Copilot](../operating/13-co-adoption-with-devsquad.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../operating/12-devsquad-mapping.md)
- [Architectural Decision Records](../sdd/08-architectural-decision-records.md)

### "I'm building a computer-use / browser-use agent (Claude Computer Use / Operator / Gemini)"
- [Computer-Use Agents](../agents/09-computer-use-agents.md)
- [Red-Team Protocol — Computer-use-specific test patterns](../operating/08-red-team-protocol.md)
- [Multi-Agent Governance — A2A protocols](../architecture/07-multi-agent-governance.md)

### "I need to design safe agent tools"
- [Least Capability](../agents/04-tools-mcp-capability-boundaries.md)
- [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md)
- [MCP Safety](../agents/mcp/03-mcp-safety.md)
- [The Read-Only Tool](../patterns/integration/read-only-tool.md)
- [The State-Changing Tool](../patterns/integration/state-changing-tool.md)

### "I need to ship safely without making the change irreversible"
- [Canary Deployment](../patterns/deployment/canary.md)
- [Rollback on Failure](../patterns/deployment/rollback.md)
- [Spec Versioning](../patterns/deployment/spec-versioning.md)
- [Model Upgrade Validation](../patterns/deployment/model-upgrade.md)

### "I need to build or expand a team repertoire"
- [The Organizational Repertoire](../repertoires/01-why-repertoires-matter.md)
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md)
- [Spec Template Library](../repertoires/03-spec-template-library.md)
- [Validation & Acceptance Templates](../repertoires/05-validation-templates.md)

---

## Cross-Reference: By Archetype

*Find all chapters relevant to a specific archetype.*

| Archetype | Definition | Used in example | Governance | Constraints |
|-----------|-----------|-----------------|-----------|-------------|
| Advisor | [advisor.md](../architecture/archetypes/advisor.md) | Example 1 (Policy Advisor) | [Proportional Governance](../operating/04-governance.md) | [Spec template library](../repertoires/03-spec-template-library.md) |
| Executor | [executor.md](../architecture/archetypes/executor.md) | Example 1 (Account Executor), Example 3 (Coding Agent) | [Proportional Governance](../operating/04-governance.md) | [Validation templates](../repertoires/05-validation-templates.md) |
| Guardian | [guardian.md](../architecture/archetypes/guardian.md) | Example 1 (Compliance Guardian), Example 2 (Standards Guardian) | [Proportional Governance](../operating/04-governance.md) | [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) |
| Synthesizer | [synthesizer.md](../architecture/archetypes/synthesizer.md) | Example 2 (Scaffold Synthesizer) | [Proportional Governance](../operating/04-governance.md) | [Spec template library](../repertoires/03-spec-template-library.md) |
| Orchestrator | [orchestrator.md](../architecture/archetypes/orchestrator.md) | Example 1 (Inquiry Orchestrator) | [Proportional Governance](../operating/04-governance.md) | [Proportional Oversight](../agents/06-human-oversight-models.md) |

---

## Cross-Reference: By Agent Class

*Find all chapters relevant to a specific deployment class. The book treats archetypes (Advisor / Executor / Guardian / Synthesizer / Orchestrator) and agent classes (coding agents, computer-use agents, multi-agent systems) as orthogonal — every agent class is a composition of one or more archetypes.*

| Agent class | Primary chapter | Worked example | Specific failure modes | Specific red-team patterns |
|---|---|---|---|---|
| **Conversational support agent** | [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md) (Advisor or Executor depending on action authority) | [Designing an AI Customer Support System](../examples/01-ai-customer-support/README.md) | Cat 1–6 (general taxonomy) | OWASP LLM01, LLM07, LLM02 (system-prompt extraction, sensitive-data disclosure) |
| **Code generation pipeline** | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) (Synthesizer + Executor + Guardian composition) | [A Code Generation Pipeline](../examples/02-code-generation-pipeline/README.md) | Cat 5 (compounding) particularly relevant | OWASP LLM05 (improper output handling) |
| **Coding agent (in-loop)** | [Coding Agents](../agents/08-coding-agents.md) (Executor with Synthesizer composition; can escalate to Orchestrator-over-self) | [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) | Test deletion (Cat 1+3), dependency typosquat (Cat 2), hallucinated APIs (Cat 6), scope-creep refactors (Cat 3) | Supply-chain (LLM03), excessive agency (LLM06), coding-agent-specific patterns in [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **Computer-use / browser-use agent** | [Computer-Use Agents](../agents/09-computer-use-agents.md) (deployment-posture-dependent: Advisor / Executor / Orchestrator-over-self) | (no worked example yet — under-served chapter) | Cat 1–6 plus **Cat 7 (Perceptual Failure)** with 4 sub-categories | Computer-use-specific test patterns in [Red-Team Protocol](../operating/08-red-team-protocol.md): lookalike domains, visual instruction injection, modal popup interception, etc. |
| **Multi-agent system** | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) (any composition; supervisor / pipeline / peer patterns) | Both Example 1 and Example 2 | MAST 14-category empirical taxonomy applies; the book's Cat 5 (compounding) is the dominant shape | Cross-agent injection, handoff manipulation, A2A protocol-layer attacks |

---

## Cross-Reference: By 2024–2026 Innovation

*Find where each significant 2024–2026 development is addressed, and how the framework responds to it. This is the practitioner's "what's new and where do I read about it" index. The full citations live in the [References](references.md) appendix.*

| Innovation | Year | Where addressed in the book | What the book contributes around it |
|---|---|---|---|
| **Anthropic MCP** + cross-vendor adoption (OpenAI, Google, Microsoft) | 2024–25 | [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md), [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md), [MCP Safety](../agents/mcp/03-mcp-safety.md), [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) | The protocol layer through which [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) becomes operationally enforceable; capability-gating discipline at the tool layer |
| **GitHub spec-kit** | 2024–25 | [Spec-Driven Development](../sdd/01-what-sdd-means.md), [SpecKit](../sdd/04-speckit.md) | Direct ancestor of the canonical spec template; the book extends spec-kit's discipline with the archetype framework and the failure taxonomy |
| **Microsoft DevSquad Copilot** | 2026 | [DevSquad Mapping](../operating/12-devsquad-mapping.md), [Co-adoption with DevSquad](../operating/13-co-adoption-with-devsquad.md), [Architectural Decision Records](../sdd/08-architectural-decision-records.md) | A complete bridge: phase-by-phase mapping, vocabulary translation, ranked addition list, 30-day co-adoption plan, ADRs as a first-class artifact |
| **Anthropic Computer Use** | Oct 2024 | [Computer-Use Agents](../agents/09-computer-use-agents.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) | New agent class chapter with archetype mapping by deployment posture; new Cat 7 (Perceptual Failure) added to the diagnostic protocol; four structural controls (sandboxed environment, auth scope minimization, domain allowlist, high-consequence confirmation gate); computer-use-specific red-team patterns |
| **OpenAI Operator / Gemini computer use** | 2025 | [Computer-Use Agents](../agents/09-computer-use-agents.md) | Same chapter — three implementations of the new class, all subject to the same structural controls and Cat 7 framework |
| **Reasoning-tier models (o1, o3, Claude extended thinking, Gemini reasoning)** | 2024–25 | [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Distinct model tier in the per-role selection table; explicit cost/latency profile (2–10× cost, 5–60s latency); when-to-use vs when-not-to budgeting discipline |
| **Anthropic Constitutional Classifiers** | 2025 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | Treated honestly as a probabilistic perimeter, not a fix; documented escape rate and over-refusal cost made explicit |
| **Anthropic prompt caching / OpenAI cached input / Gemini context caching** | 2024–25 | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Caching as architecture (layered prompt with cache breakpoints; prompt-stability as a spec constraint; cache-hit-rate as first-class telemetry); 40–70% input-cost reduction is normal when treated architecturally |
| **Google Agent2Agent (A2A) Protocol** | 2025 | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) | Protocol-layer counterpart to MCP at the tool layer; the governance question for protocol-mediated multi-agent systems |
| **OpenTelemetry GenAI semantic conventions** | 2024–25 | [Production Telemetry](../operating/10-production-telemetry.md) | Vendor-neutral observability standard; the book recommends emitting OTel-compliant spans alongside vendor SDK telemetry for portability |
| **OWASP LLM Top 10 (2025 update)** | 2025 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md), [Red-Team Protocol](../operating/08-red-team-protocol.md), [Computer-Use Agents](../agents/09-computer-use-agents.md) | Baseline coverage for the four red-team batteries; instantiation per deployment specifics |
| **MAST taxonomy** (Cemri et al.) | 2025 | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) | Empirical 14-category multi-agent failure partition; complementary to (not replacing) the book's seven-category fix-locus taxonomy |
| **Indirect prompt injection** (Greshake et al. 2023) + the **lethal trifecta** (Willison) | 2023, ongoing | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | The structural defense (trifecta reduction; capability gating) is centered on the indirect injection class that cannot be filtered at the prompt layer |
| **SWE-bench Verified, AgentBench, τ-bench, GAIA, BFCL, WebArena, OSWorld, ScreenSpot-Pro** | 2023–25 | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md), [Coding Agents](../agents/08-coding-agents.md), [Computer-Use Agents](../agents/09-computer-use-agents.md) | External calibration benchmarks; the book recommends using public benchmarks for harness calibration and team-built golden sets for actual task fit |
| **Open-source eval / red-team frameworks** (Inspect, OpenAI Evals, Promptfoo, PyRIT, Garak) | 2024–25 | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) | The toolchain layer the book recommends adopting rather than building custom |
| **Production observability stacks** (LangSmith, Langfuse, Phoenix, Helicone, Datadog LLM) | 2024–25 | [Production Telemetry](../operating/10-production-telemetry.md) | Vendor-stack landscape with a clear "which to choose if you have X" decision rule |
| **Coding agent platforms** (Cursor, Cline, Aider, Devin, Claude Code, Codex CLI) | 2023–25 | [Coding Agents](../agents/08-coding-agents.md), [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) | Treated as deployment-posture-dependent compositions; explicit decision-against-Devin-style-autonomy criteria documented in Example 3 |
| **Anthropic Skills as deployable artifact** | 2025 | [Portable Domain Knowledge](../agents/05-agent-skills.md) | The maturation of "domain knowledge as packaged context" — skills as versioned, distributed deployment units |
| **Lost in the Middle long-context attention degradation** (Liu et al. 2023) | 2023, ongoing | [Coding Agents](../agents/08-coding-agents.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Empirical grounding for the long-context anti-pattern; informs context-budget discipline and the warning against long-context dumping |
| **NIST AI RMF / ISO 42001 / Anthropic RSP / OpenAI Preparedness Framework** | 2023–25 | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) | Compliance-layer reference points; the book's four-dimensions framing is compatible with each |
