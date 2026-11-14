#!/usr/bin/env python3
"""Markdown -> LaTeX for the continuous-flow Fusion report.

The converter is deliberately conservative: it understands the Markdown the
project documents actually use (headings, prose, lists, pipe tables, fenced
code, quotes and inline emphasis) and it escapes everything else.  Tables are
emitted in small chunks because a two-column page cannot host a long
unbreakable tabular environment.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------- symbols
GREEK = {
    "α": r"\(\alpha\)", "β": r"\(\beta\)", "γ": r"\(\gamma\)",
    "δ": r"\(\delta\)", "ε": r"\(\epsilon\)", "ζ": r"\(\zeta\)",
    "η": r"\(\eta\)", "θ": r"\(\theta\)", "ι": r"\(\iota\)",
    "κ": r"\(\kappa\)", "λ": r"\(\lambda\)", "μ": r"\(\mu\)",
    "ν": r"\(\nu\)", "ξ": r"\(\xi\)", "π": r"\(\pi\)",
    "ρ": r"\(\rho\)", "σ": r"\(\sigma\)", "τ": r"\(\tau\)",
    "υ": r"\(\upsilon\)", "φ": r"\(\phi\)", "χ": r"\(\chi\)",
    "ψ": r"\(\psi\)", "ω": r"\(\omega\)",
    "Γ": r"\(\Gamma\)", "Δ": r"\(\Delta\)", "Θ": r"\(\Theta\)",
    "Λ": r"\(\Lambda\)", "Ξ": r"\(\Xi\)", "Π": r"\(\Pi\)",
    "Σ": r"\(\Sigma\)", "Φ": r"\(\Phi\)", "Ψ": r"\(\Psi\)",
    "Ω": r"\(\Omega\)",
}

UNICODE_TEXT = {
    "\u2014": "---", "\u2013": "--", "\u2212": r"\(-\)",
    "\u00d7": r"\(\times\)", "\u00b7": r"\(\cdot\)", "\u2022": r"\(\bullet\)",
    "\u2192": r"\(\rightarrow\)", "\u2190": r"\(\leftarrow\)",
    "\u2194": r"\(\leftrightarrow\)", "\u21d2": r"\(\Rightarrow\)",
    "\u2264": r"\(\leq\)", "\u2265": r"\(\geq\)", "\u2260": r"\(\neq\)",
    "\u2248": r"\(\approx\)", "\u2261": r"\(\equiv\)", "\u221d": r"\(\propto\)",
    "\u00b1": r"\(\pm\)", "\u2213": r"\(\mp\)", "\u00b0": r"\(^{\circ}\)",
    "\u221e": r"\(\infty\)", "\u221a": r"\(\sqrt{}\)", "\u2211": r"\(\sum\)",
    "\u220f": r"\(\prod\)", "\u2202": r"\(\partial\)", "\u2207": r"\(\nabla\)",
    "\u2208": r"\(\in\)", "\u2209": r"\(\notin\)", "\u2282": r"\(\subset\)",
    "\u2286": r"\(\subseteq\)", "\u2283": r"\(\supset\)", "\u2287": r"\(\supseteq\)",
    "\u222a": r"\(\cup\)", "\u2229": r"\(\cap\)", "\u2200": r"\(\forall\)",
    "\u2203": r"\(\exists\)", "\u00ac": r"\(\neg\)", "\u2227": r"\(\wedge\)",
    "\u2228": r"\(\vee\)", "\u22a5": r"\(\perp\)", "\u2225": r"\(\parallel\)",
    "\u2026": r"\ldots{}", "\u00a0": "~", "\u2009": r"\,", "\u200b": "",
    "\u2018": "`", "\u2019": "'", "\u201c": "``", "\u201d": "''",
    "\u00ab": r"\guillemotleft{}", "\u00bb": r"\guillemotright{}",
    "\u00a7": r"\S{}", "\u00b6": r"\P{}", "\u2020": r"\dag{}",
    "\u2021": r"\ddag{}", "\u00a9": r"\copyright{}", "\u00ae": r"\textregistered{}",
    "\u2122": r"\texttrademark{}", "\u00bd": r"\textonehalf{}",
    "\u00bc": r"\textonequarter{}", "\u00be": r"\textthreequarters{}",
    "\u00b5": r"\(\mu\)", "\u03bc": r"\(\mu\)",
    "\u2070": r"\(^{0}\)", "\u00b9": r"\(^{1}\)", "\u00b2": r"\(^{2}\)",
    "\u00b3": r"\(^{3}\)", "\u2074": r"\(^{4}\)", "\u2075": r"\(^{5}\)",
    "\u2076": r"\(^{6}\)", "\u2077": r"\(^{7}\)", "\u2078": r"\(^{8}\)",
    "\u2079": r"\(^{9}\)", "\u207b": r"\(^{-}\)", "\u207a": r"\(^{+}\)",
    "\u2080": r"\(_{0}\)", "\u2081": r"\(_{1}\)", "\u2082": r"\(_{2}\)",
    "\u2083": r"\(_{3}\)", "\u2084": r"\(_{4}\)",
    "\u1d40": r"\(^{\mathsf{T}}\)", "\u1d40": r"\(^{\mathsf{T}}\)",
    "\u2261": r"\(\equiv\)", "\u2245": r"\(\cong\)", "\u2243": r"\(\simeq\)",
    "\u27f6": r"\(\longrightarrow\)", "\u21a6": r"\(\mapsto\)",
    "\u27e8": r"\(\langle\)", "\u27e9": r"\(\rangle\)",
    "\u230a": r"\(\lfloor\)", "\u230b": r"\(\rfloor\)",
    "\u2308": r"\(\lceil\)", "\u2309": r"\(\rceil\)",
    "\u2220": r"\(\angle\)", "\u25b3": r"\(\triangle\)",
    "\u2605": r"\(\star\)", "\u2713": r"\(\checkmark\)",
    "\u2717": r"\(\times\)", "\u00b7": r"\(\cdot\)",
}

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF\U00002300-\U000023FF\uFE0F\u200d]+")


def clean_heading(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "")
    text = EMOJI_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" #-*:.")
    return text


def esc(text: str) -> str:
    table = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(table.get(ch, ch) for ch in text)


def code_ascii(text: str) -> str:
    text = text.replace("\t", "    ")
    repl = {
        "\u2014": "--", "\u2013": "-", "\u00d7": "x", "\u00b7": ".",
        "\u2192": "->", "\u2190": "<-", "\u2264": "<=", "\u2265": ">=",
        "\u00b1": "+/-", "\u00b0": "deg", "\u2026": "...", "\u2018": "'",
        "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00a0": " ",
        "\u2212": "-", "\u03bc": "u", "\u00b5": "u",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return "".join(ch if 32 <= ord(ch) < 127 else "" for ch in text)


MATH_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.S),
    re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$", re.S),
    re.compile(r"\\\((.+?)\\\)", re.S),
    re.compile(r"\\\[(.+?)\\\]", re.S),
]


MATH_TEXT = {
    "cdot": ".", "times": "x", "rightarrow": "->", "leftarrow": "<-",
    "leftrightarrow": "<->", "Rightarrow": "=>", "leq": "<=", "geq": ">=",
    "neq": "!=", "approx": "~", "equiv": "=", "propto": "prop", "pm": "+/-",
    "mp": "-/+", "infty": "inf", "sum": "sum", "prod": "prod", "partial": "d",
    "nabla": "grad", "in": "in", "notin": "not in", "subset": "subset",
    "subseteq": "subset=", "cup": "U", "cap": "n", "forall": "all",
    "exists": "exists", "neg": "not", "wedge": "and", "vee": "or",
    "alpha": "alpha", "beta": "beta", "gamma": "gamma", "delta": "delta",
    "epsilon": "epsilon", "zeta": "zeta", "eta": "eta", "theta": "theta",
    "kappa": "kappa", "lambda": "lambda", "mu": "mu", "nu": "nu", "xi": "xi",
    "pi": "pi", "rho": "rho", "sigma": "sigma", "tau": "tau",
    "upsilon": "upsilon", "phi": "phi", "chi": "chi", "psi": "psi",
    "omega": "omega", "Gamma": "Gamma", "Delta": "Delta", "Theta": "Theta",
    "Lambda": "Lambda", "Xi": "Xi", "Pi": "Pi", "Sigma": "Sigma",
    "Phi": "Phi", "Psi": "Psi", "Omega": "Omega", "sqrt": "sqrt",
}

GREEK_TEXT = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
    "ζ": "zeta", "η": "eta", "θ": "theta", "ι": "iota", "κ": "kappa",
    "λ": "lambda", "μ": "mu", "ν": "nu", "ξ": "xi", "π": "pi", "ρ": "rho",
    "σ": "sigma", "τ": "tau", "υ": "upsilon", "φ": "phi", "χ": "chi",
    "ψ": "psi", "ω": "omega", "Γ": "Gamma", "Δ": "Delta", "Θ": "Theta",
    "Λ": "Lambda", "Ξ": "Xi", "Π": "Pi", "Σ": "Sigma", "Φ": "Phi",
    "Ψ": "Psi", "Ω": "Omega",
}

HEADING_TEXT = {
    "\u00d7": "x", "\u00b7": ".", "\u2022": ".", "\u2192": "->",
    "\u2190": "<-", "\u2194": "<->", "\u21d2": "=>", "\u2264": "<=",
    "\u2265": ">=", "\u2260": "!=", "\u2248": "~", "\u2261": "=",
    "\u221d": "prop", "\u00b1": "+/-", "\u2213": "-/+", "\u00b0": "deg",
    "\u221e": "inf", "\u221a": "sqrt", "\u2211": "sum", "\u220f": "prod",
    "\u2202": "d", "\u2207": "grad", "\u2208": "in", "\u2209": "not in",
    "\u2282": "subset", "\u2286": "subset=", "\u222a": "U", "\u2229": "n",
    "\u2200": "all", "\u2203": "exists", "\u00ac": "not", "\u2227": "and",
    "\u2228": "or", "\u22a5": "perp", "\u2225": "par", "\u2026": "...",
    "\u00a0": " ", "\u2009": " ", "\u200b": "", "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"', "\u00ab": "<<", "\u00bb": ">>",
    "\u00a7": "S", "\u00b6": "P", "\u2020": "+", "\u2021": "++",
    "\u00a9": "(c)", "\u00ae": "(R)", "\u2122": "(TM)", "\u00bd": "1/2",
    "\u00bc": "1/4", "\u00be": "3/4", "\u00b5": "u", "\u03bc": "u",
    "\u2070": "^0", "\u00b9": "^1", "\u00b2": "^2", "\u00b3": "^3",
    "\u2074": "^4", "\u2075": "^5", "\u2076": "^6", "\u2077": "^7",
    "\u2078": "^8", "\u2079": "^9", "\u207b": "^-", "\u207a": "^+",
    "\u2080": "_0", "\u2081": "_1", "\u2082": "_2", "\u2083": "_3",
    "\u2084": "_4", "\u1d40": "T", "\u2245": "~=", "\u2243": "~",
    "\u27f6": "-->", "\u21a6": "|->", "\u27e8": "<", "\u27e9": ">",
    "\u230a": "floor(", "\u230b": ")", "\u2308": "ceil(", "\u2309": ")",
    "\u2220": "angle", "\u25b3": "triangle", "\u2605": "*", "\u2713": "ok",
    "\u2717": "x", "\u2212": "-", **GREEK_TEXT,
}


def math_text(body: str) -> str:
    body = re.sub(r"\\left|\\right", "", body)
    body = re.sub(r"\\([A-Za-z]+)", lambda m: MATH_TEXT.get(m.group(1), m.group(1)), body)
    body = body.replace("\\", "").replace("{", "").replace("}", "")
    return body


def inline_heading(text: str) -> str:
    """Heading text safe for both the page and the PDF bookmark string."""
    text = text.replace("\r", " ")
    text = re.sub(r"\\\\\[", r"\[", text)
    text = re.sub(r"\\\\\]", r"\]", text)
    text = re.sub(r"\\\\\(", r"\(", text)
    text = re.sub(r"\\\\\)", r"\)", text)
    for pat in MATH_PATTERNS:
        text = pat.sub(lambda m: " " + math_text(m.group(1)) + " ", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    for k, v in HEADING_TEXT.items():
        if k in text:
            text = text.replace(k, v)
    text = EMOJI_RE.sub("", text)
    text = "".join(ch for ch in text if ord(ch) < 128)
    text = esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\\emph{\1}", text)
    text = re.sub(r"__([^_]+)__", r"\\textbf{\1}", text)
    return text


def inline(text: str, heading: bool = False) -> str:
    """Convert one line of inline Markdown to LaTeX."""
    text = text.replace("\r", " ")
    tokens: list[str] = []

    def protect(value: str) -> str:
        tokens.append(value)
        return f"@@X{len(tokens) - 1}@@"

    # fenced/backtick code first
    text = re.sub(r"`([^`]+)`", lambda m: protect(
        r"\texttt{" + esc(code_ascii(m.group(1))) + "}"), text)

    # documents sometimes escape the math delimiters themselves
    text = re.sub(r"\\\\\[", r"\[", text)
    text = re.sub(r"\\\\\]", r"\]", text)
    text = re.sub(r"\\\\\(", r"\(", text)
    text = re.sub(r"\\\\\)", r"\)", text)

    # display math, then inline math
    def math_repl(m: re.Match) -> str:
        body = m.group(1).strip().replace("\\\\", " ")
        if m.group(0).startswith("$$"):
            return protect(r"\[" + body + r"\]")
        return protect(r"\(" + body + r"\)")

    text = MATH_PATTERNS[0].sub(math_repl, text)
    text = MATH_PATTERNS[1].sub(math_repl, text)
    text = MATH_PATTERNS[2].sub(math_repl, text)
    text = MATH_PATTERNS[3].sub(math_repl, text)

    # unicode symbols that need math mode
    for k, v in {**GREEK, **UNICODE_TEXT}.items():
        if k in text:
            text = text.replace(k, protect(v))

    text = EMOJI_RE.sub("", text)
    text = esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\\emph{\1}", text)
    text = re.sub(r"__([^_]+)__", r"\\textbf{\1}", text)

    def link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://")):
            safe = url.replace("\\", "").replace("%", r"\%").replace("#", r"\#")
            safe = safe.replace("_", r"\_")
            return r"\href{" + safe + "}{" + label + "}"
        return label

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)

    # any remaining non-ASCII that the font may not have
    text = "".join(ch if ord(ch) < 128 or ch in "éèêëáàâäíìîïóòôöúùûüñçÉÈÊËÁÀÂÄÍÌÎÏÓÒÔÖÚÙÛÜÑÇ" else "" for ch in text)
    for i, tok in enumerate(tokens):
        text = text.replace(f"@@X{i}@@", tok)
    return text


def heading(line: str) -> tuple[int, str]:
    level = len(line) - len(line.lstrip("#"))
    return level, clean_heading(line.lstrip("#").strip())


def table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    sep = all(set(c.strip()) <= set("-: ") and c.strip() for c in rows[1]) if len(rows) > 1 else False
    header, body = (rows[0], rows[2:]) if sep else (rows[0], rows[1:])
    if not body:
        body = [[""] * ncols]
    weights = []
    for c in range(ncols):
        longest = max(len(r[c]) for r in rows)
        weights.append(max(2.4, float(longest)) ** 0.62)
    total = sum(weights)
    spec = " ".join(
        r">{\raggedright\arraybackslash}p{\dimexpr %.4f\linewidth-2\tabcolsep\relax}" %
        (w / total) for w in weights)
    longest = max((len(c) for r in rows for c in r), default=0)
    size = "tiny" if longest > 110 else ("scriptsize" if longest > 55 else "footnotesize")
    char_mm = {"tiny": 0.94, "scriptsize": 1.12, "footnotesize": 1.32}[size]
    # column width is ~88mm in the two-column layout; estimate the text that fits
    cpl = [max(6, int((88.0 * (w / total)) / char_mm)) for w in weights]

    def fit(row: list[str]) -> list[str]:
        """Truncate any cell that would make the row taller than a safe chunk."""
        out = []
        for text, per_line in zip(row, cpl):
            t = text.strip()
            cap = max(48, per_line * 34)
            if len(t) > cap:
                t = t[:cap - 3].rstrip() + "..."
            out.append(t)
        return out

    header = fit(header)
    body = [fit(r) for r in body]

    def row_lines(r: list[str]) -> int:
        return max(1, max((len(c) + per - 1) // per for c, per in zip(r, cpl)))

    def cell(text: str) -> str:
        out = inline(text)
        if out.lstrip().startswith("["):
            out = r"{[}" + out.lstrip()[1:]
        return out

    def emit(chunk: list[list[str]]) -> list[str]:
        out = [r"\begin{center}", r"\begingroup\%s" % size,
               r"\setlength{\tabcolsep}{2pt}",
               r"\begin{tabular}{" + spec + "}", r"\toprule"]
        out.append(" & ".join(cell(c) for c in header) + r" \\")
        out.append(r"\midrule")
        for r in chunk:
            out.append(" & ".join(cell(c) for c in r) + r" \\")
        out += [r"\bottomrule", r"\end{tabular}", r"\endgroup", r"\end{center}"]
        return out

    out: list[str] = []
    chunk: list[list[str]] = []
    used = 0
    budget = 44
    for row in body:
        need = row_lines(row)
        if chunk and used + need > budget:
            if out:
                out.append(r"\vspace{1pt}")
            out.extend(emit(chunk))
            chunk, used = [], 0
        chunk.append(row)
        used += need
    if chunk:
        if out:
            out.append(r"\vspace{1pt}")
        out.extend(emit(chunk))
    return out


def convert(lines: list[str], labels: bool = True) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        raw = lines[i].rstrip("\n")
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue
        s = line.lstrip()
        if s.startswith("```"):
            i += 1
            code: list[str] = []
            while i < n and not lines[i].lstrip().startswith("```"):
                code.append(code_ascii(lines[i].rstrip("\n")))
                i += 1
            i += 1
            if len(code) > 20:
                code = code[:12] + ["... (listing continues)"] + code[-5:]
            out.append(r"\begin{Verbatim}[breaklines=true,breakanywhere=true,"
                       r"fontsize=\scriptsize,frame=single,rulecolor=\color{rule}]")
            out.extend(code)
            out.append(r"\end{Verbatim}")
            continue
        if s.startswith("|"):
            block = []
            while i < n and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                block.append(cells)
                i += 1
            out.extend(table(block))
            continue
        if s.startswith(">"):
            quote = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append(r"\begin{quote}\small " + inline(" ".join(quote)) + r"\end{quote}")
            continue
        if re.match(r"^\s*[-*+]\s+", line):
            out.append(r"\begin{itemize}[leftmargin=1.05em,itemsep=0.5pt,topsep=1pt,parsep=0pt]")
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                item = re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip()
                out.append(r"\item " + inline(item))
                i += 1
            out.append(r"\end{itemize}")
            continue
        if re.match(r"^\s*\d+[.)]\s+", line):
            out.append(r"\begin{enumerate}[leftmargin=1.2em,itemsep=0.5pt,topsep=1pt,parsep=0pt]")
            while i < n and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                item = re.sub(r"^\s*\d+[.)]\s+", "", lines[i]).strip()
                out.append(r"\item " + inline(item))
                i += 1
            out.append(r"\end{enumerate}")
            continue
        if s.startswith("#"):
            level, text = heading(line)
            if not text:
                i += 1
                continue
            cmd = {1: "subsection", 2: "subsection", 3: "subsubsection",
                   4: "paragraph", 5: "paragraph"}.get(level, "paragraph")
            label = ""
            m = re.match(r"^(D-\d+)", text)
            if labels and m:
                label = r"\label{dec:%s}" % m.group(1)
            m = re.match(r"^(R-\d+)", text)
            if labels and m:
                label = r"\label{res:%s}" % m.group(1)
            if cmd == "paragraph":
                out.append(r"\par\noindent\textbf{" + inline_heading(text) + r"}\ " + label)
            else:
                out.append("\\" + cmd + "{" + inline_heading(text) + "}" + label)
            i += 1
            continue
        # prose: merge hard-wrapped lines, keep very long lines as paragraphs
        para = [s]
        i += 1
        if len(s) < 220:
            while i < n:
                nxt = lines[i].strip()
                if (not nxt or nxt.startswith(("#", "```", "|", ">"))
                        or re.match(r"^[-*+]\s+", nxt)
                        or re.match(r"^\d+[.)]\s+", nxt)):
                    break
                para.append(nxt)
                i += 1
                if len(nxt) > 220:
                    break
        out.append(inline(" ".join(para)) + r"\par")
    return "\n".join(out)
