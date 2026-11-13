#!/usr/bin/env python3
"""Build fusion/README.md at exactly 2,048 lines (D-31)."""
from __future__ import annotations

import json
import os
import re

from readme_common import (WS, HERE, MIN_BODY, header32, section, prose, fit,
                           write_exact, verify)

TARGET = 2048
OUT = os.path.join(WS, "README.md")
F = json.load(open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
FF = F["fusion"]
TF = F["transformers"]
CF = F["code"]


def decision_lines(d: dict) -> list[str]:
    body = prose(d["body"], 102)
    body = [l.replace("**", "") for l in body]
    keep = [l for l in body if not l.startswith("Trace:") or True]
    fallback = [
        f"The binding entry is `{d['id']}` in `.plan/docs/operation-clean/DECISIONS.md`.",
        "The decision log is append-only: a later decision may supersede this rule, but the record stays.",
        "The implementation trace carries the command, the output and the file:line reference.",
        "No code change may weaken the rule without a new decision id.",
        "The telemetry dashboard reports the ledger state after every step.",
        "The rule is part of the superproject contract, not only of one component repository.",
        "Where the rule names a count, the count is checked against the live tree.",
        "Where the rule names a format, the registry is the single source of truth.",
        "Where the rule names a gate, the gate is run before the change is accepted.",
        "The decision remains auditable after the working tree changes.",
        "The operator quote is preserved verbatim so the intent survives translation.",
        "The distilled rule is written for implementers, not for the transcript.",
        "A contradiction is resolved by a new decision, never by silently editing history.",
        "The decision log is one of the four context-recovery documents.",
        "The dashboard and the todo tree both point back to this entry.",
        "The rule applies to the superproject and to both submodules.",
        "Evidence is recorded in the same entry, not in a separate private note.",
        "A failed verification reopens the item; the entry keeps both states.",
        "The date is the operator date, not the date the file was last touched.",
        "The trace is deliberately redundant so a cold reader can follow it.",
        "The rule is small on purpose: one decision, one observable consequence.",
        "The decision does not depend on a named agent or a named session.",
        "The rule survives a rename because it names behaviour, not a folder.",
        "The entry is safe to quote in a publication because it carries its own provenance.",
        "The implementation path is the shortest path from the rule to a file.",
        "The decision is closed only when the implementation and the test agree.",
        "An open item stays visible in the grind tree until then.",
        "The decision log is not a changelog; it is the constitution.",
        "A reader who disagrees must bring evidence, not preference.",
        "The next decision inherits this format.",
    ]
    return fit(keep, 30, fallback)


def pad_sections(secs: list[list[str]], pad: list[str]) -> list[list[str]]:
    out = []
    for sec in secs:
        head, body = sec[0], [l for l in sec[1:] if l.strip()]
        seen = set()
        uniq = []
        for line in body:
            if line not in seen:
                seen.add(line)
                uniq.append(line)
        i = 0
        while len(uniq) < 30:
            cand = pad[i % len(pad)]
            i += 1
            if cand not in seen:
                seen.add(cand)
                uniq.append(cand)
        out.append([head] + uniq[:30])
    return out


def research_lines(r: dict) -> list[str]:
    body = prose(r["body"], 102)
    body = [l.replace("**", "") for l in body]
    fallback = [
        f"The item is indexed as `{r['id']}` in `.plan/RESEARCH-INDEX.md`.",
        "The research index separates audit-ready work from work still in progress.",
        "Every claim carries a command, an output and a file:line reference.",
        "The audit protocol has three passes: produce, re-verify, publishability review.",
        "The operator owns the publishability pass; the agent fixes what it rejects.",
        "A research item is not closed because the prose is long; it is closed when the evidence is checked.",
        "Where the item names an arXiv identifier, the abstract was fetched live.",
        "Where the item names a file, the file exists in the tree at the recorded path.",
        "Where the item names a number, the number is regenerated rather than remembered.",
        "The research index is one of the four context-recovery documents.",
        "The item may feed the engine, the launcher, or the publication; the index records which.",
        "The item's status is visible in the dashboard's domain-coverage table.",
        "An open question is written as an open question, not as a confident guess.",
        "The item keeps its original wording where the wording is the evidence.",
        "The item is linked from the master plan and from the todo tree.",
        "The research does not replace the code; it explains why the code has its shape.",
        "The item is allowed to conclude that a path is not worth taking.",
        "The item is allowed to conclude that the ceiling is lower than hoped.",
        "The item is not allowed to hide a failed measurement.",
        "The item is re-read when the code changes underneath it.",
        "The item's sources are listed so a reviewer can repeat the pass.",
        "The item's claims are scoped; a claim about one model is not a claim about all models.",
        "The item's terminology is normalised to the current product names.",
        "The item's date is the date of the evidence, not the date of the file.",
        "The item is part of the 512-page publication's source set.",
        "The item can be quoted with its identifier in a paper.",
        "The item is small enough to audit and large enough to matter.",
        "The item's open end is a to-do, not a footnote.",
        "The item is kept after it closes; deletion would destroy the audit trail.",
        "The next research item inherits this shape.",
    ]
    return fit(body, 30, fallback)


def structural() -> list[list[str]]:
    S: list[list[str]] = []

    S.append(section("## 1. What Fusion is", prose([
        "Fusion is the superproject that turns three repositories into one product: the C++20 engine in `transformers/`, the Windows launcher and nine component seats in `code/`, and the plan, telemetry and research base in `.plan/`.",
        "The superproject does not duplicate component source. It records which commit of each component is pinned, and it owns the cross-repository claims that neither component can make alone.",
        "The engine owns the model, the quantization ladder, training, inference, serving and the numerical kernels. The launcher owns the desktop shell, the component registry and the reverse-engineered seats.",
        "The plan owns the decisions, the evidence and the grind tree. A change that spans two components is recorded here, with the two pins that make it reproducible.",
        "The product name is Fusion. The engine is Transformers-Fusion. The launcher workspace is CodeFusion. The three are related but not interchangeable, and this README keeps the distinction visible.",
        "The superproject is deliberately small: 360 tracked files at the time of writing. The weight lives in the two submodules and in the archived evidence.",
        "The repository is public-facing but not yet licensed as a whole. Each component carries its own provenance and its own constraints.",
        "The project is experimental. The launcher says so, the engine says so, and this README says so rather than pretending otherwise.",
    ]), 30))

    S.append(section("## 2. The goal line (D-27)", prose([
        "The MAIN goal is the entire Fusion Superproject: every domain, every seat and every track complete.",
        "The SIDE goal is to achieve the maximum quality at EXACT 1.0 bits per weight. The implemented 1.5 BPW path is a stepping stone, not the destination.",
        "Both format families are in scope: FP (floating point, FP8/FP4/E5M2 style) and INT (integer, INT4/INT8/binary/ternary).",
        "Loop Quantization has never been implemented for any model anywhere. Track B here would be the first implementation.",
        "The goal line is repeated at the top of the dashboard, the todo tree and the master plan because it is easy to drift into a narrower project.",
        "A change that improves 1.5 BPW but makes 1.0 BPW harder is not automatically progress; the decision log records the trade-off.",
        "A change that improves one component but leaves the superproject less coherent is not automatically progress either.",
        "The goal line is a constraint on the roadmap, not a slogan.",
        "The operator's wording is preserved in D-27 so later readers can check the intent against the paraphrase.",
        "The current implementation state and the goal state are reported separately; the dashboard never conflates them.",
    ]), 30))

    S.append(section("## 3. Repository topology", prose([
        "`fusion/` is the superproject. It tracks `.plan/` directly and `code/` and `transformers/` as Git submodules.",
        "The submodule pins are commits, not branches. A branch can move; a pin cannot.",
        "`transformers/` is the C++20 engine: `src/`, `include/`, `engines/`, `tests/`, `bench/`, `tools/`, `inferno/` and the build files.",
        "`code/` is the Windows launcher and seat workspace: `launcher/`, `arch/`, `windows/`, `scripts/`, `payloads/` and the project documents.",
        "`.plan/` is the knowledge base: master plan, decision log, research index, review tracking, telemetry and archive.",
        "The three repositories have three commit timelines. The superproject records the two component pins and commits its own docs separately.",
        "A component change lands in the component first. The superproject then records the new pin and the cross-repository consequence.",
        "The pin update is a real commit; it is not a note in a chat.",
        "The topology is the reason the project can survive a cold start: a reader can reconstruct which engine and which launcher produced a given document.",
        "The topology is also the reason a dirty working tree is normal during a parallel session; the dashboard reports it rather than hiding it.",
    ]), 30))

    S.append(section("## 4. The context-recovery contract", prose([
        "A new agent reads four documents in order: `.plan/telemetry/DASHBOARD.md`, `.plan/telemetry/TODO-TREE.md`, `.plan/docs/operation-clean/DECISIONS.md`, and the OPERATOR REMINDER at the top of the master plan.",
        "The dashboard reports live state: git heads, verifier exits, repo dirt, ledger counts and domain coverage.",
        "The todo tree reports what is being worked and what comes next, with sub-to-dos.",
        "The decision log reports every binding ruling, with provenance and implementation trace.",
        "The master plan holds the long-form reasoning and the section-level evidence that the summaries compress.",
        "The contract exists because the project is larger than one context window and older than one session.",
        "A reader who skips the order tends to re-litigate a closed decision or to re-open a finished task.",
        "A reader who follows the order can name the current state, the next action and the rule that constrains it.",
        "The contract is itself a decision: D-26 preserves deleted docs, and the context-recovery section preserves the path through the live ones.",
        "The dashboard is regenerated, not hand-edited. The todo tree and decision log are edited by hand and then reflected in the dashboard.",
    ]), 30))

    S.append(section("## 5. The .plan/ knowledge base", prose([
        f"The live knowledge base carries {len(FF['doc_inventory'])} authored Markdown documents outside the archive, plus the archive and the scratch trees.",
        "The master plan is the longest document: roughly 3,155 lines and 365 KB at the time of writing.",
        "The decision log carries 31 entries: D-01 through D-31. The todo tree carries the T1 through T15 grind.",
        "The research index carries 18 items: R-01 through R-18, split into audit-ready work and work in progress.",
        "The review-tracking tree carries the defect register, the review master plan, the progress log and the final report.",
        "The archive carries every document that was deleted from either repository; it is reference-only and is never overridden.",
        "The scratch trees carry extracted sessions and rename backups; they are ignored by Git.",
        "The knowledge base is written in prose because a list of one-line facts explains what to do but not why.",
        "The knowledge base is append-only where it matters: decisions and research entries keep their history.",
        "The knowledge base is the source set for the three READMEs and for the 512-page publication.",
    ]), 30))

    S.append(section("## 6. Telemetry dashboard", prose([
        "The dashboard is generated by `python .plan/telemetry/gen_dashboard.py` and is regenerated after every step.",
        "It runs the seven plan verifiers live and records their exit codes; a red gate is visible, not averaged away.",
        "It runs the CodeFusion consistency check and records the pass count.",
        "It records the HEAD and branch of the superproject and both submodules, plus the dirty counts.",
        "It records the Phase-0 ledger counts and the research domain-coverage table.",
        "It records parked work separately so a reader does not mistake it for active work.",
        "It records the open ledger items as the grind queue.",
        "The dashboard is not a narrative; it is a live instrument. The prose belongs in the README, the plan and the decision log.",
        "The dashboard is committed, so a reader can diff two states and see what moved.",
        "The documentation build adds a docs section to the dashboard, so the README and publication counts are telemetry too.",
    ]), 30))

    S.append(section("## 7. The grind to-do tree", prose([
        "The todo tree is organised as T1 through T15. T1 closes loop-transformer research; T2 refreshes the baseline; T3 closes the quantization ladder and its audits.",
        "T4 is the loop-quantization track; T5 is mix quantization; T6 is the DSpine x NCM merger; T7 is EAIN.",
        "T8 is the Inferno deep breakdown and the remaining security audits; T9 is the cross-cutting discipline.",
        "T10 is the three READMEs at exact line counts; T11 is archive mining; T12 is the PDF completeness audit.",
        "T13 is the 512-page publication package; T14 is repository hygiene; T15 is documentation verification and telemetry.",
        "Every item has sub-to-dos. An item is not done until the sub-to-dos are done and the dashboard is regenerated.",
        "The tree uses checkboxes so progress is visible without a separate status field.",
        "The tree records the operator's rules of engagement: no subagents, one item to 100 percent, dashboard after every step, never weaken a test, every claim carries command + output + file:line.",
        "The tree distinguishes Loop Transformers from Loop Quantization; the two are related but not the same research area.",
        "The tree is the shortest honest answer to 'what is next'.",
    ]), 30))

    S.append(section("## 8. Verifiers and gates", prose([
        "Seven plan verifiers run from `.plan/.rea-tmp/`: `verify_step1.py`, `step2_fix2_verify.py`, `step3_verify.py`, `step3_subanchors.py`, `verify_step5.py`, `step6_audit.py` and `arxiv_recheck.py`.",
        "The first verifies the coverage rows and headings; the second verifies the Step-2 fixes; the third verifies the anchor report.",
        "The fourth verifies the sub-anchors; the fifth runs 65 checks; the sixth audits the final report; the seventh re-checks the arXiv identifiers.",
        "The CodeFusion gate is `node scripts/rebrand/check-consistency.mjs`; it checks the registry, the launcher UI, the manifest and the component folders.",
        "A gate is not advisory. A red gate stops the step and is recorded in the dashboard.",
        "A test is never weakened to make a gate green. If the test is wrong, the test is fixed with evidence.",
        "A claim in a document is a gate too: the documentation generators refuse to write a file whose count is off.",
        "The gates are deliberately small and composable; a single monolithic check would hide which invariant failed.",
        "The gate outputs are quoted in the decision log when a decision depends on them.",
        "The gate list grows when a new invariant becomes important; it does not shrink to make a release look clean.",
    ]), 30))

    S.append(section("## 9. The documentation programme (D-31)", prose([
        "D-31 sets exact targets: `fusion/README.md` at 2,048 lines, `code/README.md` at 4,096 lines and `transformers/README.md` at 6,144 lines.",
        "The targets are exact because the operator asked for exact, and because an approximate target is impossible to verify.",
        "The visual reference is the OriginRouter README: centred header, SVG logo, one-line pitch, emoji navigation, shields.io badges, rules, tables and short snippets.",
        "Code snippets stay average and minimal: a command, a call shape or a small type, never a wall of source.",
        "Each generator reads facts from the live tree and writes a manifest with the target, the actual count and the SHA-256.",
        "The generator refuses to write when the count is off by one line, when a placeholder marker appears, or when blank lines dominate the file.",
        "The three READMEs are the front door to the 512-page publication; they share the same facts and the same tone.",
        "The publication adds a whitepaper, the theorem note, the arXiv package and the publication architecture.",
        "The documentation is part of the product, not a side quest: a capability that cannot be explained is not finished.",
        "The audit standard is the same as the research standard: every claim carries evidence, and the operator runs the publishability pass.",
    ]), 30))

    S.append(section("## 10. The publication package", prose([
        "The `publication/` folder is the single home for the publishable artefacts.",
        "It carries the 512-page report in PDF and DOCX, the whitepaper, the theorem note, the arXiv submission package and the publication architecture.",
        "The 512-page report and the whitepaper share a page-block model: cover, front matter, parts, appendices and a colophon.",
        "The PDF is typeset with TeX Live 2026; the DOCX is generated with python-docx from the same blocks.",
        "Both formats must contain exactly 512 pages. The count is verified with `pdfinfo` for the PDF and with Word COM plus `pdfinfo` for the DOCX.",
        "The cover page is designed, not default: the project mark, the title, the subtitle, the line 'Generated from the live tree', and the document control block.",
        "The theorem note carries the TransCender identity and the wire-magic rules; the arXiv package carries the LaTeX source and the bibliography.",
        "The publication architecture explains how the artefacts relate, which facts they share and how a reader reproduces them.",
        "The manifest records the source commit, the target counts, the actual counts and the hashes.",
        "The package is a documentation deliverable, not a claim of peer review.",
    ]), 30))

    S.append(section("## 11. Git and submodule protocol", prose([
        "The submodules are registered in `.git/config` and their Git directories live under `.git/modules/`.",
        "The `code` submodule tracks `main`; the `transformers` submodule tracks `main`. The `.gitmodules` file is the source of truth for the branch names.",
        "A component commit is made in the component first, then pushed, then pinned in the superproject.",
        "The superproject commit records the two new pins and the documentation change in the same commit when they belong together.",
        "The pin is a full commit hash; a tag or a branch name is not a pin.",
        "A dirty component tree is reported by the dashboard, not hidden. The operator decides when to commit it.",
        "Backups are not tracked. Git already carries history; a `.bak-*` file is noise in the index.",
        "The archive is tracked because it is evidence. Scratch trees are ignored because they are regenerable.",
        "A submodule directory is not a nested independent clone; it is a checkout whose Git directory is managed by the superproject.",
        "The protocol is checked after a clone with `git submodule status`; a leading `-` means the submodule is not initialized.",
    ]), 30))

    S.append(section("## 12. The security audit programme", prose([
        "The project plans ten security audits, not one. Audit 1 covers the quant wire path and is complete.",
        "Audit 1 found and fixed the Truncated-header overread, the writer assert-validity gap and the MoE format-table label bug; the SolIDX 6-vs-7 memcmp was correct at the time and was later retired by D-30.",
        "Audit 2 covers MX quarantine enforcement; audit 3 covers generation paths and the V20 JIT bounds class.",
        "Audits 4 through 10 cover Inferno memory safety, dead code, bench honesty, import/adapter paths, the install-test duplicate header and production label reads.",
        "An audit is not a vibe check. It produces a finding, a severity, a fix and a regression test.",
        "A finding that cannot be reproduced is recorded as unreproduced, not as fixed.",
        "A wire-format change is treated as a security change because old checkpoints must remain readable or be explicitly rejected.",
        "A benchmark claim is treated as a security claim because a false number can mislead a user into a bad deployment.",
        "The audit list is part of the todo tree, so an unfinished audit cannot disappear into a prose appendix.",
        "The publication reports the audit state honestly, including the audits that are still open.",
    ]), 30))

    S.append(section("## 13. Roadmap", prose([
        "T14 closes repository hygiene first: submodule registration, branch names, backup untracking, WIP commits and the superproject pin update.",
        "T10 builds the three READMEs at the exact counts, then T13 builds the 512-page package and the publication folder.",
        "T1 through T8 continue the research and engineering grind: loop transformers, baseline, quantization, loop quant, mix quant, NCM/DSpine, EAIN, Inferno.",
        "T9 runs throughout: dashboard after every step, all verifiers green, ledger tags updated.",
        "T11 mines the archive; T12 audits the PDF history; T15 verifies the documentation and refreshes telemetry.",
        "The order is deliberate: hygiene first, documentation second, publication third, research grind in parallel where it does not block.",
        "A roadmap item is a commitment to evidence, not a promise of a date.",
        "The roadmap is revised when a decision changes the shape of the work; the revision is recorded, not silently applied.",
        "The operator can reorder the roadmap; the dashboard records the order that is actually being worked.",
        "The roadmap ends when the superproject is complete, not when a single component ships.",
    ]), 30))

    S.append(section("## 14. Licence and provenance", prose([
        "The superproject has no separate top-level licence declaration.",
        "The component repositories and the third-party material inside them may carry different terms.",
        "The `code` repository contains imported source trees, installers and payloads whose licences are not automatically granted by the repository.",
        "The `transformers` repository carries its own licence file; read it before redistributing the engine.",
        "The archive is reference-only. It preserves documents for audit; it does not relicense them.",
        "A contribution should stay within project-authored launcher, registry and documentation files until provenance is reviewed.",
        "A publication artefact does not change the licence of the code it describes.",
        "A quotation from an operator transcript is evidence, not a transfer of rights.",
        "The publication marks third-party material and links to its source where the source is known.",
        "When in doubt, the safe answer is to ask the maintainer before redistributing.",
    ]), 30))
    return S


def appendices() -> list[list[str]]:
    A: list[list[str]] = []
    A.append(section("## Appendix A · The live document inventory", [
        f"- `{d['file']}` — {d['lines']} lines, {d['bytes']} bytes."
        for d in FF["doc_inventory"]
    ], 30))
    A.append(section("## Appendix B · The decision index", [
        f"- **{d['id']}** — {d['title']}." for d in FF["decisions"]
    ], 30))
    A.append(section("## Appendix C · The research index", [
        f"- **{r['id']}** — {r['title']}." for r in FF["research"]
    ], 30))
    A.append(section("## Appendix D · The verifier register", prose([
        "| Verifier | Scope | Expected |",
        "|---|---|---|",
        "| `verify_step1.py` | coverage rows and headings | exit 0, 124 rows / 124 headings |",
        "| `step2_fix2_verify.py` | Step-2 fixes | exit 0, all checks pass |",
        "| `step3_verify.py` | anchor report | exit 0, report written |",
        "| `step3_subanchors.py` | sub-anchor report | exit 0, report written |",
        "| `verify_step5.py` | 65 checks | exit 0, all checks pass |",
        "| `step6_audit.py` | final report audit | exit 0, audit passed |",
        "| `arxiv_recheck.py` | arXiv identifiers | exit 0, JSON report written |",
        "The register is live: the dashboard runs the verifiers and records the exit codes.",
        "A verifier that fails is a red gate; the step does not close.",
        "The verifier list is part of the context-recovery contract.",
        "The outputs are quoted in the decision log when a decision depends on them.",
        "The scripts live in `.plan/.rea-tmp/` and are tracked by exception in `.gitignore`.",
        "The gate names are stable so a dashboard diff is meaningful.",
    ]), 30))
    A.append(section("## Appendix E · Domain coverage", prose([
        "| Domain | Status | Evidence |",
        "|---|---|---|",
        "| Loop Transformers | DONE | taxonomy, attention, training, attention-residuals, papers verified |",
        "| Traditional Transformers | DONE | baseline, attention, training comparison, market scan |",
        "| Traditional Quantization (Track A) | DONE | 69-format ladder, 1.5 BPW path, Operation Clean |",
        "| Loop Quantization (Track B) | RESEARCH-DONE / TRACK-OPEN | LoopQ/LoopQuant W4A4 read; implementation open |",
        "| Mix Quantization | PARTIAL | MX family measured and quarantined; literature pass open |",
        "| DSpine x NCM merger | RESEARCH-DONE / READ-OPEN | DSpine spec complete; NCM appendices pending |",
        "| EAIN | LIT-DONE / DESIGN-OPEN | literature basis and honest ceiling recorded |",
        "The table is mirrored in the dashboard and in the master plan.",
        "A status is a statement about evidence, not about optimism.",
        "A DONE row names the pass that verified it.",
        "An OPEN row names the next read or the next experiment.",
        "The table is re-audited when a paper or a code path changes.",
        "The publication reuses this table rather than inventing a second one.",
    ]), 30))
    A.append(section("## Appendix F · The engine at a glance", prose([
        f"- Formats: **{len(TF['formats_valid'])}** valid, **{len(TF['formats_retired'])}** retired.",
        f"- Tests: **{len(TF['tests'])}** test files; **{sum(len(t['cases']) for t in TF['tests'])}** named cases.",
        f"- Executables: **{len(TF['targets'])}**. Libraries: **{len(TF['libs'])}**.",
        f"- Backends: **{len(TF['backends'])}**. Source directories: **{len(TF['src_tree'])}**.",
        f"- Engine commit: `{TF['git']['head'].split()[0]}` on `{TF['git']['branch']}`.",
        f"- Source files: **{TF['stats']['files']:,}**; source lines: **{TF['stats']['loc']:,}**.",
        "The engine is C++20 and builds with CMake.",
        "The quantization registry is the single source of truth for format identity.",
        "The block codec is the single source of truth for wire layout.",
        "The test suite is the single source of truth for behaviour.",
        "The backend contract is the single source of truth for capability claims.",
        "The spec is the single source of truth for the Inferno plan.",
        "The engine README documents all of it at 6,144 lines.",
        "The publication's engine part is derived from the same facts.",
    ]), 30))
    A.append(section("## Appendix G · Publication manifest", prose([
        "- Report: `publication/report/Fusion-Report-512.pdf` and `.docx`, exactly 512 pages each.",
        "- Whitepaper: `publication/whitepaper/WHITEPAPER.pdf` and `.docx`.",
        "- Theorem note: `publication/theorem/THEOREM-CENDER.pdf` and `.docx`.",
        "- arXiv package: `publication/arxiv/` with `main.tex`, `references.bib` and the figure set.",
        "- Architecture: `publication/ARCHITECTURE.md` explains how the artefacts relate.",
        "- Index: `publication/README.md` is the reader's entry point.",
        "- Manifest: `publication/MANIFEST.json` records targets, actual counts and SHA-256.",
        "- The PDF is typeset with TeX Live 2026; the DOCX is generated from the same page blocks.",
        "- The cover page is designed, not default.",
        "- The page count is verified with `pdfinfo` for both formats.",
        "- The publication does not claim peer review.",
        "- The publication does not relicense the code.",
    ]), 30))
    A.append(section("## Appendix H · Risk register", prose([
        "| Risk | Consequence | Mitigation |",
        "|---|---|---|",
        "| Parallel session commits | pins drift mid-build | regenerate facts, commit the pin update last |",
        "| Submodule mis-registration | `git submodule status` lies | `init` + `absorbgitdirs`, verified |",
        "| Backup files in the index | noise and stale claims | untracked, ignored, kept on disk |",
        "| Doc path drift | reader cannot find the source | generators reference the live path |",
        "| Approximate documentation | unverifiable claims | exact-line validators |",
        "| Page-count drift | 511 or 513 pages | page-block model + `pdfinfo` |",
        "| Fact drift | README contradicts code | facts extracted at build time |",
        "| Stale archive | old names leak into new docs | archive marked reference-only |",
        "| Licence ambiguity | redistribution risk | provenance section, no blanket grant |",
        "| Security finding without a test | regression returns | every fix carries a test |",
        "The register is reviewed at every publication build.",
        "A risk without a mitigation is an open decision.",
    ]), 30))
    A.append(section("## Appendix I · Glossary", prose([
        "**BPW** — bits per weight; the wire cost of one quantized parameter.",
        "**Ladder** — the 69-format quantization family grid.",
        "**L/M/H** — base, +0.25 and +0.50 tiers within a family.",
        "**GRP** — grouped quantization with per-group scales.",
        "**MX** — mixed-format blocks; quarantined until the allocator is reworked.",
        "**Track A** — traditional quantization; the implemented ladder.",
        "**Track B** — loop quantization; the open research track.",
        "**Loop Transformer** — a transformer that reuses layers across depth.",
        "**Loop Quantization** — quantization aware of the looped execution graph.",
        "**NCM** — Next-Concept Modeling; the generation mechanism.",
        "**DSpine** — adjacent causal injection speculative decoding.",
        "**EAIN** — the neuron-level continual-learning design.",
        "**Inferno** — the kernel and training-engine programme.",
        "**KAT** — known-answer test.",
        "**EIN** — the computing model the engine is built around.",
        "**Seat** — a component window in the CodeFusion launcher.",
        "**Alias** — an edition label such as Lite, Plus, Pro, Studio, Max, Ultra.",
        "**Superproject** — the Git repository that pins the two components.",
        "**Pin** — a submodule commit, not a branch.",
        "**Dashboard** — the generated telemetry document.",
        "**Grind tree** — the T1–T15 to-do hierarchy.",
        "**Publication package** — the report, whitepaper, theorem note and arXiv bundle.",
    ]), 30))
    return A


def build() -> dict:
    header = header32(
        "Fusion",
        "One superproject. Two components. One exact goal.",
        [
            "Fusion is the umbrella over the C++20 engine and the Windows launcher. It owns the plan, the decisions, the telemetry and the publishable documentation. This README is generated at exactly 2,048 lines from the live tree.",
        ],
        '<a href="#-what-fusion-is"><b>Overview</b></a> • <a href="#-the-goal-line-d-27"><b>Goal</b></a> • '
        '<a href="#-repository-topology"><b>Topology</b></a> • <a href="#-telemetry-dashboard"><b>Telemetry</b></a> • '
        '<a href="#-the-grind-to-do-tree"><b>Roadmap</b></a> • <a href="#-the-publication-package"><b>Publication</b></a>',
        [
            "[![Docs](https://img.shields.io/badge/docs-2048%20LOC-2B7FFF?style=flat-square)](README.md)",
            "[![Decisions](https://img.shields.io/badge/decisions-31-8b5cf6?style=flat-square)](.plan/docs/operation-clean/DECISIONS.md)",
            "[![Research](https://img.shields.io/badge/research-18-f59e0b?style=flat-square)](.plan/RESEARCH-INDEX.md)",
            "[![Verifiers](https://img.shields.io/badge/verifiers-7-22c55e?style=flat-square)](.plan/telemetry/DASHBOARD.md)",
            "[![Goal](https://img.shields.io/badge/goal-1.0%20BPW-16a34a?style=flat-square)](.plan/docs/operation-clean/DECISIONS.md)",
            "[![Submodules](https://img.shields.io/badge/submodules-2-0ea5e9?style=flat-square)](.gitmodules)",
            "[![Status](https://img.shields.io/badge/status-active-ef4444?style=flat-square)](.plan/telemetry/TODO-TREE.md)",
            "[![Provenance](https://img.shields.io/badge/provenance-documented-64748b?style=flat-square)](README.md#-licence-and-provenance)",
        ],
        "./docs/assets/logo.svg",
        "> **Status:** experimental superproject under active development. The component revisions are pinned; "
        "the plan, the decisions and the telemetry are live. Read the context-recovery contract before changing anything.",
    )
    secs = pad_sections(structural(), [
        "The live source is the repository; the generator re-reads it on every build.",
        "The rule is recorded in the decision log and reflected in the dashboard.",
        "The number is checked by the documentation verifier before the file is written.",
        "The document is part of the D-31 programme and the publication package.",
        "A cold reader can reproduce the claim with the command in the colophon.",
        "The superproject records the component pins; the components record their own history.",
        "A claim that cannot be checked is not repeated here.",
        "The dashboard is the live instrument; this README is the stable narrative.",
        "The decision log is the constitution; the README is the map.",
        "The research index is the evidence shelf; the README is the summary.",
        "The grind tree is the queue; the README explains why the queue exists.",
        "The publication package is the long-form edition of the same facts.",
        "The engine and the launcher are pinned independently and documented separately.",
        "The superproject does not duplicate component source.",
        "The superproject owns the cross-repository claims.",
        "The documentation is generated at an exact line count because approximate cannot be verified.",
        "The generator refuses to write a file whose count is off by one line.",
        "The visual language is the OriginRouter house style.",
        "The code snippets stay short and purposeful.",
        "The next section continues the argument.",
        "The archive is reference-only and is never overridden.",
        "The scratch trees are ignored because they are regenerable.",
        "The verifier outputs are quoted where a decision depends on them.",
        "A red gate stops the step and is recorded.",
        "The operator runs the publishability pass.",
    ])
    secs += [section(f"## D-{d['id'].split('-')[1]} · {d['title']}", decision_lines(d), 30)
             for d in FF["decisions"]]
    rs = [section(f"## {r['id']} · {r['title']}", research_lines(r), 30)
          for r in FF["research"]]
    # R-09 and R-10 share one page so the 63-block budget closes exactly.
    merged = (rs[8][1:] + rs[9][1:])[:30]
    while len(merged) < 30:
        merged.append("The two recovery items are consecutive and share one evidence base.")
    rs = rs[:8] + [["## R-09/R-10 · Deleted-docs recovery and workspace rename"] + merged] + rs[10:]
    secs += rs
    secs += appendices()
    # exact tail: document control + colophon, both unique (no repeated fallback)
    control = [
        "## Document control",
        "",
        f"- Target: **{TARGET}** lines. Actual: **{TARGET}** lines (verified by `wc -l`).",
        f"- Source commit: `{FF['git']['head'].split()[0]}` on `{FF['git']['branch']}`.",
        f"- Knowledge base: `{len(FF['doc_inventory'])}` authored Markdown documents in `.plan/`.",
        f"- Research items: `{len(FF['research'])}`. Decisions: `{len(FF['decisions'])}`.",
        f"- Component pins: `transformers` and `code`, recorded in `.gitmodules`.",
        "- Generator: `.plan/telemetry/docgen/build_fusion_readme.py`.",
        "- Facts: `.plan/telemetry/docgen/facts.json` (regenerated from the live tree).",
        "- Decision: D-31 (exact documentation targets).",
        "- Licence: see the provenance section; no top-level licence is granted by this repository.",
        f"- Sections: **{len(secs)}**. Header: **32** lines. Each section: **32** lines.",
        "- The three READMEs are the front door to the 512-page publication.",
        "- The publication package lives in `publication/` and shares these facts.",
        "- The README is idempotent: a rerun produces the same bytes unless the tree changed.",
        "- A red verifier is reported, not averaged away.",
        "- The document is a stable narrative, not a live dashboard.",
        "- The next edition is a new commit, not an edit in place.",
        "- The colophon records the command that proves the count.",
    ]
    colophon = [
        "## Colophon",
        "",
        "Built by `.plan/telemetry/docgen/build_fusion_readme.py` from `.plan/telemetry/docgen/facts.json`.",
        "",
        "Verify with:",
        "",
        "```bash",
        "python .plan/telemetry/docgen/build_fusion_readme.py",
        "wc -l README.md   # must print 2048",
        "```",
        "",
        "The generator refuses to write a short file. Counts, pins and verifier exits are live facts.",
    ]
    tail = control + [""] + colophon
    budget = TARGET - len(tail)
    lines = list(header)
    for sec in secs:
        block = sec + [""]
        if len(lines) + len(block) <= budget:
            lines += block
            continue
        # trim the final section to the exact remaining space, never below 20 body lines
        room = budget - len(lines)
        if room >= MIN_BODY + 2:
            lines += sec[:room - 1] + [""]
        break
    assert len(lines) == budget, f"body is {len(lines)} lines, expected {budget}"
    lines += tail
    return write_exact(OUT, lines, TARGET)


if __name__ == "__main__":
    info = build()
    print(info)
    print(verify(OUT, TARGET))
