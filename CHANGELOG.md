# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [2026.04]

This release incorporates feedback from the community session at ICSE 2026 in Rio de Janeiro.

### Added

- **Scope:** Defined *paper* as the manuscript PDF including any bound appendices, and *supplementary material* as anything external to it. Added a default rule that, when a guideline does not specify a reporting location, either is acceptable.
- **G3:** New recommendation that authors SHOULD release the implementation source code.

### Changed

- **G3 / G4:** Restructured the two guidelines along a static/dynamic split, and renamed them accordingly. G3 is now *Report System and Prompt Design* (was *Report Tool Architecture Beyond Models*) and covers static artifacts (files, schemas, skill and tool definitions). G4 is now *Report Session Traces* (was *Report Prompts, their Development, and Interaction Logs*) and covers dynamic runtime traces.
- **G3:** Demoted several items from MUST to SHOULD after an internal discussion about the reporting burden.
- **G5:** Reworded the clause for *LLMs for Tools* (S6) to state the recommendation explicitly as a SHOULD.
- **G3 / G4:** Clarified phrasing and added concrete examples throughout, covering tool granularity, context files, agent-to-agent communication, plan storage, non-determinism sources, and hosting environments.
- **G3:** Reordered Recommendations subheadings (universal and common topics first, specialized cases last), renamed two subheadings to *Agentic Systems and Pipelines* and *RAG and Ensembles*, and tightened prose throughout.
- **G1:** Added a contemporary example declaration alongside the existing Llama 2 quote.
- **G4:** Merged Tool-Call Traces and Usage Traces into a single *Runtime Traces* concept covering both tool calls and configured-artifact activations, consolidated the privacy fallback and anonymization rule into the relevant paragraphs, and rewrote the Agentic Plans description for concreteness.
- **G7:** Removed editorial cruft (AI-edit comments and a commented-out paragraph), tightened slop phrasings ("play an important role", "it is important to fully understand", "of course"), elevated a lowercase "should" to RFC 2119 `\should`, and tightened the opening Challenges paragraph.
- **G5:** Tightened slop phrasings ("it is essential to", "The preferred method is to", "is essentially"), fixed a missing colon in the *Agentic Tools* subheading, rephrased a lowercase prose "should" to avoid the modal, and removed leftover commented-out content.
- **G8:** Fixed a missing colon in the *Mitigation Strategies* subheading, removed leftover AI-edit comments, tightened several slop phrasings ("it is important to", "make every effort", "faces analogous conditions", "tension field"), elevated a lowercase prose "should" to RFC 2119 `\should`, and flipped a passive-voice MUST to active.
- **G2:** Tightened slop phrasings ("always essential", "always report", "Our suggestion is to", "However, in fact", "Our guidelines additionally suggest to"), elevated "should not" to `\shouldnot` for the temperature-0 caveat, removed a commented-out leftover sentence, and replaced an "is essential" assertion with a cross-reference to G3 (prompts) and G4 (interaction logs).
- **Tables:** Reconciled the applicability matrix, reporting checklist, and rationale and recommendations table with the current guideline bodies.
- **Citations:** Standardized the convention for citing gray literature.

## [2026.03]

First explicitly versioned release, corresponding to the EMSE major revision submission (2026-03-19).
