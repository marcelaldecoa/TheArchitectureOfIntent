# The Architecture of Intent — paper + companion teaching deck

The `paper/` directory contains the academic distillation of the book, plus a 19-slide teaching deck (PowerPoint + self-contained HTML) for explaining the framework to others.

## Status

**Complete v1.** 34 pages, ~15,000 words. arXiv-ready. Position-and-framework paper without empirical validation at scale (acknowledged explicitly in §6).

The teaching deck is a current, modern companion intended for workshops, recruiter screens, and onboarding sessions.

## Files

| File | Purpose |
|---|---|
| `architecture-of-intent.md` | Paper Markdown source (Pandoc + citation syntax) |
| `architecture-of-intent.pdf` | Compiled paper PDF — committed for convenience |
| `architecture-of-intent.pptx` | Teaching deck (PowerPoint, 16:9) — committed |
| `architecture-of-intent.html` | Teaching deck (self-contained HTML) — committed |
| `references.bib` | BibTeX bibliography (~30 entries across 9 domains) |
| `figures/architecture-of-intent-canvas.svg` + `.png` | Figure 1 — the framework on one page; referenced in §3 (and mirrored to `src/images/` for the book) |
| `figures/archetype-decision-tree.svg` + `.png` | Figure 2 — referenced in §3.2 |
| `figures/four-dimensions-orthogonality.svg` + `.png` | Figure 3 — referenced in §3.3 |
| `presentation_content.py` | Single source of truth for both decks (slide data + palette) |
| `build_presentation.py` | Builds the PPTX from `presentation_content.py` |
| `build_html_presentation.py` | Builds the HTML deck from `presentation_content.py` |
| `check-deck-sync.py` | Drift detector — verifies load-bearing names match between paper and deck |
| `README.md` | This file |

## Building the paper

The Pandoc command (also used by the GH Action):

```bash
cd paper
pandoc architecture-of-intent.md \
  --citeproc \
  --bibliography references.bib \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  --output architecture-of-intent.pdf
```

Required tooling: `pandoc`, `texlive-xetex`, `texlive-fonts-recommended`, `texlive-latex-recommended`, `texlive-latex-extra`, `lmodern`. The `lmodern` package is a separate package on Ubuntu and is required for `lmodern.sty` (xelatex's default font setup).

## Building the teaching deck

```bash
python3 paper/build_presentation.py        # → paper/architecture-of-intent.pptx
python3 paper/build_html_presentation.py   # → paper/architecture-of-intent.html
```

Requirements: `python-pptx`, `Pillow`, `lxml`. Both builders consume `paper/presentation_content.py` as their single source of truth — edit slide content in one place, rerun both builders. The HTML deck supports arrow-key navigation, an overview grid (`o`/`Esc`), fullscreen (`f`), and print-to-PDF (`p`). Both paper figures are embedded as inline SVG, so the file is portable.

## Sync check (paper ↔ deck)

```bash
python3 paper/check-deck-sync.py
```

Verifies that the small set of load-bearing named facts match between paper and deck:
- Five archetype names
- Seven failure category names (Cat 1–Cat 7)
- Four Cat 7 sub-category names
- Eight DevSquad phase names (paper-side check; deck condenses some rows)
- "3 novel / 4 not-claimed" honest-accounting cardinality

Run it before committing any change to either source. The script does NOT enforce prose alignment — only named-fact alignment. Freeform deck narrative can differ from paper prose.

If you intentionally rename or add a load-bearing fact, update **all three**:
1. `paper/architecture-of-intent.md`
2. `paper/presentation_content.py`
3. `paper/check-deck-sync.py` — the `CANONICAL_*` lists at the top

## Auto-rebuild on `main`

The GitHub Action **"Compile paper & decks"** (`.github/workflows/build-paper.yml`) fires on push to `main` whenever any of these change:
- `paper/architecture-of-intent.md`, `paper/references.bib`
- `paper/figures/**.svg`
- `paper/build_presentation.py`, `paper/build_html_presentation.py`, `paper/presentation_content.py`
- `.github/workflows/build-paper.yml`

The workflow:
1. Runs `check-deck-sync.py` (fails fast on drift before any build steps)
2. Regenerates each `figures/*.png` from its `.svg` via `rsvg-convert --width=1800`
3. Builds the PPTX deck
4. Builds the HTML deck
5. Compiles the paper PDF
6. Uploads everything as workflow artifacts (90-day retention)
7. Opens (or updates) a single `bot/paper-artifacts` PR with the rebuilt artifacts via `peter-evans/create-pull-request@v7`

The auto-PR pattern works regardless of branch protection on `main`. Loop-safety: trigger watches *source* paths only; the bot's commit only touches *artifact* paths, so it can't retrigger itself.

## Honest contribution accounting

The paper claims novelty for three things:

1. **Cat 7 (Perceptual Failure)** — a new failure category for perceiving-then-acting agents that prior taxonomies (MAST, hallucination surveys, OWASP LLM Top 10) do not cover.
2. **Autonomy-vs-agency operationalization** — extending Shavit & Agarwal (2023) by treating autonomy and agency as orthogonal axes with explicit mapping to spec design.
3. **The fix-locus framing** of the failure taxonomy — Cat 1–7 partitioned by which artifact must change.

The paper explicitly does *not* claim novelty for: SDD as a discipline (lineage from GitHub spec-kit and Microsoft DevSquad Copilot); archetypes as a concept (lineage from Anthropic's *Building Effective Agents*); the four dimensions individually (lineage from SAE J3016 and Shavit & Agarwal); or Cat 1–6 as categories (synthesis from common practice).

This honest accounting is in the abstract, §1.3, and §5. Reviewers reward it; overclaiming gets punished disproportionately.

## Figures

All three figures are SVG sources that pre-render to PNG. The paper Markdown references the PNG files (arXiv-portable; `librsvg2-bin` is not required at compile time). To regenerate the PNGs after editing an SVG:

```bash
rsvg-convert --format=png --width=1800 paper/figures/architecture-of-intent-canvas.svg \
  --output paper/figures/architecture-of-intent-canvas.png
rsvg-convert --format=png --width=1800 paper/figures/archetype-decision-tree.svg \
  --output paper/figures/archetype-decision-tree.png
rsvg-convert --format=png --width=1800 paper/figures/four-dimensions-orthogonality.svg \
  --output paper/figures/four-dimensions-orthogonality.png
```

Or just push to `main` and let the workflow do it. The "Compile paper & decks" workflow also mirrors the canvas PNG into `src/images/` so the book's *Introduction → The framework on one page* section stays in sync with the paper's Figure 1.

If the paper goes to a workshop or journal that prefers TikZ, both figures can be re-rendered natively in LaTeX from the same logical content; SVG is the working format until then.

## Citation style

Pandoc-style `[@key]` inline citations. Bibliography in `references.bib`. Pandoc with `--citeproc --bibliography references.bib` resolves all citations and renders the bibliography in place at compile time.

Bibliography contents (~30 entries across 9 domains): Spec-Driven Development, driving automation, agent governance, multi-agent failure analysis, indirect injection and safety, inference economics, pattern languages, systems thinking, coding agents and benchmarks, compliance and standards.

**Citation key convention:** `<authorOrOrg><Topic><Year>` — e.g., `@anthropicMCP2024`, `@microsoftDevSquadCopilot2026`, `@cemriMAST2025`.

## Relation to the book

The book is the practitioner's field guide; the paper is the academic distillation. The book covers ~80,000 words of practice-oriented material; the paper distills the conceptual contributions to ~15,000 words for citation and academic uptake. Appendix A in the paper maps each paper section back to the relevant book chapter so readers can read the paper as a summary and the book as the reference.

## Open work

- **arXiv submission** — mechanical from the current PDF; action is on the human, not on Claude.
- **Length-cut version for workshop submission** (10–12 pages from the current 34). Strategy noted in CLAUDE.md.
- **Empirical validation** — future-work track. Surveying practitioner adoption across deployments for a "v2" empirical paper.
