# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic paper submitted to Empirical Software Engineering (EMSE) journal, currently under minor revision (Reviewer 1, round 2). The paper presents guidelines for empirical studies in software engineering involving LLMs. It is co-authored by 22 researchers and synced with Overleaf via git.

**This repo is authoritative** for all content tex files (`_guidelines/`, `_studytypes/`, `_scope/`, `_tldr/`), `literature.bib`, and `shared-header.tex`. The companion website (`../llm-guidelines-website/`) references all content directly via a git submodule at `llm-guidelines-paper/`.

**Writing rules:** Apply the prose conventions in `WRITING.md` (banned/restricted words, em-dash budget, citation grounding, statistical formatting, etc.) to any prose you write or edit, whether in LaTeX, Markdown, code comments, or commit messages.

## Build Commands

```bash
# Full build (compile + bibliography + recompile twice for references)
latexmk -pdf emse26-llm-guidelines.tex

# Single compilation pass
pdflatex emse26-llm-guidelines.tex

# Bibliography only
bibtex emse26-llm-guidelines

# Word count (must use -inc to count \input files)
texcount -inc emse26-llm-guidelines.tex

# Response letter build (R2)
latexmk -pdf reviews-and-response/response-letter_r2.tex

# Compile and flatten into a single .tex file
./compile_and_flatten.sh

# Rebuild the full R2 resubmission bundle (flat tex, bib, main PDF, title page, response letter)
./versions/r2/regenerate.sh

# Generate diff PDF against old submission (requires latexpand, latexdiff)
./scripts/create_diff.sh [path/to/old/version]

# Flatten all \input files into a single .tex file (without compiling)
./scripts/flatten.sh
```

PDF outputs (`emse26-llm-guidelines.pdf`, `emse26-llm-guidelines-flat.pdf`) are gitignored. Response-letter PDFs and the R2 bundle artifacts under `versions/r2/` are tracked. `emse26-llm-guidelines-flat.tex` is the pre-generated flattened version (for diff generation and submission).

**Always run `./compile_and_flatten.sh` after content edits** before committing. The flat `.tex` is tracked, so it goes stale otherwise; the local PDF preview goes stale too. This applies to any change under `_main/`, `_scope/`, `_studytypes/`, `_guidelines/`, `_tldr/`, `_summary/`, `literature.bib`, or `shared-header.tex`. After running it, downstream rebuilds (website + skill bundle) need `./compile-latex.sh && ./convert-and-merge-sources.sh` from the `llm-guidelines-website/` repo.

**Before resubmitting R2, run `./versions/r2/regenerate.sh`.** It refreshes every R2 artifact from the current sources and aborts if the flat tex is stale, so an out-of-date PDF or bibliography cannot be uploaded by mistake.

## Document Structure

### Main Paper

The main entry point is `emse26-llm-guidelines.tex`. Its preamble loads paper-only packages, then inputs the shared header:

```
\documentclass[smallextended]{svjour3}
\newif\ifpaper\papertrue
% paper-only packages (manyfoot, tcolorbox, appendix, balance,
% algorithm, algorithmicx, subfig, stfloats, capt-of, graphicx,
% xcolor, tikz, mdframed)
% geometry override sets the page to ~Royal Octavo (178x254mm) so
% the preview matches Springer's printed trim
\input{shared-header.tex}
% paper-only lstset color overrides
% needspace + etoolbox \pretocmd to keep section headings off the
% bottom of pages
```

Content is included via `\input{}`:

- `_main/01_abstract.tex` — Abstract
- `_main/02_document.tex` — Core document structure (Introduction, Methodology, all section includes)
- `_main/guidelines-intro.tex` — Guidelines section introduction
- `_main/study-types-intro.tex` — Study types section introduction
- `_scope/` — Motivation (`01_motivation.tex`) and scope definition (`02_scope.tex`)
- `_studytypes/` — Taxonomy of 7 LLM study types, organized hierarchically (e.g., `01-02-llms-as-judges.tex`). Category 01 = LLMs as tools for researchers (annotators, judges, synthesis, subjects); Category 02 = LLMs as tools for engineers (LLM usage, new tools, benchmarking tasks). Also includes `01-05-advantages-and-challenges.tex` (cross-cutting section)
- `_guidelines/` — 8 reporting guidelines (numbered `01` through `08`)
- `_tldr/` — TL;DR summaries (one per guideline, included inline before each guideline section)
- `_summary/` — Applicability matrix (`matrix.tex`), rationale-recommendations table (`rationale-recommendations.tex`), and reporting checklist (`checklist.tex`)
- `literature.bib` — Bibliography (sorted alphabetically by citation key)
- `svjour3.cls`, `svglov3.clo`, `spbasic.bst` — Springer journal template and bibliography style (do not modify)

### Shared Header Architecture

The LaTeX preamble is shared with the website via `shared-header.tex` (lives in this repo's root). It uses `\ifpaper...\else...\fi` conditionals for commands that differ between paper and website:

- RFC 2119 keywords (`\must`, `\should`, etc.) — bold in both paper and website
- Cross-references (`\scope`, `\annotators`, etc.) — paper: `\hyperref[sec:...]`, website: `\href{/url}`
- Section formatting (`\guidelinesubsubsection`, etc.) — different heading levels
- Icons (`\iconM`, `\iconS`) — paper: TikZ circles, website: Unicode
- Framed environment — paper: mdframed (gray bg, left border); website: quote. Body is upright in both.

**Important:** Paper-only packages (`tikz`, `xcolor`, `mdframed`) must be loaded *before* `\input{shared-header.tex}` so that `\ifpaper` branches can use them.

### Revision Artifacts

- `reviews-and-response/response-letter_r1.tex` and `response-letter_r2.tex` — Point-by-point responses to reviewers (`response-letter_r1.tex` is the major-revision response; `response-letter_r2.tex` is the minor-revision R2 response). Each is a standalone document using `literature.bib`, with custom `reviewcomment`/`response` environments and one `\review` section per reviewer. Build via `versions/r2/regenerate.sh` (preferred) or directly with `latexmk -pdf reviews-and-response/response-letter_r2.tex`.
- `reviews-and-response/emse-reviews.md`, `emse-reviews_r1.md` — Raw reviewer comments in markdown for each round (reference copies for context)
- `versions/r2/title-page_r2.tex` — Standalone title page with author list (separate from main paper, uses KOMA-Script `scrbook` class). Lives inside the R2 bundle.
- `versions/r2/regenerate.sh` — Rebuilds the R2 resubmission bundle (`emse26-llm-guidelines-flat_r2.{tex,pdf}`, `literature_r2.bib`, `title-page_r2.pdf`) and `reviews-and-response/response-letter_r2.pdf` from current sources. Runs `compile_and_flatten.sh` first, then re-verifies via a fresh `latexpand` pass and aborts if the working-copy flat tex differs, so stale artifacts cannot enter the bundle. Does not touch `EMSE-D-25-00637_R2.pdf` (that PDF is downloaded from Editorial Manager).
- `scripts/create_diff.sh` — Shell script that flattens old and new versions with `latexpand`, generates a `latexdiff` markup, and compiles `versions/diff.pdf`
- `scripts/flatten.sh` — Flattens all `\input` files into `emse26-llm-guidelines-flat.tex` via `latexpand`
- `versions/` — Per-round bundles: `initial/` (original submission PDF), `r1/` (R1 diff and PDFs), `r2/` (R2 resubmission bundle with regenerate script)

## Key Conventions

**RFC 2119 terminology:** `\must`, `\mustnot`, `\should`, `\shouldnot` render bold in both paper and website (per Reviewer 1's stylistic ask: lowercase, not small-caps; this paper is not a standard). `\may` has been removed; reword as plain suggestions ("researchers may/can...").

**Cross-reference macros:** Each study type and guideline has a shorthand command that creates a hyperlinked italic reference to the corresponding section. All accept an optional `[id]` argument for in-text identifiers. Defined in `shared-header.tex` with `\ifpaper` conditionals.
- Study types: `\annotators`, `\judges`, `\synthesis`, `\subjects`, `\llmusage`, `\newtools`, `\benchmarkingtasks`
- Guidelines: `\usagerole`, `\modelversion`, `\design`, `\traces`, `\benchmarksmetrics`, `\openllm`, `\humanvalidation`, `\limitationsmitigations`
- Umbrella: `\scope`, `\studytypes`, `\guidelines`, `\llmsforresearcher`, `\llmsforengineers`

**Subsection / paragraph back-references in prose:** When mentioning a labeled subsection (`\guidelinesubsubsection`, `\scopeparagraph`) or a labeled paragraph (`\paragraph`, `\studytypeparagraph`) by its title, italicize the title with `\emph{}`. Examples: `see \emph{Challenges} below`, `in the \emph{Examples} subsection below`, `\emph{Replacing Human Judgment} applies particularly to ...`. Add the "subsection" or "paragraph" descriptor only when clarity needs it; the italics alone usually mark the title as a label. Use "above" / "below" as directional cues for nearby references. Section-level references continue to use the cross-reference macros above (`\scope`, `\guidelines`, etc.).

**Inline quotes:** `\enq{...}` renders typographically correct quotes with italics.

**Summary label:** `\summary` renders the inline "Summary" label that opens each guideline's framed summary box.

**See Also macros:** `\seesection{label}` (paper-side) renders `Section X: Full Title` with only the section number hyperlinked, pulling the title automatically via `\nameref*`. Per-guideline convenience macros (`\seeusagerole`, `\seemodelversion`, `\seedesign`, `\seetraces`, `\seebenchmarksmetrics`, `\seeopenllm`, `\seehumanvalidation`, `\seelimitationsmitigations`) take no arguments and target the corresponding guideline. Use these in `See Also` lists.

**File naming:** Content files use numeric prefixes for ordering (`01_`, `02_`, `01-02_`). Directories use underscore prefixes (`_guidelines/`, `_studytypes/`).

**Reporting location macros:** `\paper` and `\supplementarymaterial` indicate where information should be reported (renders as italic in both paper and website).

**Framed environments:** The `framed` mdframed environment is used for highlighted guideline text blocks (gray background, left border, upright body text). The website renders the same `framed` as a plain blockquote.

**Applicability matrix (`_summary/matrix.tex`):** Maps the eight guidelines to the seven study types using `\iconM` (must), `\iconS` (should), or `--` (not applicable). Cell values must match the RFC 2119 language in each guideline's "Study Types" subsection (the `\guidelinesubsubsection` in `_guidelines/0X_*.tex`). When editing guideline text that changes `\must`/`\should` for a study type, update the matrix to match.

**Reporting checklist (`_summary/checklist.tex`):** Items within each section are ordered by severity first, then by reporting location: `\iconM` before `\iconS`, and within each severity level: `\paper` → unspecified → `\supplementarymaterial`. Maintain this ordering when adding or reordering checklist items.

**Citation conventions for URLs and gray literature:** Pick one of three forms based on the URL's role in the prose, and use it consistently:

| URL role | Form |
|---|---|
| Backs a substantive claim or argument | `\cite{key}` to a `@misc` entry in `literature.bib` |
| Names a product, dataset, repository, or homepage in running prose | inline `\href{URL}{name}`; pair with `\cite{}` if a paper exists |
| Project's own site (`llm-guidelines.org`) | inline `\href{https://llm-guidelines.org}{llm-guidelines.org}` |
| Incidental utility URL not tied to a claim and not named in prose | `\footnote{\url{...}}` (rare, last-resort) |

`@misc` bib-entry rules:
- Web pages, blog posts, vendor docs: `howpublished = {\url{...}}` and `note = {Accessed YYYY-MM-DD}`
- arXiv preprints: `url = {...}`, `archiveprefix = {arXiv}`, `eprint = {...}`, `primaryclass = {...}`
- Sort fields alphabetically within an entry; sort entries alphabetically by citation key

## Syncing Content to Website

The website references all content directly from this repo via a git submodule. After editing content files or `literature.bib`, update the submodule pointer in the website repo:

```bash
cd ../llm-guidelines-website
git submodule update --remote
./compile-latex.sh && ./convert-and-merge-sources.sh
```

## Bibliography Cleanup Scripts

All scripts live in the `scripts/` directory (requires `bibtexparser`).

- **`scripts/clean_bibliography.py`** — Validates each entry against DBLP (and Crossref as fallback). For entries with an arXiv id (detected from `eprint`, DBLP CoRR key, `url`, `volume = abs/...`, or arXiv DOI), queries DBLP for all records of that work; if a non-CoRR record exists (conference, journal, workshop), the entry is upgraded and its citation key is renamed to the new DBLP key. For already-published entries that still carry leftover arXiv metadata (`eprint`, `archiveprefix`, `primaryclass`, `eprinttype`, redundant arXiv `url`), strips those fields. After bib changes, rewrites `\cite` sites in all source `.tex` files for renamed keys. A persistent JSON cache (`scripts/.bib_validation_cache.json`) records last-validation timestamp, content hash, and outcome per entry; subsequent runs skip cached entries that are fresh and unchanged. Removing unreferenced entries is opt-in via `--remove-unref` (default off, since stale `.aux` files can drop in-progress citations).

  CLI flags: `--force` (ignore cache), `--only KEY[,KEY...]`, `--max-age-days N` (default 30), `--remove-unref`, `--no-rename`, `--no-tex-update`, `--no-strip`, `--dry-run`, `--limit N`. The script writes `literature.bib` in place (backs up to `literature.bib.backup` first), updates `.tex` cite sites, refreshes the cache, and writes a per-run report at `dblp_unmatched_report.txt`. After a run that renames keys, regenerate `emse26-llm-guidelines-flat.tex` via `./scripts/flatten.sh`.

- **`scripts/retry_dblp.py`** — Retries DBLP key-based lookups for entries that failed in the initial run (e.g., 429s or transient errors). Reads failed keys from `dblp_unmatched_report.txt` and appends results. Largely superseded by `clean_bibliography.py`'s built-in retry, but kept for targeted reruns.

- **`scripts/handle_remaining.py`** — One-off handler for the entries that DBLP couldn't match during the initial cleanup (non-CS journals, gray literature, etc.). Crossref enrichment, fuzzy DBLP search, and `@misc` URL validation. Kept for historical reference; the categorized lists at the top of the file are frozen at the state of the original cleanup.

**Supporting files:**
- `literature.bib.backup` — Backup written before each `clean_bibliography.py` run (tracked by git).
- `dblp_unmatched_report.txt` — Per-run report with old → new key map, stripped fields, and unmatched entries (overwritten each run; not tracked).
- `scripts/.bib_validation_cache.json` — Persistent validation cache (not tracked).
