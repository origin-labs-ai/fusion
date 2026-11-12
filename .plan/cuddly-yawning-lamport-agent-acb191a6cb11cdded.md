# Verification: findProjectRoot treats fs provider failure as "no marker"

## Claim
`existsAsMarker` collapses every provider exception into `false`, so a transient `ctx.fs` failure on the real root marker makes `findProjectRoot` continue upward past the intended project boundary and return a higher ancestor (or the filesystem root). The ancestor's `AGENTS.md` then loads into session context.

## Verdict: NOT REFUTED — confirmed in current code

### Evidence chain (all verified)

1. **The claimed code is real and current** — `packages/context/agent-instructions/src/files.ts:145-166`:
   ```ts
   async function existsAsMarker(path, fileSystem?, signal?): Promise<boolean> {
     if (fileSystem !== undefined) {
       try {
         const target = await fileSystem.resolve(path, signalOptions(signal))
         return await fileSystem.stat(target, signal) !== undefined
       } catch {
         signal?.throwIfAborted()
         // TODO(root-marker-unavailable): preserve provider failure separately from
         // absence and stop discovery; continuing upward can cross into an ancestor project.
         return false
       }
     }
     ...
   }
   ```
   The catch returns `false` — indistinguishable from "marker absent".

2. **The call site uses the boolean directly** — `findProjectRoot` at line 185:
   ```ts
   if (await existsAsMarker(join(current, marker), fileSystem, signal)) return current
   ```
   `false` → walk continues to parent. No retry, no fallback, no validation.

3. **The tri-state distinction exists everywhere else in the same file**:
   - `fsStatFile` / `nodeStatFile` return `StatFileProbe = { kind: 'present' | 'absent' | 'unavailable' }`.
   - `probeScopeInstruction` returns `ScopeInstructionProbe` with the same three kinds.
   - Comment at line 473-474: "A non-file target (missing, or a link to a directory) is a confirmed absence; only a provider exception is reported as unavailable."
   - `allExistingInstructionFiles` explicitly handles `unavailable` differently from `absent` in comment (line 254): "a transient provider failure skips only that candidate so the remaining independent candidates still load."

   `existsAsMarker` is the single place that throws this distinction away.

4. **No upstream mitigation**:
   - Callers (`discoverInstructionFiles` line 300, `index.ts:125`, `state.ts:268`) take the returned root string with no validation or error handling.
   - `existsAsMarker` is the only helper that takes a `FileSystem` and swallows its errors; `statFile`/`probeScopeInstruction` both propagate `unavailable`.
   - The `FileSystem` interface (`packages/fs/fs/src/types.ts`) defines `FsError` codes `FS_IO_ERROR`, `FS_PERMISSION_DENIED`, `FS_SANDBOX_DENIED` — typed errors the provider throws on real failures.
   - The local backend (`fs-local/src/index.ts`) `stat` calls `probe(target.targetKey)` which uses `fs.stat` — EACCES/EPERM on a parent directory or the target itself will throw.
   - The `FileSystem` type docs explicitly mention "a remote backend might use a workspace URI or file id" — transient network failures are a designed-for scenario.

5. **Tests confirm the pattern but don't cover this case**:
   - `RecordingFileSystem` in `agent-instructions.spec.ts` has `throwOnStat` to simulate stat failures.
   - Test "preserves a visible baseline when its source is unavailable during resume" uses `throwOnStat` — but on `AGENTS.md` (which goes through tri-state `statFile`), not on the `.git` marker.
   - Test "treats a .git file as a project root marker and does not search above it" (line 383) verifies the walk stops at `.git` — but only when `stat` succeeds.
   - No test covers "marker stat throws → walk continues upward".

6. **The in-code TODO explicitly acknowledges this as a hazard** (line 152-153):
   > "preserve provider failure separately from absence and stop discovery; continuing upward can cross into an ancestor project."

   The code authors flagged the current behavior as wrong, not intended.

### Impact assessment

- **Trigger**: A transient `ctx.fs` failure (I/O error, permission error, network error on a remote backend) while stat-ing the real project root marker.
- **Consequence**: `findProjectRoot` walks past the intended boundary and returns an ancestor. That ancestor's `AGENTS.md`/`CLAUDE.md` loads into the session context as if it belonged to this project — silent context contamination.
- **Silent**: No error surfaced; the session just sees the wrong instructions.
- **Narrow but real**: The local backend's `stat` returns `undefined` for missing files (doesn't throw), so the trigger requires an actual FS fault. But the `FileSystem` interface is explicitly designed for remote backends where transient failures are expected.

### Severity

**Medium** is appropriate. It's not a crash or data loss, and it requires an error condition to trigger. But the consequence is silent wrong-context injection, the codebase clearly cares about this distinction elsewhere (tri-state probes), and the in-code TODO already plans the fix. A competent maintainer would agree this is a real actionable gap.

## Conclusion

**refuted: false** — the finding is real, in current code, not mitigated elsewhere, and acknowledged by the in-code TODO. Severity medium stands.
