# Fusion Superproject - Development Blueprint

> Generated: 2026-11-12 (operator order: "Poora ka poora blueprint, pipeline, docs, master-plan -
> sab banaa daal"). Companion files: `telemetry/DASHBOARD.md` (live state),
> `telemetry/TODO-TREE.md` (the grind queue), `docs/operation-clean/DECISIONS.md` (rulings),
> master plan `pasted-content-id-43ed-ye-aur-melodic-puddle.md` (the plan itself).
> Language policy: all work documents are English; Hinglish is reserved for operator chat.

---

## 0. GOAL LINE (D-27 - read before anything)

- **MAIN GOAL = the ENTIRE Fusion Superproject** - every domain, seat and track, complete.
- **SIDE GOAL = MAXIMUM at EXACT 1.0 BPW** - not 1.5. The implemented 1.5 BPW path is a
  stepping stone; older "1.5 BPW" statements remain implemented-state facts.
- **FP + INT research:** both quantization families (floating point and integer) are in scope.
- **Loop Quantization has never been implemented for any model anywhere** - Track B would be
  the world's first.

## 1. Project map

| Component | Location | State |
|---|---|---|
| Superproject repo (this) | `fusion/` (git, origin-labs-ai/fusion) | Fixed 2026-11-12: submodules `code/` + `transformers/` |
| Master plan | `.plan/pasted-content-id-43ed-*.md` (~342 KB) | Loop Steps 1-6 complete, all 7 verifiers green |
| Decision log | `.plan/docs/operation-clean/DECISIONS.md` | D-01..D-27, append-only |
| Ladder contract | `.plan/docs/operation-clean/LADDER.md` | 69 formats, name == nominal == wire BPW |
| Telemetry | `.plan/telemetry/{gen_dashboard.py,DASHBOARD.md}` | Regenerate after EVERY step |
| Grind queue | `.plan/telemetry/TODO-TREE.md` | T1..T9 with sub-to-dos |
| Archived docs | `.plan/_archive/` | 288 files, reference-only, never overrides |
| Component: CodeFusion | `code/` submodule (origin-labs-ai/code) | 7 seats, launcher, arch registry, gate 13/13 |
| Component: Transformers-Fusion | `transformers/` submodule (origin-labs-ai/transformers) | Engine, quant ladder implemented, Inferno |
| Effort slider plugin | `code/slider/effort` (dsh-claude-effort-slider 0.9.4) | 38/38 tests; Sonar integration + Zenix port PARKED (D-25) |
| Code extraction RE | `code/windows/**`, `.rea-tmp/codex/` | All seats extracted; RE evidence preserved |

## 2. Domain pipeline (THE grind loop - applies to every domain)

```
RESEARCH  ->  DESIGN  ->  IMPLEMENT  ->  SECURITY AUDITS (5-10)  ->  FIX ALL  ->  VERIFY  ->  COMPLETE
   |             |            |                 |                     |            |
 browser     written     code + tests      5-10 distinct        bugs found     all 7 plan
 (in-app)    design      in the right      passes (memory,      are fixed,     verifiers +
           note into    submodule         wire-format,          never waived   code gate 13/13,
           the plan                       paths, gates,                       dashboard regen
                                          audits of Inferno
                                          breakdown included)
```

Rules of engagement (binding):
1. NO subagents. One to-do to 100% - never shift until it is done.
2. Ask after every to-do; wait for "Go." before the next.
3. Dashboard after every step: `python .plan/telemetry/gen_dashboard.py` and paste it in chat.
4. Research uses the in-app browser (`/browser-use:control-in-app-browser`); if a site will not
   open, the operator supplies the content.
5. Never weaken or skip a test to make it pass. Every "done" carries command + output + file:line.
6. Fix any bug found, even outside the current to-do's ownership.
7. Per domain: finish with the FULL Inferno-style breakdown - grind the to-do until nothing can
   be missed, then compare against the origin requirement and close every gap.

## 3. Domain status board (source: 2026-11-12 audit; live copy in DASHBOARD.md)

| # | Domain | Research | Design | Implement | Audits | State |
|---|---|---|---|---|---|---|
| T1 | Loop Transformers | DONE | open (G/S note) | - | - | closing research |
| T2 | Traditional Transformers | DONE | bench spec open | - | - | mostly done |
| T3 | Traditional Quantization (Track A) | DONE | contract DONE | DONE (ladder) | open | quality-floor rulings pending |
| T4 | Loop Quantization (Track B) | evidence DONE | open | **never done by anyone** | - | design + implement |
| T5 | Mix Quantization | PARTIAL (MX quarantined) | open | partial | open | literature pass needed |
| T6 | DSpine x NCM merger | spec DONE, NCM read pending | merger doc open | V20 bug open | open | read + design |
| T7 | EAIN | literature DONE | OPEN-DESIGN | - | - | scope + stack ruling |

## 4. Context-recovery contract (one-shot handoff)

If work is cut off, the next agent needs exactly one instruction:
**"Read `fusion/.plan/telemetry/DASHBOARD.md`, then `TODO-TREE.md`, then `DECISIONS.md`, then the
OPERATOR REMINDER at the top of the master plan."** That chain carries: live state, the current
to-do, every binding ruling, and the goal line. Regenerate the dashboard first if it looks stale.
`graphify-out/` (regenerated via the graphify skill; reminder tracked in TODO-TREE) additionally
carries the codebase-wide symbol map for `code/` and `transformers/`.

## 5. Workflow protocol (what "live dash" means)

1. Execute one to-do (or sub-to-do) fully.
2. Run `python .plan/telemetry/gen_dashboard.py` (runs all 7 verifiers + code gate live).
3. Post the dashboard in chat with a 3-6 line delta (what changed since last).
4. Update the to-do checkbox in `TODO-TREE.md` and the ledger tag in the plan when an item closes.
5. Ask the operator ("Go?" or the specific ruling needed), then proceed.

## 6. Parked (do not start without operator order)

- Sonar (DSH) effort-slider integration and Zenix port (D-25: "Both later").
- Git pushes (component repos hold peer-session uncommitted work; superproject commit `c9d6e9f`
  is local; push order not yet given).
