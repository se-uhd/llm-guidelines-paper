# Changelog

All notable changes to the LLM Guidelines for SE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Calendar Versioning](https://calver.org/) (`YYYY.MM`).

## [2026.04]

### Added

- **Scope:** Defined *paper* as the manuscript PDF including any bound appendices, and *supplementary material* as anything external to it. Added a default rule that, when a guideline does not specify a reporting location, either is acceptable.
- **G3:** New recommendation that authors SHOULD release the implementation source code.

### Changed

- **G3 / G4:** Restructured the two guidelines along a static/dynamic split. G3 now covers static artifacts (files, schemas, skill and tool definitions), while G4 covers dynamic runtime traces.
- **G3:** Demoted several items from MUST to SHOULD after an internal discussion about the reporting burden.
- **G3 / G4:** Clarified phrasing and added concrete examples throughout, covering architectural diagrams, tool granularity, context files, agent-to-agent communication, plan storage, non-determinism sources, and hosting environments.
- **Tables:** Reconciled the matrix, checklist, and rationale-recommendations table with the current guideline bodies.
- **Citations:** Standardized the convention for citing gray literature.

## [2026.03]

First explicitly versioned release, corresponding to the EMSE major revision submission (2026-03-19).
