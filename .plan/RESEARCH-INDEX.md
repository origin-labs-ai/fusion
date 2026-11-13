# Fusion Superproject - Research Index

> Every research topic in one place, each with: **scope**, **source document**, **state**,
> **evidence status**, and its **audit slot** (the operator reviews each research at least 3x
> before publishing). Completed research stays listed - nothing is deleted, only promoted.
>
> Governance: `.plan/docs/operation-clean/DECISIONS.md` (rulings) ·
> `.plan/telemetry/TODO-TREE.md` (the grind queue) · `.plan/telemetry/DASHBOARD.md` (live state).
> Language policy: work documents are English; Hinglish is operator-chat only.

---

## How to audit a research item

1. Read the **Source document** section listed below.
2. Check the **Evidence status**: `DISK-VERIFIED` means every cited path/symbol was re-read from
   disk on the date shown; `PAPER-ONLY` means it is literature-level and needs a browser pass;
   `OPERATOR-SUPPLIED` means the operator provided the content.
3. Record the pass in the item's own audit log (append-only) - three passes before publish.

---

## A. Completed research (audit-ready)

### R-01 · Master plan loop, Steps 1-6 (TransFormers-Fusion architecture plan)
- **Scope:** the whole master plan: 117-row source coverage map (§10X), 13 gaps, KAT inventory
  (§2.1b.1), 156 line-anchors, 7-tree audit (§10Y), 8 decision gates (§6.1, D-1..D-8),
  corruption scan, Phase-0 ledger, arXiv re-resolve 67/67 + browser 9/9.
- **Source document:** `.plan/pasted-content-id-43ed-ye-aur-melodic-puddle.md` (345 KB)
- **Evidence status:** DISK-VERIFIED - all 7 verifiers exit 0 on 2026-11-12
  (step1 121/121 headings + 13 gaps · step2 PASSED · step3 156/156 anchors 0 problems ·
  subanchors 85/85 · step5 65 checks · step6 PASSED · arxiv 67/67).
- **Audit slots:** pass 1 = plan-loop session (2026-11-10..12) · pass 2 = the 2026-11-12
  post-rename re-verification · pass 3 = PENDING (operator).

### R-02 · Loop Transformers research (§5d, §5e, §5c)
- **Scope:** three loop shapes, attention across three axes, training effects, cost/quality
  market scan, Attention-Residual depth-axis mechanism, candidate G/S formulations, adaptive
  routing, EAIN literature basis and its honest ceiling.
- **Source document:** master plan §5c-§5f; papers: 2603.10123, 2603.15031, 2607.18730,
  2605.18855, 2610.13630, 2607.27230, 2607.09694, 2606.18524, 2610.00673, 2605.16343,
  2610.16368, 2609.30820, 2611.07226, 2510.25741, 2610.33360.
- **Evidence status:** PAPER-ONLY for the deep-read (G/S design note still OPEN-RESEARCH) -
  a browser pass per paper is required before this can be called complete.
- **Audit slots:** pass 1 = §5 pass (2026-11-10) · pass 2 = PENDING · pass 3 = PENDING.

### R-03 · Traditional Transformers baseline (§5d companion)
- **Scope:** the baseline side of the loop-vs-traditional comparison: attention/training deltas,
  market scan, fixed-depth comparison protocol.
- **Source document:** master plan §5d, §5d.4, §9.
- **Evidence status:** PAPER-ONLY (refresh pass needed for any post-2026-11-10 paper).
- **Audit slots:** 1 of 3 done.

### R-04 · Traditional Quantization / Track A - the 69-format ladder
- **Scope:** name == nominal == wire BPW contract, 1.5 BPW path, Operation Clean L1-L7 tasks,
  MX family measurement + quarantine (D-13), scale-fitting (D-12), bench honesty (D-14).
- **Source document:** `.plan/docs/operation-clean/LADDER.md`, `PLAN.md`, `DECISIONS.md`,
  `WORKING-TREE.md`; master plan §9b.1.
- **Evidence status:** DISK-VERIFIED (formats implemented and measured; MX quality numbers
  -21..-37 dB recorded). Open: D-12/D-13/D-14 rulings, TransCenderIDX wire ruling, install_test
  duplicate header ruling.
- **Audit slots:** 1 of 3 done (Operation Clean pass).

### R-05 · CodeFusion per-part research (64 sections - the product's research record)
- **Scope:** NOT a build checklist - a **research document in prose form** (the operator rejected the
  1024-line and 2048-line checklist drafts for being a checklist instead of an explanation).
  64 sections x exactly 32 lines, one heading + 30 lines of prose + 1 blank. It contains real
  research: session-history forensics (§2-9: baseline repair + CJK damage, Repo Wiki + Qoder
  evidence, MAD restoration, skills vendoring, desktop-binary extraction, the naming cycle,
  restructure + gate + inbuilt bundle), the registry schema (§11), invariants and the
  consistency gate (§12), the alias ladder (§13), **provenance research** (§14-15), per-part
  research for every seat (§16-19, §33-51: Ingot, Aster/Onyx, Chromix, Codeix, GSX-CLI, Zingma,
  Sonar, Zenix), skills inventory/provenance/wiring (§52-54), the inbuilt bundle (§55-56),
  **reverse-engineering methodology** (§57-58: routing + evidence format), phases 0-4 (§59-63)
  and verification/risks/open questions (§64).
- **Source document:** `.plan/review-tracking/DRAFT.md` (145 KB, 64 sections).
- **Evidence status:** DISK-VERIFIED (registry `arch/windows.json` + gate 13/13 green). NOTE: the
  draft still describes the pre-2026-11-12 state (8 parts incl. Chromix, Onyx->Aster rename
  pending, Zenix CC) - it is the *research record*, the live truth is `code/arch/` + D-24..D-27.
- **Audit slots:** 1 of 3 done (Operation Clean / CF pass).

### R-06 · Reverse-engineering research (the 7 seats)
- **Scope:** MSIX/ASAR extraction + beautification + REA application graph for Codeix
  (ui-old/ui-new), Onyx (Qoder + official VS Code OSS 1.147.0), Zingma (Qoder Quest window),
  Zenix (Claude Desktop 5.1231.2 + Cowork VHDX sandbox), Sonar (DSH), Ingot (ZCode source),
  GSX-CLI (opencode/MiMoCode). Exact ASAR sha256 vs MSIX match; 21,791 ASAR files in ui-new.
- **Source document:** `.rea-tmp/codex/README.md` + `evidence/*.json`; `.plan/docs/operation-clean/DECISIONS.md`.
- **Evidence status:** DISK-VERIFIED for extraction (byte-exact); branding/RE gaps remain.
- **Audit slots:** 1 of 3 done.

### R-07 · Effort slider reverse-engineering (DSH plugin)
- **Scope:** `dsh-claude-effort-slider` v0.9.4 - 6-stop slider, 4 real effort values, DSH
  `directory.select({reasoningEffort})` write path, cordis slot `conversation.input.right`,
  fail-open DOM anchors, 38/38 tests.
- **Source document:** `code/slider/effort/` (lib/client.js 1682 lines, cordis.patch.yml,
  test/client.test.mjs, ANIMATION.md).
- **Evidence status:** DISK-VERIFIED; Zenix port shape A/B still open (parked, D-25).
- **Audit slots:** 1 of 3 done.

### R-08 · Claude Code effort-slider archaeology
- **Scope:** CLI 2.1.251 / 2.1.302 / 2.1.319 and extension 2.1.302 / 2.1.319 / 2.1.322 -
  `EffortSlider` appears in CLI 2.1.302 and extension 2.1.319, never removed; the real
  "expiry" is the server-side `supportsEffort` capability gate. 5 levels, `max` included,
  per-model `effort_cost_index`.
- **Source document:** this session's forensics (recorded in the plan and PROGRESS.md).
- **Evidence status:** PAPER-ONLY (binary grep of shipped builds; not independently re-run).
- **Audit slots:** 1 of 3 done.

### R-09 · Deleted-docs recovery (the 2026-10-07 purge)
- **Scope:** commit `9c0e480` (98 files, 77 md) + `f6ee292` (34 files) in the engine repo,
  and the earlier `85d2ce167` purge in the launcher repo; what survived, what was recovered.
- **Source document:** `.plan/_archive/` (288 files, 10.6 MB) + D-26.
- **Evidence status:** DISK-VERIFIED (recovered from git history; `InNova.png` stays deleted).
- **Audit slots:** 1 of 3 done.

### R-10 · Workspace rename + superproject git recovery (2026-11-12)
- **Scope:** `code-fusion/` -> `code/`, `transformers-fusion/` -> `transformers/`, remotes ->
  `code.git` / `transformers.git`, 93-file path sweep with quote-safe rules, superproject repo
  re-init with full remote history adopted (8 commits), `.gitmodules` path fix, `.plan` tracked.
- **Source document:** D-24, D-27, `.plan/telemetry/DASHBOARD.md`, fusion git log.
- **Evidence status:** DISK-VERIFIED (git log + gate 13/13 + 7 verifiers green).
- **Audit slots:** 1 of 3 done.

---

## B. Research in progress / pending (operator-owned or queued)

### R-11 · INT x FP programme (the operator's current research topic) - ACTIVE
- **Scope:** the complete INT-vs-FP research programme: difference INT vs FP; what is already
  implemented in this project; what can be touched/improved; the unique format style applied to
  both families; best-in-every-dimension outcome and how to build it; **codebook merger**
  (ternary {0,-1,+1} vs binary {0,1} - a sovereign stack?); **measurement normalization**
  (TFLOPS for FP vs TOPS for INT).
- **Source document:** `.plan/DRAFT.md` (627 lines, 15 sections + §16 operator questions).
- **Evidence status:** the code audit inside the draft is DISK-VERIFIED (8/8 files, 3/3 symbols
  re-checked on 2026-11-12); the literature half is PAPER-ONLY and needs the browser pass.
- **Audit slots:** 1 of 3 done (draft audit) - 2 browser/research passes PENDING.

### R-12 · Loop Quantization (Track B) - never implemented anywhere
- **Scope:** loop-aware quantization as a compute contract; LoopQ (`2605.16343`) and LoopQuant
  (`2610.16368`) results are at ~4 BPW, our target is 1.0 BPW (D-27) / 1.5 BPW (implemented
  state); loop-entry adapter fails first on INT4; no looped-model fix validated above a few-B
  parameters.
- **Source document:** master plan §5f, §9b.2 Track B.
- **Evidence status:** PAPER-ONLY.
- **Audit slots:** 0 of 3.

### R-13 · Mix Quantization
- **Scope:** mixed-format / bit-mixing quantization literature; the MX family (14 formats)
  measured and quarantined; mixed-precision allocation already implemented in Q_MX/Q_G_MX.
- **Source document:** master plan §9b.1-§9b.2, LADDER.md (MX rows), DECISIONS D-13.
- **Evidence status:** PARTIAL - measured, but the mix-strategy literature pass has not been done.
- **Audit slots:** 0 of 3.

### R-14 · NCM - Next-Concept Modeling (arXiv 2610.14162)
- **Scope:** the generation mechanism; §3b spec already extracted from the HTML; Appendix F.1.1
  and I still unread; merger with DSpine (§3c) pending.
- **Source document:** master plan §3b, §3c.
- **Evidence status:** PAPER-ONLY (partly extracted) - needs the full browser read.
- **Audit slots:** 0 of 3.

### R-15 · EAIN (Enhanced Artificial Intelligence Neurons)
- **Scope:** literature basis (§5c.4), the honest ceiling, scoping to the implementable subset
  (per-unit importance/decay + thresholded activation + local plasticity), and choosing which
  of the three parallel continual-learning stacks it sits on.
- **Source document:** master plan §4.8a, §4.9, §5c.4.
- **Evidence status:** PAPER-ONLY for the literature; the design is OPEN-DESIGN.
- **Audit slots:** 0 of 3.

### R-16 · Inferno (kernel + training engine)
- **Scope:** full file-by-file breakdown of the Inferno kernel and the training engine,
  including the DSpine/NCM generation paths, the 7 CRITICAL defects register (§10M) and the
  bench-honesty gates.
- **Source document:** `transformers/inferno/`, master plan §10M, §10K.
- **Evidence status:** not yet started - this is the T8 deep-breakdown to-do.
- **Audit slots:** 0 of 3.

### R-17 · Publishable research report (PDF + DOCX, 512 pages)
- **Scope:** the same data in two extensions (PDF and DOCX), ~512 pages, produced from the
  completed research above; the operator audits the whole set 3x.
- **Source document:** T13 - generation happens once the operator's content lands.
- **Evidence status:** not started (operator-owned content).
- **Audit slots:** 0 of 3.

### R-18 · The three project READMEs (publishable depth)
- **Scope:** the operator's documentation standard - `fusion/README.md` 4,096 LOC,
  `code/README.md` 2,048 LOC, `transformers/README.md` 6,144 LOC, each written in prose with
  average code snippets, each surviving a three-pass publishability audit. The superproject
  README was deleted with everything else on 2026-10-07 and never restored; the engine README
  is being rebuilt from the code.
- **Source document:** `.plan/telemetry/build_tf_readme.py` (generator + strict validator),
  `transformers/README.md` (batch 1, sections 1-40, 1,627 LOC), `fusion/README.md`,
  `code/README.md`.
- **Evidence status:** DISK-VERIFIED by construction - the generator extracts counts, format
  names, backends, targets and tests from the tree at build time, so a number in the README
  cannot drift from the code. The validator **refuses to write** unless every section carries 30
  narrative lines (tables and code do not count), which makes padded blank lines impossible.
- **Audit slots:** 1 of 3 (batch 1 of 4 for the engine README; the other two READMEs pending).

---

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
| `review-tracking/QODER_REPO_WIKI_RE.md` | 10,137 | Qoder repo wiki reverse-engineering |
| `review-tracking/workflow_extracted/INDEX.md` | 13,442 | Extracted workflow index |
| `fusion-full-review-retry-queue.md` | 10,351 | Full-review retry queue |
| `transformers-fusion-spec-inferno-md-pla-pure-parrot.md` | 8,643 | SPEC-INFERNO implementation plan |
| `BLUEPRINT.md` | 5,886 | Superproject blueprint + workflow pipeline |
| `telemetry/DASHBOARD.md` | 6,672 | Live dashboard (regenerated) |
| `telemetry/TODO-TREE.md` | 8,475 | The grind queue (T1..T13) |
| `.draft/deep-research-report.md` | 17,387 | Draft research report (basis for the publishable package) |

Everything under `.plan/_archive/` (288 files) is **reference-only**: recovered docs, never
overridden (D-26). Everything under `.plan/.rea-tmp/` and `.plan/.extract-tmp/` is scratch.

---

## D. Audit protocol for each research item

| Pass | Who | What |
|---|---|---|
| 1 | Agent | Produce the research; every claim carries command + output + file:line |
| 2 | Agent | Re-verify against disk independently; fix every discrepancy found |
| 3 | Operator | Publishability review - is it complete, honest, and defensible? |
| 4+ | Agent | Fix whatever the operator rejects; re-run the verifiers; regenerate the dashboard |
