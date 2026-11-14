# Operation Clean — Decisions Log

> Every binding rule, decision, and trade-off, with provenance (operator quote →
> distilled rule → implementation path). Companion files: [PLAN.md](PLAN.md) (task
> DAG + DoD), [LADDER.md](LADDER.md) (69-format contract).
> Append-only. One line per decision: date | ID | decision | why | trace.

---

## D-01 · Ladder pattern L/M/H (operator: 2026-10-22, "Info 5" + "Info 2")

**Rule:** in EVERY family, L = base at exact `.0` BPW, M = base + `.25` exact, H = base
+ `.50` exact. Three genuinely different codecs. The old standalone "L" duplicate is
retired; the base id IS the L tier.

**Trace:**
- "jo Q_1 hai wo formerly known as L/M/H me se L yaani Low waala variant and L waala jo
  separate hi unko khallas aur ye exact 1.0 BPW use karenge, fir M waala, ye 1.25 BPW
  exact use karenge, H waale 1.50…"
- "har ek family me yahi rule hai aur jo L hai wahi base hai yaani .0 fir M matlab .25
  and H matlab .50 exact."
- Implementation: LADDER.md rules 1–2; tasks L1/L2.

## D-02 · Q_1 = binary, Q_1_K_H = pure ternary (operator, 2026-10-22)

**Rule:** `Q_1` keeps binary (slot-sign) at exact 1.00. `Q_1_K_H` becomes pure ternary
(−1/0/+1) at exact 1.50. The proposed standalone formats Q-10/Q-11 are **CANCELLED**
(operator said so explicitly; recorded as F-0 in DEFECTS.md).

**Trace:** "jo Q_1 hai wo hi binary rahega aur jo Q_1_5 rahega jise Q_1_K_H bolenge ya
isi type kuch, ye pure ternary and exact itna BPW hi."
- Wire: 48 B/256 w = 1.5000 exact (trits base-3 packed + FP16 scale + implicit-zero
  slots) — see LADDER.md §Q_1_K_H.

## D-03 · Rewire direction (operator: "BPW ko kam karo")

**Rule:** name says X ⇒ wire costs exactly X. The LAYOUT comes DOWN to the name; never
rename a format up to its wire. (BOW was the operator's typo for BPW.)

**Trace:** "QG2 hai to Q_G_2 rename, BPW ko kam karo … exact G bolenge, formerly known
as karke code me likh sakte ho."
- Implementation: 8 GRP rewire targets + K/half literals — LADDER.md table; L2.
- Negative-gap formats (`Q_2_5` etc., name x.5 > wire x.4375) retire rather than
  inflate the layout: folding keeps the grid clean and avoids inventing new engines.

## D-04 · GRP naming normalization

**Rule:** `QG2` → `Q_G_2` style everywhere; canonical pattern `Q_/Q_G_/Q_MX_/Q_G_MX_`
+ ` _K_M/_K_H` tiers. Renames carry "formerly known as <old>" comments in code.
Macros/env excluded from casing rules.

**Trace:** "QG2 hai to Q_G_2 rename … formerly known as karke code me likh sakte ho."

## D-05 · Casing: QUANT → Quant (operator, 2026-10-19)

**Rule:** the ALL-CAPS token `QUANT` exists only where structurally mandatory:
C/C++ macros (`QUANT_CHECK`, `QUANT_AVX`, …, defined via #define) and environment
variables (`QUANT_SEED`, `QUANT_PAGED_KV_DEBUG`, `QUANT_SKIP_FULL`, `QUANT_SKIP_GLA`).
Everything else — type names, comments, docs, printf strings — is `Quant`.
Lowercase namespace `quant` stays (distinct token).

**Trace:** "macros, env's jaisi jagaho ko chhod ke kisi bhi file me 'QUANT' poora upper
case me naa ho dhyaan rakhna, 'Quant' hona chahiye har code me aur har jagah, docs me
bhi."

## D-06 · BPW granularity (operator)

**Rule:** every format lands on exact `.0 / .25 / .50` BPW steps. No other wire values
survive anywhere in the ladder (this is what kills 3.78125, 3.4375, 6.5625, 2.625 …).

## D-07 · Zero dead code / zero stubs (operator, 2026-10-18)

**Rule:** after Operation Clean, no dead helper and no stub remains — every dead symbol
is wired up correctly or deleted.

**Documented exception:** the ~18 GPU/compute backends that exist but are unavailable
(unoptimized, incomplete by design until the backend-completion effort) are kept,
documented accurately, and excluded from the zero-stub rule. They are NOT deleted and
NOT half-fixed here.
**Trace:** "ek bhi dead code and stub nahi bachna chahiye, bas kuchh-kuchh stub chhode
gay hai majboori me unko exclude karke jaise ki 18 backends hai but wo available nahi
hai optimizations ke liye."
Implementation: task Z1 with the exception list.

## D-08 · Persistence compatibility (design decision, agent-verified)

**Rule:** old `.quant` files must survive the ladder change. Therefore:
- IDs are KEPT in place (no renumber) — a renumber silently reinterprets checkpoints
  because format is stored as raw `uint8_t` per block and no version field is read.
- 36 retired holes become invalid ids; readers remap via `legacy_format_id_remap()`
  (K_L→base, halves→same-BPW `_K_H`), one log line per file, never silent.
- All 4 clamp sites replace the ad-hoc `wire_fmt < FORMAT_COUNT && wire_fmt != 19`
  predicate with `wire_format_valid()` from a single truth (`format_compat.h`).
- Writers assert validity before write — this catches the MoE `format = 5 with FP32
  payload` label bug at write time, not on some future read.

## D-09 · M-tier encoder (SUPERSEDED by D-32 on 2026-11-13)

**Original rule (historical, no longer the shipped layout):** M tier = base layout +
1 refinement byte per 32 weights, carrying 4 × 2-bit sub-block scale multipliers
{×0.75, ×1.0, ×1.25, ×1.5} — engine-agnostic, provably +0.25 BPW exact.

**Shipped rule (`DECISIONS.md` D-32, `block_codec.cpp:2649 tier_refine_layout`):** the
refinement region carries **signed additive per-span DC corrections**, not multiplicative
gains. Plain spans are 8 weights with a 2-bit q; GRP spans are 32 weights with an 8-bit
q. A multiplicative gain cannot express a DC offset at all, and the dominant residual of
a global-scale codec is exactly that offset; additive corrections dominate at identical
byte cost and make `q = 0` bit-identical to the base decode, which turns
`NMSE(L) ≥ NMSE(M) ≥ NMSE(H)` into a construction guarantee.

The D-09 acceptance gate was kept and strengthened: the shipped test measures **NMSE**
(not PSNR) with strict `M < L` everywhere, strict `H < M` for `b < 24`, and aggregate
strictness at every rung/family on 4 fuzz distributions + trained real weights
(`tests/test_tier_order.cpp`, 433 lines). The only allowance is per-case `H == M` ties
at `b = 24`, a proven FP32-output floor (D-32).

## D-10 · Ternary tail policy (design decision; shipped form noted 2026-11-14)

**Rule:** for block sizes where the exact-1.50 ternary layout doesn't decompose
(cleanly), the encoder NEVER inflates: it drops to the largest tier that fits the
name's wire budget exactly (ternary → M → L, per-size). Same policy for every
rewired format: budget guard pattern of `quant_grp16:879-884` (a real budget test,
never the `has_d = (n >= 8)` non-test that caused the quant_6k overrun).

**Shipped form (`Q_1_K_H`, D-32 / `LADDER.md` §ternary tail):** the tail rule is
`budget = ⌈1.5·n⌉ - 16`, `k = ⌊budget / log2(3)⌋` trits, `z = n - k` implicit-zero
slots, with `log2(3)` rounded slightly **up** so `3^k ≤ 2^budget` holds by
construction. No M-tier fallback is ever needed: the wire is exactly
`⌈1.5·n/8⌉` bytes for every `n = 1..512` (pinned by `tests/test_ternary_tail.cpp`).
Below `n = 12` a 16-bit scale plus a trit cannot fit, so the encoder writes the
`Q_1` binary payload (prefix-identical) zero-padded to the same wire; the decoder
returns ±1. That is the L tier of this ladder, i.e. the same never-inflate policy.

## D-11 · K-variant honesty (design decision)

**Rule:** tier logic keys off format ID/enumeration, never the NAME string
(today `k_tier()` parses `_L/_M/_H` out of the name at `block_codec.cpp:2464-2470` —
a rename would silently change encoder effort). `Q_16_K/Q_24_K` trios split from
their shared body (`:2740-2743`) into real tiers.

## D-12 · Quality floor: scale fitting (design decision)

**Rule:** shared scale-fitter (`fit_scale_true_mse`, currently dead at
`block_codec.cpp:632-695`) lands in Q3/Q6/Q12 + Q2/Q4 with golden-section refinement
where it wins (today only `comp8_fit_scale_fp16:306-358` has golden-section; Q_12's
3-iteration LS seed is why it measures 46 dB while K_H's 24 iterations reach ~59 dB).
Acceptance: `Q_12 ≥` old K_H within documented margin; `Q_G_12 < Q_G_8` inversion gone.

## D-13 · MX quarantine (design decision, agent-verified)

**Rule:** the 14 MX formats are quarantined: kept, registry-marked, documented as
catastrophic (2-iteration-LS tier allocator, −21..−37 dB vs industrial refs at same
BPW), excluded from dominance claims, NOT deleted (their wire/persistence contracts
hold). `Q_G_MX_3_5` rewires 3.78125 → 3.50 so the name==wire grid includes them.
An adaptive rework of the tier allocator is a LATER, separate effort — not Operation
Clean scope.

## D-14 · Bench honesty (design decision)

**Rule:** every printed bench number must be measured, not hardcoded, and every
comparison must use one byte basis. Concretely: `write_quant_mixed` honors
`target_bpw` (today it ignores the knob — every "QUANT Mixed 1.50" row actually wrote
2.625); the `pick(rs, q_ids, 7)` OOB read (`bench_industry_real.cpp:904`) gets real
bounds; "negligible"/"95% scheduling" prose is regenerated from measured output;
Q-10's bitnet-victory bench stays CANCELLED as a task but the hardcoded victory
strings are covered by Q2's umbrella for the OTHER benches (bench_poc "No external
schemes" false claim dies too).

## D-15 · Priorities (operator delegated)

**Rule:** DAG order is my judgment: P0 → S (memory-safety, independent of the ladder)
→ L (ladder, tree-swallowing) → T (tests against a frozen ladder) → Q (quality on top
of final tests) → Z (hygiene sweeps last so they touch final code once) → V1 (prove
dominance) → R (review findings, code-fusion last because pausable).

**Trace:** "Ye tum khud decide karo, priority tum apne hisaab se do sabko."

## D-16 · One task to 100% (operator)

**Rule:** serial execution, one worker session per task, DoD gate green before the
next starts. Task register and gates live in PLAN.md.

**Trace:** "ek ko pleetooge fir use 100% complete karoge uske best level pe, most strict
worker in the world ki tarah … fir baari baari se sab ke sab 100% complete naa ho jaayenge
tab tak baari-baari se sabko ek ek karke karoge."

## D-17 · Execution gate (operator)

**Rule:** implementation starts ONLY after review workflow `wf_ce1d51d7-91d` reaches
100%. Documented fallback if the synthesize stage keeps dying on infra: compose the
final report + completeness pass from the journal + `findings_verified.json`, mark the
workflow *complete-by-reconstruction* in this file, and proceed.

**Trace:** "Workflow 100% complete hone ke baad ham plan ko implement karenge" /
"Plan complete ho jaayega to workflow ke wait ke liye rukna."

## D-18 · Execution name (operator)

**Rule:** this effort is called **Operation Clean** (all user-facing references and the
docs directory name).

## D-19 · Strictness (operator, general)

**Rule:** "koi chook nahi honi chahiye" — the most-strict-worker standard. Every task's
DoD includes evidence (grep-zero counts, test names, measured numbers), not claims.
Honest bench regressions after rewire are documented, not hidden; what is hidden or
faked is a defect by definition.

## D-20 · Known-caught-at-test-time traps (from exploration)

These field-tested facts feed the task DoDs directly:
- `test_fuzz_codec.cpp:278` allows claimed+1 byte — this is EXACTLY why the quant_6k
  +1-byte overrun passes today (S3 kills the allowance, strict ≤ after).
- `test_block_codec.cpp` does NOT test `block_codec.cpp` (it tests GEMM kernels) —
  `block_codec.h:65`'s claim otherwise is false (corrected everywhere in L1/Z3).
- `test_format_audit.cpp` checks `actual <= format_bpw + 1e-3` only at N=256 and never
  fails on PSNR — `test_wire_budgets.cpp` (T1) replaces all three gaps.
- `test_format_registry_complete.cpp` `singles>=19` is a floor, not the 69-set — its
  replacement pins `singles >= 55` + retired names fail parse (registry
  silent-default-on-miss becomes loud).
- GGUF bridge silently zero-fills unsupported types (`gguf_bridge.cpp:336-342`,
  verbose-gated) — raises to loud-fail during L5 (documented as part of import
  honesty, since silent zero weights are silent corruption).
- `NativeFormat` (trainer) is a separate, untouched format id-space; documented, not
  merged into the quant ladder except by alias check (L4 records this explicitly).

## D-21 · Operation Clean ≠ review findings only

**Rule:** the review workflow findings (A-ranges) and quant overhaul (B/C/E ranges)
both execute through the same greatest-strictness process; quant tasks S1–V1 run
before R-series (review) because they need a stable build/test gate. DEFECTS.md stays
the ledger for both.

---

## Workflow reconstruction record (D-17 fallback — filled only if triggered)

*(empty — the review workflow is still running; this section fills with evidence if
the synthesize stage cannot complete and complete-by-reconstruction is invoked.)*

---

### How to use this file during execution

1. Before each task: check the register in PLAN.md + relevant decisions here.
2. During each task: if a decision is contradicted by a live fact, STOP, record the
   conflict here as a new decision (append, never rewrite), then continue.
3. After each task: append one line to PLAN.md §Progress log.

---

## D-22 · LADDER COUNT RESOLVED: **69 wins** (Fusion Smash, 2026-11-01)

**Conflict raised by Prime Orchestrator:** `review-tracking/MASTER_PLAN.md` says 60 formats;
`docs/operation-clean/LADDER.md` + the live enum say 69.

**Verdict: 69 is authoritative.** Evidence (all commands run, outputs below):

| # | Evidence | Source |
|---|---|---|
| 1 | `MASTER_PLAN.md:29` §1 heading says "Target format ladder (60 formats)" — but `MASTER_PLAN.md:223` its OWN L1 task row says "`types.h`: **69 live formats**, validity table, retired-id map, new `format_compat.h`" | MASTER_PLAN internal contradiction |
| 2 | `MASTER_PLAN.md:94` §1.4 retires "GRP base `Q_G_x` (9)" — but `MASTER_PLAN.md:126-133` §2 "Rewire map" REWIRES that same family: "`Q_G_2` 2.625 → **2.00**", "`Q_G_x_K_*` (×9) → exact base", "same as their GRP base" | MASTER_PLAN internal contradiction |
| 3 | `MASTER_PLAN.md:18` G-4 verbatim: "GRP families (`Q_G_*`) **follow the identical L/M/H rule**" — L is the base; retirement contradicts the rule it cites | operator rule |
| 4 | Live enum `include/quant/types.h:146-147`: `FORMAT_ID_SLOTS = 105`, `FORMAT_COUNT = 69`; `kFormatValid[105]` marks exactly 69 ids live, and ids 37–45 (`Q_G_1`..`Q_G_24`) are LIVE | live code |
| 5 | Live `format_bpw` already carries `Q_G_2 → 2.0f` … `Q_G_24 → 24.0f` (`types.h:312-320`), matching LADDER's 69-ladder | live code |
| 6 | 69 = 10 base + 18 plain M/H + 9 GRP base + 18 GRP M/H + 14 MX, and MASTER_PLAN's own §1.1/1.2/1.3 arithmetic (28 + 18 + 14) = 60 comes from retiring the 9 GRP bases | arithmetic |

**Resolution that satisfies both documents:** keep the 9 GRP bases (LADDER.md's 69). The
§1.0 budget proof in MASTER_PLAN is still TRUE and is retained as a **design note**, not a
retirement:

> ### Design note D-22a (the real content of MASTER_PLAN §1.0)
> At `B.00` a 256-weight block has exactly `256·B` bits of budget and `B`-bit levels alone
> consume all of it — so a GRP base at `B.00` **cannot carry any per-group state**. Its
> layout is therefore the *plain base layout under a GRP name* (exactly as `Q_G_1` already
> is: `types.h:284` `Q_1 → 1.0f` and `:312` `Q_G_1 → 1.0f`, both using the same slot-sign
> codec at `block_codec.cpp`). The genuine grouping lives in the tiers: `Q_G_x_K_M` at
> `B.25` and `Q_G_x_K_H` at `B.50`.
> Consequence for L2: **the GRP base encoder must be cut down to the plain-base layout**
> (today it still calls the grouped-affine path at 2.625 BPW — see D-23).

**Trade-off accepted:** `Q_G_x` at `B.00` is byte-identical in *layout* to `Q_x` for every x.
That is not a lie (name == wire == `B.00`), but it must be **documented as a naming/API alias**
in Z3's docs pass so no one claims the GRP base is a distinct codec. If a distinct GRP base
codec is ever wanted, it requires a sub-`.00` grid, which the operator's `.0/.25/.50` rule
forbids.

**Ladder count is now frozen: 69. `FORMAT_COUNT = 69`. Any future claim of 60 is stale — this
line supersedes it.**

---

## D-23 · LIVE DEFECT found during D-22 verification (L4 is a data-corruption bug)

**Found:** 2026-11-01, Fusion Smash. **Severity: critical (silent data corruption on read).**

L1 landed (`FORMAT_COUNT` 105 → 69) but L4 did not. All four `.quant` clamp sites still use the
old predicate `wire_fmt < FORMAT_COUNT && wire_fmt != 19`:

| Site | Line |
|---|---|
| `src/codec/quant_format.cpp` | `:456` `bd.format = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) ? (Format)wire_fmt : Format::Q_32;` |
| `src/codec/quant_format.cpp` | `:611` `fmts.push_back((wire_fmt < FORMAT_COUNT && wire_fmt != 19) ? (Format)wire_fmt : Format::Q_32);` |
| `src/adapters/tools/qwen35_engine.cpp` | `:32` `const Format fmt = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) …` |
| `src/adapters/tools/qwen35_engine.cpp` | `:145` `t.fmt = (wire_fmt < FORMAT_COUNT && wire_fmt != 19) …` |

Because `FORMAT_COUNT` is now 69 while the id space is 105, **every valid format with id ≥ 69
silently decodes as `Format::Q_32`**. Parsed from the live `kFormatValid` table, that is
**17 valid formats**: ids `69, 71, 72` (`Q_G_16_K_M`, `Q_G_24_K_M`, `Q_G_24_K_H`) and
`91..104` (all 14 MX formats).

**Fix (L4, next task):** introduce `include/quant/format_compat.h` with `kFormatValid` as the
single truth plus `wire_format_valid()`, and replace all four predicates with it. Writer must
assert validity before write. Recorded as the first L4 sub-step.


## D-24 · Workspace rename: `code-fusion/` → `code/`, `transformers-fusion/` → `transformers/` (operator, 2026-11-12)

**Rule:** both repos were renamed because both already live inside `fusion/` ("fusion to hai hi").
The GitHub remotes follow: `origin-labs-ai/code.git` and `origin-labs-ai/transformers.git`
(old `*-fusion.git` URLs redirect; everything else unchanged). **The product/alias vocabulary is
NOT renamed** — CodeFusion, TransFormers-Fusion and TransCender stay as names (§1 of the master
plan governs). What changed is only *path-shaped* references: `transformers-fusion/…`,
`code-fusion/…`, `*-fusion.git` URLs — 93 live files swept (plan + PLAN.md + review-tracking +
operation-clean docs + all `.rea-tmp` scripts + `transformers/PROGRESS.md` + `code/arch` +
`code/payloads`). **Verbatim operator quotes, the alias-vocabulary table and historical evidence
dumps were deliberately left untouched** — rewriting a quote would falsify evidence. Full backup:
`.plan/.rea-tmp/rename-sweep-backup-20261112-182006/`.

> **Spelling update (2026-11-13, D-28):** the current product spelling is
> **`Transformers-Fusion`**; this 2026-11-12 entry preserves its dated spelling as history.

**Trace:**
- *"Saath me maine code-fusion/ ko code/ me rename kar diya hai and transformers-fusion/ ko
  transformers/ me kyuki dono fusion/ folder ke andar me hai yaani fusion to hai hi! Usi ke
  hisaab se thora-bahut origin bhi change hoga, transformers-fusion.git se transformers.git
  ho jaayega, baaki ka adress same hi hai, aise hi code-fusion.git se code.git ho jaayega!
  Keep in mind!"*
- Implementation: path sweep (`rename_sweep.py` + `surgical.py`), then **all 7 plan verifiers
  re-run exit 0** (step1 117/117·13/13 · step2 PASSED · step3 156/156 anchors 0 problems ·
  subanchors 85/85 · step5 65 checks · step6 PASSED · arxiv 67/67).

## D-25 · Effort slider: DSH plugin belongs to Sonar; Zenix port parked (operator, 2026-11-12)

**Rule:** `code/slider/effort` = `dsh-claude-effort-slider` v0.9.4 (MIT) — a **DeepSeek Harness
(DSH) plugin** (cordis.patch.yml + `dsh.client` bundle, 6-stop Low→Ultracode, 38/38 tests). DSH
== **Sonar (Plus)** natively. **Zenix (Claude Desktop)** has no cordis/slots (plain Electron +
React renderer) but *does* carry the hooks (`effortLevel`/`reasoningEffort` in main,
`thinkingBudget`/`extendedThinking` in renderer) — so a port is possible later, in one of two
shapes: **A** DOM-inject into the composer (fast, reversible, needs `ion-dist.asar` repack) or
**B** native rebuild wired into Fusion's layout system. **Operator ruling: park BOTH for now**
— *"look waisa implement karenge, Sonar me bhi implement karenge!"* then *"Dono baad me
karenge!"* → Sonar integration + Zenix port are context-only until unparked.

**Trace:** thread *Current Strike* runs 11–12 (host-mismatch quote + comment). Implementation:
none yet — parked. Next when un-parked: Sonar = plugin wire (profile bundle + registry) and
Zenix = choose A or B.

## D-26 · _archive/ = reference-only port of every deleted doc (operator, 2026-11-12)

**Rule:** all docs ever deleted from **both** repos (the 2026-11-01 `code-fusion` purge of
README/`docs/` and the earlier `transformers` history) are recovered ONCE into
`.plan/_archive/` — 288 files / ~10.6 MB: README (5,925 lines), `docs/` (38), `repo/memory/`
(15, the iron rules), `TransCender.png`. **`InNova.png` stays deleted** (operator ruling). The
archive is **reference only** — future docs get redesigned fresh ("sab bas reference ke liye
uthaa raha hu"), so this port defines the pattern for how deleted docs get archived: copy-once,
never override, keep the deletion history intact. Engine-repo identity recorded alongside:
TransFormers-Fusion, **formerly known as TransCender** (Inferno = kernel + training engine).

> **Spelling update (2026-11-13, D-28):** current spelling is **`Transformers-Fusion`**; D-30 also
> fixes the wire identity — `Transformers-FusionIDX` + legacy `TransCenderIDX` only.

**Trace:**
- *"IDEA! Bhai, .plan/_archive wo waala saara ka saara source yahaa copy kar! … InNova.png ko
  deleted hi rehne de! Jitna jo bhi files the — delete hue, sab ko yahaa uthaa ke le aa,
  kuchh bhi override bhi naa ho! … sab bas reference ke liye uthaa raha hu to uthaa le!"*
- Implementation: `.plan/_archive/` populated (Code Crash thread run 12 — archive + remotes
  completed before the run died on a provider 429; the path-sweep remainder was finished here).


## D-27 · Goal hierarchy + 1.0 BPW side goal + FP/INT research direction (operator, 2026-11-12)

**Rule:** the reading public (and any agent) misreads this project as "main target 1.5 BPW".
Operator ruling: **MAIN GOAL = the entire Fusion Superproject** (every domain, seat, track —
complete). **SIDE GOAL = MAXIMUM at EXACT 1.0 BPW** — *not* 1.5; the implemented 1.5 BPW path
is the *stepping stone*, and existing "1.5 BPW" statements stay true as *implemented-state
facts* while the goal line moves to 1.0. **New research direction (operator's same-day
research):** FP (floating-point) and INT (integer) quantization format families BOTH have
actionable work — research both. **Fact recorded:** Loop Quantization has never been
implemented for any model anywhere (2026-11-12 audit) — Track B will be the first.
Every implement-facing document carries the reminder note in the operator's own words.

**Trace:**
- *"Jo bhi ye project dekhta hai to use lagta hai ki is project ka main target 1.5 BPW hai… ye
  poora sabka doubt clear karne ke liye… Is project ka main goal to poora Superproject hai!
  Side goal me 1.5 BPW par nahi, exact 1.0 BPW par maximum achieve karna hai, sab kuchh!"*
- *"Aaj ke mere research ke hisaab se FP waale jo bhi quantization formats hai and INT yaani
  Floating Point and Integers waale unka bhi kuchh kara jaa sakta hai, ye sab note kar lo!
  Har document me! … apne words me jisse ki koi bhi agent plan waale file ko dekh karke
  implement kar raha ho to beech me ye padhe to mujhe yaad dilaaye!"*
- *"Aaj tak kisi ne Loop Quantization implement bhi nahi kiya hai, koi bhi model ka!"*
- Implementation: reminder inserted in master plan, PLAN.md, LADDER.md, PROGRESS.md,
  TODO-TREE, BLUEPRINT; telemetry DASHBOARD carries it top-of-file.


## D-28 · Product-name normalisation: `TransFormers-Fusion` -> `Transformers-Fusion` (operator, 2026-11-13)

**Rule:** the capital `F` in "Formers" is dropped everywhere in the Fusion Superproject -
`TransFormers-Fusion` becomes **`Transformers-Fusion`** - across documentation, code, build
scripts, CI workflows, benchmarks, tests, telemetry strings and archived documents.
`CodeFusion` and `TransCender` keep their names (D-24 left the product vocabulary alone;
this ruling narrows it for the engine name only). The spelling is **byte-length preserving**
(`TransFormers` and `Transformers` are both 12 characters), so file sizes, the archive
manifest's byte column and every size-derived fact stay valid.

**Wire-format safety:** the `.idx` magic moves from `TransFormers-FusionIDX` to
`Transformers-FusionIDX`. Both are 22 bytes (21 compared + NUL), so the layout does not
change, and the reader now accepts **both** spellings so that files written by earlier
builds keep decoding. The writer emits the new spelling only. The magic that would have
been broken is therefore not broken - this honours the standing ruling that the wire format
is not touched without an operator decision.

**Trace:**
- *"poore fusion/ me jahaa bhi and kahi bhi Trans'F'ormers-Fusion likha hua hai, 'F'ormers
  me to usko 'f' kardo, lower case kar do! Har ek jagah, docs se lekar code tak, jahaa jo
  bhi hai - sab!"*
- Implementation: project-wide sweep with backups (`.plan/.rea-tmp/rename-lowerf-backup-*`),
  dual-magic reader, test updated to assert the new magic and the legacy alias.

**Executed (2026-11-13):**
- 83 text files rewritten - 9 under `.plan/`, 74 under `transformers/`; `code/` needed none.
- The first sweep died with `WinError 206` (path too long) after 33,284 mirrored backups. It was
  completed with a flat, hash-named backup: `.plan/.rea-tmp/rlb-20261113-113652/` (83 entries,
  `index.jsonl` maps every rewritten file to its backup). Re-running the sweep changes 0 files.
- Excluded on purpose: `.git`, `.mimosa`, build trees, `__pycache__`, `.rea-tmp` snapshots, every
  `*.bak*` / backup copy, and this file (the decision log keeps the historical spelling).
- Wire format: the writer magic is lowered; the reader keeps the pre-D-28 spelling as a fourth
  accepted magic. `tests/test_sha256_corrupt.cpp` gained `Test 6` (legacy magic still readable) -
  16/16 tests pass on a fresh Ninja + clang++ build (`build-norm/`), and `test_math` /
  `test_kernel` still pass.
- Residual scan: zero `TransFormers` occurrences outside this decision log.
- Commit status: `.plan` committed with this record. `transformers/` already carried ~69 unrelated
  in-flight changes from earlier sessions, so the rename is applied in its working tree but is
  deliberately **not** committed there - committing it would mix unrelated work into a naming
  commit. `code/` was likewise left untouched.

> **Superseded in part by D-30 (2026-11-13):** the engine `.idx` reader accepts exactly two
> engine identities - `Transformers-FusionIDX` (current, 22 B) and `TransCenderIDX` (legacy
> "formerly known as", 15 B) - plus the pre-D-28 capital-F spelling of the current magic
> (same 22 B, read-only). `SolIDX` is **not** an engine magic; it is reserved for model
> manifests. D-28's byte-length argument and the writer change remain valid.


## D-29 · Zenix-CC -> Zenix (CC suffix removed) + alias-registry duplicate cleanup (operator, 2026-11-13)

**Rule:** the native Claude Desktop seat is **Zenix** - the `CC` suffix is removed from the
product name, the folder (`windows/zenix`), the registry entries and every current-state doc.
The component folders and GitHub repos carry no `-fusion` suffix (`code/`,
`origin-labs-ai/code`; `transformers/`, `origin-labs-ai/transformers`) - reaffirming D-24 -
while the product names **CodeFusion** and **Transformers-Fusion** are unchanged (D-28).
The alias registry lists each accepted spelling exactly once; a repeated variant is a
documentation defect and is removed.

**Trace:**
- *"Zenix-CC ab 'Zenix' only reh chuka hai, CC hat gaya hai, ab dono repos me se *-fusion hat
  gaya hai ... is file me ... 2 baar 'Transformers-Fusion' repeated hai to ek hataa dena,
  aise-aise jitne bhi jhol hai sab fix kar dena!"*

**Executed (2026-11-13):**
- Master plan §1: duplicate `Transformers-Fusion` alias removed from the accepted-variants
  table and the §1.1 alias registry; a path/repo note now states that folders and GitHub
  repos carry no `-fusion` suffix while product names stay unchanged.
- Master-plan §16: the D-28 entry's "before" spellings were restored (`TransFormers-Fusion`,
  `TransFormers-FusionIDX`) after the sweep had rewritten both sides of the arrow.
- `code/scripts/rebrand/fix-zenix-cc.mjs` -> `fix-zenix.mjs`; `migrate-arch.mjs` reference
  updated; all `Zenix CC` strings removed from the tooling.
- `code/BRAND.md`, `code/arch/windows.json`, `code/arch/brand.ts`, `code/launcher/index.html`
  and `code/windows/zenix/window.json` already use **Zenix** / `windows/zenix`; the new
  `window.json` is tracked and `windows/zenix/SOURCE/` stays local-only.
- `.plan/review-tracking/FINAL_REPORT.md` and `PROGRESS.md` carry dated correction notes for
  their historical `Zenix CC` rows.
- `.plan/telemetry/gen_dashboard.py` deletion note updated to `zenix-cc -> zenix`; the
  dashboard is regenerated after the sweep.
- Historical documents keep historical spellings where they are explicitly history:
  `.plan/_archive/`, this decision log's older entries, and verbatim operator quotes.


## D-30 · Wire-magic identity: engine `.idx` accepts `Transformers-FusionIDX` + `TransCenderIDX` only; `SolIDX` is model-manifest-only (operator, 2026-11-13)

**Rule:** a model name is not an engine wire identity. The `.idx` format belongs to the engine,
so its magic is the engine's own identity:

| Namespace | Accepted | Rejected |
|---|---|---|
| Engine `.idx` | `Transformers-FusionIDX` (22 B, current); pre-D-28 capital-F spelling (same 22 B, read-only); `TransCenderIDX` (15 B, the engine's former name - "formerly known as") | `SolIDX` (7 B), `InNovaIDX` (10 B) |
| Model manifest | `SolIDX` (7 B incl. NUL), reserved and specified - no engine consumer | - |

`SolIDX` is documented as a **model-manifest magic** in `transformers/docs/MODEL_MANIFEST.md`.
`tracesol` stays as the cosmetic Plotly series name. `Sol` remains the trained model family
(`sol-4-flash`).

**Legacy names.** `InNova` (the pre-rename model family, now `Sol` / `sol-4-flash`) and
`InNovaIDX` (the pre-rename wire magic, now retired) are historical names only. They are never
current identifiers, and `InNovaIDX` stays rejected by the engine `.idx` reader.

**Trace:**
- *"ye TransCenderIDX kyu SolIDX banaa? Bhai, Seedha matlab ye tha ki Transformers-FusionIDX /
  TransCenderIDX same cheej the yaani TF = TC tha, Sol to wo model ka naam socha gaya jo ki train
  kara jaayega ya fine tune karaa jaayega, ye kya jhol ho gaya!"*
- *"InNovaIDX bhi nahi rakhna hai naa! Hame TransCenderIDX / Transformers-FusionIDX dono is also
  known as ya formerly known as bhi daal sakte hai!"*

**The defect.** The 2026-11-12 rename wave (`D-27`, "Sab rename hoyega!") treated `SolIDX` as the
new name of the `.idx` legacy magic and shipped a 7-byte reader branch. That conflated the engine
wire namespace with the model namespace, and it made old 10-byte `InNovaIDX` files unreadable.
The correct equivalence is `Transformers-FusionIDX` = current engine identity and
`TransCenderIDX` = the same engine's former name; `Sol` names the model, not the file format.

**Executed (2026-11-13):**
- `transformers/src/codec/quant_format.cpp`: removed the `SolIDX` branch; `TransCenderIDX` is the
  only legacy engine branch. Writer still emits `Transformers-FusionIDX` (22 B).
- The pre-D-28 capital-F magic is compared byte-wise (`"Trans"` + `'F'` + `"ormers-FusionIDX"`) so
  the source tree never carries the old spelling; the reader still accepts it for read compatibility.
- Reader minimum size raised to **23 B** (15 B legacy magic + 8 B header); the 15 B guard was sized
  for the retired 7 B magic.
- Every early return after ownership transfer nulls `data_` as well as `mapped_file_`; the
  22-byte-magic-only probe exposed a dangling `data_` that made `valid()` return true.
- `transformers/include/quant/quant_format.h` and
  `transformers/install_test/include/quant/quant_format.h` comments corrected.
- `transformers/tests/test_sha256_corrupt.cpp`: **Test 8** asserts `TransCenderIDX` decodes and
  `SolIDX`/`InNovaIDX` are rejected.
- Proof: `build-norm/tests/test_sha256_corrupt.exe` -> **28 tests, 0 failures, exit 0**;
  `transformers/SHA256_TEST_LOG.md` regenerated.
- Docs: `transformers/README.md` §9 and §12; `transformers/PROGRESS.md` (dated correction bullet,
  historical entries marked superseded); new `transformers/docs/MODEL_MANIFEST.md`; this entry;
  master-plan §6.1 note, §10X coverage row and §16 D-30 entry; `.plan/telemetry/TODO-TREE.md`
  T3.2 closed and T3.5 annotated.

**Why `SolIDX` has a spec but no implementation.** No model-manifest consumer exists in the tree
today - the only manifest artefacts are `tools/dataset_manifest.schema.json` and the `PackManifest`
test struct. The project rule is zero dead code and zero stubs, so `SolIDX` is documented as
**reserved**, not implemented. The first consumer must add a writer, a reader and a regression test
before the status changes to **implemented**.

---

## D-31 · Exact documentation targets: 2048 / 4096 / 6144 LOC + a 512-page DOCX and PDF (operator, 2026-11-13)

**Rule:** the three project READMEs are built to **exact** line counts, and the publishable
research package is a **512-page** document in both `.docx` and `.pdf`:

| Repository | README target | Exactness |
|---|---|---|
| `fusion/` (superproject) | **2,048 LOC** | `wc -l` must equal 2,048 |
| `code/` (CodeFusion) | **4,096 LOC** | `wc -l` must equal 4,096 |
| `transformers/` (Transformers-Fusion) | **6,144 LOC** | `wc -l` must equal 6,144 |

This supersedes the T10 mapping recorded on 2026-11-12 (which had `fusion` at 4,096 and `code` at
2,048). The operator's words on 2026-11-13: *"CodeFusion repo me 4096 LOCs ka README banega,
Transfoemers-Fusion repo me 6144 LOCs ka and Fusion me 2048 LOCs ka, exact! Bhai, mera exact matlab
exact hi hota hai."*

**Format rule.** The visual reference is
`C:\Users\thaku\Workspaces\side-projects\origin-router\README.md`: centred header with an SVG logo,
one-line pitch, emoji navigation links, `shields.io` badges (`style=flat-square`), horizontal rules,
emoji-headed sections, tables, short command snippets and a licence/credits footer. Code snippets
stay **average/minimal** - a command, a call shape or a small type, never a wall of source.

**Page rule.** The 512-page package ships as **one document, two formats**: `PDF` typeset with TeX
Live 2026 (cover page, part dividers, running headers, page numbers, tables, callouts) and `DOCX`
generated with `python-docx` from the same page-block model. Each format **must** contain exactly
512 pages; 512 is not a target range.

**Telemetry rule.** Every generator writes a machine-readable manifest (target count, actual count,
sha256, timestamp, source commit) and the dashboard gains a documentation status section. The
generators live in `.plan/telemetry/docgen/`, are deterministic, read facts from the live tree, and
refuse to write a file whose count is off by even one line or one page.

**Trace:**
- *"Jo karna hai fix wo kar de, uske baad 512 page ka .docx and .pdf banayenge isi knowledge ke
  base par!"*
- *"Code snippets average hi rahenge, minimal level!"*
- *"Mast se cover page / main page / first page ke saath banana, TeX bhi installed hai .pdf banane
  ke liye! Python bhi hai! Look wisse bhi jagah hona chahiye!"*
- Implementation: `.plan/telemetry/TODO-TREE.md` T10 (READMEs), T13.2 (512-page package), T14
  (hygiene) and T15 (verification).

---

## D-32 · L2 tier codec: additive per-span DC refinement, adaptive H width, b=24 floor (implementation ruling, 2026-11-13)

**Rule (wire).** A K-tier payload is `[L-tier payload][refinement region]`, where
`region = ceil((base_bpw + delta)·n/8) - ceil(base_bpw·n/8)` — exactly 8 B for M and
16 B for H at n=256. The region carries signed per-span DC corrections; the unit is
`span_max/div` derived from the base decode, so no scale is stored and no payload can
exceed its name. Layout is resolved from `(n, base_bpw, region_bytes)` alone
(`block_codec.cpp:2649 tier_refine_layout`), so encoder and decoder agree from the wire.

**Why additive, not the planned multiplicative gain.** The LADDER draft specified 2-bit
sub-block scale multipliers `{×0.75, ×1.0, ×1.25, ×1.5}`. A global-scale codec's
dominant residual is a per-span DC offset; a multiplicative gain cannot express an
offset at all. Additive corrections dominate at identical byte cost, and they make
`q = 0` a bit-identical fallback to the base decode — which is what turns tier ordering
into a construction guarantee instead of a measurement.

**Correction quanta** (`block_codec.cpp:2616 tier_corr_div_m`):

| Family | M | H |
|---|---|---|
| plain | `2^(B+1)`, q ∈ [-2,1] | `2^(B+2)`, q ∈ [-8,7] (or adaptive narrower) |
| GRP | `2^(B+3)`, q ∈ [-128,127] | `2^(B+4)` = `2·div_M` when adaptive width > 8 |

GRP needed one bit finer than the first cut: at span 32, `2^(B+2)` rounded every q to 0
on a Q_8 uniform block (`nz = 0/8`, gain 0.000%); `2^(B+3)` gives 0.689%. Evidence:
`.plan/.rea-tmp/probe_grp8.cpp` → `span=32 shift=10 nz=0/8 ... gain 0.000%`,
`shift=11 nz=5/8 ... gain 0.689%`.

**Adaptive H width (n=48 coverage bug).** With a fixed 16-bit GRP H field, a 3-byte H
region at n=48 funds only ONE span while M's 2-byte region funds two 8-bit spans. H
therefore skipped a span M refined and lost 17.785% on a real trained bias
(`chunk@0 n=48 M=0.22645648 H=0.266731497`, span `[32,48)` worse). Fix: H picks the
largest width in `[9,16]` (GRP) / `[3,4]` (plain) that still funds `spans_m`; if even
`bits_min` cannot, it uses the exact M layout and ties instead of losing. The H seed is
the M winner scaled by `kdiv = div_H/div_M = 2`, which is exactly representable in
float, so `MSE(H) ≤ MSE(M)` holds span by span. After the fix: `bad(H>M)=0` over all
chunks of the trained model, and `test_tier_order` reports 0 strict failures.

**b=24 float floor.** `Q_24` is the top 24 bits of an FP32 (16-bit mantissa). The
M-vs-H correction difference is ~0.03 float ULP at the span max, so the decoder's
float32 add rounds both to the same values (`corrM == corrH` bit-for-bit on all 8 spans
of the tied block; probe `.plan/.rea-tmp/probe_grp24.cpp`). Contract: strict `M < L`
everywhere, strict `H < M` for `b < 24`, per-case tie allowed at `b = 24` (4/66
measured), and AGGREGATE `H < M` strictly at every rung in both families. This is a
float-output limit, not a wire shortfall: the H payload is still 8 bytes wider.

**D-22a cap raise (contract change, not a relaxed test).** `Q_G_3` is now a
byte-identical alias of `Q_3`, so its fuzz cap must cover the plain codec's worst
measured NMSE (0.9522 on the deterministic outlier corpus). Cap raised 0.80 → 1.00 in
`tests/test_fuzz_codec.cpp:146` with the provenance comment at `:140-145`. The old 0.80
belonged to the pre-D-22a grouped encoder, which is no longer the layout under that id.

**L2d invariants pinned** (`tests/test_format.cpp`): exactly 36 invalid ids out of
`FORMAT_ID_SLOTS = 105`, invalid + `FORMAT_COUNT` == slots, the exact retired set is
invalid with `format_bpw == 0`, and `format_is_half` is false for every id.

**Evidence (commands + results):**
- `test_tier_order.exe` → exit 0; `aggregate NMSE strictly decreases at every rung and
  family`; `min relative gain b<24: M<L 0.0465%, H<M 0.0001%`; `b=24 ... 4/66 H==M ties`.
- `test_ternary_tail.exe` → exit 0; `n=1..512 store exactly ceil(1.5n/8) bytes`;
  `n=256: 48 B, 16 b scale + 368 b base-3 trits + 24 slots`.
- `test_format_audit.exe` → exit 0; 69 rows `ok`, `BPW violations: 0`.
- `test_fuzz_codec.exe` → exit 0; `69 formats, 10052 generated tensors, 693588
  roundtrips, 0 crashes`.
- `grp_proof_test.exe` → exit 0; `QG3 real-weights PSNR: 29.8756 dB (Q3 plain:
  29.8756 dB)`.
- `test_block_codec.exe` → exit 0; `ALL BLOCK CODEC TESTS PASSED!`.
- **Full gate:** `ctest --test-dir build-gate --output-on-failure -j 4` → `100% tests passed,
  0 tests failed out of 78`, `Total Test time (real) = 97.00 sec` (78 = 76 before
  `test_tier_order` + `test_ternary_tail`).
- **Full technical record:** [L2-CLOSEOUT.md](L2-CLOSEOUT.md) — scope, wire contract, both
  bugs with before/after evidence, every test assertion, files touched, and the explicit
  pending queue.
