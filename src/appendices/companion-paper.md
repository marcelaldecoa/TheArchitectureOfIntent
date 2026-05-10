# The Companion Paper

**Appendices**

---

This book has a companion academic paper: *The Architecture of Intent — A Framework for Designing Delegated Systems*. It is an arXiv-format distillation of the same framework, ~15,000 words and 34 pages, written for a different audience and a different reading mode.

This appendix tells you what is in the paper, who it is for, and how to read it alongside the book.

---

## Where to find it

The paper lives in this repository at [`paper/architecture-of-intent.pdf`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.pdf), with the editable Markdown source at [`paper/architecture-of-intent.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.md). A `pandoc + xelatex` toolchain compiles one to the other; the [build instructions](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/README.md) are in `paper/README.md`.

Two companion teaching decks accompany the paper — a PowerPoint at `paper/architecture-of-intent.pptx` and a self-contained HTML deck at `paper/architecture-of-intent.html`. Both are 19 slides, generated from a shared content source.

---

## Who the paper is for

The paper has a different reader than this book.

- **The book's reader** is a tech lead, staff engineer, or platform-team member who is on the hook for an agent system going to production. They read the book to make their next decision better.
- **The paper's reader** is a researcher, a reviewer, a conference attendee, or a senior practitioner evaluating the framework for adoption. They read the paper to decide whether the framework is worth the larger investment in the book.

The paper assumes more academic context (familiarity with SAE J3016, Shavit & Agarwal 2023, MAST, *Building Effective Agents*, the OWASP LLM Top 10) and less operational detail. The book assumes the inverse.

---

## What the paper covers, and where the book covers it

The paper is structured in seven sections plus two appendices. The mapping below tells you which book chapter elaborates each section, so a paper reader can use the book to dig deeper on any one topic.

| Paper section | What it covers | Book chapters that elaborate |
|---|---|---|
| **§1 Introduction** | The judgment gap; the framework's central claim; the three novel contributions | [Prologue](../prologue.md); [Introduction](../introduction.md); [What is the Architecture of Intent?](../introduction.md#what-is-the-architecture-of-intent) |
| **§2 Prior work and lineage** | Eight bodies of standing literature the framework operates within | [Reading List & References](references.md) |
| **§3 The framework** | The four load-bearing elements: intent, archetypes, dimensions, failure taxonomy, SDD; introduced with the framework canvas (Figure 1) | [The framework on one page](../introduction.md#the-framework-on-one-page); [A Miniature Pilot](../miniature-pilot.md) |
| **§3.1 Intent as a design surface** | The intent / implementation / requirements / policy distinctions | [Intent vs. Implementation](../theory/02-intent-vs-implementation.md) |
| **§3.2 Archetypes** | The five archetypes; the selection tree (Figure 2); composition as a first-class design surface | [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md); [The Archetype Selection Tree](../architecture/04-decision-tree.md); [Composing Archetypes](../architecture/05-composing-archetypes.md); [Intent Archetype Catalog](../repertoires/02-archetype-catalog.md); per-archetype pages under [`architecture/archetypes/`](../architecture/archetypes/advisor.md) |
| **§3.3 Four dimensions of calibration** | Agency, autonomy, responsibility, reversibility; the orthogonality argument (Figure 3); spec-clause mapping | [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md); [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) |
| **§3.4 The fix-locus failure taxonomy** | Cat 1–7, with Cat 7 (Perceptual) detailed | [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md); [Computer-Use Agents](../agents/09-computer-use-agents.md) |
| **§3.5 Spec-Driven Development** | SDD as the executable protocol; the canonical spec template | All of [Part 2 — The Spec](../sdd/01-what-sdd-means.md); especially [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) |
| **§4 Application to AI agent systems** | Agentic development lifecycle; capability boundaries via MCP; coding agents; computer-use agents | [The Agent](../agents/01-what-agents-are.md); [Least Capability](../agents/04-tools-mcp-capability-boundaries.md); [The Model Context Protocol](../agents/mcp/01-what-is-mcp.md); [Coding Agents](../agents/08-coding-agents.md); [Computer-Use Agents](../agents/09-computer-use-agents.md); [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) |
| **§4 Composition with DevSquad** | Phase-by-phase mapping into the DevSquad 8-phase agentic delivery cycle | [Mapping the Framework to the DevSquad 8-Phase Cadence](../operating/12-devsquad-mapping.md); [Co-adoption with DevSquad Copilot](../operating/13-co-adoption-with-devsquad.md) |
| **§5 Discussion** | Applicability boundary; complementarity with MAST; generalization beyond AI agents | [Multi-Agent Governance](../architecture/07-multi-agent-governance.md); [Failure Modes](../theory/05-failure-as-design-signal.md) §"How this taxonomy relates to the empirical literature" |
| **§6 Limitations** | Position-paper scope; what the framework does not do | [Introduction §"Honest scope"](../introduction.md#honest-scope-what-this-book-is-and-what-it-isnt); [Signs Your Architecture of Intent Is Degrading](../operating/15-anti-patterns.md) |
| **§7 Conclusion** | The framework's reach; future work | [Introduction](../introduction.md) |
| **Appendix A** | Paper → book mapping (the inverse of this page) | This appendix |
| **Appendix B** | Mapping the framework to Microsoft DevSquad Copilot | [Mapping the Framework to the DevSquad 8-Phase Cadence](../operating/12-devsquad-mapping.md); [Co-adoption with DevSquad Copilot](../operating/13-co-adoption-with-devsquad.md) |

---

## Reading modes

**Read the paper first if you are evaluating the framework.** The paper is shorter, more compressed, and structured for a reader who needs to decide whether the larger investment in the book is worth their time. It states the framework's commitments and contributions narrowly; it does not give you the working artifacts.

**Read the book first if you have decided to adopt the framework.** The book gives you the spec templates, the worked pilots, the patterns, and the rituals (Intent Design Session, Discipline-Health Audit) you actually run. The paper is the executive summary of why those artifacts have the shapes they do.

**Read both if you are building the framework into an organization.** The paper anchors the conversations you'll have with stakeholders evaluating the framework; the book anchors the conversations you'll have with the team building against it. Treat the paper as the citation, the book as the manual.

---

## Honest scope of the paper

The paper claims novelty for three things only — the orthogonality operationalization of agency and autonomy; the fix-locus framing of the failure taxonomy; and the Cat 7 (Perceptual) category. It explicitly does *not* claim novelty for SDD, archetypes-as-concept, the four dimensions individually, or Cat 1–6.

The same accounting applies to the book. When you cite the framework, cite what is novel as novel and the rest as synthesis. The ratio is documented in [the framework changelog](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) under the v1.0.0 entry.

---

## Framework version

This appendix and the rest of the book reflect framework **v1.3.0** (2026-05-10). The paper reflects the same framework version. Both move together — the framework's load-bearing commitments are versioned, and a change in either artifact that touches a load-bearing commitment bumps the framework version. See [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) at the repository root for the versioning convention and the release history.

---
