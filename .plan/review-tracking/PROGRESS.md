# PROGRESS — review-tracking / CF scope

Session: Dev Sprint. Scope per Prime Orchestrator: `review-tracking/` + `code/{arch,launcher,BRAND.md}` + `docs/CF_PLAN.md`.
Standing rule: SOLO (no subagents/workflows). Every claim carries proof.

---

## Current task

**CF drift verification** — Phase A of the assigned task (read DRAFT.md, verify claims against disk, list drift with file:line).
Fusion full plan (separate, user-assigned) is tracked in `C:\Users\thaku\.claude\plans\pasted-content-id-43ed-ye-aur-melodic-puddle.md` and is not blocked by this file.

## Last verified evidence (2026-11-01)

| Claim | Command | Result |
|---|---|---|
| `arch/` exists | `ls -d code/arch` | EXISTS: `README.md`, `brand.ts`, `windows.json` |
| `launcher/` exists | `ls -d code/launcher` | EXISTS: `README.md`, `index.html`, `launch.ps1`, `window.json` |
| `BRAND.md` exists | `ls -d code/BRAND.md` | EXISTS |
| windows folders on disk | `ls windows/` | `chromix codeix gsx-cli ingot onyx sonar zenix-cc zingma` (8) |
| exe on disk | `ls windows/onyx/*.exe` | **`Onyx.exe`**, `unins000.exe` — **no `CodeFusion.exe`** |
| DRAFT.md size | `wc -l review-tracking/DRAFT.md` | **511 lines**, 63 `## ` headings |

---

## DRIFT FINDINGS (all verified today, file:line)

### D1 — Aster vs Onyx: BRAND.md contradicts itself (CONFIRMED)

The alias table says **Aster**; the parts table and the rest of the tree say **Onyx**.

- `code/BRAND.md:40` — `| **Studio** | Aster | deep editor workspace |` ← **Aster**
- `code/BRAND.md:23` — `| **Onyx** | windows/onyx | present | Reverse-engineered Qoder desktop build — CodeFusion.exe plus SOURCE/; 4,715 files (943 MB) |` ← **Onyx**
- `code/BRAND.md:46` — `Sending an alias to the launcher resolves it: .\launch.ps1 studio → Onyx.` ← **Onyx**
- `code/arch/windows.json:37-38` — `"alias": "Studio", "folder": "windows/onyx"` ← **onyx**
- disk: `code/windows/onyx/`

**Evidence-led resolution (no operator question needed):** every machine-readable source of truth — registry, folder, launcher — says **Onyx**. The **single** Aster mention is the BRAND.md alias table at `:40`. Therefore **Onyx is the current name** and `BRAND.md:40` is the stale line.

**Label: OBSERVATION** (the five locations above) + **INFERENCE** (that `:40` is stale rather than a pending rename).

### D2 — `launch.ps1` expects an exe that does not exist (CONFIRMED)

- `code/launcher/launch.ps1:53` — `$exe = Join-Path $folder "CodeFusion.exe"`
- `code/launcher/launch.ps1:54` — `if (-not (Test-Path $exe)) { "Onyx has no CodeFusion.exe at " + $folder; exit 1 }`
- disk: `code/windows/onyx/Onyx.exe`

**`.\launch.ps1 studio` exits 1** — the file it looks for is absent. This is the peer's DRIFT #2 and it is **correct**.

**The root cause is D3 below**, not launch.ps1: the exe *was* `CodeFusion.exe`, someone renamed it to `Onyx.exe`, and two documents describing `CodeFusion.exe` were never updated.

### D3 — BRAND.md describes an exe name that no longer exists (CONFIRMED — new, my finding)

- `code/BRAND.md:23` — parts table claims **`CodeFusion.exe`**
- `code-fusion/BRAND.md:60` — *"The only `CodeFusion` string left in the tree is the executable name of Onyx (`CodeFusion.exe`); renaming it is a separate mechanical step."*
- disk: **`windows/onyx/Onyx.exe`** — there is no `CodeFusion.exe` anywhere under `windows/onyx/`

Both `:23` and `:60` are stale: the rename **already happened** and was not recorded. `:60` explicitly says renaming it is "a separate mechanical step" — that step has since been done.

**Label: OBSERVATION** for all three locations; **INFERENCE** for the "already happened, unrecorded" part (there is no commit log proving when).

### D4 — `index.html` and `launch.ps1` help text still say CodeFusion.exe (CONFIRMED — new)

- `code/launcher/index.html:79` — `Reverse-engineered Qoder desktop build — CodeFusion.exe plus SOURCE/; 4,715 files (943 MB).`
- `code/launcher/launch.ps1:10` — `.\launch.ps1 studio       # alias -> Onyx, starts CodeFusion.exe`
- `code/launcher/launch.ps1:56` — `"Started Onyx (CodeFusion.exe)"`
- `code/launcher/README.md:17` — `.\launch.ps1 onyx       # start CodeFusion.exe`
- `code/launcher/README.md:28` — `| Studio | Onyx | yes — CodeFusion.exe |`

Same root cause as D3. **The launcher's own docs and its success message both name an exe that is not on disk.**

### D5 — DRAFT.md contradicts its own self-description (CONFIRMED — new)

- `review-tracking/DRAFT.md:1` — *"every section is exactly thirty-two lines: one heading, thirty lines of prose, one blank line. **Sixty-four sections make exactly 2048 lines.**"*
- actual: **511 lines**, **63** `## ` headings

The document's header describes a 2048-line, 64-section artefact; the file on disk is 511 lines and 63 sections. Either the format contract was abandoned or this is a truncated copy. **DRAFT.md cannot be treated as the authoritative full plan** until this is resolved — which is exactly why the assigned task is to supersede it with `docs/CF_PLAN.md`.

**Label: OBSERVATION** (both numbers) + **INFERENCE** (which of the two formats was intended).

### Non-findings — peer claims checked and REJECTED

- **Peer DRIFT #2 wording:** peer said *"registry/launch.ps1 'CodeFusion.exe' expect karte hain lekin disk pe Onyx.exe hai"* — **the registry does NOT reference the exe at all.** `arch/windows.json` contains `name`, `alias`, `folder`, `contents`, `status` only (verified `grep '"exe"' arch/windows.json` → no match). The exe expectation lives **only in `launcher/launch.ps1`**, not the registry. Correction recorded so the fix targets the right file.

---

## Blockers

None. D1–D5 are all resolvable from evidence already gathered.

## Next planned step

1. Read `review-tracking/DRAFT.md` in full (511 lines) — sections 21–23 (Aster rename) are the immediate-action sections.
2. Read `review-tracking/QODER_REPO_WIKI_RE.md` and verify its claims still hold on disk.
3. Write `docs/CF_PLAN.md` superseding DRAFT.md (DRAFT.md kept for audit — repo rule).
4. Discovery plan for the three empty seats (Zingma / Sonar / Zenix CC).
