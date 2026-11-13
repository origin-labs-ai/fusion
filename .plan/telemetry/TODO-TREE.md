# Fusion Superproject — Grind To-Do Tree

> Operator rule (2026-11-12): *"ek specific to-do ko pakarenge, uske sub-to-dos banayenge,
> poora ek task ko hi aisa ragar ke karenge ki kuchh bhi chhootne naa paaye — jaise ki research
> ke baad sab bugs, problems sab solve honge, 5 se 10 security audits honge, sab fix hoyenge,
> fir Inferno par gaye to poora Inferno ka detailed breakdown nikalega, ghis-ghis ke poore isi
> to-do ko aise complete kar lenge ki isme kuchh chootne naa paaye and shayad origin requirement
> se bhi better bane!"*
>
> Rules of engagement: NO subagents · one to-do to 100% before shifting · dashboard after EVERY
> step (`python .plan/telemetry/gen_dashboard.py`) · research via in-app browser
> (`/browser-use:control-in-app-browser`) — if a site won't open, operator provides content ·
> never weaken a test · every claim carries command+output+file:line.
>
> **Remember: Loop Transformers and Loop Quantization are DIFFERENT things** — do not conflate.


> ---
> **OPERATOR REMINDER (2026-11-12 - read this whenever you implement anything):**
>
> 1. **MAIN GOAL = the ENTIRE Fusion Superproject.** Every domain, every seat, every track -
>    all of it complete. This project is NOT just quantization; quantization is one track of it.
> 2. **SIDE GOAL = achieve the MAXIMUM at EXACT 1.0 BPW - not 1.5 BPW.** The implemented 1.5 BPW
>    path is a *stepping stone*; the real target is **1.0 BPW**. Older sections that say "1.5 BPW"
>    stay true as implemented-state facts - the GOAL line is 1.0.
> 3. **FP + INT research note (operator, same-day research):** BOTH quantization format families -
>    FP (floating point: FP8/FP4/E5M2 style) and INT (integer: INT4/INT8/binary/ternary) contain
>    actionable work. Research both; do not drop either.
> 4. **FACT (2026-11-12 audit):** Loop Quantization has NEVER been implemented for any model,
>    anywhere. Track B will be the world's first implementation.
> 5. **Current situation (exact):** Loop Quant Track B open - Mix Quant partial (MX family
>    quarantined) - NCM Appendix F.1.1/I read pending - EAIN design open. We WILL implement and
>    complete all of it - grind method (`.plan/telemetry/TODO-TREE.md`), dashboard after every
>    step (`.plan/telemetry/DASHBOARD.md`).
---

## T1 · Loop Transformers (research close-out)

- [x] T1.1 **G/S design note** (OPEN-RESEARCH #4) — deep-read §5 papers (2603.10123, 2603.15031,
      2605.18855, 2610.13630, 2607.27230, 2607.09694, 2606.18524, 2610.00673, 2605.16343,
      2610.16368) → **DONE 2026-11-13: design note written as master-plan §5c.6** (8 G-statements
      + 6 S-statements, every fork tagged to its ledger id; abstracts fetched live 2026-11-13)
- [ ] T1.2 Loop-exit policy decision (OPEN-DECISION #6) — evidence note → operator ruling
- [ ] T1.3 S/G depth-axis variant pick (OPEN-DECISION #13)
- [ ] T1.4 Loop-µP ×1/N scaling ruling (#16) · T=2 fixed-depth baseline (#17) · exit-distribution
      assert (#18) · curriculum pick (#19) · inactive-token skip (#20)
- [ ] T1.5 U-curve on WEIGHT-TIED looped model (OPEN-UNKNOWN #11) — experiment design + run
- [ ] T1.6 Stability above few-B params (OPEN-UNKNOWN #23) — literature + experiment design
## T2 · Traditional Transformers (baseline side)

- [ ] T2.1 §5d market-scan refresh (any 2026-11 papers missed) — browser pass
- [ ] T2.2 Baseline bench spec (§9) — traditional vs looped head-to-head protocol
## T3 · Traditional Quantization (Track A — the ladder)

- [ ] T3.1 Quality floor rulings: D-12 scale fitting · D-13 MX quarantine · D-14 bench honesty
- [x] T3.2 TransCenderIDX wire-magic ruling (THEOREM_CENDER.md + `quant_format.cpp:640`) —
      **RESOLVED 2026-11-13 (D-30)**: the engine `.idx` accepts `Transformers-FusionIDX` (22 B,
      current) and `TransCenderIDX` (15 B, formerly known as) only; `SolIDX` and `InNovaIDX` are
      rejected. `SolIDX` is reserved for model manifests
      (`transformers/docs/MODEL_MANIFEST.md`). Test 8 proves the accept/reject split
      (28 tests, 0 failures).
- [x] T3.3 Verify igpu_zero_copy.cpp:1127 5th-attention-site KAT entry landed (fix_igpu_audit)
      — **VERIFIED 2026-11-13**: the KAT-layer inventory §2.1b.1 GPU-backends row carries the
      corrected entry (5th attention implementation in `src/backend/`; 4 fused + 1 composed + 15
      primitive-only), post-loop audit row 2965 documents the fix.
- [ ] T3.4 install_test duplicate header ruling (magic_size_=15 deliberate stale fixture vs fix)
- [x] T3.5 **Security audit 1/10** — quant wire path: memcmp NUL bug (SolIDX 6-vs-7), legacy
      alias parser backcompat, writer assert-validity (L4 sub-step) — **AUDIT DONE 2026-11-13**:
      SolIDX 6-vs-7 = CORRECT at the time (no bug); **D-30 (2026-11-13) then retired `SolIDX`
      from the wire path entirely** — only `Transformers-FusionIDX` / `TransCenderIDX` remain;
      writer assert-validity was documented but never
      implemented → FIXED (write_block + write_format_table throw on invalid/retired ids);
      MoE format-table label bug LIVE at moe_model.cpp:414 (Q_8 label over raw FP32) → FIXED
      (writes Q_32, payload truth); QuantIDXReader truncated-header overread → FIXED (per-magic
      size gates 30/23 + header-bounds guard). Regression: `test_sha256_corrupt` Test 7
      (23/0 pass). Remaining audit items 2–10 (quant_import/adapter paths, benches, inferno
      writer, install_test dup header, MoE/production label reads) are separate to-dos.
## T4 · Loop Quantization (Track B — compute contract)

- [ ] T4.1 Research: LoopQ/LoopQuant at **1.5 BPW** feasibility note (browser — their numbers
      are ~4 BPW; what survives at 1.5?)
- [ ] T4.2 Design: loop-aware quant track spec (§9b.2 Track B → written design)
- [ ] T4.3 Shared-vs-separate weights ruling (OPEN-DECISION #5) — sets parameter count
- [ ] T4.4 KV-cache policy for T loops (OPEN-DECISION #22) — naive vs shared-KV (15→4 sets)
## T5 · Mix Quantization

- [ ] T5.1 **Research pass (browser)**: mixed-format / bit-mixing quantization literature —
      the one thin area in the audit
- [ ] T5.2 MX family ruling (D-13 quarantine vs fix) informed by T5.1
- [ ] T5.3 Security audit 2/10 — MX quarantine enforcement (no MX id sneaks into wire path)
## T6 · DSpine × NCM merger

- [ ] T6.1 NCM full read — arXiv 2610.14162 Appendix F.1.1 + I (OPEN-RESEARCH #10) — browser
- [ ] T6.2 DSpine §3c spec × NCM §3b spec → **merger design** (one generation mechanism doc)
- [x] T6.3 Fix **V20** — `code_gen.cpp:236` 2048-token stack overflow (7th CRITICAL, untested
      path) + caller `:825 spec.M` clamp — **DONE 2026-11-13**: heap score buffer (std::vector,
      real seq_len), V20 loud boundary gate (seq_len>2048 / non-positive shapes throw), caller
      clamp comment, attention_basic template heap buffer, 12 regression rows
      (`test_code_gen::test_attention_v20_budget`). Evidence: build-norm 60/60 tests pass;
      emitted 2048 kernel compiles clean at /W4 (clang-cl); gate `test_code_gen` Passed.
- [ ] T6.4 Security audit 3/10 — generation paths (V20 class: JIT-emitted C++ bounds)
## T7 · EAIN

- [ ] T7.1 Scope to implementable subset (OPEN-DESIGN #7) — per-unit importance/decay +
      thresholded activation + local plasticity
- [ ] T7.2 Stack choice ruling (OPEN-DECISION #8) — which of the 3 parallel stacks EAIN sits on
- [ ] T7.3 Bench wiring (CS-Bench / D&CC-Bench / MQC-Bench parity targets §4)
## T8 · Inferno deep breakdown (after T1–T7)

- [ ] T8.1 Full Inferno kernel + training-engine breakdown (file-by-file, call graph)
- [ ] T8.2 Security audit 4–10 across Inferno (memory-safety, dead code, bench honesty)
- [ ] T8.3 Gap review vs origin requirement → close every miss
## T9 · Cross-cutting

- [ ] T9.1 Dashboard after EVERY step (regen + paste in chat)
- [ ] T9.2 All 7 verifiers green at every checkpoint
- [ ] T9.3 Ledger tags updated as items close (nothing silently open)
- [ ] T9.4 **GRAPHIFY reminder (operator, 2026-11-12): regenerate the full `fusion/` graph** with
      the graphify skill (both component repos + `.plan` in scope; `graphify-out/` is git-ignored
      output). The operator explicitly deferred this: "Graphify waala jo kaam hai use bhi document
      hi kar dena as reminder ki ye bhi karna hai" - so this line is the reminder; run it when
      the operator says so (or as part of the next context-recovery refresh).

---

**Execution order:** T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8 (T9 runs throughout).
Dashboard checkpoints: after each T-item completion.
## T10 · READMEs to publishable depth (operator targets, D-31 2026-11-13)

> **EXACT targets (D-31):** `fusion` **2,048** · `code` **4,096** · `transformers` **6,144** LOC.
> `wc -l` must equal the target exactly. Visual reference: `origin-router/README.md` (centred
> header, SVG logo, shields.io badges, nav links, emoji sections, tables, minimal snippets).

- [x] T10.1 `fusion/README.md` -> **2,048 LOC** (superproject face; minimal snippets) - exact,
      generated by `.plan/telemetry/docgen/build_fusion_readme.py`, pushed.
- [x] T10.2 `code/README.md` -> **4,096 LOC** (CodeFusion; minimal snippets) - exact, generated
      by `.plan/telemetry/docgen/build_code_readme.py`, pushed.
- [x] T10.3 `transformers/README.md` -> **6,144 LOC** (engine; minimal snippets) - exact,
      generated by `.plan/telemetry/docgen/build_tf_readme.py`, pushed.
  - [x] T10.3a **Generator + strict validator** (`.plan/telemetry/build_tf_readme.py`) - builds from
        live extraction, **refuses to write unless every section carries 30 narrative lines**;
        tables/code do not count as narrative. No padded blanks, no filler.
  - [x] T10.3b **Batch 1 - orientation & subsystems (sections 1-40, 1,627 LOC)**: what the engine
        is, how to read the document, repo layout, the two engine trees, build system, the 20
        executables, 26 libraries, 76 tests, git state, dtype contract, the two format counts, the
        registry, block codec, codebook, quant engines, QAT, INT path, FP path, FP8 special values,
        FP8 attention path, backends, GPU capability contract, model, attention, KV cache,
        inference, trainer, code generator, MoE/multimodal, AGI/continual, telemetry, production,
        tokenizer, distributed, optimizer, continual, inference-optimisation, math, GLE, native
        weight path.
  - [x] T10.3c Batch 2 - the quantization deep dive (formats, ladder, INT/FP families, codebook
        merger, sovereign stack) - generated from live facts, sections 41-100.
  - [x] T10.3d Batch 3 - training engine / Inferno / generation mechanisms - generated from live
        facts, sections 101-150.
  - [x] T10.3e Batch 4 - inference, serving, benches, gates, build, contributing, roadmap -
        generated from live facts, sections 151-191 (191 x 32 + 32-line header = 6,144).
- [ ] T10.4 Standard: "every detail, opened up" - operator will run research audit x3 for
      publishability; docs must survive that scrutiny.
- [x] T10.5 Style pass: SVG logo per repo + shields.io badges + centred header + emoji nav,
      matching the `origin-router` README's alignment and tone - logos committed in all three
      repos; the generated headers carry the badges and navigation.
- [x] T10.6 Exactness validator: each generator asserts `wc -l == target`, zero placeholder
      markers, zero blank-padding runs; failure means no write.
- [x] T10.7 Commit the generators under `.plan/telemetry/docgen/` (deterministic, live-tree facts).
## T11 · _archive mining -> .plan/ (operator: "wahan se bhi saara docs uthaana hai")

- [ ] T11.1 Inventory `.plan/_archive` (md/pdf/docx counts, duplicate detection)
- [ ] T11.2 Mine EVERY doc; rename ours to current naming (Sol 4 Flash etc.) and copy into
      `.plan/` under a clean tree - **never override an existing file** (D-26 rule holds)
- [ ] T11.3 Cross-link mined docs from master plan + BLUEPRINT
## T12 · PDF completeness audit (transformers git + superproject fetch)

- [ ] T12.1 List every PDF that ever existed in `transformers/` git history
      (`git log --all --diff-filter=AD -- '*.pdf'`)
- [ ] T12.2 Compare vs disk + `.plan/_archive`; recover missing ones from history
- [ ] T12.3 Same check on the superproject repo history (fetched origin/main)
- [ ] T12.4 Per-doc status report: in-git / recovered / missing
## T13 · Publishable research package (operator-led; support on request)

- [ ] T13.1 Research audit x3 for publishability (operator is running this)
- [ ] T13.2 Research report **PDF + DOCX** - same page-block model, **exactly 512 pages each**,
      designed cover page, TeX typesetting for the PDF, `python-docx` for the DOCX (D-31)
  - [ ] T13.2a Cover + title page + document-control page + manual TOC (looks-first)
  - [ ] T13.2b Body: superproject, D-01..D-30, engine, quantization ladder, seats, research,
        operations, roadmap
  - [ ] T13.2c Appendix: annotated source-file cards fill the page count to exactly 512
  - [ ] T13.2d Verify with `pdfinfo` (PDF) and Word COM -> `pdfinfo` (DOCX); both must read 512

## T14 · Repository hygiene (operator: "jo karna hai fix wo kar de", 2026-11-13)

- [x] T14.1 Register the submodules properly (`git submodule init` + `absorbgitdirs`; remove the
      ambiguous `-` status and the nested full `.git` directories) - both `.git` entries are files
      pointing at `.git/modules/<name>`, and `git submodule status` has no `-`.
- [x] T14.2 `.gitmodules`: `code` branch `master` -> `main` (the checkout is on `main`)
- [x] T14.3 Untrack backup/scratch artifacts (`.bak-*`); add ignore rules; keep files on disk
- [x] T14.4 Commit the transformers WIP (84 modified + 89 untracked) and push `code` (ahead 1) -
      transformers WIP landed in `e63e2b5`; code pushed.
- [x] T14.5 Update superproject gitlinks to the new submodule commits and push all three repos -
      `code` 1e72c52e0, `transformers` 2335058, fusion pushed.
- [x] T14.6 Fix documentation path drift (README says `.plan/telemetry/BLUEPRINT.md`; the file is
      `.plan/BLUEPRINT.md`) - scan found zero `.plan/telemetry/BLUEPRINT.md` references; the only
      hit was this TODO entry.

## T15 · Documentation verification + telemetry

- [x] T15.1 `wc -l` proof for all three READMEs (2048 / 4096 / 6144) - `fusion` 2,048, `code`
      4,096 and `transformers` 6,144 are exact and pushed.
- [ ] T15.2 `pdfinfo` proof for both 512-page artifacts
- [ ] T15.3 Manifest (`docgen/manifest.json`) + dashboard section + TODO checkboxes updated
- [x] T15.4 All 7 plan verifiers green after the docs build; regenerate dashboard - 7/7 PASS,
      `rows=125 headings=125 gaps=13`, code gate 13/13, dashboard regenerated.

**Execution order:** T14 -> T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8 -> T10 -> T11 -> T12 -> T13 (T9 and T15 run throughout).
Dashboard checkpoints: after each T-item completion.
