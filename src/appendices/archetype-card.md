# Archetype Quick-Select Card

**Appendices** · *Appendix E*

---

> *"The archetype is the pre-commitment. The spec is the application of the pre-commitment. The agent is the execution of the spec."*

---

Use this card to quickly identify which archetype applies to your system. For full definitions, see [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md).

---

## The Five Canonical Intent Archetypes

| Archetype | Core Function | Agency Level | Risk Posture | Oversight Model |
|-----------|---------------|:------------:|:------------:|:---------------:|
| **Advisor** | Surfaces information, options, and recommendations — never acts | Minimal | Low | Human decides and acts |
| **Executor** | Carries out well-defined tasks autonomously within strict bounds | High | Medium | Pre-approved scope; exception escalation |
| **Guardian** | Enforces rules, validates integrity, and prevents constraint violations | Low (veto only) | Low | Alerts; humans resolve |
| **Synthesizer** | Aggregates, distills, or composes from multiple sources | Moderate | Medium | Human reviews outputs above threshold |
| **Orchestrator** | Coordinates multiple agents or services toward a compound goal | High | High | Active oversight; escalation paths required |

---

## Quick-Select Decision Tree

```
Does your system make any consequential decisions autonomously?
├── NO → Advisor
└── YES
    └── Is its primary job to ENFORCE or PREVENT?
        ├── YES → Guardian
        └── NO
            └── Does it coordinate MULTIPLE agents or services?
                ├── YES → Orchestrator
                └── NO
                    └── Does it primarily AGGREGATE / COMPOSE information?
                        ├── YES → Synthesizer
                        └── NO → Executor
```

---

## Dimension Summary

### Agency
*How much discretion does the system exercise?*

| Archetype | Agency |
|-----------|--------|
| Advisor | None — surfaces options only |
| Guardian | Veto only — can block, not initiate |
| Synthesizer | Moderate — decides how to combine, not what to act on |
| Executor | High — acts within pre-defined scope autonomously |
| Orchestrator | High — delegates to sub-agents, manages compound state |

### Reversibility Sensitivity
*How critical is reversibility to the design?*

| Archetype | Reversibility Concern |
|-----------|-----------------------|
| Advisor | Not applicable — no actions taken |
| Guardian | High — enforcement actions may be irreversible |
| Synthesizer | Medium — outputs may be distributed |
| Executor | High — tasks may modify state |
| Orchestrator | Critical — coordinates multiple state-changing steps |

### Minimum Oversight Requirements

| Archetype | Minimum Oversight |
|-----------|-------------------|
| Advisor | None required for output; human must act |
| Guardian | Monitoring + alert routing to human resolver |
| Synthesizer | Human review above defined confidence/scope threshold |
| Executor | Pre-approved scope + exception escalation path |
| Orchestrator | Active human oversight at key coordination points |

---

## Common Mistakes

**Using Executor when Guardian is needed**
If the system's primary job is to prevent bad things rather than do good things, it is a Guardian. Executors act; Guardians veto.

**Using Orchestrator for a simple automation sequence**
If there is no agent-to-agent coordination or compound state management, an Executor is simpler and safer. Orchestrators are for genuinely multi-agent, multi-step compound goals.

**Forgetting that systems can composite archetypes**
A real system often instantiates multiple archetypes in different layers. A customer support system might be an **Advisor** at the user interface, an **Executor** for ticket creation, and a **Guardian** for PII handling. See [Archetype Composition](../architecture/05-composing-archetypes.md).

---

*For full archetype specifications, see Part III: [Intent Architecture](../architecture/01-archetypes-as-constitutional-law.md)*

