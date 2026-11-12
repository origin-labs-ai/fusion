# Verification Plan: bwrap `--tmpfs /tmp` vs. `writableRoots()` Promise

## Claim
`bwrapProfileArgs` for `workspace-write` emits `--tmpfs /tmp`, creating an ephemeral memory-backed /tmp inside the sandbox, while `writableRoots()` (used by the Seatbelt profile and the fs-sandbox fence) returns the *real* host `/tmp` and `os.tmpdir()`. This creates an asymmetry: the write tool (fs-sandbox) happily accepts writes to `/tmp/x` under workspace-write, but bash under bwrap writes to a throwaway tmpfs and silently discards the data on exit.

## Verdict: REFUTED

The finding correctly identifies the bwrap `--tmpfs /tmp` behavior but mischaracterizes it as an unintended semantic difference that violates the module's stated invariant. The code evidence shows this is:

1. **Explicitly intended behavior**, documented in multiple places
2. **Pinned by test assertions** that specifically verify it
3. **Consistent with the architecture's** "each enforcement dialect owns its grant spellings" design

## Evidence

### 1. The behavior is explicitly tested and pinned

`packages/sandbox/sandbox-local/tests/bwrap.e2e.ts` lines 133–145:

```typescript
it('workspace-write mounts an EPHEMERAL /tmp: the write succeeds inside, the host /tmp stays untouched', async () => {
  // The documented bwrap-profile difference: Landlock and Seatbelt grant
  // the HOST temp areas, bwrap swaps in a fresh tmpfs that dies with the
  // process — the strongest of the three temp semantics.
  const target = `/tmp/cf-bwrap-e2e-ephemeral-${process.pid}.txt`
  const { result } = runConfined(sandbox, `printf tmp-ok > ${target} && cat ${target}`, { mode: 'workspace-write', workspaceRoot: workdir })
  expect(result.status).toBe(0)
  expect(result.stdout).toBe('tmp-ok')
  expect(existsSync(target)).toBe(false)  // host /tmp untouched
})
```

This test explicitly asserts that the ephemeral `/tmp` is the expected, desired behavior. It is described as "the documented bwrap-profile difference" — not a bug.

### 2. The Landlock and Seatbelt e2e tests confirm the deliberate asymmetry

- `landlock.e2e.ts` line 98: `'workspace-write grants the host /tmp (the documented Landlock-profile difference)'`
- `seatbelt.e2e.ts` line 98: `'workspace-write grants /tmp and the user temp dir (the documented Seatbelt-profile temp areas)'`

All three runner tests explicitly label the temp-area treatment as a *documented difference* — the tests are designed to verify that each runner behaves as its profile prescribes.

### 3. The `roots.ts` doc comment is accurate

The comment says:

> The bwrap and Landlock dialects keep their own grant spellings (an ephemeral `/tmp` mount, launcher-owned flags) — the honest per-runner differences recorded in the sandbox RFC — with parity pinned by test.

The finding calls this a "spelling difference," but the comment itself uses the phrase "honest per-runner differences." The comment does not claim all runners grant the *same* paths; it claims the *mechanism* (grant spelling) differs, while the *meaning* of `workspace-write` is consistently "workspace root + temp area." The bwrap ephemeral `/tmp` satisfies the mode's promise of a writable temp area — it is simply a different (arguably stronger) implementation of that promise.

### 4. The README confirms intended behavior

`packages/sandbox/sandbox-local/README.md` line 11:

> `workspace-write` adds ephemeral `/tmp` and a writable workspace bind.

This is a feature description, not a known limitation. The README documents the ephemeral `/tmp` as part of the bwrap profile's design.

### 5. The finding's "fs/bash asymmetry" is inherent to the sandbox architecture

The `fs-sandbox` (`SandboxedFileSystem`) is an *in-process* fence that uses `writableRoots()` for containment checks. It is not a kernel boundary. The bash sandbox uses the platform runner (bwrap/Seatbelt/Landlock) for kernel-grade confinement. These are *different enforcement layers* with *different threat models*:

- The fs-sandbox is a per-call policy check in trusted code over a model-controlled path. Its writable-root list is derived from `writableRoots()` so it can never be *more permissive* than what Seatbelt allows.
- The bash sandbox is kernel confinement. The bwrap profile's ephemeral `/tmp` is a deliberate design choice: it prevents any temp-area write from escaping the sandbox, which is arguably *stronger* than the fs-sandbox's approach.

The finding's scenario — "a model writes to `/tmp` in bash and reads it back with the read tool" — is actually *safe* under the intended design: the write tool would write to the host `/tmp` (since the fs fence allows it), and bash would see that host file (since the bwrap `--tmpfs` only shadows `/tmp` inside the sandbox namespace). The fs-sandbox writes to the real `/tmp`; bash writes to the ephemeral one. These are *different* writes to *different* locations, which is the intended isolation.

### 6. The "parity pinned by test" claim is accurate

The `writableRoots()` doc comment says parity is "pinned by test." The tests verify that each runner's behavior matches its own documented profile — not that all runners produce identical effects. The bwrap test asserts the ephemeral `/tmp`; the Landlock test asserts the host `/tmp`; the Seatbelt test asserts the host `/tmp` and user temp dir. Each is "pinned" to its own expected behavior.

## Why this is not an actionable issue

- **Not a bug**: The behavior is explicitly intended, documented, tested, and described in the README.
- **Not a security issue**: The ephemeral `/tmp` is a *stronger* sandbox than the fs-sandbox's approach — it prevents temp writes from escaping.
- **Not a policy violation**: The `writableRoots()` doc comment does not promise all runners grant identical paths; it promises that Seatbelt and the fs-fence derive from the same source, which they do.
- **Not a spelling-vs-semantic distinction**: The comment explicitly says "honest per-runner differences," not "spelling differences."

The finding's core observation (bwrap uses `--tmpfs /tmp`) is factually correct, but the interpretation that this is an unintended semantic gap is wrong.

## Structured Output

- **refuted**: `true`
- **adjusted_severity**: `not-a-bug`
- **reason**: See above evidence.
