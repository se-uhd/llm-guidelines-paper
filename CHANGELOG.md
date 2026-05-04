# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [2026.05]

EMSE minor revision: Reviewer 1's stylistic feedback plus construct-validity strengthening drawing on Cao et al.'s 572-benchmark survey and Bean et al.'s 445-benchmark review.

### Added

- **Benchmarks:** SHOULD define the phenomenon, justify the sampling strategy, isolate confounders, conduct an error analysis, document benchmark adaptations, and adopt contamination-prevention mechanisms for new benchmarks. Pointer to HOW2BENCH and Bean et al.'s checklists.
- **Benchmarks:** For ratings that vary across raters or runs, SHOULD report distributions per item rather than only point estimates.
- **Human Validation:** For value-laden or culturally contingent constructs, SHOULD describe rater demographics beyond expertise.
- **Traces:** Second example showing runtime trajectories (Bouzenia & Pradel, ASE 2025).

### Changed

- **RFC 2119 keywords:** lowercase in body text (paper plain, website bold).
- **S1–S7 / G1–G8 IDs dropped throughout.** Tables 1 and 2 use Section / Title / Short Name; matrix moved after the rationale-recommendations table.
- **Summary boxes:** *tl;dr* renamed to *Summary*; *Examples* used as the plural heading.
- **See Also blocks:** `Section n (Title): rationale` format.
- **Checklist bullets:** `\iconM` / `\iconS` replace empty `\square`.
- **Benchmarks Challenges:** new evidence from Cao et al. (84.2% ignore test-suite coverage, 64.0% single-pass, 82.5% no contamination handling), confirmed by Bean et al.
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
