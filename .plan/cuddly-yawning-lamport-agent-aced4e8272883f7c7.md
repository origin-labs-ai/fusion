# Verification: "Sandbox provider caches 'unavailable' permanently"

**Verdict: REFUTED — intended, documented, tested behavior. not-a-bug.**

## Claim under review

`LocalSandboxProvider.selectRunner` memoizes `'unavailable'` via `??=`, so probes never re-run after a transient failure. Severity claimed: medium (availability / fail-closed liveness).

## What the code actually does (evidence confirmed)

`C:/Users/thaku/Workspaces/fusion/code-fusion/packages/sandbox/sandbox-local/src/index.ts`

- L265: `private selectedRunner: SelectedRunner | 'unavailable' | undefined`
- L492-496: `this.selectedRunner ??= this.chainVerdict()` then `if (this.selectedRunner === 'unavailable') throw new SandboxUnavailableError(mode)`.
- L499-510: `chainVerdict()` walks the platform chain, probes each candidate, returns the literal `'unavailable'` when none passes.

The mechanical claim is accurate: `'unavailable'` is a truthy non-nullish string, so `??=` never re-evaluates after a failure verdict.

## Why it is not a bug

1. **Explicitly documented as intended behavior.**
   - `packages/sandbox/sandbox-local/README.md` L39, under "Known Limitations and Deferred Work": "**Runner selection is cached for the provider lifetime** — installing, removing, or repairing a runner requires reloading the plugin before selection changes." The documented remedy is plugin reload.
   - `docs/subsystems/sandbox.md` L61: "`cf-sandbox-local` selects one platform runner per provider lifetime and caches the verdict."
   - Same doc L188 (FAQ, present-but-unusable bwrap): "the verdict is cached for the provider's lifetime."

2. **Explicitly pinned by a test.**
   - `packages/sandbox/sandbox-local/tests/local.spec.ts` L235-243: `it('the unavailable verdict is cached too, and the error is structured')` asserts `probeBwrap` and `probeLandlock` are each called exactly once even after a second `confine()`. The behavior the reviewer calls a bug is a guarded contract.

3. **Design rationale is deliberate.**
   - `docs/subsystems/sandbox.md` L134: sole-candidate probing was rejected because "probe cost taxes the first confined command of every session (prohibitive for heavy future backends)." Caching the verdict (success and failure) is the same policy: one chain walk per provider lifetime, then a deterministic answer. Re-probing only on failure would make permanently-unavailable backends pay probe cost on every call and would make the selection answer flappy.

4. **Reviewer's "inconsistent with that intent" framing is wrong.** The design intent is "one chain walk per provider lifetime, cached" — not "cache only success." The failure verdict is a verdict, and the test name says so verbatim.

5. **Transient-failure scenario is speculative.** The probes are bounded (5s default), functional (spawn + exit 0), and the provider is a server-lifetime singleton. The documented operational remedy for a genuinely changed backend is plugin reload — which is the intended recovery path, not a bug.

## Structured output

- refuted: true
- adjusted_severity: not-a-bug
