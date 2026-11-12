# fusion-full-review — Retry Queue (all failed / unfinished agents)

Created: 2026-10-22 (session restart #3). Run ID: `wf_ce1d51d7-91d`

## Journal state at queue creation
- started: 400 · result: 238 · failed: 121
- 15/15 finder clusters have committed findings (255 findings) — cf-infra & cf-misc results EXIST in the journal (their last run instance failed; earlier instances succeeded)
- 25 verify labels last-event = failed (their votes never landed)
- 2 synthesize labels never succeeded (completeness-critic, final-report)
- Raw machine list: `review-tracking/retry_queue.json`

## A. Failed verify labels (25) — alternative-lens re-verification
Each needs an INDEPENDENT verifier with a DIFFERENT lens than the original run, so the
same failure mode (or the same blind spot) does not repeat. 15 of these have no title
resolvable from the journal (the finder result for their cluster was itself one of the
rolled-back runs) — for those, the alternative agent re-derives the finding from the
cluster paths and then verifies it.

### P1 · verify:`--host 0.0.0.0` is rejected only as
- finding: `--host 0.0.0.0` is rejected only as a CLI string literal; the webserver still accepts an all-interfaces bind and then auto-trusts every LAN IPv4 (high) — C:/Users/thaku/Workspaces/fusion/code/packages/bundle/web-app/src/startup.ts:74 [cluster cf-web]
- detail: The safety rail is a single string comparison inside the commander action of `cf --profile web`. The `WebServer` service still declares `0.0.0.0` as a legal config value (`packages/host/webserver/src/index.ts:61,75`), so any other composition path — a `cordis.yml`/`cordis.patch.yml` overlay, an embe

### P2 · verify:Sourcemaps with full `sourcesContent
- finding: Sourcemaps with full `sourcesContent` are emitted into the dist that the host serves (medium) — C:/Users/thaku/Workspaces/fusion/code/apps/web/vite.config.ts:113 [cluster cf-web]
- detail: `sourcemap: true` writes `.js.map` files beside every chunk in `apps/web/dist`, and `frontend-static` deliberately MIME-maps `.map` to `application/json`, so they are served over the same `/` origin as the app. `package.json`'s `files: ["dist", "!dist/**/*.map"]` and `.npmignore`'s `*.map` only stri

### P2? · verify:Model-facing web_fetch has no SSRF/p
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:API gateway has no authentication; t
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:BYOK exportConfig redaction flag is
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:node-pty patch makes the spawn-helpe
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Credentials provider silently trusts
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:WDAC policy generator writes a cert
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Lint gate disables oxlint's entire c
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:vitest.e2e.config.ts is deleted from
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:packages/cf (23 TS files) is outside
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Coverage exemption list removes most
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Repo-root config files are neither l
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Pre-commit lint silently drops every
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Web lane loads root .env uncondition
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:tsdown.config.ts imports from build
- finding: (title not resolvable from journal — cluster re-derivation required)

### P2? · verify:Real-API e2e runs on every trusted P
- finding: (title not resolvable from journal — cluster re-derivation required)

### P1 · verify:redactSecrets fails OPEN: a secret r
- finding: redactSecrets fails OPEN: a secret reachable only through a union/intersection/transform schema node is returned verbatim on the wire (high) — C:/Users/thaku/Workspaces/fusion/code/packages/settings/settings/src/redact.ts:86 [cluster cf-infra]
- detail: The redaction walker only knows how to descend `object`, `dict` and `array`. Every other schemastery node type — `union`, `intersect`, `intercept`, `transform`, `optional`, `nullable` — falls into the `default` arm, which returns the value untouched and pushes nothing into `secrets`. describe({redac

### P2 · verify:The JSON settings path leaks documen
- finding: The JSON settings path leaks document content into logs and boot errors, contradicting the secret-safety rule the YAML branch implements (medium) — C:/Users/thaku/Workspaces/fusion/code/packages/settings/settings-file/src/index.ts:289 [cluster cf-infra]
- detail: The YAML branch of parse() deliberately never surfaces the parser's message: the comment at L275-277 states that `error.message` is unused "because the parser quotes the offending source line and a settings document can hold a `role('secret')` value", and only `error.code` + line/col are emitted. Th

### P1 · verify:undefine and stop do not cancel or a
- finding: undefine and stop do not cancel or await an in-flight host-half activation, orphaning a live fiber with registered tools (high) — C:/Users/thaku/Workspaces/fusion/code/packages/extensions/cordis-host-runner/src/index.ts:210 [cluster cf-misc]
- detail: activate() at line 810 registers its promise in this.starting and then awaits startFresh(), which itself awaits evaluateHostCode and startHostHalf (group.await plus fiber.await) before assigning plugin.run. Neither undefine (line 210) nor stop (line 456) touches this.starting: undefine computes wasR

### P1 · verify:Runs left in starting-host or client
- finding: Runs left in starting-host or client-pending are never reconciled, permanently wedging the plugin in transition-in-flight (high) — C:/Users/thaku/Workspaces/fusion/code/packages/extensions/cordis-client-runner/src/client/orchestrator.ts:182 [cluster cf-misc]
- detail: reconcileApprovals only surfaces a Host run whose latest attempt is awaiting-approval, starting-host, or client-pending AND whose package row is still resolvable. A run parked in starting-host or client-pending has no page-side plan and no approval answer, so nothing ever calls resolveRequestRun for

### P1 · verify:The sandbox ctx and tool facade is e
- finding: The sandbox ctx and tool facade is escapable through any host-realm function, so the guard stated invariants are unenforceable (high) — C:/Users/thaku/Workspaces/fusion/code/packages/extensions/cordis-host-runner/src/guard.ts:685 [cluster cf-misc]
- detail: guardedService at line 685 and the ctx facade at line 753 wrap host objects in host-realm Proxies and forward host functions wrapped in host-realm arrow functions. From inside the VM sandbox, any of those values yields the host realm: calling .constructor.constructor on ctx.on, or on ctx.tools, retu

### P2 · verify:lastTurn copies and scans the entire
- finding: lastTurn copies and scans the entire session event log on every tool call, before any hook is known to match (medium) — C:/Users/thaku/Workspaces/fusion/code/packages/hooks/hooks-claude-code/src/index.ts:239 [cluster cf-misc]
- detail: lastTurn does an array spread of agent.session.events plus findLast over every session event, including every tool-result blob and message body. Both bridges call it eagerly at the top of the tools/pre-execute and tools/post-execute listeners, so it runs once per tool call per bridge regardless of w

### P2 · verify:evaluateHostCode misclassifies any r
- finding: evaluateHostCode misclassifies any runtime-thrown sandbox SyntaxError as a parse failure and returns misleading bracket-balance advice (medium) — C:/Users/thaku/Workspaces/fusion/code/packages/extensions/cordis-host-runner/src/sandbox.ts:254 [cluster cf-misc]
- detail: runInContext of an async IIFE returns a promise, so a SyntaxError thrown inside the package's own running code (a direct throw new SyntaxError, a JSON.parse or new Function the package invokes at runtime, or any host-realm intrinsic that rejects with one) rejects the awaited promise and is then caug

### P2 · verify:TeamJournal.state re-validates and r
- finding: TeamJournal.state re-validates and re-folds the entire Lead session log on every read (medium) — C:/Users/thaku/Workspaces/fusion/code/packages/experimental/agent-team/src/journal.ts:30 [cluster cf-misc]
- detail: state() calls foldTeam over the whole Lead session log, which walks every event in that log, not just the four team event types, and runs a zod parse on each team-owned event. There is no incremental cache or observedSeq, in contrast to GoalService.sync in packages/goal/goal/src/index.ts lines 437-4

## B. Failed finder labels (2) — results exist; re-run for a fresh independent pass
- find:cf-infra
- find:cf-misc

## C. Failed synthesize labels (2) — never succeeded
- completeness-critic
- final-report

## D. Execution plan for this queue
1. Resume run `wf_ce1d51d7-91d` (scriptPath workflows/scripts/fusion-full-review-wf_ce1d51d7-91d.js)
   → completed agents replay from cache; the 25 failed verify labels + critic + final-report re-launch.
2. Parallel: `fusion-review-alternatives` workflow (new) — independent alternative-lens
   verification of the 25 failed labels with a DIFFERENT approach per lens, so the
   result is not a repeat of the same failure; plus re-derivation for the 15
   unresolved titles from the cluster paths.
3. Re-derive the final VERDICT from: 238 journal results + alternative verdicts.
4. Write the final report to `review-tracking/FINAL_REVIEW.md` + `review-tracking/VERDICT.json`.
5. THEN execute `review-then-fix`: every confirmed finding fixed (Operation Clean
   execution plan in `.claude/plans/cuddly-yawning-lamport.md`).
