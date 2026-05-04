# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [2026.05]

This release accompanies the EMSE minor revision. Two independent threads: Reviewer 1's stylistic feedback, and a construct-validity strengthening that emerged separately while preparing the revision (drawing on Cao et al.'s decade-scale survey of 572 code benchmarks and Bean et al.'s parallel review of 445 ML/NLP benchmarks).

### Added

- **Benchmarks:** Construct-validity recommendations: SHOULD define the phenomenon, justify the sampling strategy, isolate confounders, conduct an error analysis, document benchmark adaptations, and adopt contamination-prevention mechanisms for new benchmarks; pointer to HOW2BENCH and Bean et al.'s checklists.
- **Benchmarks:** For ratings that vary across raters or runs (human raters, LLM-as-judge), authors SHOULD report rating distributions per item rather than only point estimates.
- **Human Validation:** For value-laden or culturally contingent constructs, authors SHOULD describe rater demographics beyond expertise.
- **Traces:** Second example showing runtime trajectories (Bouzenia & Pradel, ASE 2025).

### Changed

- **RFC 2119 keywords:** Lowercase in body text (paper plain, website bold).
- **S1–S7 / G1–G8 IDs dropped throughout.** Tables 1 and 2 restructured to Section / Title / Short Name; subsection titles drop the `(Gx)` / `(Sx)` parenthetical; matrix and rationale-recommendations rows use short names.
- **Summary tables:** centered; matrix moved after the rationale-recommendations table so it no longer splits Section 5.1's summary box; `\toprule` dropped above the rotated matrix headers.
- **Summary boxes:** *tl;dr* renamed to *Summary* (macro `\tldr` → `\summary`); `Examples` plural throughout.
- **See Also blocks:** new `Section n (Title): rationale` format, written from the source guideline's perspective; new `\seesection` macro pulls titles via `\nameref*`.
- **Checklist bullets:** empty `\square` dropped; `\iconM` / `\iconS` now mark must/should items.
- **Benchmarks Challenges:** new benchmark-quality evidence from Cao et al. (84.2% ignore test-suite coverage; 64.0% single-pass; 82.5% do not address contamination), confirmed cross-domain by Bean et al.
- **Reporting tables:** six new Benchmarks items and one new Human Validation item in the checklist; rationale-recommendations extends Benchmarks and Human Validation rows. Matrix severities unchanged.
- **Bibliography:** title proper nouns and acronyms wrapped in `{}` to preserve capitalization.

## [2026.04]

This release incorporates feedback from the community session at ICSE 2026 in Rio de Janeiro and subsequent discussions among the authors.

### Added

- **Scope:** Defined *paper* (the manuscript PDF, including any bound appendices) and *supplementary material* (anything external). When a guideline does not specify a reporting location, either is acceptable.
- **G3:** Authors SHOULD open-source their implementation.
- **G4:** New *Runtime Traces* reporting concept covering tool calls and configured-artifact activations (skills, context files, sub-agents), alongside the existing interaction-logs reporting.

### Changed

- **Guidelines order:** *Use Suitable Baselines, Benchmarks, and Metrics* moved above *Use Human Validation for LLM Outputs*. Evaluation guidelines now flow benchmarks → open-LLM baseline → human validation. The promoted guideline is now G5; *Use Human Validation* is now G7; *Use an Open LLM as a Baseline* keeps G6. Section anchors and macro names are unchanged.
- **G3 / G4:** Split and renamed. G3 *Report System and Prompt Design* (was *Report Tool Architecture Beyond Models*) covers files, schemas, skill and tool definitions. G4 *Report Session Traces* (was *Report Prompts, their Development, and Interaction Logs*) covers runtime traces. Several G3 items moved from MUST to SHOULD; G3 subheadings were reordered, with two renamed to *Agentic Systems and Pipelines* and *RAG and Ensembles*.
- **G7 (Human Validation):** Rationale and Recommendations now pick up directly from G5: where no benchmark adequately operationalizes the target construct, validate against human judgment. The *LLMs for Tools* (S6) clause is now an explicit SHOULD.
- **G2:** Treating temperature 0 as a reproducibility guarantee is now SHOULD NOT. Prompts and interaction logs cross-reference G3 and G4 instead of being restated.
- **G1:** Added a contemporary example declaration alongside the existing Llama 2 quote.
- **Throughout:** Tightened prose and elevated several plain "should" / "should not" instances to SHOULD / SHOULD NOT.
- **Tables:** Applicability matrix, reporting checklist, and rationale-recommendations table reconciled with the current guideline bodies.
- **Citations:** Standardized the convention for citing gray literature.

## [2026.03]

First explicitly versioned release, corresponding to the EMSE major revision submission (2026-03-19).
