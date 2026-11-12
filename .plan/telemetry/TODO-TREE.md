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

- [ ] T1.1 **G/S design note** (OPEN-RESEARCH #4) — deep-read §5 papers (2603.10123, 2603.15031,
      2605.18855, 2610.13630, 2607.27230, 2607.09694, 2606.18524, 2610.00673, 2605.16343,
      2610.16368) via browser → written design note in plan §5c
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
- [ ] T3.2 TransCenderIDX wire-magic ruling (THEOREM_CENDER.md + `quant_format.cpp:640`) —
      operator ruling required, wire format NOT touched without it
- [ ] T3.3 Verify igpu_zero_copy.cpp:1127 5th-attention-site KAT entry landed (fix_igpu_audit)
- [ ] T3.4 install_test duplicate header ruling (magic_size_=15 deliberate stale fixture vs fix)
- [ ] T3.5 **Security audit 1/10** — quant wire path: memcmp NUL bug (SolIDX 6-vs-7), legacy
      alias parser backcompat, writer assert-validity (L4 sub-step)

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
- [ ] T6.3 Fix **V20** — `code_gen.cpp:236` 2048-token stack overflow (7th CRITICAL, untested
      path) + caller `:825 spec.M` clamp
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
