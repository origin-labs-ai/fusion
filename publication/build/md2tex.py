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


CODE_UNICODE = {
    "\u2014": "--",
    "\u2013": "-",
    "\u00d7": "x",
    "\u00b7": ".",
    "\u2192": "->",
    "\u2190": "<-",
    "\u2264": "<=",
    "\u2265": ">=",
    "\u00b1": "+/-",
    "\u00b0": "deg",
    "\u2026": "...",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u00a0": " ",
}


def code_clean(text: str) -> str:
    for k, v in CODE_UNICODE.items():
        text = text.replace(k, v)
    return "".join(ch if ord(ch) < 128 else "" for ch in text)


def clean_unicode(text: str) -> str:
    for k, v in UNICODE.items():
        text = text.replace(k, v)
    return "".join(ch if ord(ch) < 128 else "" for ch in text)


def esc(text: str) -> str:
    return "".join(SPECIAL.get(ch, ch) for ch in text)


def inline(text: str) -> str:
    """Escape text, then apply inline markup via two token pools."""
    utokens: list[str] = []
    ctokens: list[str] = []

    def uni(m: re.Match) -> str:
        utokens.append(UNICODE[m.group(0)])
        return f"@@U{len(utokens) - 1}@@"

    def code(m: re.Match) -> str:
        ctokens.append(r"\texttt{" + esc(code_clean(m.group(1))) + "}")
        return f"@@T{len(ctokens) - 1}@@"

    text = re.sub(r"`([^`]*)`", code, text)

    pattern = "[" + "".join(re.escape(k) for k in UNICODE) + "]"
    text = re.sub(pattern, uni, text)
    text = "".join(ch if ord(ch) < 128 else "" for ch in text)

    text = esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", text)

    def link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        if url.startswith("http"):
            return r"\href{" + url.replace("%", r"\%").replace("#", r"\#") + "}{" + label + "}"
        return label

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    for i, tok in enumerate(utokens):
        text = text.replace(f"@@U{i}@@", tok)
    for i, tok in enumerate(ctokens):
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
    weights = []
    for c in range(ncols):
        longest = max((len(r[c]) if c < len(r) else 0) for r in rows)
        weights.append(max(3.0, float(longest)) ** 0.65)
    total = sum(weights)
    spec = " ".join(
        r">{\raggedright\arraybackslash}p{\dimexpr %.4f\linewidth-2\tabcolsep\relax}"
        % (w / total)
        for w in weights)
    longest_cell = max((len(c) for r in rows for c in r), default=0)
    if longest_cell > 140:
        size = "tiny"
    elif longest_cell > 80:
        size = "scriptsize"
    else:
        size = "footnotesize"

    def row(cells: list[str]) -> str:
        cells = cells + [""] * (ncols - len(cells))
        return " & ".join(inline(c) for c in cells) + r" \\"

    out = [r"\begingroup\%s" % size,
           r"\begin{tabular}{" + spec + "}",
           r"\toprule",
           row(header),
           r"\midrule"]
    for r in body:
        out.append(row(r))
    out += [r"\bottomrule", r"\end{tabular}", r"\endgroup"]
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
            out.append(r"\vspace{3pt}")
            out.append(r"\begin{Verbatim}[fontsize=\footnotesize,frame=single,rulecolor=\color{rule}]")
            out.extend(code_clean(c) for c in code)
            out.append(r"\end{Verbatim}")
            out.append(r"\vspace{3pt}")
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
        # ordinary prose: merge hard-wrapped physical lines back into sentences
        para = [line.strip()]
        i += 1
        while i < n and not re.search(r"[.!?:;]`?$", para[-1]):
            nxt = md_lines[i].rstrip()
            if (not nxt.strip() or nxt.lstrip().startswith(("```", "|", ">", "#"))
                    or re.match(r"^\s*[-*]\s+", nxt)
                    or re.match(r"^\s*\d+\.\s+", nxt)):
                break
            para.append(nxt.strip())
            i += 1
        out.append(inline(" ".join(para)) + r"\par")
    return "\n".join(out)
