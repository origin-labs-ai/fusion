#!/usr/bin/env python3
"""Build the 512-page PDF report with pdfLaTeX."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

import corpus
import md2tex
from pubfacts import (N_FORMATS, N_RETIRED, N_TESTS, N_LIBS, N_TARGETS,
                      N_SEATS, N_DECISIONS, N_RESEARCH, N_CASES, N_ASSERTS,
                      TF_HEAD, CODE_HEAD, FUSION_HEAD)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "report"))
TEX = os.path.join(OUT, "Fusion-Report-512.tex")

PREAMBLE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{inconsolata}
\usepackage[margin=21mm,top=22mm,bottom=22mm,headheight=14pt]{geometry}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{ragged2e}
\usepackage{enumitem}
\usepackage{fancyvrb}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}

\definecolor{ink}{HTML}{0B1220}
\definecolor{ink2}{HTML}{101B2E}
\definecolor{ink3}{HTML}{16233A}
\definecolor{blue}{HTML}{2B7FFF}
\definecolor{cyan}{HTML}{22D3EE}
\definecolor{violet}{HTML}{8B5CF6}
\definecolor{amber}{HTML}{F59E0B}
\definecolor{pink}{HTML}{F472B6}
\definecolor{rule}{HTML}{24324D}
\definecolor{muted}{HTML}{64748B}
\definecolor{paper}{HTML}{F8FAFC}

\setlength{\parindent}{0pt}
\setlength{\parskip}{2.6pt}
\linespread{1.02}
\setlength{\emergencystretch}{2em}
\renewcommand{\arraystretch}{0.94}

\titleformat{\section}[block]
  {\Large\bfseries\color{ink}}{}{0pt}{}
  [\vspace{2pt}{\color{rule}\hrule height 0.6pt}]
\titlespacing*{\section}{0pt}{0pt}{7pt}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyfoot[L]{\footnotesize\color{muted}Fusion \textperiodcentered{} The Superproject Technical Report}
\fancyfoot[R]{\footnotesize\color{muted}\thepage}
\fancyfoot[C]{}

\newcommand{\chip}[3]{%
  \node[rounded corners=4pt, fill=#1, text=white, inner sep=7pt,
        font=\footnotesize\bfseries] at (#2) {#3};}

\begin{document}
\color{ink}
"""

COVER = r"""
\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[ink] (current page.south west) rectangle (current page.north east);
  \shade[top color=ink3, bottom color=ink, middle color=ink2]
    (current page.south west) rectangle (current page.north east);
  \foreach \i in {0,...,16} {
    \draw[white,opacity=0.025,line width=0.4pt]
      ([xshift=\i cm]current page.south west) -- ([xshift=\i cm]current page.north west);
    \draw[white,opacity=0.025,line width=0.4pt]
      ([yshift=\i cm]current page.south west) -- ([yshift=\i cm]current page.south east);
  }
  \begin{scope}[shift={([xshift=0mm,yshift=58mm]current page.center)}]
    \draw[cyan,opacity=0.30,line width=1.1pt] (0,0) circle (55mm);
    \draw[blue,opacity=0.22,line width=2pt] (0,0) circle (72mm);
    \draw[violet,opacity=0.30,line width=0.9pt,rotate=18] (0,0) ellipse (86mm and 44mm);
    \foreach \a in {0,45,...,315} {
      \fill[cyan,opacity=0.55] (\a:72mm) circle (1.35pt);
    }
    \begin{scope}[shift={(0,-6mm)}]
      \draw[cyan,line width=3.4pt,line join=round] (-34mm,14mm) -- (0,30mm) -- (34mm,14mm) -- (0,-2mm) -- cycle;
      \draw[violet,line width=3.4pt,line join=round,opacity=0.95] (-34mm,-6mm) -- (0,10mm) -- (34mm,-6mm) -- (0,-22mm) -- cycle;
      \draw[pink,line width=3.4pt,line join=round,opacity=0.95] (-34mm,-26mm) -- (0,-10mm) -- (34mm,-26mm) -- (0,-42mm) -- cycle;
      \fill[white] (0,-6mm) circle (2.1pt);
    \end{scope}
  \end{scope}

  \node[anchor=west, text=cyan, font=\fontsize{9}{11}\selectfont\bfseries]
    at ([xshift=22mm,yshift=122mm]current page.south west) {SUPERPROJECT TECHNICAL REPORT \quad \textperiodcentered \quad EDITION 2026.11};

  \node[anchor=west, text=white, font=\fontsize{66}{68}\selectfont\bfseries]
    at ([xshift=21mm,yshift=70mm]current page.south west) {Fusion};
  \node[anchor=west, text=white, opacity=0.92, font=\fontsize{17}{21}\selectfont]
    at ([xshift=22mm,yshift=55mm]current page.south west) {Quantization \textperiodcentered{} Training \textperiodcentered{} Inference \textperiodcentered{} Serving};
  \draw[cyan,line width=1.4pt] ([xshift=22mm,yshift=47mm]current page.south west) -- ([xshift=74mm,yshift=47mm]current page.south west);

  \node[anchor=north west, text=white, opacity=0.86, font=\fontsize{10.5}{14}\selectfont,
        text width=118mm, align=left]
    at ([xshift=22mm,yshift=40mm]current page.south west)
    {The C++20 engine and the Windows launcher, documented from the live tree.
     Every number, every format and every gate in this edition is generated,
     not remembered.};

  \node[anchor=west, rounded corners=4pt, fill=blue, text=white, inner sep=7pt,
        font=\footnotesize\bfseries] at ([xshift=22mm,yshift=20mm]current page.south west) {@@FORMATS@@ formats};
  \node[anchor=west, rounded corners=4pt, fill=violet, text=white, inner sep=7pt,
        font=\footnotesize\bfseries] at ([xshift=62mm,yshift=20mm]current page.south west) {@@TESTS@@ test files};
  \node[anchor=west, rounded corners=4pt, fill=amber, text=white, inner sep=7pt,
        font=\footnotesize\bfseries] at ([xshift=104mm,yshift=20mm]current page.south west) {@@SEATS@@ seats};
  \node[anchor=west, rounded corners=4pt, fill=pink, text=white, inner sep=7pt,
        font=\footnotesize\bfseries] at ([xshift=132mm,yshift=20mm]current page.south west) {512 pages};

  \node[anchor=west, text=white, opacity=0.60, font=\footnotesize]
    at ([xshift=22mm,yshift=10mm]current page.south west)
    {Generated \today \quad \textperiodcentered \quad PDF and DOCX \quad \textperiodcentered \quad pdfLaTeX};
\end{tikzpicture}
\clearpage
"""


def esc_title(text: str) -> str:
    return md2tex.inline(text)


def part_page(page: dict, n: int) -> str:
    num = page.get("part", "")
    title = page["title"]
    name = title.split("·", 1)[1].strip() if "·" in title else title
    subtitle = page.get("subtitle", "")
    line = (page.get("body") or [""])[0]
    return rf"""
\clearpage
\thispagestyle{{empty}}
\begin{{tikzpicture}}[remember picture,overlay]
  \fill[ink] (current page.south west) rectangle (current page.north east);
  \shade[top color=ink2, bottom color=ink] (current page.south west) rectangle (current page.north east);
  \node[anchor=north west, text=cyan, font=\fontsize{{10}}{{12}}\selectfont\bfseries]
    at ([xshift=22mm,yshift=-24mm]current page.north west) {{PART {num}}};
  \node[anchor=north west, text=white, opacity=0.10, font=\fontsize{{200}}{{200}}\selectfont\bfseries]
    at ([xshift=10mm,yshift=-46mm]current page.north west) {{{num}}};
  \draw[cyan,line width=1.4pt] ([xshift=22mm,yshift=-126mm]current page.north west) -- ([xshift=62mm,yshift=-126mm]current page.north west);
  \node[anchor=north west, text=white, font=\fontsize{{34}}{{38}}\selectfont\bfseries, text width=150mm, align=left]
    at ([xshift=22mm,yshift=-128mm]current page.north west) {{{esc_title(name)}}};
  \node[anchor=north west, text=white, opacity=0.80, font=\fontsize{{13}}{{17}}\selectfont, text width=146mm, align=left]
    at ([xshift=22mm,yshift=-150mm]current page.north west) {{{esc_title(subtitle)}}};
  \node[anchor=north west, text=cyan, opacity=0.90, font=\fontsize{{10.5}}{{14}}\selectfont, text width=140mm, align=left]
    at ([xshift=22mm,yshift=-174mm]current page.north west) {{{esc_title(line)}}};
  \node[anchor=south west, text=white, opacity=0.55, font=\footnotesize]
    at ([xshift=22mm,yshift=16mm]current page.south west) {{Fusion \textperiodcentered{{}} 512-page edition \textperiodcentered{{}} page {n}}};
\end{{tikzpicture}}
"""


def end_page(page: dict, n: int) -> str:
    body = page.get("body", [])
    lines = "\\\\\n".join(esc_title(x) for x in body)
    return rf"""
\clearpage
\thispagestyle{{empty}}
\begin{{tikzpicture}}[remember picture,overlay]
  \fill[ink] (current page.south west) rectangle (current page.north east);
  \draw[cyan,opacity=0.22,line width=1pt] (current page.center) circle (46mm);
  \draw[blue,opacity=0.16,line width=2pt] (current page.center) circle (62mm);
  \node[text=white, font=\fontsize{{30}}{{34}}\selectfont\bfseries, align=center]
    at ([yshift=10mm]current page.center) {{{lines}}};
  \node[text=cyan, opacity=0.85, font=\footnotesize]
    at ([yshift=-30mm]current page.center) {{Generated from the live tree \textperiodcentered{{}} superproject {FUSION_HEAD}}};
\end{{tikzpicture}}
"""


def normal_page(page: dict, n: int) -> str:
    title = esc_title(page["title"])
    body = md2tex.convert(page.get("body", []))
    size, lead = page.get("fit", (11.0, 15.4))
    return rf"""
\clearpage
\label{{blk:{n}}}
\section*{{{title}}}
\begingroup
\fontsize{{{size}}}{{{lead}}}\selectfont
{body}
\endgroup
"""


def build_tex(pages: list[dict]) -> str:
    cover = (COVER.replace("@@FORMATS@@", str(N_FORMATS))
                  .replace("@@TESTS@@", str(N_TESTS))
                  .replace("@@SEATS@@", str(N_SEATS)))
    out = [PREAMBLE, cover]
    for n, page in enumerate(pages, start=1):
        kind = page["kind"]
        if kind in {"cover"}:
            continue
        if kind == "part":
            out.append(part_page(page, n))
        elif kind == "end":
            out.append(end_page(page, n))
        else:
            out.append(normal_page(page, n))
    out.append(r"\end{document}")
    return "\n".join(out)


def run(cmd: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def page_count(pdf: str) -> int:
    r = run(["pdfinfo", pdf], os.path.dirname(pdf))
    if r.returncode != 0:
        raise SystemExit("pdfinfo failed:\n" + r.stderr)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    if not m:
        raise SystemExit("pdfinfo gave no page count:\n" + r.stdout)
    return int(m.group(1))


def label_pages(aux: str) -> dict[int, int]:
    pages = {}
    if not os.path.exists(aux):
        return pages
    for line in open(aux, encoding="utf-8", errors="replace"):
        if "newlabel{blk:" not in line:
            continue
        try:
            n = int(line.split("blk:", 1)[1].split("}", 1)[0])
            rest = line[line.index("}{{") + 3:]
            pages[n] = int(rest.split("}{", 2)[1])
        except (ValueError, IndexError):
            continue
    return pages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="build a prefix for testing")
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    pages = corpus.build()
    if args.limit:
        pages = pages[:args.limit]
    tex = build_tex(pages)
    open(TEX, "w", encoding="utf-8", newline="\n").write(tex)
    print(f"wrote {TEX} ({len(pages)} blocks, {len(tex):,} bytes)")

    for pass_no in (1, 2):
        r = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 os.path.basename(TEX)], OUT)
        if r.returncode != 0:
            tail = (r.stdout or "")[-4000:]
            print(tail)
            raise SystemExit(f"pdflatex pass {pass_no} failed")

    pdf = os.path.join(OUT, "Fusion-Report-512.pdf")
    got = page_count(pdf)
    print(f"pdf pages={got} expected={len(pages)}")
    if got != len(pages):
        labels = label_pages(os.path.join(OUT, "Fusion-Report-512.aux"))
        bad = [(n, labels.get(n)) for n in range(1, len(pages) + 1)
               if labels.get(n) not in (None, n)]
        print("blocks that did not start on their own page:", bad[:20])
        return 1
    print("OK: page count exact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
