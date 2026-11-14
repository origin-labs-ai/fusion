# BASELINE — Transformers-Fusion Inference Gauntlet

> Verified 2026-11-14. Every fact below carries the command that produced it.
> Legend: **[V]** verified by run, **[R]** read from source, **[A]** assumed/unknown.

## 1. Repositories and exact commits

| Repo | Path | Remote | HEAD | Branch | Working tree |
|---|---|---|---|---|---|
| Fusion superproject | `fusion/` | origin-labs-ai/fusion | see `git log -1` | main | dirty (telemetry + publication WIP, pre-existing) |
| Transformers-Fusion | `fusion/transformers/` (submodule) | origin-labs-ai/transformers | `28373ed` | main | 4 modified + 3 untracked (pre-existing, peer work) **[V]** |
| Reference fork | `fusion/.ref/llama.cpp/` | ggml-org/llama.cpp | `61dbf49228c8a96b72e40c89d93cb7c003411f8c` | master | clean, 0 entries **[V]** |
| CodeFusion | `fusion/code/` (submodule) | origin-labs-ai/code | HEAD at superproject commit | main | out of scope (D-28 rule: do not touch) |

Reference fork upstream pin (verified `git log -1`):

```
61dbf49228c8a96b72e40c89d93cb7c003411f8c | Fri Nov 13 23:57:05 2026 -0500
Hexagon: add support for IQ2_XXS and NVFP4 (#31954)
```

**License:** llama.cpp / ggml = MIT, "Copyright (c) 2023-2026 The ggml authors" (`head -5 .ref/llama.cpp/LICENSE`). MIT permits reuse, adaptation and redistribution; we preserve attribution by recording the source commit + file in `MIGRATION-MATRIX.md` for every ported implementation. No GPL/AGPL code is pulled in. **Transformers-Fusion = Apache-2.0** (`transformers/LICENSE`). MIT → Apache-2.0 incorporation is compatible; however a ported file must carry a notice that it is derived from ggml/llama.cpp (MIT, copyright notice retained) and is distributed under Apache-2.0. Every ported kernel in this mission carries such a header.

## 2. Toolchain

| Item | Value | Evidence |
|---|---|---|
| C++ compiler | Clang 22.1.7, target `x86_64-pc-windows-msvc` | `clang++ --version` |
| clang-cl | Clang 22.1.7 | `clang-cl --version` |
| MSVC | 19.51.36256 for x64 (VS 18, MSVC 14.51.36231) | `cl` banner |
| C++ standard | C++20 | `CMakeLists.txt:4-7` (`CMAKE_CXX_STANDARD 20`), verified in compile command `-std=c++20` |
| Build system | CMake 4.3.1-msvc1 + Ninja 1.13.2 | `cmake --version`, `ninja --version` |
| Build type | Release (`-O3 -DNDEBUG -D_FORTIFY_SOURCE=2`) | compile command |
| Warning set | `-Wall -Wextra -Wpedantic -fstack-protector-strong` | `cmake/compiler.cmake:5-9` |

## 3. Target host hardware

| Item | Value |
|---|---|
| CPU | AMD Ryzen 5 5600GT (Zen 3), 6C/12T **[V]** (`/proc/cpuinfo` model name) |
| SIMD flags present | `avx2`, `fma`, `f16c`, `bmi1/bmi2`, `sse4_1/2`, `ssse3`, `aes`, `sha_ni`, `movbe`, `popcnt`, `xsave` **[V]** (`/proc/cpuinfo` flags) |
| AVX-512 | **absent** — not in the flags string **[V]** |
| NEON | not applicable (x86 host) |
| GPU | AMD Radeon Vega 7 integrated (iGPU), shared DDR4 **[R]** `transformers/SPEC-INFERNO.md:1.1` |
| Device spec string | `AMD Radeon Vega 7 / 5600GT integrated GPU (RDNA/Vega iGPU), 7 CUs, ~448 shaders` **[R]** `SPEC-INFERNO.md:1.2` |
| OS | Windows 11 Pro 10.0.26300, x64 |
| RAM | 14,567,816 kB total ≈ 13.9 GiB **[V]** `/proc/meminfo` |
| Working backends on this host (per SPEC) | `GPU_DIRECTX`, `IGPU_SHARED`, `GPU_OPENCL`, `RAM_SWAP`, `CPU` **[R]** `SPEC-INFERNO.md:1.4` |
| Unavailable backends and reasons | CUDA/HIP/VULKAN/WEBGPU hardware or SDK absent; HEXAGON/ZDNN/OPENVINO/MUSA/METAL/SYCL/CANN/AVX512/NEON/ZENDNN/RPC/DISTRIBUTED need their own hardware — `SPEC-INFERNO.md:1.5` |

**Consequence for benchmarking honesty:** no GPU claim may ever be based on this host's iGPU path being "measured" against an NVIDIA CUDA baseline. CPU results are CPU results. The 32× floor in SPEC-INFERNO is defined against PyTorch on this device (`SPEC-INFERNO.md:2.1`) and the spec itself records ~2.9× measured (`SPEC-INFERNO.md:2.4`) — treat 32× as an open target, not an achieved fact.

## 4. Baseline build

Policy in this mission: **`build-gate` is the canonical, authoritative build tree** (it is the one the docs/progress call the gate build and it is the most recently configured, 2026-11-13 15:20). All build, test and benchmark evidence is taken from it unless a record states otherwise. `build/` and `build-eng2/` are stale peer artefacts (2026-10-17 / 2026-10-28 caches) and are not used for claims.

Command and result:

```bash
cd transformers/build-gate && ninja
# [92/92] Linking CXX executable tests\test_trainer_core.exe
```

**92/92 targets built, exit 0. [V]**

## 5. Baseline test suite

```bash
cd transformers/build-gate && ctest --output-on-failure -j 6
```

```
100% tests passed, 0 tests failed out of 77
Total Test time (real) = 116.17 sec
```

**77/77 pass, 0 fail. [V]** Label breakdown: codec 4, core 34, distributed 6, engine 3, gle 1, gpu 4, inference 13, moe 1, rl 3, trainer 1, training 27. Slowest: `test_fuzz_codec` 116 s, `test_training` 83 s, `test_quant_convergence` 14.7 s.

## 6. Baseline kernel benchmarks (BEFORE any change)

Command: `transformers/build-gate/bench_kernels.exe` **[V]**

| Kernel | Shape | Time (µs) | GFLOPS |
|---|---|---|---|
| scalar GEMM | 128³ | 2,067.03 | **2.03** |
| tiled64 GEMM | 128³ | 2,222.17 | **1.89** (0.93× scalar) |
| scalar GEMM | 256³ | 24,899.77 | **1.35** |
| tiled64 GEMM | 256³ | 22,503.79 | **1.49** (1.11× scalar) |

Honest reading: **1.3–2.0 GFLOPS on a Zen 3 6-core at 12 threads.** A single 3.9 GHz Zen 3 core with AVX2+FMA peaks near 2 FMA/cycle × 8 floats × 2 ops ≈ 62 GFLOP/s; 12 threads exceed 400 GFLOP/s theoretical. The baseline is therefore **~1–2 % of peak**, which is the signature of (a) not using SIMD at all, and (b) a cache-hostile B layout (`B[k*N+n]` stride-N inner loop). Both are confirmed by source: `src/kernel/kernel_gemm.cpp:13-38` is a plain triple loop, and the AVX2 paths at `:40-162` are `#if defined(QUANT_HAS_AVX2)`-gated.

## 7. ROOT CAUSE (measured, not assumed) — AVX2 never enabled

Three independent pieces of evidence:

1. **Actual compile command for the kernel TU has no `-mavx2`.** `ninja -t commands | grep kernel_gemm.cpp` in `build-gate` prints:
   `clang++.exe ... -O3 -DNDEBUG -std=c++20 ... -Wall ... -c src/kernel/kernel_gemm.cpp`
   No `-mavx2`, no `-march`, no `-mfma`. Therefore `__AVX2__` is undefined and every `#if defined(QUANT_HAS_AVX2)` block in `kernel_gemm.cpp` compiles to its scalar `#else` fallback. The "AVX2" functions exist as symbols but are plain scalar loops. **[V]**
2. **`cmake/compiler.cmake:23-28` only adds `-mavx2 -mavx -mbmi2 -mfma` when `QUANT_AVX2` is truthy**, and `cmake/arch.cmake:30` sets `QUANT_AVX2` only `if(HAVE_AVX2)`. **[R]**
3. **`check_cxx_source_compiles` never ran.** `cmake/arch.cmake:3` begins with `set(HAVE_AVX2 FALSE)` — this defines the cache variable *before* the check, and CMake's `check_cxx_source_compiles` is a no-op ("already in cache") when its result variable is pre-defined. So `HAVE_AVX2` stays `FALSE` unconditionally, on every host, including this Ryzen 5600GT. Fresh configure output proves it: `ARCH: AVX2 check result: FALSE`, and the result does not appear anywhere in `CMakeFiles/CMakeConfigureLog.yaml`. A minimal control project with the same `check_cxx_source_compiles` snippet and the same flags prints `Success / HAVE_AVX2=1` on this host — so the compiler and CPU are capable; only the guard is broken. **[V]** (control: `%TEMP%/avxprobe`)

Net effect: **every AVX2 kernel in the entire codebase is dead code at run time** on builds made by `cmake/arch.cmake` as it stands — kernels, math, codecs, quant engines. It "works" only because scalar fallbacks are correct, which is why 77/77 tests pass while throughput is 1-2 % of peak.

## 8. Related findings in the same audit

- `include/quant/simd_math.h:21` enables its AVX2 intrinsics under `#if defined(__AVX2__) || defined(_MSC_VER)`. Under clang (this toolchain) `_MSC_VER` is undefined and `__AVX2__` is undefined (no `-mavx2`), so that whole SIMD header is inert too. Same root cause.
- `include/quant/simd_math.h:23` defines `QUANT_HAS_AVX2` **inside the header**, i.e. a public macro whose meaning silently changes with the consumer TU's flags. Any TU compiled without `-mavx2` that includes it will see `QUANT_HAS_AVX2` undefined even though sibling TUs were compiled with AVX2 — an ODR/ABI hazard for anything `inline` or template in that header, and a correctness hazard for code that selects a code path from it. This must become a single configure-time definition, not a per-TU one. (Medium; see DEFECTS.md D-2.)
- `bench_kernels` "tiled64" 128³ is *slower* than scalar (0.93×) — a 64×64 blocking of a 128×128×128 multiply with an inner scalar loop has no compute-density gain; only the 256³ case shows 1.11×. So the cache tiling, on its own, is not earning its complexity. The real win has to come from SIMD + register blocking + B-panel packing (llama.cpp's `ggml_gemm` shape).

## 9. Baseline inference-pipeline state (to be completed in Phase 0)

Known from source reads so far:

- `Linear::forward` routes through `AutogradEngine::matmul_op` (`src/model/transformer.cpp:77`), i.e. **the training-path matmul is the inference matmul** — there is no separate inference GEMM entry point today. Any speedup on `matmul_op` lifts both, but it also means inference pays autograd bookkeeping. To be quantified.
- `Embedding::forward` is a per-row `memcpy` loop (`transformer.cpp:48-53`) with clamping — fine, but no fused dequant-on-gather.
- Backend enum: 24 members, live in `include/quant/backend.h:9-33` **[V]**; 20 source files in `src/backend/` **[V]** — matches the documented split (4 fused + 1 composed + 15 primitive) that the audit must now re-derive from disk.
- `ggml` reference has 207k LOC across the surveyed source files; the migration matrix in `MIGRATION-MATRIX.md` records which of them are actually implemented, buildable optimizations worth porting versus which are per-vendor glue we cannot verify on this host.

## 10. Reproduction commands

```bash
# toolchain
clang++ --version; cmake --version; ninja --version
# reference identity
git -C .ref/llama.cpp log -1 --format='%H %ad %s'
# build + tests
cd transformers/build-gate && ninja && ctest --output-on-failure -j 6
# kernels baseline
./bench_kernels.exe
# prove AVX2 is off
cd transformers/build-gate && ninja -t commands | grep -m1 kernel_gemm.cpp
# control that the check itself works
cmake -S $TEMP/avxprobe -B $TEMP/avxprobe/b -G Ninja
```
