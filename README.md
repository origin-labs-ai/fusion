# Fusion

Fusion is the **superproject** that tracks two component repositories as Git submodules:

- [Transformers-Fusion](https://github.com/origin-labs-ai/transformers) - the C++20 engine (folder: `transformers/`).
- [CodeFusion](https://github.com/origin-labs-ai/code) - the Launcher Desktop workspace (folder: `code/`).

> **GOAL LINE (2026-11-12, D-27):** the MAIN goal is the **entire Fusion Superproject** - every
> domain, seat and track complete. The SIDE goal is to achieve the **MAXIMUM at EXACT 1.0 BPW**
> (not 1.5; the implemented 1.5 BPW path is a stepping stone). Both FP (floating point) and INT
> (integer) quantization format families are in scope for research. Loop Quantization has never
> been implemented for any model anywhere - the Track B implementation here would be the first.

## What lives where

| Path | What it is |
|---|---|
| `.plan/` | The master plan, decision log, review tracking, archives, **telemetry** |
| `.plan/telemetry/DASHBOARD.md` | **Live status dashboard** - regenerate after every step |
| `.plan/telemetry/TODO-TREE.md` | The grind plan: to-dos with sub-to-dos |
| `.plan/telemetry/BLUEPRINT.md` | Full development blueprint + workflow pipeline |
| `.plan/docs/operation-clean/DECISIONS.md` | Binding decision log (D-01..D-27+) |
| `.plan/_archive/` | Reference-only port of every doc ever deleted from either repo |
| `code/` (submodule) | 7 seats, launcher, architecture registry, gate scripts |
| `transformers/` (submodule) | The engine: quantization ladder, Inferno, benches |

## Context-recovery contract (for any agent picking this up cold)

Read exactly these, in order, and you will know the project: **1)** `.plan/telemetry/DASHBOARD.md`
(live state) - **2)** `.plan/telemetry/TODO-TREE.md` (what is being worked, what is next) -
**3)** `.plan/docs/operation-clean/DECISIONS.md` (every binding ruling) - **4)** the OPERATOR
REMINDER at the top of the master plan (`.plan/pasted-content-id-43ed-ye-aur-melodic-puddle.md`).
Run `python .plan/telemetry/gen_dashboard.py` to refresh the dashboard from live state.

## Clone

```bash
git clone --recurse-submodules https://github.com/origin-labs-ai/fusion.git
cd fusion
git submodule update --init --recursive
```

If you already cloned without submodules, run the update command from the repository root.

## Contributing

- For engine code, tests and quantization work, contribute in [Transformers-Fusion](https://github.com/origin-labs-ai/transformers).
- For launcher or component-registry work, read the contribution scope in [CodeFusion](https://github.com/origin-labs-ai/code) first.
- For changes to the set of component revisions or the plan, update this repository
  (`.plan/` is tracked here; component source is tracked in the submodules).

## Licensing

This superproject has no separate top-level license declaration. The component repositories and any third-party material within them may have different licensing terms. Review each component's license and provenance before using or redistributing its contents.
