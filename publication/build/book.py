#!/usr/bin/env python3
"""Assemble and typeset the continuous-flow Fusion report."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

import book_appendix
import book_extra
import book_front
import book_sources
import booktex
import pubfacts as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "report"))
TEX = os.path.join(OUT, "Fusion-Report-512.tex")


def preamble(size: float, lead: float, margin: float) -> str:
    return rf"""
\documentclass[10pt,a4paper]{{extarticle}}
\usepackage[a4paper,left={margin}mm,right={margin}mm,top=15mm,bottom=15mm,
  headheight=10pt,headsep=2.5mm,footskip=5.5mm,columnsep=5mm]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{unicode-math}}
\setmainfont{{TeX Gyre Termes}}
\setsansfont{{TeX Gyre Heros}}
\setmonofont{{DejaVu Sans Mono}}[Scale=0.76]
\setmathfont{{TeX Gyre Termes Math}}
\usepackage{{microtype}}
\usepackage{{xcolor}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{ragged2e}}
\usepackage{{enumitem}}
\usepackage{{fvextra}}
\usepackage{{titlesec}}
\usepackage{{fancyhdr}}
\usepackage{{amsthm}}
\usepackage{{tikz}}
\usepackage{{needspace}}
\usepackage[hidelinks,bookmarks=true,bookmarksnumbered=true]{{hyperref}}
\hypersetup{{pdftitle={{Fusion: Superproject Technical Report}},
  pdfauthor={{Fusion Superproject}},pdfsubject={{Engine, launcher, quantization, research}},
  pdfkeywords={{quantization, training, inference, serving, Cender, CodeFusion}}}}

\definecolor{{ink}}{{HTML}}{{0B1220}}
\definecolor{{ink2}}{{HTML}}{{101B2E}}
\definecolor{{ink3}}{{HTML}}{{16233A}}
\definecolor{{blue}}{{HTML}}{{2B7FFF}}
\definecolor{{cyan}}{{HTML}}{{22D3EE}}
\definecolor{{violet}}{{HTML}}{{8B5CF6}}
\definecolor{{amber}}{{HTML}}{{F59E0B}}
\definecolor{{pink}}{{HTML}}{{F472B6}}
\definecolor{{rule}}{{HTML}}{{24324D}}
\definecolor{{muted}}{{HTML}}{{64748B}}
\definecolor{{paper}}{{HTML}}{{F8FAFC}}

\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{1.15pt}}
\setlength{{\emergencystretch}}{{2.2em}}
\setlength{{\tabcolsep}}{{2pt}}
\renewcommand{{\arraystretch}}{{0.93}}
\setlength{{\abovedisplayskip}}{{2pt}}
\setlength{{\belowdisplayskip}}{{2pt}}
\setlength{{\abovedisplayshortskip}}{{0pt}}
\setlength{{\belowdisplayshortskip}}{{1pt}}
\fontsize{{{size}pt}}{{{lead}pt}}\selectfont
\linespread{{1.0}}

\titleformat{{\section}}[block]
  {{\normalfont\large\bfseries\color{{ink}}}}{{\thesection}}{{0.55em}}{{}}[{{\vspace{{1.5pt}}{{\color{{rule}}\hrule height 0.5pt}}}}]
\titlespacing*{{\section}}{{0pt}}{{7pt plus 2pt minus 1pt}}{{3pt}}
\titleformat{{\subsection}}
  {{\normalfont\normalsize\bfseries\color{{ink2}}}}{{\thesubsection}}{{0.45em}}{{}}
\titlespacing*{{\subsection}}{{0pt}}{{4.5pt plus 1pt minus 1pt}}{{1pt}}
\titleformat{{\subsubsection}}
  {{\normalfont\small\bfseries\color{{ink3}}}}{{}}{{0pt}}{{}}
\titlespacing*{{\subsubsection}}{{0pt}}{{3.5pt plus 1pt minus 1pt}}{{0.5pt}}

\pagestyle{{fancy}}
\fancyhf{{}}
\renewcommand{{\headrulewidth}}{{0pt}}
\renewcommand{{\footrulewidth}}{{0pt}}
\fancyhead[L]{{\fontsize{{6.6}}{{7.8}}\selectfont\color{{muted}}FUSION \textperiodcentered{{}} TECHNICAL REPORT}}
\fancyhead[R]{{\fontsize{{6.6}}{{7.8}}\selectfont\color{{muted}}EDITION 2026.11}}
\fancyfoot[C]{{\fontsize{{7.2}}{{8}}\selectfont\color{{muted}}\thepage}}

\setcounter{{tocdepth}}{{2}}
\renewcommand{{\contentsname}}{{Contents}}

\theoremstyle{{plain}}
\newtheorem{{theorem}}{{Theorem}}[section]
\newtheorem{{lemma}}[theorem]{{Lemma}}
\newtheorem{{corollary}}[theorem]{{Corollary}}
\theoremstyle{{definition}}
\newtheorem{{definition}}[theorem]{{Definition}}

\newcommand{{\partband}}[4]{{%
  \par\addvspace{{7pt}}%
  \noindent\colorbox{{ink}}{{\parbox{{\dimexpr\linewidth-2\fboxsep\relax}}{{%
    \color{{white}}\fontsize{{8.4}}{{10}}\selectfont\bfseries PART #1\quad #2}}}}%
  \par\vspace{{2pt}}%
  {{\color{{muted}}\fontsize{{7.3}}{{9}}\selectfont #3\par}}%
  \label{{#4}}%
  \addcontentsline{{toc}}{{section}}{{Part #1 \textperiodcentered{{}} #2}}%
  \par\vspace{{4pt}}%
}}
"""


COVER = r"""
\onecolumn
\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[ink] (current page.south west) rectangle (current page.north east);
  \foreach \i in {0,...,22} {
    \draw[white,opacity=0.022,line width=0.35pt]
      ([xshift=\i cm]current page.south west) -- ([xshift=\i cm]current page.north west);
    \draw[white,opacity=0.022,line width=0.35pt]
      ([yshift=\i cm]current page.south west) -- ([yshift=\i cm]current page.south east);
  }
  \begin{scope}[shift={([xshift=38mm,yshift=-38mm]current page.north east)}]
    \draw[cyan,opacity=0.20,line width=0.8pt] (0,0) circle (19mm);
    \draw[blue,opacity=0.16,line width=1.4pt] (0,0) circle (28mm);
    \draw[violet,opacity=0.16,line width=0.7pt,rotate=20] (0,0) ellipse (36mm and 15mm);
    \draw[cyan,line width=1.8pt,line join=round] (-10mm,5mm) -- (0,10mm) -- (10mm,5mm) -- (0,0) -- cycle;
    \draw[violet,line width=1.8pt,line join=round] (-10mm,-2mm) -- (0,3mm) -- (10mm,-2mm) -- (0,-7mm) -- cycle;
    \draw[pink,line width=1.8pt,line join=round] (-10mm,-9mm) -- (0,-4mm) -- (10mm,-9mm) -- (0,-14mm) -- cycle;
  \end{scope}
\end{tikzpicture}
\begin{minipage}[t][\dimexpr\textheight-\topskip-\parskip\relax][t]{\textwidth}
\color{white}
{\fontsize{7.2}{9}\selectfont\color{cyan}\bfseries
FUSION SUPERPROJECT \quad\textperiodcentered\quad TECHNICAL REPORT \quad\textperiodcentered\quad EDITION 2026.11\par}
\vspace{7mm}
{\fontsize{46}{48}\selectfont\bfseries Fusion\par}
\vspace{1mm}
{\fontsize{13.2}{16}\selectfont\color{white!92}Quantization \textperiodcentered{} Training \textperiodcentered{} Inference \textperiodcentered{} Serving\par}
\vspace{2mm}
{\color{cyan}\rule{62mm}{1.2pt}\par}
\vspace{4mm}

\noindent\begin{minipage}[t]{0.56\textwidth}
{\fontsize{8.3}{10.4}\selectfont
The technical report of the Fusion superproject: the C++20 engine, the Windows launcher and its
nine seats, and the plan, decision, research, and telemetry record that binds them. The edition
documents the engine specification and API, the format ladder and the quantization claim ledger,
the CodeFusion product record, a live arXiv research compendium, a theorem note on constant-memory
context and wire identity, and the full reference apparatus.\par}
\vspace{3mm}
{\fontsize{7.4}{9}\selectfont\color{white!75}
Every number in the registers is an edition fact tied to a named source. The report separates
disk-verified evidence from paper-only reading and from operator-supplied requirements. It states
what is implemented, what is designed, and what is still a target.\par}
\end{minipage}\hfill
\begin{minipage}[t]{0.40\textwidth}
{\fontsize{7.2}{8.6}\selectfont\color{cyan}\bfseries EDITION RECORD\par}
\vspace{1mm}
{\fontsize{7.0}{8.4}\selectfont
\begin{tabular}{@{}p{0.42\linewidth}p{0.52\linewidth}@{}}
\toprule
\textcolor{cyan}{Document} & Superproject technical report \\
\textcolor{cyan}{Edition} & 2026.11 \\
\textcolor{cyan}{Extent} & 512 pages \\
\textcolor{cyan}{Parts} & Eight \\
\textcolor{cyan}{Chapters} & @@NCHAPTERS@@ \\
\textcolor{cyan}{Research} & 101 arXiv records \\
\textcolor{cyan}{Components} & Engine, launcher, plan \\
\textcolor{cyan}{Language} & English \\
\bottomrule
\end{tabular}\par}
\end{minipage}

\vspace{6mm}
{\fontsize{7.2}{8.6}\selectfont\color{cyan}\bfseries THE EDITION IN NUMBERS\par}
\vspace{1mm}
{\fontsize{7.4}{9}\selectfont
\noindent\begin{tabular}{@{}p{0.235\textwidth}p{0.235\textwidth}p{0.235\textwidth}p{0.235\textwidth}@{}}
\toprule
\textbf{@@FILES@@} engine files & \textbf{@@FORMATS@@} wire formats & \textbf{@@TESTS@@} test files & \textbf{@@SEATS@@} launcher seats \\
\textbf{@@DECISIONS@@} decisions & \textbf{@@RESEARCH@@} research items & \textbf{@@LIBS@@} libraries & \textbf{@@BACKENDS@@} backends \\
\bottomrule
\end{tabular}\par}

\vspace{5mm}
{\fontsize{7.2}{8.6}\selectfont\color{cyan}\bfseries CONTENTS AT A GLANCE\par}
\vspace{1mm}
{\fontsize{7.1}{8.5}\selectfont
\noindent\begin{tabular}{@{}p{0.07\textwidth}p{0.25\textwidth}p{0.52\textwidth}r@{}}
\toprule
\textcolor{cyan}{Part} & \textcolor{cyan}{Subject} & \textcolor{cyan}{Scope} & \textcolor{cyan}{Page} \\
\midrule
I & The programme & Mission, master plan, decisions, research index, queue & \pageref{part:I} \\
II & CodeFusion & Launcher, registry, seats, provenance, slider & \pageref{part:II} \\
III & Transformers-Fusion & Engine specification, architecture, API, release & \pageref{part:III} \\
IV & Quantization science & Whitepaper, ladder, claims, proofs & \pageref{part:IV} \\
V & Research compendium & Six research lines and 101 arXiv records & \pageref{part:V} \\
VI & Theorem note & Constant memory, Cender design, wire identity & \pageref{part:VI} \\
VII & Method and evidence & Research loop, evidence register, validity & \pageref{part:VII} \\
VIII & Reference apparatus & Registers, glossary, bibliography, index & \pageref{part:VIII} \\
\bottomrule
\end{tabular}\par}

\vfill
{\fontsize{6.8}{8}\selectfont\color{white!55}
Fusion \textperiodcentered{} Superproject Technical Report \textperiodcentered{} Edition 2026.11
\textperiodcentered{} 512 pages \textperiodcentered{} PDF and DOCX\par}
\end{minipage}
\clearpage
\twocolumn
"""


def chapter_tex(ch: dict, generated: bool) -> str:
    title = booktex.inline_heading(ch["title"])
    if generated:
        return ch["body"] + "\n"
    body = booktex.convert(ch["lines"])
    return (r"\section{" + title + r"}\label{ch:" + ch["id"] + "}" +
            "\n" + body + "\n")


def part_band(part: str) -> str:
    title, scope = book_sources.PART_TITLES[part]
    return (r"\partband{" + part + "}{" + booktex.inline(title) + "}{" +
            booktex.inline(scope) + "}{part:" + part + "}" + "\n")


def index_table(chapters: list[dict]) -> str:
    rows = []
    for ch in chapters:
        part = ch["part"] if ch["part"] != "0" else "--"
        rows.append([booktex.inline(ch["title"]), part, r"\pageref{ch:" + ch["id"] + "}"])
    return "\n".join(booktex.table([["Chapter", "Part", "Page"]] + rows))


def assemble(size: float, lead: float, margin: float) -> tuple[str, list[dict]]:
    src = book_sources.load_all()
    generated = (book_extra.research_sections() + book_extra.theorem_sections()
                 + book_extra.method_sections() + book_appendix.appendix_sections())
    front = book_front.front_sections()
    chapters = front + src + generated

    cover = (COVER.replace("@@NCHAPTERS@@", str(len(chapters)))
             .replace("@@FILES@@", f"{F.N_FILES:,}")
             .replace("@@FORMATS@@", str(F.N_FORMATS))
             .replace("@@TESTS@@", str(F.N_TESTS))
             .replace("@@SEATS@@", str(F.N_SEATS))
             .replace("@@DECISIONS@@", str(F.N_DECISIONS))
             .replace("@@RESEARCH@@", str(F.N_RESEARCH))
             .replace("@@LIBS@@", str(F.N_LIBS))
             .replace("@@BACKENDS@@", str(F.N_BACKENDS)))

    out = [preamble(size, lead, margin), r"\begin{document}", cover,
           r"\tableofcontents", r"\clearpage"]

    seen_part = None
    for ch in chapters:
        if ch["part"] not in ("0", seen_part):
            out.append(part_band(ch["part"]))
            seen_part = ch["part"]
        out.append(chapter_tex(ch, "lines" not in ch))

    body = "\n".join(out)
    body = body.replace("@@CHAPTER_INDEX@@", index_table(chapters))
    body += "\n\\end{document}\n"
    return body, chapters


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=float, default=9.6)
    ap.add_argument("--lead", type=float, default=11.8)
    ap.add_argument("--margin", type=float, default=14.0)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    tex, chapters = assemble(args.size, args.lead, args.margin)
    open(TEX, "w", encoding="utf-8", newline="\n").write(tex)
    print(f"wrote {TEX} ({len(tex):,} bytes, {len(chapters)} chapters, "
          f"size={args.size}, lead={args.lead}, margin={args.margin})")
    if args.no_compile:
        return 0

    for pass_no in (1, 2, 3):
        r = run(["lualatex", "-interaction=nonstopmode", "-halt-on-error",
                 os.path.basename(TEX)], OUT)
        if r.returncode != 0:
            tail = (r.stdout or "")[-5000:]
            print(tail)
            raise SystemExit(f"lualatex pass {pass_no} failed")
        print(f"pass {pass_no}: ok")

    pdf = os.path.join(OUT, "Fusion-Report-512.pdf")
    print(f"pdf pages={page_count(pdf)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
