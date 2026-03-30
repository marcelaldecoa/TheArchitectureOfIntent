# The Synthesizer Archetype

**Part III: Intent Architecture** · *Archetype Deep Dive 4 of 5*

---

> *"The value of synthesis is not the aggregation. Any database can aggregate. The value is the judgment about what to include, what matters, and how to present it so the right decision becomes clear."*

---

## Identity

**Primary Act:** Compose  
**Discretion Scope:** Moderate — selects what to include, how to structure, and what emphasis to apply; does not act on the produced artifact

The Synthesizer aggregates information from multiple sources, applies compositional judgment — deciding relevance, structure, and emphasis — and produces a coherent artifact for human consumption or downstream use. It acts on information, not on external systems. Like the Advisor, it produces rather than executes. Unlike the Advisor, it operates across multiple sources and applies meaningful compositional judgment.

---

## The Defining Characteristic

The Synthesizer's defining characteristic is its **multi-source compositional judgment**: it is not merely retrieving and presenting a single source, nor executing a transformation with a defined mapping. It is deciding *across sources* what matters and assembling it into a coherent whole.

This is why the Synthesizer has a higher agency level than the Advisor. The Synthesizer exercises genuine judgment about what to include, what to omit, how to weight competing signals, and how to structure the output for clarity. That judgment is real discretion — and it must be bounded.

The boundary: the Synthesizer's discretion applies to the *artifact it produces*, not to *what happens to the artifact*. The Synthesizer does not decide whether the artifact gets published, deployed, or acted upon.

---

## Typical Forms

- **Research synthesizer**: Reads multiple sources (documents, databases, search results), produces a structured summary or analysis for a human researcher.
- **Status report generator**: Aggregates data from multiple systems (metrics, tickets, alerts, deployments), produces a coherent status digest for a human reviewer.
- **Code review synopsis**: Reads multiple PRs, issues, or test results, produces a prioritized synthesis for an engineering lead.
- **Risk assessment composer**: Reads from multiple risk signals (logs, dependency data, policy checks), produces a composed risk profile for a security reviewer.
- **Competitive intelligence report**: Aggregates from multiple market sources, produces a structured briefing for a human strategist.
- **Meeting notes synthesizer**: Processes multiple inputs (transcript, agenda, action items), produces a structured meeting record for human distribution.

---

## Agency Profile

| Dimension | Typical Value | Range |
|-----------|:-------------:|-------|
| Agency Level | 3 | 2–3 |
| Risk Posture | Low to Medium | Low to Medium |
| Oversight Model | B (Periodic Review) | A or B |
| Reversibility | Fully to Largely reversible | R1–R2 |

**Why Agency Level 3 (not 1–2 like the Advisor):** The Synthesizer exercises meaningful compositional judgment — it decides what is relevant across sources, which signals outweigh others. This is not retrieval; it is editorial. Agency Level 3 is appropriate for editorial judgment within a bounded domain.

**Why Risk Posture Low to Medium:** The Synthesizer's direct output is an artifact for human consumption. The risk is in the quality and accuracy of the synthesis — an incorrect or misleading synthesis can cause a human to make a poor decision. This is real risk, but it is mediated by human judgment. The risk escalates to Medium when the synthesis domain is high-stakes (medical, financial, security), because the errors are hard to detect and the downstream decisions are consequential.

---

## Invariants

1. **The artifact is produced for human evaluation, not for automated consumption.** If the Synthesizer's output automatically feeds another system that takes action, the composition has changed — the Synthesizer is now embedded in an Executor or Orchestrator, and its governance requirements have escalated.

2. **Source references are preserved.** The Synthesizer does not strip attribution. Any factual claim in the synthesized artifact is traceable to a source, either inline or in an appendix. A synthesis that cannot be verified is an assertion, not a synthesis.

3. **The scope of sources is declared.** The Synthesizer does not autonomously expand what it reads. The declared sources — databases, APIs, document collections — are specified in the spec and reviewed. Reaching outside declared sources is a constraint violation.

4. **Compositional criteria are specified.** The spec declares what the Synthesizer prioritizes: recency? relevance score? specific signal types? These criteria are not left to the system's general intelligence. They are declared, so the synthesis can be audited against them.

5. **Uncertainty is surfaced, not hidden.** When the Synthesizer cannot confidently resolve a question from its sources — conflicting data, insufficient coverage — it says so. It does not synthesize a confident answer from insufficient evidence.

---

## The Quality Problem

The most common failure of a Synthesizer-class system is not scope violation — it is quality degradation that erodes trust and, eventually, oversight.

When a Synthesizer is trusted, humans read its output carefully and validate against sources. When a Synthesizer is *highly* trusted, humans skim it and assume it's right. When a Synthesizer has been wrong occasionally without anyone noticing, it is operating in the most dangerous condition: it produces confident output, humans trust it implicitly, and errors compound.

The design principle: build skepticism triggers into the synthesis itself. Explicit confidence signals, flagged uncertainties, and surface-level consistency checks in the output are not signs of weakness — they are the mechanism by which human judgment remains engaged.

A synthesis that always looks equally confident regardless of source quality, coverage gaps, or conflicting signals is training its readers to stop thinking. That is a design failure.

---

## Synthesizer vs. Advisor (The Distinction)

| | Advisor | Synthesizer |
|---|---|---|
| Source scope | Typically single source or narrow query | Multiple sources by design |
| Compositional judgment | Minimal (retrieval and formatting) | Substantial (what to include, how to weight) |
| Agency level | 1–2 | 3 |
| Typical form | Q&A, retrieval, recommendation | Report, analysis, digest |
| Risk vector | Wrong recommendation | Misleading synthesis, false confidence |

An Advisor answers: *"Here is the relevant information."*  
A Synthesizer answers: *"Here is my assessment, assembled from these sources."*

The "my assessment" is the difference. Agency Level 3 names that judgment explicitly, so it can be scoped and governed.

---

## Spec Template Fragment

```markdown
## Archetype

**Classification:** Synthesizer  
**Agency Level:** 3 — Editorial (exercises compositional judgment about 
                  relevance, structure, and emphasis across declared sources)  
**Risk Posture:** Low / Medium (produces artifact for human evaluation; 
                  risk scales with stakes of downstream decisions)  
**Oversight Model:** B — Periodic review (output quality reviewed on cadence 
                  [weekly/per-run]; alert on anomalous output patterns)  
**Reversibility:** R1 — Fully reversible (artifact can be disregarded; 
                  no external state mutation)

## Source Scope

**Authorized sources:**
- [Source 1]: [access level — read only, specific tables/endpoints]
- [Source 2]: [access level]

**Explicitly NOT in scope:**
- [Excluded sources]

## Compositional Criteria

Priority signals:
1. [Signal type] — weighted [high/medium/low]
2. [Signal type] — weighted [high/medium/low]

Conflict resolution: [how conflicting signals are handled]
Confidence threshold: [when uncertainty must be stated rather than resolved]

## Invariants

1. All factual claims in output include source attribution.
2. Source scope does not expand autonomously.
3. Conflicting or insufficient signals are surfaced, not silently resolved.
4. Output is produced for [specific consumer]; automated downstream consumption 
   requires separate Executor governance.
```

---

## Failure Analysis

| Failure Type | Synthesizer Manifestation | Response |
|---|---|---|
| Intent Failure | Synthesis is technically accurate but not useful for the decision at hand | Compositional criteria are wrong; re-examine what the human consumer actually needs |
| Context Failure | Sources are stale, incomplete, or outside declared scope | Freshen data contracts; re-examine source scope declaration |
| Constraint Violation | Output flows automatically to a downstream action system without human gate | Architecture change required; Synthesizer output must pass through human or output gate |
| Implementation Failure | Poor editorial judgment — wrong things highlighted, buried lede, false confidence | May be implementation issue; spec may need more explicit compositional criteria |

---

## Connections

**Archetype series:** [← Guardian](guardian.md) · [Orchestrator →](orchestrator.md)  
**Governing patterns:** [Canonical Intent Archetypes](../02-canonical-intent-archetypes.md) · [Archetype Dimensions](../03-archetype-dimensions.md) · [Decision Tree](../04-decision-tree.md)  
**Composition:** [Composing Archetypes](../05-composing-archetypes.md) — Synthesizer + Executor composition in compose-then-publish patterns  
**SDD:** [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)

