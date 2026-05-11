# The Architecture of Intent

**A Field Guide to Designing and Shipping AI Agent Systems**

*by Marcel Aldecoa*

---

## What this book is

A field guide for the tech lead, staff engineer, or platform team running their first — or next — AI-agent pilot. By the end of it, you should be able to:

1. **Pick an archetype** for the system you are about to build (Advisor, Executor, Guardian, Synthesizer, or Orchestrator).
2. **Calibrate** its agency, autonomy, responsibility, and reversibility deliberately rather than by accident.
3. **Write the spec** that the agent will execute against, using a canonical template.
4. **Build the agent** with the right capability boundaries, system prompt, skills, and tools.
5. **Set up oversight, safety, observability, and metrics** proportional to what the agent is allowed to do.
6. **Ship it** with canary, rollback, and spec versioning in place.

The book is structured by *order of decisions* — Decisions → Spec → Agent → Oversight → Ship — so a team can map it onto whatever timeline they actually have.

It is not a book about prompt engineering, model selection, or AI strategy. It assumes you already have access to a capable model and tooling. The discipline it teaches is the part that the model and the tooling do *not* give you: the structures around the agent that make delegation safe at scale.

## Who this is for

- **Tech leads and staff engineers** writing the spec, the system prompt, and the oversight model for an agent system going to production.
- **Platform teams** building the agent infrastructure, MCP tools, and governance scaffolding that other teams will reuse.
- **Architects** responsible for the structural integrity of systems that agents now help build and operate.

If you're trying to answer "how do we ship this agent without it doing something we'll regret?" — this is the book.

## How it's organized

The book is organized as five activities — Frame, Specify, Delegate, Validate, Evolve & Operate — preceded by a *Foundations* part that establishes the vocabulary.

| Part | Purpose |
|------|---------|
| **Prologue / Introduction / How to read** | What changed, what's at stake, and how to navigate the book |
| **0. Foundations** | What the Architecture of Intent is, intent vs implementation, the four calibration dimensions, failure as a design signal, what changes for senior engineers, the intent design session |
| **1. Frame** | Pick an archetype (Advisor, Executor, Guardian, Synthesizer, Orchestrator), the four orthogonal dimensions, the decision tree, composing archetypes, multi-agent compositions, *Frame in practice* scenarios |
| **2. Specify** | Spec-driven development, specs as control surfaces, the canonical 12-section template, ADRs, SpecKit, *Specify in practice* scenarios |
| **3. Delegate** | What agents are, autonomy vs agency, the executor model, least capability, tools and MCP, agent skills, agent classes (coding, computer-use, deep-research), *Delegate in practice* scenarios |
| **4. Validate** | Intent review, four signal metrics, evals, red-team, *Validate in practice* scenarios |
| **5. Evolve** | The closed loop, anti-patterns, framework versioning, the Minimum Viable Architecture of Intent, deployment patterns (canary, rollback, spec versioning, model-upgrade, deprecation), *Evolve in practice* scenarios |
| **6. Operations** | The sustaining-ops layer that runs alongside the five activities — proportional governance, cost & latency engineering, cacheable prompt architecture, production telemetry, the Adoption Playbook, DevSquad mapping and co-adoption. Not a sixth activity. |
| **7. Reference — Cross-Cutting Patterns** | Coordination and state patterns that span the framework (12 of ~50 patterns; the other 38 live alongside their parent chapters in Parts 3–6) |
| **Repertoires** | Spec templates, code standards |
| **Appendices** | Glossary, pattern index, reading paths, companion paper, legacy v1.x worked-pilots archive, references, archetype card, RACI card, MCP & skills card, model-tier card |

## Companion paper and teaching deck

Alongside the book, this repo also contains:

- **The paper** — `paper/architecture-of-intent.pdf` (and `.md` source). The arXiv-format distillation of the book, ~15,000 words / 34 pages. Position-and-framework paper.
- **A teaching deck** — `paper/architecture-of-intent.pptx` (PowerPoint) and `paper/architecture-of-intent.html` (self-contained browser deck). 19 slides built from a single source of truth.

A GitHub Action ("Compile paper & decks") rebuilds all three artifacts when the paper sources change on `main`.

## Building the book

This book is built with [mdBook](https://rust-lang.github.io/mdBook/) v0.5+.

```bash
# Install mdBook
cargo install mdbook   # or: winget install Rustlang.mdBook on Windows

# Clone and build
git clone https://github.com/marcelaldecoa/TheArchitectureOfIntent.git
cd TheArchitectureOfIntent
mdbook build
```

The compiled HTML is written to the `book/` directory. Open `book/index.html` to read offline.

```bash
# Serve with live reload at http://localhost:3000
mdbook serve --open
```

## Deployment

The book auto-deploys to GitHub Pages on every push to `main` via [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

Once enabled (Settings → Pages → Source: GitHub Actions), the site will live at:

```
https://marcelaldecoa.github.io/TheArchitectureOfIntent/
```

## Repository layout

```
TheArchitectureOfIntent/
├── book.toml
├── CHANGELOG.md                                # Framework version history
├── .github/workflows/
│   ├── deploy.yml                              # Auto-publish book to GitHub Pages on push to main
│   └── build-paper.yml                         # Auto-rebuild paper PDF + decks on source change
├── src/                                        # The book (mdBook source)
│   ├── SUMMARY.md                              # Table of contents
│   ├── introduction.md, how-to-read.md, prologue.md, miniature-pilot.md, cover.md
│   ├── images/                                 # Book-side image copies (canvas mirror, kept in sync by GH workflow)
│   ├── foundations/                            # Part 0: vocabulary — intent vs implementation, calibration, failure as design signal
│   ├── frame/                                  # Part 1: archetypes, dimensions, decision tree, composition + frame/scenarios/
│   ├── specify/                                # Part 2: SDD, the canonical spec template, ADRs, SpecKit + specify/scenarios/
│   ├── delegate/                               # Part 3: agents, autonomy vs agency, least capability, MCP, agent classes + delegate/scenarios/
│   ├── validate/                               # Part 4: intent review, signal metrics, evals, red-team + validate/scenarios/
│   ├── evolve/                                 # Part 5 (EVOLVE): closed loop, anti-patterns, framework versioning, MVP-AoI, deployment patterns + evolve/scenarios/
│   ├── operate/                                # Part 6 (OPERATIONS): governance, cost & latency, cacheable prompts, telemetry, adoption playbook, DevSquad mapping & co-adoption
│   ├── patterns/                               # ~50 pattern one-pagers (capability, integration, coordination, safety, observability, testing, state, deployment)
│   ├── repertoires/                            # Spec templates, code standards
│   ├── examples/                               # v1.x worked pilots archive (preserved on disk; reached via appendices/legacy-pilots.md)
│   └── appendices/                             # Glossary, pattern index, reading paths, companion paper, legacy-pilots archive, references, quick-select cards
├── paper/                                      # Companion arXiv paper + teaching deck
│   ├── architecture-of-intent.{md,pdf}         # Paper source + compiled PDF
│   ├── architecture-of-intent.{pptx,html}      # Teaching deck (PowerPoint + self-contained HTML)
│   ├── presentation_content.py                 # Single source of truth for both decks
│   ├── build_{presentation,html_presentation}.py   # Deck builders
│   ├── check-deck-sync.py                      # Drift detector between paper and deck
│   ├── figures/                                # Figure SVGs + pre-rendered PNGs (canvas, decision tree, orthogonality)
│   └── references.bib                          # Bibliography
├── scripts/                                    # Helper scripts (link checker, orphan checker)
└── theme/                                      # Custom CSS and zoom widget
```

## Framework version

The framework is at **v2.4.0** as of 2026-05-10. The book and the companion paper move together: a change to a load-bearing commitment (the five archetypes, the four dimensions, the seven failure categories, the four oversight models, the four signal metrics, the **five** activities, composition as a first-class design surface) bumps the framework version. See [`CHANGELOG.md`](CHANGELOG.md) for the versioning convention and the release history.

## Status

The book is structured as a working pilot playbook. It is opinionated and incomplete by design: the archetype framework, the spec template, the oversight models, and the failure taxonomy are stable; the pattern reference will keep growing as more pilots ship and surface new patterns worth naming.

If you adopt any of the patterns here, the most valuable thing you can contribute back is a record of what worked, what failed, and what needs refinement. Disciplines are built from accumulated practice, not from theory.

## References

- [Spec-Driven Development](https://github.com/github/spec-kit) — modern spec-first AI development methodology
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Model Context Protocol](https://modelcontextprotocol.io/)
