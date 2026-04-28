# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [Unreleased]

## [2026.04] - 2026-04-28

### Added

- **Scope:** Location-default clause for Reporting Locations.
- **Scope:** Definitions for reporting-location terms.
- **G3:** \should clause to release implementation source code.
- **G3:** Hosting-environment examples for time-sensitive measurements.
- **G3:** AIware citation alongside the pinned 'context' terminology.
- **G4:** Plan-storage conventions note in Agentic Plans.
- **G4:** Probabilistic sampling listed among non-determinism sources.

### Changed

- **G3 / G4:** Restructured along a static/dynamic split. G3 now covers static artifacts (files, schemas, skill/tool definitions); G4 covers dynamic runtime traces.
- **G3:** Softened nine \must items to \should after reviewer feedback on reporting volume; subsequently re-elevated RAG retrieval and dynamic prompts back to \must.
- **G3:** Mirrored the softened severity in the TL;DR and checklist.
- **G3:** Refined the architecture paragraph from review feedback.
- **G3:** Applied a high-level/detail split to the Agent-Based paragraph.
- **G3:** Softened reviewer-advice phrasing on prompt-development reporting.
- **G3:** Softened the system-prompt version note from \must to \should.
- **G3:** Reworded the context-file evolution note; clarified that context-file reporting is a snapshot and edits are captured in traces.
- **G4:** Simplified phrasing on the two kinds of session trace.
- **G4:** Made agent-to-agent explicit in the tool-call trace; tightened the challenges sentence on agent-to-agent logging.
- **G4:** Rephrased the LangGraph reference in the plan-storage note.
- **Tables:** Reconciled matrix, checklist, and rationale-recommendations with the guideline bodies.
- **Citations:** Standardized the gray-literature citation convention.

### Fixed

- **G4:** Non-determinism phrasing on temperature = 0.

## [2026.03] - 2026-03-19

Initial public version, marking the EMSE revision submission. Eight guidelines (G1–G8), seven study types (S1–S7), scope, and reporting checklist.
