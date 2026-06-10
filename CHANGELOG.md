# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [Ahead of last paper release]

## [2026.06]

Version accepted at Empirical Software Engineering (EMSE).

### Added

- **Limitations and Mitigations:** External Validity absorbed the former Generalizability list, gaining two new threats (configuration sensitivity, research-to-practice gap). Construct Validity gained five threats: construct under-specification, reliability without validity, capability confounding, prompt sensitivity, judge biases (position, verbosity, format).
- **Limitations and Mitigations:** Item-level cross-references added from each threat to the guideline carrying the relevant reporting requirement.
- **Benchmarks and Metrics:** AgentBench (Liu et al., ICLR 2024) added as an LLM-as-agent benchmark example with eight environments.
- **Human Validation:** Krippendorff threshold tiers (α<0.667 discard, 0.667≤α<0.8 tentative, α≥0.8 reliable) elevated from Examples to a **should** in Recommendations.
- **Guidelines introduction:** New paragraph explaining that **must** covers disclosure obligations and **should** covers methodological recommendations.
- **Declare Usage:** For studies that assign multiple distinct LLM roles, **should** declare each role separately. DevBench (Golnari et al.) cited as illustration, with generator, evaluation subjects, and judge each disclosed.
- **Benchmarks:** Synthesizing benchmark instances added as a third contamination-mitigation strategy alongside post-cutoff collection and private benchmarks. DevBench listed under *Benchmark Examples*.
- **Open LLM:** DevBench cited as an example that combines three open-weight models with commercial frontier models under an MIT-licensed release.
- **Scope:** New *Related Reporting Guidelines* paragraph cites CONSORT (template for our checklist), TRIPOD-LLM (Gallifant et al.), Navarro et al.'s HCI guidelines (CHI 2026), Kapoor et al.'s REFORMS (Science Advances 2024), and Korn et al.'s FORGE 2026 prompt reporting guideline; positions Korn et al. as complementing our recommendations and names two substantive points where the HCI guidelines diverge (selective prompt reporting; modest technical evaluation). Gallifant, Sallou, and the prior position paper move into this paragraph from the SE-target paragraph.
- **Motivation:** Shift-left paragraph added (Liu et al. 2024): with LLMs, reporting must cover upstream artifacts (prompts, context) in addition to the code and data that traditional open science practice releases.
- **Human Validation:** New *Replacing Human Judgment* paragraph: When LLMs replace humans, researchers **must** explain whether and how the replacement is justified.
- **Traces:** Mixture-of-Experts routing added to the list of non-determinism causes; citations split between Yuan et al. (batching, GPU floating-point) and Chann (MoE).
- **Benchmarks and Metrics:** Latency reporting added as a conditional **must** when study outcomes depend on response time (e.g., interactive user studies, latency comparisons). Tagged `[latency-sensitive]` in the reporting checklist.
- **Annotators:** Open and closed coding named explicitly in the *Description*.
- **Design:** **should** justify substantive architectural choices where alternatives existed (e.g., agentic framework, tool catalog).
- **Benchmarks and Metrics:** Dror et al. (2018) cited as a decision tree for selecting among inferential tests (Mann-Whitney U, McNemar, bootstrap), based on distributional assumptions and test-set size.
- **Open LLM:** OpenRouter named as an aggregator option alongside cloud services and self-hosting frameworks; open-source agentic tools (Continue, Cline, opencode) and vendor-hosted services (GitHub Copilot, Claude Code) contrasted on what they expose.
- **Study Types:** Each of the seven study-type subsections opens with a one-sentence framing of the role within its grouping (researcher tools / engineer tools).
- **Human Validation:** *Benefits* notes that disagreements between human reviewers and the LLM point to concrete improvements in the prompts, the context provided to the LLM, or the construct's operational definition.

### Changed

- **New Software Engineering Tools:** The GenAI-agent description now centers on a control loop around the model (observe, inspect, choose, act), with supporting building blocks (repository context, prompt and tool definitions, session memory, subagent delegation) drawn from Raschka's coding-agent decomposition and CoALA (Sumers et al.), replacing the earlier three-component framing.
- **Citations audited and grounded:** every cited claim was checked against its source and several miscitations corrected: mode collapse now cites Verbalized Sampling (Zhang et al.) and Kirk et al.; non-determinism under fixed settings cites Atil et al.; benchmark overconfidence cites Banerjee et al.; TnT-LLM and other unsupported citations removed.
- **Limitations and Mitigations:** Threat sections restructured. Mitigation strategies distributed from a single consolidated list into the corresponding threat sections as prose. Generalizability merged into External Validity, which now leads the threat sections. Internal Validity contamination mitigations now cross-reference Benchmarks and Metrics for concrete strategies (post-cutoff construction, held-out subsets, canary strings).
- **Session Traces:** Interaction-log and runtime-trace definitions tightened. Interaction logs cover the human-observable exchange at the LLM's interface (prompts in, responses out, including human-in-the-loop exchanges for agentic systems). Runtime traces cover the LLM's internal activity (tool calls and configured-artifact activations), naming the tool/artifact, arguments, and result per entry.
- **Session Traces:** Agentic plans **should** scoped to "any plans the system exposes" (e.g., Claude Code's editable Markdown plans), so the conditioning is on system exposure rather than a vague "if available".
- **Open LLM:** Replication-package recommendation narrowed to the open-LLM baseline specifically ("ensure the open-LLM baseline is independently reproducible from supplementary material"); broader full-replication-package guidance moved to Limitations and Mitigations as a Reliability & Reproducibility mitigation.
- **Human Validation:** *Subjective Judgment and Agreement* restructured so the opening sentence makes the LLM-vs-aggregated-human-reference comparison structure explicit. Established-reference-models recommendation moved up to follow the comparison setup. *Agentic Tools* paragraph reorganized to lead with the human-in-the-loop motivation; uses the paper-standard term "agentic systems" (with cross-ref to Design) instead of the outlier "agentic software development tools".
- **Scope:** *Related Reporting Guidelines* moved to the end of the scope section to avoid forward references to guideline shorthand macros.
- **Open LLM / Design / Benchmarks and Metrics:** Two methodology **must** requirements downgraded to **should**: the open-LLM-in-benchmarking carve-out and the inferential-statistics requirement when comparing models. *System and Prompt Design* now elevates the harness-description recommendation to **must** for benchmarking and adds a **should** that the harness support plugging in open models.
- **Design:** Few-shot example selection rationale required in the paper as a **must** (was a **should**); concrete examples remain in the supplementary material.
- **Model Version:** The **must** to report generation parameters now reads "parameters they configured" (active voice), making explicit that the requirement covers parameters the researcher actually set, not values they cannot see (e.g., temperature in a ChatGPT session). Defaults remain a **should**. "Experiments" replaced by "study execution" throughout the guideline, since not every LLM interaction is an experiment.
- **Design:** Topic-specific paragraphs reorganized. *Context Files* generalized to *Context Files and Agent Configuration*, with configuration mechanisms (context files, skills, subagents, hooks, settings, rules) introduced as an umbrella; configuration artifacts **must** be reported with the same level of detail as prompts. *Tool Catalog and Skill Definitions* renamed *Tool Catalog and MCP Servers* (skills are configuration artifacts). *RAG and Ensembles* folded into *Pipelines and Complex Systems*. *Agentic Systems* carved out as a separate paragraph; for agentic systems with external tools, **must** distinguish three kinds of activity (model reasoning, tool calls, interactions with users or the environment). The vague "explain design decisions and which retrieval mechanisms were implemented" **should** removed (retrieval is covered under the RAG sub-case).
- **Traces:** Open-format **should** softened. OpenTelemetry GenAI semantic conventions and OpenInference are preferred where they fit; tool-native formats (e.g., Claude Code transcripts, LangGraph state logs) are acceptable when researchers describe the file format and report the tool version.
- **Scope:** *Related Reporting Guidelines* tightened (~20% shorter): CONSORT year and "across communities" filler removed; HCI per-paper contrasts reorganized so the two "On X" comparisons read consecutively.
- **Methodology:** Chronology of ISERN 2024 → CHASEAI 2024 → WSESE 2025 made explicit (a preprint of the position paper was the basis for the CHASEAI discussions; paper published at WSESE 2025).
- **Model Version:** Summary item (4) for fine-tuned models names *approach* (full vs LoRA) and *hyperparameters* explicitly instead of generic "parameters and procedure".
- **Limitations and Mitigations:** *Environmental & Sustainability Constraints* caption flipped to a period with a one-sentence preamble, matching the structure of the other six validity-category captions.
- **Open LLM:** *Challenges* refactored from prose enumeration to an itemize with named captions (*Definitional inconsistency*, *Performance gap*, *Hardware demands*, *Operational complexity*).
- **Benchmarks and Metrics:** Metric definitions sharpened. BLEU-N specified as modified n-gram precision with a brevity penalty. CodeBLEU and CrystalBLEU distinguished by mechanism: AST and data-flow matching versus removal of corpus-common n-grams. pass@k clarified as a per-prompt estimator that draws k samples without replacement from n ≥ k generations, with the reported benchmark value the mean over prompts.
- **Editorial pass:** Tightened *Benefits* in Declare Usage, Design, Benchmarks and Metrics, and Human Validation (others reverted to original after review); split five 90+-word sentences in *Advantages and Challenges* into shorter units; applied the caption-punctuation rule (`\paragraph{Title.}` for captions followed by prose); standardized *human validation* across *See Also* lines; split filler semicolons and colons where both halves stand alone.
- **Declare Usage:** Aligned with the 2026 ACM Policy on Authorship, which requires research use of LLMs to be reported in the methods section and exempts writing-only assistance from disclosure. Advice for Reviewers now cites the policy's author-accountability and reject/retract provisions.
- **Benchmarks and Metrics:** Guideline short name expanded from *Benchmarks* to *Benchmarks & Metrics*, removing the label collision with the benchmarking study type's short name; the website page moved to /guidelines/benchmarks-metrics/ with a redirect from the old URL.
- **Open LLM:** In-prose cross-reference name now singular (*Open LLM*), matching the guideline title and all tables.
- **Study Types:** The benchmarking study type's short name expanded from *Benchmarks* to *Benchmarking*, completing the disambiguation from the Benchmarks & Metrics guideline; the website page moved to /study-types/benchmarking/ with a redirect from the old URL.

### Fixed

- **Reporting Checklist:** Items added for guideline requirements that had no checklist counterpart: reliability and construct validity discussion of benchmark and metric choices, few-shot example selection (new `[few-shot]` tag), prompt and trace anonymization, standalone-setup declaration, the three-activity distinction for tool-using agentic systems, benchmark version and modifications, data sources and collection dates for new benchmark releases, tool-native trace formats, representative prompt examples in the paper, and user feedback statistics for agentic tools. Hosting split into a general **should** and a conditional **must** for time-sensitive measurements.
- **Reporting Checklist:** Data-leakage item now mirrors the guideline's obligation to discuss leakage effects instead of an "avoid leaking" command; full-replication-package item replaced by Open LLM's baseline-reproducibility **should**; metric-justification item absorbs the **must not** on prior use as sole justification; reporting-location markers aligned with the guideline bodies.
- **Summary boxes:** Realigned with the guideline bodies: disclosure location is a **should**, hosting is conditional, "configuration mechanisms" replaces "context-file mechanisms", the open-LLM definition follows OSI, the replication-package sentence narrowed to the open-LLM baseline, and power analysis is optional ("may").
- **Open LLM:** The controlled-experiments **should** now names Studying LLM Usage as its study type, matching the scoping used in Design.
- **Benchmarks and Metrics:** The pass@k display formula no longer embeds "where:" inside the math, fixing the website rendering; study-type short names in Table 1 pluralized to match the applicability matrix.
- **Guideline captions:** Run-in captions now use a `\guidelineparagraph` macro that appends the period in the paper only, so website and skill headings no longer end with a stray period.

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

[Ahead of last paper release]: https://github.com/se-uhd/llm-guidelines-paper/compare/2026.06...main
[2026.06]: https://github.com/se-uhd/llm-guidelines-paper/releases/tag/2026.06
[2026.05]: https://github.com/se-uhd/llm-guidelines-paper/releases/tag/2026.05
[2026.04]: https://github.com/se-uhd/llm-guidelines-paper/releases/tag/2026.04
[2026.03]: https://github.com/se-uhd/llm-guidelines-paper/releases/tag/2026.03
