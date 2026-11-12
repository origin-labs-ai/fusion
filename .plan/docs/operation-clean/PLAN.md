# Operation Clean — Execution Plan

> Master task DAG for the Fusion quantization overhaul + review-then-fix execution.
> Source of truth for *order and gates*. Rules live in [DECISIONS.md](DECISIONS.md);
> the target format ladder lives in [LADDER.md](LADDER.md).
> This file is generated from the verified plan (`.claude/plans/cuddly-yawning-lamport.md`)
> and is updated in place as tasks complete — never rewritten.

## Non-negotiables (from the operator)

1. **Gate:** no implementation task starts until the review workflow `wf_ce1d51d7-91d`
   reports 100%. Verification phase + critic + final report must all land, or the
   documented *complete-by-reconstruction* fallback is invoked and recorded in
   [DECISIONS.md](DECISIONS.md).
2. **One task at a time, to 100%.** A task is done only when its DoD commands pass
   and no follow-up is left open. Most-strict-worker standard.
3. **Zero dead code / zero stubs**, except the documented ~18 unavailable GPU backends
   (keep + document accurately).
4. **Zero BPW violations**, project-wide. Direction is always **rewire the layout down
   to the name** — never rename a format up to the wire.
5. **`QUANT` all-caps only where structurally mandatory** (C/C++ macros, env vars).
   Everywhere else: `Quant` (lowercase namespace `quant` already fine).
6. Priorities within the DAG are mine (the implementing agent); the DAG itself is fixed
   except for insertions produced by the plan audit.

## Working state at plan time

| Item | State |
|---|---|
| Review workflow `wf_ce1d51d7-91d` | 240 results committed; verify votes 155 upheld / 59 refuted; critic + final-report never succeeded |
| Alternatives workflow `wf_b69ac10e-c2b` | Reverify + Rederive + Verdict; 25 failed labels re-derived with different lenses |
| Working tree | 10 dirty inherited files (disposition table in task P0.0) |
| `build-eng2` | ABSENT — recreated in P0.0 |
| Plan audit `wf_d9de5129-db7` | 5 section audits → completeness critic → enhancement merge |

## Task DAG

```
P0.1 workflow-wait + findings-reconcile
  → P0.0 working-tree triage + build-eng2 bootstrap
  → P0.2 planning docs (this directory)
  → P0.3 plan-audit integration (wf_d9de5129-db7 corrections)
  → S1 sc_f stack overflow
  → S2 quant_6k tail overrun
  → S3 kill the +1 byte allowance
  → S4 TF critical/high review findings
  → L1 types.h enum + validity table
  → L2 codec rewire + M/H encoders + ternary H
  → L3 registry / planner / inferno / ste_quantizer
  → L4 persistence compat (format_compat.h)
  → L5 consumers (adapter, import, benches consumers)
  → L6 model + production labels
  → L7 MX quarantine + 3.78125 → 3.50
  → T1 test migration + kCaps regen + wire-budget harness
  → Q1 wire fit_scale_true_mse (scale-fit quality)
  → Q2 bench honesty
  → Z1 zero dead code
  → Z2 casing QUANT → Quant
  → Z3 README / docs rewrite
  → V1 final verify + dominance bench
  → R1 TF security findings → R2 TF correctness → R3 TF build
  → R4 CF criticals → R5 CF highs → R6 CF mediums
```

### Why this order

- **P0 first**: nothing is safe to edit until the tree is triaged and a green baseline
  build exists (a rewire with a broken baseline is unattributable).
- **S\* before L\***: memory-safety and contract bugs are independent of the ladder and
  must not be lost inside a 69-format rewrite; they also make the later fuzz/tail tests
  meaningful.
- **L1 → L2 → L3 → L4 → L5 → L6 → L7**: enum first (everything else reads it), then
  codecs (wire truth), then everything that *maps* to the enum, then persistence
  (the only consumer that can silently corrupt data), then outward to labels.
- **T1 after L\***: caps and pins can only be regenerated once the ladder is final.
- **Q\*, Z\* after T1**: quality and hygiene edits must run against the final test gate,
  otherwise T1's pins go stale twice.
- **V1 before R\***: the dominance bench must prove the ladder; review findings come
  last because R4–R6 (code-fusion) are independent of the quantization work and are
  pausable without stranding the engine.
- **block_codec.cpp is touched by S1, S2, L2, Q1, Z1, Z2** — strictly serialized, so
  no two tasks in one session ever overlap in that file.

## Task register

DoD column abbreviations resolve as:
- **cfg** = `cmake -S . -B build-eng2 -G Ninja -DCMAKE_BUILD_TYPE=Release -DQUANT_BUILD_ADAPTERS=ON -DQUANT_BUILD_TESTS=ON -DQUANT_BUILD_BENCHMARKS=ON -DQUANT_BUILD_TOOLS=ON`
- **gate** = `ctest --test-dir build-eng2 -R "test_format$|test_all|test_fuzz_codec|test_format_audit|test_format_registry_complete|test_quant_mix|test_mix_components|grp_proof_test|test_wire_budgets" --output-on-failure`
- **full** = `ctest --test-dir build-eng2 --output-on-failure -E test_paged_kv_4m`

| ID | Task | Primary files | DoD |
|---|---|---|---|
| **P0.1** | Workflow-wait + findings reconcile | `review-tracking/*` | Workflow at 100% (or reconstruction recorded); `findings_verified.json` totals match runtime counts; DEFECTS.md entries carry final verdicts |
| **P0.0** | Working-tree triage + build-eng2 | 10 dirty files, `CMakeLists.txt` | Disposition table written for every dirty file (keep / revert / finish); `build-eng2` configured; `ninja -C build-eng2` green; `full` green before any edit |
| **P0.2** | Planning docs | `docs/operation-clean/{PLAN,LADDER,DECISIONS}.md` | All three exist; every operator rule appears verbatim-traceable in DECISIONS.md; LADDER has the complete id/name/BPW table |
| **P0.3** | Plan-audit integration | this file + DECISIONS.md | Audit corrections applied; new tasks inserted in DAG order; in-task edits merged into the task register |
| **S1** | `dequant_grp8_compound` sc_f overflow | `src/codec/block_codec.cpp:365-427`, `tests/` | `float sc_f[256]` made bound-safe (dynamic or `ng ≤ 256` guard in `fits()`); regression rows at n=8224 and n=32768 added to fuzz/audit; `gate` green; reachable paths (`adapter_core.cpp:199`, `probe_t4.cpp:15`) exercised |
| **S2** | `quant_6k` d-only tail overrun | `src/codec/block_codec.cpp:1146-1198` | Real budget test replaces `has_d = (n >= 8)`; raw pokes replaced with a checked write path (pattern of `quant_grp16:879-884` / `affine_budget_ok:1469-1479`); exact-byte budget holds at all 12 violating sizes {8..15,17,18,19,23}; `gate` green |
| **S3** | Kill the +1 byte allowance | `tests/test_fuzz_codec.cpp:278`, `tests/test_quant_mix.cpp:~175` | Allowance removed (strict `<=`); tests green only after S2; any remaining overrun surfaces as a failure, not a pass |
| **S4** | TF critical + high review findings | per finding, one task each | Each finding independently fixed with a regression test; DEFECTS.md marks it fixed with commit/file evidence; `full` green |
| **L1** | Format enum + validity table | `include/quant/types.h` | 69 surviving ids kept in place, 36 holes retired; `FORMAT_COUNT = 69`, `FORMAT_ID_SLOTS = 105`, `format_is_valid()` replaces ID-range predicates (`types.h:268-276`); all 98 legacy aliases removed; `format_name`/`format_bpw`/`format_nominal_bpw` cover exactly the valid set; every name == nominal == wire on the .0/.25/.50 grid; `gate` green with updated pins |
| **L2** | Codec rewire + M/H encoders + ternary H | `src/codec/block_codec.cpp` | Every wire literal cut to the name: 2.625→2.00, 3.5→3.0, 4.5→4.0, 8.5→8.0, 12.5→12.0, 16.5→16.0, 24.5→24.0, 6.5625→6.00, plus the K/half literals (:2753, :2772, :2791, :2833, :2865-2867, :2904-2922, :865). `Q_X_5 ≡ Q_G_X_5` duplicate pairs collapsed. M-tier encoder lands (refinement byte per 32 weights) with PSNR strictly between L and H on 4 fuzz distributions + real weights. `Q_1_K_H` ternary encoder lands at exact 1.50 (n=256: 16b FP16 scale + 368b base-3 trits + 24 implicit-zero slots = 384b) with per-size Diophantine tail sizing and never-inflate fallback. `k_tier()` rewired off name-string parsing to id/enum logic (`:2464-2470`); `Q_16_K`/`Q_24_K` trios split from the shared body (`:2740-2743`). `gate` + `full` green |
| **L3** | Registry / planner / inferno / ste_quantizer | `format_registry.{h,cpp}`, `format_planner.cpp:74`, `inferno.h:34-74`, `inferno_format_info.cpp:19-57`, `ste_quantizer.cpp:319-391` | `format_to_regformat()` no longer lossy (GRP/K/K_G/MX distinct, half twins collapse correctly, `Q_MX_* → Q_G_MX_*` fixed at `:233-239`); every valid format reachable via `parse_format_name` / `get_single_format` / `select_best*` / `get_format_table` (silent-default-on-miss becomes loud failure); inferno duplicate tables merged to one truth; `INFERNO_NUM_FORMATS` derived, not a dropped-index trap; planner + ste_quantizer consume `format_bpw` instead of their own literal ladders; `regformat_nominal/wire_bpw` wired or deleted |
| **L4** | Persistence compat | `include/quant/format_compat.h`, `quant_format.cpp`, `qwen35_engine.cpp` | `kFormatValid[105]` single truth; `wire_format_valid()` used by all 4 clamp sites (`quant_format.cpp:456`, `:611`, `qwen35_engine.cpp:33`, `:147`) replacing `wire_fmt < FORMAT_COUNT && wire_fmt != 19`; `legacy_format_id_remap()` on read (K_L→base, halves→`_K_H` same BPW: 73→12, 74→14 …) with one log line per file; writer asserts validity before write (catches the MoE label bug at write time); fixture: 105 ids × 1 block round-trips; `quant_format.h:23-27` stale "0..14" comment corrected; `gate` + `full` green |
| **L5** | Consumers | `adapter_core.cpp:319-420`, `quant_import.cpp:64-84`, `inferno_format_info.cpp`, benches | `write_quant_mixed` honors `cfg.target_bpw` (today ignores it, defaults `Q_G_2` at `:332`); import whitelist covers every valid format (today only Q_1/2/4/8/16/32, Q_G_{1,2,4,8,16}, Q_1_5, Q_G_1_5, 7 MX); format_planner/inferno/ste consume the single ladder; `gate` green |
| **L6** | Model + production labels | `src/model/moe_model.cpp:414`, `src/api/production_api.cpp:272,310,328-329,391` | `MoEModel::save` writes the payload's true format (today writes `format = 5` = Q_8 with raw FP32; compare correct `DenseModel::save:199`); ModelZoo reads the file's actual format instead of hardcoding "Q_8"; `gate` + `full` green |
| **L7** | MX quarantine + 3.50 | `types.h`, `format_registry.cpp:85-109`, MX encoders | `Q_G_MX_3_5` 3.78125 → exact 3.50; 14 MX formats marked quarantined in registry + docs (catastrophic −21..−37 dB root cause: 2-iteration-LS tier allocator); test pins updated; `gate` green |
| **T1** | Test migration + harness | `tests/*` | `FORMAT_COUNT==105` pins → 69 + validity iteration (`test_format.cpp:19`, `test_all.cpp:32`); `test_fuzz_codec` kFormats=105 → 69 with **measured** kCaps (3× worst of new tier over 4 distributions at n∈{256,1024}); 36 retired rows dropped; ternary ordering row + n=8224/32768 Q_G_8 regression; strict budgets at all 12 old overrun sizes; `test_quant_mix` 3.78125→3.50 pins; registry test `singles≥55` + retired names must FAIL parse; `format_master_table.py:22-24` 105-assert → validity parse; **new `tests/test_wire_budgets.cpp`**: every valid format × 15 sizes × 4 distributions, strict budget + PSNR floors that FAIL (tolerance 1e-4, not 1e-3; PSNR failure must actually fail); `test_trainer_engine.cpp` hunk in dirty `tests/CMakeLists.txt` compiles or is dropped; `gate` + `full` green |
| **Q1** | Scale-fit quality | `src/codec/block_codec.cpp:632-695` | `fit_scale_true_mse` wired into Q3/Q6/Q12 + Q2/Q4 (or deleted if superseded by golden-section); header comment `:622-627` made true; golden-section extended beyond `comp8_fit_scale_fp16:306-358` where it wins; measured Q_12 gap to K_H (46 dB → ≥59 dB) closed or explicitly justified; Q_G_12 vs Q_G_8 inversion gone; `gate` green + quality numbers recorded |
| **Q2** | Bench honesty | `bench/*` | `write_quant_mixed` target_bpw honored end-to-end (every "Mixed 1.50" row really writes 1.50); `bench_industry_real.cpp:904` OOB `pick(rs, q_ids, 7)` fixed (array has 6); QUANT-vs-industry rows compared on the same byte basis; `bench_quant_loss:140` hardcoded prose replaced with measured output; `plot_comparison_charts.cpp:12-42` 30 hardcoded rows and `bench_compare:475` hardcoded composition removed or fed from data; `bench_poc` false "No external schemes" removed; `bench_format_comparison:492-494` honest comment kept, fields corrected; benches rebuild and run clean. **Q-10 (bitnet bench rewrite) stays CANCELLED** |
| **Z1** | Zero dead code | repo-wide | Every symbol greps to zero or is wired: `fit_scale_true_mse` (unless Q1 wires it), `grp16_pad_fits`, `format_codebook_size`, `format_to_dtype`, `regformat_nominal_bpw/wire_bpw`, `data_start_`, `blob_index_`, `QUANT_FORMAT_COUNT=15`, inferno duplicate table, TWI paths. **Exception:** ~18 unavailable GPU backends kept + documented accurately. `knip`/grep evidence recorded |
| **Z2** | Casing QUANT → Quant | repo-wide | Every remaining ALL-CAPS `QUANT` token is macro or env var only. Type renames (~60): `QUANTReader/QUANTWriter/QUANTHeader/QUANTWeight/QUANTIdxWriter → Quant*`, `ExternalFormat::QUANT → Quant` (`adapter_core.cpp:115,117,135,151`, `test_adapter_bridges.cpp:64`). Prose/strings (~100+): comments, printf/argv (`quant_import`, `quant_ptq`, `quant_adapt`), bench labels. Verify with whitelist grep; `gate` + `full` green |
| **Z3** | README / docs rewrite | `README.md`, docs | Root `README.md` exists (none today); false "no external schemes" (`README:237` claim) corrected; `SHA256_TEST_LOG.md` ×3 conflict resolved (root 13/13 vs build 7/13, stale paths); 54 borrowed K names given honest provenance; 9 half-twin line-identical pairs documented as folded; format table regenerated from code, not hand-written |
| **V1** | Final verify + dominance bench | bench + docs | Full ladder runs on real weights (cached DeepSeek V4.1 Flash); every format vs its industrial counterpart at every BPW; results recorded honestly (losses documented, not gated away); `full` green; DEFECTS.md all closed or explicitly waived with reason |
| **R1** | TF security findings | per finding | Fixed + regression test; DEFECTS.md evidence |
| **R2** | TF correctness findings | per finding | Fixed + regression test; DEFECTS.md evidence |
| **R3** | TF build findings | per finding | Fixed; build flags verified; DEFECTS.md evidence |
| **R4** | CF criticals | `code-fusion` | Fixed + test; DEFECTS.md evidence; pausable |
| **R5** | CF highs | `code-fusion` | Fixed + test; DEFECTS.md evidence; pausable |
| **R6** | CF mediums | `code-fusion` | Fixed + test; DEFECTS.md evidence; pausable |

## Explicit non-tasks

| ID | Status | Note |
|---|---|---|
| Q-10 | **CANCELLED** | bitnet bench hardcoded-victory rewrite — do not do. Q2 covers the honesty umbrella for other benches. |
| Q-11 | **CANCELLED** | new standalone ternary format — ternary lives in `Q_1_K_H` (L2). |
| GPU backend completion | **OUT OF SCOPE** | ~18 unavailable backends: documented, not fixed, not deleted (zero-stub exception). |

## Verification commands (run verbatim at every gate)

```bash
# configure (once, in P0.0)
cmake -S . -B build-eng2 -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DQUANT_BUILD_ADAPTERS=ON -DQUANT_BUILD_TESTS=ON \
  -DQUANT_BUILD_BENCHMARKS=ON -DQUANT_BUILD_TOOLS=ON

ninja -C build-eng2                       # + named adapter targets (EXCLUDE_FROM_ALL)

# quant gate (every task)
ctest --test-dir build-eng2 --output-on-failure \
  -R "test_format$|test_all|test_fuzz_codec|test_format_audit|test_format_registry_complete|test_quant_mix|test_mix_components|grp_proof_test|test_wire_budgets"

# full (cross-cutting tasks: P0.0, L2, L4, Z2, V1)
ctest --test-dir build-eng2 --output-on-failure -E test_paged_kv_4m
```

## Progress log

Append one line per task completion: `<ISO date> | <ID> | <result> | <evidence (test names / files)>`.