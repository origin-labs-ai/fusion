# Operation Clean — Working-Tree Disposition (P0.0 input)

> Every inherited dirty/untracked file in `transformers-fusion`, its content, and the
> disposition P0.0 applies. Nothing here is an implementation edit — this is the
> read-only audit that makes P0.0's baseline build trustworthy.
> Source: `git status` + `git diff` of the working tree at planning time (2026-10-23).

## 1. Modified files (12) — dispositions

| # | File | What the diff does | Verdict | Rationale |
|---|---|---|---|---|
| 1 | `.gitignore` | Removes ~20 lines: `Lumina/`, `FRAUD_REPORT.md`, `TASKS.md`, `DIFFUSION.txt`, `build_linux.sh`, `FLYWHEEL_LOG.md`, `PEER_REVIEW_LOG.md` … | **INVESTIGATE, likely KEEP (as uncommitted)** | Deleting `Lumina/` (a separate project) and audit logs from ignore is suspicious — it looks like someone's housekeeping that hides prior reports. Operation Clean needs those reports (`FRAUD_REPORT.md`, `PEER_REVIEW_LOG.md`) visible. **Default: restore the removed lines** so audited history stays tracked; revisit only if a tracked file breaks the build. |
| 2 | `CMakeLists.txt` (+41) | Registers ~30 trainer sources across `quant_dense` / `quant_moe` / `quant_multimodal` (schedulers, losses, opt_factory, precision, checkpoint, callbacks, distributed, profiler, ema, noise, data_augment, curriculum, metrics_dense, lora, distill, regularizers, rl_align, grad_utils, sampler, init, hooks, swa, pruning, flops, mtp, gradcheck + moe: routers, expert_parallel, aux_losses, layers, moe_pipeline, moe_eval + multimodal: vision, audio, video, cross_modal, fusion_layers, projection …) | **KEEP — required** | These sources are untracked (`??`) and are part of the trainer work; the tree doesn't build without them. Compiling them is also the only way to prove the new trainer code is sound (Z1 + R3 later depend on it). |
| 3 | `engines/trainer/dense/loss.cpp` (+10/−3) | **Fixes a real math bug**: focal-loss `dL/dz_v` had the modulating term multiplied by `0` (dropped) then re-added with the wrong sign. New derivation: `w·(1 − γ·p_t·log p_t/(1−p_t))·(p_v − δ_vt)`, comments state finite-difference checks catch both errors. | **KEEP — real correctness fix** | Independent numeric test exists later (`test_trainer_core.cpp`). Must survive; its regression is checked in R2 (TF correctness). |
| 4 | `engines/trainer/dense/parallel.cpp` (+1/−1) | **Fixes a double-scaling bug**: `e.bytes = bytes[i] * 4` → `e.bytes = bytes[i]` ("`bytes` is already a byte count"). | **KEEP — real correctness fix** | Shard planning was quadrupling byte counts. R2 regression. |
| 5 | `include/quant/gpu_compute_opencl.h` (+20) | Adds OpenCL helpers to the header. | **KEEP — part of the OpenCL work below** | Must stay consistent with `gpu_compute_opencl.cpp`. |
| 6 | `inferno/inferno_bench.cpp` (+2/−2) | Changes a printed CUDA ratio from "99x claim" to "32x target". | **INVESTIGATE** | Looks like a *marketing downgrade* of a claim in bench output — direction is opposite to "bench honesty" (it should state what is measured, not a lower target). Re-check in Q2: bench honesty requires measured numbers, not reworded targets. |
| 7 | `src/adapters/tools/bench_industry_real.cpp` (+2/−2) | `RegFormat::Q1_5`/`QG_1_5` → `Q_1` (Q_1_5 + Q_G_1_5 map there), `Q6_K_M` → `Q_6`. Comment: "Q_1_5 + Q_G_1_5 both map here". | **KEEP (for now) — L5 re-does it** | This was a workaround so the bench built after a registry renumber. L5/Q2 rewrite this bench against the final ladder anyway (the `:904` OOB read lives here). Do not hand-carry. |
| 8 | `src/backend/gpu_compute.cpp` (+14) | Adds a PSO cache (`std::unordered_map<string, ComPtr<ID3D12PipelineState>>`) keyed by entry+source under a mutex in `DirectXCompute::Impl`. | **KEEP — perf feature** | Thread-safe cache for D3D12 pipeline states. Verify in P0.0 that it compiles (DirectX-only path). |
| 9 | `src/backend/gpu_compute_opencl.cpp` (+152/−…) | Reworks the OpenCL backend (152 lines changed). | **KEEP — part of the OpenCL work** | Must build on this host or be in the documented-exception list for unavailable backends (D-07). |
| 10 | `src/codec/block_codec.cpp` (+75) | **ADDS `fit_scale_true_mse`** (`:632-695`): LS seed → 9-point grid → 12-iteration golden-section → FP16 snap ±6 neighborhood sweep. Header comment claims it is shared by Q3/Q6/Q12 + Q2/Q4. **Zero callers** — the patch was partially applied. | **KEEP THE CODE — Q1 WIRES IT** | This is exactly the shared scale-fitter D-12/D-20 describe as the Q_12 46 dB fix. P0.0 does NOT delete it. Q1 wires it into the four encoders and then corrects the comment if the reach differs. **Z1 must not delete it either** — it has a planned caller. |
| 11 | `src/codec/quant_format.cpp` (+1/−1) | `file_.write(MAGIC, 15)` → `22` in `QuantIDXWriter::write_idx`. | **INVESTIGATE — likely KEEP, verify against the MAGIC literal** | If `MAGIC` is 22 bytes long, 15 was a real bug (wrote 15 of 22 bytes). Verify `MAGIC` declaration length; if it is 22, keep the fix. |
| 12 | `tests/CMakeLists.txt` (+37) | Registers 3 new test executables: `test_trainer_engine`, `test_trainer_moe_multimodal`, `test_trainer_core` (labels `engine;training`, TIMEOUT 60). | **KEEP — required** | They reference untracked test sources; without these lines they cannot run. Compiling them is P0.0's job (if one doesn't build, its hunk gets dropped with evidence). |

## 2. Untracked files (18+) — dispositions

| Group | Files | Verdict |
|---|---|---|
| Trainer sources registered in CMakeLists (#2) | `engines/trainer/moe/{moe_pipeline,routers}.{h,cpp}`, `engines/trainer/multimodal/dense/{audio,cross_modal,fusion_layers,projection,video,vision}.{h,cpp}`, `engines/trainer/multimodal/moe/{mm_experts,mm_fusion,mm_router}.{h,cpp}`, `engines/trainer/dense/{callbacks,checkpoint,curriculum,data_augment}.{h,cpp}` | **KEEP — required** (build) |
| New tests | `tests/test_trainer_core.cpp`, `tests/test_trainer_engine.cpp`, `tests/test_trainer_moe_multimodal.cpp` | **KEEP — required** (compile-check in P0.0) |
| `SHA256_TEST_LOG.md` | untracked | **INVESTIGATE** — a test log left untracked; Z3 reconciles the three `SHA256_TEST_LOG.md` files (root vs build) |
| `build_linux.sh` | untracked (and `.gitignore` removal tried to un-ignore it) | **KEEP as untracked** unless the team tracks it; Z3 decides |

## 3. What P0.0 must do (in order)

1. Restore `.gitignore` lines for the audited reports (`FRAUD_REPORT.md`, `PEER_REVIEW_LOG.md`,
   `TASKS.md`, `DIFFUSION.txt`, `FLYWHEEL_LOG.md`) — they are Operation Clean inputs.
   Keep `Lumina/` removal only if it is genuinely out of tree; otherwise restore.
2. Verify `MAGIC` byte-length in `quant_format.cpp` → confirm the 15→22 fix is correct; if
   `MAGIC` is 15, revert the diff instead.
3. Configure `build-eng2` (the cfg command in PLAN.md) and run `ninja -C build-eng2`.
4. **If the trainer sources or the 3 new tests fail to compile**, drop exactly those
   registration hunks (file + line evidence recorded here), then re-run until green.
   A red baseline build is unacceptable — Operation Clean edits must be attributable.
5. Run the `full` ctest gate and record the pre-Operation Clean baseline pass/fail set
   (this is the "before" evidence for V1 and for every later task's gate).
6. Record all of the above in PLAN.md §Progress log with file:line evidence.

## 4. Baseline expectations (so regressions are attributable)

- The trainer diffs (#3, #4) and OpenCL/D3D work (#5, #8, #9) must be **building before
  any Operation Clean edit**. If they don't, that is a P0.0 blocker, not an
  Operation Clean task.
- `block_codec.cpp`'s `fit_scale_true_mse` must remain **present but uncalled** until
  Q1 wires it (zero-dead-code rule does NOT apply to it — it has a scheduled caller).
- Nothing in this table may be deleted during Z1 without a decision line here.