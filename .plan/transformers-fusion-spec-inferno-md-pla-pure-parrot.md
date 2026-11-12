# SPEC-INFERNO Implementation Plan — transformers-fusion training engine

## Context

The user asked: `@transformers/SPEC-INFERNO.md` — "Plan karle isko implement karne ka!"
The spec describes a "feature-complete" training engine under `engines/trainer/`. Reading the
spec against the actual code shows the engine is ~90% built and genuinely tested — but the spec
overstates completeness in a few specific places. Verified facts first, then the gap plan.

Important nuance (verified, do not "fix" blindly):
- `SPEC-INFERNO.md` is **507 lines**, not the 1024 its own header claims (line 7: "Header files:
  exactly 1024 lines"; 15.9: "this file is exactly 1024 lines"). The "1024 lines" instruction in
  the file header refers to *header files* discipline, and section 15.9 is simply wrong as written.
- `ctest -N` in `build/` reports **Total Tests: 75** — spec 12.6's "75 tests" is accurate.

## Verified facts (spec claims that ARE true in code)

| Spec | Evidence |
|---|---|
| 12.6 75 ctest tests | `ctest -N` → `Total Tests: 75` (build/) |
| 4.3 14 optimizers exist | `include/quant/optimizer.h:54-250` (AdamW, SGD, Adam, Adamax, NAdam, RAdam, Lion, Adafactor, RMSProp, Ranger, Adabound, Lamb, LARS, NovoGrad); factory maps all 14 at `engines/trainer/dense/opt_factory.cpp:9-66` |
| 10.1 warmup_cosine UAF fix | `engines/trainer/dense/schedulers.cpp:41` — "OWNERSHIP: capture the decay scheduler via shared_ptr so the lambda" |
| 10.5 ModalityAdapter [in,out] | `engines/trainer/multimodal/dense/projection.cpp:60-63` — `[in,hidden]` / `[hidden,out]` |
| 10.7 LoRA [in,out]/[in,rank]/[rank,out] | `engines/trainer/dense/lora.cpp:62-66`, merge = mm(A,B) |
| 10.8 repetition penalty returns 1.0 | `engines/trainer/dense/rl_align.cpp:22` — `if (max_freq <= 1) return 1.0f;` |
| 10.11 plan_shards no 4x bytes | `engines/trainer/dense/parallel.cpp:164-165` — "`bytes` is already a byte count — do NOT scale it again." |
| 6.9 RL trainers | `include/quant/trainer.h:347` PPOTrainer, :398 DPOTrainer, :427 GRPOTrainer, :450 RLVRTrainer, :468 RLHFPipeline; `compute_gae` at trainer.h:359,494 + `engines/trainer/dense/rl_align.cpp:67,70` |
| 5.9 Sensor3D all 10 methods | `engines/trainer/multimodal/dense/modalities.h:66-84` — voxelize, depth_to_normals, normalize_thermal, spectral_index, hs_pca3, sar_to_db, lidar_to_xyz, radar_speed, imu_tilt, gps_local |

## Real gaps (spec vs code)

### G1 — DECISIONS modality is MISSING (spec 0.4, 6.9, 11.27) — highest priority
Spec 11.27: `DECISIONS -> policy head + rewards + GAE (rl_align.cpp) trains a model that outputs
decisions/actions`. Spec 0.4: "engine must also be a system to TRAIN a decisions model".
- `engines/trainer/multimodal/dense/modalities.h:13-18` — `enum class Modality` has 26 entries
  (TEXT..GPS) + COUNT. **No DECISIONS.** Repo-wide grep for `DECISIONS` in engines/ + include/
  returns nothing.
- The underlying machinery EXISTS and is orphaned relative to the modality matrix:
  `rl_align.cpp` rewards + `compute_gae`, quant:: PPO/DPO/GRPO/RLVR trainers.
- **Fix:** add `DECISIONS` to the Modality enum (before COUNT, so `kNumModalities` becomes 27),
  add a policy-head training path in `modalities.cpp`, and register it so 11.27 is a live path,
  not just available primitives. Update `modality_name()`.
- Must not break `kNumModalities` consumers — grep all uses before touching the enum.

### G2 — `OptimSuite::Kind` exposes only 5 of 14 (spec 4.3)
Spec 4.3 promises "14 optimizers" for `optim.{h,cpp}`. The factory (`opt_factory.cpp`) does have
all 14. But `engines/trainer/dense/optim.h:28` declares `enum class Kind { ADAMW, ADAM, ADAFACTOR,
SGD, LION }` — only 5, and `optim.cpp:8-20` constructs all 5 member objects unconditionally.
- **Fix:** extend `Kind` to all 14 and dispatch in the ctor; or document `OptimSuite` as the
  5-optimizer convenience wrapper and point spec 4.3 readers at `opt_factory` for the full set.
  Prefer extending — spec says "14 optimizers ... plus param-group builder".
- Check `Optimizer` base API compatibility for the 9 additions (Ranger/Adabound/Lamb/LARS/
  NovoGrad/Adamax/NAdam/RAdam/RMSProp) — they exist in `include/quant/optimizer.h:102-250`.

### G3 — Spec self-inconsistencies to correct in SPEC-INFERNO.md (doc-only)
1. Line 7 + 15.9 claim the file is 1024 lines; actual is 507. Either pad to 1024 (as the header
   literally demands) or correct both lines to the truth. Recommend correcting the text — padding
   a spec with filler is worse than an honest line count. **Ask the user.**
2. Section 4.3 says optim.{h,cpp} has 14 optimizers — true only via the factory; see G2.
3. Section 12.4/12.5 claim 55 + 57 checks; `tests/test_trainer_moe_multimodal.cpp` is 313 lines
   and `tests/test_trainer_core.cpp` is 358 lines — plausible but unverified. Count `CHECK(` in
   each before asserting.
4. Spec 15.5 says "8 modules" for moe/ and 15.6 "14 modules" for multimodal/ — file listing shows
   8 moe files and 14 multimodal files. ✓ consistent (engines/trainer/{moe,multimodal}).

### G4 — Unverified spec claims worth measuring before trusting
- 8.1/8.2 performance numbers (DirectX 22→42 GFLOPS, OpenCL 6.6→72 GFLOPS) — run
  `build/bench_inferno.exe` (exists) to get live numbers instead of quoting the spec.
- 2.3's label at `inferno/inferno_bench.cpp:469,471` — verified present at those exact lines.
- 12.1/12.2 test claims — run `ctest --output-on-failure` for the real pass/fail state rather
  than trusting "PASSED" in the doc.

## Implementation approach

Solo, small verified steps, no speculation — each edit followed by a real check (this matches the
codebase's own testing culture: 75 live ctest cases, and spec 12.7's "any new loss MUST be
FD-validated with gradcheck").

1. **Measure first (read-only):** run `bench_inferno.exe` + `ctest -N`/selected ctest to get the
   real baseline. Record numbers in the spec's section 8/12 only after measuring.
2. **G1 DECISIONS:** grep `kNumModalities`/`Modality::COUNT` consumers → add enum entry → wire a
   policy path in `modalities.cpp` using existing `rl_align` + `compute_gae` → add a test case to
   `tests/test_trainer_moe_multimodal.cpp` (or a new small test) that runs the path.
3. **G2 optimizers:** extend `OptimSuite::Kind` to 14, ctor dispatch, keep `param_norm`/
   `update_norm`/`snapshot` probes intact; rebuild `quant_dense`.
4. **G3 doc corrections:** fix line 7/15.9 line-count untruth (pending user choice), align 4.3
   wording, insert measured numbers for 8.1/8.2 and 12.x pass counts.
5. **Rebuild + test:** `cmake --build build` then `ctest` for the three engine tests
   (`test_trainer_engine`, `test_trainer_moe_multimodal`, `test_trainer_core`) plus
   `test_backends_realonly`, `test_gpu_capability`.

### Files to modify
- `engines/trainer/multimodal/dense/modalities.h` / `.cpp` — DECISIONS enum + policy path (G1)
- `engines/trainer/dense/optim.h` / `.cpp` — 14-optimizer `Kind` (G2)
- `tests/test_trainer_moe_multimodal.cpp` — new DECISIONS-path check
- `SPEC-INFERNO.md` — doc corrections + measured numbers (G3, G4)

### Reuse (don't reinvent)
- `rl_align.cpp` rewards + `compute_gae` for the DECISIONS path
- `include/quant/trainer.h:347-494` PPO/DPO/GRPO/RLVR/RLHFPipeline for policy loops
- existing `CHECK(...)` test pattern in `tests/test_trainer_engine.cpp:40`
- `opt_factory.cpp`'s 14-way construction as the reference for `OptimSuite`

## Verification

```powershell
Set-Location C:\Users\thaku\Workspaces\fusion\transformers-fusion
cmake --build build --target quant_dense quant_multimodal          # G1/G2 compile
ctest --test-dir build -R "test_trainer_engine|test_trainer_moe_multimodal|test_trainer_core" --output-on-failure
ctest --test-dir build -R "test_backends_realonly|test_gpu_capability" --output-on-failure
ctest --test-dir build -N                                            # expect 75 + any new tests
.\build\bench_inferno.exe                                            # live GFLOPS for spec sections 2/8
```
A change is done when: it compiles, the touched test passes with real output, and the spec text
no longer contains the untruth that motivated the change.

## Open questions for the user

1. **Spec line count:** header line 7 + 15.9 claim "exactly 1024 lines" but the file is 507.
   Correct the text (recommended), or pad to 1024?
2. **Priority:** G1 (DECISIONS — real missing feature) vs G2 (OptimSuite 14) vs doc-only G3?
   Do all three, or G1 first then reassess?
3. **Bench numbers:** should I re-run `bench_inferno.exe` and write measured GFLOPS into the spec,
   or leave the spec's claimed numbers untouched?
