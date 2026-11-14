# Operation Clean — Target Format Ladder

> The complete post-overhaul ladder: 69 formats, every name == nominal == wire BPW,
> every wire BPW on the .0 / .25 / .50 grid. This table is the contract that L1–L7
> implement and T1 pins. Derived from the verified plan
> (`.claude/plans/cuddly-yawning-lamport.md`, rewiring table) and the live enum
> (`transformers/include/quant/types.h:22-104`).

## Rules the ladder encodes


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
1. **Family pattern (every family):** `B = base` at exact `.00` BPW — the L tier.
   `M = B + 0.25` exact. `H = B + 0.50` exact. Three genuinely different codecs
   (the old L≡M≡H lie ends).
2. **Q_1 family:** L = `Q_1` = **binary** (slot-sign), exact 1.00. M = 1.25 exact.
   H = `Q_1_K_H` = **pure ternary** (−1/0/+1), exact 1.50.
3. **GRP base rewire down to name:** 2.625→2.00, 3.5→3.0, 4.5→4.0, 6.5625→6.00,
   8.5→8.0, 12.5→12.0, 16.5→16.0, 24.5→24.0.
4. **K_G M/H take the M/H tiers**; K_L ids retire (both plain and GRP).
   `Q_16_K_*` wire 16.25/16.50 and `Q_24_K_*` wire 24.25/24.50 — every tier is
   name-plus-delta, no family is exempt. (An earlier draft said these kept
   16.0/24.0 because 16 and 24 are "already exact"; that contradicts D-01 and
   is corrected here. `include/quant/types.h:294-298` has always carried the
   deltas.)
5. **Half formats fold:** the 18 half ids (73–90) retire; their wire spaces land in
   `_K_H` tiers at the same BPW. Names with a negative gap (`Q_2_5`, `Q_6_5`,
   `Q_G_2_5`, `Q_G_6_5` name x.5, wire x.4375) are retired without rewire.
6. **MX quarantine:** all 14 MX formats keep ids but are marked quarantined
   (2-iteration-LS tier allocator, −21..−37 dB); `Q_G_MX_3_5` rewires 3.78125 → 3.50.
7. **`Q_32` float ceiling: no tiers** (lossless is lossless).
8. **ID strategy: keep surviving ids in place**, retire the rest; no renumber.
   A renumber silently reinterprets old `.quant` checkpoints (format is stored as
   raw `uint8_t` per block, no version field read anywhere).

## Wire-count arithmetic (n = 256 block, bytes per block = BPW × 256 / 8)

| Format | bytes/block | Layout | Fits? |
|---|---|---|---|
| `Q_1` (1.00) | 32 | FP16 scale + 240 sign/2-bit-slot-packed signs | existing |
| `Q_2` (2.00) | 64 | FP16 scale + lattice 2-bit | existing |
| `Q_3` (3.00) | 96 | FP16 scale + codebook 3-bit | existing |
| `Q_4` (4.00) | 128 | FP16 scale + lattice 4-bit | existing |
| `Q_6` (6.00) | 192 | FP16 scale + codebook 6-bit | existing |
| `Q_8` (8.00) | 256 | FP16 scale + comp8 8-bit | existing |
| `Q_12` (12.00) | 384 | FP16 scale + 12-bit | existing |
| `Q_16` (16.00) | 512 | FP16 scale + 16-bit | existing |
| `Q_24` (24.00) | 768 | FP16 scale + 24-bit | existing |
| `Q_32` (32.00) | 1024 | FP32 passthrough | existing |

| Tier | bytes added over base | Layout | Layout proof |
|---|---|---|---|
| M (+0.25) | +8 B/block | signed per-span DC correction: plain 8-weight spans × 2 bits, GRP 32-weight spans × 8 bits | 256/8×2 = 64 b = 8 B; 256/32×8 = 64 b = 8 B |
| H (+0.50) | +16 B/block | same per-span DC correction, wider q field: plain 8-weight spans, GRP 32-weight spans; H's width is resolved adaptively from the region size (see §L2 tier wire) | 16 B = 0.50 BPW |

The multiplicative-gain sketch originally planned here ({×0.75, ×1.0, ×1.25, ×1.5}
per 32 weights) was rejected at implementation time: a global-scale codec's
dominant residual is a per-span **DC offset**, and a multiplicative gain cannot
express an offset at all. Additive corrections dominate at identical byte cost;
the evidence and the ordering proof are in §L2 tier wire below.

| Format | wire BPW today | wire BPW target | Layout change |
|---|---|---|---|
| `Q_G_2` | 2.625 | **2.00** | cut pad + budget literal (`:2596`, `:3044`, `:865`) |
| `Q_G_3` | 3.500 | **3.00** | same pattern |
| `Q_G_4` | 4.500 | **4.00** | same pattern |
| `Q_G_6` | 6.5625 | **6.00** | `quant_6k` path (`:1149`) |
| `Q_G_8` | 8.500 | **8.00** | same pattern incl. stale `8.0f` at `:2833` |
| `Q_G_12` | 12.500 | **12.00** | same, pad `:2865-2867` |
| `Q_G_16` | 16.500 | **16.00** | grp16 sizing table `:865` |
| `Q_G_24` | 24.500 | **24.00** | same pattern |

### GRP K_G family (takes M/H tiers; K_L retires)

| Old ids (retired) | New meaning |
|---|---|
| `Q_G_B_K_L` (+0.4375 or +0.5625 wire) | **retired**, id hole |
| `Q_G_B_K_M` | M tier = B + 0.25 exact |
| `Q_G_B_K_H` | H tier = B + 0.50 exact (absorbs old half twins at the same BPW) |

## Final ladder table (69 formats — L1 writes this into the enum)

### Keep (69 ids — every id below survives; nothing renumbers)

**10 base** (L tier of each family): `Q_1`(0), `Q_2`(1), `Q_3`(2), `Q_4`(3),
`Q_6`(4), `Q_8`(5), `Q_12`(6), `Q_16`(7), `Q_24`(8), `Q_32`(9).

**18 plain M/H:** `Q_1_K_M`(11), `Q_1_K_H`(12) — H is the new **ternary**; then
`Q_2_K_M/H`(14,15), `Q_3_K_M/H`(17,18), `Q_4_K_M/H`(20,21), `Q_6_K_M/H`(23,24),
`Q_8_K_M/H`(26,27), `Q_12_K_M/H`(29,30), `Q_16_K_M/H`(32,33), `Q_24_K_M/H`(35,36).

**9 GRP base:** `Q_G_1`(37) … `Q_G_24`(45) — rewired down to name (8.0 not 8.5 etc).

**18 GRP M/H:** `Q_G_B_K_M/H` for B ∈ {1,2,3,4,6,8,12,16,24}:
`Q_G_1_K_M`(47), `Q_G_1_K_H`(48), `Q_G_2_K_M`(50), `Q_G_2_K_H`(51),
`Q_G_3_K_M`(53), `Q_G_3_K_H`(54), `Q_G_4_K_M`(56), `Q_G_4_K_H`(57),
`Q_G_6_K_M`(59), `Q_G_6_K_H`(60), `Q_G_8_K_M`(62), `Q_G_8_K_H`(63),
`Q_G_12_K_M`(65), `Q_G_12_K_H`(66), `Q_G_16_K_M`(68), `Q_G_16_K_H`(69),
`Q_G_24_K_M`(71), `Q_G_24_K_H`(72).

**14 MX (quarantined):** `Q_MX_3_5`(91), `Q_MX_4_5`(92), `Q_MX_6_5`(93),
`Q_MX_8_5`(94), `Q_MX_12_5`(95), `Q_MX_16_5`(96), `Q_MX_24_5`(97),
`Q_G_MX_3_5`(98, rewired 3.78125→3.50), `Q_G_MX_4_5`(99), `Q_G_MX_6_5`(100),
`Q_G_MX_8_5`(101), `Q_G_MX_12_5`(102), `Q_G_MX_16_5`(103), `Q_G_MX_24_5`(104).

Count check: 10 + 18 + 9 + 18 + 14 = **69** = `FORMAT_COUNT`.

### Retire (36 id holes — format_is_valid() = false; decode maps via L4)

| Range | Old family | Reason |
|---|---|---|
| 10, 13, 16, 19, 22, 25, 28, 31, 34 | plain `Q_B_K_L` | L tier lives in the base id |
| 46, 49, 52, 55, 58, 61, 64, 67, 70 | `Q_G_B_K_L` | same |
| 73–81 | plain halves `Q_B_5` | folded into `Q_B_K_H` tiers |
| 82–90 | GRP halves `Q_G_B_5` | folded into `Q_G_B_K_H` tiers |

`Q_16_K_L`(31) and `Q_24_K_L`(34) retire even though their K_M/K_H siblings keep
16.0/24.0 wire — the tiers collapse into base.

### Q_1_K_H ternary wire contract (the operator's H example, made exact)

For n = 256:

```
bytes  0–1   : FP16 scale               = 16 bits
bits      2–369: 232 trits, base-3 packed = ⌈232 × log2(3)⌉ = 368 bits
bits    370–383: 14 bits — covered by the 24 evenly-spread implicit-zero slots
                               (is_slot() Bresenham spread, slot weight = 0, never stored)
TOTAL = 384 bits = 48 bytes = 1.5000 BPW exact
```

Tail sizes (n ≠ 256): the shipped rule is `budget = ⌈1.5·n⌉ - 16`,
`k = ⌊budget / log2(3)⌋` trits and `z = n - k` implicit-zero slots, with `log2(3)`
rounded slightly **up** so `3^k ≤ 2^budget` holds by construction. The wire is
always exactly `⌈1.5·n/8⌉` bytes — **never inflate**. Below `n = 12` no room exists
for a 16-bit scale plus a trit, so the encoder writes the `Q_1` binary payload
(prefix-identical) zero-padded to the same wire and the decoder returns ±1.
Measured and pinned by `tests/test_ternary_tail.cpp` for `n = 1..512`.

Gate: measured tier ordering `Q_1 < Q_1_K_M < Q_1_K_H` on the 4 fuzz distributions
+ real weights. `Q_10`/`Q_11` stay CANCELLED (binary = `Q_1`; ternary = `Q_1_K_H`).

## L2 tier wire (implemented 2026-11-13 — the contract the tests pin)

A K tier's payload is `[ L-tier payload ][ refinement region ]`:

```
target_bytes = ceil((base_bpw + delta) * n / 8)   <- the NAME's BPW
base_bytes   = ceil(base_bpw * n / 8)             <- the L payload
region       = target_bytes - base_bytes          <- 8 B (M) / 16 B (H) at n = 256
```

The region carries SIGNED PER-SPAN DC CORRECTIONS added to the decoded base
values. The unit is `span_max / div`, where `span_max` is the largest |decoded|
value in that span; no scale is stored, so the region cannot inflate the wire.
Spans are disjoint, so a span's unit depends only on the base decode in that
span, never on earlier corrections.

| Family | M span / q bits | H span / q bits | `div` M | `div` H |
|---|---|---|---|---|
| plain | 8 / 2 | 8 / 3..4 (adaptive) | `2^(B+1)` | `2 * div_M` |
| GRP | 32 / 8 | 32 / 9..16 (adaptive) | `2^(B+3)` | `2 * div_M` |

Strict ordering `L < M < H` rests on four facts, all asserted by
`tests/test_tier_order.cpp`:

1. every grid includes `q = 0`, whose refined value is bit-identical to the
   base decode, so a tier can never lose to the tier below it;
2. every candidate is scored by the refined MSE — the exact float add the
   decoder performs — not by a proxy;
3. H's candidate set contains the M winner scaled by `kdiv = div_H/div_M = 2`;
   scaling by a power of two commutes with round-to-nearest, so the M winner is
   exactly representable on the H wire;
4. H funds at least as many spans as M (adaptive width, below).

**Adaptive H width.** A fixed 16-bit GRP H field in a 3-byte region cannot fund
two spans, so at n=48, b=1, H refined one span while M (2-byte region, two
8-bit fields) refined two — measured 17.785% worse on a real trained bias.
H therefore picks the largest width in `[9,16]` (GRP) / `[3,4]` (plain) that
still funds `spans_m` spans; if none does, it uses M's exact layout and ties
rather than losing. Both sides derive the layout from
`(n, base_bpw, region_bytes)` alone.

**Correction quanta.** GRP M uses `1<<(B+3)`, not `1<<(B+2)`: at span 32 on a
Q_8 uniform block the coarser quantum rounded every q to 0 (`nz = 0/8`,
0.000% gain); one bit finer gives 0.689% and restores strict `M < L`.

**b=24 float floor.** Q_24 stores the top 24 bits of an FP32 (16-bit mantissa),
so the base error is already at float resolution. The M-vs-H correction
difference is ~0.03 float ULP at the span max, and the decoder's float add
rounds both to the same float32. Strictness is required for `b < 24`; at
`b = 24` a per-case tie is allowed (4/66 measured), while the AGGREGATE H total
must still beat M at every rung in both families — `test_tier_order` asserts
exactly that.

**GRP bases.** Per D-22a a GRP base at B.00 is a byte-identical alias of the
plain base; the genuine grouping lives in the GRP M/H tiers, whose 32-wide spans
spend the region on grouped DC state. `Q_G_1` keeps its existing binary slot
codec.

## formerly-known-as map (renames with provenance comments in code)

| Old name (removed) | New name | Comment in code |
|---|---|---|
| `Q_B_K_L` / `Q_G_B_K_L` | *(retired)* | formerly known as L variant; base id is the L tier |
| `Q_1_5` / `Q_G_1_5` | replaced by `Q_1_K_H` ternary wire | formerly known as half binary |
| `Q_B_5` (2..24) | `Q_B_K_H` tiers at same BPW | formerly known as half plain |
| `Q_G_B_5` | `Q_G_B_K_H` tiers | formerly known as half GRP |
| `QG2`-style aliases | `Q_G_2` | legacy alias removed; canonical name keeps |
| `Q_G_MX_3_5` at 3.78125 | same name, wire 3.50 | formerly known as 3.78125 wire |

All 98 legacy enum aliases (`Q1`, `QG1`, `QG_2_K_L`, `Q1_5`, …) are removed by L1 —
canonical names only.

## Registry means every format is REACHABLE

- `parse_format_name` must accept all 69 canonical names (today: silent default on
  miss — becomes loud failure; whitelist in `quant_import.cpp:64-84` widens to all
  valid formats).
- `format_to_regformat()` becomes lossless (today: all GRP/K → plain base, 9 half
  formats collapse, MX → GRP ids).
- Exactly **one** table per fact: `format_bpw` (wire) = `format_nominal_bpw` (name)
  for all 69 (the two functions remain distinct only to catch future drift — a
  `static_assert`-style runtime loop in test_wire_budgets compares them equal).
