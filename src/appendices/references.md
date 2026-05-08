# Reading List & References

**Appendices** · *Appendix C*

---

> *"Every book is in conversation with other books. These are the ones this book is most explicitly in debt to, and the ones a serious practitioner should read alongside it."*

---

This appendix is organized by topic. Within each topic, a short **Read first** subsection identifies the one or two primary sources that contain most of what you need; **Further reading** provides depth. Citations referenced inline within chapters carry through to the chapter-level References sections.

A note on honest framing: much of what this book describes is not novel. It synthesizes work from the agent design literature (Anthropic, OpenAI, LangChain), AI governance literature (NIST, ISO, OpenAI), spec-driven development practice (GitHub spec-kit), classical software engineering (Brooks, Meyer, Jackson), and human-systems thinking (Deming, Meadows, Reason). Where the book contributes, it contributes a synthesis with consistent vocabulary and an opinionated archetype frame; the underlying ideas are mostly older. The reading list below makes that lineage explicit.

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
- **Microsoft.** (2024–2025). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot (site at microsoft.github.io/devsquad-copilot). — Parallel work from Microsoft arriving at compatible conclusions from a different angle. Where this book gives you a *design vocabulary* (archetypes, dimensions, failure taxonomy), DevSquad gives you a *delivery cadence* — an 8-phase iterative cycle (envisioning → thin-slice spec → plan with ADRs → decompose → TDD-first implement → learn → independent review → continuous refinement). The two converge on living specs, risk-tiered human-in-the-loop, principle of least privilege, context isolation across sub-agents, and spec-first response to failure. They diverge on emphasis: DevSquad is process-prescriptive and centered on multi-developer Copilot teams; this book is process-agnostic and centered on agent-system design with deeper coverage of failure modes, prompt injection, evals, and telemetry. Recommended as a complementary read — a team adopting DevSquad's 8-phase cadence plus this book's archetype framework, failure taxonomy, and security/eval/telemetry stacks would have a more complete operating model than either source provides alone. Notable distinctive contribution from DevSquad: the explicit treatment of ADRs as a first-class durable artifact alongside specs.

**Further reading**

- **Jackson, M.** (1995). *Software Requirements & Specifications: A Lexicon of Practice, Principles, and Prejudices.* Addison-Wesley. — The domain/machine distinction maps directly onto the book's intent/implementation distinction. Read for the precision of the language and the discipline of problem framing.
- **Meyer, B.** (1997). *Object-Oriented Software Construction* (2nd ed.). Prentice Hall. — Origin of Design by Contract. The constraint sections of an SDD spec are Design by Contract for agent behavior.
- **IEEE 830-1998 / ISO/IEC/IEEE 29148:2018.** *Software Requirements Specifications.* — The canonical SRS structure; sections 1–3, 5, 7, 9 of the Canonical Spec Template are recognizably descended from this lineage.
- **Cohn, M.** (2004). *User Stories Applied.* — INVEST criteria for specifications.
- **North, D.** (2006, ongoing). *Behaviour-Driven Development* and the Gherkin Given/When/Then format. — Source of the acceptance criteria style used in Section 9.

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

Specific sources cited within chapters of this book:

| Source | Cited in |
|---|---|
| Anthropic, *Building Effective Agents* (2024) | [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md) |
| Anthropic, *Model Context Protocol* | [Least Capability](../agents/04-tools-mcp-capability-boundaries.md), [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md) |
| Anthropic, *Constitutional Classifiers* (2025) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| Cemri et al., MAST (2025) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) |
| GitHub spec-kit | [Spec-Driven Development](../sdd/01-what-sdd-means.md), [SpecKit](../sdd/04-speckit.md) |
| Microsoft DevSquad Copilot | [The Living Spec](../sdd/06-living-specs.md), [Adoption Playbook](../operating/11-adoption-playbook.md) |
| Greshake et al. (2023) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| Hines et al., Spotlighting (2024) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| Jimenez et al., SWE-bench (2024) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| Liang et al., HELM (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| Liu et al., AgentBench (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| Liu et al., *Agent Design Pattern Catalogue* (2024) | [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md) |
| Mialon et al., GAIA (2023) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| OWASP LLM Top 10 (2025) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| SAE J3016 | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) |
| Shavit, Agarwal et al. (OpenAI 2023) | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md) |
| Weng, L., *LLM Powered Autonomous Agents* (2023) | [What Agents Are](../agents/01-what-agents-are.md) |
| Willison, S., *Prompt Injection / Lethal Trifecta* | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| Yao et al., ReAct (2022) | [The Executor Model](../agents/03-agents-as-executors.md) |
| Yao et al., τ-bench (2024) | [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) |
| Zhang et al., LLM-Agent Hallucinations (2025) | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) |

---

*This list will be updated as the field develops. Suggestions and corrections are welcome via the book's repository.*
