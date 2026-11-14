#!/usr/bin/env python3
"""Front matter written for this edition: preface and conventions."""
from __future__ import annotations

import booktex


def tex(text: str) -> str:
    return booktex.inline(str(text))


PREFACE = r"""
\section{Preface}\label{ch:preface}
This is the technical report of the Fusion superproject. It documents one product assembled from
three repositories: the C++20 engine, the Windows launcher and its nine seats, and the plan,
decision, research, and telemetry record that keeps the other two honest. The report is written
for a reader who has the tree open and wants to know what is true, what is designed, and what is
still a target. It is not a release note, a build log, or a benchmark paper. It is the long-form
edition of the same facts that the project records in its registers.

\subsection{What this edition contains}
The report has eight parts. Part I records the programme: the goal line, the master plan, the
decision register, the research index, and the live queue. Part II documents CodeFusion: the
launcher, the registry, the seats, the reverse-engineering work, and the product history. Part III
documents Transformers-Fusion: the training-engine specification, the architecture, the API, the
tensor contract, the build and usage paths, the manifest and wire identity, and the engine's own
README. Part IV collects the quantization science: the QUANT whitepaper, the format ladder, the
claim ledger, the comparison charts, and the proof expansions. Part V is a
research compendium built from live arXiv metadata. Part VI is the theorem note: a constant-memory
context bound, the Cender design contract, and the wire-identity theorem. Part VII records the
method and the evidence register. Part VIII is the reference apparatus: format, test, library,
seat, decision, and research registers, a glossary, a bibliography, and an index.

\subsection{What the report does not claim}
The report does not claim that Cender is implemented. The engine still runs transformer attention;
the Cender recurrence is a design with a stated experiment. The report does not claim that the
1.0 bit-per-weight goal has been reached. The implemented path is 1.5 bits per weight, and the
difference is a research target. The report does not claim that a backend is fast because it is
listed. Availability is probed at runtime, and a backend that is unavailable is reported as
unmeasurable rather than as zero. The report does not claim that a generated number will be true
tomorrow. The counts are edition facts; the registers are the live source.

\subsection{The goal line}
The main goal is the entire Fusion superproject: every domain, every seat, and every track
complete. The side goal is maximum quality at exactly 1.0 bit per weight. The implemented 1.5 BPW
path is a stepping stone, not the destination. Both format families are in scope: floating point
(FP8, FP4, E5M2 and their relatives) and integer (INT8, INT4, binary, and ternary). Loop
quantization has never been implemented for any model anywhere; Track B would be the first. The
report repeats the goal line because a reader who sees only the 1.5 BPW tables can mistake the
stepping stone for the destination.

\subsection{The evidence labels}
Three labels recur. \textbf{Disk-verified} means the claim was re-read from the tree on a stated
date and a command or test reproduces it. \textbf{Paper-only} means the claim comes from the
literature and has not been re-run on this hardware. \textbf{Operator-supplied} means the claim is
a requirement or a ruling, not a measurement. A sentence without a label inherits the weakest
label in its paragraph. The labels are not decoration; they tell a reader how much work is left
before a claim can be published as a measurement.

\subsection{Reading paths}
\begin{center}
\footnotesize
\begin{tabular}{@{}p{0.24\linewidth}p{0.66\linewidth}@{}}
\toprule
Reader & Path \\
\midrule
New to the project & Preface, Part I (mission and master plan), Part III (engine overview), Part VIII (glossary). \\
Engineer & Part III (specification, API, tensor, build), Part IV (ladder and claims), Part VII (method). \\
Researcher & Part IV (whitepaper and proofs), Part V (arXiv compendium), Part VI (theorem note). \\
Operator & Part I (goal line and decisions), Part II (seats and provenance), Part VII (evidence). \\
Reviewer & Part VII (threats), Part VIII (registers), then the chapter under review. \\
\bottomrule
\end{tabular}
\end{center}

\subsection{A note on names}
The product is \textbf{Fusion}. The launcher side is \textbf{CodeFusion}; its folder and repository
are named \texttt{code}. The engine side is \textbf{Transformers-Fusion}; its folder and repository
are named \texttt{transformers}. \textbf{TransCender} is the engine's former name and remains a
legacy wire identity. The three names are related but not interchangeable, and the report keeps
the distinction visible. A model name is not a wire identity: \texttt{Sol} names the trained model
family, while \texttt{SolIDX} is reserved for model manifests.

\subsection{A note on numbers}
A format count is a contract count. A test-file count is a file count, not a coverage percentage.
An assertion count is a static count of declared assertions, not a count of executed assertions.
A page count is a typeset fact of this edition. The report keeps these distinctions because the
project has already been burned by a number that was true in one sense and false in another.
"""

CONVENTIONS = r"""
\section{Conventions}\label{ch:conventions}
\subsection{Identifiers}
Decision identifiers have the form \texttt{D-01}; research identifiers have the form
\texttt{R-01}; formats are written in the engine's spelling, for example \texttt{Q\_1} or
\texttt{Q\_4\_K\_M}. The underscore is part of the name, not a typographic separator. A format
identifier in a table is the integer wire id; a format name is the stable API spelling. When a
name and an identifier disagree, the identifier is the wire truth and the name is the API truth;
the register records both.

\subsection{Units}
Bits per weight (BPW) are nominal unless the text says wire BPW. A nominal BPW ignores scales,
zero points, and block metadata; a wire BPW includes them. Latency is wall-clock time in
milliseconds; throughput is tokens per second. Memory is bytes per sequence or bytes per model,
stated explicitly. A ratio without a denominator is not a measurement.

\subsection{Dates}
Dates are ISO 8601 (YYYY-MM-DD) unless a document quotes an operator message. The report uses
"2026-11" as the edition stamp. A date in a trace is the date the operator said it, not the date
the document was edited.

\subsection{Code and commands}
Inline code is set in a monospace face. A command is shown as it would be typed, but the report
does not print machine-specific paths. A reader who needs the exact path should read the
corresponding register or the component's own documentation. Code listings are abbreviated when
they exceed the page's capacity; the abbreviation is marked and the surrounding prose names the
file and the symbol.

\subsection{Tables}
Tables are generated from the same registers that the text cites. A table row is a record, not a
sentence; the prose around it explains why the record matters. When a table is split across
columns, the header is repeated. A row that is absent from a register is absent from the table,
and that absence is itself a fact.

\subsection{Quotations}
Operator quotations are preserved verbatim where they carry a ruling. They are marked as traces
and are not translated. A quotation is evidence of intent, not a specification; the specification
is the decision that cites it. Where a quotation and a later decision disagree, the later decision
wins and the quotation is kept as history.
"""


def front_sections() -> list[dict]:
    return [
        {"id": "preface", "part": "0", "title": "Preface", "body": PREFACE},
        {"id": "conventions", "part": "0", "title": "Conventions", "body": CONVENTIONS},
    ]
