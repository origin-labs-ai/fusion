# CodeFusion — Continuation Report (2026-10-27)

Session source: ZCode `session_e457ee6bc5a4f1ca937c4301f1eeba09` ("Stacky Crunch", 553 messages)
plus the follow-up Repo Wiki / branding request.

## 1. Baseline repair (damage from the rebrand pipeline)

`pnpm typecheck` went from a hard failure (truncated sources, missing exports, malformed
tsconfig, broken vitest config) to **green** by reconstructing:

| File | Damage | Fix |
| --- | --- | --- |
| `packages/services/src/node.ts` | service chain unterminated: plugin-management registration, `return services`, closing brace missing | restored chain, registered `IPluginManagementService`, added `createTelemetryUserIdLoader` |
| `packages/services/src/plugins/pluginManagement.ts` | import head + `withPluginTelemetry` tail lost | rebuilt contract + Proxy telemetry tagging |
| `packages/services/src/plugins/pluginManagementService.ts` | entire factory head lost | rebuilt from tests (action mapping, noop/partial/cancelled, fire-and-forget telemetry) |
| `packages/shared/src/cf-protocol-v4/methods.ts` | `V4_METHODS` / `V4Method` missing | new module with the 33 wire methods (values pinned by existing tests) |
| `packages/services/src/cf-agent/cfAgentService.ts` | `isOffPeakToolSupported`, `getMcpStatusClient`, `resolveSavedWorkflowCarrier`, `disposeLocalState` lost | rebuilt from call sites + off-peak policy tests |
| `packages/desktop/src/main/browserView/browserCommandScripts.ts` | snapshot/element scripts truncated mid-string | rebuilt to `browserSnapshotSchema` (refs, DOM tree, xpath, rect, viewport) |
| `packages/desktop/src/main/exportLogs.ts` | redaction/collection helpers lost + function swallowed by missing brace | rebuilt encoding detection, sanitization, exclusions, lookback, about content |
| `packages/ui/tsconfig.json` | `paths`/`include` corrupted → `tsc` crash `paths[key] is not iterable` | restored `"@/*": ["./src/*"]` + include |
| `vitest.config.ts` | truncated projects block | restored `unit` + `fork-isolated` projects |
| `packages/ui/src/v4/ConversationShareReadonlyTimeline.tsx` | presentation components + snapshot context lost | rebuilt `UserInput/AssistantText/Reasoning/ToolCall` presentations, `ToolSnapshotContext`, `toolNodeWithSnapshot` |
| `pluginManagementStore.ts` / e2e helpers | missing interface head, truncated string, corrupted scenario | repaired; R3 server-update case marked `test.skip` pending re-authoring |

## 2. Repo Wiki (new feature)

**Evidence base (rewritten 2026-10-28):** the previous version of this section cited a
page layout (`.qoder/repowiki/knowledge/<lang>/…`, `WIKI_INIT`) that was never observed in
the shipped app. It has been withdrawn. The authoritative record is
`review-tracking/QODER_REPO_WIKI_RE.md`, produced from the installed **Qoder 1.18.0** at
`%LOCALAPPDATA%\Programs\Qoder` plus its own cache. What that evidence actually shows:

- cache `SharedClientCache/repowiki/{knowledge.db (+wal/shm), wiki_snapshots/<hash>/<lang>/{metadata.json, mtree.json, files/**}}`
- key `<project>#wiki#<branch|Q0DeR-MaG1C-…-C0MmIt>#wiki#<lang>`; DB tables
  `agent_knowledge_task|upload|workspace` (schema quoted in the RE doc)
- ingestion caps 250 000 files / 100 000 indexed / depth 100 / 10 000 per dir, `.qoderignore`
- message surface `wiki/startGenerate|cancelGenerate|pauseGenerate|getStatus|getContent|…`
- `.qoder/repowiki` is the import/export sync dir; generation is server-side and
  credit-gated; **the page-level Markdown layout was not observable** (no completed
  generation exists on this machine), so CodeFusion's page layout is our own design.

CodeFusion implementation (original code):

- `packages/shared/src/repo-wiki.ts` — contracts, `RepoWikiSnapshot.workspaceKey`, and
  `repoWikiWorkspaceKey()` implementing Qoder's exact key shape + sentinel branch.
- `packages/services/src/repo-wiki/` — scanner (bounded walk, `.qoderignore`, language
  stats, modules, excerpts, fingerprint), prompt builder, storage
  (`.cf/repowiki/<lang>/wiki.json` + pages), service (jobs, progress, cancel, manifest).
- `packages/ui/src/repo-wiki/` — the in-app view is unwired (see §8); the service and CLI
  remain the supported surfaces.
- `cf wiki [list|show <slug>|path] [--lang xx] [--json]` — read the wiki from the terminal.
- tests: `repoWikiService.test.ts` (4) + `repoWikiScanner.test.ts` (4) — 8/8 green,
  covering `.qoderignore`, depth/per-dir ceilings, and the workspace-key shape.

Generation uses the host's current model via `cfAgentService.generateWorkspaceText`; there
is no free/paid gate — the legacy `freeOnly` flag only narrows the candidate list when a
caller asks for it explicitly.

## 3. Branding / version

- `cf-logo.png` ← provided CF monogram; `cf-wordmark-logo.png` ← provided CodeFusion wordmark
- About page: wordmark, “CodeFusion IDE”, version, commit, build time, platform, links
- Display name: `CodeFusion IDE` / `CodeFusion IDE Preview` (electron identity), web title,
  native About panel
- Version: root `3.17.0` (drives `CF_VERSION` for desktop + web), package-lock synced
- lock/package name leftovers (`zcode`) removed

## 4. CJK purge

- translation map: 26,326+ unique strings translated (LLM, resumable via
  `scripts/rebrand/cjk_phase3_translate.py`)
- apply pass validated on the real tree: 35,402 replacements across 3,547 files with
  property-key skipping and quote escaping; **reverted** afterwards because a string-only
  rewrite leaves Chinese regex literals, comments and assertions behind and caused 142
  test failures (`cfAgentProcessManager` expects `/字节码入口缺失/`, etc.)
- current shipped state: unchanged Chinese surface (reverted), typecheck + targeted tests green
- next step: extend the pipeline to regex literals and comments (and translate both sides of
  test assertions in the same pass) before re-applying; 1,169 source files still contain Han
  characters

## 5. CF plan R4–R6

All source paths named in `DEFECTS.md` for CF (MAD/god-runtime/byok/cordis/home-paths/
hooks-claude-code/web scaffold) are absent from the shipped tree; documented as
verified-not-a-bug in `DEFECTS.md` §H instead of fabricating fixes.

## 6. Not lifted from `cf-old` (and why)

- `cf-old/packages/mad/**` (28 files, 83 KB) — MAD runtime; the new CLI has no MAD host,
  so `/mad` needs a port + workflow bridge design (see below)
- `cf-old/skills/design/**` (16 brand systems + 30+ HTML exemplars) — reference assets,
  intentionally not shipped
- retired ACP runtime, cordis host/client runners, BYOK modules — superseded by the new
  agent CLI (`apps/cli`)
- `.agents/notes/**` archive — kept deleted by the rebrand baseline

## 7. MAD — natively integrated (2026-10-28)

MAD is no longer vendored-but-dead. It is a first-class part of the tree:

**Packages (`apps/cli/packages/mad/`, 7 sibling packages + 2 foundations)**
- Added `@origin-ai/cf-brand` (`brand/`) and `@origin-ai/cf-invariants` (`invariants/`) —
  the two packages cf-old imported but never shipped. `invariants` provides the cordis
  service (`ctx.invariants.register/list`) via `ctx.reflect.provide`.
- Vendored `@deepseek-ai/cordis` (prebuilt) and `@deepseek-ai/cosmokit` at
  `apps/cli/vendor/*`, wired with `workspace:*`; both workspace manifests list
  `packages/mad/*` and `vendor/*`.
- All MAD packages export TypeScript source (`main`/`types`/`exports` → `src/*.ts`) so the
  CLI esbuild bundle compiles them directly — no build-order coupling.
- All cross-package deps are `workspace:*` (brand, invariants, cordis) and `god-runtime`
  now depends on `cf-discussion-bus`, `cf-verification`, `cf-memory-fabric`.

**Runtime (`god-runtime/src/index.ts`, rewritten)**
- 2-stage router: eligibility filter (availability/health) + scored selection
  (VOI + empirical history + diversity + evidence quality − latency − cost − correlation),
  with `recordOutcome`/`empiricalPerformance` fed by completed tasks.
- Scheduler: token/time/cost/concurrency ceilings, `charge`, exponential backoff
  (`handleFailure` → attempts, `retryAllowed`, `nextAttemptAt`), `restore` for resumed runs.
- Discussion: real `DiscussionBus` service (claims/hypotheses/questions/evidence/
  counterarguments) with the `UNTIL_CONTEXT_CLEAR` convergence checker.
- Claims are evidence-gated: a claim without evidence stays `proposed` and
  `resolveClaim(accept)` throws; `finalize` reports every evidence hash.
- Arbiter counts distinct evidence hashes, returns `undecided` on ties/empties, and never
  invents a winner.
- `snapshot()` / `GodRuntime.restore()` round-trip a run (tasks, routing, claims, bus,
  budget usage) so each CLI invocation can resume the same run.

**CLI + skill**
- `cf mad status|run|list|show|discuss|claim|resolve|arbiter|complete|cancel|finalize`
  (`apps/cli/packages/cli/src/mad-command.ts`, wired in `run.ts`; local JSON formatter so
  the command has no core-dist dependency).
- Runs persist to `<workspace>/.cf/mad/runs/<runId>.json` + `latest.json` and emit
  `<runId>.orders.md` work orders.
- Bundled `/mad` skill (`apps/cli/packages/bundled-skills/skills/mad/SKILL.md`) documents
  the protocol and the bidirectional handoff with `/workflow`: MAD emits orders, the
  workflow skill executes them, results come back via `cf mad complete` / `cf mad claim`;
  a workflow may also open a MAD run and read the decision back with `cf mad show`.

**Verified**: `node --import tsx --test apps/cli/packages/mad/god-runtime/test/*.test.ts`
→ **13/13 pass** (7 runtime tests, 6 command tests: routing, budgets, backoff, arbitration,
evidence gate, snapshot restore, cancel, persistence, work orders).

## 8. IDE vs main split (corrected 2026-10-27)

- **`code/`** = the main ZCode-lineage app. Repo Wiki here is agent-native: the
  bundled `/repo-wiki` skill (`apps/cli/packages/bundled-skills/skills/repo-wiki/SKILL.md`)
  writes the wiki, and `cf wiki list|show|path` reads it. The in-app Repo Wiki sidebar/view
  is no longer wired (props optional, App no longer passes them); service + CLI remain.
- **`code/IDE/`** = the separate editor window. New Vite + React app
  (`IDE/package.json`, `server.mjs`, `src/App.tsx`) with the Repo Wiki view: CF logo,
  "CodeFusion IDE", page tree, status badge, sanitized Markdown (DOMPurify + marked).
  It reads `<workspace>/.cf/repowiki/<lang>/` through `GET /api/wiki` (port 5175).
- No "free models only" toggle anywhere: the IDE and skill use the configured model; there
  is no plan gate and no quota check (the Qoder screenshot's "Upgrade plan" is Qoder's own
  paywall, not part of this implementation).

## 9. Verification (2026-10-28)

```bash
NODE_OPTIONS=--max-old-space-size=8192 pnpm typecheck   # 0 errors (default 2 GB heap OOMs)
cd IDE && npm install && npm run build                  # tsc -b + vite build, dist/ emitted
node --import tsx --test apps/cli/packages/mad/god-runtime/test/*.test.ts   # 13/13
pnpm exec vitest run packages/services/test/repoWikiService.test.ts \
  packages/services/test/pluginManagementService.test.ts \
  packages/services/test/telemetryUserIdLoader.test.ts   # 15/15
pnpm exec vitest run packages/desktop/test/exportLogs.test.ts  # 22/22
```

Repairs made while unblocking the build (see `## 10`).

Note on the IDE UI check: an earlier browser pass rendered the Repo Wiki view against a
hand-written demo workspace. That fixture was **deleted** (2026-10-28) because its numbers
and pages were synthetic; the IDE build and API are verified, but end-to-end rendering must
be re-checked against a real generated wiki, not a fixture.

## 10. CJK-damage repair (2026-10-28)

The rebrand translation pass had unescaped quotes and truncated lines across JSON and TS.
Fixed in this pass:

- `config/provider/cf-builtin.json` + `cf-builtin.test.json`: 63 strings each re-escaped →
  both parse again (the CLI build failed on these).
- 11 `tsconfig*.json`: `lib: es2025` → `es2024` (the base config's level; older bundled TS in
  the editor rejected `es2025`, which produced the `--lib` warnings in the Problems panel).
- `apps/cli/packages/dynamic-workflow`: regenerated `src/compiler/libs.generated.ts` (it had
  been double-escaped), repaired quote damage in `artifacts.ts`, `world-run.ts`,
  `engine.test.ts` (two truncated tests restored) and `hole-sites.ts` → package builds green.
- Repo-wide `scripts/repair-ts-quotes.mjs` (parser-driven, only accepts a candidate when the
  parse-diagnostic count drops) fixed 14 files; `scripts/repair-escaped-quotes.mjs` fixes the
  JSON class.
- `@origin-ai/cf-core`/`cf-adapters`/`cf-i18n` "cannot find module" in the editor is a
  **build-order** symptom: those packages export `dist/*`, and `apps/cli` dists are not built.

**Still open (pre-existing, not caused by this pass):** three `apps/cli` sources were
truncated by the same pass and cannot be reconstructed from any tree on disk —
`core/src/tool/handlers/agent.ts`, `core/src/tool/handlers/create-workflow-source.ts`,
`bootstrap/src/cf-protocol-v4/v4-gateway.ts`. Until the upstream sources are restored,
`pnpm --dir apps/cli run build` cannot complete, so the `cf` binary (and therefore the
`cf mad` entry point) is exercised through its test harness rather than a built binary.

## 11. Qoder skills vendored + IDE rebuilt from real UI copy (2026-10-28)

**Skills.** All Qoder-provided command skills were copied into
`apps/cli/packages/bundled-skills/skills/`, verbatim, and de-duplicated by name against
what CodeFusion already shipped (zero name collisions were found):

| Source | Count |
| --- | --- |
| `~/.agents/skills` (the environment's "/" skills) | 47 |
| `~/.qoder/plugins/cache/qoder-bundler` (better-harness, computer-use, create-plugin, security-scan) | 4 |
| `/knowledge-plan` — built-in command, materialised from its exact payload | 1 |

Provenance + per-skill sha256: `apps/cli/packages/bundled-skills/skills/QODER_SKILLS.md`.
`scripts/rebrand/rebrand_skills_cf.mjs` then rebranded the vendored set: 239 product-name
tokens rewritten ("Qoder" → "CodeFusion", `.qoder/` → `.cf/`). Research datasets, fixtures
and platform adapters (`platforms/qoder.mjs`) were deliberately left untouched, because they
describe Qoder as an external subject or key off its name.

**IDE window.** `IDE/` was rebuilt around Qoder's real screen copy instead of invented text:

- `IDE/src/qoder-strings.json` — 334 strings extracted from the installed bundle by
  `scripts/re/qoder-extract-strings.mjs` (`repoWiki.*`, `quest.knowledge.*`).
- `App.tsx` renders Qoder's structure: repository filter + search, per-document status dots,
  toolbar (`Update`, `Import from .cf/repowiki`, `Synchronize`, `Generate`), the
  "Generate Your Repo Wiki" card with Language / Auto Update / Citation / Export-to tiles,
  and `Create With Plan` wired to `/knowledge-plan`.
- Credit-only wording is dropped (no "Free …", no "(N Left)") because CodeFusion has no
  quota; the IDE never calls a model itself — it copies `/repo-wiki` or `/knowledge-plan` and
  the agent generates into `.cf/repowiki/<lang>/`.

Verified in the browser against the real workspace (no fixture data): brand, search,
repository `code-fusion`, branch `master`, "Not generated" badge, all four toolbar buttons,
the generate card and its four tiles, and the `/knowledge-plan` toast
(`Copied /knowledge-plan — run it in CodeFusion chat.`), with zero console errors.
`npm run build` emits `dist/` (`tsc -b` + vite).

## 12. Desktop binary: extracted source + rebranded launch (2026-10-28)

The installed Qoder app was copied to `code/CF-Desktop/` (4 703 files, 842 MB) and
inventoried file-by-file (`CF-Desktop/SOURCE/MANIFEST.jsonl`, sha256 per file):

- **3 778** application files (JS/JSON/CSS/HTML/TS/docs, 279.5 MB) — full source, beautified
  into `CF-Desktop/SOURCE/beautified/` (≈4.33 M readable lines across the main process,
  workbench, agents window and the aicoding-agent extension; `node --check` passes).
- **153** native payloads (`.exe/.dll/.node/.pak`, 545.6 MB) — machine code, inventoried only.

`CF-Desktop/CodeFusion.exe` is the genuine binary (sha256 identical to `Qoder.exe`), and the
application layer was modified in place:

| Change | Proof |
| --- | --- |
| `product.json` identity → CodeFusion (`nameShort`, `win32*`, `win32AppUserModelId`, `urlProtocol`) | JSON valid, values in file |
| `package.json` name → `codefusion` | JSON valid |
| `resources/bin/x86_64_windows/Qoder.exe` → `CodeFusion.exe` | Go service starts and health-checks |
| `out/main.js` window title `"Quest Window"` → `"CodeFusion"` | sha256 `b011d056…` → `5feb0fd6…` |

Launched the copy: 12 `CodeFusion` processes, both top-level windows titled **CodeFusion**,
workbench + Quest panel rendered with no error dialog (`SOURCE/proof/*.png`). Documented in
`CF-Desktop/SOURCE/README.md`, including the hard limit: no C++/Chromium source exists, so
the JS resource layer is the modifiable surface.

## 13. Current state — restructure, codenames, launcher (2026-10-31)

**This section supersedes the paths in §8, §11 and §12.** The repository was restructured:
`code/` now holds `architecture/`, `launcher/`, `windows/` and `BRAND.md`; the old
tree (`apps/`, `packages/`, `docs/`, `scripts/`, `vendor/`, `node_modules/`) sits read-only in
`.dead/` with `OLD-TREE-NOTICE.md`.

Live layout:

```
arch/{windows.json, brand.ts, README.md}   registry + typed resolver
launcher/{index.html, launch.ps1, window.json}     Launcher Desktop (window title "Launcher")
windows/<codename>/                                one folder per part
BRAND.md                                           naming: decided vs undecided
```

Parts and alias ladder (Lite → Plus → Pro → Studio → Max → Ultra):

| Codename | Alias | Folder | Contents | Status |
| --- | --- | --- | --- | --- |
| Ingot | Max | `windows/ingot` | monorepo tree, 160,239 files (3.9 GB) | present |
| Onyx | Studio | `windows/onyx` | reverse-engineered Qoder build, `CodeFusion.exe` + `SOURCE/` | present |
| Chromix | # | `windows/chromix` | Zephium browser source | present |
| Codeix | Pro | `windows/codeix` | OpenAI Codex MSIX (`ui-old`, `ui-new`) + toggle | present |
| GSX-CLI | # | `windows/gsx-cli` | opencode workspace + MiMoCode (Xiaomi) source | present |
| Zingma | Lite | `windows/zingma` | empty — seat for Qoder's native Quest/agents window | empty |
| Sonar | Plus | `windows/sonar` | empty — seat for the reverse-engineered DeepSeek Harness | empty |
| Zenix CC | Ultra | `windows/zenix-cc` | empty — seat for native Claude Desktop | empty |

Rules now enforced by the registry (`arch/windows.json` is the single source of
truth; `launcher/launch.ps1` and every `window.json` are derived from it):

- No part is named "CodeFusion"; the only surviving string is the Obsidian/Onyx executable
  name `CodeFusion.exe`.
- An alias resolves to exactly one part; `#` means the alias seat is retired (`Core`,
  and Chromix/GSX-CLI hold none).
- Roles are not assigned: **Ingot is not the main part**.
- `windows/onyx` is a real folder again; the junction is gone.

Open items: place the three empty seats (Zingma, Sonar, Zenix CC), rename the physical
`obsidian` folder to `onyx`, and finish the `apps/cli` truncation repair tracked in §10.

