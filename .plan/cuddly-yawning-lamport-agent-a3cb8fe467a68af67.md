# Verify: "spill artifacts never deleted — unbounded temp dir growth"

## Verdict: REFUTED (intended, documented deferred behavior — not a bug)

## What I checked

1. `packages/spill/spill-local/src/store.ts` — `saveTextFile` indeed never deletes;
   `privateRoot()` = `mkdtempSync(join(tmpdir(),'cf-spill-'))`, never removed. The
   reviewer's factual claim is accurate.
2. Grep across `code-fusion` for unlink/rm/purge/cleanup/retention in spill code:
   nothing deletes spill files (only test teardown `rmSync`).
3. Docs — and here the claim collapses:
   - `packages/spill/spill-local/README.md:31` — "Known Limitations and Deferred
     Work: Local spill files persist until external cleanup — the backend has no
     session-lifecycle deletion or age-based retention policy, because persisted,
     resumed, and forked sessions may still reference a path."
   - `.agents/notes/implemented/architecture/2026-07-08-tool-output-spill-files.md:56`
     — "A retention-period cleanup may expire old locators with other old session
     artifacts; the spill seam does not define a per-session cleanup policy."
   - Same note, Deferred section (line 161) — "Cleanup and retention policy for
     old spill files, likely tied to session cleanup."
   - `packages/spill/spill/src/index.ts` — the seam explicitly owns NO retention
     policy (that is deliberate separation of concerns, not an oversight).
   - `packages/spill/spill-policy/src/index.ts:182` — orphan spill file on
     cap-exceeded fallback is called out as "harmless… cleanup is deferred."

## Why refuted

- The reviewer's own evidence (`spill/src/index.ts` docs) is the seam explicitly
  disclaiming retention; the reviewer misreads that disclaimer as evidence of an
  ownership gap, while the architecture note's Deferred section and the
  spill-local README's Known Limitations section both name this exact limitation.
- Rationale is stated and sound: sessions can be persisted/resumed/forked and
  still reference spilled locators from the seeded log, so session-lifecycle
  deletion would break resume. "External cleanup" (e.g. OS tmpdir retention or a
  future session-cleanup pass) is the designated mechanism.
- Impact as claimed ("every host boot leaks a new world-adjacent temp tree") is
  also overstated: the tree is 0700, created lazily only when a spill actually
  happens, and lives in tmpdir which most OSes already reclaim.

A maintainer would close this as "documented deferred limitation," not file a bug.
Severity: not-a-bug.
