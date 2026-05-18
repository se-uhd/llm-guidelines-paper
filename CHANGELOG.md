# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [Ahead of last paper release]

### Added

- **Declare Usage:** For studies that assign multiple distinct LLM roles, **should** declare each role separately. DevBench (Golnari et al.) cited as illustration, with generator, evaluation subjects, and judge each disclosed.
- **Benchmarks:** Synthesizing benchmark instances added as a third contamination-mitigation strategy alongside post-cutoff collection and private benchmarks. DevBench listed under *Benchmark Examples*.
- **Open LLM:** DevBench cited as an example that combines three open-weight models with commercial frontier models under an MIT-licensed release.
- **Scope:** New *Related Reporting Guidelines* paragraph cites CONSORT (template for our checklist), TRIPOD-LLM (Gallifant et al.), Navarro et al.'s HCI guidelines (CHI 2026), Kapoor et al.'s REFORMS (Science Advances 2024), and Korn et al.'s FORGE 2026 prompt reporting guideline; positions Korn et al. as complementing our recommendations and names two substantive points where the HCI guidelines diverge (selective prompt reporting; modest technical evaluation). Gallifant, Sallou, and the prior position paper move into this paragraph from the SE-target paragraph.
- **Motivation:** Shift-left paragraph added (Liu et al. 2024): with LLMs, reporting must cover upstream artifacts (prompts, context) in addition to the code and data that traditional open science practice releases.

## [2026.05]

EMSE minor revision: addresses Reviewer 1's stylistic feedback, strengthens construct validity drawing on Cao et al.'s 572-benchmark survey and Bean et al.'s 445-benchmark review, and incorporates further input from discussions during ICSE 2026 (April 2026) and the 3rd Copenhagen Symposium on Human-Centered Software Engineering AI (May 2026).

### Added

- **Reporting Checklist:** Bracketed conditional tags (`[fine-tuning]`, `[agents]`, `[restricted-sharing]`, etc.) prefix items that apply only to studies with that feature.
- **Benchmarks:** **should** define the phenomenon, justify the sampling strategy, isolate confounders, conduct an error analysis, document benchmark adaptations, and adopt contamination-prevention mechanisms for new benchmarks. Pointer to HOW2BENCH and Bean et al.'s checklists.
- **Benchmarks:** For ratings that vary across raters or runs, **should** report distributions per item rather than only point estimates.
- **Human Validation:** For value-laden or culturally contingent constructs, **should** describe rater demographics beyond expertise.
- **Human Validation:** *See Also* subsection added (was missing).
- **Limitations and Mitigations:** *Examples*, *Benefits*, and *Challenges* subsections added (were missing). *Examples* cites Sallou et al.'s threat-and-mitigation catalog and Du et al.'s ClassEval threat-mitigation pairings.
- **Traces:** Second example showing runtime trajectories (Bouzenia & Pradel, ASE 2025).
- **Traces:** **should** record runtime traces in an OTLP-compatible format such as the OpenTelemetry GenAI semantic conventions or OpenInference, and report the version used.
- **Declare Usage:** Cheng et al. (2025) cited supporting disclosure placement in the methods section rather than acknowledgments.

### Changed

- **must** / **should** keywords lowercased in body text.
- **S1–S7 / G1–G8 IDs dropped throughout.** Tables 1 and 2 use Section / Title / Short Name; applicability matrix and rationale-recommendations table moved to the appendix.
- **Prose:** Removed em-dashes, AI-style filler verbs (utilize, leverage, facilitate), and non-statistical uses of *significant*.
- **Summary boxes:** *tl;dr* renamed to *Summary*; *Examples* used as the plural heading.
- **See Also blocks:** `Section n (Title): rationale` format.
- **Checklist bullets:** `\iconM` / `\iconS` replace empty `\square`.
- **Benchmarks Challenges:** new evidence from Cao et al. (84.2% ignore test-suite coverage, 64.0% single-pass, 82.5% no contamination handling), confirmed by Bean et al.
- **Bibliography:** seven arXiv preprints replaced with peer-reviewed citations; entries normalized to DBLP keys; proper nouns and acronyms wrapped in `{}` to preserve capitalization.
- **Reporting Checklist:** Items now ordered general-before-conditional within each severity. The sampling-strategy bullet split into a general "describe and justify the sampling strategy" item plus a conditional non-probability follow-up. The open-LLM-baseline item moved to *Model Selection and Configuration* because its trigger is a model-choice condition.
- **Limitations and Mitigations:** Threat-list and mitigation bullets unified across all six categories. Cross-model transfer, tool-architecture, and over-reliance bullets refactored from vague "and capabilities" / "API or capabilities" / "intended construct" to concrete dimensions (post-training procedures, vendor-specific features, the capability the benchmark tests). Construct validity gained behavioral equivalence as a second SE-specific aspect. Infrastructure dependence absorbed vendor quotas, throttling, and pricing changes as reproducibility threats.
- **Benchmarks:** *Recommendations* MUSTs lifted into prose; bullet list now SHOULDs only.
- **Model Version:** Two summary lists condensed into one prose summary.
- **Tools / Human Validation:** HULA (Takerngsaksiri et al., ICSE-SEIP 2025) repositioned from a definitional citation cluster to an industrial example.
- **ClassEval citation:** upgraded from arXiv preprint to the ICSE 2024 entry.
- **Open LLM:** Severity split for formal benchmarking studies (**must** include an open LLM; rationale added that scores are otherwise unverifiable) and controlled experiments (**should** include, unless required capabilities are specific to a commercial model).

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
