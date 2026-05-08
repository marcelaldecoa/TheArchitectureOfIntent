# The Architecture of Intent — paper

Companion arXiv paper to the book of the same title.

## Status

**Skeleton draft (v0.1).** The structure, abstract, section purposes, key claims, contribution accounting, and reference list are in place. Each section contains either prose (where it's already written) or a `*Stub paragraph*` block (where it isn't yet). The full paper will land at ~12–15 pages once the stubs are expanded.

## Files

| File | Purpose |
|---|---|
| `architecture-of-intent.md` | The paper draft (Markdown source with Pandoc citation syntax) |
| `references.bib` | BibTeX bibliography (~30 entries across 9 domains) |
| `figures/archetype-decision-tree.svg` | Figure 1 — referenced in §3.2 |
| `figures/four-dimensions-orthogonality.svg` | Figure 2 — referenced in §3.3 |
| `README.md` | This file |

## Figures

Two figures, both inline SVGs that convert cleanly to LaTeX `\includegraphics{...}`:

- **Figure 1 (`figures/archetype-decision-tree.svg`)** — the four-question decision tree for selecting one of the five archetypes, with the risk-override note. Adapted from the book chapter `src/architecture/04-decision-tree.md`.
- **Figure 2 (`figures/four-dimensions-orthogonality.svg`)** — Agency × Autonomy plotted against each other with example deployments in each quadrant, supporting the orthogonality argument in §3.3. The other two dimensions (Responsibility, Reversibility) are similarly orthogonal; we omit additional 2D plots for brevity.

If the paper goes to a workshop or journal that prefers TikZ, both figures can be re-rendered natively in LaTeX from the same logical content; SVG is the working format until then.

## Citations and bibliography

The Markdown source uses Pandoc-style `[@key]` inline citations. The bibliography lives in `references.bib`. Pandoc with `--citeproc --bibliography references.bib` resolves all citations and renders the bibliography in place at compile time.

**Citation style:** numeric (arXiv default for the first version). For workshop or journal submission we will normalize to the venue's required style by changing the `--csl` flag.

**Bibliography contents** (~30 entries across 9 domains):
- Spec-Driven Development (3)
- Driving automation (1)
- Agent governance and design (8)
- Multi-agent failure analysis (3)
- Indirect injection and safety (2)
- Inference economics and long context (2)
- Pattern languages and software architecture (4)
- Systems thinking and human error (2)
- Coding agents and benchmarks (3)
- Compliance and standards (3)
- Observability (1)

## Target

- **Format:** position / framework paper
- **Length:** ~12–15 pages (5,000–7,000 words)
- **Venue:** arXiv first (cs.SE / cs.AI cross-listing). Workshop or journal submission decided after the arXiv version is out.

## Honest contribution accounting

The paper claims novelty for three things:

1. **Cat 7 (Perceptual Failure)** — a new failure category for perceiving-then-acting agents that prior taxonomies (MAST, hallucination surveys, OWASP LLM Top 10) do not cover.
2. **Autonomy-vs-agency operationalization** — extending Shavit & Agarwal (2023) by treating autonomy and agency as orthogonal axes with explicit mapping to spec design.
3. **The synthesis itself** — five archetypes, four dimensions, fix-locus taxonomy, and SDD as a coherent framework with consistent vocabulary.

The paper explicitly does *not* claim novelty for: SDD as a discipline (lineage from GitHub spec-kit and Microsoft DevSquad Copilot); archetypes as a concept (lineage from Anthropic's *Building Effective Agents*); the four dimensions individually (lineage from SAE J3016 and Shavit & Agarwal); or Cat 1–6 as categories (synthesis from common practice).

This honest accounting belongs in the introduction and the discussion. Reviewers reward it; overclaiming gets punished disproportionately.

## How to convert to LaTeX (for arXiv submission)

The Markdown source uses constructs that map cleanly:

- Sections (`#`, `##`, `###`) → `\section`, `\subsection`, `\subsubsection`
- Tables → LaTeX `tabular`
- Bold and italic → `\textbf`, `\emph`
- Inline citations `[@key]` → `\cite{key}`
- Figures `![caption](path)` → `\includegraphics{path}` with `\caption{...}`

Pandoc handles the conversion in one shot:

```bash
pandoc architecture-of-intent.md \
  --from markdown \
  --to latex \
  --citeproc \
  --bibliography references.bib \
  --output architecture-of-intent.tex
```

Or to PDF directly (useful for review iteration):

```bash
pandoc architecture-of-intent.md \
  --citeproc \
  --bibliography references.bib \
  --output architecture-of-intent.pdf
```

Manual cleanup typically needed before arXiv: arXiv-specific preamble, abstract formatting (some templates require explicit `\begin{abstract}`), figure placement options (`[h!]`, `[t]`), and any venue-specific style sheet (`--csl acm-sig-proceedings.csl` etc.).

## Next steps

1. Review the skeleton for shape (does §3 cover the framework completely; does §4 instantiate it convincingly; is the contribution accounting honest enough).
2. Expand stubs to prose, section by section. Order recommended: §3 (the framework, conceptual core) → §1 (introduction, frames the framework) → §2 (prior work, situates it) → §4 (worked application) → §5 (discussion) → §6 (limitations) → §7 (conclusion) → §0 (abstract, last).
3. ~~Add figures.~~ Done — Figure 1 (decision tree) and Figure 2 (orthogonality) are in `figures/`.
4. ~~Compile reference list to BibTeX with consistent keys.~~ Done — see `references.bib`.
5. First arXiv submission once §3 + §1 + §2 are publication-quality.

## Relation to the book

The book is the practitioner's field guide; the paper is the academic distillation. The book covers ~80,000 words of practice-oriented material; the paper distills the conceptual contributions to ~6,000 words for citation and academic uptake. Appendix A in the paper maps each paper section back to the relevant book chapter so readers can read the paper as a summary and the book as the reference.
