# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [2026.05]

This release accompanies the EMSE minor revision. It addresses Reviewer 1's stylistic feedback and strengthens construct-validity guidance, drawing on Cao et al.'s decade-scale survey of 572 code benchmarks and Bean et al.'s parallel review of 445 ML/NLP benchmarks.

### Added

- **G5:** Construct-validity recommendations: SHOULD define the phenomenon, justify the sampling strategy (citing Baltes & Ralph 2022), isolate confounders, conduct an error analysis, document benchmark adaptations, and adopt contamination-prevention mechanisms for new benchmarks; pointer to HOW2BENCH and Bean et al.'s checklists.
- **G5:** For ratings that vary across raters or runs (human raters, LLM-as-judge), authors SHOULD report rating distributions per item rather than only point estimates.
- **G7:** For value-laden or culturally contingent constructs, authors SHOULD describe rater demographics beyond expertise.
- **G4:** Second example showing runtime trajectories (Bouzenia & Pradel, ASE 2025).

### Changed

- **RFC 2119 keywords:** Lowercase in body text (paper plain, website bold); the Table 3 distinction is unchanged.
- **Matrix:** Column headers replaced S1–S7 with short names (Annotator, Judge, Synthesis, Subject, Usage, Tools, Benchmarks).
- **Summary boxes:** *tl;dr* renamed to *Summary*; macro renamed `\tldr` → `\summary`.
- **Example(s) headings:** renamed *Examples* throughout (singular *Example* where a single example is given).
- **See Also blocks:** new format `Section X (Title): rationale`, where each rationale explains why the linked guideline is relevant from the source guideline's vantage point. A generic `\seesection{label}` macro pulls section titles via `\nameref*` so future renames propagate automatically.
- **Checklist:** empty `\square` bullets dropped; `\iconM` / `\iconS` symbols now serve as bullet markers.
- **G5 Challenges:** New evidence on benchmark-quality gaps from Cao et al.'s survey (84.2% ignore test-suite coverage; 64.0% are single-pass; 82.5% do not address contamination), with cross-domain confirmation from Bean et al.
- **Tables:** Reporting checklist gains six new G5 items and one new G7 item; rationale-recommendations table extends G5 and G7 rows. Matrix severities unchanged.
- **Bibliography:** proper nouns and acronyms in titles wrapped in `{}` to preserve capitalization through the bibstyle.

## [2026.04]

This release incorporates feedback from the community session at ICSE 2026 in Rio de Janeiro.

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
