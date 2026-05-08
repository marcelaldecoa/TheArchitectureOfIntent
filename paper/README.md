# The Architecture of Intent — paper

Companion arXiv paper to the book of the same title.

## Status

**Skeleton draft (v0.1).** The structure, abstract, section purposes, key claims, contribution accounting, and reference list are in place. Each section contains either prose (where it's already written) or a `*Stub paragraph*` block (where it isn't yet). The full paper will land at ~12–15 pages once the stubs are expanded.

## Files

| File | Purpose |
|---|---|
| `architecture-of-intent.md` | The paper draft (Markdown source) |
| `README.md` | This file |

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
- Inline citations (currently in author-year form) → `\cite{key}` against a BibTeX file

Pandoc can do most of the conversion automatically:

```bash
pandoc architecture-of-intent.md \
  --from markdown \
  --to latex \
  --output architecture-of-intent.tex \
  --bibliography references.bib  # once we have one
```

Manual cleanup needed: figures (none yet; planned for §3.2 archetype decision tree and §3.3 orthogonality argument); citation key normalization; abstract formatting; arXiv-specific preamble.

## Next steps

1. Review the skeleton for shape (does §3 cover the framework completely; does §4 instantiate it convincingly; is the contribution accounting honest enough).
2. Expand stubs to prose, section by section. Order recommended: §3 (the framework, conceptual core) → §1 (introduction, frames the framework) → §2 (prior work, situates it) → §4 (worked application) → §5 (discussion) → §6 (limitations) → §7 (conclusion) → §0 (abstract, last).
3. Add figures: archetype decision tree (already in the book at `src/architecture/04-decision-tree.md`) and an orthogonality diagram for the four dimensions.
4. Compile reference list to BibTeX with consistent keys.
5. First arXiv submission once §3 + §1 + §2 are publication-quality.

## Relation to the book

The book is the practitioner's field guide; the paper is the academic distillation. The book covers ~80,000 words of practice-oriented material; the paper distills the conceptual contributions to ~6,000 words for citation and academic uptake. Appendix A in the paper maps each paper section back to the relevant book chapter so readers can read the paper as a summary and the book as the reference.
