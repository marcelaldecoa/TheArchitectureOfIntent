# CLAUDE.md — context for working in this repo

This file is the handoff between Claude Code sessions. Keep it current.

## What this repo is

Two artifacts in one repo, both about *The Architecture of Intent*:

| Artifact | Path | Format | Purpose |
|---|---|---|---|
| **Book** | `src/` | mdBook (Markdown → HTML) | A practitioner field guide. ~80,000 words. Deploys to GitHub Pages on push to `main`. |
| **Paper** | `paper/` | Pandoc (Markdown → LaTeX → PDF) | The arXiv distillation. ~15,000 words / 34 pages. Position-and-framework paper. |

The paper is the **academic distillation** of the book. They share vocabulary and citations.

## Title and framing

- **Title:** *The Architecture of Intent*
- **Subtitle (book):** *A Field Guide to Designing and Shipping AI Agent Systems*
- **Subtitle (paper):** *A Framework for Designing Delegated Systems*

The framework's central claim: *intent is a primary design surface for any delegated system; AI agents are the most-acute current instance.*

Four load-bearing elements:
1. **Five archetypes** — Advisor, Executor, Guardian, Synthesizer, Orchestrator
2. **Four orthogonal calibration dimensions** — Agency, Autonomy, Responsibility, Reversibility
3. **Seven-category fix-locus failure taxonomy** — Cat 1 (Spec) through Cat 7 (Perceptual Failure)
4. **Spec-Driven Development** as the executable protocol layer

## Honest contribution accounting

The paper claims novelty for **three things only**:
- Cat 7 (Perceptual Failure) — new failure category for perceiving-then-acting agents
- Autonomy-vs-agency *operationalization* (orthogonality argument extending Shavit & Agarwal 2023)
- The *fix-locus* framing of the failure taxonomy

The paper does **not** claim novelty for: SDD (lineage from spec-kit and DevSquad), archetypes-as-concept (Anthropic *Building Effective Agents*), the four dimensions individually (SAE J3016, Shavit & Agarwal), or Cat 1–6.

When making future changes, preserve this accounting. Reviewers reward honest framing; overclaiming gets punished disproportionately.

---

## Repo structure (what to expect where)

```
.
├── CLAUDE.md                          ← you are here
├── README.md                          ← public-facing book overview
├── book.toml                          ← mdBook config
├── src/                               ← the BOOK
│   ├── SUMMARY.md                     ← table of contents (mdBook reads this)
│   ├── introduction.md, prologue.md, how-to-read.md
│   ├── theory/                        ← intent vs implementation, calibration, failure modes
│   ├── architecture/                  ← archetypes, decision tree, dimensions, multi-agent
│   ├── sdd/                           ← spec-driven development
│   ├── agents/                        ← agent classes, MCP, oversight
│   ├── patterns/                      ← ~50 pattern one-pagers (capability/integration/coordination/safety/observability/testing/state/deployment)
│   ├── repertoires/                   ← spec templates, code standards
│   ├── operating/                     ← governance, metrics, evals, red-team, cost, telemetry, adoption, DevSquad mapping, co-adoption
│   ├── examples/                      ← three worked pilots (customer support, code-gen pipeline, coding agent)
│   └── appendices/                    ← glossary, pattern index, references, archetype card, model-tier card, MCP reference
├── paper/                             ← the PAPER
│   ├── architecture-of-intent.md      ← Pandoc Markdown source
│   ├── architecture-of-intent.pdf     ← compiled artifact (committed for convenience)
│   ├── references.bib                 ← BibTeX (~30 entries)
│   ├── figures/
│   │   ├── archetype-decision-tree.svg + .png   ← Figure 1
│   │   └── four-dimensions-orthogonality.svg + .png  ← Figure 2
│   └── README.md                      ← compile instructions
├── scripts/                           ← helper scripts (link/orphan checkers)
├── theme/                             ← mdBook custom CSS/JS
└── .github/workflows/                 ← deploy.yml publishes book to GitHub Pages on push to main
```

## Build & verification commands

### Compile the paper to PDF

```bash
pandoc paper/architecture-of-intent.md \
  --citeproc \
  --bibliography paper/references.bib \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  --output paper/architecture-of-intent.pdf
```

Required tooling: `pandoc`, `texlive-xetex`, `texlive-fonts-recommended`, `texlive-latex-recommended`. SVG figures are pre-rendered to PNG; `librsvg2-bin` is *not* required at compile time.

### Check internal links and orphans (book)

```bash
python3 scripts/check-internal-links.py
python3 scripts/check-orphans.py
```

Both are fast and run before every commit that touches the book or SUMMARY.

### Build the book locally

```bash
mdbook build           # output to ./book/
mdbook serve --open    # live reload at localhost:3000
```

GitHub Actions auto-publishes on push to `main` via `.github/workflows/deploy.yml`.

---

## Conventions that matter

### Branch naming
`claude/<short-descriptive-name>` — e.g., `claude/paper-section-3`, `claude/devsquad-second-pass`. One PR per pass.

### PR descriptions
Verbose by design. Honest accounting matters: what changed, what didn't change, what was deliberately left out, why. Reviewers read these as the change record.

### Citation style in paper
Pandoc `[@key]` inline citations. Bibliography in `paper/references.bib`. Pandoc + `--citeproc` resolves at compile time.

### Citation key convention
`<authorOrOrg><Topic><Year>` — e.g., `@anthropicMCP2024`, `@microsoftDevSquadCopilot2026`, `@cemriMAST2025`.

### "Structural fixes live in spec / manifest / CI / platform — never only in the prompt"
This is a *load-bearing discipline* for the framework. When a Cat 1 / Cat 3 hybrid (e.g., the deleted-tests example) recurs, the fix is structural: NOT-authorized clauses, tool-manifest scope, CI guard. Prompt-level patches don't compound.

---

## mdBook gotchas

### `SUMMARY.md` parser is strict
**Do not put italic paragraph text between a `##` sub-heading and its bullet list inside a numbered part.** mdBook reports the failure misleadingly as *"Suffix chapters cannot be followed by a list"* but the actual cause is the paragraph between heading and list. Italic descriptions go *only* under top-level `#` headings.

This caused PR #11 (deploy hotfix). The check-orphans script does *not* catch it; only `mdbook build` does. If `deploy.yml` fails, look here first.

### File numbering has gaps
Some directories have non-contiguous file numbers (e.g., `theory/02, 03, 05` — no 01, 04, 06; `agents/01-06, 08, 09` — no 07). The gaps correspond to chapters cut/merged earlier. Don't renumber; cross-references rely on stable paths.

### Figures use `.png` not `.svg` in the paper
The paper's Markdown references PNG files (pre-rendered from SVG via `rsvg-convert`). Reasoning: arXiv build environments may not have `librsvg2-bin`; PNG is portable. SVG sources kept as the editable form.

If you edit a figure SVG, regenerate the PNG:
```bash
rsvg-convert --format=png --width=1600 paper/figures/archetype-decision-tree.svg \
  --output=paper/figures/archetype-decision-tree.png
```

### `rsvg-convert` mismeasures Georgia bold
The ORCHESTRATOR label in Figure 1 originally clipped because rsvg-convert's font-width estimate diverged from the SVG author's pixel calculation. Fix was to wrap the label as ORCHESTRA-TOR on two lines. If you add long labels in serif bold to figures, test by rendering at multiple widths.

---

## DevSquad Copilot — terminology to use

DevSquad's own README is sometimes informal; the docs site is more precise. Always use docs-site terminology for paper claims. Verified facts:

- **Released:** 2026 (not 2024–2025)
- **8 phases (exact names):** *envisioning phase → Spec the next slice → Plan only what the current slice needs → Decompose that slice → Implement with TDD discipline → Learn in the open → Review in an independent context → Refine continuously*
- **12 named specialist agents + conductor = 13 total:** *init, envision, kickoff, specify, plan, decompose, implement, review, security, sprint, refine, extend*
- **5 first-party MCP servers:** GitHub, Azure DevOps, Azure, Microsoft Learn, Draw.io
- **3 impact tiers:** low (skip ceremony), medium (plan + comprehension checkpoint + automated review), high (mandatory ADR + explicit approval + full review)
- **Config paths:** `.github/copilot-instructions.md`, `.github/docs/coding-guidelines.md`, `.github/instructions/<role>.instructions.md`
- **Invocation:** `copilot --agent devsquad:devsquad`; `--yolo` flag for unattended mode
- **Other named concepts:** comprehension checkpoint, reasoning log, "loop over ladder", 20-skill catalog (semantic activation)

The book uses paraphrases like "TDD-first" in some chapter bodies; that's an internal vocabulary choice consistent through those chapters. Do not bulk-rewrite. The exact names live in `src/operating/12-devsquad-mapping.md` (phase table), `src/appendices/references.md` (citation), and `src/operating/13-co-adoption-with-devsquad.md` vocabulary translation table.

For paper claims about DevSquad, always use exact names — see `paper/architecture-of-intent.md` Appendix B for the canonical statement.

---

## GitHub & MCP gotchas

### MCP server may disconnect mid-session
If you can't open PRs via `mcp__github__create_pull_request`, the MCP server has dropped. Check with `ToolSearch query "select:mcp__github__create_pull_request"`. If returned `No matching deferred tools found`, the server is gone for the session. Two options:
- User restarts Claude session to reconnect
- User opens PRs manually via `https://github.com/marcelaldecoa/TheArchitectureOfIntent/pull/new/<branch>`

### Sandbox blocks remote branch deletion
`git push --delete <branch>` fails with HTTP 403 from this environment. Local branch deletion works. To clean up merged remote branches, use the GitHub UI: https://github.com/marcelaldecoa/TheArchitectureOfIntent/branches

### GitHub MCP scope
The MCP is restricted to `marcelaldecoa/thearchitectureofintent`. Calls to other repos will be denied.

### Repo name vs. brand name
The repo is `TheArchitectureOfIntent` (preserves the GitHub Pages URL). The book and paper title is *The Architecture of Intent*. Repo name not renamed because the Pages URL `marcelaldecoa.github.io/TheArchitectureOfIntent/` would break for any external links.

---

## Recent meaningful decisions

- **Title:** kept "The Architecture of Intent" after briefly trying "Intent Engineering" (PR #14 → #15 reverted). The original title is more memorable, paper-friendly, and citation-friendly. The subtitle is the practical-signal layer.
- **Position paper, not empirical:** the paper does not claim empirical validation at scale; §6 names this explicitly.
- **arXiv first, workshop later:** the paper is sized for arXiv (no length limit). For workshop submission, a length-cut pass is needed (~34 pages now; most workshops cap at 10–12). Compression strategy documented in earlier PR descriptions.
- **`--yolo`, comprehension checkpoint, config paths:** all *are* documented in DevSquad (just in the docs site, not the README). My earlier review dismissed several as unverified — that was wrong; PR #27 corrected. If you read these things in old session transcripts, the corrections are now in main.

---

## Open work / candidates for next sessions

### Paper
- **arXiv submission** (mechanical from current PDF). Action is on the human, not on Claude.
- **Length-cut version for workshop submission** (10–12 pages). Strategy: collapse §2's eight subsections into 4–5 thematic paragraphs; trim §3.3 (orthogonality argument) and §3.4 (Cat 7 sub-categories) where they ran longest.
- **HiL-Bench / Karpathy citations** — if the user has verifiable sources for the "judgment gap" empirical claim in §1.1–§1.2, swap the current "emerging 2026 evaluations" framing for proper citations.
- **Empirical validation** — future-work track. Surveying practitioner adoption across deployments for a "v2" empirical paper.

### Book
- **Multi-tenant fleet governance** — chapter the framework currently doesn't have; identified as a 2026 gap in the introduction's honest-scope section. Hard to write well without case studies.
- **Computer-use agent worked example** — the pattern index notes "no worked example yet" for computer-use. Cat 7 lands in concept but not in concrete pilot.
- **Pattern audit (item 9 from earlier review)** — already done in PR #13, finding was that the pattern library was sturdier than my own review claimed. Could be revisited if specific patterns surface as filler in practice.

### General
- **Bulk-delete merged remote branches** — sandbox can't do remote ref deletion; needs the GitHub UI.
- **Optional CI workflow** — currently `deploy.yml` runs `mdbook build` only on push to main, not on PRs. A PR-time mdBook build check would catch SUMMARY parse errors before merge.

---

## Session continuation playbook

When opening this repo in a new Claude session:

1. **Read this file first.** It's the registry.
2. **Check `git log --oneline -10`** to see recent merged PRs.
3. **Run the link/orphan checkers** before making any book changes:
   ```bash
   python3 scripts/check-internal-links.py && python3 scripts/check-orphans.py
   ```
4. **Branch as `claude/<descriptive-name>`** for any non-trivial change.
5. **One PR per pass.** Verbose PR descriptions; honest accounting.
6. **For paper changes:** verify the PDF still compiles cleanly (`pandoc` command above) before committing the .md so the committed PDF stays current.
7. **For DevSquad-related changes:** verify against the docs site, not just the README. Always.
