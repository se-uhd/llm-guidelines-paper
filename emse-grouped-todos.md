# Major Todos

## Whole Paper / Global Structure
- [ ] **E-01 (Major)** - Make the manuscript more concise, cut repetition, and add summary tables of the guidelines for navigability. *(Global; emse-todos.md:3)*
  
### RFC/MUST terminology
- [ ] **E-02 (Major)** - Reconsider the RFC-style terminology because the paper is not a community standard. *(Global; emse-todos.md:5)*
- [ ] **R2-03 (Major)** - Eliminate the RFC MUST/SHOULD framing because EMSE is not a standards body. *(Global; emse-todos.md:167)*
- [ ] **R2-04 (Major)** - Avoid absolute “MUST” language; emphasize critical thinking over commands. *(Global; emse-todos.md:168)*
- [ ] **R3-09 (Major)** - Provide reviewer-facing guidance/checklists for interpreting RFC 2119 terms and partial compliance. *(Global; emse-todos.md:203)*

### Presentation and navigability
- [ ] **E-03 (Major)** - Avoid framing guidelines as “undisputable truths”; allow flexibility for constrained teams. *(Global; emse-todos.md:7)*
- [ ] **R1-04 (Major)** - Improve verifiability guidance so readers can independently confirm contributions. *(Global; emse-todos.md:17)*
- [ ] **R1-05 (Major)** - Codify recurring challenges/advantages once and reference them (preferably via tables) instead of repeating prose. *(Global; emse-todos.md:19)*
- [ ] **R1-06 (Major)** - Split recommendations into a hierarchical list and a separate rationale discussion for clarity. *(Global; emse-todos.md:19)*
- [ ] **R2-01 (Major)** - Trim the overall length; consider removing the heavy “study type” subsections in Sec. 5. *(Global; emse-todos.md:165)*
- [ ] **R2-05 (Major)** - Temper guidelines that are methodologically sound but impractical (e.g., long-term commercial-model retesting). *(Global; emse-todos.md:169)*
- [ ] **R2-06 (Major)** - Explain how example studies were selected to avoid cherry-picking or collaborator bias. *(Global; emse-todos.md:170)*
- [ ] **R3-01 (Major)** - Discuss trade-offs/conflicts between guidelines and how to prioritize them; consider a decision tree by study type. *(Global; emse-todos.md:181)*
- [ ] **R3-07 (Major)** - Clarify strategies when multiple guidelines must be combined (e.g., human validation plus open baselines) and the associated costs. *(Global; emse-todos.md:197)*
- [ ] **R3-08 (Major)** - Add a dependency diagram or checklist capturing relationships among guidelines (e.g., 5.2 feeding 5.3, 5.6 with 5.7). *(Global; emse-todos.md:199)*
- [ ] **R2-02 (Major)** - Provide a one-page overview table summarizing all guidelines near the beginning. *(Global; emse-todos.md:166)*

## Section 1 - Introduction (pp. 3-4)

## Section 2 - Scope & Terminology

## Section 3 - Methodology & Validity
- [ ] **E-04 (Major)** - Add methodological detail and rigor per reviewer requests (no new experiments needed). *(Section 3; emse-todos.md:9)*
- [ ] **R1-01 (Major)** - Strengthen Section 3 methods with systematic input from other disciplines. *(Section 3; emse-todos.md:15)*
- [ ] **R1-02 (Major)** - Include an appendix/model study showing the guidelines applied end-to-end for practicality. *(Section 3; emse-todos.md:15)*
- [ ] **R1-03 (Major)** - Add explicit threats-to-validity and explain their impact. *(Section 3; emse-todos.md:15)*

## Section 4 - Study Types & Use Cases (pp. 5-12)
- [ ] **R1-23 (Major)** - Discuss whether human judgment is an appropriate gold standard in Section 4.1. *(Section 4; emse-todos.md:59)*
- [ ] **R1-26 (Major)** - Separate “synthetic data generation” so “synthesis” is unambiguous (page 10 line 32). *(Section 4; emse-todos.md:68)*
- [ ] **R1-27 (Major)** - Reframe Section 4.1.3 examples to match other subsections (or justify the meta-level). *(Section 4; emse-todos.md:71)*

## Section 5 - General Guidelines Overview
- [ ] **R1-32 (Major)** - Add guidelines for reviewers of LLM papers, including replication package expectations. *(Section 5; emse-todos.md:86)*

## Section 5.2 - Model Versioning & Study-Type Summaries
- [ ] **R1-33 (Major)** - Expand on SaaS model reproducibility, discussing trustworthiness mechanisms (triangulation, audit trails, etc.). *(Section 5.2; emse-todos.md:89)*
- [ ] **R1-35 (Major)** - Summarize recommendations by study type in tabular form for Sec. 5.2.5 (and other §5.x subsections). *(Section 5.2; emse-todos.md:95)*

## Section 5.3 - Sharing Artifacts
- [ ] **R1-36 (Major)** - Require distribution of concrete source code alongside abstract models/architectures. *(Section 5.3; emse-todos.md:98)*

## Section 5.4 - Interaction Logs
- [ ] **R3-04 (Major)** - Address feasibility limits of Guideline 5.4 for large-scale studies (storage/privacy constraints on releasing logs). *(Section 5.4; emse-todos.md:193)*

## Section 5.5 - Human Validation
- [ ] **R1-40 (Major)** - Provide actionable recommendations despite low human-model/human-human agreement findings. *(Section 5.5; emse-todos.md:110)*
- [ ] **R3-03 (Major)** - Supply guidance on statistical power, sample sizes, repetition counts, comparison metrics, and contamination-aware evaluation for LLM experiments. *(Section 5.5; emse-todos.md:185 & 201)*

## Section 5.6 - Open Baselines & Infrastructure
- [ ] **R1-42 (Major)** - Clarify why including an open LLM baseline might be impossible when human subjects are involved. *(Section 5.6; emse-todos.md:116)*
- [ ] **R3-05 (Major)** - Justify including underperforming open baselines when proprietary models dominate, or define when they add little value. *(Section 5.6; emse-todos.md:194)*

## Section 5.7 - Benchmarks, Repetition & Model Identification
- [ ] **R1-47 (Major)** - Move background material out of Sec. 5.7.2 or supplement it with concrete examples. *(Section 5.7; emse-todos.md:131)*
- [ ] **R1-50 (Major)** - Provide a structured classification of benchmarks discussed in Sec. 5.7.2. *(Section 5.7; emse-todos.md:140)*
- [ ] **R1-51 (Major)** - Elevate the issue on page 40 line 18 and add concrete recommendations. *(Section 5.7; emse-todos.md:143)*

## Section 5.8 - Cost, Contamination & Environmental Impact
- [ ] **R1-55 (Major)** - Report costs by breaking down inputs/outputs and token pricing to aid reproducibility. *(Section 5.8; emse-todos.md:155)*
- [ ] **R3-02 (Major)** - Elevate data contamination/leakage into a standalone guideline with mitigation strategies. *(Section 5.8; emse-todos.md:183)*
- [ ] **R3-06 (Major)** - Explain how cost-reporting remains meaningful despite fluctuating cloud API prices. *(Section 5.8; emse-todos.md:195)*

## Cross-Guideline Conflicts & Dependencies
- [ ] **R3-07 (Major)** - Clarify strategies when guidelines need to be combined (e.g., validation plus open baselines) while controlling cost. *(Global; emse-todos.md:197)*
- [ ] **R3-08 (Major)** - Provide a dependency diagram/checklist showing logical flow among guidelines. *(Global; emse-todos.md:199)*
- [ ] **R3-09 (Major)** - Offer reviewer guidance on how to handle RFC 2119 terminology and partial compliance. *(Global; emse-todos.md:203)*

## Examples, Citations & Related Work
- [ ] **R2-06 (Major)** - Document how illustrative papers/examples were chosen to avoid bias. *(Global; emse-todos.md:170)*

# Minor Changes Checklist

### Whole Paper / Global Structure
- [ ] **R1-07** - Lead recommendation paragraphs (e.g., Sec. 5.8.1) with the action before the rationale.
- [ ] **R1-09** - Convert RFC verbs to lowercase so the tone stays non-standard.
- [ ] **R1-10** - Reduce or relocate distracting in-text cross-references.
- [ ] **R1-11** - Add navigational figures to summarize the guideline structure.

### Section 1 - Introduction
- [ ] **R1-12** - Provide LLM-specific motivating details/examples (p.3 l.16).
- [ ] **R1-13** - Cite ACM SIGSOFT Empirical Standards (p.3 l.29).
- [ ] **R1-14** - Highlight that LLMs need fresh methodological guidance (p.3 l.33).
- [ ] **R1-15** - Rephrase “recent version” to “recent version of this document” (p.4 l.7).
- [ ] **R1-16** - Remove stray “xw” (p.4 l.9).
- [ ] **R1-17** - Change “advise” to “advice” (p.4 l.38).

### Section 2 - Scope & Terminology
- [ ] **R1-18** - Clarify whether code artifacts are in scope alongside natural language.
- [ ] **R2-07** - Rename “Natural Language Use Cases” to “Textual Use Cases.”

### Section 4 - Study Types & Use Cases
- [ ] **R1-19** - Mention data generation at p.5 l.23 alongside other tasks.
- [ ] **R1-20** - Fix numbering near p.6 l.29.
- [ ] **R1-21** - Replace “inter-rater agreement” with “accuracy” at p.7 l.38.
- [ ] **R1-22** - Clarify the statement at p.8 l.16.
- [ ] **R1-24** - Merge overlapping advantages between §§ 4.1.1 and 4.1.2.
- [ ] **R1-25** - Explain why the p.10 l.11 issue matters.
- [ ] **R1-28** - Merge overlapping challenges across subsections.
- [ ] **R1-29** - Clarify the meaning of “should” at p.12 l.32.

### Section 5 - General Guidelines Overview
- [ ] **R1-30** - Note automation of human tasks as a key advantage (p.16 l.22).
- [ ] **R1-31** - Clarify the replicability point at p.16 l.44.

### Section 5.2 - Model Versioning & Study-Type Summaries
- [ ] **R1-34** - Elaborate on the pros/cons of forcing temperature 0 (Sec. 5.2.4).

### Section 5.4 - Interaction Logs
- [ ] **R1-37** - Remove AI-sounding filler (e.g., “crucial for accuracy”) around p.29 l.1.

### Section 5.5 - Human Validation
- [x] **R1-38** - Fix paraphrased quotes and define “first three categories” in §5.5.2.
- [ ] **R1-39** - Clarify why p.32 l.25 is relevant to human validation.
- [x] **R1-41** - Explain the connection between “struggle with adapting to AI-assisted work” and §5.5.4.

### Section 5.6 - Open Baselines & Infrastructure
- [x] **R1-43** - Reword “managed cloud APIs provided by proprietary vendors” for clarity.
- [ ] **R1-44** - Add a comparison table for proprietary vs. open-weight vs. full-open models.
- [x] **R1-45** - Use static analysis as the example at p.37 l.15.

### Section 5.7 - Benchmarks, Repetition & Model Identification
- [ ] **R1-46** - Specify which benchmarks are referenced at p.37 l.4.
- [ ] **R1-48** - Typeset the equation at p.38 l.37 as a display equation.
- [ ] **R1-49** - Align tasks at p.38 l.49 with the earlier problem types.
- [ ] **R1-52** - Clarify whether GPT‑4o identification issues extend to same-fingerprint models (p.42 l.7).
- [ ] **R1-53** - Begin the p.42 l.35 paragraph with a thematic sentence.
- [ ] **R1-54** - Separate generalizability and code duplication discussion at p.44 l.26.

### Section 5.8 - Cost, Contamination & Environmental Impact
- [ ] **R1-56** - Justify or reconsider environmental impact assessments for research contexts.

### Examples, Citations & Related Work
- [ ] **R3-10** - Tie cross-domain examples back to SE-specific challenges.
- [ ] **R3-11** - Evaluate and cite the suggested arXiv references where appropriate.
