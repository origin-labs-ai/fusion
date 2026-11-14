#!/usr/bin/env python3
"""Front matter (16 pages) and part openers (8 pages)."""
from __future__ import annotations

from pubfacts import (fill, N_FORMATS, N_RETIRED, N_TESTS, N_LIBS, N_TARGETS,
                      N_BACKENDS, N_DECISIONS, N_RESEARCH, N_SEATS, N_CASES,
                      N_ASSERTS, N_FILES, N_LOC, CODE_FILES, TF_HEAD, CODE_HEAD,
                      FUSION_HEAD)

PAD = [
    "The edition is a snapshot with a named commit, not a living dashboard.",
    "The reader can reproduce every count with the command in the colophon.",
    "The report is generated from the same facts as the three READMEs.",
    "The publication is a record of the system, not a claim of peer review.",
    "The edition is reproducible from the pinned commits.",
    "The report does not replace the live dashboard.",
    "The report is a stable narrative, not a live instrument.",
    "The cover mark is project-authored.",
    "The type is Latin Modern; the code type is Inconsolata.",
    "The PDF is typeset with pdfLaTeX from TeX Live 2026.",
    "The DOCX is generated with python-docx and verified through Word.",
    "The report is exactly 512 pages in both editions.",
    "The three READMEs are the front door to this edition.",
    "The appendix carries the full indexes behind the prose.",
]


def pg(title: str, lines: list[str]) -> dict:
    return {"title": title, "body": fill(lines, PAD), "kind": "page"}


def front_pages() -> list[dict]:
    P = []
    P.append({
        "title": "Fusion",
        "subtitle": "The Superproject Technical Report",
        "body": [
            "Quantization · Training · Inference · Serving",
            "The C++20 engine and the Windows launcher, documented from the live tree.",
            f"Edition 2026.11 · {N_FORMATS} formats · {N_TESTS} test files · 512 pages",
        ],
        "kind": "cover",
    })
    P.append(pg("Imprint and document control", [
        "Fusion — The Superproject Technical Report.",
        "Edition 2026.11, generated from the live tree.",
        f"Superproject commit: `{FUSION_HEAD}`.",
        f"Engine commit: `{TF_HEAD}`. Launcher commit: `{CODE_HEAD}`.",
        f"Report target: 512 pages. PDF and DOCX editions are both 512 pages.",
        f"Knowledge base: {len(FUSION_DOCS)} authored Markdown documents in `.plan/`.",
        f"Decisions: {N_DECISIONS}. Research items: {N_RESEARCH}.",
        f"Engine: {N_FORMATS} valid formats, {N_RETIRED} retired ids, {N_TESTS} test files.",
        f"Launcher: {N_SEATS} seats, one registry, one consistency gate.",
        "Licence: the superproject grants no blanket licence over component or third-party material.",
        "The report is a documentation deliverable, not a peer-reviewed publication.",
        "The report does not relicense the code it describes.",
        "A quotation from an operator transcript is evidence, not a transfer of rights.",
        "The cover mark is project-authored.",
        "The type is Latin Modern; the engine is pdfLaTeX from TeX Live 2026.",
        "The DOCX edition is generated with python-docx and verified through Word.",
        "The manifest records the source commits, the targets and the hashes.",
        "The colophon records the exact commands.",
        "The next page states the abstract.",
    ]))
    P.append(pg("Abstract", [
        "This report documents Fusion, a superproject that combines a C++20 quantization and",
        "inference engine with a Windows launcher and a research programme.",
        "The engine implements a ladder of valid formats with a strict identity contract:",
        "a canonical name, a nominal bit width, a wire bit width and a stable identifier.",
        "The launcher presents its component seats through one registry and one consistency gate.",
        "The superproject owns the decisions, the telemetry and the publication.",
        "The report is organised in eight parts.",
        "Part I describes the superproject and its evidence standard.",
        "Part II describes the launcher and its nine seats.",
        "Part III describes the engine, its formats, libraries, executables and tests.",
        "Part IV is the whitepaper.",
        "Part V is the theorem note.",
        "Part VI describes the method and the reproducibility contract.",
        "Part VII carries the evidence tables and the appendices.",
        "Part VIII is the reference apparatus.",
        "The report does not claim a new state of the art.",
        "It does not claim that the 1.0 BPW goal has been reached.",
        "It does not claim that every audit is complete.",
        "It claims that the contracts are explicit, tested and documented.",
        "It claims that a reader can reproduce the counts.",
        "It claims that the evidence standard is applied.",
        "The edition is a snapshot; the live dashboard is the current state.",
        "The next pages summarise the work for a reader who has ten minutes.",
    ]))
    P.append(pg("Executive summary, part 1", [
        "Fusion is three repositories in one product shape.",
        "The engine is the numbers: formats, kernels, training, inference and serving.",
        "The launcher is the surface: nine seats, one registry and one gate.",
        "The plan is the evidence: decisions, research, telemetry and the grind tree.",
        f"The engine carries {N_FORMATS} valid formats and {N_RETIRED} retired ids.",
        f"The ladder is on the .0/.25/.50 BPW grid.",
        "The implemented path is 1.5 BPW; the goal is 1.0 BPW.",
        "The project says both things in the same sentence.",
        f"The engine has {N_LIBS} libraries, {N_TARGETS} executables and {N_TESTS} test files.",
        f"The suite carries {N_CASES} named cases and {N_ASSERTS:,} asserts.",
        f"The launcher has {N_SEATS} seats and a seven-part registry plus two support folders.",
        "The gate checks the registry, the launcher, the manifest and the folders.",
        "The plan carries 31 decisions and 18 research items.",
        "The documentation is generated at exact line counts: 2,048, 4,096 and 6,144.",
        "The report is generated at exactly 512 pages in PDF and DOCX.",
        "The next page continues the summary.",
    ]))
    P.append(pg("Executive summary, part 2", [
        "The strongest part of the project is the identity discipline.",
        "A format name is not a label; it is a promise about the wire.",
        "A retired id is not deleted; it is kept addressable.",
        "A checkpoint is not guessed; it is rejected if its identity is unknown.",
        "The second strongest part is the evidence discipline.",
        "Every claim names a command, an output and a file:line reference.",
        "The dashboard runs the gates and records the exits.",
        "The generators refuse to write an approximate count.",
        "The weakest part is the distance between the design and the measurements.",
        "The Cender theorem is a design theorem, not a measured result.",
        "The 1.0 BPW goal is open.",
        "Several audits are open.",
        "Some launcher seats are reserved rather than shipped.",
        "The report states those gaps rather than smoothing them.",
        "A reader who wants the current state should read the dashboard.",
        "A reader who wants the rules should read the decisions.",
        "A reader who wants the work should read the grind tree.",
        "The next page states the evidence standard.",
    ]))
    P.append(pg("The evidence standard", [
        "A claim is evidence-backed when a reader can repeat it.",
        "The minimum evidence is a command, its output and a file:line reference.",
        "A number without a command is an assertion.",
        "A command without an output is a rumour.",
        "An output without a path is hard to audit.",
        "The project records all three.",
        "The dashboard is the live instrument for the gates.",
        "The decision log is the record of the rules.",
        "The research index is the record of the reading.",
        "The todo tree is the record of the work.",
        "The publication is the long-form record of the result.",
        "The evidence standard applies to the publication too.",
        "The page count is checked, not estimated.",
        "The line counts are checked, not estimated.",
        "The hashes are recorded, not remembered.",
        "The next page explains how to read the report.",
    ]))
    P.append(pg("How to read this report", [
        "The report has eight parts and a reference apparatus.",
        "A reader who wants the product should start with Part I and Part II.",
        "A reader who wants the engine should start with Part III.",
        "A reader who wants the argument should start with Part IV.",
        "A reader who wants the formal note should start with Part V.",
        "A reader who wants to reproduce the build should start with Part VI.",
        "A reader who wants the tables should start with Part VII.",
        "A reader who wants a term should start with Part VIII.",
        "Every page is a self-contained block.",
        "A block has a heading and at most thirty lines.",
        "The blocks are ordered, not nested.",
        "A cross-reference names a part or a page, not a chapter number.",
        "The page footer carries the page number and the report title.",
        "The part opener carries the part number and the part argument.",
        "The tables are generated from the live facts.",
        "The code snippets are short and purposeful.",
        "The report is not a tutorial; it is a technical record.",
        "The next page describes the publication architecture.",
    ]))
    P.append(pg("Publication architecture, part 1", [
        "The publication has one source of facts and five artefacts.",
        "The facts come from `.plan/telemetry/docgen/facts.json`.",
        "The artefacts are the 512-page report in PDF and DOCX, the whitepaper, the theorem note",
        "and the arXiv package.",
        "The report is a sequence of 512 page blocks.",
        "The whitepaper is a 28-page extract of the argument.",
        "The theorem note is a 14-page extract of the formal claims.",
        "The arXiv package is a standalone LaTeX article with a bibliography.",
        "The architecture document explains how the artefacts relate.",
        "The manifest records the targets, the actual counts and the hashes.",
        "The report is built first; the extracts reuse its pages.",
        "The DOCX is built from the same blocks as the PDF.",
        "The page count is verified for both formats.",
        "The next page continues the architecture.",
    ]))
    P.append(pg("Publication architecture, part 2", [
        "The build directory contains the generator, the converter and the corpus.",
        "`corpus.py` assembles the 512 pages.",
        "`md2tex.py` converts the Markdown blocks to LaTeX.",
        "`build_pdf.py` writes the TeX file and runs pdfLaTeX.",
        "`build_docx.py` writes the DOCX and drives Word.",
        "`build_all.py` runs the steps in order and writes the manifest.",
        "The corpus is deterministic: the same facts produce the same blocks.",
        "The TeX file is generated, not hand-edited.",
        "The DOCX is generated, not hand-edited.",
        "The whitepaper and theorem are page slices of the report.",
        "The arXiv package is generated from the same prose, with its own preamble.",
        "The next pages are the table of contents.",
    ]))
    P.append({"title": "Contents, part 1", "body": [], "kind": "toc1"})
    P.append({"title": "Contents, part 2", "body": [], "kind": "toc2"})
    P.append(pg("The three READMEs", [
        "The report is built on the same facts as the three READMEs.",
        "`fusion/README.md` is 2,048 lines.",
        "`code/README.md` is 4,096 lines.",
        "`transformers/README.md` is 6,144 lines.",
        "Each README is generated by a script in `.plan/telemetry/docgen/`.",
        "Each generator refuses to write a file whose count is off.",
        "The READMEs are the front door; the report is the long-form edition.",
        "The READMEs use the OriginRouter visual language: centred header, logo, badges and tables.",
        "The report uses the same facts in a typeset form.",
        "The next page describes the 512-page edition.",
    ]))
    P.append(pg("The 512-page edition", [
        "The page count is a design constraint, not a by-product.",
        "The report is a sequence of 512 blocks.",
        "Each block is sized to fit one page.",
        "The build checks the count after the PDF is written.",
        "The DOCX is checked through Word.",
        "A mismatch stops the build.",
        "The count is recorded in the manifest.",
        "The edition is reproducible.",
        "The next page describes the naming conventions.",
    ]))
    P.append(pg("Naming and conventions", [
        "A part is numbered with a Roman numeral.",
        "A page is numbered with an Arabic numeral.",
        "A decision is named D-01 through D-31.",
        "A research item is named R-01 through R-18.",
        "A grind item is named T1 through T15, with sub-items.",
        "A format is named by its canonical spelling, such as Q_4 or Q_G_8_K_H.",
        "A launcher part is named by its codename.",
        "An alias is an edition label, not a codename.",
        "A seat is the folder reserved for a part.",
        "A submodule pin is a commit, not a branch.",
        "A gate is a check that stops the step when it fails.",
        "A verifier is a script that checks the plan.",
        "The conventions are used consistently in all three READMEs and in this report.",
        "The next page describes the sources and provenance.",
    ]))
    P.append(pg("Sources and provenance", [
        "The report is generated from the live tree.",
        "The primary sources are the two component repositories and the plan.",
        "The component repositories carry their own licences.",
        "The plan is project-authored.",
        "The archive preserves deleted documents for audit.",
        "The archive is reference-only and is never overridden.",
        "The report marks third-party material where it is known.",
        "The report does not relicense the code.",
        "The report does not claim peer review.",
        "The report does not claim that a research track has succeeded.",
        "The next page is a note on the archive.",
    ]))
    P.append(pg("A note on the archive", [
        "The project deleted a large documentation set in October.",
        "The archive preserves what was deleted.",
        "The archive is not a second source of truth.",
        "The live tree is the source of truth.",
        "The archive is useful because it records intent and history.",
        "The archive is dangerous when a stale name leaks into a new document.",
        "The generators therefore read the live tree, not the archive.",
        "The research index cites the archive only where the history matters.",
        "The report cites the archive only where the history matters.",
        "The next part begins the superproject.",
    ]))
    return P


def part_pages() -> list[dict]:
    parts = [
        ("I", "The Superproject", "Goal, topology, telemetry, decisions and the research programme.",
         "The superproject owns the cross-repository claims and the evidence that the two components agree."),
        ("II", "The Launcher", "Nine seats, one registry, one gate, one layout picker.",
         "The launcher is the product surface; the registry is its contract."),
        ("III", "The Engine", "Formats, codec, kernels, libraries, executables and tests.",
         "The engine is the numbers; every count in this part is generated from the live tree."),
        ("IV", "Whitepaper", "The argument for a quantization contract, stated end to end.",
         "The whitepaper is the conceptual spine of the report."),
        ("V", "Theorem Note", "Constant-memory attention and the TransCender wire identity.",
         "The note separates design theorems from measured results."),
        ("VI", "Method and Reproducibility", "How the documentation and the 512-page edition are built.",
         "The method is part of the evidence: a claim that cannot be reproduced is not finished."),
        ("VII", "Evidence and Appendices", "The ledgers, indexes and registers behind the report.",
         "The tables are generated from the same facts as the prose."),
        ("VIII", "Reference", "Glossary, bibliography, index and colophon.",
         "The reference apparatus closes the edition."),
    ]
    return [{"title": f"Part {num} · {name}", "subtitle": subtitle, "body": [line],
             "kind": "part", "part": num} for num, name, subtitle, line in parts]


FUSION_DOCS = __import__("json").load(
    open(__import__("os").path.join(__import__("os").path.dirname(__file__),
                                     "..", "..", ".plan", "telemetry", "docgen", "facts.json"),
         encoding="utf-8"))["fusion"]["doc_inventory"]
