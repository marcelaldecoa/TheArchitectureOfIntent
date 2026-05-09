# Reading List & References

**Appendices** · *Appendix C*

---

> *"Every book is in conversation with other books. These are the ones this book is most explicitly in debt to, and the ones a serious practitioner should read alongside it."*

---

This appendix is organized by topic. Within each topic, a short **Read first** subsection identifies the one or two primary sources that contain most of what you need; **Further reading** provides depth. Citations referenced inline within chapters carry through to the chapter-level References sections.

A note on honest framing: much of what this book describes is not novel. It synthesizes work from the agent design literature (Anthropic, OpenAI, LangChain), AI governance literature (NIST, ISO, OpenAI), spec-driven development practice (GitHub spec-kit, Microsoft DevSquad Copilot), classical software engineering (Brooks, Meyer, Jackson), and human-systems thinking (Deming, Meadows, Reason). Where the book contributes, it contributes a synthesis with consistent vocabulary and an opinionated archetype frame; the underlying ideas are mostly older. The reading list below makes that lineage explicit.

---

## Quick reference: where 2024–2026 developments are addressed

The agent landscape has moved quickly between 2024 and 2026. This table maps each significant development to the chapter(s) in this book where it is addressed, so readers can find the framework's response to a specific technology or technique without reading linearly.

| Innovation | Year | Where addressed | Relation to the framework |
|---|---|---|---|
| **Anthropic Model Context Protocol (MCP)** | 2024–25 | [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md), [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md), [MCP Safety](../agents/mcp/03-mcp-safety.md) | The protocol that makes [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) operationally enforceable |
| **MCP cross-vendor adoption** (OpenAI, Google, Microsoft Copilot) | 2025 | [The Model Context Protocol — 2026 ecosystem](../agents/mcp/01-what-is-mcp.md) | Treats MCP as the *de facto* tool integration protocol; not using it is now the choice that needs justification |
| **GitHub spec-kit** | 2024–25 | [Spec-Driven Development](../sdd/01-what-sdd-means.md), [SpecKit](../sdd/04-speckit.md) | The direct ancestor of the book's SDD chapters and canonical spec template |
| **Microsoft DevSquad Copilot** | 2026 | [DevSquad Mapping](../operating/12-devsquad-mapping.md), [Co-adoption with DevSquad](../operating/13-co-adoption-with-devsquad.md), [The Living Spec](../sdd/06-living-specs.md), [Adoption Playbook](../operating/11-adoption-playbook.md) | Parallel framework with high conceptual overlap; the book is process-agnostic, DevSquad is process-prescriptive; they compose cleanly |
| **Anthropic Computer Use** | Oct 2024 | [Computer-Use Agents](../agents/09-computer-use-agents.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) | The reference implementation that made GUI-acting agents mainstream; introduced the new failure-mode surface Cat 7 (Perceptual Failure) |
| **OpenAI Operator** | Early 2025 | [Computer-Use Agents](../agents/09-computer-use-agents.md) | Browser-use agent with autonomous task completion posture; canonical Orchestrator-over-self deployment for the new class |
| **Google Gemini computer use** | 2025 | [Computer-Use Agents](../agents/09-computer-use-agents.md) | Third major implementation of the GUI-acting agent class |
| **OpenAI o1, o3 (reasoning tier)** | 2024–25 | [Cost and Latency Engineering — reasoning tier specifics](../operating/09-cost-and-latency.md) | Distinct model tier with 2–10× cost and 5–60s latency profile; deserves explicit per-role budgeting |
| **Anthropic Claude with extended thinking** | 2025 | [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | The Anthropic equivalent of the reasoning tier |
| **Anthropic Constitutional Classifiers** | 2025 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | Inference-time classifier for jailbreak/injection defense; documented ~5% escape rate against motivated red-teamers, ~25% over-refusal cost |
| **Anthropic prompt caching** | 2024 | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | 40–70% structural input-cost reduction; cache-control parameter at the prompt-architecture level; prompt-stability as a spec constraint |
| **OpenAI cached inputs** | 2024–25 | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Automatic prefix-based caching; ~50% discount on cached prefix tokens; 1024-token minimum |
| **Google Gemini context caching** | 2024–25 | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Explicit `CachedContent` resources referenced by ID; storage cost separate from per-call discount |
| **Google Agent2Agent (A2A) Protocol** | 2025 | [Multi-Agent Governance — Agent-to-agent protocols](../architecture/07-multi-agent-governance.md) | Cross-vendor agent communication standard; the protocol-layer counterpart to MCP at the tool layer |
| **OpenTelemetry GenAI semantic conventions** | 2024–25 | [Production Telemetry](../operating/10-production-telemetry.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) | Vendor-neutral observability standard that the book recommends emitting alongside vendor SDK telemetry |
| **OWASP LLM Top 10 (2025 update)** | 2025 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md), [Red-Team Protocol](../operating/08-red-team-protocol.md), [Computer-Use Agents](../agents/09-computer-use-agents.md) | Canonical attack-surface enumeration for agent systems; baseline coverage for the four red-team batteries |
| **MAST taxonomy** (Cemri et al.) | 2025 | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) | Empirical 14-category multi-agent failure partition; complements the book's seven-category fix-locus partition |
| **Anthropic Skills as deployable artifact** | 2025 | [Portable Domain Knowledge](../agents/05-agent-skills.md) | Skills as versioned, distributed deployment units; the maturation of the "domain knowledge as packaged context" pattern |
| **SWE-bench Verified** | 2024 | [Coding Agents](../agents/08-coding-agents.md), [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) | Human-validated subset of SWE-bench; the external calibration benchmark for coding agents |
| **WebArena, VisualWebArena, OSWorld, ScreenSpot-Pro** | 2024–25 | [Computer-Use Agents](../agents/09-computer-use-agents.md), [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) | External calibration benchmarks for computer-use agents; reveal that "computer-use works" is an overclaim for many task domains |
| **τ-bench, GAIA, AgentBench** | 2023–24 | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) | General agent evaluation; multi-environment task suites |
| **Berkeley Function-Calling Leaderboard (BFCL)** | 2024 | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md), [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md) | Tool-call correctness comparison across model versions |
| **Anthropic Inspect / OpenAI Evals / Promptfoo / PyRIT / Garak** | 2024–25 | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) | Open-source eval and red-team frameworks; the toolchain layer the book recommends adopting rather than building custom |
| **LangSmith / Langfuse / Phoenix / Helicone / Datadog LLM** | 2024–25 | [Production Telemetry](../operating/10-production-telemetry.md) | The vendor-stack landscape for production agent observability |
| **Cursor, Cline, Aider, Devin, Claude Code, Codex CLI** | 2023–25 | [Coding Agents](../agents/08-coding-agents.md), [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) | The dominant implementation of the in-loop coding-agent pattern; treated by the book as a deployment-posture-dependent composition (Advisor / Executor / Orchestrator-over-self) |
| **Indirect prompt injection (Greshake et al.)** | 2023 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | The attack class that cannot be defended at the prompt layer; the lethal trifecta framing centers on it |
| **Microsoft Spotlighting** | 2024 | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) | Data-marking technique for indirect injection mitigation; partial defense, not a fix |
| **Lost in the Middle attention degradation** | 2023 | [Coding Agents](../agents/08-coding-agents.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) | Empirical grounding for the long-context anti-pattern; informs context-budget discipline |

This is the working set as of the book's current revision. The list will grow as the field develops.

---

## Building agents — patterns, architecture, runtime

**Read first**

- **Anthropic.** (Dec 2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The current canonical practitioner reference. Distinguishes workflows (predetermined paths) from agents (model-driven control flow), names the core compositional patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. If you read one source on agent design, this is it.
- **Weng, L.** (June 2023). *LLM Powered Autonomous Agents.* lilianweng.github.io. — The most-cited technical survey; covers planning, memory, tool use, and reflection patterns. Older but foundational.

**Further reading**

- **Liu, Y., et al.** (May 2024). *Agent Design Pattern Catalogue: A Collection of Architectural Patterns for Foundation Model based Agents.* arXiv:2405.10467. — 18 architectural patterns including goal creation, plan generation, tool use, and reflection. The most comprehensive academic pattern catalogue.
- **OpenAI.** (Oct 2024). *Swarm — Lightweight multi-agent orchestration.* github.com/openai/swarm. — Reference implementation of routing and handoff patterns; useful as a minimal mental model of multi-agent coordination.
- **LangGraph documentation.** *Supervisor architecture, hierarchical teams, HITL middleware, checkpointing.* langchain-ai.github.io/langgraph. — The most production-tested implementation surface for the patterns Anthropic and Weng describe.
- **MetaGPT** (Hong et al., 2023, arXiv:2308.00352) and **AutoGen** (Wu et al., 2023, arXiv:2308.08155). — Multi-agent SOPs and conversation-driven coordination; useful comparison points to LangGraph's supervisor model.

---

## AI agent class developments (2024–2026)

The two new agent classes that emerged during the 2024–2026 period — *coding agents* and *computer-use agents* — each have their own chapter in the book ([Coding Agents](../agents/08-coding-agents.md), [Computer-Use Agents](../agents/09-computer-use-agents.md)). The references below ground those chapters.

### Coding agents

- **Anthropic.** *Claude Code documentation.* claude.com/product/claude-code. — Reference architecture for in-loop coding-agent design.
- **GitHub.** *Copilot agent mode.* github.com/features/copilot. — Mainstream pair-programmer pattern that became Cursor-style in-loop deployments.
- **Cognition Labs.** *Devin.* cognition.ai/devin. — The autonomous-engineering-agent posture (Orchestrator-over-self) reference implementation.
- **Cursor, Cline, Aider, Codex CLI.** Practitioner tools that converged on the in-loop Executor pattern; substantial influence on production coding-agent design as of 2026.
- **Yang, J., et al.** (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* arXiv:2405.15793. — Tool-design study specific to coding agents; introduces the "Agent-Computer Interface" concept.
- **Liu, N. F., et al.** (2023). *Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172. — Empirical grounding for long-context attention degradation; relevant whenever a coding agent operates over large repositories.

### Computer-use / browser-use agents

- **Anthropic.** (October 2024). *Computer use.* anthropic.com/news/3-5-models-and-computer-use. — The reference implementation that made computer-use agents mainstream.
- **OpenAI.** (Early 2025). *Operator.* openai.com. — OpenAI's browser-use agent platform.
- **Google.** (2025). *Gemini computer use.* — Google's equivalent capability.
- **Zhou, S., et al.** (2024). *WebArena: A Realistic Web Environment for Building Autonomous Agents.* arXiv:2307.13854. — The benchmark for web-acting agents.
- **Koh, J. Y., et al.** (2024). *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks.* arXiv:2401.13649.
- **Xie, T., et al.** (2024). *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.* arXiv:2404.07972. — The desktop-environment benchmark.
- **Li, K., et al.** (2024). *ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use.* — Higher-stakes benchmark for professional GUI tasks.

### Reasoning-tier models

The reasoning-tier class emerged in 2024–2025 as a distinct deployment category from standard large-tier models, with characteristic 2–10× cost and 5–60s latency profiles. Treatment in [Cost and Latency Engineering](../operating/09-cost-and-latency.md).

- **OpenAI.** (2024). *Introducing OpenAI o1.* openai.com/o1. — The reasoning tier's first mainstream release.
- **OpenAI.** (2025). *o3 system card.* — Successor reasoning model with different cost/latency profile.
- **Anthropic.** (2025). *Claude with extended thinking.* — Anthropic's reasoning-tier capability.
- **DeepSeek.** (2025). *DeepSeek-R1.* — Open-weights reasoning model demonstrating the technique outside the major U.S. labs.

### Agent-to-agent protocols

The protocol-layer counterpart to MCP at the tool layer; emerging standardization arc as of 2026. Treatment in [Multi-Agent Governance — Agent-to-agent protocols](../architecture/07-multi-agent-governance.md).

- **Google.** (2025). *Agent2Agent (A2A) Protocol.* a2aprotocol.dev. — Cross-vendor agent communication standard.
- **OpenAI.** (2025, ongoing). *Agent SDK.* — Vendor-specific coordination primitives that approximate A2A semantics within OpenAI's ecosystem.
- **LangChain.** *LangGraph supervisor and handoff patterns.* — In-vendor reference implementations; remain the dominant practical guide for multi-agent coordination.

### Inference economics and prompt caching

- **Anthropic.** (2024, ongoing). *Prompt caching with Claude.* anthropic.com/news/prompt-caching. — Cache control parameters with documented economic effect.
- **OpenAI.** (2024). *Prompt caching.* platform.openai.com/docs/guides/prompt-caching.
- **Google.** *Context caching with Gemini.* ai.google.dev/gemini-api/docs/caching.
- **Pope, R., et al.** (2022). *Efficiently Scaling Transformer Inference.* arXiv:2211.05102. — Foundational inference-cost economics underlying provider model-tier pricing.

---

## Governance and oversight of agentic AI

**Read first**

- **Shavit, Y., Agarwal, S., et al.** (OpenAI, 2023). *Practices for Governing Agentic AI Systems.* cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf. — Closest prior art for this book's four-dimensions framing. Explicitly covers action-space, default behaviors, reversibility, attributability, and interruptibility as governance dimensions.
- **NIST.** (2023). *AI Risk Management Framework (AI RMF 1.0).* nist.gov/itl/ai-risk-management-framework. — The U.S. governmental framework; Govern / Map / Measure / Manage. Used as compliance ground truth in many regulated settings.

**Further reading**

- **ISO/IEC 42001:2023.** *Information technology — Artificial intelligence — Management system.* — The first international management-system standard for AI; complements NIST AI RMF for organizations seeking certification.
- **Anthropic.** (Sept 2023, ongoing). *Responsible Scaling Policy.* anthropic.com/responsible-scaling-policy. — Anthropic's published commitments on capability evaluations and deployment thresholds.
- **OpenAI.** (Dec 2023, ongoing). *Preparedness Framework.* openai.com/preparedness. — OpenAI's analogue to RSP; defines model risk categories and deployment gates.
- **SAE International.** (2021). *J3016 — Taxonomy and Definitions for Terms Related to Driving Automation Systems.* — The canonical six-level autonomy taxonomy that informed the autonomy dimension in [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md).

---

## Spec-driven development

**Read first**

- **GitHub.** (2024–2025). *spec-kit.* github.com/github/spec-kit. — The most active practitioner project on spec-as-source-of-truth for AI-augmented development. Direct ancestor of this book's SDD chapters and the canonical spec template.
- **Microsoft.** (2026). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot (site at microsoft.github.io/devsquad-copilot). — Parallel work from Microsoft arriving at compatible conclusions from a different angle. Where this book gives you a *design vocabulary* (archetypes, dimensions, failure taxonomy), DevSquad gives you a *delivery cadence* — the documented 8-phase iterative cycle: *envisioning phase → Spec the next slice → Plan only what the current slice needs → Decompose that slice → Implement with TDD discipline → Learn in the open → Review in an independent context → Refine continuously*. Coordination is performed by a single conductor agent that delegates to twelve named specialist agents (*init, envision, kickoff, specify, plan, decompose, implement, review, security, sprint, refine, extend*), with autonomy scaled by an impact classification (low/medium/high). Tool access is mediated through five first-party MCP servers (GitHub, Azure DevOps, Azure, Microsoft Learn, Draw.io). The two converge on living specs, risk-tiered human-in-the-loop, principle of least privilege, context isolation across sub-agents, and spec-first response to failure. They diverge on emphasis: DevSquad is process-prescriptive and centered on multi-developer Copilot teams; this book is process-agnostic and centered on agent-system design with deeper coverage of failure modes, prompt injection, evals, and telemetry. Recommended as a complementary read — a team adopting DevSquad's 8-phase cadence plus this book's archetype framework, failure taxonomy, and security/eval/telemetry stacks would have a more complete operating model than either source provides alone. Notable distinctive contribution from DevSquad: the explicit treatment of ADRs as a first-class durable artifact alongside specs, plus a comprehension checkpoint after medium- and high-impact implementation.

**Further reading**

- **Jackson, M.** (1995). *Software Requirements & Specifications: A Lexicon of Practice, Principles, and Prejudices.* Addison-Wesley. — The domain/machine distinction maps directly onto the book's intent/implementation distinction. Read for the precision of the language and the discipline of problem framing.
- **Meyer, B.** (1997). *Object-Oriented Software Construction* (2nd ed.). Prentice Hall. — Origin of Design by Contract. The constraint sections of an SDD spec are Design by Contract for agent behavior.
- **IEEE 830-1998 / ISO/IEC/IEEE 29148:2018.** *Software Requirements Specifications.* — The canonical SRS structure; sections 1–3, 5, 7, 9 of the Canonical Spec Template are recognizably descended from this lineage.
- **Cohn, M.** (2004). *User Stories Applied.* — INVEST criteria for specifications.
- **North, D.** (2006, ongoing). *Behaviour-Driven Development* and the Gherkin Given/When/Then format. — Source of the acceptance criteria style used in Section 9.
- **Nygard, M.** (2011). *Documenting Architecture Decisions.* cognitect.com/blog/2011/11/15/documenting-architecture-decisions. — The original ADR format that this book inherits in [Architectural Decision Records](../sdd/08-architectural-decision-records.md), and that Microsoft DevSquad Copilot also adopts.
- **ADR Tools and Templates.** (ongoing). adr.github.io. — Community resources for ADR format variations.

---

## Failure modes, hallucination, and agent reliability

**Read first**

- **Cemri, M., et al.** (2025). *Why Do Multi-Agent LLM Systems Fail? — MAST: A Multi-Agent System Failure Taxonomy.* OpenReview / arXiv. — Empirical 14-category partition derived from 200+ multi-agent failure traces. The most rigorous practitioner-facing failure taxonomy currently published.
- **Zhang, Y., et al.** (2025). *LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions.* arXiv:2509.18970. — Fine-grained partition of model-level (Category 6) failures; tool-call hallucination, planning hallucination, instruction-following inconsistency.

**Further reading**

- *Where LLM Agents Fail and How They Can Learn from Failures.* (2025). arXiv:2509.25370.
- **Reason, J.** (1990). *Human Error.* Cambridge. — Active vs. latent failures, the Swiss-cheese model. Underlying theory for "fix the system, not the operator."
- **Toyota Production System / 5 Whys.** (Ohno, 1988). — Origin of the per-failure root-cause discipline that the book's diagnostic protocol simplifies.

---

## Prompt injection and agent security

**Read first**

- **Greshake, K., Abdelnabi, S., et al.** (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* arXiv:2302.12173. — The foundational paper distinguishing direct from indirect prompt injection. Required reading.
- **Willison, S.** (2022–present). *Prompt injection* series, including *The lethal trifecta for AI agents.* simonwillison.net. — The most consistent practitioner-facing analysis of prompt injection. Where the "lethal trifecta" framing originates.
- **OWASP.** (2025). *LLM Top 10 — LLM01: Prompt Injection.* genai.owasp.org/llm-top-10. — The industry-standard categorization, including direct, indirect, multimodal, and payload-smuggling subtypes.

**Further reading**

- **Hines, K., et al.** (2024). *Defending Against Indirect Prompt Injection Attacks With Spotlighting.* arXiv:2403.14720. — Microsoft Research's spotlighting / data-marking approach.
- **Anthropic.** (2025). *Constitutional Classifiers: Defending against universal jailbreaks.* anthropic.com/research. — Inference-time classifier defense; the strongest currently-published mitigation, with documented over-refusal cost.
- **NIST.** (2024). *AI 100-2 E2024: Adversarial Machine Learning — A Taxonomy and Terminology of Attacks and Mitigations.* nvlpubs.nist.gov.
- **Anthropic.** (2024). *Many-shot jailbreaking.* anthropic.com/research. — The discovery that long context windows enable a new class of jailbreak attacks.

---

## Tool use, MCP, and capability protocols

**Read first**

- **Anthropic.** (Nov 2024). *Model Context Protocol.* modelcontextprotocol.io. — The open protocol for tool/data integration. The book's MCP chapters provide the conceptual frame; the spec is the technical reference.
- **Anthropic / OpenAI / Google.** *Tool use / function calling documentation.* — Provider-specific guidance on capability declarations, structured outputs, and tool-result handling.

**Further reading**

- **Schick, T., et al.** (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* arXiv:2302.04761. — Foundational work on typed tool interfaces.
- **Yao, S., et al.** (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. — The reasoning + acting interleaving pattern that underlies most agent loops.
- **Berkeley Function-Calling Leaderboard (BFCL).** gorilla.cs.berkeley.edu. — Empirical comparison of tool-use reliability across models.

---

## Evals and benchmarks

**Read first**

- **Jimenez, C. E., et al.** (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv:2310.06770; SWE-bench Verified subset. — The reference benchmark for code-fixing agents.
- **Liu, X., et al.** (2023). *AgentBench: Evaluating LLMs as Agents.* arXiv:2308.03688.
- **Yao, S., et al.** (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.*
- **Mialon, G., et al.** (2023). *GAIA: A Benchmark for General AI Assistants.* arXiv:2311.12983.

**Further reading**

- **Liang, P., et al.** (2023). *Holistic Evaluation of Language Models (HELM).* arXiv:2211.09110. — The holistic eval framework that informed much of the agent-eval design space.
- **Zheng, L., et al.** (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv:2306.05685. — Foundational analysis of judge-model bias and calibration.
- **Anthropic.** *Inspect — A framework for large language model evaluations.* inspect.aisi.org.uk. — Open-source eval framework.
- **OpenAI.** *Evals.* github.com/openai/evals. — The original public agent-eval framework.

---

## Pattern languages and design

**Read first**

- **Alexander, C., Ishikawa, S., & Silverstein, M.** (1977). *A Pattern Language: Towns, Buildings, Construction.* Oxford University Press. — Structural inspiration for how the Architecture of Intent is organized. Read at least the introduction and the first 50 patterns to understand what a pattern language *is* before evaluating any framework that claims to be one.

**Further reading**

- **Alexander, C.** (1979). *The Timeless Way of Building.* Oxford. — The companion volume; addresses the epistemology of pattern languages.
- **Gamma, E., Helm, R., Johnson, R., & Vlissides, J.** (1994). *Design Patterns: Elements of Reusable Object-Oriented Software.* Addison-Wesley. — The software application of Alexander's approach.
- **Fowler, M.** (2002). *Patterns of Enterprise Application Architecture.* Addison-Wesley. — Useful primarily for the discipline of catalog-format pattern documentation.

---

## Software engineering foundations

- **Brooks, F. P.** (1995). *The Mythical Man-Month* (Anniversary ed.). Addison-Wesley. — Read "No Silver Bullet" for Brooks's distinction between accidental and essential complexity. Agents reduce accidental complexity dramatically; the essential complexity is what specs address.
- **Feathers, M. C.** (2004). *Working Effectively with Legacy Code.* Prentice Hall. — A book about systems whose intent was never captured. The kind of system SDD prevents.

---

## Organizations, systems thinking, and quality

- **Deming, W. E.** (1982). *Out of the Crisis.* MIT Press. — Quality problems are primarily system problems. The 85/15 rule should calibrate how the four signal metrics chapter is read.
- **Meadows, D. H.** (2008). *Thinking in Systems: A Primer.* Chelsea Green. — The clearest short introduction to feedback loops; balancing vs. reinforcing loops directly inform how the Spec Gap Log functions in the SDD practice.
- **Kim, G., Debois, P., Willis, J., & Humble, J.** (2016). *The DevOps Handbook.* IT Revolution Press. — The Three Ways (flow, feedback, continual learning) map cleanly onto SDD practice.

---

## AI ethics, alignment, and societal context

- **Russell, S.** (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Viking. — Russell's preference-uncertainty argument as the alignment framing closest to this book's spec-and-validation discipline.
- **Bostrom, N.** (2014). *Superintelligence.* — More speculative; useful primarily as a systematic catalog of objective-misalignment failure modes.
- **Crawford, K.** (2021). *Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence.* Yale. — The costs that don't appear in spec templates. Read as a corrective to the technical-optimism bias that pervades most AI engineering literature.

---

## Inline citations index

Specific sources cited within chapters of this book, organized alphabetically by source. Use this index to find every chapter that draws on a specific paper, framework, or product.

### Industry frameworks and platforms

| Source | Cited in |
|---|---|
| **Anthropic** — *Building Effective Agents* (Dec 2024) | [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md), [Coding Agents](../agents/08-coding-agents.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md), [Adoption Playbook](../operating/11-adoption-playbook.md), [Co-adoption with DevSquad](../operating/13-co-adoption-with-devsquad.md) |
| **Anthropic** — *Claude Code* | [Coding Agents](../agents/08-coding-agents.md), [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) |
| **Anthropic** — *Computer Use* (Oct 2024) | [Computer-Use Agents](../agents/09-computer-use-agents.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **Anthropic** — *Constitutional Classifiers* (2025) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| **Anthropic** — *Inspect* (eval framework) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **Anthropic** — *Many-shot jailbreaking* (2024) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| **Anthropic** — *Model Context Protocol* (2024) | [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md), [Designing MCP Tools](../agents/mcp/02-designing-mcp-tools.md), [MCP Safety](../agents/mcp/03-mcp-safety.md), [Least Capability](../agents/04-tools-mcp-capability-boundaries.md) |
| **Anthropic** — *Prompt caching with Claude* (2024) | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **Anthropic** — *Responsible Scaling Policy* (2023, ongoing) | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) |
| **Datadog** — *LLM Observability* | [Production Telemetry](../operating/10-production-telemetry.md) |
| **GitHub** — *spec-kit* (2024–25) | [Spec-Driven Development](../sdd/01-what-sdd-means.md), [SpecKit](../sdd/04-speckit.md) |
| **Google** — *Agent2Agent (A2A) Protocol* (2025) | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) |
| **Google** — *Gemini computer use* (2025) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **Google** — *Gemini context caching* | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **Helicone** — LLM observability proxy | [Production Telemetry](../operating/10-production-telemetry.md) |
| **LangChain** — *LangGraph supervisor / hierarchical / HITL middleware* | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md), [Co-adoption with DevSquad](../operating/13-co-adoption-with-devsquad.md) |
| **LangChain** — *LangSmith* | [Production Telemetry](../operating/10-production-telemetry.md) |
| **Langfuse** — open-source LLM observability | [Production Telemetry](../operating/10-production-telemetry.md) |
| **Microsoft** — *DevSquad Copilot* (2026) | [The Living Spec](../sdd/06-living-specs.md), [Architectural Decision Records](../sdd/08-architectural-decision-records.md), [DevSquad Mapping](../operating/12-devsquad-mapping.md), [Co-adoption with DevSquad](../operating/13-co-adoption-with-devsquad.md), [Adoption Playbook](../operating/11-adoption-playbook.md), [References — Spec-driven development](references.md) |
| **Microsoft** — *PyRIT* | [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **NIST** — *AI 100-2 E2024* (Adversarial ML) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **NIST** — *AI Risk Management Framework (AI RMF 1.0)* | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) |
| **NVIDIA** — *Garak* (LLM vulnerability scanner) | [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **OpenAI** — *Agent SDK* (2025) | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) |
| **OpenAI** — *Operator* (2025) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **OpenAI** — *Practices for Governing Agentic AI Systems* (Shavit, Agarwal et al., 2023) | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md), [References](references.md) |
| **OpenAI** — *Prompt caching / cached input pricing* (2024) | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **OpenAI** — *o1 / o3 reasoning models* (2024–25) | [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **OpenInference / Phoenix** (Arize) | [Production Telemetry](../operating/10-production-telemetry.md) |
| **OpenTelemetry** — *GenAI semantic conventions* | [Production Telemetry](../operating/10-production-telemetry.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) |
| **OWASP** — *LLM Top 10* (2025) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md), [Red-Team Protocol](../operating/08-red-team-protocol.md), [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **SAE International** — *J3016 driving automation taxonomy* | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) |

### Academic and research references

| Source | Cited in |
|---|---|
| **Cemri, M., et al.** — *MAST: Multi-Agent System Failure Taxonomy* (2025) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md), [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) |
| **Greshake, K., et al.** — *Not what you've signed up for* (2023, indirect prompt injection) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| **Hines, K., et al.** — *Spotlighting* (Microsoft Research, 2024) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| **Hong, S., et al.** — *MetaGPT* (2023) | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md), [References](references.md) |
| **Jimenez, C. E., et al.** — *SWE-bench* (2024) | [Coding Agents](../agents/08-coding-agents.md), [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Koh, J. Y., et al.** — *VisualWebArena* (2024) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **Li, K., et al.** — *ScreenSpot-Pro* (2024) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **Liang, P., et al.** — *HELM* (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Liu, N. F., et al.** — *Lost in the Middle* (2023) | [Coding Agents](../agents/08-coding-agents.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **Liu, X., et al.** — *AgentBench* (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Liu, Y., et al.** — *Agent Design Pattern Catalogue* (2024) | [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md), [References](references.md) |
| **Mialon, G., et al.** — *GAIA* (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Pope, R., et al.** — *Efficiently Scaling Transformer Inference* (2022) | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md), [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **Schick, T., et al.** — *Toolformer* (2023) | [References — Tool use](references.md) |
| **Weng, L.** — *LLM Powered Autonomous Agents* (2023) | [What Agents Are](../agents/01-what-agents-are.md) |
| **Willison, S.** — *Prompt Injection / Lethal Trifecta series* | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md), [Red-Team Protocol](../operating/08-red-team-protocol.md) |
| **Wu, Q., et al.** — *AutoGen* (2023) | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md), [References](references.md) |
| **Xie, T., et al.** — *OSWorld* (2024) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **Yang, J., et al.** — *SWE-agent* (2024) | [Coding Agents](../agents/08-coding-agents.md) |
| **Yao, S., et al.** — *ReAct* (2022) | [The Executor Model](../agents/03-agents-as-executors.md) |
| **Yao, S., et al.** — *τ-bench* (2024) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Zhang, Y., et al.** — *LLM-Agent Hallucinations Survey* (2025) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) |
| **Zheng, L., et al.** — *Judging LLM-as-a-Judge / MT-Bench* (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| **Zhou, S., et al.** — *WebArena* (2024) | [Computer-Use Agents](../agents/09-computer-use-agents.md) |

### Foundational software engineering and organizational

| Source | Cited in |
|---|---|
| **Alexander, C.** — *A Pattern Language* (1977) | [References — Pattern languages and design](references.md) |
| **Brooks, F. P.** — *The Mythical Man-Month* (1995) | [References — Software engineering foundations](references.md) |
| **Cohn, M.** — *User Stories Applied* (2004) | [References — Spec-driven development](references.md) |
| **Deming, W. E.** — *Out of the Crisis* (1982) | [Four Signal Metrics](../operating/06-metrics.md), [References](references.md) |
| **Forsgren, N., Humble, J., Kim, G.** — *Accelerate* (2018) | [Adoption Playbook](../operating/11-adoption-playbook.md) |
| **Fowler, M.** — *Patterns of Enterprise Application Architecture* (2002) | [Architectural Decision Records](../sdd/08-architectural-decision-records.md), [References](references.md) |
| **IEEE 830-1998 / ISO/IEC/IEEE 29148:2018** | [References — Spec-driven development](references.md) |
| **ISO/IEC 42001:2023** | [References — Governance and oversight](references.md) |
| **Jackson, M.** — *Software Requirements & Specifications* (1995) | [Writing for Machine Execution](../sdd/05-writing-specs-for-agents.md) |
| **Kim, G., Debois, P., Willis, J., Humble, J.** — *The DevOps Handbook* (2016) | [Proportional Governance](../operating/04-governance.md) |
| **Kotter, J. P.** — *Leading Change* (1996) | [Adoption Playbook](../operating/11-adoption-playbook.md) |
| **Meadows, D. H.** — *Thinking in Systems* (2008) | [The Living Spec](../sdd/06-living-specs.md), [Adoption Playbook](../operating/11-adoption-playbook.md) |
| **Meyer, B.** — *Object-Oriented Software Construction* (1997) | [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md) |
| **North, D.** — *Behaviour-Driven Development / Gherkin* | [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) |
| **Nygard, M.** — *Documenting Architecture Decisions* (2011) | [Architectural Decision Records](../sdd/08-architectural-decision-records.md), [DevSquad Mapping](../operating/12-devsquad-mapping.md) |
| **Ohno, T.** — *Toyota Production System* (1988, 5 Whys) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) |
| **Reason, J.** — *Human Error / Swiss-cheese model* (1990) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) |
| **Russell, S.** — *Human Compatible* (2019) | [References — AI ethics, alignment](references.md) |
| **Westrum, R.** — *A typology of organisational cultures* (2004) | [Adoption Playbook](../operating/11-adoption-playbook.md) |

---

*This list will be updated as the field develops. Suggestions and corrections are welcome via the book's repository.*
