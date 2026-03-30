# The Architecture of Intent

**Designing Agency in an Age Where Code Is No Longer Scarce**

*by Marcel Aldecoa*

---

> *"This site is a living body of knowledge for intent engineering: how humans author behavior, how agency is distributed, and how systems are safely delegated to agents at scale."*

---

## About This Book

*The Architecture of Intent* is a body of knowledge for **intent engineering** — the emerging discipline of designing, specifying, and governing the delegation of work to AI agents at scale.

It is structured as a **pattern language**, inspired by Christopher Alexander's *A Pattern Language* (1977). Each chapter is a pattern: a named, recurring solution to a recurring problem, connected to the patterns it assumes and the patterns it enables.

The book moves deliberately from philosophy → theory → method → execution:

| Part | Topic |
|------|-------|
| **I: Foundations** | Why this shift is happening and what it means |
| **II: Theory** | The formal vocabulary of intent engineering |
| **III: Intent Architecture** | Archetypes, constitutional design, decision structures |
| **IV: Spec-Driven Development** | How intent becomes executable |
| **V: Agents & Execution** | What agents are, and how to delegate safely |
| **VI: Standards & Repertoires** | Templates, catalogs, and pre-authorized structures |
| **VII: Operating the System** | Skills, governance, and org design |
| **VIII: Applied Examples** | End-to-end real systems |

---

## Prerequisites

This book is built with [mdBook](https://rust-lang.github.io/mdBook/) v0.5+.

### Install mdBook

**Option A — winget (Windows, recommended):**
```powershell
winget install Rustlang.mdBook
```

**Option B — cargo (cross-platform, requires [Rust](https://rustup.rs)):**
```bash
# Install Rust toolchain (if not already installed)
# Windows: download and run https://win.rustup.rs
# macOS/Linux:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Then install mdBook
cargo install mdbook
```

**Option C — prebuilt binary:**  
Download the latest release from [github.com/rust-lang/mdBook/releases](https://github.com/rust-lang/mdBook/releases), extract, and add to your PATH.

---

## Building the Book

```bash
# Clone the repository
git clone https://github.com/marcelaldecoa/TheArchitectureOfIntent.git
cd TheArchitectureOfIntent

# Build static output to book/
mdbook build
```

The compiled HTML is written to the `book/` directory. Open `book/index.html` in any browser to read offline.

---

## Local Development

```bash
# Serve with live reload at http://localhost:3000
mdbook serve --open
```

The dev server watches `src/` for changes and rebuilds automatically. The browser refreshes on save.

> **Windows note:** After installing mdBook for the first time, open a new terminal session so the updated PATH is picked up before running `mdbook`.

---

## Repository Structure

```
TheArchitectureOfIntent/
├── book.toml           # mdBook configuration (author, theme, search, MathJax)
├── src/
│   ├── SUMMARY.md      # Table of contents — defines all pages and their order
│   ├── introduction.md
│   ├── preface.md
│   ├── how-to-read.md
│   ├── foundations/    # Part I  (6 chapters)
│   ├── theory/         # Part II (6 chapters)
│   ├── architecture/   # Part III (6 chapters + 5 archetype deep-dives)
│   ├── sdd/            # Part IV (7 chapters)
│   ├── agents/         # Part V  (7 chapters + 3 MCP sub-chapters)
│   ├── repertoires/    # Part VI (5 chapters + templates + code standards)
│   ├── operating/      # Part VII (6 chapters)
│   ├── examples/       # Part VIII (2 end-to-end examples)
│   └── appendices/     # Glossary, Pattern Index, References, Quick-Reference cards
├── theme/
│   ├── custom.css      # Custom styling overrides
│   └── zoom.js         # Floating font-size zoom widget (A+/A−)
└── book/               # Build output (git-ignored)
```

---

## Status

**Complete.** All 82 content files are written across all 8 Parts and 6 Appendices.

| Section | Files | Status |
|---------|-------|--------|
| Cover + front matter (cover, intro, preface, how-to-read) | 4 | ✅ |
| Part I: Foundations | 6 | ✅ |
| Part II: Theory | 6 | ✅ |
| Part III: Intent Architecture | 11 | ✅ |
| Part IV: Spec-Driven Development | 7 | ✅ |
| Part V: Agents & Execution | 10 | ✅ |
| Part VI: Standards & Repertoires | 14 | ✅ |
| Part VII: Operating the System | 6 | ✅ |
| Part VIII: Applied Examples | 12 | ✅ |
| Appendices A–F | 6 | ✅ |

---

## Inspiration

- [A Pattern Language](https://www.amazon.com/Pattern-Language-Buildings-Construction-Environmental-ebook/dp/B07J1T8P1W/ref=tmm_kin_swatch_0) — Christopher Alexander (1977)
- [Spec-Driven Development](https://github.com/github/spec-kit) — modern AI-native development methodology
- [SpecKit](https://github.com/github/spec-kit) — open-source toolkit for spec-first agent development
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) — skill-based agent architecture
- [Anthropic Skills](https://github.com/anthropics/skills) — reusable skill definitions for AI agents

