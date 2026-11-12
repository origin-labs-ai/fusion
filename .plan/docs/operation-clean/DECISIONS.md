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

## D-09 · M-tier encoder (design decision, pre-authorized)

**Rule:** M tier = base layout + 1 refinement byte per 32 weights
(4 × 2-bit sub-block scale multipliers {×0.75, ×1.0, ×1.25, ×1.5}) — engine-agnostic,
provably +0.25 BPW exact. Per-family alternatives (e.g. soft-threshold for the binary
family) may supersede ONLY if measurably better; acceptance gate stays: PSNR strictly
between L and H on 4 fuzz distributions + real weights.

## D-10 · Ternary tail policy (design decision)

**Rule:** for block sizes where the exact-1.50 ternary layout doesn't decompose
(cleanly), the encoder NEVER inflates: it drops to the largest tier that fits the
name's wire budget exactly (ternary → M → L, per-size). Same policy for every
rewired format: budget guard pattern of `quant_grp16:879-884` (a real budget test,
never the `has_d = (n >= 8)` non-test that caused the quant_6k overrun).

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
