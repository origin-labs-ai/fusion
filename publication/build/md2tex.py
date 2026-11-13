#!/usr/bin/env python3
"""Minimal, deterministic Markdown -> LaTeX converter for the Fusion report.

The input is the subset the README generators emit: headings, prose, bullets,
pipe tables, fenced code and inline bold/code/links.  Nothing else is trusted.
"""
from __future__ import annotations

import re

SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}

UNICODE = {
    "\u2014": "---",
    "\u2013": "--",
    "\u00d7": r"\(\times\)",
    "\u00b7": r"\(\cdot\)",
    "\u2192": r"\(\rightarrow\)",
    "\u2190": r"\(\leftarrow\)",
    "\u2264": r"\(\leq\)",
    "\u2265": r"\(\geq\)",
    "\u00b1": r"\(\pm\)",
    "\u00b0": r"\(^{\circ}\)",
    "\u2026": r"\ldots{}",
    "\u2018": "`",
    "\u2019": "'",
    "\u201c": "``",
    "\u201d": "''",
    "\u00a0": "~",
}


def clean_unicode(text: str) -> str:
    for k, v in UNICODE.items():
        text = text.replace(k, v)
    return "".join(ch if ord(ch) < 128 else "" for ch in text)


def esc(text: str) -> str:
    text = clean_unicode(text)
    return "".join(SPECIAL.get(ch, ch) for ch in text)


def inline(text: str) -> str:
    """Escape text, then apply inline markup via token placeholders."""
    text = clean_unicode(text)
    tokens: list[str] = []

    def code(m: re.Match) -> str:
        tokens.append(r"\texttt{" + esc(m.group(1)) + "}")
        return f"@@T{len(tokens) - 1}@@"

    text = re.sub(r"`([^`]*)`", code, text)
    text = esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", text)

    def link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        if url.startswith("http"):
            return r"\href{" + url.replace("%", r"\%").replace("#", r"\#") + "}{" + label + "}"
        return label

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    for i, tok in enumerate(tokens):
        text = text.replace(f"@@T{i}@@", tok)
    return text


def table(lines: list[str]) -> list[str]:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) >= 2 and all(set(c) <= set("-: ") for c in rows[1]):
        header, body = rows[0], rows[2:]
    else:
        header, body = rows[0], rows[1:]
    ncols = max(len(r) for r in rows)
    header += [""] * (ncols - len(header))
    spec = " ".join([r">{\raggedright\arraybackslash}X"] * ncols)

    def row(cells: list[str]) -> str:
        cells = cells + [""] * (ncols - len(cells))
        return " & ".join(inline(c) for c in cells) + r" \\"

    out = [r"\begingroup\footnotesize",
           r"\begin{tabularx}{\linewidth}{" + spec + "}",
           r"\toprule",
           row(header),
           r"\midrule"]
    for r in body:
        out.append(row(r))
    out += [r"\bottomrule", r"\end{tabularx}", r"\endgroup"]
    return out


def convert(md_lines: list[str]) -> str:
    """Convert a block body (no leading heading) to LaTeX."""
    out: list[str] = []
    i = 0
    n = len(md_lines)
    while i < n:
        line = md_lines[i].rstrip()
        if not line.strip():
            out.append("")
            i += 1
            continue
        if line.lstrip().startswith("```"):
            fence = line.lstrip()[3:]
            i += 1
            code: list[str] = []
            while i < n and not md_lines[i].lstrip().startswith("```"):
                code.append(md_lines[i].rstrip())
                i += 1
            i += 1
            out.append(r"\begin{Verbatim}[breaklines=true,fontsize=\footnotesize,frame=single,rulecolor=\color{rule}]")
            out.extend(code)
            out.append(r"\end{Verbatim}")
            continue
        if line.lstrip().startswith("|"):
            block = []
            while i < n and md_lines[i].lstrip().startswith("|"):
                block.append(md_lines[i])
                i += 1
            out.extend(table(block))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            out.append(r"\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=2pt]")
            while i < n and re.match(r"^\s*[-*]\s+", md_lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", md_lines[i])
                out.append(r"\item " + inline(item))
                i += 1
            out.append(r"\end{itemize}")
            continue
        if line.lstrip().startswith(">"):
            out.append(r"\begin{quote}\small " + inline(line.lstrip()[1:].strip()) + r"\end{quote}")
            i += 1
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            out.append(r"\begin{enumerate}[leftmargin=1.4em,itemsep=1pt,topsep=2pt]")
            while i < n and re.match(r"^\s*\d+\.\s+", md_lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", md_lines[i])
                out.append(r"\item " + inline(item))
                i += 1
            out.append(r"\end{enumerate}")
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            cmd = {1: "section*", 2: "subsection*", 3: "subsubsection*"}.get(level, "paragraph*")
            out.append("\\" + cmd + "{" + inline(text) + "}")
            i += 1
            continue
        # ordinary paragraph line: keep lines separate, ragged right
        out.append(inline(line) + r"\par")
        i += 1
    return "\n".join(out)
