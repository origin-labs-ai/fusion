# Qoder Repo Wiki — reverse-engineering evidence (2026-10-28)

Target: the **installed native Qoder app** on this machine, not documentation and not memory.

| Item | Value |
| --- | --- |
| Install root | `C:\Users\thaku\AppData\Local\Programs\Qoder` |
| Package | `resources/app/package.json` → `name: Qoder`, `version: 1.18.0` |
| Family | Electron + VS Code fork (`product.json`: `nameShort: Qoder`, `dataFolderName: .qoder`, `licenseName: Proprietary`) |
| Second install | `C:\Users\thaku\AppData\Local\Programs\Qoder IDE` (same `resources/app` layout) |
| Layout | `resources/app/{out,extensions,node_modules,featureFlags.json,product.json}`; no `app.asar` (unpacked) |

Everything below is a quoted observation from those files or from Qoder's own cache.
No claim here is inherited from the earlier session notes.

## 1. Feature flag

`resources/app/featureFlags.json` (offset 158):

```json
{ ... "questModeSupportRemote": true, "repoWikiEnable": true,
  "codebaseIgnoreFileName": ".qoderignore", ... }
```

So Repo Wiki is a first-class, flag-enabled product surface, and Qoder honours a
`.qoderignore` file when choosing what to index.

## 2. Generation is a server task with credits — not a local prompt

`out/lingma/agents-window/agents-window.desktop.main.js` string table:

- `repoWiki.button.generateWithCredits` = 生成 (剩余{0}次) — "generate (remaining {n})"
- `repoWiki.button.regenerateWithCredits` = 免费重新生成（剩余{0}次）
- `repoWiki.button.upgradePlan`, `repoWiki.button.getMoreCredits`
- `repoWiki.subscription.teamsSuspendedAdmin` = …Repo Wiki 已停用… ("Repo Wiki has been disabled")

`extensions/aicoding-agent/dist/extension.js` contains the status forwarder
(`[WikiNotifyStatusHandler]`, `repoWiki:notifyStatus`) and a Mermaid repair round-trip
(`repoWiki:fixMermaidResult`, message type `wiki/fixMermaid/sync`).

Conclusion: the *content* is produced by Qoder's backend and streamed back through the
extension; the client keeps status, cache, and export/import. There is no local prompt
string in the shipped bundle that generates the wiki body.

## 3. IPC / message surface (verbatim strings from `extension.js`)

```
wiki/startGenerate   wiki/cancelGenerate   wiki/pauseGenerate   wiki/getStatus
wiki/notifyStatus    wiki/getContent       wiki/getCatalogs     wiki/changeLanguage
wiki/deleteIndex     wiki/regenerate       wiki/regenerateContent
wiki/update          wiki/updateConfig     wiki/synchronize      wiki/fixMermaid
wiki/fixMermaid/sync
```

Observer-side events: `repoWiki:notifyStatus`, `repoWiki:fixMermaidResult`.
Status payload fields seen in the log format string: `wiki_workspace_path`, `language`,
`branch`, `version`.

## 4. On-disk cache layout (this machine, real files)

```
%APPDATA%\Qoder\SharedClientCache\repowiki\
  knowledge.db        (+ -wal 94 KB, -shm)
  wiki_snapshots\<project-hash>\<lang>\
      metadata.json      (727 KB in the sample)
      mtree.json         (722 KB)
      files\<repo-relative paths>   (94 files copied verbatim, incl. .py/.md/.json)
```

Sample snapshot: `<hash>` = `792d9560d09f58a03bf6dba6fb796520`, `lang` = `en`,
`project_path` = `c:\Users\thaku\Downloads\Origin-Ultra-0.1-max`.

`metadata.json` keys (exact): `mtree`, `file_count` (94), `total_size` (1 222 555),
`created_at` (`2026-06-18T18:43:47.5981033+05:30`), `project_path`, `workspace_path`,
`relative_file_paths[]` (199 entries in the sample; Windows-style separators).

`workspace_path` is the cache key and has a fixed shape:

```
<project_path>#wiki#<branch>#wiki#<language>
c:\Users\thaku\Downloads\Origin-Ultra-0.1-max#wiki#Q0DeR-MaG1C-BrAnCh-Fo2-NoN-GiT-Or-No-C0MmIt#wiki#en
```

`Q0DeR-MaG1C-BrAnCh-Fo2-NoN-GiT-Or-No-C0MmIt` is the sentinel used when the project is not
a git checkout (or has no commit); a real branch name replaces it otherwise.

`mtree.json` is the ingestion index, not the wiki text:

```json
{ "rootPath": "c:\\Users\\thaku\\Downloads\\Origin-Ultra-0.1-max",
  "dirNum": 86, "fileNum": 535, "indexingFileNum": 378,
  "maxDepth": 100, "maxFileNum": 250000, "maxIndexingFileNum": 100000,
  "maxDirFileNum": 10000, "maxIndexingDirFileNum": 1000,
  "enablesSimHash": true, "simHasher": {…}, "simHashCache": {…},
  "root": { "relativePath": ".", "hash": "<sha256>", "rhash": "<sha256>",
            "indexing": true, "type": "root", "fileType": 0, "mtime": 0,
            "children": [ { "relativePath": ".env", "hash": "",
                            "rhash": "<sha256>", "indexing": false,
                            "type": "leaf", "fileType": 0, "mtime": 1781786244325 }, … ] } }
```

## 5. SQLite schema (`knowledge.db`, dumped with `node:sqlite`)

```sql
CREATE TABLE agent_knowledge_task (
  id VARCHAR(64) PRIMARY KEY, workspace_path TEXT, project_path TEXT, repo TEXT,
  org_id VARCHAR(64), branch VARCHAR(256), language VARCHAR(64), status VARCHAR(64),
  kind VARCHAR(32) NOT NULL DEFAULT 'wiki', parent_task_id VARCHAR(64) NOT NULL DEFAULT '',
  progress INTEGER, local_commit VARCHAR(64), local_commit_timestamp INTEGER DEFAULT 0,
  server_commit VARCHAR(64), server_commit_timestamp INTEGER DEFAULT 0,
  error_message TEXT DEFAULT '', gmt_create TIMESTAMP, gmt_modified TIMESTAMP,
  completed_at TIMESTAMP);

CREATE TABLE agent_knowledge_upload (
  id VARCHAR(64) PRIMARY KEY, task_id VARCHAR(64), workspace_path TEXT, repo TEXT,
  org_id VARCHAR(64), branch VARCHAR(256), status VARCHAR(64), reason TEXT DEFAULT '',
  commit_hash VARCHAR(64), commit_timestamp INTEGER DEFAULT 0,
  retry_count INTEGER DEFAULT 0, max_retries INTEGER DEFAULT 3,
  gmt_create TIMESTAMP, gmt_modified TIMESTAMP);

CREATE TABLE agent_knowledge_workspace (
  project_path TEXT NOT NULL, branch VARCHAR(256) NOT NULL, language VARCHAR(64),
  gmt_create TIMESTAMP, gmt_modified TIMESTAMP, PRIMARY KEY (project_path, branch));

CREATE INDEX idx_knowledge_task_project_status   ON agent_knowledge_task (project_path, status);
CREATE INDEX idx_knowledge_task_status           ON agent_knowledge_task (status);
CREATE INDEX idx_knowledge_task_workspace_status ON agent_knowledge_task (workspace_path, status);
CREATE INDEX idx_task_kind_workspace             ON agent_knowledge_task (kind, workspace_path);
CREATE INDEX idx_task_parent                     ON agent_knowledge_task (parent_task_id);
CREATE INDEX idx_knowledge_upload_task_id        ON agent_knowledge_upload (task_id);
CREATE INDEX idx_knowledge_upload_workspace      ON agent_knowledge_upload (workspace_path);
```

All three tables are **empty** on this machine (`0 rows`): a wiki was never completed, which
matches the credit-gated UI. The schema still proves the model: one task row per
(workspace, branch, language) generation, a parent/child task tree, local+server commit
tracking, and an upload queue with retries.

## 6. Export / import contract

From the i18n table in `agents-window.desktop.main.js`:

| Key | Value |
| --- | --- |
| `quest.knowledge.generate.autoExportDesc` | 开启后，生成的 RepoWiki 将自动导出至项目的 .qoder/repowiki 目录下 |
| `quest.knowledge.action.exportToFolderHint` | `.qoder/repowiki` |
| `quest.knowledge.action.importFromHint` | `.qoder/repowiki` |
| `repoWiki.sync.exportToLocal` | 导出到 `.qoder/repowiki` |
| `repoWiki.sync.importToWiki` | 从 `.qoder/repowiki` 导入 |
| `quest.knowledge.action.language` / `autoUpdate` / `citation` | language switch, auto-update, agent-citable |

So `.qoder/repowiki` is the **sync directory** (export *and* import), separate from the
per-project cache snapshot under `SharedClientCache`.

## 7. UI evidence (tab + per-document lifecycle)

- `quest.knowledge.tab.repoWiki` — the Repo Wiki is a tab in the knowledge area.
- `quest.knowledge.repoWiki.searchPlaceholder`, `…filter.repository`,
  `…filter.selectRepository`, `…infoDescription`, `…learnMore`, `…repoWikiConfig`.
- Per-document states: `repoWiki.description.completed` / `documentGenerating` /
  `documentFailed` / `directoryGenerating` / `directoryFailed` — i.e. status is tracked per
  directory and per document, not just per repository.
- Actions: `repoWiki.button.pause` / `resume` / `retry` / `update` / `regenerate`,
  `quest.knowledge.action.pullFromServer` / `syncTeamKnowledge`.

## 8. What CodeFusion ships today vs this evidence

| Capability | Qoder (observed) | CodeFusion today | Gap |
| --- | --- | --- | --- |
| Cache key | `<project>#wiki#<branch>#wiki#<lang>` | `.cf/repowiki/<lang>/` | key format differs; branch/language not in a key |
| Ingestion caps | 250 k files / 100 k indexed / depth 100 / 10 k per dir / simhash | 8 000 files / depth 14 / 60 excerpts | caps far smaller |
| Ignore file | `.qoderignore` | `.gitignore` only | missing |
| Snapshot | `metadata.json` + `mtree.json` + `files/**` | `wiki.json` + `<slug>.md` | different artifact set |
| Page status | per directory/document (`completed|generating|failed`) | per manifest (`status`) | missing per-page status |
| Sync dir | `.qoder/repowiki` (export + import) | none | missing |
| Generation | server task + credits | local service, no gate (by design) | intentional difference |
| Pause/resume/retry | yes | cancel only | missing |

## 9. Bounds of this evidence

- Observed: file contents listed above, DB schema, cache tree, string tables.
- Not observed: the server-side prompt(s) that produce wiki prose, and the exported
  `.qoder/repowiki` page format — no completed generation exists on this machine, so no
  export sample could be inspected. Any claim about Qoder's page-level Markdown layout
  would be inference, not evidence.
- The `Qoder IDE` install was identified but not separately analysed; both ship the same
  `resources/app` layout.

Reproduction: `node scripts/re/qoder-repo-wiki-evidence.mjs <qoder-app-dir> repowiki
".qoder/repowiki" knowledge.db _index.yaml` and
`node scripts/re/qoder-knowledge-db-dump.mjs` (both read-only; the DB is copied to
`.plan/re-tmp/qoder-repowiki/` first).
