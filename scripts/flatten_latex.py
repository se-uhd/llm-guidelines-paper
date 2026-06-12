#!/usr/bin/env python3
r"""Generate a self-contained TeX file by recursively inlining inputs.

Usage:
  python3 scripts/flatten_latex.py
  python3 scripts/flatten_latex.py <main.tex> <output.tex>

Problem:
  The submission needs a single TeX file, but the generated PDF from that flat
  source must match the PDF from the normal multi-file source. Naive textual
  ``\input`` expansion can change whitespace around include boundaries.

  pdfTeX does not only care about the visible characters in the manuscript. It
  tokenizes input streams, line endings, comments, and spaces at file boundaries.
  If an included file is pasted directly into the caller, the token stream at an
  ``\input`` edge can change: a newline may become a space, a space may
  disappear, or an extra blank line may turn into a paragraph break.
  Those tiny boundary changes are enough to alter line breaking and extracted
  PDF text. That is the failure this script prevents; it is not a manuscript
  rewrite and should not be fixed with hardcoded content substitutions.

What this does:
  The generated file recursively replaces project-local ``\input`` commands
  with the referenced file bodies. It does not use ``filecontents*`` or any
  temporary generated TeX files: compiling the flat source should only create
  normal LaTeX auxiliary files.

  The important detail is whitespace at the replacement site. If an ``\input``
  occupies a line by itself and the inlined file already ends with a newline,
  the original ``\input`` line ending must become a space token without becoming
  an empty source line. The script writes ``\space%`` at that input boundary:
  ``\space`` preserves the token seen after returning from ``\input``, and ``%``
  prevents an extra blank line in the flat file. If source text follows the
  ``\input`` on the same line, that tail is kept after the inlined body; this
  preserves inline cases such as ``\input{...}\end{framed}`` without adding a
  blank line.

Generator contract:
  * Inline only files under the paper repository root.
  * Leave comments untouched so commented-out ``\input`` text stays inert.
  * Fail instead of guessing when an input cannot be resolved safely.
  * Remove stale LaTeX auxiliary files for the selected flat output.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


INPUT_RE = re.compile(r"""\\input\s*(?:\{([^}]+)\}|([^\s%{}]+))""", re.VERBOSE)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAIN = PROJECT_ROOT / "emse26-llm-guidelines.tex"
DEFAULT_OUTPUT = PROJECT_ROOT / "emse26-llm-guidelines-flat.tex"
LATEX_AUXILIARY_SUFFIXES = (
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".lof",
    ".log",
    ".lot",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
)

def split_comment(line: str) -> tuple[str, str]:
    r"""Split one TeX source line into code and comment parts.

    Only unescaped ``%`` starts a comment. This keeps ``\input`` mentioned in a
    comment from being treated as a real include.
    """
    for index, char in enumerate(line):
        if char != "%":
            continue

        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1

        if backslashes % 2 == 0:
            return line[:index], line[index:]

    return line, ""


def trim_trailing_horizontal_whitespace(text: str) -> str:
    """Keep generated output stable without touching line structure."""
    return "".join(line.rstrip(" \t") for line in text.splitlines(keepends=True))


def cleanup_latex_auxiliary_files(output: Path) -> None:
    """Delete stale LaTeX auxiliary files for the generated flat TeX.

    Running ``latexmk`` on a flat output creates ignored auxiliary files next
    to it, such as ``.aux``, ``.log``, and ``.out``. Before rewriting that
    output, remove only standard LaTeX auxiliary files with the same stem.
    Source ``.tex`` files and PDFs are left alone.
    """
    output = output.resolve()
    output_dir = output.parent
    output_stem = output.stem

    for path in output_dir.iterdir():
        if not path.is_file():
            continue
        if not any(path.name.endswith(suffix) for suffix in LATEX_AUXILIARY_SUFFIXES):
            continue

        stem = path.name
        for suffix in LATEX_AUXILIARY_SUFFIXES:
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break

        if stem == output_stem:
            path.unlink()


class Flattener:
    r"""Recursively replaces project-local ``\input`` commands with file bodies."""

    def __init__(self, main: Path) -> None:
        self.main = main.resolve()
        self.root = self.main.parent
        self.active_stack: list[Path] = []

    def flatten(self) -> str:
        """Return the self-contained TeX source for ``self.main``."""
        return self.inline_file(self.main)

    def resolve_input(self, target: str, base_dir: Path) -> Path:
        r"""Resolve an ``\input`` target the way this project is compiled.

        TeX in this repository is invoked from the project root, so root-relative
        include paths are tried first. The including file's directory is kept as
        a fallback for conventional relative includes. Inputs outside the paper
        repository are rejected so the flat file remains self-contained and
        predictable.
        """
        candidates = [
            self.root / target,
            base_dir / target,
            self.root / f"{target}.tex",
            base_dir / f"{target}.tex",
        ]

        for candidate in candidates:
            if candidate.exists():
                path = candidate.resolve()
                try:
                    path.relative_to(self.root)
                except ValueError as error:
                    raise ValueError(f"refusing to flatten input outside project root: {path}") from error
                return path

        raise FileNotFoundError(f"cannot resolve input {target!r} from {base_dir}")

    def inline_file(self, path: Path) -> str:
        """Read ``path`` and inline any nested project-local inputs."""
        path = path.resolve()
        if path in self.active_stack:
            cycle = " -> ".join(
                p.relative_to(self.root).as_posix()
                for p in [*self.active_stack, path]
            )
            raise ValueError(f"recursive \\input cycle detected: {cycle}")

        self.active_stack.append(path)
        try:
            return self.rewrite_inputs(path.read_text(encoding="utf-8"), path.parent)
        finally:
            self.active_stack.pop()

    def rewrite_inputs(self, text: str, base_dir: Path) -> str:
        r"""Inline real ``\input`` commands while leaving comments untouched."""
        rewritten_lines: list[str] = []
        for line in text.splitlines(keepends=True):
            if line.endswith("\r\n"):
                body, eol = line[:-2], "\r\n"
            elif line.endswith(("\n", "\r")):
                body, eol = line[:-1], line[-1]
            else:
                body, eol = line, ""

            code, comment = split_comment(body)
            matches = list(INPUT_RE.finditer(code))
            if not matches:
                rewritten_lines.append(line)
                continue

            rewritten = []
            cursor = 0
            line_ending = eol

            for match in matches:
                target = match.group(1) or match.group(2)
                path = self.resolve_input(target, base_dir)
                inlined = self.inline_file(path)
                rewritten.append(code[cursor:match.start()])
                rewritten.append(inlined)
                cursor = match.end()

                tail = code[cursor:]
                if inlined.endswith(("\n", "\r")) and not tail.strip() and not comment:
                    line_ending = rf"\space%{eol}"

            rewritten.append(code[cursor:])
            rewritten.append(comment)
            rewritten.append(line_ending)
            rewritten_lines.append("".join(rewritten))
        return "".join(rewritten_lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a self-contained TeX file that preserves TeX input boundaries."
    )
    parser.add_argument(
        "main",
        nargs="?",
        type=Path,
        default=DEFAULT_MAIN,
        help=f"main TeX file (default: {DEFAULT_MAIN})",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output flat TeX file (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    cleanup_latex_auxiliary_files(args.output)
    args.output.write_text(
        trim_trailing_horizontal_whitespace(Flattener(args.main).flatten()),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
