# Guidelines for Empirical Studies in SE involving LLMs

Source repository for the community guidelines on reporting empirical studies in software engineering that involve large language models. The guidelines are rendered as a living resource at [llm-guidelines.org](https://llm-guidelines.org) and published as an [Agent Skill](https://llm-guidelines.org/skill/).

This repo is authoritative for the content: the LaTeX sources under `_main/`, `_scope/`, `_studytypes/`, `_guidelines/`, `_tldr/`, and `_summary/`, plus `literature.bib` and `shared-header.tex`. The [website repo](https://github.com/se-uhd/llm-guidelines-website) references them directly through a git submodule.

## Citing

To cite the guidelines, cite the article in *Empirical Software Engineering*:

> Baltes, S., Angermeir, F., Arora, C., Muñoz Barón, M., Chen, C., Böhme, L., Calefato, F., Ernst, N., Falessi, D., Fitzgerald, B., Fucci, D., He, J., Treude, C., Kalinowski, M., Lambiase, S., Russo, D., Lungu, M., Martinez Montes, C., Prechelt, L., Ralph, P., van Tonder, R., & Wagner, S. (2026). Guidelines for Empirical Studies in Software Engineering involving Large Language Models. *Empirical Software Engineering*. https://doi.org/10.1007/s10664-026-10922-3

A preprint is on [arXiv](https://arxiv.org/abs/2508.15503). To reference a specific version of the guidelines rather than the article, cite the Zenodo record for that release (see below). GitHub's "Cite this repository" button reads `CITATION.cff`.

## Releases

Releases are `YYYY.MM` tags (CalVer). Each one is published as a new arXiv version and archived on Zenodo, which mints a DOI for the version and a concept DOI that always resolves to the latest. The full history is in [`CHANGELOG.md`](CHANGELOG.md); the website tracks `main`, so it can be ahead of the latest release.

Release metadata lives in two files. `CITATION.cff` is the source of truth and is edited by hand; `.zenodo.json` is generated from it plus `scripts/zenodo-overlay.json` and must not be edited directly:

```bash
python3 scripts/generate_zenodo_json.py          # regenerate
python3 scripts/generate_zenodo_json.py --check  # fail if stale
```

Both exist because Zenodo ignores `CITATION.cff` whenever `.zenodo.json` is present, while GitHub's citation widget reads only `CITATION.cff`.

## License

The guidelines content is licensed under [CC BY 4.0](LICENSE). The Springer journal template files `svjour3.cls`, `svglov3.clo`, and `spbasic.bst` are redistributed under their own terms and are not covered by it.

## Contributing

Open an issue or pull request against `main`. Apply the prose conventions in [`WRITING.md`](WRITING.md) to any text you write or edit, and validate that the LaTeX still compiles (`./compile_and_flatten.sh`) before pushing. See [`CLAUDE.md`](CLAUDE.md) for the repository layout and build details.
