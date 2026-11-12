# Verification: PolicyAgentTreeManager.terminateAgent capacity-leak claim

## Verdict: REFUTED (not-a-bug as framed)

## What's mechanically true in the code
- `terminateAgent` (god-runtime.ts:3819-3830) only sets `status='terminated'` and clears
  `childrenIds`; it never calls `agentTree.delete(...)`.
- `spawnChildAgent` (3787) gates on raw `this.agentTree.size >= maxTotalAgents`.

## Why the claimed impact is not real
1. **No idle sweeper exists.** `cleanupIdleAgents` has exactly two references: its
   definition (3875) and one call from `GodRuntime.shutdown()` (6054). shutdown() is a
   terminal path (SHUTTING_DOWN -> IDLE, `initialized=false`). No setInterval/timer
   invokes it. The claim that an "idle sweeper manufactures spawn/terminate cycles on
   its own" is false.
2. **spawnChildAgent is dead code.** Grep across the entire code-fusion tree finds
   spawnChildAgent at its definition only — zero call sites. No spawn/terminate cycle
   ever occurs, so the 20-slot wedge is unreachable. GodRuntime's real participant flow
   uses a separate `activeAgents: ActiveAgent[]` + DiscussionCoordinator, not the tree.
3. **Type mismatch confirms scaffolding.** `spawnPolicy: SpawnPolicy` is typed from
   ../types (types.ts:940) whose fields are maxAgents/maxTreeDepth/... — none of
   maxDepth/maxChildrenPerNode/maxTotalAgents/requireParentApproval/autoTerminateIdleMs
   exist on the declared type. Unintegrated, unfinished code.

## Secondary claim (duplicate childConfig.id overwrite)
Mechanically true if spawnChildAgent were called with a dup id, but again the method is
never invoked — theoretical only.

## Adjusted severity: not-a-bug (latent hygiene note at most)
