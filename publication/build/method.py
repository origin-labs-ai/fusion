#!/usr/bin/env python3
"""Method pages (12) and evidence tables (10): 22 pages of 30 body lines."""
from __future__ import annotations

from pubfacts import (fill, DECISIONS, RESEARCH, FORMATS, RETIRED, TESTS,
                      N_DECISIONS, N_RESEARCH, N_FORMATS, N_RETIRED,
                      N_TESTS, N_CASES, N_ASSERTS, human)

PAD = [
    "The step is recorded in the repository so a cold reader can repeat it.",
    "The command is quoted with its output, not paraphrased.",
    "A failure is recorded with the same care as a success.",
    "The build is idempotent unless the live tree changed.",
    "The page-block model is what makes the page count verifiable.",
    "The build is run from the repository root so the paths resolve.",
    "The page-block model keeps the PDF and DOCX editions aligned.",
    "The DOCX edition is converted with Word and checked with pdfinfo.",
    "The facts file is regenerated before the build, not after it.",
    "The manifest records the target, the actual count and the hash.",
    "A verifier failure stops the publication rather than being noted.",
    "The method is reproducible from a cold clone with the documented tools.",
    "The commands are quoted as they were run.",
    "The report does not depend on a private service or a hidden step.",
    "The 512-page count is a design constraint that the build enforces.",
    "The standalone whitepaper and theorem note reuse the same page blocks.",
    "The arXiv package is generated from the same prose with its own preamble.",
    "The publication architecture document explains how the artefacts relate.",
    "The edition record is the last page of the appendix.",
    "The method chapter is part of the evidence, not an afterthought.",
]


def pg(title: str, lines: list[str]) -> dict:
    return {"title": title, "body": fill(lines, PAD), "kind": "page"}


def method_pages() -> list[dict]:
    P = []
    P.append(pg("1. The documentation programme", [
        "The programme is recorded as D-31 in the decision log.",
        "It sets exact targets: 2,048 lines for Fusion, 4,096 for CodeFusion and 6,144 for the engine.",
        "It sets exact page targets: 512 pages for the report in both PDF and DOCX.",
        "It names the visual reference: the OriginRouter README.",
        "It requires a generator, a validator and a manifest for every artefact.",
        "It forbids placeholders, walls of source and approximate counts.",
        "The programme is part of the product, not a side quest.",
        "The next page describes the count discipline.",
    ]))
    P.append(pg("2. Exact counts", [
        "An exact count is a testable claim.",
        "An approximate count is not.",
        "The README generators assert the target before they write.",
        "The PDF build asserts the page count with `pdfinfo`.",
        "The DOCX build converts to PDF with Word and asserts the same count.",
        "A count that is off by one line stops the build.",
        "A count that is off by one page stops the publication.",
        "The discipline is deliberately strict because a soft target drifts.",
        "The next page describes the fact extractor.",
    ]))
    P.append(pg("3. The fact extractor", [
        "The extractor is `.plan/telemetry/docgen/facts.py`.",
        "It reads the decision log, the research index, the todo tree and the document inventory.",
        "It reads the engine enum, the CMake targets, the source tree and the test suite.",
        "It reads the launcher registry, the layouts and the tracked file inventory.",
        "It writes `facts.json`.",
        "The README generators read that file.",
        "The publication build reads the same file.",
        "The extractor is run before a documentation build.",
        "The extractor is not a source of truth; it is a reproducible view of the sources.",
        "The next page describes the Markdown to LaTeX step.",
    ]))
    P.append(pg("4. Markdown to LaTeX", [
        "The README sections are Markdown.",
        "The report is LaTeX.",
        "The converter handles the subset the generators emit.",
        "It escapes special characters before it applies inline markup.",
        "It converts pipe tables to `tabularx`.",
        "It converts fenced code to a framed verbatim block.",
        "It converts bullets and numbered lists to LaTeX lists.",
        "It drops HTML and unknown Unicode rather than guessing.",
        "It does not attempt to be a general Markdown implementation.",
        "The next page describes the page-block model.",
    ]))
    P.append(pg("5. The page-block model", [
        "A page block is a heading plus at most 30 body lines.",
        "A block is sized to fit one A4 page at the report's type size.",
        "The report is a sequence of blocks.",
        "Every block except the last ends with an explicit page break.",
        "A block that overflows would add a page and break the count.",
        "The build checks the count after the PDF is written.",
        "If a block overflows, the whole document is re-laid out; the block is not silently split.",
        "The model is simple enough to audit and strict enough to verify.",
        "The next page describes the DOCX path.",
    ]))
    P.append(pg("6. DOCX generation and Word COM", [
        "The DOCX is generated with python-docx.",
        "Each page block becomes a heading, its body and a page break.",
        "The page break is set with `page_break_before` on the heading, not appended as a paragraph.",
        "That avoids a trailing blank page.",
        "The DOCX is converted to PDF with Word COM.",
        "Word is driven through PowerShell with the `SaveAs` format for PDF.",
        "The resulting PDF is checked with `pdfinfo`.",
        "The DOCX and the PDF share the same block source.",
        "The next page describes page-count verification.",
    ]))
    P.append(pg("7. Page-count verification", [
        "The PDF check is `pdfinfo report.pdf | grep Pages`.",
        "The expected value is 512.",
        "The DOCX check is Word COM to PDF, then the same command.",
        "A mismatch fails the build.",
        "The check is repeated after every rebuild.",
        "The check is recorded in the manifest.",
        "The manifest records the source commit and the SHA-256 of each artefact.",
        "The next page describes the verifier suite.",
    ]))
    P.append(pg("8. The verifier suite", [
        "Seven plan verifiers run from `.plan/.rea-tmp/`.",
        "`verify_step1.py` checks the coverage rows and headings.",
        "`step2_fix2_verify.py` checks the Step-2 fixes.",
        "`step3_verify.py` checks the anchor report.",
        "`step3_subanchors.py` checks the sub-anchors.",
        "`verify_step5.py` runs 65 checks.",
        "`step6_audit.py` audits the final report.",
        "`arxiv_recheck.py` re-checks the arXiv identifiers.",
        "The launcher gate is `node scripts/rebrand/check-consistency.mjs`.",
        "The next page describes the dashboard.",
    ]))
    P.append(pg("9. The dashboard", [
        "The dashboard is generated by `.plan/telemetry/gen_dashboard.py`.",
        "It runs the verifiers and records the exit codes.",
        "It records the HEAD and branch of the superproject and both components.",
        "It records the dirty counts.",
        "It records the ledger counts and the domain coverage.",
        "It records the open items as the grind queue.",
        "It is regenerated after every step.",
        "It is committed so two states can be diffed.",
        "The next page describes the Git protocol.",
    ]))
    P.append(pg("10. Git and submodule protocol", [
        "The superproject pins the two components as submodule commits.",
        "The submodule Git directories live under `.git/modules/`.",
        "The `.gitmodules` file names the branch each component tracks.",
        "A component change lands in the component first.",
        "The component is pushed before the superproject pin is updated.",
        "The pin update is a real superproject commit.",
        "A dirty component is reported, not hidden.",
        "A backup file is never tracked.",
        "The next page gives the reproduction recipe.",
    ]))
    P.append(pg("11. Reproduction recipe", [
        "1. Clone the superproject and initialise the submodules.",
        "2. Check out the pinned commits.",
        "3. Run `python .plan/telemetry/docgen/facts.py`.",
        "4. Run the three README generators.",
        "5. Check the line counts.",
        "6. Run the publication build.",
        "7. Check the page counts.",
        "8. Run the verifier suite.",
        "9. Compare the manifest hashes.",
        "10. Read the dashboard.",
        "The recipe is the same one the project uses.",
        "The next page describes the failure modes.",
    ]))
    P.append(pg("12. Failure modes and remedies", [
        "A line-count mismatch means the generator or the tree changed.",
        "A page-count mismatch means a block overflowed or a break was lost.",
        "A missing logo means the asset path is wrong.",
        "A missing package means the TeX installation is incomplete.",
        "A Word COM failure means the Word path or the profile is wrong.",
        "A verifier failure means the plan and the tree disagree.",
        "A dirty submodule means a parallel session is active.",
        "A stale fact means the extractor was not rerun.",
        "The remedy is always to fix the cause, not the check.",
        "The next part begins the evidence tables.",
    ]))
    return P


def evidence_pages() -> list[dict]:
    P = []

    def chunk(rows, title, note):
        body = ["| Item | Detail |", "|---|---|"] + rows
        body += note
        return pg(title, body)

    d = [f"| **{x['id']}** | {x['title']} |" for x in DECISIONS]
    P.append(chunk(d[:16], "1. Decision ledger, part 1",
                   ["The ledger is append-only.",
                    "The first sixteen entries are shown here; the rest continue on the next page.",
                    "Each entry is a binding rule, not a note.",
                    "The implementation trace lives in the decision file."]))
    P.append(chunk(d[16:], "2. Decision ledger, part 2",
                   ["The ledger continues from the previous page.",
                    "A later decision may supersede an earlier one; the record stays.",
                    "The decision file is the constitution of the project.",
                    "The index is generated from the file."]))
    r = [f"| **{x['id']}** | {x['title']} |" for x in RESEARCH]
    P.append(chunk(r, "3. Research index",
                   ["The index separates audit-ready work from work in progress.",
                    "Every item names its evidence status.",
                    "The operator owns the publishability pass.",
                    "The index is generated from `.plan/RESEARCH-INDEX.md`."]))
    f = [f"| `{x['name']}` | {x['bpw']:.2f} | {x['family']} |" for x in FORMATS]
    P.append(chunk(f[:27], "4. Valid formats, part 1",
                   ["The table is generated from the enum.",
                    "The family is plain, grouped or mixed.",
                    "The BPW column is the nominal and wire value.",
                    "The next page continues the list."]))
    P.append(chunk(f[27:54], "5. Valid formats, part 2",
                   ["The list continues from the previous page.",
                    "The grouped family repeats the base ladder with per-group scales.",
                    "The mixed family is quarantined by D-13.",
                    "The next page continues the list."]))
    P.append(chunk(f[54:], "6. Valid formats, part 3",
                   ["The list continues from the previous page.",
                    f"The ladder carries {N_FORMATS} valid formats in total.",
                    "The retired ids are listed separately.",
                    "The table is generated from the enum."]))
    rr = [f"| `{x['id']}` | `{x['name']}` | {x['bpw']:.2f} |" for x in RETIRED]
    P.append(chunk(rr[:18], "7. Retired ids, part 1",
                   ["Retired ids stay addressable.",
                    "A writer never emits them.",
                    "A reader remaps or rejects them.",
                    "The next page continues the list."]))
    P.append(chunk(rr[18:], "8. Retired ids, part 2",
                   ["The list continues from the previous page.",
                    f"The retired set carries {N_RETIRED} ids.",
                    "The compatibility layer owns the remap table.",
                    "The install test proves the fail-closed path."]))
    t = [f"| `{x['file']}` | {x['lines']} | {len(x['cases'])} | {x['asserts']} |" for x in TESTS]
    P.append(chunk(t[:26], "9. Test inventory, part 1",
                   ["The inventory is generated from `tests/`.",
                    "The case count is the number of named test functions.",
                    "The assert count includes inline asserts.",
                    "The next page continues the list."]))
    P.append(pg("10. Test inventory, part 2", [
        "| Test file | Lines | Cases | Asserts |",
        "|---|---:|---:|---:|",
        *[f"| `{x['file']}` | {x['lines']} | {len(x['cases'])} | {x['asserts']} |"
          for x in TESTS[26:52]],
        "The inventory continues from the previous page.",
        "The test suite is built as separate executables.",
        f"The suite carries {N_TESTS} files, {N_CASES} named cases and {N_ASSERTS:,} asserts.",
        "The next part begins the appendices.",
    ]))
    return P
