# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic paper submitted to Empirical Software Engineering (EMSE) journal, currently under major revision. The paper presents guidelines for empirical studies in software engineering involving LLMs. It is co-authored by 22 researchers and synced with Overleaf via git.

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
./scripts/create_diff.sh [path/to/old/version]
```

PDF outputs (`emse25-llm-guidelines.pdf`, `title-page.pdf`) are gitignored. `response-letter.pdf` is tracked by git.

## Document Structure

### Main Paper

The main entry point is `emse25-llm-guidelines.tex`, which defines the preamble (packages, custom commands) and includes content via `\input{}`:

- `_main/01_abstract.tex` — Abstract
- `_main/02_document.tex` — Core document structure (Introduction, Methodology, all section includes)
- `_scope/` — Motivation (`01_motivation.tex`) and scope definition (`02_scope.tex`)
- `_studytypes/` — Taxonomy of 7 LLM study types, organized hierarchically (e.g., `01-02-llms-as-judges.tex`). Category 01 = LLMs as tools for researchers, Category 02 = LLMs as tools for engineers
- `_guidelines/` — 8 reporting guidelines (numbered `01` through `08`)
- `_tldr/` — TL;DR summaries of guidelines and study types (one per guideline, included inline before each guideline section)
- `_summary/` — Applicability matrix (`matrix.tex`), rationale-recommendations table (`rationale-recommendations.tex`), and reporting checklist (`checklist.tex`)
- `literature.bib` — Bibliography (~171 entries, sorted alphabetically by citation key)
- `svjour3.cls`, `svglov3.clo`, `spbasic.bst` — Springer journal template and bibliography style (do not modify)

### Revision Artifacts

- `response-letter.tex` — Point-by-point response to reviewers (standalone document, uses `literature.bib`). Structured with custom `reviewcomment`/`response` environments, one `\review` section per reviewer. Build with `latexmk -pdf response-letter.tex`.
- `emse-reviews.md` — Raw reviewer comments in markdown (reference copy for context)
- `title-page.tex` — Standalone title page with author list (separate from main paper, uses KOMA-Script `scrbook` class)
- `scripts/create_diff.sh` — Shell script that flattens old and new versions with `latexpand`, generates a `latexdiff` markup, and compiles `versions/diff.pdf`
- `versions/` — Contains original submission PDF (`EMSE-D-25-00637.pdf`) and diff output

## Key Conventions

**RFC 2119 terminology:** The paper uses custom commands for requirement levels — `\must`, `\mustnot`, `\should`, `\shouldnot`, `\may`. These render as small-caps. Note: `\may` is deprecated in the revision; reword as plain suggestions ("researchers may/can...") without small-caps.

**Cross-reference macros:** Each study type and guideline has a shorthand command (e.g., `\annotators`, `\judges`, `\humanvalidation`, `\prompts`) that creates a hyperlinked italic reference to the corresponding section. These are defined in the preamble of `emse25-llm-guidelines.tex`.

**File naming:** Content files use numeric prefixes for ordering (`01_`, `02_`, `01-02_`). Directories use underscore prefixes (`_guidelines/`, `_studytypes/`).

**Reporting location macros:** `\paper` and `\supplementarymaterial` indicate where information should be reported (renders as italic "paper" / "supplementary material").

**Framed environments:** The `framed` mdframed environment is used for highlighted guideline text blocks (gray background, left border).

## Bibliography Cleanup Scripts

All scripts live in the `scripts/` directory. Three Python scripts (requires `bibtexparser` package) were used to clean `literature.bib`. They are kept for reference and potential re-runs but are not part of the paper build.

- **`scripts/clean_bibliography.py`** — Initial cleanup: removes unreferenced entries (cross-checked against `.tex` and `.aux` files), then queries DBLP for each remaining entry to upgrade metadata (e.g., arXiv preprints promoted to published venue entries). Writes `literature.bib` in-place (backs up to `literature.bib.backup` first) and generates `dblp_unmatched_report.txt`.

- **`scripts/retry_dblp.py`** — Retries DBLP key-based lookups for entries that failed in the initial run (e.g., due to rate limiting or transient errors). Reads failed keys from `dblp_unmatched_report.txt`, re-fetches from DBLP, upgrades if better, and appends results to the report.

- **`scripts/handle_remaining.py`** — Handles entries that DBLP couldn't match (non-CS journals, gray literature, arXiv preprints). Step 1: enriches entries with DOIs via Crossref (adds publisher, ISSN, pages, normalizes DOI format). Step 2: fuzzy DBLP title search for CS/SE papers that exact-match missed. Step 3: validates URLs in `@misc` entries. Appends a categorized summary to `dblp_unmatched_report.txt`.

**Run order:** `scripts/clean_bibliography.py` → `scripts/retry_dblp.py` → `scripts/handle_remaining.py`

**Supporting files:**
- `literature.bib.backup` — Pre-cleanup backup of the bibliography (tracked by git)
- `dblp_unmatched_report.txt` — Cumulative log of all cleanup actions and remaining entry status (generated on demand, not tracked)
