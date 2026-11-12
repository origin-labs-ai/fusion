# Fusion Superproject - Telemetry Dashboard

> **GOAL LINE:** MAIN goal = the ENTIRE Fusion Superproject. SIDE goal = MAXIMUM at **EXACT 1.0 BPW** (not 1.5 - that path is the stepping stone). FP + INT both research. Loop Quant never implemented anywhere before - Track B is the first. Details: `.plan/docs/operation-clean/DECISIONS.md` D-27.

> Generated: **2026-11-12 19:08:59** - regen: `python .plan/telemetry/gen_dashboard.py`

## 1. Plan verifiers (live run)

| Verifier | Exit | Verdict |
|---|---|---|
| `verify_step1.py` | 0 | **PASS**   rows=120  headings=120  gaps=13 |
| `step2_fix2_verify.py` | 0 | **PASS** STEP 2 ALL CHECKS PASSED |
| `step3_verify.py` | 0 | **PASS** report     : C:\Users\thaku\Workspaces\fusion\.plan\.rea-tmp\step3_anc |
| `step3_subanchors.py` | 0 | **PASS** wrote C:\Users\thaku\Workspaces\fusion\.plan\.rea-tmp\step3_subanchors |
| `verify_step5.py` | 0 | **PASS** STEP 5 ALL CHECKS PASSED  (65 checks) |
| `step6_audit.py` | 0 | **PASS** STEP 6 AUDIT PASSED |
| `arxiv_recheck.py` | 0 | **PASS** report: .plan/.rea-tmp/arxiv_recheck.json |

**Gate: ALL GREEN**

## 2. Code repo gate

check-consistency: exit=0 **13/13 checks passed**

## 3. Repos (working tree)

| Repo | Modified | Untracked | Remote |
|---|---|---|---|
| `code` | 5759 | 45 | `origin-labs-ai/code.git` |
| `transformers` | 28 | 92 | `origin-labs-ai/transformers.git` |

> Working tree holds peer-session work - **no commits without operator order.**
>
> code/windows shows tracked-file deletions by design/history: chromix 3,687
> (intentional, integrated browser = Codeix), gsx-cli 2,053 (peer seat refresh in
> flight - disk has 1,503 files + 2,093 untracked, HEAD recoverable), zenix-cc/codeix
> renames. Disk intact: 239,227 files, all 9 seats present.

## 4. Phase-0 ledger (master plan)

- OPEN-DECISION: **15**
- OPEN-RESEARCH: **2**
- OPEN-DESIGN: **1**
- OPEN-UNKNOWN: **2**
- OPEN-ACTION: **1**
- RESOLVED (tagged 2026-11-12): **29**

> Bullet tags in the Phase-0 section (ledger table in 11 mirrors them).

## 5. Research domain coverage (audit 2026-11-12)

| Domain | Status | Evidence |
|---|---|---|
| Loop Transformers | **DONE** | 5d taxonomy/attention/training + 5e attention-residuals + papers (Loopback/LoopQuant/OASIS/ASTRA/2603.10123) verified 2026-11-10 |
| Traditional Transformers | **DONE** | 5d same pass - baseline/attention/training comparison + market scan |
| Traditional Quantization (Track A) | **DONE** | 69-format ladder contract (LADDER.md), 1.5 BPW path (9b.1), Operation Clean implemented |
| Loop Quantization (Track B) | **RESEARCH-DONE / TRACK-OPEN** | 5f+9b.2 evidence read (LoopQ/LoopQuant W4A4); implementation track open; ~4BPW->1.5BPW gap + few-B-param ceiling flagged |
| Mix Quantization | **PARTIAL** | MX family (14 formats) measured + quarantined (D-13, -21..-37 dB); no dedicated mix-strategy literature pass yet |
| DSpine x NCM merger | **RESEARCH-DONE / NCM-READ-OPEN** | 3c DSpine full implementable spec (2026-11-09); NCM 3b spec extracted; Appendix F.1.1/I read remaining |
| EAIN | **LIT-DONE / DESIGN-OPEN** | 5c.4 literature basis + honest ceiling; OPEN-DESIGN (implementable subset) + OPEN-DECISION (which of 3 stacks) |

## 6. Parked (operator: 'Dono baad me karenge!')

- Sonar (DSH) effort-slider integration - D-25
- Zenix (Claude Desktop) effort-slider port (A DOM-inject / B native) - D-25
- Git commits for both repos - awaiting order

## 7. Open ledger items (the grind queue)

1. **[OPEN-RESEARCH]** Deep-read the §5 papers; produce a written design note for `G` and `S`.
2. **[OPEN-DECISION]** Resolve: whether transformed layers use **shared weights** (one set, both modes) or **separate weigh
3. **[OPEN-DECISION]** Decide the **loop-exit policy** (learned gate vs post-hoc confidence readout — §5 evidence favours t
4. **[OPEN-DESIGN]** Design **EAIN** scoped to the implementable subset only (§4.9): per-unit importance/decay + threshol
5. **[OPEN-DECISION]** **Decide which existing continual-learning stack EAIN sits on** (§4.8a): three parallel stacks exist
6. **[OPEN-RESEARCH]** **Research NCM** (§3b) — read arXiv `2610.14162` in full. **The §3b.6 spec is already extracted from
7. **[OPEN-UNKNOWN]** **Reproduce the step-0 U-curve on a WEIGHT-TIED looped model** (§5c.2, gap 5). The `2603.10123` dead
8. **[OPEN-DECISION]** **Decide the `G` formulation** — §5c.2 recommends **B (index-selected, `log m` normalisation) + C (d
9. **[OPEN-DECISION]** **Pick the `S`/`G` depth-axis variant** (§5e). The Attention-Residual family (`2603.15031`, `2607.18
10. **[OPEN-DECISION]** **Put `G` in the quantisation test set from day one** (§5f). OASIS (`2605.17887`) shows an extra dep
11. **[OPEN-DECISION]** **Default the routing to a small loop count and measure against a fixed-depth baseline** (§5d). The
12. **[OPEN-DECISION]** **Adopt the Loop-µP residual scaling on the looped path** (§5d.3.4, `2606.18524`): residual branch
13. **[OPEN-DECISION]** **Default the loop count to 2 and measure up to 4** (§5d.3.6). Two independent sources: Ouro's **T=8
14. **[OPEN-DECISION]** **Design the exit gate and monitor it directly** (§5d.3.2, `2510.25741`, `2610.00673`): `λ_t(x) = σ(
15. **[OPEN-DECISION]** **Use the correctness-directed online depth mask as our loop curriculum** (§5d.3.3, `2610.00673`): c
16. **[OPEN-DECISION]** **Make §5's routing per-token AND attention-work-reducing** (§5d.2 axis 3, §5d.5 item 5): inactive t
17. **[OPEN-DECISION]** **Decide our residual interface for the looped path** (§5d.3.4, `2611.07226`). Loop-µP's **× 1/N** a
18. **[OPEN-DECISION]** **Decide our KV-cache policy for `T` loops** (§5d.1 item 2, `2610.33360`). The naive choice is `T` s
19. **[OPEN-UNKNOWN]** **Add an OOD-stability gate, not just a loss gate** (§5d.4). The corpus reports looped models at **~
20. **[OPEN-DECISION]** Decide **where the harness talks to the engine** — the C++ `quant::agi::WorldModel` is complete but
21. **[OPEN-ACTION]** Deliverable: a design note in `transformers/` (which has no docs system — create one modelled on `co
