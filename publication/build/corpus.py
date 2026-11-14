#!/usr/bin/env python3
"""Assemble the 512-page report corpus.

Order (fixed by the publication plan):
  1-16   front matter
  17     Part I opener
  18-81  Fusion README (64 blocks)
  82     Part II opener
  83-210 CodeFusion README (128 blocks)
  211    Part III opener
  212-403 Transformers README (192 blocks)
  404    Part IV opener
  405-432 whitepaper (28)
  433    Part V opener
  434-447 theorem note (14)
  448    Part VI opener
  449-460 method (12)
  461    Part VII opener
  462-471 evidence (10)
  472    Part VIII opener
  473-492 appendices (20)
  493-500 glossary (8)
  501-506 bibliography (6)
  507-510 index (4)
  511-512 closing (2)
"""
from __future__ import annotations

import os
import re

import appendices
import front
import method
import theorem
import whitepaper
from pubfacts import WS

TARGET = 512


def readme_blocks(rel: str) -> list[dict]:
    path = os.path.join(WS, rel)
    lines = open(path, encoding="utf-8").read().splitlines()
    idx = [i for i, line in enumerate(lines) if line.startswith("## ")]
    out = []
    for k, i in enumerate(idx):
        end = idx[k + 1] if k + 1 < len(idx) else len(lines)
        title = lines[i][3:].strip()
        body = [l.rstrip() for l in lines[i + 1:end] if l.strip()]
        if len(body) > 30:
            raise SystemExit(f"{rel}: '{title}' has {len(body)} body lines")
        out.append({"title": title, "body": body, "kind": "readme"})
    return out


def blank(title: str, kind: str) -> dict:
    return {"title": title, "body": [], "kind": kind}


def estimate_lines(page: dict) -> float:
    """Rough typeset height of a block, in 11pt lines."""
    lines = 0.0
    fence = False
    for row in page.get("body", []):
        s = row.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            lines += 0.9
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and all(set(c) <= set("-: ") for c in cells):
                continue
            ncol = max(1, len(cells))
            per = max(8.0, 104.0 / ncol)
            lines += max(1.0, max(len(c) for c in cells) / per) * 0.86
            continue
        if s.startswith(("- ", "* ")):
            lines += max(1.0, len(s) / 90.0) * 1.05
            continue
        lines += max(1.0, len(s) / 88.0)
    return lines + 3.0


FITS = [
    (38.0, (11.0, 15.4)),
    (43.0, (10.5, 14.2)),
    (48.0, (10.0, 13.2)),
    (54.0, (9.6, 12.5)),
    (60.0, (9.2, 11.8)),
    (999.0, (8.8, 11.2)),
]


def fit_for(page: dict) -> tuple[float, float]:
    est = estimate_lines(page)
    size = FITS[-1][1]
    for limit, candidate in FITS:
        if est <= limit:
            size = candidate
            break
    maxcell = 0
    for row in page.get("body", []):
        if row.strip().startswith("|"):
            maxcell = max(maxcell, max((len(c) for c in row.split("|")), default=0))
    if maxcell > 200:
        size = min(size, (8.2, 10.4))
    elif maxcell > 120:
        size = min(size, (8.8, 11.2))
    return size


def build() -> list[dict]:
    fusion = readme_blocks("README.md")
    code = readme_blocks(os.path.join("code", "README.md"))
    tf = readme_blocks(os.path.join("transformers", "README.md"))
    assert len(fusion) == 64, len(fusion)
    assert len(code) == 128, len(code)
    assert len(tf) == 192, len(tf)

    parts = front.part_pages()
    wp = whitepaper.pages()
    th = theorem.pages()
    mp = method.method_pages()
    ev = method.evidence_pages()
    ax = appendices.appendix_pages()
    gl = appendices.glossary_pages()
    bb = appendices.bibliography_pages()
    cl = appendices.closing_pages()

    assert len(parts) == 8
    assert len(wp) == 28
    assert len(th) == 14
    assert len(mp) == 12
    assert len(ev) == 10
    assert len(ax) == 20
    assert len(gl) == 8
    assert len(bb) == 6
    assert len(cl) == 2

    pages: list[dict] = []
    pages += front.front_pages()
    pages.append(parts[0])
    pages += fusion
    pages.append(parts[1])
    pages += code
    pages.append(parts[2])
    pages += tf
    pages.append(parts[3])
    pages += wp
    pages.append(parts[4])
    pages += th
    pages.append(parts[5])
    pages += mp
    pages.append(parts[6])
    pages += ev
    pages.append(parts[7])
    pages += ax
    pages += gl
    pages += bb
    pages += [blank("Index, part 1", "index"), blank("Index, part 2", "index"),
              blank("Index, part 3", "index"), blank("Index, part 4", "index")]
    pages += cl

    if len(pages) != TARGET:
        raise SystemExit(f"corpus is {len(pages)} pages, expected {TARGET}")

    fill_toc(pages)
    fill_index(pages)
    for page in pages:
        page["fit"] = fit_for(page)
    return pages


def page_of(pages: list[dict], title: str) -> int:
    for n, page in enumerate(pages, start=1):
        if page["title"] == title:
            return n
    raise KeyError(title)


def fill_toc(pages: list[dict]) -> None:
    p1 = next(p for p in pages if p["kind"] == "toc1")
    p2 = next(p for p in pages if p["kind"] == "toc2")
    parts = [p for p in pages if p["kind"] == "part"]

    lines = ["| Part | Contents | Page |", "|---|---|---:|"]
    starts = [(p["title"], page_of(pages, p["title"])) for p in parts]
    for n, (title, start) in enumerate(starts):
        end = (starts[n + 1][1] - 2) if n + 1 < len(starts) else TARGET - 2
        short = title.split("·", 1)[1].strip() if "·" in title else title
        lines.append(f"| **{title.split('·')[0].strip()}** | {short} | {start}–{end} |")
    lines += [
        "The page numbers are the block numbers of this edition.",
        "A part opener is a full page and is counted in the range.",
        "The ranges are generated by `publication/build/corpus.py`.",
        "The front matter precedes Part I and is numbered 1–16.",
        "The reference apparatus follows Part VIII.",
        "The contents pages are themselves blocks and are counted.",
        "The report is exactly 512 pages; the last block is the end page.",
        "A reader can jump to a part by its start page.",
        "The table is generated from the assembled corpus, not typed.",
    ]
    p1["body"] = lines[:30]

    lines = ["| Reference | Page |", "|---|---:|"]
    for a in appendices.appendix_pages():
        lines.append(f"| {a['title']} | {page_of(pages, a['title'])} |")
    lines += [
        f"| Glossary A–Z | {page_of(pages, 'Glossary A–C')}–{page_of(pages, 'Glossary V–Z')} |",
        f"| Bibliography | {page_of(pages, 'Bibliography 1')}–{page_of(pages, 'Bibliography 6')} |",
        f"| Index | {page_of(pages, 'Index, part 1')}–{page_of(pages, 'Index, part 4')} |",
        f"| Colophon and end | {page_of(pages, 'Colophon')}–{TARGET} |",
        "The appendix letters run A through T.",
        "The glossary is grouped by initial letter.",
    ]
    p2["body"] = lines[:30]


def fill_index(pages: list[dict]) -> None:
    terms: list[str] = []
    for g in appendices.glossary_pages():
        for line in g["body"]:
            m = re.match(r"\*\*(.+?)\*\*", line)
            if m:
                terms.append(m.group(1))
    seen = set()
    entries: list[tuple[str, list[int]]] = []
    for term in terms:
        if term.lower() in seen:
            continue
        seen.add(term.lower())
        hits = []
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        for n, page in enumerate(pages, start=1):
            if page["kind"] in {"toc1", "toc2", "index"}:
                continue
            text = page["title"] + "\n" + "\n".join(page.get("body", []))
            if pat.search(text):
                hits.append(n)
                if len(hits) == 4:
                    break
        if hits:
            entries.append((term, hits))

    entries.sort(key=lambda e: e[0].lower())
    lines: list[str] = []
    last = ""
    for term, hits in entries:
        initial = term[0].upper()
        if initial != last:
            lines.append(f"**{initial}**")
            lines.append("")
            last = initial
        lines.append(f"**{term}** — " + ", ".join(str(h) for h in hits) + ".")

    stubs = [p for p in pages if p["kind"] == "index"]
    q, r = divmod(len(lines), len(stubs))
    pos = 0
    for n, stub in enumerate(stubs):
        take = q + (1 if n < r else 0)
        chunk = lines[pos:pos + take]
        pos += take
        stub["body"] = chunk or ["The index is complete on the preceding pages."]


if __name__ == "__main__":
    corpus = build()
    print(f"pages={len(corpus)}")
    for n in (1, 16, 17, 18, 81, 82, 210, 211, 403, 404, 432, 433, 447, 448,
              460, 461, 471, 472, 492, 493, 500, 501, 506, 507, 510, 511, 512):
        print(n, corpus[n - 1]["kind"], corpus[n - 1]["title"][:60])
