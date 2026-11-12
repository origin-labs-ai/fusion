# Verification: mux/host SSE fan-out has no backpressure

Task type: adversarial verification (refute-or-confirm). Read-only; no fix applied in this step.

## Verdict: CONFIRMED (not refuted) — severity medium stands

### Evidence re-checked in source

- `packages/host/apiproxy/src/api-proxy.ts:355-386` — `FrameQueue` is exactly as quoted:
  `push()` unconditionally `this.buffer.push(item)` (only the `done` flag short-circuits).
  No cap, no eviction, no byte accounting. `iterate()` is the sole drain point and ends only
  on signal abort.
- `packages/host/apiproxy/src/fetch/handler.ts:203-236` — `sseResponse` does
  `controller.enqueue(...)` per frame inside `for await (const narrow of frames)`, with no
  `desiredSize` check and no `pull`/`cancel` hooks on `new ReadableStream({ start })`.
  The default count strategy's `highWaterMark: 0` does not bound the queue; `enqueue` never
  blocks. Claim correct.
- `packages/host/apiproxy/src/api-proxy.ts:3328-3429` — `events.mux()` registers
  `ctx.on('session/event', ...)` per connected client and pushes
  `frame({ type: 'session/event', sessionId, event, ...view })` — full events including
  tool results and assistant messages — for **every** session into that client's queue.
  Impact claim is real.

### Mitigation search — nothing bounds it

- `desiredSize` appears exactly once in the whole `packages/` tree:
  `session-export.ts:291` (inside `ResponseCapacityGate.wait`).
- `bufferedAmount` appears **zero** times in the repo.
- `session-export.ts:275,278-308,406-456` — the ZIP export path implements exactly the
  missing control (`ResponseCapacityGate` + `highWaterMark: RESPONSE_HIGH_WATER_MARK_BYTES`
  = 64 KiB, `size: chunk => chunk.byteLength`), and the package README documents that
  bounded-memory posture. The live stream carries far more data and has none.
- No idle timeout, no max-mux-connections limit, no disconnect-on-lag on either stream.

### Precision correction (does not refute)

The cited `sseResponse` path is **not** the production network data plane:
`packages/client/connection/src/index.ts:150-155` answers `426 Upgrade Required` for GET
`/api/events.mux|host`; the browser carrier is `WebSocketDownlinks`
(`2026-08-04-websocket-downlink-carrier.md`, connection README). `sseResponse` serves only
the isomorphic in-process carrier.

But this **strengthens** rather than refutes the finding: `FrameQueue` is the shared
accumulator, and the WebSocket path is unbounded in the same place.
`websocket-downlink.ts:124` does `for await (const frame of frames) await send(...)` with no
`bufferedAmount` pacing; in the installed `ws` (`node_modules/ws/lib/sender.js:566-570`) the
send callback is `_socket.write(data, cb)` — local write-flush completion, **not** client
consumption. A zero-window peer fills the kernel socket buffer, the pump then blocks, and
`FrameQueue.buffer` grows without bound from that point on.

### Why not higher severity

`/api` is fenced to loopback / declared `trustedHosts` (no anonymous remote vector), the
growth rate is bounded by producer throughput, and the socket's close/error does eventually
free the buffer. Host memory exhaustion, not data loss or RCE → medium.

### Suggested fix shape (for the follow-up fix pass)

Bound `FrameQueue` (high-water cap + disconnect or drop policy), and/or add consumer-capacity
pacing in `sseResponse` (mirror `ResponseCapacityGate`) and `bufferedAmount` pacing in the
WebSocket pump.
