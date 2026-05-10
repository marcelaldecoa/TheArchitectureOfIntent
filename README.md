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

| Part | Purpose |
|------|---------|
| **Prologue** | What changed, what's at stake, and what this playbook gives you |
| **1. Decisions** | Pick an archetype, calibrate the four dimensions, anticipate failure, separate intent from implementation |
| **2. The Spec** | Spec-driven development, the canonical template, writing for machine execution, living specs |
| **3. The Agent** | What agents are, capability boundaries, knowledge & context, tools and MCP |
| **4. Oversight, Safety & Operations** | Proportional oversight, safety patterns, retry, observability, conformance testing |
| **5. Ship** | Canary, rollback, versioning, governance cadence, signal metrics, intent review |
| **6. Worked Pilots** | Two end-to-end examples: AI customer support, and a code-generation pipeline |
| **Cross-Cutting Patterns** | Coordination and state patterns that span the framework (12 of ~50 patterns; the other 38 live alongside their parent chapters in Parts 3–5) |
| **Repertoires & Reference** | Spec templates, archetype catalog, validation templates, code standards |
| **Appendices** | Glossary, archetype card, MCP & SpecKit references, pattern index |

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
├── .github/workflows/deploy.yml
├── src/
│   ├── SUMMARY.md            # Table of contents
│   ├── introduction.md
│   ├── how-to-read.md
│   ├── prologue.md           # Short prologue: what changed and what's at stake
│   ├── architecture/         # Archetypes, decision tree, dimensions, composition
│   ├── theory/               # Intent vs implementation, calibration, failure diagnosis
│   ├── sdd/                  # Spec-driven development
│   ├── agents/               # Agents, MCP, oversight
│   ├── patterns/             # ~50 pattern one-pagers (capability, integration, coordination, ...)
│   ├── repertoires/          # Templates, archetype catalog, code standards
│   ├── operating/            # Governance, metrics, intent review
│   ├── examples/             # End-to-end worked pilots
│   └── appendices/           # Glossary, archetype card, references, pattern index
├── paper/                    # Companion arXiv paper + teaching deck
│   ├── architecture-of-intent.{md,pdf}    # Paper source + compiled PDF
│   ├── architecture-of-intent.{pptx,html} # Teaching deck (PowerPoint + self-contained HTML)
│   ├── presentation_content.py             # Single source of truth for both decks
│   ├── build_{presentation,html_presentation}.py  # Deck builders
│   ├── check-deck-sync.py                  # Drift detector between paper and deck
│   ├── figures/                            # Figure SVGs + pre-rendered PNGs
│   └── references.bib                      # Bibliography
├── scripts/                  # Helper scripts (link checker, orphan checker)
└── theme/                    # Custom CSS and zoom widget
```

## Framework version

The framework is at **v2.0.0-rc3** as of 2026-05-10. The book and the companion paper move together: a change to a load-bearing commitment (the five archetypes, the four dimensions, the seven failure categories, the four oversight models, the four signal metrics, the **five** activities, composition as a first-class design surface) bumps the framework version. See [`CHANGELOG.md`](CHANGELOG.md) for the versioning convention and the release history.

## Status

The book is structured as a working pilot playbook. It is opinionated and incomplete by design: the archetype framework, the spec template, the oversight models, and the failure taxonomy are stable; the pattern reference will keep growing as more pilots ship and surface new patterns worth naming.

If you adopt any of the patterns here, the most valuable thing you can contribute back is a record of what worked, what failed, and what needs refinement. Disciplines are built from accumulated practice, not from theory.

## References

- [Spec-Driven Development](https://github.com/github/spec-kit) — modern spec-first AI development methodology
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Model Context Protocol](https://modelcontextprotocol.io/)
