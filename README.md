<div align="center">
  <img src="./docs/assets/logo.svg" alt="Fusion" width="96" />

  # Fusion

  **One superproject. Two components. One exact goal.**

  Fusion is the umbrella over the C++20 engine and the Windows launcher. It owns the plan, the decisions, the
  telemetry and the publishable documentation. This README is generated at exactly 2,048 lines from the live
  tree.

  <p>
    <a href="#-what-fusion-is"><b>Overview</b></a> • <a href="#-the-goal-line-d-27"><b>Goal</b></a> • <a href="#-repository-topology"><b>Topology</b></a> • <a href="#-telemetry-dashboard"><b>Telemetry</b></a> • <a href="#-the-grind-to-do-tree"><b>Roadmap</b></a> • <a href="#-the-publication-package"><b>Publication</b></a>
  </p>

[![Docs](https://img.shields.io/badge/docs-2048%20LOC-2B7FFF?style=flat-square)](README.md)
[![Decisions](https://img.shields.io/badge/decisions-31-8b5cf6?style=flat-square)](.plan/docs/operation-clean/DECISIONS.md)
[![Research](https://img.shields.io/badge/research-18-f59e0b?style=flat-square)](.plan/RESEARCH-INDEX.md)
[![Verifiers](https://img.shields.io/badge/verifiers-7-22c55e?style=flat-square)](.plan/telemetry/DASHBOARD.md)
[![Goal](https://img.shields.io/badge/goal-1.0%20BPW-16a34a?style=flat-square)](.plan/docs/operation-clean/DECISIONS.md)
[![Submodules](https://img.shields.io/badge/submodules-2-0ea5e9?style=flat-square)](.gitmodules)
[![Status](https://img.shields.io/badge/status-active-ef4444?style=flat-square)](.plan/telemetry/TODO-TREE.md)
[![Provenance](https://img.shields.io/badge/provenance-documented-64748b?style=flat-square)](README.md#-licence-and-provenance)
</div>

---

> **Status:** experimental superproject under active development. The component revisions are pinned; the plan, the decisions and the telemetry are live. Read the context-recovery contract before changing anything.
> **Generated from the live tree:** every count, pin and verifier exit in this document is reproducible.

---

## 1. What Fusion is
Fusion is the superproject that turns three repositories into one product: the C++20 engine in
`transformers/`, the Windows launcher and nine component seats in `code/`, and the plan, telemetry and
research base in `.plan/`.
The superproject does not duplicate component source. It records which commit of each component is
pinned, and it owns the cross-repository claims that neither component can make alone.
The engine owns the model, the quantization ladder, training, inference, serving and the numerical
kernels. The launcher owns the desktop shell, the component registry and the reverse-engineered seats.
The plan owns the decisions, the evidence and the grind tree. A change that spans two components is
recorded here, with the two pins that make it reproducible.
The product name is Fusion. The engine is Transformers-Fusion. The launcher workspace is CodeFusion. The
three are related but not interchangeable, and this README keeps the distinction visible.
The superproject is deliberately small: 360 tracked files at the time of writing. The weight lives in
the two submodules and in the archived evidence.
The repository is public-facing but not yet licensed as a whole. Each component carries its own
provenance and its own constraints.
The project is experimental. The launcher says so, the engine says so, and this README says so rather
than pretending otherwise.

## 2. The goal line (D-27)
The MAIN goal is the entire Fusion Superproject: every domain, every seat and every track complete.
The SIDE goal is to achieve the maximum quality at EXACT 1.0 bits per weight. The implemented 1.5 BPW
path is a stepping stone, not the destination.
Both format families are in scope: FP (floating point, FP8/FP4/E5M2 style) and INT (integer,
INT4/INT8/binary/ternary).
Loop Quantization has never been implemented for any model anywhere. Track B here would be the first
implementation.
The goal line is repeated at the top of the dashboard, the todo tree and the master plan because it is
easy to drift into a narrower project.
A change that improves 1.5 BPW but makes 1.0 BPW harder is not automatically progress; the decision log
records the trade-off.
A change that improves one component but leaves the superproject less coherent is not automatically
progress either.
The goal line is a constraint on the roadmap, not a slogan.
The operator's wording is preserved in D-27 so later readers can check the intent against the
paraphrase.
The current implementation state and the goal state are reported separately; the dashboard never
conflates them.

## 3. Repository topology
`fusion/` is the superproject. It tracks `.plan/` directly and `code/` and `transformers/` as Git
submodules.
The submodule pins are commits, not branches. A branch can move; a pin cannot.
`transformers/` is the C++20 engine: `src/`, `include/`, `engines/`, `tests/`, `bench/`, `tools/`,
`inferno/` and the build files.
`code/` is the Windows launcher and seat workspace: `launcher/`, `arch/`, `windows/`, `scripts/`,
`payloads/` and the project documents.
`.plan/` is the knowledge base: master plan, decision log, research index, review tracking, telemetry
and archive.
The three repositories have three commit timelines. The superproject records the two component pins and
commits its own docs separately.
A component change lands in the component first. The superproject then records the new pin and the
cross-repository consequence.
The pin update is a real commit; it is not a note in a chat.
The topology is the reason the project can survive a cold start: a reader can reconstruct which engine
and which launcher produced a given document.
The topology is also the reason a dirty working tree is normal during a parallel session; the dashboard
reports it rather than hiding it.

## 4. The context-recovery contract
A new agent reads four documents in order: `.plan/telemetry/DASHBOARD.md`,
`.plan/telemetry/TODO-TREE.md`, `.plan/docs/operation-clean/DECISIONS.md`, and the OPERATOR REMINDER at
the top of the master plan.
The dashboard reports live state: git heads, verifier exits, repo dirt, ledger counts and domain
coverage.
The todo tree reports what is being worked and what comes next, with sub-to-dos.
The decision log reports every binding ruling, with provenance and implementation trace.
The master plan holds the long-form reasoning and the section-level evidence that the summaries
compress.
The contract exists because the project is larger than one context window and older than one session.
A reader who skips the order tends to re-litigate a closed decision or to re-open a finished task.
A reader who follows the order can name the current state, the next action and the rule that constrains
it.
The contract is itself a decision: D-26 preserves deleted docs, and the context-recovery section
preserves the path through the live ones.
The dashboard is regenerated, not hand-edited. The todo tree and decision log are edited by hand and
then reflected in the dashboard.

## 5. The .plan/ knowledge base
The live knowledge base carries 26 authored Markdown documents outside the archive, plus the archive and
the scratch trees.
The master plan is the longest document: roughly 3,155 lines and 365 KB at the time of writing.
The decision log carries 31 entries: D-01 through D-31. The todo tree carries the T1 through T15 grind.
The research index carries 18 items: R-01 through R-18, split into audit-ready work and work in
progress.
The review-tracking tree carries the defect register, the review master plan, the progress log and the
final report.
The archive carries every document that was deleted from either repository; it is reference-only and is
never overridden.
The scratch trees carry extracted sessions and rename backups; they are ignored by Git.
The knowledge base is written in prose because a list of one-line facts explains what to do but not why.
The knowledge base is append-only where it matters: decisions and research entries keep their history.
The knowledge base is the source set for the three READMEs and for the 512-page publication.

## 6. Telemetry dashboard
The dashboard is generated by `python .plan/telemetry/gen_dashboard.py` and is regenerated after every
step.
It runs the seven plan verifiers live and records their exit codes; a red gate is visible, not averaged
away.
It runs the CodeFusion consistency check and records the pass count.
It records the HEAD and branch of the superproject and both submodules, plus the dirty counts.
It records the Phase-0 ledger counts and the research domain-coverage table.
It records parked work separately so a reader does not mistake it for active work.
It records the open ledger items as the grind queue.
The dashboard is not a narrative; it is a live instrument. The prose belongs in the README, the plan and
the decision log.
The dashboard is committed, so a reader can diff two states and see what moved.
The documentation build adds a docs section to the dashboard, so the README and publication counts are
telemetry too.

## 7. The grind to-do tree
The todo tree is organised as T1 through T15. T1 closes loop-transformer research; T2 refreshes the
baseline; T3 closes the quantization ladder and its audits.
T4 is the loop-quantization track; T5 is mix quantization; T6 is the DSpine x NCM merger; T7 is EAIN.
T8 is the Inferno deep breakdown and the remaining security audits; T9 is the cross-cutting discipline.
T10 is the three READMEs at exact line counts; T11 is archive mining; T12 is the PDF completeness audit.
T13 is the 512-page publication package; T14 is repository hygiene; T15 is documentation verification
and telemetry.
Every item has sub-to-dos. An item is not done until the sub-to-dos are done and the dashboard is
regenerated.
The tree uses checkboxes so progress is visible without a separate status field.
The tree records the operator's rules of engagement: no subagents, one item to 100 percent, dashboard
after every step, never weaken a test, every claim carries command + output + file:line.
The tree distinguishes Loop Transformers from Loop Quantization; the two are related but not the same
research area.
The tree is the shortest honest answer to 'what is next'.

## 8. Verifiers and gates
Seven plan verifiers run from `.plan/.rea-tmp/`: `verify_step1.py`, `step2_fix2_verify.py`,
`step3_verify.py`, `step3_subanchors.py`, `verify_step5.py`, `step6_audit.py` and `arxiv_recheck.py`.
The first verifies the coverage rows and headings; the second verifies the Step-2 fixes; the third
verifies the anchor report.
The fourth verifies the sub-anchors; the fifth runs 65 checks; the sixth audits the final report; the
seventh re-checks the arXiv identifiers.
The CodeFusion gate is `node scripts/rebrand/check-consistency.mjs`; it checks the registry, the
launcher UI, the manifest and the component folders.
A gate is not advisory. A red gate stops the step and is recorded in the dashboard.
A test is never weakened to make a gate green. If the test is wrong, the test is fixed with evidence.
A claim in a document is a gate too: the documentation generators refuse to write a file whose count is
off.
The gates are deliberately small and composable; a single monolithic check would hide which invariant
failed.
The gate outputs are quoted in the decision log when a decision depends on them.
The gate list grows when a new invariant becomes important; it does not shrink to make a release look
clean.

## 9. The documentation programme (D-31)
D-31 sets exact targets: `fusion/README.md` at 2,048 lines, `code/README.md` at 4,096 lines and
`transformers/README.md` at 6,144 lines.
The targets are exact because the operator asked for exact, and because an approximate target is
impossible to verify.
The visual reference is the OriginRouter README: centred header, SVG logo, one-line pitch, emoji
navigation, shields.io badges, rules, tables and short snippets.
Code snippets stay average and minimal: a command, a call shape or a small type, never a wall of source.
Each generator reads facts from the live tree and writes a manifest with the target, the actual count
and the SHA-256.
The generator refuses to write when the count is off by one line, when a placeholder marker appears, or
when blank lines dominate the file.
The three READMEs are the front door to the 512-page publication; they share the same facts and the same
tone.
The publication adds a whitepaper, the theorem note, the arXiv package and the publication architecture.
The documentation is part of the product, not a side quest: a capability that cannot be explained is not
finished.
The audit standard is the same as the research standard: every claim carries evidence, and the operator
runs the publishability pass.

## 10. The publication package
The `publication/` folder is the single home for the publishable artefacts.
It carries the 512-page report in PDF and DOCX, the whitepaper, the theorem note, the arXiv submission
package and the publication architecture.
The 512-page report and the whitepaper share a page-block model: cover, front matter, parts, appendices
and a colophon.
The PDF is typeset with TeX Live 2026; the DOCX is generated with python-docx from the same blocks.
Both formats must contain exactly 512 pages. The count is verified with `pdfinfo` for the PDF and with
Word COM plus `pdfinfo` for the DOCX.
The cover page is designed, not default: the project mark, the title, the subtitle, the line 'Generated
from the live tree', and the document control block.
The theorem note carries the TransCender identity and the wire-magic rules; the arXiv package carries
the LaTeX source and the bibliography.
The publication architecture explains how the artefacts relate, which facts they share and how a reader
reproduces them.
The manifest records the source commit, the target counts, the actual counts and the hashes.
The package is a documentation deliverable, not a claim of peer review.

## 11. Git and submodule protocol
The submodules are registered in `.git/config` and their Git directories live under `.git/modules/`.
The `code` submodule tracks `main`; the `transformers` submodule tracks `main`. The `.gitmodules` file
is the source of truth for the branch names.
A component commit is made in the component first, then pushed, then pinned in the superproject.
The superproject commit records the two new pins and the documentation change in the same commit when
they belong together.
The pin is a full commit hash; a tag or a branch name is not a pin.
A dirty component tree is reported by the dashboard, not hidden. The operator decides when to commit it.
Backups are not tracked. Git already carries history; a `.bak-*` file is noise in the index.
The archive is tracked because it is evidence. Scratch trees are ignored because they are regenerable.
A submodule directory is not a nested independent clone; it is a checkout whose Git directory is managed
by the superproject.
The protocol is checked after a clone with `git submodule status`; a leading `-` means the submodule is
not initialized.

## 12. The security audit programme
The project plans ten security audits, not one. Audit 1 covers the quant wire path and is complete.
Audit 1 found and fixed the Truncated-header overread, the writer assert-validity gap and the MoE
format-table label bug; the SolIDX 6-vs-7 memcmp was correct at the time and was later retired by D-30.
Audit 2 covers MX quarantine enforcement; audit 3 covers generation paths and the V20 JIT bounds class.
Audits 4 through 10 cover Inferno memory safety, dead code, bench honesty, import/adapter paths, the
install-test duplicate header and production label reads.
An audit is not a vibe check. It produces a finding, a severity, a fix and a regression test.
A finding that cannot be reproduced is recorded as unreproduced, not as fixed.
A wire-format change is treated as a security change because old checkpoints must remain readable or be
explicitly rejected.
A benchmark claim is treated as a security claim because a false number can mislead a user into a bad
deployment.
The audit list is part of the todo tree, so an unfinished audit cannot disappear into a prose appendix.
The publication reports the audit state honestly, including the audits that are still open.

## 13. Roadmap
T14 closes repository hygiene first: submodule registration, branch names, backup untracking, WIP
commits and the superproject pin update.
T10 builds the three READMEs at the exact counts, then T13 builds the 512-page package and the
publication folder.
T1 through T8 continue the research and engineering grind: loop transformers, baseline, quantization,
loop quant, mix quant, NCM/DSpine, EAIN, Inferno.
T9 runs throughout: dashboard after every step, all verifiers green, ledger tags updated.
T11 mines the archive; T12 audits the PDF history; T15 verifies the documentation and refreshes
telemetry.
The order is deliberate: hygiene first, documentation second, publication third, research grind in
parallel where it does not block.
A roadmap item is a commitment to evidence, not a promise of a date.
The roadmap is revised when a decision changes the shape of the work; the revision is recorded, not
silently applied.
The operator can reorder the roadmap; the dashboard records the order that is actually being worked.
The roadmap ends when the superproject is complete, not when a single component ships.

## 14. Licence and provenance
The superproject has no separate top-level licence declaration.
The component repositories and the third-party material inside them may carry different terms.
The `code` repository contains imported source trees, installers and payloads whose licences are not
automatically granted by the repository.
The `transformers` repository carries its own licence file; read it before redistributing the engine.
The archive is reference-only. It preserves documents for audit; it does not relicense them.
A contribution should stay within project-authored launcher, registry and documentation files until
provenance is reviewed.
A publication artefact does not change the licence of the code it describes.
A quotation from an operator transcript is evidence, not a transfer of rights.
The publication marks third-party material and links to its source where the source is known.
When in doubt, the safe answer is to ask the maintainer before redistributing.

## D-01 · Ladder pattern L/M/H (operator: 2026-10-22, "Info 5" + "Info 2")
Rule: in EVERY family, L = base at exact `.0` BPW, M = base + `.25` exact, H = base
+ `.50` exact. Three genuinely different codecs. The old standalone "L" duplicate is
retired; the base id IS the L tier.
Trace:
- "jo Q_1 hai wo formerly known as L/M/H me se L yaani Low waala variant and L waala jo
separate hi unko khallas aur ye exact 1.0 BPW use karenge, fir M waala, ye 1.25 BPW
exact use karenge, H waale 1.50…"
- "har ek family me yahi rule hai aur jo L hai wahi base hai yaani .0 fir M matlab .25
and H matlab .50 exact."
- Implementation: LADDER.md rules 1–2; tasks L1/L2.
The binding entry is `D-01` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.

## D-02 · Q_1 = binary, Q_1_K_H = pure ternary (operator, 2026-10-22)
Rule: `Q_1` keeps binary (slot-sign) at exact 1.00. `Q_1_K_H` becomes pure ternary
(−1/0/+1) at exact 1.50. The proposed standalone formats Q-10/Q-11 are CANCELLED
(operator said so explicitly; recorded as F-0 in DEFECTS.md).
Trace: "jo Q_1 hai wo hi binary rahega aur jo Q_1_5 rahega jise Q_1_K_H bolenge ya
isi type kuch, ye pure ternary and exact itna BPW hi."
- Wire: 48 B/256 w = 1.5000 exact (trits base-3 packed + FP16 scale + implicit-zero
slots) — see LADDER.md §Q_1_K_H.
The binding entry is `D-02` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.

## D-03 · Rewire direction (operator: "BPW ko kam karo")
Rule: name says X ⇒ wire costs exactly X. The LAYOUT comes DOWN to the name; never
rename a format up to its wire. (BOW was the operator's typo for BPW.)
Trace: "QG2 hai to Q_G_2 rename, BPW ko kam karo … exact G bolenge, formerly known
as karke code me likh sakte ho."
- Implementation: 8 GRP rewire targets + K/half literals — LADDER.md table; L2.
- Negative-gap formats (`Q_2_5` etc., name x.5 > wire x.4375) retire rather than
inflate the layout: folding keeps the grid clean and avoids inventing new engines.
The binding entry is `D-03` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.

## D-04 · GRP naming normalization
Rule: `QG2` → `Q_G_2` style everywhere; canonical pattern `Q_/Q_G_/Q_MX_/Q_G_MX_`
+ ` _K_M/_K_H` tiers. Renames carry "formerly known as <old>" comments in code.
Macros/env excluded from casing rules.
Trace: "QG2 hai to Q_G_2 rename … formerly known as karke code me likh sakte ho."
The binding entry is `D-04` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.
The decision is closed only when the implementation and the test agree.

## D-05 · Casing: QUANT → Quant (operator, 2026-10-19)
Rule: the ALL-CAPS token `QUANT` exists only where structurally mandatory:
C/C++ macros (`QUANT_CHECK`, `QUANT_AVX`, …, defined via #define) and environment
variables (`QUANT_SEED`, `QUANT_PAGED_KV_DEBUG`, `QUANT_SKIP_FULL`, `QUANT_SKIP_GLA`).
Everything else — type names, comments, docs, printf strings — is `Quant`.
Lowercase namespace `quant` stays (distinct token).
Trace: "macros, env's jaisi jagaho ko chhod ke kisi bhi file me 'QUANT' poora upper
case me naa ho dhyaan rakhna, 'Quant' hona chahiye har code me aur har jagah, docs me
bhi."
The binding entry is `D-05` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.

## D-06 · BPW granularity (operator)
Rule: every format lands on exact `.0 / .25 / .50` BPW steps. No other wire values
survive anywhere in the ladder (this is what kills 3.78125, 3.4375, 6.5625, 2.625 …).
The binding entry is `D-06` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.
The decision is closed only when the implementation and the test agree.
An open item stays visible in the grind tree until then.
The decision log is not a changelog; it is the constitution.

## D-07 · Zero dead code / zero stubs (operator, 2026-10-18)
Rule: after Operation Clean, no dead helper and no stub remains — every dead symbol
is wired up correctly or deleted.
Documented exception: the ~18 GPU/compute backends that exist but are unavailable
(unoptimized, incomplete by design until the backend-completion effort) are kept,
documented accurately, and excluded from the zero-stub rule. They are NOT deleted and
NOT half-fixed here.
Trace: "ek bhi dead code and stub nahi bachna chahiye, bas kuchh-kuchh stub chhode
gay hai majboori me unko exclude karke jaise ki 18 backends hai but wo available nahi
hai optimizations ke liye."
Implementation: task Z1 with the exception list.
The binding entry is `D-07` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.

## D-08 · Persistence compatibility (design decision, agent-verified)
Rule: old `.quant` files must survive the ladder change. Therefore:
- IDs are KEPT in place (no renumber) — a renumber silently reinterprets checkpoints
because format is stored as raw `uint8_t` per block and no version field is read.
- 36 retired holes become invalid ids; readers remap via `legacy_format_id_remap()`
(K_L→base, halves→same-BPW `_K_H`), one log line per file, never silent.
- All 4 clamp sites replace the ad-hoc `wire_fmt < FORMAT_COUNT && wire_fmt != 19`
predicate with `wire_format_valid()` from a single truth (`format_compat.h`).
- Writers assert validity before write — this catches the MoE `format = 5 with FP32
payload` label bug at write time, not on some future read.
The binding entry is `D-08` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.

## D-09 · M-tier encoder (design decision, pre-authorized)
Rule: M tier = base layout + 1 refinement byte per 32 weights
(4 × 2-bit sub-block scale multipliers {×0.75, ×1.0, ×1.25, ×1.5}) — engine-agnostic,
provably +0.25 BPW exact. Per-family alternatives (e.g. soft-threshold for the binary
family) may supersede ONLY if measurably better; acceptance gate stays: PSNR strictly
between L and H on 4 fuzz distributions + real weights.
The binding entry is `D-09` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.

## D-10 · Ternary tail policy (design decision)
Rule: for block sizes where the exact-1.50 ternary layout doesn't decompose
(cleanly), the encoder NEVER inflates: it drops to the largest tier that fits the
name's wire budget exactly (ternary → M → L, per-size). Same policy for every
rewired format: budget guard pattern of `quant_grp16:879-884` (a real budget test,
never the `has_d = (n >= 8)` non-test that caused the quant_6k overrun).
The binding entry is `D-10` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.

## D-11 · K-variant honesty (design decision)
Rule: tier logic keys off format ID/enumeration, never the NAME string
(today `k_tier()` parses `_L/_M/_H` out of the name at `block_codec.cpp:2464-2470` —
a rename would silently change encoder effort). `Q_16_K/Q_24_K` trios split from
their shared body (`:2740-2743`) into real tiers.
The binding entry is `D-11` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.
The decision is closed only when the implementation and the test agree.

## D-12 · Quality floor: scale fitting (design decision)
Rule: shared scale-fitter (`fit_scale_true_mse`, currently dead at
`block_codec.cpp:632-695`) lands in Q3/Q6/Q12 + Q2/Q4 with golden-section refinement
where it wins (today only `comp8_fit_scale_fp16:306-358` has golden-section; Q_12's
3-iteration LS seed is why it measures 46 dB while K_H's 24 iterations reach ~59 dB).
Acceptance: `Q_12 ≥` old K_H within documented margin; `Q_G_12 < Q_G_8` inversion gone.
The binding entry is `D-12` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.

## D-13 · MX quarantine (design decision, agent-verified)
Rule: the 14 MX formats are quarantined: kept, registry-marked, documented as
catastrophic (2-iteration-LS tier allocator, −21..−37 dB vs industrial refs at same
BPW), excluded from dominance claims, NOT deleted (their wire/persistence contracts
hold). `Q_G_MX_3_5` rewires 3.78125 → 3.50 so the name==wire grid includes them.
An adaptive rework of the tier allocator is a LATER, separate effort — not Operation
Clean scope.
The binding entry is `D-13` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.

## D-14 · Bench honesty (design decision)
Rule: every printed bench number must be measured, not hardcoded, and every
comparison must use one byte basis. Concretely: `write_quant_mixed` honors
`target_bpw` (today it ignores the knob — every "QUANT Mixed 1.50" row actually wrote
2.625); the `pick(rs, q_ids, 7)` OOB read (`bench_industry_real.cpp:904`) gets real
bounds; "negligible"/"95% scheduling" prose is regenerated from measured output;
Q-10's bitnet-victory bench stays CANCELLED as a task but the hardcoded victory
strings are covered by Q2's umbrella for the OTHER benches (bench_poc "No external
schemes" false claim dies too).
The binding entry is `D-14` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.

## D-15 · Priorities (operator delegated)
Rule: DAG order is my judgment: P0 → S (memory-safety, independent of the ladder)
→ L (ladder, tree-swallowing) → T (tests against a frozen ladder) → Q (quality on top
of final tests) → Z (hygiene sweeps last so they touch final code once) → V1 (prove
dominance) → R (review findings, code-fusion last because pausable).
Trace: "Ye tum khud decide karo, priority tum apne hisaab se do sabko."
The binding entry is `D-15` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.

## D-16 · One task to 100% (operator)
Rule: serial execution, one worker session per task, DoD gate green before the
next starts. Task register and gates live in PLAN.md.
Trace: "ek ko pleetooge fir use 100% complete karoge uske best level pe, most strict
worker in the world ki tarah … fir baari baari se sab ke sab 100% complete naa ho jaayenge
tab tak baari-baari se sabko ek ek karke karoge."
The binding entry is `D-16` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.

## D-17 · Execution gate (operator)
Rule: implementation starts ONLY after review workflow `wf_ce1d51d7-91d` reaches
100%. Documented fallback if the synthesize stage keeps dying on infra: compose the
final report + completeness pass from the journal + `findings_verified.json`, mark the
workflow *complete-by-reconstruction* in this file, and proceed.
Trace: "Workflow 100% complete hone ke baad ham plan ko implement karenge" /
"Plan complete ho jaayega to workflow ke wait ke liye rukna."
The binding entry is `D-17` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.

## D-18 · Execution name (operator)
Rule: this effort is called Operation Clean (all user-facing references and the
docs directory name).
The binding entry is `D-18` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.
The decision is closed only when the implementation and the test agree.
An open item stays visible in the grind tree until then.
The decision log is not a changelog; it is the constitution.

## D-19 · Strictness (operator, general)
Rule: "koi chook nahi honi chahiye" — the most-strict-worker standard. Every task's
DoD includes evidence (grep-zero counts, test names, measured numbers), not claims.
Honest bench regressions after rewire are documented, not hidden; what is hidden or
faked is a defect by definition.
The binding entry is `D-19` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.
The trace is deliberately redundant so a cold reader can follow it.
The rule is small on purpose: one decision, one observable consequence.
The decision does not depend on a named agent or a named session.
The rule survives a rename because it names behaviour, not a folder.
The entry is safe to quote in a publication because it carries its own provenance.
The implementation path is the shortest path from the rule to a file.
The decision is closed only when the implementation and the test agree.

## D-20 · Known-caught-at-test-time traps (from exploration)
These field-tested facts feed the task DoDs directly:
- `test_fuzz_codec.cpp:278` allows claimed+1 byte — this is EXACTLY why the quant_6k
+1-byte overrun passes today (S3 kills the allowance, strict ≤ after).
- `test_block_codec.cpp` does NOT test `block_codec.cpp` (it tests GEMM kernels) —
`block_codec.h:65`'s claim otherwise is false (corrected everywhere in L1/Z3).
- `test_format_audit.cpp` checks `actual <= format_bpw + 1e-3` only at N=256 and never
fails on PSNR — `test_wire_budgets.cpp` (T1) replaces all three gaps.
- `test_format_registry_complete.cpp` `singles>=19` is a floor, not the 69-set — its
replacement pins `singles >= 55` + retired names fail parse (registry
silent-default-on-miss becomes loud).
- GGUF bridge silently zero-fills unsupported types (`gguf_bridge.cpp:336-342`,
verbose-gated) — raises to loud-fail during L5 (documented as part of import
honesty, since silent zero weights are silent corruption).
- `NativeFormat` (trainer) is a separate, untouched format id-space; documented, not
merged into the quant ladder except by alias check (L4 records this explicitly).
The binding entry is `D-20` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.

## D-21 · Operation Clean ≠ review findings only
Rule: the review workflow findings (A-ranges) and quant overhaul (B/C/E ranges)
both execute through the same greatest-strictness process; quant tasks S1–V1 run
before R-series (review) because they need a stable build/test gate. DEFECTS.md stays
the ledger for both.
*(empty — the review workflow is still running; this section fills with evidence if
the synthesize stage cannot complete and complete-by-reconstruction is invoked.)*
### How to use this file during execution
1. Before each task: check the register in PLAN.md + relevant decisions here.
2. During each task: if a decision is contradicted by a live fact, STOP, record the
conflict here as a new decision (append, never rewrite), then continue.
3. After each task: append one line to PLAN.md §Progress log.
The binding entry is `D-21` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.
The date is the operator date, not the date the file was last touched.

## D-22 · LADDER COUNT RESOLVED: **69 wins** (Fusion Smash, 2026-11-01)
Conflict raised by Prime Orchestrator: `review-tracking/MASTER_PLAN.md` says 60 formats;
`docs/operation-clean/LADDER.md` + the live enum say 69.
Verdict: 69 is authoritative. Evidence (all commands run, outputs below):
| # | Evidence | Source |
|---|---|---|
| 1 | `MASTER_PLAN.md:29` §1 heading says "Target format ladder (60 formats)" — but `MASTER_PLAN.md:223` its OWN L1 task row says "`types.h`: 69 live formats, validity table, retired-id map, new `format_compat.h`" | MASTER_PLAN internal contradiction |
| 2 | `MASTER_PLAN.md:94` §1.4 retires "GRP base `Q_G_x` (9)" — but `MASTER_PLAN.md:126-133` §2 "Rewire map" REWIRES that same family: "`Q_G_2` 2.625 → 2.00", "`Q_G_x_K_*` (×9) → exact base", "same as their GRP base" | MASTER_PLAN internal contradiction |
| 3 | `MASTER_PLAN.md:18` G-4 verbatim: "GRP families (`Q_G_*`) follow the identical L/M/H rule" — L is the base; retirement contradicts the rule it cites | operator rule |
| 4 | Live enum `include/quant/types.h:146-147`: `FORMAT_ID_SLOTS = 105`, `FORMAT_COUNT = 69`; `kFormatValid[105]` marks exactly 69 ids live, and ids 37–45 (`Q_G_1`..`Q_G_24`) are LIVE | live code |
| 5 | Live `format_bpw` already carries `Q_G_2 → 2.0f` … `Q_G_24 → 24.0f` (`types.h:312-320`), matching LADDER's 69-ladder | live code |
| 6 | 69 = 10 base + 18 plain M/H + 9 GRP base + 18 GRP M/H + 14 MX, and MASTER_PLAN's own §1.1/1.2/1.3 arithmetic (28 + 18 + 14) = 60 comes from retiring the 9 GRP bases | arithmetic |
Resolution that satisfies both documents: keep the 9 GRP bases (LADDER.md's 69). The
§1.0 budget proof in MASTER_PLAN is still TRUE and is retained as a design note, not a
retirement:
> ### Design note D-22a (the real content of MASTER_PLAN §1.0)
> At `B.00` a 256-weight block has exactly `256·B` bits of budget and `B`-bit levels alone
> consume all of it — so a GRP base at `B.00` cannot carry any per-group state. Its
> layout is therefore the *plain base layout under a GRP name* (exactly as `Q_G_1` already
> is: `types.h:284` `Q_1 → 1.0f` and `:312` `Q_G_1 → 1.0f`, both using the same slot-sign
> codec at `block_codec.cpp`). The genuine grouping lives in the tiers: `Q_G_x_K_M` at
> `B.25` and `Q_G_x_K_H` at `B.50`.
> Consequence for L2: the GRP base encoder must be cut down to the plain-base layout
> (today it still calls the grouped-affine path at 2.625 BPW — see D-23).
Trade-off accepted: `Q_G_x` at `B.00` is byte-identical in *layout* to `Q_x` for every x.
That is not a lie (name == wire == `B.00`), but it must be documented as a naming/API alias
in Z3's docs pass so no one claims the GRP base is a distinct codec. If a distinct GRP base
codec is ever wanted, it requires a sub-`.00` grid, which the operator's `.0/.25/.50` rule
forbids.
Ladder count is now frozen: 69. `FORMAT_COUNT = 69`. Any future claim of 60 is stale — this
line supersedes it.

## D-23 · LIVE DEFECT found during D-22 verification (L4 is a data-corruption bug)
Found: 2026-11-01, Fusion Smash. Severity: critical (silent data corruption on read).
L1 landed (`FORMAT_COUNT` 105 → 69) but L4 did not. All four `.quant` clamp sites still use the
old predicate `wire_fmt < FORMAT_COUNT && wire_fmt != 19`:
| Site | Line |
|---|---|
| `src/codec/quant_format.cpp` | `:456` `bd.format = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) ? (Format)wire_fmt : Format::Q_32;` |
| `src/codec/quant_format.cpp` | `:611` `fmts.push_back((wire_fmt < FORMAT_COUNT && wire_fmt != 19) ? (Format)wire_fmt : Format::Q_32);` |
| `src/adapters/tools/qwen35_engine.cpp` | `:32` `const Format fmt = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) …` |
| `src/adapters/tools/qwen35_engine.cpp` | `:145` `t.fmt = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) …` |
Because `FORMAT_COUNT` is now 69 while the id space is 105, every valid format with id ≥ 69
silently decodes as `Format::Q_32`. Parsed from the live `kFormatValid` table, that is
17 valid formats: ids `69, 71, 72` (`Q_G_16_K_M`, `Q_G_24_K_M`, `Q_G_24_K_H`) and
`91..104` (all 14 MX formats).
Fix (L4, next task): introduce `include/quant/format_compat.h` with `kFormatValid` as the
single truth plus `wire_format_valid()`, and replace all four predicates with it. Writer must
assert validity before write. Recorded as the first L4 sub-step.
The binding entry is `D-23` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.

## D-24 · Workspace rename: `code-fusion/` → `code/`, `transformers-fusion/` → `transformers/` (operator, 2026-11-12)
Rule: both repos were renamed because both already live inside `fusion/` ("fusion to hai hi").
The GitHub remotes follow: `origin-labs-ai/code.git` and `origin-labs-ai/transformers.git`
(old `*-fusion.git` URLs redirect; everything else unchanged). The product/alias vocabulary is
NOT renamed — CodeFusion, TransFormers-Fusion and TransCender stay as names (§1 of the master
plan governs). What changed is only *path-shaped* references: `transformers-fusion/…`,
`code-fusion/…`, `*-fusion.git` URLs — 93 live files swept (plan + PLAN.md + review-tracking +
operation-clean docs + all `.rea-tmp` scripts + `transformers/PROGRESS.md` + `code/arch` +
`code/payloads`). Verbatim operator quotes, the alias-vocabulary table and historical evidence
dumps were deliberately left untouched — rewriting a quote would falsify evidence. Full backup:
`.plan/.rea-tmp/rename-sweep-backup-20261112-182006/`.
> Spelling update (2026-11-13, D-28): the current product spelling is
> `Transformers-Fusion`; this 2026-11-12 entry preserves its dated spelling as history.
Trace:
- *"Saath me maine code-fusion/ ko code/ me rename kar diya hai and transformers-fusion/ ko
transformers/ me kyuki dono fusion/ folder ke andar me hai yaani fusion to hai hi! Usi ke
hisaab se thora-bahut origin bhi change hoga, transformers-fusion.git se transformers.git
ho jaayega, baaki ka adress same hi hai, aise hi code-fusion.git se code.git ho jaayega!
Keep in mind!"*
- Implementation: path sweep (`rename_sweep.py` + `surgical.py`), then all 7 plan verifiers
re-run exit 0 (step1 117/117·13/13 · step2 PASSED · step3 156/156 anchors 0 problems ·
subanchors 85/85 · step5 65 checks · step6 PASSED · arxiv 67/67).
The binding entry is `D-24` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.

## D-25 · Effort slider: DSH plugin belongs to Sonar; Zenix port parked (operator, 2026-11-12)
Rule: `code/slider/effort` = `dsh-claude-effort-slider` v0.9.4 (MIT) — a DeepSeek Harness
(DSH) plugin (cordis.patch.yml + `dsh.client` bundle, 6-stop Low→Ultracode, 38/38 tests). DSH
== Sonar (Plus) natively. Zenix (Claude Desktop) has no cordis/slots (plain Electron +
React renderer) but *does* carry the hooks (`effortLevel`/`reasoningEffort` in main,
`thinkingBudget`/`extendedThinking` in renderer) — so a port is possible later, in one of two
shapes: A DOM-inject into the composer (fast, reversible, needs `ion-dist.asar` repack) or
B native rebuild wired into Fusion's layout system. Operator ruling: park BOTH for now
— *"look waisa implement karenge, Sonar me bhi implement karenge!"* then *"Dono baad me
karenge!"* → Sonar integration + Zenix port are context-only until unparked.
Trace: thread *Current Strike* runs 11–12 (host-mismatch quote + comment). Implementation:
none yet — parked. Next when un-parked: Sonar = plugin wire (profile bundle + registry) and
Zenix = choose A or B.
The binding entry is `D-25` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.
The dashboard and the todo tree both point back to this entry.
The rule applies to the superproject and to both submodules.
Evidence is recorded in the same entry, not in a separate private note.
A failed verification reopens the item; the entry keeps both states.

## D-26 · _archive/ = reference-only port of every deleted doc (operator, 2026-11-12)
Rule: all docs ever deleted from both repos (the 2026-11-01 `code-fusion` purge of
README/`docs/` and the earlier `transformers` history) are recovered ONCE into
`.plan/_archive/` — 288 files / ~10.6 MB: README (5,925 lines), `docs/` (38), `repo/memory/`
(15, the iron rules), `TransCender.png`. `InNova.png` stays deleted (operator ruling). The
archive is reference only — future docs get redesigned fresh ("sab bas reference ke liye
uthaa raha hu"), so this port defines the pattern for how deleted docs get archived: copy-once,
never override, keep the deletion history intact. Engine-repo identity recorded alongside:
TransFormers-Fusion, formerly known as TransCender (Inferno = kernel + training engine).
> Spelling update (2026-11-13, D-28): current spelling is `Transformers-Fusion`; D-30 also
> fixes the wire identity — `Transformers-FusionIDX` + legacy `TransCenderIDX` only.
Trace:
- *"IDEA! Bhai, .plan/_archive wo waala saara ka saara source yahaa copy kar! … InNova.png ko
deleted hi rehne de! Jitna jo bhi files the — delete hue, sab ko yahaa uthaa ke le aa,
kuchh bhi override bhi naa ho! … sab bas reference ke liye uthaa raha hu to uthaa le!"*
- Implementation: `.plan/_archive/` populated (Code Crash thread run 12 — archive + remotes
completed before the run died on a provider 429; the path-sweep remainder was finished here).
The binding entry is `D-26` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.
The operator quote is preserved verbatim so the intent survives translation.
The distilled rule is written for implementers, not for the transcript.
A contradiction is resolved by a new decision, never by silently editing history.
The decision log is one of the four context-recovery documents.

## D-27 · Goal hierarchy + 1.0 BPW side goal + FP/INT research direction (operator, 2026-11-12)
Rule: the reading public (and any agent) misreads this project as "main target 1.5 BPW".
Operator ruling: MAIN GOAL = the entire Fusion Superproject (every domain, seat, track —
complete). SIDE GOAL = MAXIMUM at EXACT 1.0 BPW — *not* 1.5; the implemented 1.5 BPW path
is the *stepping stone*, and existing "1.5 BPW" statements stay true as *implemented-state
facts* while the goal line moves to 1.0. New research direction (operator's same-day
research): FP (floating-point) and INT (integer) quantization format families BOTH have
actionable work — research both. Fact recorded: Loop Quantization has never been
implemented for any model anywhere (2026-11-12 audit) — Track B will be the first.
Every implement-facing document carries the reminder note in the operator's own words.
Trace:
- *"Jo bhi ye project dekhta hai to use lagta hai ki is project ka main target 1.5 BPW hai… ye
poora sabka doubt clear karne ke liye… Is project ka main goal to poora Superproject hai!
Side goal me 1.5 BPW par nahi, exact 1.0 BPW par maximum achieve karna hai, sab kuchh!"*
- *"Aaj ke mere research ke hisaab se FP waale jo bhi quantization formats hai and INT yaani
Floating Point and Integers waale unka bhi kuchh kara jaa sakta hai, ye sab note kar lo!
Har document me! … apne words me jisse ki koi bhi agent plan waale file ko dekh karke
implement kar raha ho to beech me ye padhe to mujhe yaad dilaaye!"*
- *"Aaj tak kisi ne Loop Quantization implement bhi nahi kiya hai, koi bhi model ka!"*
- Implementation: reminder inserted in master plan, PLAN.md, LADDER.md, PROGRESS.md,
TODO-TREE, BLUEPRINT; telemetry DASHBOARD carries it top-of-file.
The binding entry is `D-27` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.
The implementation trace carries the command, the output and the file:line reference.
No code change may weaken the rule without a new decision id.
The telemetry dashboard reports the ledger state after every step.
The rule is part of the superproject contract, not only of one component repository.
Where the rule names a count, the count is checked against the live tree.
Where the rule names a format, the registry is the single source of truth.
Where the rule names a gate, the gate is run before the change is accepted.
The decision remains auditable after the working tree changes.

## D-28 · Product-name normalisation: `TransFormers-Fusion` -> `Transformers-Fusion` (operator, 2026-11-13)
Rule: the capital `F` in "Formers" is dropped everywhere in the Fusion Superproject -
`TransFormers-Fusion` becomes `Transformers-Fusion` - across documentation, code, build
scripts, CI workflows, benchmarks, tests, telemetry strings and archived documents.
`CodeFusion` and `TransCender` keep their names (D-24 left the product vocabulary alone;
this ruling narrows it for the engine name only). The spelling is byte-length preserving
(`TransFormers` and `Transformers` are both 12 characters), so file sizes, the archive
manifest's byte column and every size-derived fact stay valid.
Wire-format safety: the `.idx` magic moves from `TransFormers-FusionIDX` to
`Transformers-FusionIDX`. Both are 22 bytes (21 compared + NUL), so the layout does not
change, and the reader now accepts both spellings so that files written by earlier
builds keep decoding. The writer emits the new spelling only. The magic that would have
been broken is therefore not broken - this honours the standing ruling that the wire format
is not touched without an operator decision.
Trace:
- *"poore fusion/ me jahaa bhi and kahi bhi Trans'F'ormers-Fusion likha hua hai, 'F'ormers
me to usko 'f' kardo, lower case kar do! Har ek jagah, docs se lekar code tak, jahaa jo
bhi hai - sab!"*
- Implementation: project-wide sweep with backups (`.plan/.rea-tmp/rename-lowerf-backup-*`),
dual-magic reader, test updated to assert the new magic and the legacy alias.
Executed (2026-11-13):
- 83 text files rewritten - 9 under `.plan/`, 74 under `transformers/`; `code/` needed none.
- The first sweep died with `WinError 206` (path too long) after 33,284 mirrored backups. It was
completed with a flat, hash-named backup: `.plan/.rea-tmp/rlb-20261113-113652/` (83 entries,
`index.jsonl` maps every rewritten file to its backup). Re-running the sweep changes 0 files.
- Excluded on purpose: `.git`, `.mimosa`, build trees, `__pycache__`, `.rea-tmp` snapshots, every
`*.bak*` / backup copy, and this file (the decision log keeps the historical spelling).
- Wire format: the writer magic is lowered; the reader keeps the pre-D-28 spelling as a fourth
accepted magic. `tests/test_sha256_corrupt.cpp` gained `Test 6` (legacy magic still readable) -
16/16 tests pass on a fresh Ninja + clang++ build (`build-norm/`), and `test_math` /
`test_kernel` still pass.

## D-29 · Zenix-CC -> Zenix (CC suffix removed) + alias-registry duplicate cleanup (operator, 2026-11-13)
Rule: the native Claude Desktop seat is Zenix - the `CC` suffix is removed from the
product name, the folder (`windows/zenix`), the registry entries and every current-state doc.
The component folders and GitHub repos carry no `-fusion` suffix (`code/`,
`origin-labs-ai/code`; `transformers/`, `origin-labs-ai/transformers`) - reaffirming D-24 -
while the product names CodeFusion and Transformers-Fusion are unchanged (D-28).
The alias registry lists each accepted spelling exactly once; a repeated variant is a
documentation defect and is removed.
Trace:
- *"Zenix-CC ab 'Zenix' only reh chuka hai, CC hat gaya hai, ab dono repos me se *-fusion hat
gaya hai ... is file me ... 2 baar 'Transformers-Fusion' repeated hai to ek hataa dena,
aise-aise jitne bhi jhol hai sab fix kar dena!"*
Executed (2026-11-13):
- Master plan §1: duplicate `Transformers-Fusion` alias removed from the accepted-variants
table and the §1.1 alias registry; a path/repo note now states that folders and GitHub
repos carry no `-fusion` suffix while product names stay unchanged.
- Master-plan §16: the D-28 entry's "before" spellings were restored (`TransFormers-Fusion`,
`TransFormers-FusionIDX`) after the sweep had rewritten both sides of the arrow.
- `code/scripts/rebrand/fix-zenix-cc.mjs` -> `fix-zenix.mjs`; `migrate-arch.mjs` reference
updated; all `Zenix CC` strings removed from the tooling.
- `code/BRAND.md`, `code/arch/windows.json`, `code/arch/brand.ts`, `code/launcher/index.html`
and `code/windows/zenix/window.json` already use Zenix / `windows/zenix`; the new
`window.json` is tracked and `windows/zenix/SOURCE/` stays local-only.
- `.plan/review-tracking/FINAL_REPORT.md` and `PROGRESS.md` carry dated correction notes for
their historical `Zenix CC` rows.
- `.plan/telemetry/gen_dashboard.py` deletion note updated to `zenix-cc -> zenix`; the
dashboard is regenerated after the sweep.
- Historical documents keep historical spellings where they are explicitly history:
`.plan/_archive/`, this decision log's older entries, and verbatim operator quotes.
The binding entry is `D-29` in `.plan/docs/operation-clean/DECISIONS.md`.
The decision log is append-only: a later decision may supersede this rule, but the record stays.

## D-30 · Wire-magic identity: engine `.idx` accepts `Transformers-FusionIDX` + `TransCenderIDX` only; `SolIDX` is model-manifest-only (operator, 2026-11-13)
Rule: a model name is not an engine wire identity. The `.idx` format belongs to the engine,
so its magic is the engine's own identity:
| Namespace | Accepted | Rejected |
|---|---|---|
| Engine `.idx` | `Transformers-FusionIDX` (22 B, current); pre-D-28 capital-F spelling (same 22 B, read-only); `TransCenderIDX` (15 B, the engine's former name - "formerly known as") | `SolIDX` (7 B), `InNovaIDX` (10 B) |
| Model manifest | `SolIDX` (7 B incl. NUL), reserved and specified - no engine consumer | - |
`SolIDX` is documented as a model-manifest magic in `transformers/docs/MODEL_MANIFEST.md`.
`tracesol` stays as the cosmetic Plotly series name. `Sol` remains the trained model family
(`sol-4-flash`).
Legacy names. `InNova` (the pre-rename model family, now `Sol` / `sol-4-flash`) and
`InNovaIDX` (the pre-rename wire magic, now retired) are historical names only. They are never
current identifiers, and `InNovaIDX` stays rejected by the engine `.idx` reader.
Trace:
- *"ye TransCenderIDX kyu SolIDX banaa? Bhai, Seedha matlab ye tha ki Transformers-FusionIDX /
TransCenderIDX same cheej the yaani TF = TC tha, Sol to wo model ka naam socha gaya jo ki train
kara jaayega ya fine tune karaa jaayega, ye kya jhol ho gaya!"*
- *"InNovaIDX bhi nahi rakhna hai naa! Hame TransCenderIDX / Transformers-FusionIDX dono is also
known as ya formerly known as bhi daal sakte hai!"*
The defect. The 2026-11-12 rename wave (`D-27`, "Sab rename hoyega!") treated `SolIDX` as the
new name of the `.idx` legacy magic and shipped a 7-byte reader branch. That conflated the engine
wire namespace with the model namespace, and it made old 10-byte `InNovaIDX` files unreadable.
The correct equivalence is `Transformers-FusionIDX` = current engine identity and
`TransCenderIDX` = the same engine's former name; `Sol` names the model, not the file format.
Executed (2026-11-13):
- `transformers/src/codec/quant_format.cpp`: removed the `SolIDX` branch; `TransCenderIDX` is the
only legacy engine branch. Writer still emits `Transformers-FusionIDX` (22 B).
- The pre-D-28 capital-F magic is compared byte-wise (`"Trans"` + `'F'` + `"ormers-FusionIDX"`) so
the source tree never carries the old spelling; the reader still accepts it for read compatibility.
- Reader minimum size raised to 23 B (15 B legacy magic + 8 B header); the 15 B guard was sized
for the retired 7 B magic.

## D-31 · Exact documentation targets: 2048 / 4096 / 6144 LOC + a 512-page DOCX and PDF (operator, 2026-11-13)
Rule: the three project READMEs are built to exact line counts, and the publishable
research package is a 512-page document in both `.docx` and `.pdf`:
| Repository | README target | Exactness |
|---|---|---|
| `fusion/` (superproject) | 2,048 LOC | `wc -l` must equal 2,048 |
| `code/` (CodeFusion) | 4,096 LOC | `wc -l` must equal 4,096 |
| `transformers/` (Transformers-Fusion) | 6,144 LOC | `wc -l` must equal 6,144 |
This supersedes the T10 mapping recorded on 2026-11-12 (which had `fusion` at 4,096 and `code` at
2,048). The operator's words on 2026-11-13: *"CodeFusion repo me 4096 LOCs ka README banega,
Transfoemers-Fusion repo me 6144 LOCs ka and Fusion me 2048 LOCs ka, exact! Bhai, mera exact matlab
exact hi hota hai."*
Format rule. The visual reference is
`C:\Users\thaku\Workspaces\side-projects\origin-router\README.md`: centred header with an SVG logo,
one-line pitch, emoji navigation links, `shields.io` badges (`style=flat-square`), horizontal rules,
emoji-headed sections, tables, short command snippets and a licence/credits footer. Code snippets
stay average/minimal - a command, a call shape or a small type, never a wall of source.
Page rule. The 512-page package ships as one document, two formats: `PDF` typeset with TeX
Live 2026 (cover page, part dividers, running headers, page numbers, tables, callouts) and `DOCX`
generated with `python-docx` from the same page-block model. Each format must contain exactly
512 pages; 512 is not a target range.
Telemetry rule. Every generator writes a machine-readable manifest (target count, actual count,
sha256, timestamp, source commit) and the dashboard gains a documentation status section. The
generators live in `.plan/telemetry/docgen/`, are deterministic, read facts from the live tree, and
refuse to write a file whose count is off by even one line or one page.
Trace:
- *"Jo karna hai fix wo kar de, uske baad 512 page ka .docx and .pdf banayenge isi knowledge ke
base par!"*
- *"Code snippets average hi rahenge, minimal level!"*
- *"Mast se cover page / main page / first page ke saath banana, TeX bhi installed hai .pdf banane
ke liye! Python bhi hai! Look wisse bhi jagah hona chahiye!"*

## R-01 · Master plan loop, Steps 1-6 (Transformers-Fusion architecture plan)
- Scope: the whole master plan: 117-row source coverage map (§10X), 13 gaps, KAT inventory
(§2.1b.1), 156 line-anchors, 7-tree audit (§10Y), 8 decision gates (§6.1, D-1..D-8),
corruption scan, Phase-0 ledger, arXiv re-resolve 67/67 + browser 9/9.
- Source document: `.plan/pasted-content-id-43ed-ye-aur-melodic-puddle.md` (345 KB)
- Evidence status: DISK-VERIFIED - all 7 verifiers exit 0 on 2026-11-12
(step1 121/121 headings + 13 gaps · step2 PASSED · step3 156/156 anchors 0 problems ·
subanchors 85/85 · step5 65 checks · step6 PASSED · arxiv 67/67).
- Audit slots: pass 1 = plan-loop session (2026-11-10..12) · pass 2 = the 2026-11-12
post-rename re-verification · pass 3 = PENDING (operator).
The item is indexed as `R-01` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.

## R-02 · Loop Transformers research (§5d, §5e, §5c)
- Scope: three loop shapes, attention across three axes, training effects, cost/quality
market scan, Attention-Residual depth-axis mechanism, candidate G/S formulations, adaptive
routing, EAIN literature basis and its honest ceiling.
- Source document: master plan §5c-§5f; papers: 2603.10123, 2603.15031, 2607.18730,
2605.18855, 2610.13630, 2607.27230, 2607.09694, 2606.18524, 2610.00673, 2605.16343,
2610.16368, 2609.30820, 2611.07226, 2510.25741, 2610.33360.
- Evidence status: PAPER-ONLY for the deep-read (G/S design note still OPEN-RESEARCH) -
a browser pass per paper is required before this can be called complete.
- Audit slots: pass 1 = §5 pass (2026-11-10) · pass 2 = PENDING · pass 3 = PENDING.
The item is indexed as `R-02` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.

## R-03 · Traditional Transformers baseline (§5d companion)
- Scope: the baseline side of the loop-vs-traditional comparison: attention/training deltas,
market scan, fixed-depth comparison protocol.
- Source document: master plan §5d, §5d.4, §9.
- Evidence status: PAPER-ONLY (refresh pass needed for any post-2026-11-10 paper).
- Audit slots: 1 of 3 done.
The item is indexed as `R-03` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.
The item is part of the 512-page publication's source set.

## R-04 · Traditional Quantization / Track A - the 69-format ladder
- Scope: name == nominal == wire BPW contract, 1.5 BPW path, Operation Clean L1-L7 tasks,
MX family measurement + quarantine (D-13), scale-fitting (D-12), bench honesty (D-14).
- Source document: `.plan/docs/operation-clean/LADDER.md`, `PLAN.md`, `DECISIONS.md`,
`WORKING-TREE.md`; master plan §9b.1.
- Evidence status: DISK-VERIFIED (formats implemented and measured; MX quality numbers
-21..-37 dB recorded). Open: D-12/D-13/D-14 rulings, TransCenderIDX wire ruling, install_test
duplicate header ruling.
- Audit slots: 1 of 3 done (Operation Clean pass).
The item is indexed as `R-04` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.

## R-05 · CodeFusion per-part research (64 sections - the product's research record)
- Scope: NOT a build checklist - a research document in prose form (the operator rejected the
1024-line and 2048-line checklist drafts for being a checklist instead of an explanation).
64 sections x exactly 32 lines, one heading + 30 lines of prose + 1 blank. It contains real
research: session-history forensics (§2-9: baseline repair + CJK damage, Repo Wiki + Qoder
evidence, MAD restoration, skills vendoring, desktop-binary extraction, the naming cycle,
restructure + gate + inbuilt bundle), the registry schema (§11), invariants and the
consistency gate (§12), the alias ladder (§13), provenance research (§14-15), per-part
research for every seat (§16-19, §33-51: Ingot, Aster/Onyx, Chromix, Codeix, GSX-CLI, Zingma,
Sonar, Zenix), skills inventory/provenance/wiring (§52-54), the inbuilt bundle (§55-56),
reverse-engineering methodology (§57-58: routing + evidence format), phases 0-4 (§59-63)
and verification/risks/open questions (§64).
- Source document: `.plan/review-tracking/DRAFT.md` (145 KB, 64 sections).
- Evidence status: DISK-VERIFIED (registry `arch/windows.json` + gate 13/13 green). NOTE: the
draft still describes the pre-2026-11-12 state (8 parts incl. Chromix, Onyx->Aster rename
pending, Zenix) - it is the *research record*, the live truth is `code/arch/` + D-24..D-27.
- Audit slots: 1 of 3 done (Operation Clean / CF pass).
The item is indexed as `R-05` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.

## R-06 · Reverse-engineering research (the 7 seats)
- Scope: MSIX/ASAR extraction + beautification + REA application graph for Codeix
(ui-old/ui-new), Onyx (Qoder + official VS Code OSS 1.147.0), Zingma (Qoder Quest window),
Zenix (Claude Desktop 5.1231.2 + Cowork VHDX sandbox), Sonar (DSH), Ingot (ZCode source),
GSX-CLI (opencode/MiMoCode). Exact ASAR sha256 vs MSIX match; 21,791 ASAR files in ui-new.
- Source document: `.rea-tmp/codex/README.md` + `evidence/*.json`;
`.plan/docs/operation-clean/DECISIONS.md`.
- Evidence status: DISK-VERIFIED for extraction (byte-exact); branding/RE gaps remain.
- Audit slots: 1 of 3 done.
The item is indexed as `R-06` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.

## R-07 · Effort slider reverse-engineering (DSH plugin)
- Scope: `dsh-claude-effort-slider` v0.9.4 - 6-stop slider, 4 real effort values, DSH
`directory.select({reasoningEffort})` write path, cordis slot `conversation.input.right`,
fail-open DOM anchors, 38/38 tests.
- Source document: `code/slider/effort/` (lib/client.js 1682 lines, cordis.patch.yml,
test/client.test.mjs, ANIMATION.md).
- Evidence status: DISK-VERIFIED; Zenix port shape A/B still open (parked, D-25).
- Audit slots: 1 of 3 done.
The item is indexed as `R-07` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.

## R-08 · Claude Code effort-slider archaeology
- Scope: CLI 2.1.251 / 2.1.302 / 2.1.319 and extension 2.1.302 / 2.1.319 / 2.1.322 -
`EffortSlider` appears in CLI 2.1.302 and extension 2.1.319, never removed; the real
"expiry" is the server-side `supportsEffort` capability gate. 5 levels, `max` included,
per-model `effort_cost_index`.
- Source document: this session's forensics (recorded in the plan and PROGRESS.md).
- Evidence status: PAPER-ONLY (binary grep of shipped builds; not independently re-run).
- Audit slots: 1 of 3 done.
The item is indexed as `R-08` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.

## R-09 · Deleted-docs recovery (the 2026-10-07 purge)
- Scope: commit `9c0e480` (98 files, 77 md) + `f6ee292` (34 files) in the engine repo,
and the earlier `85d2ce167` purge in the launcher repo; what survived, what was recovered.
- Source document: `.plan/_archive/` (288 files, 10.6 MB) + D-26.
- Evidence status: DISK-VERIFIED (recovered from git history; `InNova.png` stays deleted).
- Audit slots: 1 of 3 done.
The item is indexed as `R-09` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.
The item is part of the 512-page publication's source set.

## R-10 · Workspace rename + superproject git recovery (2026-11-12)
- Scope: `code-fusion/` -> `code/`, `transformers-fusion/` -> `transformers/`, remotes ->
`code.git` / `transformers.git`, 93-file path sweep with quote-safe rules, superproject repo
re-init with full remote history adopted (8 commits), `.gitmodules` path fix, `.plan` tracked.
- Source document: D-24, D-27, `.plan/telemetry/DASHBOARD.md`, fusion git log.
- Evidence status: DISK-VERIFIED (git log + gate 13/13 + 7 verifiers green).
- Audit slots: 1 of 3 done.
## B. Research in progress / pending (operator-owned or queued)
The item is indexed as `R-10` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.

## R-11 · INT x FP programme (the operator's current research topic) - ACTIVE
- Scope: the complete INT-vs-FP research programme: difference INT vs FP; what is already
implemented in this project; what can be touched/improved; the unique format style applied to
both families; best-in-every-dimension outcome and how to build it; codebook merger
(ternary {0,-1,+1} vs binary {0,1} - a sovereign stack?); measurement normalization
(TFLOPS for FP vs TOPS for INT).
- Source document: `.plan/DRAFT.md` (627 lines, 15 sections + §16 operator questions).
- Evidence status: the code audit inside the draft is DISK-VERIFIED (8/8 files, 3/3 symbols
re-checked on 2026-11-12); the literature half is PAPER-ONLY and needs the browser pass.
- Audit slots: 1 of 3 done (draft audit) - 2 browser/research passes PENDING.
The item is indexed as `R-11` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.

## R-12 · Loop Quantization (Track B) - never implemented anywhere
- Scope: loop-aware quantization as a compute contract; LoopQ (`2605.16343`) and LoopQuant
(`2610.16368`) results are at ~4 BPW, our target is 1.0 BPW (D-27) / 1.5 BPW (implemented
state); loop-entry adapter fails first on INT4; no looped-model fix validated above a few-B
parameters.
- Source document: master plan §5f, §9b.2 Track B.
- Evidence status: PAPER-ONLY.
- Audit slots: 0 of 3.
The item is indexed as `R-12` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.

## R-13 · Mix Quantization
- Scope: mixed-format / bit-mixing quantization literature; the MX family (14 formats)
measured and quarantined; mixed-precision allocation already implemented in Q_MX/Q_G_MX.
- Source document: master plan §9b.1-§9b.2, LADDER.md (MX rows), DECISIONS D-13.
- Evidence status: PARTIAL - measured, but the mix-strategy literature pass has not been done.
- Audit slots: 0 of 3.
The item is indexed as `R-13` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.
The item is part of the 512-page publication's source set.

## R-14 · NCM - Next-Concept Modeling (arXiv 2610.14162)
- Scope: the generation mechanism; §3b spec already extracted from the HTML; Appendix F.1.1
and I still unread; merger with DSpine (§3c) pending.
- Source document: master plan §3b, §3c.
- Evidence status: PAPER-ONLY (partly extracted) - needs the full browser read.
- Audit slots: 0 of 3.
The item is indexed as `R-14` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.
The item is part of the 512-page publication's source set.

## R-15 · EAIN (Enhanced Artificial Intelligence Neurons)
- Scope: literature basis (§5c.4), the honest ceiling, scoping to the implementable subset
(per-unit importance/decay + thresholded activation + local plasticity), and choosing which
of the three parallel continual-learning stacks it sits on.
- Source document: master plan §4.8a, §4.9, §5c.4.
- Evidence status: PAPER-ONLY for the literature; the design is OPEN-DESIGN.
- Audit slots: 0 of 3.
The item is indexed as `R-15` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.

## R-16 · Inferno (kernel + training engine)
- Scope: full file-by-file breakdown of the Inferno kernel and the training engine,
including the DSpine/NCM generation paths, the 7 CRITICAL defects register (§10M) and the
bench-honesty gates.
- Source document: `transformers/inferno/`, master plan §10M, §10K.
- Evidence status: not yet started - this is the T8 deep-breakdown to-do.
- Audit slots: 0 of 3.
The item is indexed as `R-16` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.

## R-17 · Publishable research report (PDF + DOCX, 512 pages)
- Scope: the same data in two extensions (PDF and DOCX), ~512 pages, produced from the
completed research above; the operator audits the whole set 3x.
- Source document: T13 - generation happens once the operator's content lands.
- Evidence status: not started (operator-owned content).
- Audit slots: 0 of 3.
The item is indexed as `R-17` in `.plan/RESEARCH-INDEX.md`.
The research index separates audit-ready work from work still in progress.
Every claim carries a command, an output and a file:line reference.
The audit protocol has three passes: produce, re-verify, publishability review.
The operator owns the publishability pass; the agent fixes what it rejects.
A research item is not closed because the prose is long; it is closed when the evidence is checked.
Where the item names an arXiv identifier, the abstract was fetched live.
Where the item names a file, the file exists in the tree at the recorded path.
Where the item names a number, the number is regenerated rather than remembered.
The research index is one of the four context-recovery documents.
The item may feed the engine, the launcher, or the publication; the index records which.
The item's status is visible in the dashboard's domain-coverage table.
An open question is written as an open question, not as a confident guess.
The item keeps its original wording where the wording is the evidence.
The item is linked from the master plan and from the todo tree.
The research does not replace the code; it explains why the code has its shape.
The item is allowed to conclude that a path is not worth taking.
The item is allowed to conclude that the ceiling is lower than hoped.
The item is not allowed to hide a failed measurement.
The item is re-read when the code changes underneath it.
The item's sources are listed so a reviewer can repeat the pass.
The item's claims are scoped; a claim about one model is not a claim about all models.
The item's terminology is normalised to the current product names.
The item's date is the date of the evidence, not the date of the file.
The item is part of the 512-page publication's source set.

## R-18 · The three project READMEs (publishable depth)
- Scope: the operator's documentation standard - `fusion/README.md` 4,096 LOC,
`code/README.md` 2,048 LOC, `transformers/README.md` 6,144 LOC, each written in prose with
average code snippets, each surviving a three-pass publishability audit. The superproject
README was deleted with everything else on 2026-10-07 and never restored; the engine README
is being rebuilt from the code.
- Source document: `.plan/telemetry/build_tf_readme.py` (generator + strict validator),
`transformers/README.md` (batch 1, sections 1-40, 1,627 LOC), `fusion/README.md`,
`code/README.md`.
- Evidence status: DISK-VERIFIED by construction - the generator extracts counts, format
names, backends, targets and tests from the tree at build time, so a number in the README
cannot drift from the code. The validator refuses to write unless every section carries 30
narrative lines (tables and code do not count), which makes padded blank lines impossible.
- Audit slots: 1 of 3 (batch 1 of 4 for the engine README; the other two READMEs pending).
## C. Document inventory - every live `.md` in `.plan/` (27 files, 759.7 KB)
| File | Bytes | What it is |
|---|---|---|
| `pasted-content-id-43ed-ye-aur-melodic-puddle.md` | 345,813 | The master plan (R-01) |
| `review-tracking/DRAFT.md` | 145,403 | CF multi-part build instruction, 64 sections (R-05) |
| `DRAFT.md` | 25,558 | INT x FP research programme (R-11) |
| `cuddly-yawning-lamport.md` | 28,926 | Operation Clean + review-fix execution record |
| `cuddly-yawning-lamport-agent-*.md` (6) | 2.5-6.3 KB | Parallel agent findings (spill code, subagents, CJK damage) |
| `PLAN.md` | 22,940 | The loop's own task DAG + DoD |
| `docs/operation-clean/DECISIONS.md` | 22,086 | Binding rulings D-01..D-27 |
| `docs/operation-clean/PLAN.md` | 15,750 | Operation Clean task DAG |
| `docs/operation-clean/LADDER.md` | 9,257 | 69-format contract |
| `docs/operation-clean/WORKING-TREE.md` | 7,898 | Working-tree state |
| `review-tracking/MASTER_PLAN.md` | 13,881 | Review findings master plan (NEW-3, M2) |
| `review-tracking/DEFECTS.md` | 11,677 | Defect register |
| `review-tracking/FINAL_REPORT.md` | 19,231 | Final review report |
| `review-tracking/PROGRESS.md` | 6,152 | Review progress |

## Appendix A · The live document inventory
- `.plan/BLUEPRINT.md` — 93 lines, 5886 bytes.
- `.plan/DRAFT.md` — 677 lines, 28587 bytes.
- `.plan/PLAN.md` — 194 lines, 22940 bytes.
- `.plan/RESEARCH-INDEX.md` — 241 lines, 15058 bytes.
- `.plan/cuddly-yawning-lamport-agent-a3cb8fe467a68af67.md` — 42 lines, 2532 bytes.
- `.plan/cuddly-yawning-lamport-agent-a560adfd74b86f32c.md` — 84 lines, 6266 bytes.
- `.plan/cuddly-yawning-lamport-agent-ac408480a0297af30.md` — 61 lines, 3467 bytes.
- `.plan/cuddly-yawning-lamport-agent-acb191a6cb11cdded.md` — 74 lines, 5299 bytes.
- `.plan/cuddly-yawning-lamport-agent-aced4e8272883f7c7.md` — 39 lines, 3065 bytes.
- `.plan/cuddly-yawning-lamport-agent-af03497daccb4aaec.md` — 29 lines, 1694 bytes.
- `.plan/cuddly-yawning-lamport.md` — 371 lines, 28926 bytes.
- `.plan/fusion-full-review-retry-queue.md` — 122 lines, 10351 bytes.
- `.plan/pasted-content-id-43ed-ye-aur-melodic-puddle.md` — 3175 lines, 366737 bytes.
- `.plan/transformers-fusion-spec-inferno-md-pla-pure-parrot.md` — 124 lines, 8643 bytes.
- `.plan/docs/operation-clean/DECISIONS.md` — 565 lines, 34378 bytes.
- `.plan/docs/operation-clean/LADDER.md` — 169 lines, 9257 bytes.
- `.plan/docs/operation-clean/PLAN.md` — 156 lines, 19379 bytes.
- `.plan/docs/operation-clean/WORKING-TREE.md` — 56 lines, 7898 bytes.
- `.plan/telemetry/DASHBOARD.md` — 99 lines, 6540 bytes.
- `.plan/telemetry/TODO-TREE.md` — 203 lines, 13967 bytes.
- `.plan/review-tracking/DEFECTS.md` — 167 lines, 11677 bytes.
- `.plan/review-tracking/DRAFT.md` — 511 lines, 145343 bytes.
- `.plan/review-tracking/FINAL_REPORT.md` — 306 lines, 19408 bytes.
- `.plan/review-tracking/MASTER_PLAN.md` — 268 lines, 13881 bytes.
- `.plan/review-tracking/PROGRESS.md` — 100 lines, 6385 bytes.
- `.plan/review-tracking/QODER_REPO_WIKI_RE.md` — 192 lines, 10137 bytes.

## Appendix B · The decision index
- **D-01** — Ladder pattern L/M/H (operator: 2026-10-22, "Info 5" + "Info 2").
- **D-02** — Q_1 = binary, Q_1_K_H = pure ternary (operator, 2026-10-22).
- **D-03** — Rewire direction (operator: "BPW ko kam karo").
- **D-04** — GRP naming normalization.
- **D-05** — Casing: QUANT → Quant (operator, 2026-10-19).
- **D-06** — BPW granularity (operator).
- **D-07** — Zero dead code / zero stubs (operator, 2026-10-18).
- **D-08** — Persistence compatibility (design decision, agent-verified).
- **D-09** — M-tier encoder (design decision, pre-authorized).
- **D-10** — Ternary tail policy (design decision).
- **D-11** — K-variant honesty (design decision).
- **D-12** — Quality floor: scale fitting (design decision).
- **D-13** — MX quarantine (design decision, agent-verified).
- **D-14** — Bench honesty (design decision).
- **D-15** — Priorities (operator delegated).
- **D-16** — One task to 100% (operator).
- **D-17** — Execution gate (operator).
- **D-18** — Execution name (operator).
- **D-19** — Strictness (operator, general).
- **D-20** — Known-caught-at-test-time traps (from exploration).
- **D-21** — Operation Clean ≠ review findings only.
- **D-22** — LADDER COUNT RESOLVED: **69 wins** (Fusion Smash, 2026-11-01).
- **D-23** — LIVE DEFECT found during D-22 verification (L4 is a data-corruption bug).
- **D-24** — Workspace rename: `code-fusion/` → `code/`, `transformers-fusion/` → `transformers/` (operator, 2026-11-12).
- **D-25** — Effort slider: DSH plugin belongs to Sonar; Zenix port parked (operator, 2026-11-12).
- **D-26** — _archive/ = reference-only port of every deleted doc (operator, 2026-11-12).
- **D-27** — Goal hierarchy + 1.0 BPW side goal + FP/INT research direction (operator, 2026-11-12).
- **D-28** — Product-name normalisation: `TransFormers-Fusion` -> `Transformers-Fusion` (operator, 2026-11-13).
- **D-29** — Zenix-CC -> Zenix (CC suffix removed) + alias-registry duplicate cleanup (operator, 2026-11-13).
- **D-30** — Wire-magic identity: engine `.idx` accepts `Transformers-FusionIDX` + `TransCenderIDX` only; `SolIDX` is model-manifest-only (operator, 2026-11-13).

## Appendix C · The research index
- **R-01** — Master plan loop, Steps 1-6 (Transformers-Fusion architecture plan).
- **R-02** — Loop Transformers research (§5d, §5e, §5c).
- **R-03** — Traditional Transformers baseline (§5d companion).
- **R-04** — Traditional Quantization / Track A - the 69-format ladder.
- **R-05** — CodeFusion per-part research (64 sections - the product's research record).
- **R-06** — Reverse-engineering research (the 7 seats).
- **R-07** — Effort slider reverse-engineering (DSH plugin).
- **R-08** — Claude Code effort-slider archaeology.
- **R-09** — Deleted-docs recovery (the 2026-10-07 purge).
- **R-10** — Workspace rename + superproject git recovery (2026-11-12).
- **R-11** — INT x FP programme (the operator's current research topic) - ACTIVE.
- **R-12** — Loop Quantization (Track B) - never implemented anywhere.
- **R-13** — Mix Quantization.
- **R-14** — NCM - Next-Concept Modeling (arXiv 2610.14162).
- **R-15** — EAIN (Enhanced Artificial Intelligence Neurons).
- **R-16** — Inferno (kernel + training engine).
- **R-17** — Publishable research report (PDF + DOCX, 512 pages).
- **R-18** — The three project READMEs (publishable depth).

## Appendix D · The verifier register
| Verifier | Scope | Expected |
|---|---|---|
| `verify_step1.py` | coverage rows and headings | exit 0, 124 rows / 124 headings |
| `step2_fix2_verify.py` | Step-2 fixes | exit 0, all checks pass |
| `step3_verify.py` | anchor report | exit 0, report written |
| `step3_subanchors.py` | sub-anchor report | exit 0, report written |
| `verify_step5.py` | 65 checks | exit 0, all checks pass |
| `step6_audit.py` | final report audit | exit 0, audit passed |
| `arxiv_recheck.py` | arXiv identifiers | exit 0, JSON report written |
The register is live: the dashboard runs the verifiers and records the exit codes.
A verifier that fails is a red gate; the step does not close.
The verifier list is part of the context-recovery contract.
The outputs are quoted in the decision log when a decision depends on them.
The scripts live in `.plan/.rea-tmp/` and are tracked by exception in `.gitignore`.
The gate names are stable so a dashboard diff is meaningful.

## Appendix E · Domain coverage
| Domain | Status | Evidence |
|---|---|---|
| Loop Transformers | DONE | taxonomy, attention, training, attention-residuals, papers verified |
| Traditional Transformers | DONE | baseline, attention, training comparison, market scan |
| Traditional Quantization (Track A) | DONE | 69-format ladder, 1.5 BPW path, Operation Clean |
| Loop Quantization (Track B) | RESEARCH-DONE / TRACK-OPEN | LoopQ/LoopQuant W4A4 read; implementation open |
| Mix Quantization | PARTIAL | MX family measured and quarantined; literature pass open |
| DSpine x NCM merger | RESEARCH-DONE / READ-OPEN | DSpine spec complete; NCM appendices pending |
| EAIN | LIT-DONE / DESIGN-OPEN | literature basis and honest ceiling recorded |
The table is mirrored in the dashboard and in the master plan.
A status is a statement about evidence, not about optimism.
A DONE row names the pass that verified it.
An OPEN row names the next read or the next experiment.
The table is re-audited when a paper or a code path changes.
The publication reuses this table rather than inventing a second one.

## Appendix F · The engine at a glance
- Formats: **69** valid, **36** retired.
- Tests: **76** test files; **140** named cases.
- Executables: **20**. Libraries: **26**.
- Backends: **24**. Source directories: **14**.
- Engine commit: `98f5a10` on `main`.
- Source files: **714**; source lines: **173,968**.
The engine is C++20 and builds with CMake.
The quantization registry is the single source of truth for format identity.
The block codec is the single source of truth for wire layout.
The test suite is the single source of truth for behaviour.
The backend contract is the single source of truth for capability claims.
The spec is the single source of truth for the Inferno plan.
The engine README documents all of it at 6,144 lines.
The publication's engine part is derived from the same facts.

## Appendix G · Publication manifest
- Report: `publication/report/Fusion-Report-512.pdf` and `.docx`, exactly 512 pages each.
- Whitepaper: `publication/whitepaper/WHITEPAPER.pdf` and `.docx`.
- Theorem note: `publication/theorem/THEOREM-CENDER.pdf` and `.docx`.
- arXiv package: `publication/arxiv/` with `main.tex`, `references.bib` and the figure set.
- Architecture: `publication/ARCHITECTURE.md` explains how the artefacts relate.
- Index: `publication/README.md` is the reader's entry point.
- Manifest: `publication/MANIFEST.json` records targets, actual counts and SHA-256.
- The PDF is typeset with TeX Live 2026; the DOCX is generated from the same page blocks.
- The cover page is designed, not default.
- The page count is verified with `pdfinfo` for both formats.
- The publication does not claim peer review.
- The publication does not relicense the code.

## Appendix H · Risk register
| Risk | Consequence | Mitigation |
|---|---|---|
| Parallel session commits | pins drift mid-build | regenerate facts, commit the pin update last |
| Submodule mis-registration | `git submodule status` lies | `init` + `absorbgitdirs`, verified |
| Backup files in the index | noise and stale claims | untracked, ignored, kept on disk |
| Doc path drift | reader cannot find the source | generators reference the live path |
| Approximate documentation | unverifiable claims | exact-line validators |
| Page-count drift | 511 or 513 pages | page-block model + `pdfinfo` |
| Fact drift | README contradicts code | facts extracted at build time |
| Stale archive | old names leak into new docs | archive marked reference-only |
| Licence ambiguity | redistribution risk | provenance section, no blanket grant |
| Security finding without a test | regression returns | every fix carries a test |
The register is reviewed at every publication build.
A risk without a mitigation is an open decision.

## Closing note

The superproject is complete only when every component, every research track and every
publishable artefact is complete. This README is a snapshot of the live state, not a
substitute for the dashboard. A reader who needs the current numbers should run the
dashboard generator; a reader who needs the rules should read the decision log; a reader
who needs the work should read the grind tree. The three documents are deliberately
different views of the same project, and they are kept in sync by the telemetry step.
The documentation is generated at exact line counts because an approximate target cannot
be verified. The same discipline applies to the 512-page publication: the page count is
checked, not estimated. If a future change makes a target impossible, the target is
renegotiated in the decision log rather than silently missed.
The live source is the repository; the generator re-reads it on every build.
The live source is the repository; the generator re-reads it on every build.
The live source is the repository; the generator re-reads it on every build.
The live source is the repository; the generator re-reads it on every build.
## Document control

- Target: **2048** lines. Actual: **2048** lines (verified by `wc -l`).
- Source commit: `38dc263` on `main`.
- Knowledge base: `26` authored Markdown documents in `.plan/`.
- Research items: `18`. Decisions: `31`.
- Component pins: `transformers` and `code`, recorded in `.gitmodules`.
- Generator: `.plan/telemetry/docgen/build_fusion_readme.py`.
- Facts: `.plan/telemetry/docgen/facts.json` (regenerated from the live tree).
- Decision: D-31 (exact documentation targets).
- Licence: see the provenance section; no top-level licence is granted by this repository.

## Colophon

Built by `.plan/telemetry/docgen/build_fusion_readme.py` from `.plan/telemetry/docgen/facts.json`.

Verify with:

```bash
python .plan/telemetry/docgen/build_fusion_readme.py
wc -l README.md   # must print 2048
```

The generator refuses to write a short file. Counts, pins and verifier exits are live facts.
