# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic paper submitted to Empirical Software Engineering (EMSE) journal, currently under major revision. The paper presents guidelines for empirical studies in software engineering involving LLMs. It is co-authored by 22 researchers and synced with Overleaf via git.

**This repo is authoritative** for all content tex files (`_guidelines/`, `_studytypes/`, `_scope/`, `_tldr/`), `literature.bib`, and `shared-header.tex`. The companion website (`../llm-guidelines-website/`) references all content directly via a git submodule at `llm-guidelines-paper/`.

## Build Commands

```bash
# Full build (compile + bibliography + recompile twice for references)
latexmk -pdf emse25-llm-guidelines.tex

# Single compilation pass
pdflatex emse25-llm-guidelines.tex

# Bibliography only
bibtex emse25-llm-guidelines

# Word count (must use -inc to count \input files)
texcount -inc emse25-llm-guidelines.tex

# Response letter build
latexmk -pdf response-letter.tex

# Generate diff PDF against old submission (requires latexpand, latexdiff)
./scripts/create-diff.sh [path/to/old/version]

# Flatten all \input files into a single .tex file
./scripts/flatten.sh
```

PDF outputs (`emse25-llm-guidelines.pdf`, `title-page.pdf`) are gitignored. `response-letter.pdf` is tracked by git. `emse25-llm-guidelines-flat.tex` is the pre-generated flattened version (for diff generation and submission).

## Document Structure

### Main Paper

The main entry point is `emse25-llm-guidelines.tex`. Its preamble loads paper-only packages, then inputs the shared header:

```
\documentclass[smallextended]{svjour3}
\newif\ifpaper\papertrue
% paper-only packages (lineno, manyfoot, tcolorbox, appendix, balance,
% algorithm, algorithmicx, subfig, stfloats, graphicx, xcolor, tikz, mdframed)
\input{shared-header.tex}
% paper-only lstset color overrides and settings
```

Content is included via `\input{}`:

- `_main/01_abstract.tex` — Abstract
- `_main/02_document.tex` — Core document structure (Introduction, Methodology, all section includes)
- `_main/guidelines-intro.tex` — Guidelines section introduction
- `_main/study-types-intro.tex` — Study types section introduction
- `_scope/` — Motivation (`01_motivation.tex`) and scope definition (`02_scope.tex`)
- `_studytypes/` — Taxonomy of 7 LLM study types, organized hierarchically (e.g., `01-02-llms-as-judges.tex`). Category 01 = LLMs as tools for researchers (S1–S4), Category 02 = LLMs as tools for engineers (S5–S7). Also includes `01-05-advantages-and-challenges.tex` (cross-cutting section)
- `_guidelines/` — 8 reporting guidelines (numbered `01` through `08`)
- `_tldr/` — TL;DR summaries (one per guideline, included inline before each guideline section)
- `_summary/` — Applicability matrix (`matrix.tex`), rationale-recommendations table (`rationale-recommendations.tex`), and reporting checklist (`checklist.tex`)
- `literature.bib` — Bibliography (sorted alphabetically by citation key)
- `svjour3.cls`, `svglov3.clo`, `spbasic.bst` — Springer journal template and bibliography style (do not modify)

### Shared Header Architecture

The LaTeX preamble is shared with the website via `shared-header.tex` (lives in this repo's root). It uses `\ifpaper...\else...\fi` conditionals for commands that differ between paper and website:

- RFC 2119 keywords (`\must`, `\should`, etc.) — paper: `\textsc`, website: `\textbf`
- Cross-references (`\scope`, `\annotators`, etc.) — paper: `\hyperref[sec:...]`, website: `\href{/url}`
- Section formatting (`\guidelinesubsubsection`, etc.) — different heading levels
- Icons (`\iconM`, `\iconS`) — paper: TikZ circles, website: Unicode
- Framed environment — paper: mdframed (gray bg, left border), website: quote

**Important:** Paper-only packages (`tikz`, `xcolor`, `mdframed`) must be loaded *before* `\input{shared-header.tex}` so that `\ifpaper` branches can use them.

### Revision Artifacts

- `response-letter.tex` — Point-by-point response to reviewers (standalone document, uses `literature.bib`). Structured with custom `reviewcomment`/`response` environments, one `\review` section per reviewer. Build with `latexmk -pdf response-letter.tex`.
- `emse-reviews.md` — Raw reviewer comments in markdown (reference copy for context)
- `title-page.tex` — Standalone title page with author list (separate from main paper, uses KOMA-Script `scrbook` class)
- `scripts/create-diff.sh` — Shell script that flattens old and new versions with `latexpand`, generates a `latexdiff` markup, and compiles `versions/diff.pdf`
- `scripts/flatten.sh` — Flattens all `\input` files into `emse25-llm-guidelines-flat.tex` via `latexpand`
- `versions/` — Contains original submission PDF (`EMSE-D-25-00637.pdf`) and diff output

## Key Conventions

**RFC 2119 terminology:** `\must`, `\mustnot`, `\should`, `\shouldnot` render as small-caps in the paper. `\may` has been removed; reword as plain suggestions ("researchers may/can...").

**Cross-reference macros:** Each study type and guideline has a shorthand command that creates a hyperlinked italic reference to the corresponding section. All accept an optional `[id]` argument for in-text identifiers. Defined in `shared-header.tex` with `\ifpaper` conditionals.
- Study types (S1–S7): `\annotators`, `\judges`, `\synthesis`, `\subjects`, `\llmusage`, `\newtools`, `\benchmarkingtasks`
- Guidelines (G1–G8): `\usagerole`, `\modelversion`, `\toolarchitecture`, `\prompts`, `\humanvalidation`, `\openllm`, `\benchmarksmetrics`, `\limitationsmitigations`
- Umbrella: `\scope`, `\studytypes`, `\guidelines`, `\llmsforresearcher`, `\llmsforengineers`

**Inline quotes:** `\enq{...}` renders typographically correct quotes with italics.

**TL;DR label:** `\tldr` renders the inline "tl;dr" label.

**File naming:** Content files use numeric prefixes for ordering (`01_`, `02_`, `01-02_`). Directories use underscore prefixes (`_guidelines/`, `_studytypes/`).

**Reporting location macros:** `\paper` and `\supplementarymaterial` indicate where information should be reported (renders as italic in the paper).

**Framed environments:** The `framed` mdframed environment is used for highlighted guideline text blocks (gray background, left border).

**Applicability matrix (`_summary/matrix.tex`):** Table 1 maps guidelines (G1–G8) to study types (S1–S7) using `\iconM` (must), `\iconS` (should), or `--` (not applicable). Cell values must match the RFC 2119 language in each guideline's "Study Types" subsection (the `\guidelinesubsubsection` in `_guidelines/0X_*.tex`). When editing guideline text that changes `\must`/`\should` for a study type, update the matrix to match.

**Reporting checklist (`_summary/checklist.tex`):** Items within each section are ordered by severity first, then by reporting location: `\iconM` before `\iconS`, and within each severity level: `\paper` → unspecified → `\supplementarymaterial`. Maintain this ordering when adding or reordering checklist items.

## Syncing Content to Website

The website references all content directly from this repo via a git submodule. After editing content files or `literature.bib`, update the submodule pointer in the website repo:

```bash
cd ../llm-guidelines-website
git submodule update --remote
./compile-latex.sh && ./convert-and-merge-sources.sh
```

## Bibliography Cleanup Scripts

All scripts live in the `scripts/` directory. Three Python scripts (requires `bibtexparser` package) were used to clean `literature.bib`. They are kept for reference and potential re-runs but are not part of the paper build.

- **`scripts/clean-bibliography.py`** — Initial cleanup: removes unreferenced entries (cross-checked against `.tex` and `.aux` files), then queries DBLP for each remaining entry to upgrade metadata (e.g., arXiv preprints promoted to published venue entries). Writes `literature.bib` in-place (backs up to `literature.bib.backup` first) and generates `dblp_unmatched_report.txt`.

- **`scripts/retry-dblp.py`** — Retries DBLP key-based lookups for entries that failed in the initial run (e.g., due to rate limiting or transient errors). Reads failed keys from `dblp_unmatched_report.txt`, re-fetches from DBLP, upgrades if better, and appends results to the report.

- **`scripts/handle-remaining.py`** — Handles entries that DBLP couldn't match (non-CS journals, gray literature, arXiv preprints). Step 1: enriches entries with DOIs via Crossref (adds publisher, ISSN, pages, normalizes DOI format). Step 2: fuzzy DBLP title search for CS/SE papers that exact-match missed. Step 3: validates URLs in `@misc` entries. Appends a categorized summary to `dblp_unmatched_report.txt`.

**Run order:** `scripts/clean-bibliography.py` → `scripts/retry-dblp.py` → `scripts/handle-remaining.py`

**Supporting files:**
- `literature.bib.backup` — Pre-cleanup backup of the bibliography (tracked by git)
- `dblp_unmatched_report.txt` — Cumulative log of all cleanup actions and remaining entry status (generated on demand, not tracked)
