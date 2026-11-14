# L2 codec close-out — full record (2026-11-14)

> Status: **COMPLETE — L2, L2b, L2c, L2d all landed and green.**
> Gate: `ctest --test-dir build-gate -j 4` → **78/78 passed, 0 failed, 97.00 s**.
> This file is the durable, self-contained record: what changed, why, the evidence,
> and what is still pending. Companion rulings: `DECISIONS.md` **D-32**, contract
> text in `LADDER.md` **§L2 tier wire**.
> Nothing in this session was committed or pushed.

---

## 1. Scope of L2 and its sub-tasks

| Sub-task | Claim | Verdict |
|---|---|---|
| **L2** | Codec rewire: every GRP base wire literal cut to its name at exact `.00`; GRP bases become D-22a aliases; all 69 formats reachable | **DONE** |
| **L2b** | M/H tiers are genuinely ordered `L < M < H` on the 4 fuzz distributions and on trained real weights, with a construction proof (not a tolerance) | **DONE** |
| **L2c** | `Q_1_K_H` pure ternary at exact 1.50 BPW for every tail size, never inflating; base-3 trit packing; binary fallback below n=12 | **DONE** |
| **L2d** | Half-format retirement: 36 retired ids never valid, exactly 69 live, `format_is_half` dead | **DONE** |

---

## 2. Wire contract that shipped

A K-tier payload is `[L-tier payload][refinement region]`:

```
target_bytes = ceil((base_bpw + delta) * n / 8)   <- the NAME's BPW
base_bytes   = ceil(base_bpw * n / 8)             <- the L payload
region       = target_bytes - base_bytes          <- 8 B (M) / 16 B (H) at n = 256
```

The region carries signed per-span DC corrections. The unit is `span_max / div`,
where `span_max` is the largest `|decoded|` value in that span; **no scale is
stored**, so a payload can never exceed its name. Spans are disjoint, so a span's
unit depends only on the base decode in that span.

| Family | M span / q bits | H span / q bits | `div` M | `div` H |
|---|---|---|---|---|
| plain | 8 / 2 | 8 / 3..4 adaptive | `2^(B+1)` | `2 * div_M` |
| GRP | 32 / 8 | 32 / 9..16 adaptive | `2^(B+3)` | `2 * div_M` |

Code placement (`transformers/src/codec/block_codec.cpp`):

| Symbol | Line | Role |
|---|---|---|
| `tier_corr_div_m(bool, float)` | 2616 | correction quantum table |
| `tier_refine_layout(bool, int, int, float, size_t)` | 2649 | resolves width / spans / divisor from the wire size alone |
| `tier_refine_build(...)` | 2684 | encoder: builds the region, scores by refined MSE |
| `tier_refine_apply(...)` | 2798 | decoder: recomputes the same layout and applies corrections |
| `Q_1_K_H` ternary block | 2833 | pure-ternary codec (documented block) |

The six ordering facts, all pinned by a test:

1. every grid includes `q = 0`, whose refined value is bit-identical to the base
   decode, so a tier can never lose to the tier below it;
2. candidates are scored by the exact float add the decoder performs;
3. H's candidate set contains the M winner scaled by `kdiv = div_H/div_M = 2`
   (a power of two, exactly representable, commutes with round-to-nearest);
4. H funds at least as many spans as M (adaptive width below);
5. spans are disjoint, so no correction depends on an earlier one;
6. `MSE(H) <= MSE(M) <= MSE(L)` therefore holds span by span, by construction.

---

## 3. Bugs found and fixed (with before/after evidence)

### 3.1 GRP correction quantum was one bit too coarse

**Symptom:** strict `M < L` failed at GRP `b=8`, uniform distribution.
**Root cause:** `div_M = 2^(B+2)` at span 32 makes one quantum larger than a typical
span DC residual, so every candidate rounded to `q = 0`.
**Evidence (scratch probe `.plan/.rea-tmp/probe_grp8.cpp`):**

```
span=32 shift=10 nz=0/8  nmse=0.00139191 (base 0.00139191, gain 0.000%)
span=32 shift=11 nz=5/8  nmse=0.00137010 (base 0.00139191, gain 1.568%)
```

**Fix:** GRP `div_M = 2^(B+3)`; GRP `div_H = 2^(B+4)` when the adaptive width is
used. Result: `0 STRICT-FAIL` across 72 family × distribution × rung cases.

### 3.2 H could refine fewer spans than M (n=48 coverage bug)

**Symptom:** real trained weights, GRP `b=1`, `n=48`: H was **17.785% worse** than M.
**Root cause:** the H region is 3 bytes; a fixed 16-bit q field funds only **one**
span, while M's 2-byte region funds **two** 8-bit spans. H silently skipped the
span `[32,48)` that M refined.
**Evidence (`.plan/.rea-tmp/probe_real1.cpp`):**

```
param 8 chunk@0 n=48  M=0.22645648 H=0.266731497 (17.785% worse)
  total bytes M=8 H=9  base=6  identical base=1
  span  0 [  0, 32): diff= 0/32 sseM=6.34123 sseH=6.34123
  span  1 [ 32, 48): diff=16/16 sseM=4.08015 sseH=5.93358 <-- H WORSE
```

**Fix:** `tier_refine_layout` picks the largest H width in `[9,16]` (GRP) /
`[3,4]` (plain) that still funds `spans_m` spans; if none does, it uses M's exact
layout and ties instead of losing. The layout is derived from
`(n, base_bpw, region_bytes)` alone, so encoder and decoder agree.
**After:** `bad(H>M)=0` over every chunk of the trained model; `test_tier_order`
exit 0.

### 3.3 Observation — b=24 is a float32 floor, not a wire shortfall

`Q_24` stores the top 24 bits of an FP32 (16-bit mantissa). The M-vs-H correction
difference is ~0.03 float ULP at the span max, so the decoder's float add rounds
both to the same values.
**Evidence (`.plan/.rea-tmp/probe_grp24.cpp`):**

```
bytes L=768 M=776 H=784
SSE L=4.1660890785682526e-10 M=4.1364668716456347e-10 H=4.1364668716456347e-10
span 0..7: corrM == corrH bit-for-bit; diff=0/32 on every span
```

**Contract adopted:** strict `M < L` everywhere; strict `H < M` for `b < 24`;
per-case equality allowed at `b = 24` (4/66 measured ties); **aggregate** `H < M`
strictly at every rung in both families.

### 3.4 D-22a consequence — GRP bases are aliases, caps change honestly

A GRP base at `B.00` cannot carry per-group state (budget proof, D-22a). `Q_G_2` …
`Q_G_24` are therefore byte-identical aliases of `Q_2` … `Q_24`; `Q_G_1` keeps its
existing binary slot codec. The genuine grouping lives in the GRP M/H tiers
(32-wide spans).

Because `Q_G_3` is now the `Q_3` alias, its fuzz cap must cover plain `Q_3`'s worst
measured NMSE (`0.9522` on the deterministic outlier corpus). The cap moved
`0.80 → 1.00` in `tests/test_fuzz_codec.cpp:146` with the provenance comment at
`:140-145`. This is a **contract change**, not a relaxed test: the old 0.80
belonged to the pre-D-22a grouped encoder, which is no longer the layout under
that id.

Also carried from this session's earlier work: `Q_G_MX_3_5` / `Q_G_MX_4_5` skip
per-32 sign-tier scale grouping (`quad_mix_grouped(...)` is false for `bits == 1`),
which stopped a collapse that rendered unit-scale signs (NMSE ≈ 364 on
`gaussian(0.05)`).

---

## 4. Ternary wire (`Q_1_K_H`, D-02)

```
[ FP16 scale (16 bits) ][ base-3 trit stream ][ zero padding ]

target_bits = ceil(1.5 * n)
budget      = target_bits - 16
k           = floor(budget / log2 3)   trits stored
z           = n - k                    implicit-zero slots (Bresenham spread)
```

- At `n = 256`: `16 + 368 + 24 = 384` bits = **48 B**, `k = 232`, `z = 24`.
- Slots use the same deterministic `is_slot(i, n, z)` scheme as `Q_1`:
  `floor((i+1)z/n) != floor(i*z/n)`.
- `log2(3)` is deliberately rounded **up** at the 16th decimal, so
  `3^k <= 2^budget` holds by construction; encoder and decoder share the helper.
- Below `n = 12` there is no room for a 16-bit scale plus a trit, so the encoder
  writes the `Q_1` binary payload (prefix-identical) zero-padded to the same
  `ceil(1.5n/8)` wire, and the decoder returns ±1.

---

## 5. Tests added / changed

### New: `transformers/tests/test_tier_order.cpp` (433 lines)

Registered in `transformers/tests/CMakeLists.txt:169-170` (labels `codec;core`,
`TIMEOUT 600`). Asserts, over `2 families × 4 distributions × 8 blocks × 9 rungs`
plus every 256-wide chunk of a trained `DenseModel`:

- exact stored byte count per tier at `n=256` (`ceil(bpw*n/8)`);
- `NMSE(M) <= NMSE(L)` and `NMSE(H) <= NMSE(M)` with **no epsilon**;
- strict `M < L` everywhere; strict `H < M` for `b < 24`;
- aggregate `H < M` and `M < L` strictly at **every** rung in both families;
- documented minima: `M<L 0.0465%` (plain b=16 outlier), `H<M 0.0001%`
  (GRP b=1 sparse), `4/66` allowed b=24 ties.

### New: `transformers/tests/test_ternary_tail.cpp` (348 lines)

Registered in `transformers/tests/CMakeLists.txt:172-173`. Six checks:

1. `n = 1..512` store exactly `ceil(1.5n/8)` bytes, no codebook;
2. fallback `n = 1..11` is a prefix-identical `Q_1` payload, zero-padded, decodes
   to ±1;
3. `n = 256` is 48 B with `k = 232` / `z = 24`; all-±1 and ±0.5 blocks reconstruct
   bit-exactly on non-slots, zero on slots;
4. `n = 12` is the first ternary layout (3 B, 1 trit, 11 slots);
5. slot sweep `n = 12..128`: zero count equals `z` exactly on the slot positions;
6. every prefix of a payload decodes safely and finitely; 0 bytes → all zeros.

### Changed: `transformers/tests/test_format.cpp` (+30 lines at `:22`)

Pins L2d: exactly 36 invalid ids, `invalid + FORMAT_COUNT == FORMAT_ID_SLOTS`, the
exact retired id set is invalid with `format_bpw == 0`, and `format_is_half` is
false for every id.

### Changed: `transformers/tests/test_fuzz_codec.cpp`

`Q_G_3` / `Q_G_3_K_*` caps `0.80 → 1.00` with the D-22a provenance comment.

### Changed: `transformers/tests/CMakeLists.txt`

Two registrations (lines 169-173).

---

## 6. Verification evidence (commands + exact results)

```text
$ ctest --test-dir build-gate --output-on-failure -j 4
100% tests passed, 0 tests failed out of 78
Total Test time (real) = 97.00 sec

$ ./build-gate/tests/test_fuzz_codec.exe
FUZZ CODEC PASS: 69 formats, 10052 generated tensors, 693588 roundtrips, 0 crashes

$ ./build-gate/tests/test_format_audit.exe
69 rows ok
BPW violations: 0

$ ./build-gate/tests/test_tier_order.exe
aggregate NMSE strictly decreases at every rung and family
min relative gain b<24: M<L 0.0465% (plain b=16 outlier-mix blk=3),
                        H<M 0.0001% (GRP b=1 sparse(90%) blk=1)
b=24 (float32 floor): 4/66 H==M ties; min strict gain M<L 0.0001%, H<M 0.0000%
TIER ORDER TEST PASSED: L < M < H strict on corpus and real weights

$ ./build-gate/tests/test_ternary_tail.exe
byte exact: n=1..512 store exactly ceil(1.5n/8) bytes
fallback: n=1..11 is prefix-identical to Q_1, padded, decodes to +-1
n=256: 48 B, 16 b scale + 368 b base-3 trits + 24 slots; signs exact at 1.0 and 0.5 amplitude
n=12: first ternary layout (1 trit, 11 slots, 3 B)
slot sweep: n=12..128 zero count == z at the exact slot positions
truncation: every prefix of every payload decodes safely; 0 bytes -> all zeros
TERNARY TAIL TEST PASSED

$ ./build-gate/tests/grp_proof_test.exe
QG3 real-weights PSNR: 29.8756 dB (Q3 plain: 29.8756 dB)
GRP QUALITY PROOF TEST PASSED SUCCESSFULLY!

$ ./build-gate/tests/test_block_codec.exe
ALL BLOCK CODEC TESTS PASSED!
```

Toolchain used: `build-gate` (Ninja, Release). Test exes live in
`transformers/build-gate/tests/`.

---

## 7. Files touched in this work

| File | Change |
|---|---|
| `transformers/src/codec/block_codec.cpp` | L2 wire rewrite; tier refinement (`tier_refine_layout`, `tier_refine_build`, `tier_refine_apply`, `tier_corr_div_m`); GRP aliases; ternary block; MX collapse guard |
| `transformers/tests/test_tier_order.cpp` | **new** (433 lines) |
| `transformers/tests/test_ternary_tail.cpp` | **new** (348 lines) |
| `transformers/tests/test_format.cpp` | L2d invariants (+30 lines) |
| `transformers/tests/test_fuzz_codec.cpp` | D-22a cap provenance |
| `transformers/tests/CMakeLists.txt` | two test registrations |
| `transformers/src/adapters/tests/test_adapter_bridges.cpp` | QG_MX expectation 3.78125→3.50, FP8 fixture 0xBC→0xB8 |
| `.plan/docs/operation-clean/LADDER.md` | rule-4 correction; tier layout table; §L2 tier wire |
| `.plan/docs/operation-clean/DECISIONS.md` | **D-32** |

Working-tree note: `transformers/README.md` and the `publication/` tree carry
**pre-existing peer-session changes** (T13.2e) that this work did not touch.
Untracked `test_adapter.quant` / `test_adapter_raw.fp32` are adapter-test
artefacts, not source.

---

## 8. What is still pending (explicit)

From the 10-item session queue:

| # | Item | Status |
|---|---|---|
| 1 | L2 codec rewire | **DONE** |
| 2 | L2b M-tier encoder + ordering | **DONE** |
| 3 | L2c `Q_1_K_H` ternary encoder | **DONE** |
| 4 | L2d half-format collapse + retirement | **DONE** |
| 5 | T1.2–T1.4 decision memos | **PENDING — not started** |
| 6 | T6.1 NCM Appendix F.1.1/I read + 4 questions | **PENDING — not started** |
| 7 | T10.3c README batch 2 | **ALREADY DONE / verified**: `wc -l transformers/README.md = 6144`; queue entry was stale |
| 8 | T11.1–T11.3 `_archive` mining + cross-links | **PENDING — not started** |
| 9 | T12.1–T12.4 PDF completeness audit | **PENDING — not started** |
| 10 | T9.1 dashboard after every step | **DONE this session** (regenerated after each step); remains a standing rule |

Absent from the queue but still open in `TODO-TREE.md`: T1.5/T1.6, T2, T3.1,
T3.4, T4, T5–T8, T9.2–T9.4, T10.4, T13 (peer session in flight), T14, T15.
See `.plan/telemetry/TODO-TREE.md` §Session status for the canonical list.

---

## 9. Reproduce

```bash
cd transformers
cmake --build build-gate --target test_tier_order test_ternary_tail test_format \
      test_fuzz_codec test_format_audit test_block_codec grp_proof_test
./build-gate/tests/test_tier_order.exe
./build-gate/tests/test_ternary_tail.exe
ctest --test-dir build-gate --output-on-failure -j 4
```

Scratch probes (not part of the build): `.plan/.rea-tmp/probe_tiers.cpp`,
`probe_real1.cpp`, `probe_grp8.cpp`, `probe_grp24.cpp`, `probe_mx.cpp`,
`probe_q24.cpp`.
