# Fusion — Full Alternative to the Transformer

> **Status:** FINAL — audited, corrected, and research-complete.
> The user speaks casual Hinglish; this plan is in English per their explicit instruction.
> This file is the **single source of truth** for the sprint — memory holds only the Hinglish preference (§13).
>
> **Audit:** §16 records the adversarial review (4 independent dimensions). Two verdicts were refuted and produced material corrections — the sweep inventory (§2.1) and the internal consistency (§16). The plan now names **21 model-layer sites plus the KAT layer**, and every remaining gap is listed rather than hidden.
> **Research:** §5c is the consolidated solo research (arXiv, verified by fetch). **Workflows were not used** — the user directed that everything be done by hand; the one workflow launched for research returned 5/5 failures on free-tier caps and contributed nothing. What is still unknown is listed in §5c.5 rather than papered over.
> **Out of scope by the user's instruction:** ECC consolidation of the three parallel continual-learning stacks (§4.8a) — do not merge them.


> ---
> **OPERATOR REMINDER (2026-11-12 - read this whenever you implement anything):**
>
> 1. **MAIN GOAL = the ENTIRE Fusion Superproject.** Every domain, every seat, every track -
>    all of it complete. This project is NOT just quantization; quantization is one track of it.
> 2. **SIDE GOAL = achieve the MAXIMUM at EXACT 1.0 BPW - not 1.5 BPW.** The implemented 1.5 BPW
>    path is a *stepping stone*; the real target is **1.0 BPW**. Older sections that say "1.5 BPW"
>    stay true as implemented-state facts - the GOAL line is 1.0.
> 3. **FP + INT research note (operator, same-day research):** BOTH quantization format families -
>    FP (floating point: FP8/FP4/E5M2 style) and INT (integer: INT4/INT8/binary/ternary) contain
>    actionable work. Research both; do not drop either.
> 4. **FACT (2026-11-12 audit):** Loop Quantization has NEVER been implemented for any model,
>    anywhere. Track B will be the world's first implementation.
> 5. **Current situation (exact):** Loop Quant Track B open - Mix Quant partial (MX family
>    quarantined) - NCM Appendix F.1.1/I read pending - EAIN design open. We WILL implement and
>    complete all of it - grind method (`.plan/telemetry/TODO-TREE.md`), dashboard after every
>    step (`.plan/telemetry/DASHBOARD.md`).
---

## Context

### The problem

Every frontier model today is a **transformer**, and the whole game inside it is **attention**: every word compared against every other word. Two failure modes follow, and both are **architecture-level, not bugs**:

1. **Context rot** — the bigger the context window, the more the model degrades. Chroma (2025) tested 18 top models with an identical Q&A and only growing surrounding text; accuracy fell as text grew. Anthropic researchers retested in 2026: only slightly better.
2. **Lost in the Middle** — Stanford / U. Washington: information at the top or bottom of a large prompt is caught; the same information in the **middle** drops accuracy by up to **30%**.

Neither is fixable by an update. **As long as it is a transformer, the problem exists.** Labs stopped trying to fix attention and *flipped the problem* into "context engineering" — RAG, chunking, recursive language models. **None solve it; they only manage it.** RAG can actively make things worse: wrong-chunk retrieval, **distractor accumulation** (10 chunks pulled, 1 has the answer, the rest is noise that dilutes attention), semantic fragmentation, hallucination, wasted tokens.

The "10 million token" marketing is also misleading. Needle-in-a-haystack requires no reasoning at all. In practice a model behaves normally to roughly **2 lakh (200k)** of a claimed **10 lakh (1M)** window.

### The intended outcome

**Fusion** is a complete alternative to the transformer — a new attention core plus the harness that makes a *small, bad* model behave like a large one on long-horizon agentic tasks.

The user's definition of the system:

> **"It predicts next token, but — according to the context, and never forgets anything."**

Plus: it takes decisions **according to the context**, and it **learns from its environment**.

### The two anchor facts

- **Astra (GPT-6)** scored **99.9% on ARC-AGI-3** — but the same model in a **provider-neutral setup scored 62.7%**. The capability is not in the weights; it lives in the **harness and the adapter**. On the ARC-AGI-3 community leaderboard the pattern holds across vendors: `*-provider-adapter` entries hit **99.99%** while the identical model without the adapter sits at **3–35%**. (An earlier claim of "~66-67% without" was thought wrong, then the transcript's **62.7%** reconciled it — the user was right.)
- **Yann LeCun: LLMs are not the future; world models are.** A full world-model implementation **already exists** in this codebase (§7C).

### Hard technical goal

> Use `code-fusion` so that a **bad dense DeepSeek V4.1 Flash** scores **90%+ on Terminal-Bench-4.0-style benchmarks**.

---

## 1. Naming — must appear in docs (all accepted spellings)

### The equation

```
Fusion  =  CodeFusion  +  Transformers-Fusion
```

### Accepted name variants — ALL are valid

The user gave these explicitly and said the plan must follow them:

| Component | Canonical | Also accepted (spellings / casing) |
|---|---|---|
| **The whole project** | **Fusion** | — |
| **Harness side** | **CodeFusion** | `code-fusion` |
| **Engine side** | **Transformers-Fusion** | `TransformersFusion` · `transformers-fusion` · **TransCender** · **transcender** · **Transcender** |

> Verbatim: *"Fusion = CodeFusion / code-fusion + Transformers-Fusion / transformers-fusion / TransCender / transcender / Transcender."*

**Rule for docs and code:** pick **one canonical form per surface** and use it consistently there, but recognise **every** variant above as referring to the same thing. Recommended per surface:

| Surface | Use |
|---|---|
| Directory on disk | `code/`, `transformers/` (already the case) |
| Prose / product name | **CodeFusion**, **Transformers-Fusion** |
| GitHub remote (already set) | `origin-labs-ai/code`, `origin-labs-ai/transformers` |
| The legacy / nickname for the engine | **TransCender** — *"is also / formerly known as"* |

> **Path/repo note (D-24, reaffirmed 2026-11-13, D-29):** the component folders and GitHub
> repos carry no `-fusion` suffix — `code/` (`origin-labs-ai/code`) and `transformers/`
> (`origin-labs-ai/transformers`). The product names **CodeFusion** and **Transformers-Fusion**
> are unchanged; this path rule does not rename product vocabulary.

### 1.1 Complete alias registry — ALL names the user has given

Saved verbatim so nothing is ever lost to a spelling difference again.

**Projects**

| Thing | Every alias accepted |
|---|---|
| The whole project | **Fusion** · `fusion` · FUSION |
| The harness | **CodeFusion** · `code-fusion` · `cf` · `@origin-ai/cf` |
| The engine | **Transformers-Fusion** · **TransformersFusion** · `transformers-fusion` · **TransCender** · `transcender` · **Transcender** |
| The combination | **Fusion = CodeFusion + Transformers-Fusion** |

**Models**

| Thing | Aliases |
|---|---|
| The trained model | **`sol-4-flash`** · "Sol 4 Flash" · "Sol" |
| The 27B benchmark model | **DeepSeek V4.1 Flash** · "the bad 27B dense DeepSeek V4.1 Flash" · `deepseek-v4.1-flash` |
| The ARC-AGI-3 reference model | **Astra** · **GPT-6** · ChatGPT · (once typed **"Askta"** by mistake — corrected to **Astra**) |

**Neurons**

| Thing | Aliases |
|---|---|
| The hybrid neuron | **Enhanced Artificial Intelligence Neurons** · **EAIN** · "dono capabilities waale neurons" · "best performer dono me, but digital" |

**Benchmarks**

| Benchmark | Aliases |
|---|---|
| **CS-Bench-1.0** | Common Sense Bench 1.0 · "CS matlab Common Sense Bench" |
| **CS-Bench-1.1** | Common Sense Bench 1.1 · the "top 100 / maan lo" set |
| **D&CC-Bench-1.0** | Decision and Context Check Bench 1.0 |
| **MQC-Bench-1.0** | Model Quality Check Bench 1.0 |

**Mechanisms**

| Thing | Aliases |
|---|---|
| The attention formula | `QKᵀG(GS)` · `QK^TG(GS)` · "5 letters: Q, K, T, V & G" · TransCender formula (superseded — see §2.1) |
| **The generation mechanism** | `NCM` · `Next Concept Modeling` · `Next-Concept Modeling` · arXiv `2610.14162` · "coarse-to-fine generation" · "level-by-level decoding" |
| The adapter | "the provider-adapter" · "usi adapter ka use" · Astra's adapter |
| The training target | "Terminal-Bench-4.0 jaise benchmarks" |

**Machine-readable form** (for scripts, docs, and grep):

```
fusion        = code-fusion | cf                 → CodeFusion
fusion        = transformers-fusion | transcender → Transformers-Fusion / TransCender
model.train   = sol-4-flash                      @ 1.5 BPW
model.bench   = deepseek-v4.1-flash
bench         = CS-Bench-1.0 | CS-Bench-1.1 | D&CC-Bench-1.0 | MQC-Bench-1.0
neuron        = EAIN  (Enhanced Artificial Intelligence Neurons)
formula       = softmax(QKᵀ · G(GS) / √d_k) · V
generation    = NCM (Next-Concept Modeling, arXiv 2610.14162)
generation.accel = DSpine (Adjacent Causal Injection, arXiv 2609.36173, tencent/dspine)
```

> **RESEARCH UPDATE (2026-11-09, DSpine x NCM research pass):** two additions to the
> mechanism registry, both fully read and verified live from arXiv:
> 1. **DSpine** — see new §3c below (full implementable spec).
> 2. **NCM appendix completion** — see §3b.6a below (Table 5/6 configs, K-ablation,
>    Appendix I limitations; resolves §5c.5 gap 4).

### 1.2 Roles

| | Role |
|---|---|
| `transformers-fusion` | The **engine** — the new architecture. |
| `code-fusion` | The **harness** — *"bas harness hai"*. |
| **Together** | **Fusion.** The engine comes together **only when both are ready**. |

**TransCender carries no architectural baggage** — it is a name only. The stale comment at `include/quant/transformer.h:119-122` referencing a superseded *"Cender/ formula (Phase 19-23, owner-gated)"* plan must be rewritten (§2.1); nothing else in the plan inherits from it.

---

## 2. THE SWEEP — replace every traditional-transformer file with Fusion code

> **This is the central implementation task.**
>
> The user, verbatim:
>
> *"Bahut se files hai poore codebase me jo transformers pe base hai, traditional transformers par and hamaare implementation ka kuchh hai hi nahi usme. Tumhe kya karna hai ki wo poore files ka code ko fusion ke code se replace karoge, tabhi wo transformers-fusion se model train karega instead of traditional transformers."*

**Scope:** the codebase contains many files built on the traditional transformer which contain **none of our implementation**. Every one of those must have its code **replaced with Fusion's code**. Only then will models train on `transformers-fusion` rather than on a traditional transformer.

This is a **wholesale replacement sweep**, not a patch to `Attention::forward`.

**A complete inventory of these files is a Phase-0 deliverable** — the workflow `fusion-full-explore` produces it (categories **CORE / SUPPORTING / DEAD**, per-directory counts, and how many separate transformer implementations exist: `src/model`, `engines/trainer/dense`, `engines/trainer/moe`, `engines/trainer/multimodal/*`). Nothing in this sweep starts before that inventory is complete **and** the 100% research gate (§11 Phase 0) has passed.

### Rules for the sweep

**⚠️ THE OLD PLAN IS SUPERSEDED — DO NOT FOLLOW IT.**
The header comment at `include/quant/transformer.h:119-122` reads:

> *"attention-variant layer classes REMOVED ... Standard Attention + TransformerBlock remain the only sequence mixers until the **Cender/ formula (Phase 19-23, owner-gated)** proves parity."*

**That is a previous plan and it is dead.** Do not implement Phase 19-23 as written there. The user's instruction, verbatim:

> *"iske hisaab se nahi karna hai, ye uraana plan hai. Poora ka poora hamaare new plan and architecture ke hisaab se banega. ... TransCender bas formerly/also known as waala naam ho gaya."*

Everything below is built to **our** plan and **our** architecture. **TransCender is only a name** — "is also / formerly known as" (§1) — it carries no other baggage. The existing comment must be **rewritten** to point at this plan, not inherited.

- **CORE** files → traditional-transformer logic replaced with Fusion's `QKᵀG(GS)` + routing implementation.
- **SUPPORTING** files → reused as-is.
- **DEAD** files → either **wired in** or **removed**.
- **NO DEAD CODE ANYWHERE.** Standing rule, verbatim:
  > *"Dead code nahi bachna chahiye poore project me."*

  **Zero dead code may remain anywhere in either project.** Every dead, unreachable, unwired or vestigial path is either removed or actually used — nothing is left behind as a comment saying it is out of scope. The `AttentionResidual` comment (*"dead but out of Wave-6 scope"*, `transformer.cpp:684`) is exactly the pattern this rule forbids. Project-wide, not just the sweep.
- Preserve `scale = 1/√head_dim` (`transformer.cpp:357`) and the existing NaN / div-by-zero guards — those are correctness fixes, not traditional-transformer assumptions.
- **Definition of done:** after the sweep, a model trains through the **Fusion path only**. Verified by V8 in §14.

### 2.1 Sweep inventory — CORRECTED after adversarial verification (4/4 reviewers)

**The first inventory was REFUTED. It undercounted and mis-anchored.** The corrected count is **8-10 distinct transformer stacks**, not 5. Two structural problems were found:

> *"The plan conflates three different line-number bases with no indication: **.cpp definition lines, .h class-declaration lines, and section-comment banner lines.** Every 'WRONG' above traces to that. Any executor following the plan literally will patch the wrong lines in at least eight places."*

**Therefore: this table names FILES and SYMBOLS, not line numbers.** Line anchors are given only where a verifier confirmed them exactly. A **line-anchor cleanup pass is a Phase-0 deliverable** (the plan is a working document, so its citations must be correct before execution starts).

#### 2.1a The stacks

| # | File | What it is |
|---|---|---|
| **1** | `src/model/transformer.cpp` | **The anchor.** `Attention::forward` (295), `TransformerBlock::forward` (605), `Embedding` (38), `Linear` (69), `RMSNorm` (119), `RotaryEmbedding::apply` (213), `FFN` (542). 686 lines. **DEAD `AttentionResidual`** — class at 629, body to ~671, "dead but out of Wave-6 scope" comment at 684. |
| **2** | `src/model/model.cpp` | `DenseModel::forward` (102) — the training path. `collect_named_tensors` is a **static at 138** (not 137) and hardcodes the on-disk schema (`layers.N.attention.q_proj.weight`, `ffn.gate_proj.weight`, `tok_embeddings.weight`, `lm_head.weight`). |
| **3** | `src/model/moe_model.cpp` | `MoEBlock` (ctor 18, forward 33) = RMSNorm + `Attention` + RMSNorm + `SparseMoE`. `MoEModel` ctor at **119** (not 47), forward 180. Presets `config_48T` 242, `config_1T` 258, `config_100B` 274 — the Qwen-27B / 48T targets. |
| **4** | `src/model/hybrid_block.cpp` + `include/quant/hybrid_block.h` | `HybridBlock` members: `RMSNorm attention_norm` (h:11), `RMSNorm ffn_norm` (h:12), `FFN ffn` (h:13), `Attention attn` (h:17). **`HybridAttnKind` has exactly one enumerator `STD`** (`include/quant/hybrid_scheduler.h:9`); `build_hybrid_schedule` returns all-STD (`src/model/hybrid_scheduler.cpp:13`). **This is the routing seam.** |
| **4b** | `src/model/hybrid_moe_model.cpp` + `include/quant/hybrid_moe_model.h` | **`HybridMoeBlock` / `HybridMoeModel` are NOT in `hybrid_block.cpp`** — separate files. Block ctor 5, forward 17; model ctor 48, forward 58. |
| **5** | `src/model/moe_variants.cpp` (1382 lines) + `include/quant/moe_variants.h` | **27** classes in the header, **25** `MoEOutput::*::forward` definitions. `AttentionMoE` class at **h:520** (the header; the .cpp definition of `AttentionMoE::forward` is 1093). **Corrected characterisation:** `AttentionMoE` has `q_proj`/`k_proj` -> `mul_op` Q*K -> `softmax_with_topk`, but **no value projection, no causal mask, no RoPE**, and the top-k is over the **expert** axis, not the sequence. It is **attention-shaped routing, not attention** — a candidate for *replacement*, but not a fourth attention implementation. |
| **6** | `src/model/mommoe_block.cpp` (585 lines) + `include/quant/mommoe_block.h` | **Missed entirely.** A **second independent `CrossModalAttention`** (h:130) with its own raw `q_proj_`/`k_proj_`/`v_proj_`/`o_proj_` Tensors (h:154, ctor cpp:202, forward cpp:219). `MoMBlock::forward` 363 runs self-attention then cross-modal attention; `MoMMoE::forward` 456. |
| **7** | `src/model/native_quant_moe.cpp` | **Missed entirely.** `NativeQUANTMoEModel::forward` 126 with its own `attention_norm` / `attention.forward` / `ffn_norm` / `ffn.forward` layer loop (142-146). |
| **8** | `src/adapters/tools/qwen35_engine.cpp` (888 lines) | **Missed entirely — a THIRD complete engine.** A self-contained **Qwen3.5 decoder**: own `rmsnorm()` 46; HF `self_attn.q_proj/k_proj/v_proj/o_proj` weight loading at 170-176 and 467-569; `q_norm`/`k_norm` 178-180; **RoPE with theta 1e7** at 504; full-attention single-token step 467-571; **prefill attention pass 573-790**; `final_norm` 790. Invisible to the first inventory. |
| **9** | `src/multimodal/multimodal_cross_attn.cpp` (1043 lines) | `CrossAttentionBlock` — Impl 365, ctor 367, class decl `include/quant/multimodal_cross_attn.h:182`. `forward_self_attn` 414, `forward` 422. `VisionTransformer::forward` 160, `PatchEmbedding::forward` 48, `AudioTransformer::forward` 299, `Conv1DExtractor::forward` 247, `MultimodalCrossAttention::forward` 926. The static is **`softmax_inplace` at 19** — there is **no `softmax_core`** anywhere in the repo. |
| **10** | `src/multimodal/multimodal.cpp` (1335 lines) | **Missed entirely.** `CrossModalAttention::forward` 20 (scaled dot-product cross-attention, `inv_sqrt_d` 60, softmax 73-87), `Perceiver::forward` 1061 (query-based cross-attention), and **five** `math::softmax`-routed MoE models: `VisionMoE` 1111, `AudioMoE` 1144, `VisionTextMoE` 1178, `AudioTextMoE` 1231, `AllModalityMoE` 1282. |
| **11** | `src/multimodal/multimodal_fusion.cpp` (358 lines) | **Missed entirely.** `CrossAttentionFusion` — ctor 38 with `q_proj`/`k_proj`/`v_proj`/`out_proj` and `scale = 1/sqrt(hidden)` 41; `forward` 43 (K-transpose 57-61, gemm 65, mask 73-83, row softmax 85-96, `out_proj` 99). `MultimodalFusion` 105. |
| **12** | `engines/trainer/multimodal/dense/vision.cpp` + `vision.h` | `PatchEmbedder::forward` 198, `softmax_rows` 55, `layernorm` **75** (36 is `init_matrix`), `VisionEncoder::forward_features` 296, `forward` 317. ViT is **12 layers / 12 heads** (`vision.h:15-16`). |
| **13** | `engines/trainer/multimodal/dense/projection.cpp` + `projection.h` | `QueryProjector` — class decl `projection.h:36`, **ctor 103** (93 is inside `ModalityAdapter::param_count`), `forward` 126. `wq_`/`wk_`/`wv_`/`wo_` built at 119-122. **A Q-Former cross-attention head misnamed "projection".** |
| **14** | `engines/trainer/multimodal/dense/fusion_layers.cpp` + `fusion_layers.h` | **Missed entirely.** A **second `CrossAttentionBlock`** under a colliding name — `quant::multimodal_dense::CrossAttentionBlock` (`fusion_layers.h:33`), distinct from `quant::CrossAttentionBlock`. `Tensor wq_`/`wk_`/`wv_`/`wo_`, forward `fusion_layers.cpp:85`, scale `1/sqrt(D)`. |
| **15** | `src/inference/inference_paging.cpp` | **Missed entirely.** `PagedAttention::forward` 68 — a **fully implemented vLLM-style tiled online softmax** with `scale 1/sqrt(D)` over paged K/V blocks. `ContinuousBatching::build_attention_mask` 129 builds a causal mask. |
| **16** | `src/inference/inference_kv.cpp` | **Missed entirely.** `flash_decoding` 141 — another tiled online-softmax attention. |
| **17** | `src/model/moe_enhance.cpp` + `include/quant/moe_enhance.h` | `SwitchV2Router` (cpp 292 / h 53), `DynamicExpertPool` (cpp 503 / h 82). |
| **18** | `src/model/expert_parallel.cpp` | `CapacityAwareRouter` 1399, `LoadBalanceMetrics` 1345, `RedistributionPlan` 1465. **Not** in `moe_advanced_support.cpp` (which is 1414 lines, so 1465 could not be there). |
| **19** | `src/model/moe_advanced_support.cpp` (1414 lines) | `import_weights` only. The file's own header says "all 25" but it defines **26**. **Corrected count.** |
| **20** | `src/model/moe_core.cpp` | `ExpertFFN::forward` 78, `softmax_with_topk` 98, `moe_dispatch_batched` 214, `create_moe_variant` 446. Shared by every MoE model. |
| **21** | `engines/trainer/moe/routers.cpp` | **Missed entirely** — a **genuine second router stack**. The first inventory did not cover `engines/trainer/moe/` at all. |
| — | `engines/trainer/dense/` (80+ files) | **Verified: NO transformer stack.** It is callbacks / checkpoint / optim / loss / curriculum / EMA / LoRA / distill / distributed plumbing. **Supporting, not CORE.** |

#### 2.1b THE BIGGEST GAP — the sweep is incomplete without the kernel layer

This is the finding that would have made the whole project fail its own definition of done:

> *"The plan never states what happens to the softmax/attention **KAT layers (math, kernel, backend, code_gen)**. If the sweep only rewrites `src/model/`, **every GPU backend, the AVX/AVX512 kernels, the JIT code generator and the flash-attention kernel still compute traditional `softmax(QK^T/sqrt(D))V`**, so the 'definition of done — a model trains through the Fusion path only' **cannot be reached** by the inventory as written."*

**Therefore the sweep must include the compute layers, not just the model layer.** The KAT stack — `src/math/`, `src/kernel/`, `src/backend/`, and **`src/trainer/code_gen.cpp`** — implements the actual `softmax(QK^T/sqrt(D))V`. If the formula changes, **these change too**, or the model layer computes a Fusion formula that the kernels do not implement. **CORRECTION 2026-11-10:** the earlier draft of this section listed a **`src/code_gen/` directory — it does not exist**; the JIT generator is a single file, `src/trainer/code_gen.cpp` (1,255 lines).

##### 2.1b.1 KAT-layer inventory — MAPPED (read from disk)

**The single most important function in the project is `ScaledDotProductAttentionFunction::forward`.** That is the training path's actual attention. Everything else is an inference variant of the same formula.

| Layer | File | What it computes | Status |
|---|---|---|---|
| **TRAINING** | `src/model/autograd_functions.cpp:17` — `ScaledDotProductAttentionFunction::forward` | `scale = 1.0f/std::sqrt((float)D_)` at **:25**; score loop with `sum * scale` at **:56**; **`softmax_forward_avx2(wd + row, sd + row, S_full_)` at :67**; backward at **:107** with its own `scale` at **:125** and `sum * scale` at **:178**, **:196** | 🔴 **CORE — the #1 change site.** Both forward **and** backward must learn `G`/`S`, or training will not match inference. |
| **JIT codegen** | `src/trainer/code_gen.cpp:232` — `attention_flash` | **Emits the literal formula as generated C++**: `float scale = 1.0f / sqrtf((float)head_dim);` at **:241**; max-subtracted softmax at **:284–286** (`expf(scores[j] - max_score)`, then `/= (sum + 1e-10f)`); also `generate_softmax` at **:406+** and the `attention_basic` template at **:1146** | 🔴 **CORE.** The generator *writes* the traditional attention into every JIT-compiled kernel. **✅ FIXED 2026-11-13 (V20/T6.3):** the score buffer is now a heap `std::vector<float> scores(static_cast<size_t>(seq_len), 0.0f)` at **:258** (real seq_len, no cap), `generate_attention` rejects `seq_len > 2048` and non-positive shapes loudly, the caller clamp at **:852** is the boundary gate, and `tests/test_code_gen.cpp::test_attention_v20_budget` covers 8/2048/2049/8224/32768 — **60/60 tests pass**, emitted kernel compiles clean at `/W4`. **Still open (capability):** streaming/tiled softmax for >2048-token contexts (gate **V20** second half). |
| **Flash kernel** | `src/kernel/flash_attention.cpp` | `scale = 1.0f/std::sqrt((float)D)` at **:50** (with an INF/NaN guard at **:45–51**); tiled online softmax with max-subtraction at **:109–166** | 🔴 **CORE** — the fast path for `S_full > 64`. |
| **Scalar/AVX math** | `src/math/math.cpp` | `softmax(const Tensor&, Tensor&, int axis)` at **:232** — **verified 2026-11-10: this is a GENERIC axis-parameterised elementwise softmax, NOT a duplicate of the attention formula** (same class as the already-confirmed `math_avx2*` / `math_avx512` files, which RESEARCH-4 already proved attention-free). It is the *primitive* every attention path calls, not a copy of the formula. `vec_softmax_stable` at **:373**; `vec_softmax_stable_avx2` at **:556** — which **just forwards to the scalar version**, i.e. an **AVX2-named function with no AVX2 implementation** — a §2 dead-code violation in its own right | 🟡 **SUPPORTING (shared primitive)** + 🟡 **DEAD** (the AVX2 wrapper) — **the previous 🔴 CORE label was wrong** |
| **SIMD math** | `src/math/simd_math.cpp` | `rms_norm_scalar` :47, `rms_norm_avx2` :61, `rms_norm_avx512` :101 | 🟢 **SUPPORTING** — but the RoPE AVX2 stride bug (§10M) lives in this file |
| **SIMD math (vector)** | `src/math/math_avx2.cpp`, `math_avx2_tiled.cpp`, `math_avx2_vec.cpp`, `math_avx512.cpp` | AVX2/AVX512 math variants | 🟢 **SUPPORTING** (unless any computes attention — Phase 0 must confirm) |
| **GPU backends** | `src/backend/` — **20 files**, of which **only 4 carry a fused attention implementation**: `src/backend/gpu_compute_cuda.cpp:296` (`attention_kernel`), `src/backend/gpu_compute_hip.cpp:187` (`attention_kernel`), `src/backend/gpu_compute_vulkan.cpp:1578` (`VulkanBackend::flash_attention` — ⚠️ an **honest CPU fallback**, not a GPU kernel: `:1580` records *"no SPIR-V flash_attention shader"* and `:1585` warns *"SPIR-V not implemented (REAL ONLY): CPU fallback, perf-invalid"*; the CPU implementation is `cpu_flash_attention` at **:1398**, tensor wrapper `vk_flash_attention` at **:1663**), `src/backend/gpu_compute_full.cpp:318` (`g_attn_fwd_cs` — the literal `softmax(Q*K^T/sqrt(D) + causal_mask) * V` in a ComputeShader) | **The other 16 split 1 + 15** (corrected 2026-11-12, post-loop audit). **1 more carries a *composed* attention:** `src/backend/igpu_zero_copy.cpp:1127` — `IGPUZeroCopyTrainer::forward_attention` (tensor wrapper at `:1216`) runs a full max/`std::exp`/`sum_exp` softmax and the `O += w*V` accumulation **itself**, inline, in plain C++ — it is **not** a primitive-only backend, and it is the **5th attention implementation** in this directory. The remaining **15 are primitive-only** (`backend.cpp`, `gpu_compute.cpp`, and cann/hexagon/metal/musa/opencl/openvino/rpc/sycl/virtgpu/webgpu/zdnn/zendnn + `gpu_extras.cpp`): they expose `gemm`/`gemv`/`softmax` as separate ops and let the model layer compose them. **⚠️ NAMING TRAP:** `src/backend/gpu_compute_metal.cpp:88` declares a kernel literally named `attention_kernel` that is **not attention** — it is a plain elementwise kernel with **no softmax in its body** (verified). | 🔴 **CORE — but only 4 copies, not 18** — and **5 attention implementations, not 4.** A Fusion formula needs **one canonical implementation** with these 4 (+ `igpu_zero_copy`) delegating to it; the 15 primitive-only backends stay valid unchanged under design (b). |
| **Other kernels** | `src/kernel/{kernel_gemm,kernel_production,kernel_q12,kernel_q24,kernel_q3,kernel_q6,kernel_quant4,kernel_quant8,kernel_tl,int8_quant}.cpp` | Quantization and GEMM kernels | 🟢 **SUPPORTING** — none is attention. |

**What this changes about the design.** The Fusion formula must be expressible in **four** places that currently duplicate it:
`ScaledDotProductAttentionFunction` (training) · `src/trainer/code_gen.cpp` (JIT-emitted C++ — **two** paths: `attention_flash` **:219** and the `attention_basic` template **:1108**) · `flash_attention.cpp` (fast inference) | **5 backend attention implementations** — 4 fused (cuda, hip, full — real device kernels — and vulkan, an **honest CPU fallback**, not a GPU kernel) **plus** `src/backend/igpu_zero_copy.cpp:1127` `IGPUZeroCopyTrainer::forward_attention`, a naive composed one. **The 15 primitive-only backends do not duplicate the formula** and stay valid under design (b).

**Phase-0 design requirement (added):** decide how `G` and `S` reach the hardware —
- **(a)** a **fused Fusion kernel** (new SIMD/CUDA path) and the existing paths delegate to it, or
- **(b)** a formulation that keeps the existing kernel contract — i.e. `G`/`S` are computed **outside** the attention inner loop and passed in as tensors, so `softmax(QKᵀ/√d)V` becomes `softmax(QKᵀ·G/√d)V` with the same kernel shape, or
- **(c)** a **separate Fusion path** for training and inference, leaving the traditional kernels for legacy checkpoints only.

**(b) is the cheapest to land** and keeps the 16 primitive-only backends valid (and leaves the 4 fused ones needing only a `G`/`S` parameter), but it may not achieve the O(n) common case §3.2 requires. **This is a Phase-0 decision, and it must be made before any kernel work starts.**

**The 2048 ceiling was worse than a ceiling — a live stack buffer overflow (DEFECT FOUND 2026-11-10, **FIXED 2026-11-13**).** The generator used to size the score buffer at `min(seq_len, 2048)` while the generated kernel's loops ran `j < seq_len` — for any `seq_len > 2048` the JIT-emitted `quant_attention` wrote past the end of a 2048-element stack buffer, and the caller passed `spec.M` unclamped with no test ever exercising `seq_len > 2048`. **Fix (T6.3/V20, 2026-11-13):** the emitted buffer is now `std::vector<float> scores(static_cast<size_t>(seq_len), 0.0f)` — heap, sized to the **real** seq_len, standard C++ at every size (`src/trainer/code_gen.cpp:258`); `generate_attention` **rejects loudly** (`std::invalid_argument`, naming gate V20) for non-positive shapes and `seq_len > 2048` (`:211` region), because truncate-clamping would be a bench-honesty lie; the `attention_basic` template got the same heap buffer (`:1146`); the caller clamp is the boundary gate at `:852`. Regression: `tests/test_code_gen.cpp::test_attention_v20_budget` (12 assertions — seq_len 8/2048 generate, 2049/8224/32768 throw, caller clamp, template heap buffer; pre-fix, `tests/test_code_gen.cpp:43` only ever called `generate_attention(8, …)`, so the overflow path was untested) — build-norm **60/60**, gate `test_code_gen` Passed, and the emitted 2048 kernel compiles clean at `/W4` with clang-cl. **Remaining (capability fix 2):** the generator still refuses `seq_len > 2048`, so a 4M-token context must go through the flash path — streaming/tiled softmax in generated code is the open capability work (gate **V20**'s second half).

#### 2.1c Breakage surface the first inventory missed

> *"6 test TUs reference `Attention` or `flash_attention` — `test_transformer`, `test_wave6_model_feats`, `test_protected`, `test_inference_opt`, `test_multimodal`, `test_trainer_moe_multimodal` — none of which the plan accounts for as breakage surface."*
>
> **CORRECTION 2026-11-12 (Step 4):** the count **6 is an undercount.** The full `tests/` tree is **77 files / 14,832 lines**, **40 of them** carry attention/softmax references, and the *strong* implementation-shaped sites are **not 6 but 9**: `test_protected.cpp` (calls `flash_attention_forward` at :134), `test_inference_opt.cpp` (`test_flash_attention` :166), `test_simd_math.cpp` (SIMD-vs-scalar **softmax parity**, :110-124 — the numerical conformance test for the softmax primitive), `test_backends_realonly.cpp` (CANN `reference_softmax` rows-are-distributions, :260), `test_gpu_capability.cpp` (the **fail-loud** contract test, :29 / :300 — this is the **GAP-2** test surface), `test_quant_mix.cpp` + `test_trainer.cpp` + `test_training.cpp` (the **attention-projection parameter enumeration** — where a new format's coverage of attention weights is asserted, i.e. the **Track-A** test surface), `test_code_gen.cpp` (the JIT path — `seq_len=8` only), and `test_kv_cache_quant4.cpp` (the real KV-quant4 test). Full list with the grep command and its output: **§10Y.6**.

> **AUDITED 2026-11-12 (plan-loop Step 4) — the five tree paths are now closed; see §10Y.** The old note said all five were *"spot-grepped — no attention or softmax found"*. That was **true for three** (`src/gle/`, `inferno/`, `scripts/` — 0 hits each) and **false for two**: `src/core/telemetry.cpp` contains a whole `KVCacheQuantizer` (**12 hits**), and `src/server/` carries the serve-time attention-shape authority plus **three** `INADDR_ANY` binds. The `tests/` tree is **not** clean either — it is the **conformance surface** for the attention formula (40 of 77 files carry attention/softmax references), and the sibling `code-fusion` monorepo is **clean** (2,713 source files, **0** implementation-shaped hits). `include/quant/*.h` for further declared-but-unimplemented attention variants **remains open** — that is §2.1d and it is unaffected by this pass.

#### 2.1d A live dead-code violation, confirmed

`include/quant/inference_opt.h` **declares** `PagedAttention` (17), `MultiQueryAttention` (278), `GroupedQueryAttention` (296), `SlidingWindowAttention` (316) and `ALiBi` (333) — and `src/inference/inference_serve.cpp:5-8` documents that **MQA/GQA/SWA/ALiBi have zero definitions anywhere**. These are **dead declarations**, which §2's zero-dead-code rule already forbids. Either implement them (in Fusion form) or delete them.

#### 2.1e The rule that follows

- If it builds a **Q/K/V/O product** or a **softmax over it** -> **CORE**, replace.
- If it is a **norm, embedding, FFN, tokenizer or loss** -> check whether a replaced mixer uses it; if it contains its own softmax/attention -> **CORE**.
- If it has **zero call sites tree-wide** -> **DEAD**, wire in or delete.
- If it is in the **KAT layer** and implements `softmax(QK^T/sqrt(D))V` -> **CORE** — because §3 changes that formula.
- `HybridAttnKind` currently having only `STD` is the **intended seam** for routing — built to *our* §5 design, **not** to the superseded Phase 19-23 plan.

## 3. The new attention core

### 3.1 Baseline (exists today)

```
Attention(Q, K, V) = softmax( QKᵀ / √d_k ) · V
```

`Q, K, V` keep their **Google/traditional definitions exactly**. The change is additive.

### 3.2 Fusion attention

```
Attention(Q, K, V, G, S) = softmax( QKᵀ · G(GS) / √d_k ) · V
```

Five letters: **Q, K, T, V, G** — with **S** the argument that makes `G` work.

**`G` — Gate.** A learned, **length-invariant relevance gate** that decides, per token, how much loop depth to spend and which slice of state to consult. Three jobs, one per failure mode:

| Failure | What `G` must do |
|---|---|
| **Context rot** | Keep the attention mass carried by a relevant token **constant as `n` grows**, instead of the standard `1/n` dilution. |
| **Lost in the middle** | Make attention **position-independent** — a fact in the middle gets the same opportunity as one at the top. |
| **O(n²) cost** | Compute against the index `S`, not the full sequence, so the common case is **O(n)**. |

**`S` — Structure.** The compact, indexable, **never-discarded** representation of everything seen, backed by **`.idx`**.

| Requirement | What `S` must do |
|---|---|
| **"Never forgets anything"** | Nothing is evicted or compacted away — it moves **into the index**, not out of existence. |
| **Window doubling** | The active window grows (4M → 8M → 16M) because the cost of carrying full history lives in `S`, not in the attention matrix. |

> **This is the load-bearing design.** `G`/`S` must be **researched before implementation** — a hard gate (§11 Phase 0).

### 3.3 Where it goes in the code

`transformers/src/model/transformer.cpp:295` — `Attention::forward`.

- Q/K/V projections **303–305**; reshape `{B,S,H,D}` **307–309**
- RoPE on q,k **316–317**, **335–337**; KV cache append / `get_all` **337–341**
- YARN mult pre-scale with NaN guard **347–353**
- **`scale = 1/√head_dim`, div-by-zero guarded: 357–358** ← the `÷√d_k` to keep
- GQA expansion **362–382**
- Long path `flash_attention_forward` when `S_full > 64` **385–394**
- Short path builds the `n×n` score matrix directly **401+**
- Config in `include/quant/transformer.h`: `head_dim=64`, `rope_theta=10000`, **`max_seq_len=2048`**, `RoPEScalingMode`, YARN params (**17–38**), FP8 path (**74–94**)

**Insertion points:** the scale at **357**, the score build at **386–394 / 401+**. The position-dependent causal mask at **386–392** is exactly the Lost-in-the-Middle term.

**A dead `AttentionResidual` exists at `transformer.cpp:629`** (comment **684**) — resurrect or remove, never leave.

---

## 3b. NCM — Next-Concept Modeling (the generation mechanism)

> Added by the user with a third transcript (§15.3): *"Isko bhi plan me add karne ka, ispe bhi research hoyega."*
> The user's framing: **"tokens predict karne me speed badhegi"** — NCM speeds up token prediction.

### 3b.1 What it actually is (VERIFIED — arXiv `2610.14162`, published 2026-10-09)

**"Next-Concept Modeling: Fast, Parallel Coarse-to-Fine Text Generation"** — Hermann Kumbong, Ishan S. Khare, Iddah Mlauzi, Andrew Woen, Charles Ding, E. Kelly Buchanan, Simran Arora, Azalia Mirhoseini, **Christopher Ré** (Stanford Hazy Research).

| Field | Value |
|---|---|
| **arXiv** | `2610.14162v1` |
| **Published** | 2026-10-09 |
| **Categories** | cs.CL (primary), cs.AI, cs.LG |

**The problem NCM attacks:** autoregressive generation writes one token at a time and each step waits for the previous one. Diffusion models allow parallel sampling but **lose quality at fewer steps, reprocess the whole sequence every step, and need many dataset passes.**

**NCM = a two-stage, coarse-to-fine framework:**
1. A **multiscale residual VQ-VAE** encodes text into a **hierarchy of discrete codes** (the "tokenizer").
2. A **transformer generator** produces **one level at a time**, predicting **all codes within that level in parallel**, conditioned on earlier levels.

It **still uses a transformer** — it changes *what* the transformer predicts (discrete codes, not words) and *the order* (coarse → fine levels, not left → right tokens). It does **not** replace transformers.

### 3b.2 Reported results (from the paper, as verified above)

| Benchmark | Result |
|---|---|
| **XSum summarization** | ROUGE-L **parity** with the best DLM baseline, **31× faster** |
| **LM1B** | **Better** generative perplexity than the strongest DLM baseline, **21× faster** |
| **OpenWebText** | **Competitive** with the strongest DLM baseline, **10× faster** |
| **Sudoku** | Outperforms **both autoregressive and diffusion baselines** across all difficulty levels, with **fewer function evaluations** |

**Critical caveat — the 31× is not "faster than ChatGPT":** it is NCM vs a **diffusion** baseline (Aurora LM) on XSum, 1,024 sequences, batch 16, single H100 SXMGPU. It does **not** establish NCM beats standard autoregressive models on every workload.

### 3b.3 Why this belongs in Fusion — five specific points

1. **It is exactly the system definition the user gave.** *"It predicts next token, but — according to the context"* (§Context). AR predicts the next word left-to-right with no view of the whole answer. NCM **first sketches the shape of the whole answer**, then fills detail in passes — i.e. it **decides according to the whole context before committing**. This is the generation-side embodiment of the same idea as `G`/`S`.

2. **It composes with the architecture; it does not conflict with it.** Loop transformers change **depth**; `G`/`S` change **what gets attended to and for how long**; NCM changes **what is predicted and in what order**. Three orthogonal axes. NCM's level-parallel decoding also **reduces sequential steps**, which multiplies with the loop-exit policy (§5) for total speedup.

3. **Coarse levels are a natural consumer of `S`.** A coarse level is a low-resolution sketch of the whole sequence — which is precisely what an index-addressed `S` (§8) can supply cheaply, O(n), without dense attention over 4M tokens. The sketch lives in the index; the fine levels resolve it.

4. **Discrete code hierarchy is quantization-friendly.** NCM already predicts **discrete codes**. Our target is **1.5 BPW** (§9b.1). A generator operating over discrete levels interacts with quantized weights far more favourably than a floating-token AR head — and MQC-Bench-1.0 (§9) should measure this directly.

5. **It serves the speed target for benchmarks.** Our hard goal is **90%+ on Terminal-Bench-4.0-style benchmarks** with a *bad* 27B model (§Context). Agentic benchmarks are tool-loop latency-bound; fewer sequential generation steps per decision is a direct lever on that number, and D&CC-Bench-1.0 specifically requires **live, immediate decisions** (§7 target 7).

### 3b.4 Open questions the research phase must answer

The transcript is explicit that NCM is a research system, not a drop-in. These become **Phase-0 research items**:

- **Scale.** The paper's generators go to **725M parameters** in scaling experiments. Our models are **4B** and **27B**. Scaling improved quality in the paper's experiments, but behaviour at these sizes is **untested**.
- **Reconstruction fidelity.** *"If details are lost in the representation, the generator can't reliably restore them later… especially important for **names, numbers, and other exact details**."* This is **fatal** for our PDF test (§7 target 5: exact line and page number) — reconstruction loss breaks V5.
- **Task-specific configs vs general-purpose.** NCM's output format is **structured and bounded**; the experiments use task-specific configurations. A general assistant must answer *"one sentence, then a page, then a longer report in the same system."* How NCM handles open-ended, variable-length output is unanswered.
- **Structured tasks are its strength** — Sudoku shows a hierarchy of representations helps **globally consistent** answers. That maps to our "decides according to the context" requirement, but the transcript cautions a controlled benchmark does not imply broad reasoning gains.
- **Checkpoints.** Published NCM checkpoints exist on HuggingFace for **XSUM, WMT14 (De→En), Sudoku, TinyStories, LM1B**; **OpenWebText is pending**. There is **no general-purpose NCM chat assistant** — it must be integrated into our engine, not downloaded.

### 3b.5 Implementation shape (Phase 6 addition — see §11)

NCM needs two stages, matching the paper:

1. **Multiscale residual VQ-VAE tokenizer** — trains to encode text into the discrete code hierarchy and decode back. **Freeze it after stage 1.**
2. **Transformer generator** — trained with the tokenizer **frozen** to predict the levels in order, all codes of a level in parallel, conditioned on earlier levels.

**Where it lands in our engine:** `DenseModel::forward` (`model.cpp:102`) is the training path and the token head is `lm_head`. NCM changes the head from "next-token logits" to "per-level discrete-code logits" and changes the generation loop from left-to-right to level-by-level. **This is a second sweep, downstream of the `QKᵀG(GS)` sweep** — the attention core can be built first and NCM layered onto it.

**An important scoping decision for Phase 0:** NCM can be adopted **incrementally** — the tokenizer + generator can first be trained **on top of** the Fusion attention core as a separate objective, or fused into one training run. The incremental path is far lower risk and should be the default.

### 3b.6 THE FULL SPEC — extracted from the paper (arXiv `2610.14162v1`)

> Source: `https://arxiv.org/html/2610.14162v1`. This is the implementable detail; the mechanism below is transcribed from the paper's §3, Eq. 9, Eq. 10 and Algorithms 1–2.

#### Stage 1 — multiscale residual VQ-VAE (the tokenizer)

- Encoder maps input tokens to latents: `z = E_φ(x) ∈ ℝ^{L×d}`.
- **K levels with GROWING lengths**: `l₁ < l₂ < … < l_K = L`. Level `k` owns codebook `V_k` (size `|V_k|`) and `l_k` positions.
- **Each level quantizes the residual the earlier levels missed:**
  - down-sample the previous residual: `u_k = Down_k(z^{(k−1)})`
  - nearest-codebook lookup: `r_k^i = argmin_j ‖u_k^i − e_{k,j}‖²`
  - lift back to length `L` and accumulate: `ẑ^{(k)} = ẑ^{(k−1)} + R_k(e_k(r_k))`
  - new residual: `z^{(k)} = z − ẑ^{(k)}`
- **Training — nested dropout:** keep only the first `k` levels for a random cutoff `k`, forcing early levels to carry real meaning on their own.
- **Stage-1 loss (Eq. 9):** reconstruction cross-entropy **+** `β`-weighted commitment MSE **+** latent quantization MSE with stop-gradient, trained with a **straight-through estimator**.

#### Stage 2 — the transformer generator

- **Factorisation:** `p(r_{1:K}) = Π_k p(r_k | ẑ^{(k−1)})`, and within a level `Π_i p(r_k^i | ẑ^{(k−1)})`. **Codes inside one level are conditionally independent**, so **all `l_k` positions are produced in a single forward pass** and sampled in parallel.
- **Conditioning:** the cumulative reconstruction of all earlier levels `ẑ^{(k−1)}`, resized to `l_k` positions and projected to hidden width.
- **Stage-2 loss (Eq. 10):** `L_NCM = −Σ_k w_k Σ_i log p(r_k^i | z̃^{(k−1)})` with weight `w_k = l_k^{−α} / Σ_j l_j^{1−α}`. **`α = 0` equalises code positions; `α = 1` equalises levels.** — this is a tunable knob we get to set.
- **Conditioning corruption:** a fraction of conditioning codes are swapped for other codes **from the same codebook** while the ground-truth codes stay as labels, so the generator tolerates accumulated VQ error. Swap rates vary by level.
- **Attention pattern:** block-diagonal for unconditional generation; a **prefix-LM** pattern for prompts (prompt embeds via the frozen VQ-VAE token embedding table), with prompt positions unable to attend to targets.

#### Training order

1. Train the multiscale VQ tokenizer (nested dropout, VQ + commitment losses).
2. **Freeze it**; train the generator on **all K levels in a single forward pass** with cross-entropy. For paired tasks (XSum/WMT14) the generator is first trained on unpaired text, then on pairs. **Seed 42, BF16.**

#### Numbers we can hold the work to

| Quantity | Value |
|---|---|
| **Default model size** | ~100M |
| **Task generators** | WMT14 **120M** · XSum **88M** · Sudoku **25M** |
| **Scaling sweep (LM1B)** | **97M / 317M / 725M** — one frozen tokenizer shared |
| **NFE, unconditional** | ~4–11× fewer than diffusion baselines. LM1B: 11× fewer NFE than DUO, **21× faster** |
| **NFE, conditional** | XSum: **8 NFE** vs AURORA-LM's 128 (**16×**), running **31× faster**. WMT14: 11 NFE vs E2D2's 64 (5.8×) |
| **NFE, Sudoku** | **12** — fewest of all methods (FMLM+ 16, others 128) |
| **Training budget** | LM1B tokenizer+generator process **13.36B** token positions vs baselines' **66B** (~4.9× fewer) |

**Tokenizer reconstruction accuracy (the number that decides whether NCM is usable for us):**

| Corpus | Exact reconstruction | Codebook utilisation |
|---|---|---|
| OpenWebText | **99.99%** | 62–90% |
| LM1B | 99.86% | |
| TinyStories | 99.98% | |
| XSum | 99.79% | |
| **WMT14** | **98.79%** ← worst | bottoms out ~62% |
| **Sudoku** | **100%** | |

**Quality results:** LM1B beats the strongest DLM at matched scale; OpenWebText competitive at 10× faster; XSum ROUGE-1/2/L **37.3/14.0/29.6** with MBR (beats guided AURORA-LM's 36.3/13.4/28.6 at 184 NFE); WMT14 BLEU **25.2** with MBR, tying the AR baseline; **Sudoku fully-solved 99.5 / 96.5 / 86.1** (easy/med/hard) versus **AR sampling's 13.9 / 5.1 / 0.6**.

**Code: `https://github.com/HazyResearch/ncm`.** No model-weights link was found in the paper page.

#### Stated limitations — the authors' own

- Scaling is called **"preliminary"**; they suggest "potential for further gains from larger generators."
- The training-budget advantage is a **conjecture**: *"One possible explanation is that NCM's fixed coarse-to-fine order simplifies learning."*
- **Tokenizer errors are non-trivial: they "often involve substitutions of related words or entities."** ← **this is the single biggest risk for us** — see §3b.7.
- Test-time scaling needs extra candidates + MBR, so **NFE savings are partly spent on decoding**.

### 3b.7 The three risks this spec creates for Fusion — and what to do

**RISK 1 — exact-detail loss breaks V5.** WMT14 reconstructs at only **98.79%**, and the authors say errors "often involve substitutions of related words or entities." V5 (§14) requires the model to state **which line and which page number** — i.e. exact numbers and exact strings. A 1.2% substitution rate destroys that.

**Mitigation:** measure reconstruction **on our own corpus** (filenames, error strings, page/line refs, numeric values) before committing — this is **V23**. If the hierarchy loses detail, either raise `K`, enlarge the fine-level codebook, or keep an **exact-token escape channel** for numerals and identifiers. **Sudoku's 100%** is the encouraging signal: structured, exact content *can* be lossless.

**RISK 2 — scale.** The largest generator tested is **725M**. Ours are **4B** and **27B** (§9b). The authors themselves call scaling "preliminary" and admit they cannot explain the advantage.

**Mitigation:** **V25** — prove quality holds at our size before NCM carries any headline result. Treat the incremental adoption path (§3b.5) as the default so a scale failure does not block the attention work.

**RISK 3 — the benchmarks are task-specific.** XSum, WMT14, Sudoku and LM1B each get their **own generator at its own size** with its own schedule (unpaired → paired). A general assistant must answer *"one sentence, then a page, then a longer report"* in one system.

**Mitigation:** NCM is adopted for **generation**, not as a replacement for the agent loop. The harness (CodeFusion) keeps owning variable-length, tool-using, open-ended behaviour; NCM speeds the token-producing step inside it. **D&CC-Bench-1.0** (§9) is where we test whether live decision-making survives at our level.

**What NCM gives us that is unambiguous:** `p(r_k | ẑ^{(k−1)})` is a **coarse-to-fine** factorisation — the model commits to a **whole-sequence sketch** before any detail. That is literally *"predicts next token, but according to the context"* (the system definition), and it is a natural consumer of `S`: the coarse level is exactly the low-resolution index lookup §8.2 describes.

---

## 3c. DSpine — Adjacent Causal Injection speculative decoding (RESEARCH ADDED 2026-11-09)

> Operator asked: **"TF — DSpine x NCM"** — implement both generation mechanisms in
> Transformers-Fusion. DSpine accelerates the AR token loop (lossless); NCM replaces the
> generation shape. They compose. This section is the implementable spec, extracted from
> the full paper ([arXiv `2609.36173v2`](https://arxiv.org/html/2609.36173v2), read live
> 2026-11-09; code [tencent/dspine](https://github.com/tencent/dspine); models
> `tencent/Qwen3-8B-DSpine-b16`, `tencent/Qwen3.8-27B-DSpine-b16`, Apache 2.0).

### 3c.1 The problem it attacks

Parallel drafters (DFlash lineage) draft a block of M candidates in ONE backbone pass, but
positions predict **before predecessors commit** → individually plausible tokens form
inconsistent continuations → prefix acceptance decays. Prior fixes (Domino/DSpark/DFlash2)
condition **after** the backbone — predecessor info enters too late. DSpine's two measured
insights:

1. **Early positions form recoverable predictions in shallow layers** (layer-wise readouts
   recover substantial token-predictive info at early positions in shallow layers).
2. **Accurate adjacent-predecessor features help successors more when they enter earlier**
   — replacing the correct predecessor with its draft prediction lowers successor accuracy
   by **31.8 pp**; earlier (L2 vs L4) K/V injection adds **+14.8 pp**.

### 3c.2 The mechanism (four parts)

**Part 1 — Unified Transfer Space** (what is passed between positions):

- From the target LM head: ℓ2-normalize rows → center/PCA-whiten → keep top-r directions →
  re-normalize rows → fixed table `C_v = normalize(Λ_r^(-1/2)·P_r^T·(Ē_v − μ))` (Appendix A).
- Predicted feature: `z_{ℓ,t} = √r · normalize(R_ℓ·u_{ℓ,t})` (no vocab decode).
- Known token x enters as `√r·C_x` — same pathway carries predictions AND decided tokens.

**Part 2 — Gated Adjacent Injection** (after EVERY layer ℓ, position t ← predecessor t−1 only):

```
g_{ℓ,t} = σ(G_q·z_{ℓ,t} + G_p·z_{ℓ,t−1} + b)          # gate (sigmoid)
m_{ℓ,t} = A·z_{ℓ,t−1}                # message = A·predecessor feature
h_{ℓ,t} = u_{ℓ,t} + RMS(u_{ℓ,t})·W_ℓ·(g_{ℓ,t} ⊙ m_{ℓ,t})  # gated residual write
```

- `A, G_q, G_p` LAYER-SHARED; `W_ℓ` per-layer; `b` shared. All messages use pre-update features →
  injection is parallel within a layer; anchor unchanged.
- **Block-causal attention** in all L backbone layers (unlike DFlash's bidirectional).
- Effects propagate through depth: layer-ℓ messages shape layer-ℓ+1 messages (the "spine").
- Fused kernels: 3 projections merged into one matmul + 2 fused kernels inside the draft
  backbone's CUDA graph.

### 3c.3 Transition-cached predecessor-conditioned decoding

- Final layer: h_{L,t} → RMSNorm + shared LM head → top-K candidates per position (K=16).
- **Last-write refinement**: for predecessor token s, replace z_{L,t−1} ← √r·C_s, redo the
  final-layer write (Eq. 5) from cached pre-injection state u_{L,t} → conditional scores
  S_t(s, v). 
- **Transition cache** `T_t[i,j] = S_t(v_{t−1,i}, v_{t−1,j})` — enumerating all K² pairs in parallel; selection walks the cache.

### 3c.4 Layer-wise output-embedding supervision

`L_emb = Σ_ℓ Σ_i w_i·[1 − cos(e_{ℓ,i}, C_{y_i})]`, `w_i = exp(−(t_i−1)/γ)` (block-position decay).
Table 3 ablation: directional embedding supervision WINS; per-layer full-vocab CE FALLS BELOW
the unsupervised baseline ("forcing intermediate states to classify tokens may interfere with
their contextual computation").

### 3c.5 Training recipe (Appendix A, verbatim numbers)

| Item | Value |
|---|---|
| Backbone | **5 layers**, block size **16** (1 anchor + 15 candidates), block-causal attention |
| Injection params | **+33M ≈ 3% of backbone** (A, G_q, G_p, b, W_ℓ, R_ℓ) |
| Transfer space | r dims from target LM-head PCA (fixed, shared by all layers) |
| Loss | `L = L_dist + λ·L_emb`; `L_dist = Σ w_i[−α·log q_i(y_i) + (1−α)·‖q_i − p_i‖₁]`, **α=0.1** |
| λ schedule | `λ = β_t·sg(CE_bb)`, β_t 0→0.5 over first 146 steps |
| Correct-predecessor curriculum | p=0.5 for first 1/6 of training, linear → 0 by 1/3 |
| Data | ShareGPT, responses regenerated by target (thinking disabled) |
| Optimizer | AdamW no-wd, lr 6e-4, 4% warmup (146 steps), cosine, max seq 3072, **6 epochs (3655 steps)** |
| Frozen | target input embeddings + LM head shared & frozen |

### 3c.5a Training loss details

- Backbone output predicts full vocab; last-write-refinement output predicts over top-K=16
  candidates only (target renormalized to the set; CE where correct token ∈ candidates; ℓ1 where candidates hold >1e-4 target prob).
- Injection init: R_ℓ ← P_r^T; W_ℓ, G_p zero-init with b=0 → injection starts as identity.
- Supervision ablation (Table 3): directional (embedding-space) supervision wins; per-layer
  full-vocab CE falls below unsupervised baseline.
- Correct-predecessor curriculum: p=0.5 (first 1/6) → 0 (by 1/3), one draw shared by layers 1–3.

### 3c.6 Numbers (verified from the paper)

| Metric | Value |
|---|---|
| Acceptance length τ (Qwen3-8B, T=0, 7-bench mean) | **3.77 → 4.82 (+27.8%) vs DFlash** |
| vs strongest baselines | +10.0% over DFlash2 (greedy), +12.8% over DSpark (sampling) |
| SGLang throughput | **+23.3% vs DFlash, +11.1% vs DFlash2; up to 4.0× over AR** |
| Round cost | 7.14 ms vs DFlash2 7.19 ms; **10.9% less decode time per token** |
| Injection overhead | ≤0.15 ms/round (5 layers); transition cache < half the cost of post-backbone heads |
| Benchmarks | GSM8K, MATH-500, HumanEval, MBPP, LiveCodeBench, MT-Bench, Arena-Hard (T=0/1) |

### 3c.7 Why DSpine belongs in Fusion (composition analysis)

1. **Lossless** — speculative verification preserves the target distribution exactly
   (Eq. 1 acceptance + Eq. 11 correction), so it composes with **any** generator behind it
   (AR, NCM, loop routing) without touching quality. It multiplies with LoopSpec-style
   self-speculation (§5, 6.83×) as a second, independent lever.
2. **Independent axis of speed.** Loop routing changes depth (§5); G/S change what is attended
   (§3.2); NCM changes generation shape (§3b); DSpine changes the token loop (§3c) — four
 orthogonal levers that multiply.
3. **Qwen3.8-27B drafter already exists** (`tencent/Qwen3.8-27B-DeepSpine-b16` exact name TBC on HF; `tearch/Qwen3-8B-DSpine-tnt`...). Drafters for Qwen3-8B/4B released; **Qwen3.8-27B-DSpine-b16 exists** per search — verify exact HF id when landing.
4. **Qwen3.8-27B was this workspace's benchmark model** (superseded by DeepSeek V4.1 Flash per NEW-2) — the drafter exists for the **engine's own models** once they exist.
5. **The iGPU host constraint** (Vega 7, 7 CUs, ~448 shaders, shared DDR4) makes DSpine's
   cost profile attractive: injection ≤0.15 ms/round on H100-class hardware; on our host the
   relative savings of higher acceptance length are even more valuable (verify host runs slow).
6. **NCM composition** — NCM emits levels in parallel; DSpine accelerates whatever loop
   remains. Two accelerators on the same engine: NCM for the generation shape, DSpine for the
   remaining AR/loop steps. Order: engine → NCM → DSpine (DSpine needs a stable target to draft FOR).
7. **SGLang integration is the paper's harness; ours is CodeFusion ↔ TF engine bridge.** The
   paper runs DSpine in SGLang; our equivalent is the CodeFusion ↔ TF engine bridge (§10R item 5).
8. **The "spine" name is a direct fit** — the engine IS Transformers-Fusion; DSpine injects
   conditioning through the depth of a drafter backbone ("spine") — the plan's "spine" language
   ("the engine IS the spine") now has a literal mechanism match. The engine-side analogue:
   predecessor→successor injection through depth = a per-token-depth spine. (Narrative note,
 not a technical dependency.)

### 3c.8 What DSpine does NOT do (boundaries, so scope stays honest)

- **Not a context fix.** It does not address context rot / lost-in-the-middle (§5c.1) — that is
  `G`/`S` (§3.2) and window doubling (§7). DSpine is a token-loop accelerator.
**Corrections applied in this section (research pass 2026-11-09, repaired 2026-11-10):**
- Eq. 5 message form is `m_{ℓ,t} = A·z_{ℓ,t−1}` — the earlier `m_{ℓ,tm}` / `m_{ℓ,tm} = A·z_{ℎ}` fragments were typos. See §3c.2.
- Eq. 5 gated write is `h_{ℓ,t} = u_{ℓ,t} + RMS(u_{ℓ,t})·W_ℓ·(g_{ℓ,t} ⊙ m_{ℓ,t})` — the earlier `h_{typo}` fragments were typos. See §3c.2.
- HF id check: `tencent/Qwen3.8-27B-DSpine-b16` is the likely HF id (an earlier note mis-typed it as `ternel/…` and `DeepSpine`); verify the exact id at landing time.
- Not a quality change: verification is lossless (Eq. 1/11) — acceptance length τ is the only metric.

### 3c.8.1 Same-trunk four-lever structure (the design conclusion)

Same trunk, four levers:
- **Lever 1: G/S (§3.2)** — what gets attended (context rot / LITM / O(n) via index).
- **Lever 2: Loop routing (§5)** — per-token depth (T-LoopFormer token-choice routing + recursion-wise KV cache).
- **Lever 3: NCM (§3b)** — generation shape (levels in parallel, coarse-to-fine).
- **Lever 4: DSpine (§3c)** — token-loop acceleration (lossless speculative decoding).
These four levers on one trunk = "TF — DSpine x NCM" scope. Levers 3+4 = the two NEW levers added by this research pass.

### 3c.9 Phase-6c scope

- Drafter backbone: 5-layer block-causal drafter, block 16 (1 anchor + 15 candidates).
- Unified transfer space table C_v from the engine's LM head (PCA-whitened, r dims).
- Gated adjacent injection (Eq. 4/5) + layer-wise embedding supervision (Eq. 6) + transition cache (K=16 candidates) — Appendix A: K=16 (candidates); r (transfer-space dims) is a paper Appendix-A value to extract at landing (Table 4 has it).
- Transition cache (K=16) + last-write refinement + lossless verification (Eq. 1/11).
- Training recipe per §3c.5 (α=0.1). DSpine drafter trained ON OUR corpus, not ShareGPT —
  our-corpus regenerated-response recipe, seeded by released Qwen3-3-8B drafter weights only if target = Qwen3-8B; for our own models, train from scratch on our corpus.
- **Do not use the released Qwen3-8B drafter for our models — train our own drafter on our corpus** (released drafters are target-specific). Released weights useful only as a correctness reference for the mechanism.
- V-gates: V28 (τ ≥ 4.0 on our corpus), V29 (lossless parity + composition with NCM).
- **iGPU constraint note:** paper used H100-class; our host is Vega 7 iGPU — injection overhead and transition cache cost must be re-measured on OUR host (V28/V29 measured on our host).

**Appendix A values still to extract:** transfer-space rank `r` and the other Appendix-A values (Table 4) — the HTML text-dump did not render Table 4’s numeric cells. Extract them from the paper PDF at landing time.


---


## 4. Neurons — Req 1

### 4.1 The requirement

The user, verbatim:

> *"Humans ke paas bhi hote hai aur AI ke bhi hote. To dono ke alag-alag capabilities hote hain, mujhe dono capabilities waale neurons banane hai aur unhi pe hamaare AI models train honge, capabilities dono ke and best performer dono me, but digital."*

Clarified by the user:

> *"Honge ye bhi AI ke hi neurons but ye Enhanced Artificial Intellegence Neurons honge jo dono ka capability hold karte hai aur dono ka power ho inme and benchmarks me bhi haraa de un dono ko."*

**Build Enhanced Artificial Intelligence Neurons — EAIN.**

- They **are still AI neurons** — not a biological simulation. They are the AI unit, **upgraded**.
- They **hold the capabilities of both** human neurons and AI neurons.
- They carry **the power of both**.
- Models are trained **on these neurons**.
- **They must beat BOTH — humans AND ordinary AI — on benchmarks.**

### 4.1a The benchmark bar

This is a hard, measurable target, and it raises the stakes of §14:

| Must beat | Where it shows up |
|---|---|
| **Ordinary AI** | CS-Bench, D&CC-Bench, MQC-Bench — EAIN-trained models must outperform conventional-neuron models. |
| **Humans** | CS-Bench-1.1 is built so that it can **confuse humans** — the top-100 / *"maan lo"* questions. EAIN models must score **above** the human baseline. |

**"Defeat both"** means reporting an explicit three-way comparison — **EAIN-trained model vs human baseline vs ordinary-AI baseline** — on every benchmark, not just an absolute score. Human baselines must be **captured for the same question sets**, so the comparison is real rather than asserted. This is added as **V15** in §14.

> Note the coupling: humans are the *bar* for CS-Bench-1.1 (§9), so EAIN beating humans there is the single clearest demonstration that common sense has been delivered (§9, "Why common sense is the real bar").

### 4.2 Why the distinction matters (from Transcript 2)

We use the **same vocabulary** for both — *neurons, memory, reasoning, understanding, hallucination* — and unconsciously assume AI is like a human brain. **It is not.**

| | **AI neuron** | **Human / biological neuron** |
|---|---|---|
| **Nature** | A **mathematical function** — takes numbers, passes an output | An **insanely complex living cell** |
| **Mechanism** | Matrix multiply, activation, gradient update | **Electrical signals, chemicals, timing**, interactions with **thousands** of other neurons |
| **Learning rule** | **Backpropagation** — loss computed, billions of **parameters** ("knobs") nudged microscopically over unimaginable data, plus **RLHF** | Plasticity, neuromodulation, experience-driven permanent change |
| **Adaptation speed** | Frozen after training; adapts only via context or fine-tuning | **Continuously updates** — you exist in reality and reality continuously changes you |

**EAIN takes the AI neuron as its base and adds the right-hand column's capabilities as digital mechanisms** — it does not become a biological cell.

**Brain complexity is not confined to neurons.** The open questions listed, none with complete answers:

- How is **memory** formed?
- How do we **permanently change** from a single experience?
- How do different parts of the brain **synchronize**?
- How do **chemicals** alter **attention** and **learning**?

**The target is the union of both columns — as a digital AI construct.**

### 4.3 Design framing

Take the best of each side:

- **From the AI side** — the properties that make current models work: the mathematical unit, gradient-trainability, and the full existing learning stack, which must be **honoured, not discarded**: statistical representation learning, next-token prediction, **backpropagation**, **loss**, **parameters**, **RLHF**.
- **From the human side** — the properties AI lacks: continuous self-update from environment, experience-driven permanent change, chemical/modulatory gating of attention, cross-region synchronization, and temporal dynamics (**timing** matters, not just magnitude).

**The digital constraint is not a limitation — it is the point.** We are not simulating biology; we are taking biology's *capabilities* and expressing them in a construct that trains with backpropagation on digital hardware.

### 4.4 What it must connect to

- **The `J` jump (Einstein, 1952).** The user stated Fusion **can** make this jump; showing how is on us. Einstein's letter to Maurice drew a **three-step loop**: observe the real world → collect data → **the jump** to a new rule, denoted **"J"**. AI cannot make it because it lacks real-world physics — falling, hanging upside down, the feel of a lift. **There is no fixed algorithm from real-world observation to a new idea.** A continuously-updating, environment-learning, biologically-informed neuron is meant to close exactly this gap.
- **The World Model** (§7C) — already implemented. This is where environment learning lives.
- **Continuous self-update as a first-class property** — *"apne aap ko continuously update karna human intelligence ki ek major property hai."*
- **RSI — Recursive Self-Improvement.** Named by the user as **the genuine threat**, distinct from fear-mongering. Structurally the same capability: a system improving itself without human intervention.
- **Feelings as encoded representations** — happy/sad/awkward are mathematical relationships in the network; a question activates those patterns.
- **AGI definition discipline** — *"Ek model agar mera computer use karne lag jaye to main usko AGI nahi bolunga."* Before real AGI, **~10 fake AGIs will come and die.**
- **Predictions are not facts** — Hinton's 2016 radiologist prediction failed (there are more radiologists now). And **LeCun: LLMs are not the future; world models are.**

### 4.5 Status — RESOLVED by direct audit (no longer open)

A full-workspace audit was run (category **neurons**). **Verdict: zero. Nothing exists.**

> *"There is NO neuron implementation of any kind anywhere in the workspace. No bio-inspired unit, no spiking neuron, no LIF, no dendrite, synapse, soma, axon, tau, refractory, STDP, or neuromodulator code. **This is a net-new build.**"*

**How the audit was run:** `rg --no-ignore --hidden` — because `code/.rgignore` and a large `.gitignore` chain **silently hide matches**, so an ordinary grep reports a **false clean** here. Anyone re-checking must repeat with `--no-ignore`.

**Categories, cleanly separated:**
- **(a) Real neuron implementation — NONE.** No file, class, struct, or function.
- **(b) Generic NN vocabulary misread as neuron-like** — all verified as false positives:
  `NeuralArchitectureSearch` (`include/quant/agi.h:378`, a generic NAS over `struct Architecture { int layers; int hidden; float score; }`) · Exa's `'neural'` search mode (`packages/web/web-search-exa/src/types.ts:13`) · `leaky_relu` — **a ReLU variant, NOT leaky-integrate-and-fire** (`engines/trainer/dense/init.h:23,26`; this is the most dangerous trap for any automated coverage check) · `consolidate()` — memory dedup by cosine > 0.95 (`src/agi/agi_extended.cpp:507`, `world_model.cpp:630`), not sleep-like consolidation · `has_vnni` = "Vector Neural Network Instructions" (an Intel INT8 GEMM ISA flag) · ANN prose in `bench/bench_poc_benchmark.cpp` · `NPU` — a **hardware target**, with comments explicitly noting NPU work is *not* really running.
- **(c) Nothing** — everything else.

### 4.6 What already exists to build ON (module-level, verified)

The workspace is **rich in module-level analogues** of exactly the mechanisms a neuron needs — but has **no unit-level implementation** of any of them.

| Block | Path | Why it matters |
|---|---|---|
| **ECC / Elastic Weight Consolidation** | `include/quant/continual_engine.h:90-101` (`ECCState { fisher_diagonal, anchor_weights }`, `update_fisher`, `update_anchor`, `regularize`). Also `fisher_importance` at **35** (not 34), `update_importance(decay_rate)` at **67**, `importance_resample` at **56** (not 54-55). | **Per-parameter importance** = the canonical synaptic-consolidation primitive. The single most directly reusable piece. **There are three parallel continual-learning stacks — see §4.8a; they are NOT to be consolidated.** |
| **Fisher-weighted importance decay** | `include/quant/continual_engine.h:35, 56, 67` | A working importance-decay mechanism. |
| **Stability / Plasticity controller** | `include/quant/inferno_integration.h:152-197` — `StabilityPlasticityParams {forgetting_weight, current_lr_factor, stability_lr_factor, plasticity_lr_factor, forgetting_threshold}`; `inferno_hook_stability_plasticity` | **CORRECTED — this is DEAD, not wired.** The hook has **zero call sites** workspace-wide. The rule actually used is a *different, simpler* implementation at `src/adapters/src/continual_trainer.cpp:152-159` with a hardcoded `0.1f` threshold and a `[0.01, 10.0]` clamp — **and that class is never instantiated either.** Treat as **declared-but-dead**: the real controller must be written fresh. |
| **Reward + prediction error + curiosity** | `include/quant/reward.h:18-56` (`RewardModel`, `reward_loss`, `compute_abstention_reward`, `importance_factor = 8.0`) · `include/quant/agi.h:366-374` (`CuriosityDrivenExplorer::intrinsic_reward`) · `include/quant/world_model.h:94-99, 114, 79-80` (`avg_prediction_error`, `predict_with_uncertainty` at **114**, epistemic/aleatoric split at **79-80**) | Supplies the **dopamine analogue** and a novelty/curiosity signal for **local credit assignment without a global backward pass**. **Caveat:** `importance_factor_ = 8.0f` is **never consumed** in `src/trainer/reward.cpp` — it is a dead field. |
| **`StateMemoryEntry`** | `include/quant/world_model.h:86-91` (`importance_weight`, `access_count`, `last_accessed`) in a bounded deque, max 10000, plus `update_importance_weights()`, `consolidate_memory()` | The **closest existing per-unit state container** and the natural host surface for a hybrid neuron. |
| **MoE router / gating** | `include/quant/moe_enhance.h:13` | The gating primitive — the natural home of a "which unit fires" decision. |
| **AGI subsystem** | `src/agi/` — agi.cpp 44.2K, agi_extended.cpp 34.0K, agi_flywheel.cpp 102.9K, agi_guardrails.cpp 11.2K, meta_cognition.cpp 30.7K, multi_agent.cpp 27.3K, self_eval.cpp 31.5K, world_model.cpp 25.0K; `include/quant/agi.h` 19.3K | Substantial scaffolding with host classes: `SelfMonitor`, `MemorySystem`, `PlanningEngine`, `ToolUse`, `EvaluationHarness`, `Flywheel`, `CapabilityAmplifier`, `CuriosityDrivenExplorer`, `HPOptimizer`, `ContinuousLearner`, `KnowledgeDistillation`. Real — the missing part is the neuron itself, **not** a place to put it. |

### 4.7 The exact gap — unit-level, not module-level

This is the sharpest finding and it defines the whole Phase-4 design:

**Present (wrong granularity):**
- plasticity → a scalar LR factor over a whole trainer (`inferno_integration.h:164`, `continual_trainer.cpp:152`)
- importance → a per-parameter Fisher diagonal (`continual_engine.h:86-100`) or a per-memory-entry weight (`world_model.h:87-91`) — **never a per-unit weight trace**
- decay → `update_importance(decay_rate)` over replay samples (`continual_engine.h:54`)
- reward / prediction error → `RewardModel`, `WorldModelStats` — real and usable
- gating → MoE router

**Absent entirely:**
- any notion of **TIME inside a unit** — no `tau`, no time constant, no timestep
- any **threshold** or spike
- any **refractory period**
- any **per-unit local update rule**
- any **soma-like state integration**

**Conclusion:** EAIN is a **NEW unit type** whose per-unit state sits **on top of these existing signals**. It cannot be assembled by renaming or re-exposing what is there.

### 4.7a Each missing primitive now has a literature source (§5c.4)

| Missing (§4.7) | Paper that supplies the mechanism |
|---|---|
| **Time constant inside the unit** — no `tau`, no time dynamics | **LTC** `2006.04439` (state-coupled liquid time-constants, ODE-solver outputs, stable/bounded, proven universal approximator `1811.00321`); **LTC-SE** `2304.08691` unifies LIF + CTRNN + NODE + CTGRU in one library |
| **Threshold / spike** | Surrogate-gradient SNN line `2304.13289`, `2505.10371` (ILIF — names the "dilemma of gamma": surrogate support width trades overactivation vs vanishing gradients) |
| **Refractory period** | `2505.10371` inhibitory LIF with coupled inhibitory units — the closest construct |
| **Per-unit local update rule** | `2605.00402` — local plasticity with **three-factor rules + eligibility traces, no backprop**; `2002.10585` (Backpropamine) for the differentiable version |
| **Soma-like state integration** | **TC-LIF** `2307.07231` / `2308.13250` — two compartments tuned for short- and long-term memory, with theory for **relief of vanishing gradients**; online-learning fix in `2402.15969` |
| **Chemicals altering attention/learning** | **Backpropamine** `2002.10585` — neuromodulated plasticity trained by gradient descent, gains on RL *and* supervised; measured, not speculative |
| **Brain-state modulation** | `2311.06074` — apical vs perisomatic compartments with **amplification / isolation / drive regimes** tied to wake / NREM / REM |
| **Permanence, no catastrophic forgetting** | Already in-repo: ECC/Fisher (§4.6). CLS framing: **UNKNOWN** — no paper surfaced; do not cite one |

### 4.7b The trap to avoid

`2302.14311` found the **temporal branch of BPTT contributes little to gradients** and dropped it for a >70% memory saving at SOTA accuracy. Read correctly, this warns that **adding spikes for their own sake will not help.** EAIN's gains must come from the two mechanisms where the literature reports *measured* wins:

- **liquid time-constants** (changes expressivity — `1811.00321`, `2006.04439`)
- **neuromodulated plasticity** (changes *what learns when* — `2002.10585`)

Everything else — spike counts, refractory periods, energy claims — is optional and must earn its place with an ablation, not by biological resemblance.

### 4.7c The concrete unit shape the literature supports

- **State:** activation `h`, **liquid** `tau(h, input)` per LTC, an **eligibility trace** per `2605.00402`.
- **Two compartments:** soma (fast, short-term) + dendrite (slow, long-term) per TC-LIF — *this is how one digital unit holds both a working state and a persistent state*, which is exactly §4.4's "continuously updates" property.
- **Plasticity:** weight update **modulated by reward-prediction error**, trained end-to-end by gradient descent (Backpropamine). Our existing `RewardModel` (§4.6) is the modulator source — no new signal needed.
- **Consolidation:** per-parameter Fisher importance (already in ECC) + the brain-state regime of `2311.06074` to decide **when** a unit consolidates.
- **All differentiable** — the AI-side column (§4.2) is preserved exactly, which is non-negotiable: these are **Enhanced AI neurons**, not a biology simulation.

---

### 4.8 Two constraints to honour

1. **`install_test/` is a build OUTPUT, not a source tree — never hand-edit it.** The first plan said neuron work "must land in both trees or the copy drifts." **That premise was wrong.** `install_test/` is a `cmake --install` **output** (`CMakeLists.txt:600`), contains only `bin/` + `include/`, has **no CMakeLists of its own**, and is **100% untracked** (`git ls-files install_test` = 0). **Drift has already occurred** — 126 shared names, 32 differ; `inferno_*` was renamed to `sops_*`. The correct instruction is: **regenerate it from the build, or delete it** — never mirror changes into it by hand.
2. **Must live in `transformers-fusion`.** `code/` holds **no** neural substrate — no reward/prediction-error/gating machinery, no analogue at all. It is the harness. The neuron is engine-side.

### 4.8a Three parallel ECC/continual implementations — **NO consolidation**

> **The user rejected this:** *"Kya ECC consolidations? Koi ECC ka skill add nahi karna, wo mera puraana decision tha add karne ka!"*
>
> **Adding an ECC consolidation is explicitly out of scope. Do not merge, consolidate or unify the three continual-learning stacks.** The three implementations stay as they are.

| # | Where | What |
|---|---|---|
| **1** | `src/trainer/continual_engine.cpp` + `include/quant/continual_engine.h` | `ContinualEngine` + `ECCState` — the full Fisher/anchor implementation |
| **2** | `src/adapters/src/continual_trainer.cpp:152-159` | A hand-rolled `fisher_`/`anchor_` pair with the stability-plasticity rule and a `[0.01, 10.0]` clamp. Never instantiated. |
| **3** | `src/trainer/trainer_core.cpp:1153` | `Trainer::enable_continual` — the third entry point. |

**Consequence for Phase 4:** EAIN is built **on top of** this existing machinery as-is. Which of the three it sits on is an implementation detail to settle during design — **not** a consolidation project. §4.6's "reuse what exists" instruction stands unchanged.

### 4.9 Scope warning — implement only what is actually implementable

The audit also flagged a hazard in the requirement's own framing. The transcript it derives from explicitly states the biological side is **not fully understood** — *"we ourselves still don't have a complete answer"* to how memory forms, how one experience permanently changes the brain, how regions synchronize, how chemicals alter attention and learning.

**Therefore there is no complete spec to implement against.** Anyone building this must scope it to the implementable subset rather than implying the biological half can be faithfully reproduced:

> **Implementable subset** = per-unit importance/decay + thresholded activation + local plasticity driven by reward prediction error + offline consolidation.

That is what Phase 4 designs. Not a biological simulation.

### 4.10 Sequence — and it was explicitly confirmed by the user

> *"ham karenge naa isko. Banayenge. Pehle planning fir research fir baaki phases and sab baari-baari se ban jaayenge."*

**Planning → research → implementation, one phase at a time.** That is exactly the Phase 0 gate in §11: nothing is implemented until planning and research are complete.

---

## 5. Architecture: hybrid **adaptive routing**, not a static split

**An early misunderstanding, now corrected.** "Half loop, half traditional" does **not** mean some layers are one thing and some another, fixed. The user's clarification, verbatim:

> *"Ya to teeno ka hybrid theek hoga ya kuchh aisa karna hoga ki layers re-arrange ho sake, jahaa jaroorat ho loop waale ki wahaa sab traditional waale bhi loop me transform ho jaaye."*

On what "transform" means:

> *"traditional pe chalta rahega to loop me kaam karne lagega saath me learned gated bhi hoga"*

So the mechanism is **both**:

- **Layer re-arrangement** — a layer running in traditional mode **must also be able to work in loop mode**. Not two disjoint populations; every layer is capable of either and switches as needed.
- **A learned gate** decides when.

Design intent: **the hardest work is handled by loop reasoning**, and a direct benefit is **saved compute cost** — the cheap path stays cheap, depth is spent only where it pays.

### Hard constraint — RESEARCH BEFORE IMPLEMENT

> *"Bahut jaroori hai, internet pe research iske liye karna jaroori hai, bina research ke implement mat kar dena."*

**Nothing about routing or `G`/`S` may be implemented before research is 100% complete.** A gate, not a guideline.

### Research grounding (verified — these papers exist)

`WebSearch` is non-functional in this environment. Findings came via the **arXiv API**, which works. DuckDuckGo HTML is bot-gated; Google hits a consent wall.

| Paper | arXiv | Relevance |
|---|---|---|
| **Looped Transformers for Length Generalization** | 2409.15647 | Adaptive step counts → **unseen input lengths**. Attacks the 4M/doubling target. |
| **LT2: Linear-Time Looped Transformers** | 2605.20670 | Linear/sparse attention **inside** loops; *iterative memory refinement*. A converted **1.4B beat industry 4B models**. Validates small-model-big-behaviour. |
| **Looped Transformers with Source-Centered State Evolution** | 2607.27656 | A learned **anchor** that is "a one-step fixed point by construction", with **exact anchor invariance** — closest published analogue to **"never forgets"**. Informs `S`. |
| **SpiralFormer: Multi-Resolution Recursion** | 2602.11698 | Recurrence over **compressed multi-resolution sequences**. Informs how `S` holds a 3000-page PDF. |
| **T-LoopFormer: Token-Level Elastic-Depth** | 2609.15160 | Per-token iteration counts + **recursion-wise KV cache**. |
| **FlashLoop** | 2609.29812 | Token-sparse updates, **KV-residual quantization** — relevant to **MQC-Bench** at 1.5 BPW. |
| **Adaptive Depth in Looped Transformers** | 2607.20519 | Post-hoc confidence readouts **match or beat** learned gates. Practical loop-exit guidance. |
| **TaH2 (Improving Test-Time Scaling)** | 2609.35748 | Extra iterations **only to tokens that benefit**. |
| **LoopSpec** | 2609.17184 | Self-speculative decoding — up to **6.83×** speedup. |
| **TTT: Learning to (Learn at Test Time)** | 2407.04620 | The hidden state **is itself a model**; unlike Mamba it **keeps improving past 16k**. Strongest conceptual match for `S`. |
| **Huginn (recurrent-depth)** | 2502.05171 | Prelude / core-loop / coda split, latent test-time compute. |

**Unverified — do not cite:** **"ALSTA"** returned **zero hits**. An earlier pass also mis-assigned arXiv **2407.04620** to ALSTA; that ID is **TTT**.

**Synthesis for design:** `S` should be a **test-time-learning state** (TTT) that is **anchor-invariant** (SCSE), carried at **multi-resolution** (SpiralFormer), reachable by **linear/sparse attention** (LT2). `G` decides per token how much loop depth and which slice of `S`.

---

## 5c. CONSOLIDATED RESEARCH FINDINGS (solo, arXiv — verified 2026-11-01)

> The user's standing instruction: *"workflows ka jitna data aa gaya hai uska use karke final data bana, baaki ka poora kaam khudse karke."* Workflows returned **nothing** (5/5 failed on free-tier caps), so everything below was fetched **directly, solo**, via the arXiv API and `arxiv.org/html`. Every ID below was read from a live response — none is from memory.

### 5c.1 WHY lost-in-the-middle happens — the mechanism G must attack

This is the most important research result in the whole plan, because it changes what `G` has to be.

**Three theory papers explain the U-curve without blaming training data:**

| Paper | arXiv | The finding |
|---|---|---|
| **Lost in the Middle at Birth: An Exact Theory of Transformer Position Bias** | `2603.10123` | The U-shape appears **at initialisation, before training and independent of positional encoding** — *"a geometric property of the causal decoder with residuals."* Layered attention behaves as powers of the **Cesàro matrix**; causal masking gives a **logarithmic gradient divergence at the prompt start**, residuals create an **O(1) terminal anchor**, and between them lies a **factorial dead zone of order `O(1/(H−1)!)`**. Verified on **untrained** Qwen2 and GPT-2 at step 0, with or without RoPE. |
| **Kinetic theory for Transformers and the lost-in-the-middle phenomenon** | `2605.09213` | Models causal self-attention as an **interacting particle system** with a mean-field limit. For uniformly random tokens the correlation equation is solved **in closed form**, *"yielding a rigorous explanation"* of the U-shape with primacy, recency, and a **single interior minimum**. |
| **An Adjoint-Sensitivity Framework for Lost-in-the-Middle in Causal Residual Transformers** | `2607.17696` | Defines a normalised influence density under gradient flow and finds that **causal masking and residual identity paths individually do NOT force a U-shape** — it gives **sufficient, not necessary**, conditions. Offers **positional reweighting** and observability balance as diagnostics/regularisers. |

**Consequences for `G` and `S` — these are now design requirements, not guesses:**

1. **The middle dead zone is `O(1/(H−1)!)` — factorial in depth `H`.** So the penalty **worsens superlinearly with depth**. A `G` that only rescales attention weights at one layer cannot fix this; the fix must act on the **residual/depth path**, not just the softmax row. This is the strongest argument in the plan for `G` living in `QKᵀ·G(GS)` *inside* every layer rather than as a post-hoc reweight.
2. **Because it is present at initialisation and RoPE-independent**, removing positional encodings will **not** fix it. Any plan that says "drop RoPE" is refuted by `2603.10123`. **V12** (the top/middle/bottom regression test) is therefore testing the right thing — but it must run on the **untrained** model too, or we will be tuning a geometric constant.
3. **Per `2607.17696`, the U-shape is sufficient-not-necessary** — so the *architecture can be changed* to avoid it. That paper's own suggestion, **positional reweighting**, is effectively what `G` is. Its adjoint-sensitivity machinery gives us a **measurable target**: keep the influence density flat across positions. Add to **V12**: assert the influence-density curve is flat, not merely that accuracy is.

**What is already known about the softmax itself being the culprit:**

| Paper | arXiv | Relevance to `G` |
|---|---|---|
| **When Attention Sink Emerges in Language Models** | `2410.10781` (ICLR 2025 Spotlight) | The sink *"acts more like key biases, storing extra attention scores"* that are *"non-informative and do not contribute to the value computation"*, and stems from **token interdependence via softmax normalisation**. Replacing softmax with **unnormalised sigmoid attention prevents sinks up to 1B params.** |
| **Softpick: No Attention Sink, No Massive Activations with Rectified Softmax** | `2504.20966` | A **rectified, non-sum-to-one softmax** replacement: reported **0% sink rate** at 340M and 1.8B, lower-kurtosis hidden states, sparse attention maps, and **quantised variants beat softmax with the gap widening at low bit precision.** |

**This is a direct hit on two of our requirements at once.** Our target is **1.5 BPW** (§9b.1) — Softpick reports its advantage *widening at low bit precision*, which is exactly our regime. And a **non-sum-to-one** normaliser is precisely the mechanism that keeps per-token attention mass **constant as n grows** (§3.2 requirement a) instead of the `1/n` dilution.

**So `G` now has a concrete literature-backed form** — see §5c.2.

### 5c.2 Candidate formulations for `G(GS)` — grounded, with trade-offs

`G`'s three jobs (§3.2): length-invariant mass, position-independence, O(n) common case. Three candidate forms, each traceable to the papers above:

**Form A — rectified / unnormalised gate (Softpick-lineage, `2504.20966` + `2410.10781`)**
```
Attention = rectify(QKᵀ·G(GS) / √d_k) · V
```
`G` supplies a per-query scale that is **not** forced to sum to 1 across keys, so a relevant token's mass stays constant as the window doubles. Kills the sink (which `2410.10781` attributes to softmax normalisation) and therefore kills the primacy anchor.
- **Length invariance: yes** (that is the point). **Position independence: yes** for the sink component. **O(n): not by itself** — needs `S` to pick a subset.
- **Reduces to standard softmax when disabled? NO** — the whole normaliser changes. This breaks **V10** as written. **V10 must be amended**: the strict-superset property should hold for `G(GS)` as a *multiplicative* term with `G ≡ 1` recovering today's behaviour, and the normaliser change should be a *separate* gated flag.
- **Risk:** unnormalised attention changes the training dynamics of everything downstream; needs its own gradient check (V19).

**Form B — index-selected gate (RETRO / memory-layer / sparse-attention lineage)**
```
G(GS) = g(S_q, K_idx)   →  selects m ≪ n keys, then softmax over those m
```
`S` is the persistent structure; `G` scores the query against `S` and returns a **selection mask plus a size normaliser `log m` instead of `log n`**. Length invariance follows because the softmax is over `m`, which is fixed.
- **Length invariance: yes, cleanly.** **O(n): yes** — `m` is constant. **Position independence: yes** *provided the index is not position-ordered* (an important design constraint on `S`).
- **Reduces to standard softmax when `m = n` and `G ≡ 1`: YES.** **Best fit for V10.**
- This is the formulation that makes the **4M→8M→16M doubling actually survivable**, because the dense cost stops tracking the window.

**Form C — depth-corrected gate (targets the factorial dead zone directly)**
Because `2603.10123` locates the dead zone in the **residual-depth** path, `G` can also carry a **per-layer influence correction** — the adjoint-sensitivity view of `2607.17696` — so mid-position tokens keep influence as depth grows.
- Not a stand-alone answer; **a required complement** to A or B. Without it, the O(1/(H−1)!) decay remains.

**Recommended composite:** **B as the backbone** (index-selected, `log m` normalisation, satisfies V10 by construction) **+ C as the depth correction** (targets the measured dead zone) **+ A as an experimental flag** (sink/quantisation benefits, tested separately because it breaks the strict-superset property).

**Note on what we do *not* yet know** — labelled **UNKNOWN**: whether the factorial dead-zone result of `2603.10123` holds for **looped/weight-tied** blocks, where the "powers of the Cesàro matrix" argument would iterate a *shared* operator rather than distinct layers. §5's routing means many of our layers are weight-tied, so the constant may behave differently. **Phase-0 experiment:** reproduce the step-0 U-curve on a weight-tied looped model.

### 5c.3 Adaptive routing — what the literature supports

| Paper | arXiv | Finding we use |
|---|---|---|
| **Attention Is All You Need For Mixture-of-Depths Routing** (A-MoD) | `2412.20875` | Standard MoD routers **add layers that are hard to train and cost deployment overhead**. A-MoD **reuses the preceding layer's existing attention map for routing**, adding **"no additional trainable parameters"** and adapting easily from pretrained transformers. Up to 2% higher ImageNet accuracy, up to 2× faster transfer learning. |
| **Mixture-of-Depths Attention** (MoDA) | `2603.15619` | Deep-LLM signal degradation: shallow features get **diluted by repeated residual updates**. Lets each head attend to **current-layer KV *and* depth KV from earlier layers**; hardware-efficient, **97.3% of FlashAttention-2 efficiency at 64K**. Pairs **better with post-norm than pre-norm**. |
| **X-MoD** | `2609.34212` | MoD's fixed one-sparse/one-dense alternation **couples total capacity to active capacity**. Decouples token sparsity from anchor stride so total params grow while active-equivalent capacity stays ~fixed. Gives an explicit **scaling law** for sparse depth. |
| **Comparing Fixed and Adaptive Computation Time for RNNs** | `1803.08165` | **Surprising: Repeat-RNN (a *fixed* repeat count) performed as well as ACT** on the tasks tested. A caution against assuming the learned gate will pay for itself. |
| **DACT-BERT** | `2109.11745` | Differentiable ACT controlling how many Transformer blocks execute at inference; beats baselines **in tightly constrained compute regimes**, competitive under looser budgets. |
| **Probabilistic ACT** | `1712.00386` | Reframes ACT as an **ad-hoc relaxation** of a proper discrete-latent model; per-input compute via amortised MAP with Concrete relaxation; matches ACT's trade-off with **lower memory** and deterministic eval. |
| **p-MoD / UniMoD** | `2412.04449` / `2502.06474` | **Naive MoD pruning underperforms** — p-MoD needed tanh-gated weight normalisation and symmetric reweighting to stabilise; UniMoD found **redundancy differs by task** and needed **a separate router per task**. |

**Four conclusions the plan now adopts:**

1. **Route with the attention map we already compute (A-MoD), not a new router network.** Our engine has no spare router budget at **1.5 BPW**, and `2412.20875` shows the extra trainable router is the main cost *and* the main training difficulty. **This changes §5's "learned gate"** from a new module into a **read-out of the existing attention scores** — cheaper, and it composes with `G`.
2. **Expect the fixed-repeat baseline to be hard to beat.** `1803.08165` found fixed repeats matched learned ACT. So the routing gate needs a **measured ablation against a fixed-schedule baseline**, and we must be honest if it loses. Add to V13's spirit: **assert learned routing beats fixed-depth looping on our own benchmarks** — if it doesn't, use the fixed schedule.
3. **One router is probably not enough.** `2502.06474` found redundancy varies by task; our D&CC-Bench and Terminal-Bench-style tasks are very different. Budget for **task-conditional routing**, not a single global gate.
4. **Watch the norm interaction.** MoDA *"pairs better with post-norm than pre-norm"*; our `TransformerBlock` is pre-norm (`transformer.h:139-142`). **This is a concrete, checkable risk to the routing design** and becomes a Phase-0 experiment rather than an assumption.

**Also relevant to `S`:** MoDA's idea of attending to **depth KV from earlier layers** is a second axis for `S` — the index can hold both *sequence* history and *depth* history. Worth a Phase-0 experiment.

### 5c.4 EAIN — the literature basis, and its honest ceiling

| Capability the user asked for | Literature basis (verified) |
|---|---|
| **Time constant inside the neuron** (the thing §4.7 says is entirely absent) | **Liquid Time-constant Networks** — `1811.00321` (universal-approximator proof; time-constants that **vary through a nonlinear synaptic transmission model**, inspired by small-species nervous systems) and `2006.04439` (AAAI-21; state-coupled **liquid time-constants**, outputs from numerical ODE solvers, stable and bounded, stronger expressivity within the neural-ODE family). **`2304.08691` (LTC-SE)** unifies **LIF spiking, CTRNNs, NODEs and CTGRUs into one TensorFlow class library** — the cleanest engineering base for our unit. |
| **Neuromodulation gating plasticity** (the dopamine/serotonin role) | **Backpropamine** — `2002.10585`: *"the first demonstration that networks with neuromodulated plasticity can be trained by gradient descent."* Plastic LSTMs with **millions** of parameters beat standard LSTMs on language modelling, and neuromodulation improved both RL **and supervised** performance. **This is the single most directly reusable paper for EAIN** — it is *digital, backprop-compatible, and implements chemical modulation.* |
| **Two compartments — soma + dendrite** | **TC-LIF** — `2307.07231` / `2308.13250`: somatic and dendritic compartments tuned for **short- and long-term memory**, with theory for **relief of the vanishing gradient problem**, fast convergence, energy efficiency. **`2402.15969`** fixes its BPTT memory cost with online learning + an **Adaptive TC-LIF**. **`2311.06074`** models apical vs. perisomatic compartments with **brain-state-specific amplification/isolation/drive regimes** (wake / NREM / REM) — a literal mechanism for *"state changes how attention and learning work."* |
| **Spikes with backprop** (if we want threshold + refractory) | Surrogate-gradient SNN line: `2304.13289` (tunable surrogate shape + membrane-potential distribution adjustment), `2302.14311` (SLTT — **drops the temporal branch** because it contributes little to gradients, cutting memory >70% and time >50% at SOTA ImageNet), `2410.11488` (rate-based backprop captures rate coding at far lower cost), `2505.10371` (**ILIF** — names the "dilemma of gamma": surrogate-support width trades overactivation against vanishing gradients; adds coupled inhibitory units), `2602.01978` (**SpikingGamma — surrogate-gradient-FREE** online training via sigma-delta coding, no surrogate needed), `2003.01250` (explicitly trains spiking sparsity into the loss). |
| **Permanent change from a single experience / consolidation** | **Already in our codebase** — ECC/Fisher (§4.6). Literature check for the **complementary-learning-systems** framing (hippocampus+neocortex) returned **no matching paper** in the queried set — labelled **UNKNOWN**, not fabricated. |
| **Local, non-backprop credit assignment** | `2605.00402` — structured recurrent SNN trained with **local plasticity only**: winner-take-all teaching, fixed random broadcast alignment, **three-factor rules with eligibility traces**, **no backprop or surrogate gradients.** Directly relevant to a per-unit update rule. |

**The honest ceiling (must be stated, not glossed).** §4.9's warning now has teeth: `2302.14311` found the **temporal branch of BPTT contributes little to gradients** — i.e. when we do add real time dynamics to our neurons, the naive reading is that most of the temporal computation may be gradient-irrelevant. The same paper had to *drop it for efficiency*, which means the temporal signal was weak *under that task*. **So EAIN's benefit will not come from adding spikes for their own sake.** It must come from **liquid time-constants** (which change expressivity, `1811.00321`) and **neuromodulated plasticity** (which changes *what learns when*, `2002.10585`), where the papers report measured gains.

**Concrete EAIN unit shape the literature supports** (replaces the hand-waved version):
- **State:** membrane/activation `h`, **liquid time constant** `τ(h, input)` per LTC `2006.04439`, an eligibility trace per `2605.00402`.
- **Two compartments:** soma (fast, short-term) + dendrite (slow, long-term) per TC-LIF `2307.07231` — this is *how one digital unit holds both a working and a persistent state*, which is the §4.4 "continuously updates" property.
- **Plasticity:** weight update **modulated by a reward-prediction-error signal**, trained end-to-end by gradient descent per Backpropamine `2002.10585`. Our existing `RewardModel` (§4.6) is the modulator source.
- **Consolidation:** per-parameter Fisher importance (already in ECC, §4.6) + the brain-state regime idea of `2311.06074` to decide *when* a unit consolidates.
- **All of it differentiable** — preserving the AI-side column (§4.2) exactly as required.

### 5c.5 Research gaps — what is still UNKNOWN (stated, not hidden)

Labelled per DRAFT.md §57's observation / inference / **unknown** rule.

1. **ASTRA — RESOLVED as *reported*, still NOT confirmed by OpenAI (2026-11-10).** *The Information*, 2026-09-01/02 ("OpenAI Technique in 'Astra' Model Sparks Security Concerns", Efrati / Palazzolo / Rocket): **GPT-6 "Astra" uses recurrent depth** — text is repeatedly routed through shared transformer layers before the next token is predicted. OpenAI **neither confirmed nor denied** (per The Verge); chief scientist **Jakub Pachocki** stated the compute-graph depth of Astra and the other frontier models is **"within a factor of two of GPT-4"**, that the loop is deliberately **limited to keep the CoT legible**, and that OpenAI would publish more architectural detail later. **What OpenAI *did* document in its own system card: "GPT-6 Astra shows a substantial decrease in chain-of-thought monitorability compared to previous models"** — that part is *documented*, not merely reported. Corroborating (2026-10-13): a Microsoft Azure page for **GPT-6.1 Sol** read *"uses the same base model weights as GPT-6 Sol with two inference passes instead of three"** — deleted after it surfaced; consistent with looping. **The plan's earlier note is now explained:** the leaderboard string `gpt-6-1-sol` = *GPT-6.1 Sol*, a sibling of GPT-6 Astra — it was never contradicting "Astra", just differently named. **Status: REPORTED, UNCONFIRMED-BY-OPENAI.** The plan still does not depend on it: every Astra-derived number is about the **adapter** (§10G/§10P), and that design stands on the leaderboard data alone.
2. **The provider-adapter mechanism itself.** No public document was found describing what a `-provider-adapter` run *does*. The empirical pattern (99.99% with, 3–35% without, across two vendors) is solid; the mechanism is **inferred**. §10V's `CONTEXT_WINDOW_EXCEEDED → extend` swap and §10P's reasoning-across-compaction gap remain the concrete build targets — they are derived from *our* codebase's actual gap, which is the safer ground.
3. **62.7% / 99.9% / 99.99% have no independent source.** All come from the user's transcript and the leaderboard they pasted. Internally consistent, externally unconfirmed. **UNKNOWN.**
4. **NCM appendix details — RESOLVED (2026-11-09 research pass).** `2610.14162v1` was read from character offset 100000 onward: Appendix C Tables 5–6 (exact `K` and `|V_k|`), the Appendix F.1.1 levels ablation (`K ∈ {4, 8, 16, 32}`) and Appendix I "Limitations & Future Work" were all retrieved. **What remains are our decisions, not the paper's gaps:** scale beyond 725M, reconstruction fidelity for names/numbers (fatal for the PDF test — see the 98.79% WMT14 figure at §3b.6), general-purpose variable-length output vs task-specific configs, and whether `github.com/HazyResearch/ncm` is usable as a starting point. Decide incremental adoption vs fused training (§3b.5).
5. **Whether the factorial dead-zone result holds for weight-tied loops** (§5c.2 note) — untested in the literature as far as found.
6. **Complementary learning systems / hippocampal CLS** — no matching paper surfaced in the query run. **UNKNOWN**, though our in-repo ECC covers the practical need.

### 5c.6 G/S DESIGN NOTE — the written design (OPEN-RESEARCH #4 deliverable, 2026-11-13)

> **Method:** deep-read of the ten §5 papers — `2603.10123` (Cesàro U-curve), `2603.15031` (AttnRes),
> `2605.18855` (Delta AttnRes), `2610.13630` (MSAR), `2607.27230` (MHAR), `2607.09694` (LR-AttnRes),
> `2606.18524` (Loop-µP), `2610.00673` (Closing the Loop), `2605.16343` (LoopQ), `2610.16368`
> (LoopQuant) — abstracts fetched live this session, bodies consolidated against §5c.2/§5c.3, §5d
> and §5e (whose 2026-11-10 pass read every ID from live arXiv API responses). **This note states
> the design and tags every remaining fork; it closes no OPEN-DECISION by fiat** — each fork keeps
> its ledger id and the operator stamps it (D-15 delegation covers priority, not the ruling).

**G — the gate (design statements G1…G8):**

1. **G1 · Backbone = Form B on both axes.** Sequence axis: `G(GS)` selects `m ≪ n` keys from the
   index `S` and softmaxes over those `m` with a `log m` normaliser — length-invariant, O(n), and
   V10's strict-superset property holds **by construction** (`m = n, G ≡ 1` recovers today's
   softmax). Depth axis: the *same* mechanism is AttnRes (`2603.15031`) — softmax attention over
   preceding layer outputs. One mechanism, two axes; §5e names the family.
2. **G2 · No new router module.** Route by **reading the attention scores already computed**
   (A-MoD, `2412.20875`): *"no additional trainable parameters"*, adapts from pretrained
   transformers, and it composes with `G`. Our engine has no spare router budget at the
   1.0-BPW side goal. Learned-gate vs post-hoc readout stays **OPEN-DECISION #6** (readout is the
   recommended default, and the fixed-repeat baseline of `1803.08165` is a mandatory ablation).
3. **G3 · Routing cost decoupled from width.** Use **LR-AttnRes's r-dimensional routing keys**
   (`2607.09694`) for any `G`-side scoring — the only family variant whose routing cost does not
   scale with hidden width `d`. MHAR (`2607.27230`) shows a single shared depth query degrades
   progressively **as width grows** — a scaling hazard, not a styling choice.
4. **G4 · Form C is required, as a hypothesis.** The factorial dead zone `O(1/(H−1)!)`
   (`2603.10123`) lives in the **residual-depth** path; without a depth correction the
   mid-context influence collapses regardless of the sequence-axis gate. **Caveat carried into
   the gate:** the Cesàro result assumes **distinct per-layer operators**; under weight-tied
   loops the constant is **OPEN-UNKNOWN #11** — Form C stays a hypothesis until the step-0
   U-curve is reproduced on a weight-tied looped model.
5. **G5 · Attend over deltas, not cumulative states.** Delta AttnRes (`2605.18855`): cumulative
   hidden states are redundant, driving **routing collapse** (weights near-uniform, max ≈ 0.2)
   at depth; routing over per-sublayer **deltas** restores contrast (max ≈ 0.6). Design
   consequences: `S`'s depth entries store **sublayer deltas**; and `G`'s V-gate asserts
   **depth-attention contrast** (max routing weight), not merely output correctness — the same
   spirit as V12's flat influence-density assertion.
6. **G6 · Exit gate, specified.** `λ_t(x) = σ(Gate(F^(t)(x)))`; inference uses the **Q-exit
   rule** (exit when the exit-CDF crosses `q` — a deployment knob, no retraining). Training
   requirements: **LR warmup** (without it `p(exit at step 1)` stays 1.00 for 2,267 steps —
   the silent collapse), **β ≥ 0.10** for recovery, and the **smoothed exit loss**
   `L = (1−ε)·Σ p_t·L_t + (ε/T)·Σ L_t` with **ε = 0.05** so abandoned steps keep gradient
   (≥ 0.0167 of LM weight at T = 3). **Monitor the exit distribution directly; the LM loss
   will not show the collapse.** [OPEN-DECISION #18's content, stated as design.]
7. **G7 · The policy must shrink work, not just depth.** Per-token routing where inactive
   tokens skip deeper recursions **including their attention and KV work**
   (Mixture-of-Recursions; T-LoopFormer `2609.15160`). This is a **design requirement on the
   `HybridAttnKind` / `build_hybrid_schedule` seam**, not an optimisation. [OPEN-DECISION #20.]
8. **G8 · Norm interaction + Form A quarantine.** Our `TransformerBlock` is **pre-norm**
   (`transformer.h:139-142`); MoDA (`2603.15619`) reports depth attention *"pairs better with
   post-norm than pre-norm"* — a concrete, checkable Phase-0 risk, not an assumption.
   Form A (rectified/unnormalised gate, Softpick lineage) breaks V10's normaliser and changes
   downstream training dynamics: **experimental flag only**, with its own gradient check (V19).

**S — the structure (design statements S1…S6):**

1. **S1 · Bounded is state of the art.** ARLoop (`2611.05234`): **sliding-window depth attention
   matches or outperforms full-history** at larger recurrent depths. So `S` = a **bounded,
   sliding, persistent index**: the active window stays hot, older state moves **into the
   `.idx`-backed store**. "Never forgets anything" is satisfied by *eviction into* `S`, never
   by deletion — the §3.2 wording holds.
2. **S2 · Two axes in one index.** `S` holds **sequence history and depth history**
   (MoDA, `2603.15619`: depth-KV entries from earlier layers alongside sequence entries). The
   depth entries carry the **deltas** (G5).
3. **S3 · Position-independence constraint.** The index is **not position-ordered** (§5c.2
   Form B requirement) — keying `S` by position would re-introduce the position bias `G`
   exists to kill.
4. **S4 · KV-cache policy, stated.** Naive = `T` separate KV sets per position; **shared-KV**
   (`2610.33360`) cuts persistent cache sets **15 → 4** and removes **81–89%** of the
   continuation-loss penalty (parallel pass supplies cache entries, continuation reads
   recursively, **consistency loss in the final 10%** of the token budget). At the 1.0/1.5-BPW
   × 4M-window budget this is first-order memory. [**OPEN-DECISION #22**; recommendation:
   shared-KV.]
5. **S5 · Loop-entry identity path.** `2609.30820`: per-channel INT4 fails **first at the
   non-residual loop-entry adapter** — quantised perturbation without an identity path feeds
   back through later steps. Our looped entry seam gets an **identity path**, and any PTQ on
   looped blocks accumulates GPTQ Hessians over **all** recurrence steps.
6. **S6 · Quantisation-first discipline.** `G` is a normalisation over an attention row —
   OASIS (`2605.17887`) shows an extra depth-wise normalisation channel **amplifies sinks,
   outliers and low-bit error**. Therefore `G` goes **inside the quantisation test set from
   day one**, at **every** wire BPW on the ladder — the **1.0-BPW side goal included**, and
   both **FP and INT** format families (D-27). [**OPEN-DECISION #14**; recommendation: yes.]

**Forks this note deliberately leaves open** (each carries its ledger id — the operator stamps):
#12 confirm B+C composite (recommend: yes) · #13 single-stream vs multi-stream + routing-key
dimensionality · #6 learned gate vs post-hoc readout · #16 adopt Loop-µP `×1/N` · #21 residual
interface: Loop-µP scaling vs Loopback per-block-update · #22 KV policy · #17 default loop
ladder (recommend: T = 2, measure to 4) · #14 `G` in the quant set (recommend: day one) ·
#11 weight-tied dead-zone measurement (OPEN-UNKNOWN) · #20 work-shrinking routing seam.

---

## 5d. LOOP vs TRADITIONAL — the two transformer types: attention, and training (verified 2026-11-10)

> **The framing (user, 2026-11-09, restated 2026-11-10):** there are exactly **two kinds of transformer** here — **traditional** and **loop**; **the whole game is attention**; and the topic is **training**. An earlier pass of this section drifted to quantisation; that material is demoted to **§5f (deployment)** and the spine below is loop-vs-traditional → attention → training. **Every arXiv ID below was read from a live arXiv API response on 2026-11-10 — none from memory.**

### 5d.0 The taxonomy — three loop shapes, one idea

A **traditional** transformer uses each layer's parameters **once**; depth = (parameter count) / (per-layer parameters). A **looped** transformer (also *recurrent-depth*, *depth-sharing*, *weight-tied*) applies **the same parameters repeatedly**, so **effective depth = stored layers × loops** while the parameter count is unchanged. The taxonomy of the corpus has **three loop shapes**:

| Shape | What repeats | Who |
|---|---|---|
| **model-loop** | the **whole stack** is traversed, then repeated | the survey's baseline; Loopie calls this *"the traditional whole-model recurrence pattern"* |
| **block-loop** | only the **middle segment** repeats, with **input injection** | **SMELT** (`2609.01343`) loops the **middle half** of the layers twice |
| **layer-loop** | each **Attention/MoE layer** is applied recurrently *before* passing its output to the next layer | **Loopie** (`2607.16051`) — its choice |

**GPT-6 "Astra" is model-loop**: 22 blocks applied twice ⇒ effective depth 44, where block-application 23 uses block-1's weights, 24 uses block-2's, and so on.

**A second, complementary taxonomy** (`2604.17121`) cuts by **recurrence axis** instead of granularity: **depth** (the looped transformer — our whole subject) vs **step** (block-recurrent transformers, linear attention, DeltaNet, Mamba, RWKV), and by the ratio of input tokens per recurrence step. **Our §3.2 sequence-axis work (Softpick, the LITM theory) sits on the `step` side, not the `depth` side** — an independent reason the two must not be conflated.

**Loopie's "Loopie Recipe"** is the framing we want: *rather than treating loops as a direct substitute for additional parameters, **jointly choose stored width, stored depth and recurrent depth** so the model maximises performance under a **fixed pre-training compute budget**.*

### 5d.1 What actually changes when you loop — and what does NOT

**What does NOT change (this is the load-bearing point):**

- **The sequence-axis attention.** Loopie's backbone is Qwen3-MoE and *"its attention mechanism, sparsity pattern, and other architectural details **remain the same** as those of the Qwen3-MoE family."* **The strongest open looped model does not change attention at all** — it changes the **schedule**. So "the whole game is attention" is right in the sense that **attention is where the quality comes from — but the loop buys depth, not a new attention.**
- The training objective stays the standard autoregressive LM loss.

**What DOES change:**

1. **Parameters vs compute.** Parameters and optimiser state stay **flat**; compute scales with the loop count; activation memory grows **linearly** with it unless backprop is truncated. Backprop runs through *every* application, so **training a looped model costs about the same as an untied model of the same executed depth** — you save *parameters*, not *FLOPs*.
2. **The KV cache grows per stack.** Because the hidden states entering the second pass differ, the resulting **keys and values differ too** — a looped model with `T` passes keeps **`T` separate KV sets for the same token positions**. (At 1.5 BPW and a 4M window this is a first-order memory fact, not a footnote.)
   - **But that blow-up is not inevitable.** **LSTM-Style Looped Transformers with Shared KV Caches (`2610.33360`)** shares **one** KV cache across the recurrent core: at width 1024 it uses **40.4% fewer parameters** than an untied control at nearly matched forward FLOPs, and **reduces persistent cache sets from fifteen to four**. Parallel training supplies cache entries from a standard-attention pass while continuation reads entries produced recursively; aligning the two passes with a **consistency loss during the final 10%** of the token budget removes **81–89%** of the continuation-loss penalty, replicated on disjoint documents across two seeds. → **"`T` separate KV sets" is the naive choice, not the only one — this directly changes the Phase-1 memory budget.**
3. **The forward pass becomes a discrete dynamical system.** *"Its stability is not guaranteed"* — this is the single biggest difference, and it is a **training** problem (§5d.3), not an architecture problem.
4. **The residual stream grows linearly in the loop count, not √L.** At initialisation, *distinct* layers add nearly **uncorrelated** increments (sum ~ √L), whereas a **shared** layer adds **positively correlated** increments at every loop (sum ~ **N**, linear). Our `TransformerBlock` is **pre-norm**, and our §5 routing **weight-ties layers** — so this applies to us directly. (`2606.18524`, §5d.3.4.)
5. **Input injection becomes a design axis.** `h_{t+1} = F_θ(h_t, x, e_t)`, where `e_t` may encode **the loop index**, **a halting state**, or **an injected copy of the input**.

### 5d.2 ATTENTION — the crux, on three axes

**Axis 1 — the sequence axis (token attends to token).** **Unchanged by looping.** This is where our §3.2 `QKᵀ·G(GS)` lives, and where Softpick (`2504.20966`), the attention-sink work (`2410.10781`) and the lost-in-the-middle theory (`2603.10123`, `2605.09213`, `2607.17696`) apply unchanged. **Looping buys us no exemption from any of it** — and §5c.2's **Form B (index-selected, `log m` normalisation) + Form C (depth correction)** is unaffected by looping.

**Axis 2 — the depth axis (a layer attends to *previous depths*).** **This is the one place where looping genuinely changes attention**, and it is where the 2026 attention literature concentrates:

- **PreNorm gives only fixed unit-weight accumulation** of every layer output into one residual stream — no way to choose *which* earlier depth to reuse. (This is the motivation of `2603.15031`.)
- **Attention Residuals (`2603.15031`)** replace it with **softmax attention over preceding layer outputs** — learned, input-dependent depth selection.
- **ARLoop (`2611.05234`)** puts AttnRes inside a loop and finds **sliding-window depth attention matches or outperforms full-history depth attention at larger recurrent depths** ⇒ a **bounded depth index is the state of the art, not a compromise.**
- The family: **DAR** `2607.18730` (historical retrieval × multi-stream), **MSAR** `2610.13630` (multi-head depth attention), **MHAR** `2607.27230` (per-subspace routing query; cost grows with width), **LR-AttnRes** `2607.09694` (**r-dimensional routing keys** — the only variant whose routing cost is decoupled from hidden width `d`), **Delta AttnRes** `2605.18855` (**routing collapse**: weights go low-contrast and near-uniform, max ≈ 0.2, at depth), **OASIS** `2605.17887` (attention sinks, outliers and **low-bit quantisation error** amplified by the extra depth-wise normalisation channel).
- **This is our `G`/`S` mechanism.** Detail in **§5e**.

**Axis 3 — how much attention is computed.** Token-level depth policies change the attention **workload**, not just the depth:

- **Mixture-of-Recursions**: the router assigns a different recursion depth per token; inactive tokens skip deeper recursions, so **attention computation and KV caching at deeper recursions are restricted to the active tokens**.
- **T-LoopFormer (`2609.15160`)**: token-level elastic depth + a **recursion-wise KV cache**.
- **TaH (`2609.35748`)**: extra iterations **only to the tokens that benefit**.
- **FlashLoop (`2609.29812`)**: token-sparse updates + **KV-residual quantisation**.
- **This is the direct precedent for our §5 routing.** Our `HybridAttnKind` / `build_hybrid_schedule` seam is exactly this shape: a per-token depth that **must also shrink the attention and KV work**.

### 5d.3 TRAINING — the topic

**5d.3.1 The three ways training differs from a standard Transformer** (survey `202610.1404` — **preprints.org, NOT arXiv**: Azizi, Baghaei Potraghloo & Pedram (USC), *Looped Language Models: A Survey and Meta-Analysis of Recurrent-Depth Transformers*, DOI `10.20944/preprints202610.1404.v1`, snapshot 2026-10-06; 557 papers, 1211-claim ledger; repo `github.com/ArminAzizi98/looped-lm-survey`):

1. **The same parameters receive gradients from every iteration**, so updates are **correlated across depth**.
2. **The forward pass is a discrete dynamical system** and *"its stability is not guaranteed."*
3. **A loop-count policy must often be learned together with the model.** The policy `π` sets the iteration count `T` **globally, per sequence, or per token**.

**The survey's own risk triad** names the three failure modes explicitly: *"exit-gate collapse that **does not show in the loss**, residual growth from tied updates, and norm drift beyond the training horizon."* **All three are ours**: §5d.3.2 (the collapse), §5d.3.4 (residual growth), and — new — **norm drift**, which is the failure mode that bites at *inference* time when `T` exceeds the trained `T`. **Monitoring rule for us: the LM loss and the training loss surface none of the three.**

**Loop-count policy and depth sampling.** *Sampling the iteration count during training makes the model robust to the inference depth, and **useful depth saturates at the mean training depth**.* Three regimes: **fixed-depth** (`L_train = L_test`); **test-time scaling** (train on one depth or a range, raise the recurrence at inference); **learned/adaptive** (exit gates).

**5d.3.2 Exit gates — and the collapse that hides in plain sight.**

- **Ouro (`2510.25741`)**: gate `λ_t(x) = σ(Gate(F^(t)(x)))` — a learned linear projection plus a sigmoid on the current hidden state. **Stage I** optimises an **entropy-regularised objective with a uniform prior over exit steps** so all recurrent depths are explored unbiased; the exit distribution *widens* coverage of the optimal step. **Stage II** trains **only the gates**, sharpening toward the optimal exit step with a soft cross-entropy on an **improvement-vs-compute** signal (the **"Ponder" gate**, which is best at every compute budget). **Inference: the Q-exit rule** — exit when the CDF of the exit distribution crosses a threshold `q`; **`q` is a deployment knob that trades compute for accuracy with no retraining.** Ouro's sequence length also progresses **4K → 4K → 16K → 64K → 32K** across its five stages.
- **The collapse.** With a small entropy coefficient and **no warmup**, `p(exit at step 1)` *"stays at p₀ = 1.00 for all 2,267 steps of the run"* — the later iterations stop receiving gradient and **the model silently trains as a plain transformer, with no visible sign in the language-modelling loss.** **An LR warmup removes the early collapse, and a larger KL coefficient lets the gate recover.** → **Operational rule: monitor the exit distribution directly; the loss will not show this.**
- **Loss smoothing** (`2610.00673`): under `L_LM = Σ_t p_t L_t`, a step the gate abandons receives no gradient and its loss drifts. Smooth **only the exit distribution used for the loss**: `L_LM^smooth = (1-ε)·Σ_t p_t L_t + (ε/T)·Σ_t L_t`. With **ε = 0.05, T = 3**, every step retains at least **0.0167** of the LM weight, preventing the later-step losses from drifting.

**5d.3.3 Curriculum over loop count.**

- **Depth schedule**: `L_max(s) = min(L_target, L₀ + k·s)`.
- **Correctness-directed online depth mask** (`2610.00673`): run the maximum active number of recurrent steps and compare the **top-1 prediction at every step** with the target token; if **no** step predicts the target correctly, assign the token to the **final active step**; treat the discrete mask as a **stop-gradient routing decision**. **The maximum active depth is increased one step at a time** — step 2 is introduced in the second half of training, *after* step 1 has learned a useful refinement. This combines TaH's correctness-directed supervision with **more than two** recurrent steps while avoiding the intermediate-step collapse that makes a fully dynamic oracle unstable.
- **Truncated backprop through the last iterations** makes deep recurrence affordable (ICLR 2024: a **truncated loss window** that shifts `[1, T] → [b−T, b]` with `b` progressively increased; a lower `T` may compromise performance, a larger `T` *"could induce instability in training"* — per the recurrent-model training literature).
- **Retrofitted recurrence** (McLeish 2025): a curriculum that slowly raises the mean recurrence **beats post-training the original on math at equal compute**.
- **Stochastic stopping** (`2606.29983`): sample one stopping time `τ`, supervise the model **only at the realised depth**, and train the stopping rule with the reward `R(x,y,τ) = −ℓ(θ;x,y,τ)`. This replaces a single-depth gradient with **an average over nearby depths** — *"randomisation changes the expected gradient from a single-depth gradient to an average over nearby loop depths"* — which **sharply reduces OOD variance** and stabilises predictions across inference-time loop counts.

**5d.3.4 Stability — Loop-µP (`2606.18524`) — the single most directly applicable result for us.**

- Depth-µP multiplies each residual branch by `L^(−1/2)` so that an LR tuned on a shallow untied network transfers to a deep one.
- **Loops cannot simply be treated as extra depth, because the loops share weights.** Distinct layers add nearly uncorrelated increments (sum ~ √L); a shared layer adds **positively correlated** increments at every loop (sum ~ **N**, linear).
- For a single layer looped `N` times, in the infinite-width limit, **multiplying the residual branch by `1/N` and keeping the learning rate independent of `N`** is the **only** parameterisation with **both** a stable forward pass **and** maximal residual-stream updates.
- **Loop-µP** = loop factor `1/N` × depth factor `L^(−1/2)`: **residual branch × `1/(N√L)`**, Adam **LR factor `1/√L` with no factor of `N`**. Empirically, the base LR tuned on the smallest model stays best for **loop counts up to 8 and executed depths up to 384 layers**.
- **Consequence for Transformers-Fusion:** our `TransformerBlock` is pre-norm and §5's routing **weight-ties layers**, so **our residual stream will grow linearly in the loop count** — exactly the failure Loop-µP fixes. **Phase-0 action: add the `1/N` residual scaling on the looped path and assert the residual-stream norm is flat across loop counts.** This is a cheap, concrete experiment with a published reference result.
- **The alternative fix is a different residual *interface*, not a different scaling law.** **Loopback Transformer (`2611.07226`)** shows that a full block output **contains both its input and its new update**, so weighting that output also reweights the history already carried by the input. Reading the **individual update** instead — keeping the shared stack's input on a separate path — gives **separate controls over input strength, total update weight, and allocation across updates**: **geometric decay** sets the total update weight and supplies a recency prior, **attention** learns how to allocate it. Loopback reaches lower validation loss than standard Transformer baselines with **40–75% of their Transformer parameters** (191M–3B, ClimbMix). **Two caveats, read before adopting:** *"extra visits have not improved validation loss"*, and Hyperloop's advantage **did not persist** after switching to GPT-2-style initialisation and retuning learning rates — so a residual-interface change must be **re-tuned**, not dropped in. **For us this is the concrete alternative to Loop-µP's `1/N`, and it is the same shape as our §5e `G`/`S` idea (attention over prior depths).**
- **The instability has two named sources** (`2605.18797`, Fully Looped Transformer): **gradient oscillation** and **residual explosion**. Its two *parameter-free* fixes — distribute inter-loop signals across all layers, and **attention injection** — make training stable to **12 loops**. **Our `1/N` residual scaling addresses the second; nothing in our plan yet addresses the first (gradient oscillation), so it must be measured rather than assumed.**
- **Stability now has a usable theory.** `2604.15259` frames looped architectures along three axes — **local attractivity, input-dependence, geometry** — and proves that looped networks **without recall** have countable fixed points and **cannot achieve strong input-dependence at any spectral regime**, while **recall with outer normalization** reliably produces a regime where the fixed point is simultaneously **locally attractive, locally smooth in the input, and supported by stable backpropagation**. → **Design implication: without a mechanism to re-read earlier depths, our looped model cannot become input-dependent in the fixed point.** That is a direct argument for keeping §5e's depth attention (`G`/`S`) as **core**, not optional.
- The rest of the stability checklist (from the corpus): depth curricula, **gradient clipping**, **conservative learning rates** and **activation-norm monitoring** all matter **more** in looped models than in ordinary ones; the residual update must be **small enough to avoid explosion**; normalisation must keep **hidden-state statistics consistent across loops**; **input injection must be bounded**.

**5d.3.5 Two ways to generalise past the training horizon (`2609.33144`) — a taxonomy of *recurrence-training schemes*.**

| | **MR-Loop** (Matched-Recurrence) | **DR-Loop** (Decoupled-Recurrence) |
|---|---|---|
| Recurrence depth vs length | **matched**: loss after `T = n` passes | **sampled independently of input length** |
| Where the intermediate state lives | a **fixed readout position** | an **advancing computational frontier** |
| Mechanism | adjacent-token interactions + a **transferable progress cue** advance relation selection | intermediate states propagate through the frontier |

Both achieve length generalisation, **by distinct mechanisms**, and the analysis concludes the model *"learns an **iterative attention mechanism** that extends beyond the positions encountered during training."* **When does recurrence actually become an algorithm?** `2607.20594` gives a **budget law**: free training installs a linear computation frontier that solves `v` positions per loop, with **`v ~ n_train / T_train`** (exponent 0.98 ± 0.04, R² = 0.99). **Weight tying is what flips the selection to the serial frontier** — at matched depth and parameters, untied models extrapolate worst and fail to learn A5 at all. The implied halting rule is **`T* = ceil(n / v̂)`**. → **This is the cleanest statement of what looping buys us: it buys a serial, position-advancing frontier — and it costs us extrapolation.**

**This is the loop analogue of our §5c.1 problem: a learning-dynamics problem, not an architecture problem.** Also `2604.07822` — depth recurrence enables **implicit reasoning** (no emitted intermediate tokens), effective rolled-out depth `D = L × R`, and **training requires a stopping strategy**.

**5d.3.6 The recipes that actually work — the answer to "what do we do".**

| Recipe | What it does |
|---|---|
| **Closing the Loop** (`2610.00673`) | **Two** stages instead of Ouro's five: **210B-token pretraining + 100B high-quality mid-training**. **T = 4 from the start** — their own T=8 run showed the **per-loop loss stops improving after loop 3–4** and the gate spreads mass over loops 4–8, so *"the extra iterations cost compute without measurable gain."* **LR warmup** prevents early exit-gate collapse; **β = 0.15** allows recovery; **smoothed exit loss (ε = 0.05)**; the **online correctness-directed depth curriculum**. **A 1.4B looped model beats a parameter-matched dense baseline on all 12 benchmarks, and from-scratch training is cut from 7.7T → 310B tokens.** |
| **Ouro** (`2510.25741`) | Five stages: pretrain **T=8** → continued pretrain **T=4** (loss spikes at T=8) → high-quality annealing → context extension → supervised mid-training. Entropy-regularised gates + a focused gate-training stage; **Q-exit** at inference. |
| **Loop-µP** (`2606.18524`) | Residual **× 1/N**, LR independent of N ⇒ **hyperparameters stop needing re-search for every loop count**; the LR transfers up to **8 loops / 384 executed layers**. |
| **Stochastic stopping** (`2606.29983`) | Sample `τ`, supervise at `τ`, reward = −loss ⇒ **averaging the gradient over nearby depths**; stabilises OOD and inference-time loop counts. |
| **SMELT** (`2609.01343`) | MoE + **middle half looped ×2**; matches **FLOPs + parameters + KV** simultaneously; saves **6.8–18%** of training FLOPs; holds to 54B. |
| **Loopie** (`2607.16051`) | **layer-loop**; the **Loopie Recipe** (stored width / stored depth / recurrent depth chosen jointly under a fixed compute budget); `h_{t+1} = F_θ(h_t, x, e_t)`. |

### 5d.4 Cost and quality — the market scan (verified 2026-11-10)

**The compute-matching gate has been crossed, and recently.** For years the objection to looping was that, at a fixed FLOP budget, spending on *parameters* beats spending on *depth*. Two 2026 results removed that objection:

| Model | arXiv | Org | Params | Tokens | Loops | Headline |
|---|---|---|---|---|---|---|
| **SMELT** | `2609.01343` | ByteDance Seed + Tsinghua + M-A-P | to 54B non-emb | — | **middle half of the layers, looped ×2** | Matches the unlooped baseline on **FLOPs, parameters and KV cache simultaneously**; saves **6.8–18%** of training FLOPs; the advantage **does not vanish with scale** |
| **Loopie** | `2607.16051` | IQuest Lab / Ubiquant | 20B-A2B / 6B-A0.6B (MoE) | 800B | 2 | *"the most powerful open-source looped Transformer to date"*; substantially beats a reproduced vanilla **Qwen3-30B-A3B** |
| **ARLoop** | `2611.05234` | open (code + checkpoints released) | 0.6B / 1.2B | 0.5T | 3 | **1.2B beats Huginn-3.5B on all 8 benchmarks**, competitive with **Qwen3.5-2B** on a fraction of the data |
| **Ouro** | `2510.25741` | ByteDance Seed | 1.4B / 2.6B | 7.7T | 4 | first industrial-scale open LoopLM; 2.6B matches up-to-12B dense models on reasoning |
| **Huginn-0125** | `2502.05171` | UMD / ELLIS Tübingen / LLNL | 3.5B dense | 0.8T | r̄=32 (random at train, free at test) | first open billion-scale recurrent-depth LM; the checkpoint most analysis papers use |
| **RLT** | `2610.07591` | Princeton + UPenn | — | — | — | recurrent looped transformer; **gated merge** of the previous token's final state into the next input, at fixed per-token cost |
| **Loopback** | `2611.07226` | Princeton / UCLA / MIT | 191M–3B | — | — | residual **interface** redesign — read the **per-block update**, not the full output, with geometric decay + attention allocation; **40–75% of Transformer parameters**; caveat: extra visits did not improve validation loss |

**Five open looped-model families** now exist — Huginn, Ouro, LoopCoder-v2 (7B, 18T tokens, 2 loops), Loopie, Nanbeige4.2-3B (28T tokens, **shipped as a product**). LoopFormer (elastic-depth, budget-conditioned reasoning) is in the **ICLR 2026 proceedings**.

**Three numbers that sharpen the claim** (all from the survey's meta-analysis, verified 2026-11-10):

- **Matched parameters vs matched inference compute are different claims.** *"At matched parameters, a looped model beats its dense counterpart. At matched inference compute, it **ties on math and trails on knowledge benchmarks**."* → **looping is a parameter-efficiency win, not a universal compute win — and the loss shows up in *knowledge*, not math.** Our §9 benchmark set must include a knowledge axis, not only reasoning.
- **Out-of-distribution behaviour is measurably worse.** *"Across seeds, looped Transformers show out-of-distribution standard deviations of **0.087–0.122**, against at most **0.009** for fixed-depth"* — roughly **10× worse OOD spread**. This is a **gate**, not a footnote.
- **Retrofitting may be far cheaper than pretraining.** *"Converting a dense checkpoint can cost as little as about **0.5% of its pretraining compute**, and it requires **anchoring each iteration to the input**."* → a Phase-0 fallback path if a from-scratch looped run is too expensive: convert a dense checkpoint and anchor each iteration to the input.
- **Stability is not solved at our scale.** *"Each risk has a fix, but **no fix has been validated above a few billion parameters**."* Our 4B target sits **above** that ceiling — **UNKNOWN at our scale**.

**The cost answer, stated plainly.** Looped transformers reach comparable quality at **50–90% less compute** (reported). But *"it's **not necessarily faster to train or run**"* — parameters and memory stay flat while **compute multiplies per loop**. Two sharper numbers from the corpus:

- **Under a fixed pre-training budget the answer is 2**: *"each extra loop multiplies training FLOPs and the marginal return **decays fastest after R = 2**"*.
- **With variable inference compute the answer is "as needed, adaptively"**: Huginn's ARC-C saturates at **8 loops zero-shot** and **32 loops with 25–50 shots**.

Stability ceilings in the literature: **Fully Looped Transformer trains stably to 12 loops; LoopMTP to 15.**

**The honest caveat:** both compute-matching wins need the **same** configuration — **MoE backbone + per-layer or mid-stack looping + exactly two loops**. Our §5 routing is a **dense** plan, and the published compute-matching evidence is **MoE-only**. This is a caveat, not a blocker.

### 5d.5 What this means for Transformers-Fusion — the actionable list

1. **Adopt the Loop-µP residual scaling on the looped path** — residual **× 1/N**, LR independent of N. Cheapest concrete Phase-0 experiment with a published reference (LR transfers to 8 loops / 384 executed layers). **Add a V-gate: residual-stream norm flat across loop counts.**
2. **Default `T = 2`, measure up to 4.** Two independent sources: Ouro's T=8 loss spikes, and `2610.00673`'s own T=8 run showing no gain past loop 3–4. The two compute-matching wins use exactly **2**. Ship a ladder 2 → 4 with the fixed-depth baseline at **T = 2** (not an arbitrary baseline — §5c.3's "fixed-repeat baseline" must be the marginal-return knee).
3. **Implement the exit gate properly, and monitor it directly.** `λ_t(x) = σ(Gate(F^(t)(x)))` + **Q-exit** at inference (a deployment knob, no retraining) + **LR warmup** and **β ≥ 0.10** to prevent the step-1 collapse + **smoothed exit loss (ε = 0.05)**. **The LM loss will not show the collapse — assert on the exit distribution itself.**
4. **Use the correctness-directed online depth mask** as our curriculum: one-step-at-a-time increase of the maximum active depth, stop-gradient routing. It is the only curriculum in the corpus that supports **more than two** steps without the intermediate-step collapse.
5. **Our §5 routing *is* a token-level depth policy** — so the loop-count policy `π` must be **per-token**, and per the Mixture-of-Recursions / T-LoopFormer precedent the routing decision must **also shrink the attention and KV work** (inactive tokens skip deeper recursions ⇒ no attention, no KV for them). **This is a design requirement on `HybridAttnKind` / `build_hybrid_schedule`, not an optimisation.**
6. **The depth-axis attention family (§5e) is our `G`/`S` mechanism**, and ARLoop's sliding-window result means our **bounded `S` is the state of the art**. But the **sequence-axis work (§3.2 `G`, Softpick, the LITM theory) is unchanged by looping** — looping buys depth, not attention.
7. **Budget the KV cache for `T` stacks.** `T` passes ⇒ `T` separate K/V sets per token position, because the hidden states differ per pass. At **1.5 BPW × 4M window** this is a first-order memory fact for Phase 1.
8. **Re-check the MR-Loop vs DR-Loop fork** (§5d.3.5) against our §5c.2 **Form C (depth correction)**: both mechanisms are *learning-dynamics* stories for the same architectural question, so our Phase-0 experiment should be able to distinguish them — **reproduce the step-0 U-curve on a weight-tied looped model (the §5c.2 gap-5 action) and check whether the intermediate state sits at a fixed readout (MR) or advances (DR).**


## 5e. ATTENTION RESIDUALS — the depth-axis mechanism our `G`/`S` was reaching for

> **Axis 2 of §5d.2.** The sequence-axis attention is unchanged by looping; the **depth axis** is where looping genuinely changes attention, and this family is the mechanism. Read together with §5d.

> **This is the most important new finding of the 2026-11-10 pass.** §3.2's `QKᵀ·G(GS)` gates the **sequence** axis and holds `S` as a persistent index. §5c.3 noted only in passing that *"MoDA's idea of attending to depth KV from earlier layers is a second axis for `S`"*. That axis now has a **named, verified paper family** — and it is exactly a learned, content-dependent gate over the residual/depth history. **Eight papers, all verified live on 2026-11-10.**

| Paper | arXiv | Finding |
|---|---|---|
| **Attention Residuals (AttnRes)** | `2603.15031` | Replaces PreNorm's **fixed unit-weight accumulation** of all layer outputs with **softmax attention over preceding layer outputs** — learned, input-dependent depth selection. Motivation: uniform accumulation causes **uncontrolled hidden-state growth with depth**, progressively diluting each layer's contribution. (Kimi Team, 2026.) |
| **ARLoop** | `2611.05234` | Puts AttnRes **inside a looped transformer** — each layer's input is selectively aggregated **by attention over model depth**. Key result: **sliding-window depth attention matches or outperforms full-history depth attention at larger recurrent depths**, i.e. **the index does not need to be complete**. |
| **Dual Attention Residuals (DAR)** | `2607.18730` | Combines **historical retrieval** (select across depths) with **multi-stream** residuals via reciprocal cross-stream addressing. |
| **Multi-Stream Attention Residuals (MSAR)** | `2610.13630` | Generalises depth attention to **multi-head**; stream diversity from sequence context via multi-scale causal convolutions. |
| **Multi-Head Attention Residuals (MHAR)** | `2607.27230` | A single shared depth query forces every feature subspace through one distribution, and the cost of that compromise **grows with model width**. Gives each subspace its own routing query. |
| **Low-Rank Attention Residuals (LR-AttnRes)** | `2607.09694` | Full-dimensional residual **values**, but **r-dimensional routing keys** (`r < d`) — depth-routing cost stops scaling with hidden width. |
| **Delta Attention Residuals** | `2605.18855` | **Routing collapse**: at depth, standard AttnRes attends over cumulative hidden states that are highly redundant, so weights go low-contrast and near-uniform (**max weight ≈ 0.2**). |
| **OASIS** | `2605.17887` | AttnRes' extra depth-wise normalisation channel **amplifies attention sinks, activation outliers and low-bit quantization error**. Fixes with dual-normalised Softmax1 null routes plus token-to-depth null coupling. |

**What this changes in the plan:**

1. **`G`/`S` gets a named implementation family.** "Attention over depth KV from earlier layers" — the second axis for `S` — **is** AttnRes. The plan should stop describing it as an idea and start choosing among the seven variants.
2. **The `S`-completeness question is answered in our favour.** ARLoop shows **sliding-window depth attention ≥ full-history** at larger recurrent depths. Our §3.2 requirement that `S` be *persistent but bounded* is therefore **not a compromise — it is the state of the art.** A windowed / evicting `S` is a legitimate design, not a degraded one.
3. **The form of `G` is now specified by a family, not guessed.** §5c.2 recommended **Form B (index-selected, `log m` normalisation) + Form C (depth correction)**. AttnRes *is* Form B applied on the depth axis, with Form C supplied by **Delta Attention Residuals'** redundancy/collapse analysis. The plan's recommendation was right for a reason it could not previously name.
4. **Two known failure modes, and both map onto our own gates.**
   - **Routing collapse** (`2605.18855`) → our `G` gate must assert **depth-attention contrast**, not merely output correctness. Same shape as §5c.1's insistence that V12 assert a *flat influence-density curve*, not merely accuracy.
   - **Quantisation amplification** (`2605.17887`, OASIS) → OASIS is a **known threat to the 1.5 BPW target** (§9b.1), because `G` is itself a normalisation over an attention row. Its null-routing discipline must be considered **before** `G` is frozen.
5. **Width scaling is a first-order concern for us at 1.5 BPW.** MHAR (`2607.27230`) and LR-AttnRes (`2607.09694`) both attack *depth-routing cost scaling with hidden width*. **LR-AttnRes's low-rank routing key is the variant to benchmark first** — it is the only one whose routing cost is decoupled from `d`.
6. **Multi-stream vs single-stream is a real fork.** DAR/MSAR (multi-stream) vs AttnRes/MHAR (single-stream) changes the residual topology of our `TransformerBlock`, which is **pre-norm** (`transformer.h:139-142`, §5c.3). **UNRESOLVED — pick in Phase 0.**

---

## 5f. DEPLOYING LOOPED MODELS — quantisation evidence for 1.5 BPW (supporting, verified 2026-11-10)

> **This section is supporting evidence, not the topic.** The topic is **loop vs traditional transformers, attention, and training** (§5d). Quantisation matters here for exactly one reason: §9b.1's target is **1.5 wire BPW**, and these three papers say whether *looping* makes that target harder than it already is. **The loop-specific numbers (T stacks of KV, `T`× activation memory, `1/N` residual scaling) are in §5d.1 and §5d.5.**

> §9b.1 sets the target at **1.5 wire BPW**. Softpick (`2504.20966`, §5c.1) already told us the *softmax* advantage widens at low bit precision. These three papers tell us the **other half**: what breaks when you quantise a **looped** model, and how to fix it. **All three IDs read from live arXiv API responses on 2026-11-10.**

| Paper | arXiv | Finding we use |
|---|---|---|
| **LoopQ** | `2605.16343` | Looped LMs are **specifically sensitive to PTQ** for three reasons: **distribution shift across roles**, **state reuse across loop transitions**, **recursive error accumulation**. Fix = keep a shared quantised backbone, add lightweight loop-dependent adaptations (**loop-aware activation scaling**, **selective loop-aware transformation**, **cross-loop state alignment**, **trajectory-aware calibration**) touching **< 0.12% of total parameters**. Under **W4A4**: **+68.8%** mean downstream accuracy and **−87.7%** mean perplexity vs the strongest static PTQ baseline. W4A4 memory: **−57.1% / −61.7% / −27.3% / −28.3%** on Ouro-1.4B / Ouro-2.6B / LoopFormer 3×8 / Parcae-370M. |
| **LoopQuant** | `2610.16368` | Adds what LoopQ misses: **cross-loop distribution canonicalization (CLDC)**, **interaction-aware loop-wise precision allocation (ILPA)**, **task-aligned calibration along the low-bit recursive trajectory (LCTC)**. On Ouro-2.6B, **W4A4 beats every W4A8 baseline**; **−65.3% model memory** with only **+3.4% storage overhead** over naive INT4, and a **1.7× decoding speedup vs BF16**. Defines **W4A6** = mixed loop-wise activation precision (half the loops at 4-bit, half at 8-bit). Claims to be the first **open-source** LoopLM quantisation framework. |
| **Quantizing Looped Transformers: Feedback Exposure and Calibration Blindness** | `2609.30820` | Names the mechanism precisely: on Huginn-3.5B, **per-channel INT4 fails primarily at the non-residual loop-entry adapter**, while quantising the residual core is much less damaging. **Feedback exposure** = a quantised layer perturbs the recurrent state **without an identity path**, and the error is fed back at later steps. Fix = accumulate GPTQ Hessians over **all** recurrence steps, not one. |

**Consequences for us:**

1. **1.5 BPW is not blocked by looping.** The published frontier for looped models is **W4A4**, and LoopQuant reaches a W4A4 that *beats* W4A8. Our 1.5 BPW **wire** target is a different axis from activation precision — but the message is the right one: **looping does not cost us the low-bit regime, provided we design for it.**
2. **The loop-entry adapter is a named risk.** `2609.30820` says the *non-residual* loop-entry path is where INT4 fails first. Our §5 routing has an exactly analogous seam (the entry into a looped block). **Phase-0 action: identify our loop-entry path and give it an identity path.**
3. **Quantise across the loop, not at one step.** Any PTQ we run on a looped Fusion block must accumulate Hessians over **all** recurrence steps — otherwise we reproduce `2609.30820`'s failure by accident.
4. **`G` is a normalisation over an attention row — quantisation-sensitive by construction.** OASIS (`2605.17887`) warns that an extra depth-wise normalisation channel amplifies outliers and low-bit error. **Our `G` must be inside the quantisation test set from the start**, not retrofitted.
5. **LoopQ's own limitation applies to us:** it targets **fixed-path decoding with a predetermined loop structure**. Our §5 is **adaptive** routing, so the low-bit results do **not** transfer directly. **UNKNOWN** whether adaptive-path quantisation holds the same gains.

---

## 6. Confirmed decisions

| # | Decision | Answer |
|---|---|---|
| 1 | **Routing mechanism** | **Layer re-arrangement + learned gate.** Traditional-mode layers must also work in loop mode. **Research first — mandatory gate.** |
| 2 | **Base window** | **Every model, smallest to largest, base = 4M.** The *trainer* may extend it — via code, architecture, or config; that is the trainer's choice. **On every fill, double:** 4M → 8M → 16M → … always ×2. |
| 3 | **Rebrand** | **Clean break.** Both `@origin-ai/xhe` and `.dsh` shut down, no aliases; `.dsh` auto-migrate runs **once**. Priority within the sequence is mine (§11). |
| 4 | **Dead code** | **Zero, project-wide.** Wired-in or removed — no exceptions. |
| 5 | **Research gate** | 100% research must precede any implementation. |
| 6 | **Benchmark / reference model** | **DeepSeek V4.1 Flash** (`deepseek-v4.1-flash`) — **not** Qwen-3.8-27B. Source of truth: `review-tracking/MASTER_PLAN.md` **NEW-2**. |
| 7 | **The ruler model we train** | **`sol-4-flash`** — "Sol 4 Flash" — **exact**: no `4B`/`4b` suffix or prefix in the id or the display name. 4B parameters, 1.5 BPW. **Renamed from `innova-x-1.1-4b` by user ruling, 2026-11-12** (`MASTER_PLAN.md` **NEW-3** updated in the same pass). |

> **User ruling, 2026-11-12 — model identity (NEW-2 + NEW-3). Verbatim:**
> *"Sab fix karne ka, sab kuchh add kar daalne ka, kuchh bhi bach ke jaane naa paaye."* · *"ham model me Qwen-3.8-27B nahi, DeepSeek V4.1 Flash use karenge! ... jo model train hone waala tha Innova naam ka wo Sol 5 Flash naam ka hoyega!"* — *(superseded later the same day: the exact name is **Sol 4 Flash**; see §16, "rename waves", item 5.)*
>
> - **Benchmark / reference model = `deepseek-v4.1-flash`** (DeepSeek V4.1 Flash). §1.1 and `MASTER_PLAN.md` **NEW-2** already said this, but the *machine-readable* block still carried `model.bench = qwen-3.8-27b`. **Stale — now fixed.**
> - **The ruler model we train = `sol-4-flash`** ("Sol 4 Flash" — exact name, no `4B`/`4b` suffix or prefix). Renamed from `innova-x-1.1-4b` across **all 10** plan sites, plus `review-tracking/MASTER_PLAN.md` **NEW-3** and **M2**.
> - **Both legacy strings were renamed in the 2026-11-12 wave** (user ruling: *"Sab rename hoyega!"*): `SolIDX` ← `InNovaIDX`, `tracesol` ← `traceInnovas`. **The wire-magic half was reverted on 2026-11-13 by D-30.**
>   - **`SolIDX` is not an engine `.idx` magic.** A model name is not a wire identity. The engine `.idx` reader accepts `Transformers-FusionIDX` (22 B, current) and `TransCenderIDX` (15 B, the engine's former name — "formerly known as"); `SolIDX` and `InNovaIDX` are rejected. `SolIDX` (7 B incl. NUL) is reserved and specified for **model manifests** in `transformers/docs/MODEL_MANIFEST.md`. Regression: `tests/test_sha256_corrupt.cpp` Test 8.
>   - **`tracesol`** remains the Plotly series variable (`transformers/scripts/plot_comparison_charts.py:149`), renamed from `traceInnovas`. It is cosmetic and stays. Code was touched under the explicit rename ruling; the Go gate remains closed for *feature* work.


### 6.1 Decision gates closed — the eight open Phase-0 questions (2026-11-12)

> **Why this subsection exists.** The Step-1 coverage audit (§10X) found work the plan *described* but
> never *decided*. Those are not research tasks — they are forks, and a fork nobody takes is a fork the
> build trips over three phases later. The user's instruction on 2026-11-12 was *"Sab fix kar! … Saara
> kaam complete kar, poora plan loop complete kar! Sab kar daal! Go."* — so **all eight gates are closed
> here, by best judgement, with the evidence that decided each**, and each lands in a **named,
> checkable gate**. **Every ruling is reversible by an explicit override; none of them overwrites an
> already-verified fact.**
>
> **Id namespaces (Step 5, 2026-11-12):** `GAP-n` = this plan's own Step-1 audit gaps (§10X.1).
> `OC-G-n` = **Operation Clean's** quantisation rules (`review-tracking/MASTER_PLAN.md:15-19`). Before
> today *"G-5"* meant **both** *"zero BPW violations"* **and** *"MTP is absent"*; the prefixes are now
> disjoint.

| # | Gate | Ruling | Decided by (evidence, all re-verified on disk) | Lands in |
|---|---|---|---|---|
| **D-1** | **GAP-1** — the 32× Inferno speed bar | **ADOPT as a hard V-gate.** `best_live_backend_GFLOPS / baseline >= 32.0`, measured on the **target device — AMD Radeon Vega 7 / 5600GT iGPU**. **A ratio that cannot be measured live is reported `UNMEASURABLE`, never fabricated.** | `inferno/inferno_bench.cpp:469` prints the 32× label; `:471` prints `UNMEASURABLE (CUDA offline here — 32x target not verifiable on this host)`. SPEC-INFERNO §0.2/§2/§8, Appendix C (measured reference) and R (5-step methodology, R.4 = the no-fabrication rule). | §7 proof target **#8** + gate **V30** |
| **D-2** | **GAP-2** — backend count + fail-loud contract | **ADOPT the 24-backend contract.** Every `BackendType` gets one explicit `case` in `src/backend/backend.cpp`; an **unknown enum throws**; **never a silent CPU fallback while reporting GPU GFLOPS** (Appendix P.1). **Also settle the count confusion:** `src/backend/` has **20 files** and the `BackendType` enum has **24 members** — two different counts, and the plan had merged them. The *fused-attention* count is a third number: **4 of the 20 files**. | `include/quant/backend.h:9` — 24 enum members. `src/backend/backend.cpp` — 3,103 lines, `throw_unavailable` at `:86`. `src/backend/gpu_compute_vulkan.cpp:1578` is the **existing violation** of the contract (honest CPU fallback, `:1585` *"SPIR-V not implemented (REAL ONLY): CPU fallback, perf-invalid"*). §2.1b.1 (Step 2) for the 4-of-20 fused count. | §7 proof target **#9** + gate **V31** |
| **D-3** | **GAP-3** — training-engine scope | **IN SCOPE — all three libraries, one attention core.** `quant_dense` / `quant_moe` / `quant_multimodal` (112 files, 11,878 LOC) are part of the deliverable, and **the Fusion attention core must exist on the engine path too**, not only on `src/model`. **One formula, one implementation, two call sites** — the engine delegates to the same core. Add the three CMake targets in Phase 1. | `engines/trainer/` = 112 files (56 `.h` + 56 `.cpp`), 11,878 LOC — `dense/` 7,019, `moe/` 1,742, `multimodal/dense/` 2,284, `multimodal/moe/` 833. SPEC-INFERNO §0.1/§3/§4/§5/§6, Appendix G (CMake targets) and L (32 config structs). | §11 Phase 1 (three CMake targets) + gate **V8** already covers *"no traditional-attention code reachable in a training run"* — **the engine is a training run** |
| **D-4** | **GAP-4** — missed sweep sites | **RESOLVED — three sites, rows 22, 23 and the 5th backend attention (post-loop audit 2026-11-12).** (a) `engines/trainer/multimodal/dense/video.cpp:140` — `Tensor probs = softmax_rows(scores);` in the video ViT block. (b) `src/server/production_core.cpp:162` — `KVCache cache((int)cfg.num_layers, cfg.max_seq_len, cfg.num_heads, cfg.head_dim);`, the **serve-time attention-shape authority** found in Step 4. | (a) verified live. (b) verified live — §10Y.1. The §2.1a table had rows for `vision.cpp`, `projection.cpp` and `fusion_layers.cpp` but not `video.cpp`; and no row at all for the server. | §2.1a rows **22** and **23** (both Phase-0 bullets already updated) |
| **D-5** | **GAP-5** — MTP vs DSpine | **BOTH — and they are not rivals.** MTP (`engines/trainer/dense/mtp.{h,cpp}`) is a **training objective** (an auxiliary head predicting t+2..t+k to sharpen the representation); DSpine (§3c) is an **inference-time accelerator** (it changes how tokens are *proposed*). They overlap only in touching "more than one token per step". **Sequence: MTP first** (it lives inside the trainer we must build anyway and needs no extra inference machinery), **DSpine second** (it needs the trained model to draft from). They compose — MTP-trained weights are what makes DSpine's proposals cheap. | SPEC-INFERNO §4.34/§6, Appendix L.17 (`MTPConfig`, `MTPHead`, `mtp_total_loss`, `shift_labels` — all present on disk); §3c's DSpine spec (arXiv `2609.36173`, verified). | §11 Phase 6 (MTP) then **Phase 6c** (DSpine) |
| **D-6** | **GAP-6** — decisions model / RLHF | **IN SCOPE — as a head + an RL algorithm on the *same* model, not a third checkpoint.** `sol-4-flash` stays the single ruler model; the decisions/policy capability trains **on top of it** (rewards, GAE, PPO/DPO/GRPO/RLVR). **Start with outcome-verified RL (GRPO/RLVR)**, because D&CC-Bench tasks have **verifiable outcomes** while the harness's free-form tool use does not — and the GAE/PPO machinery is largely the same trainer code Phase 4 (EAIN) already needs. | SPEC-INFERNO §0.4/§6.9/§11.27, Appendix M (reward design, GAE, RLHF wiring recipe). §9's D&CC-Bench-1.0 is the gate — *"Live decisions + env learning"*. | §11 Phase 4 (EAIN) + §9 D&CC-Bench-1.0 |
| **D-7** | **GAP-7** — modality matrix (26 types) | **IN SCOPE as a coverage table, not a Phase-1 build.** (a) **The number is re-derived, never quoted**: SPEC-INFERNO itself says **25** (§5.9), **26** (§16.5) and lists **27** (§11.1–11.27) — so the **live `engines/trainer/multimodal/` tree is the authority** and Phase 0 enumerates it; the count is whatever the code has. (b) **Phase 1 scope = the modalities with a live training path today** (`dense/` + `moe/`); every other modality becomes an **explicitly tracked row with a named owner and a gate** — never a silent omission. (c) **§9 gains a modality-coverage axis**: every modality has a live eval or is marked `UNSUPPORTED` with the reason. **Zero silent gaps.** | SPEC-INFERNO §0.3/§11, Appendix E (encoder spec) and O (per-modality recipe). The 25/26/27 contradiction is **GAP-8**, verified live. | §9 (modality-coverage axis) + §11 Phase 0 (enumerate the live encoders) |
| **D-8** | **GAP-13** — Operation Clean quality gates | **CARRY ALL OF THEM.** NEW-1 industrial parity at equal BPW → **V32**. D-12 scale-fit quality floor → part of **V32**. D-13 MX quarantine → **the MX family stays quarantined** and is **not** a candidate format for the ruler model. D-14 bench honesty → **V28** (no fabricated metrics, §10Y.3). Format reachability (all **69** canonical names must parse) + D-05 casing sweep → **V33**. D-20 known test-time traps → carried into the test list. **And both quantisation tracks are in scope** (§9b.2), with the intersection — **1.5 BPW on a *looped* model** — as the project's own research contribution. | `review-tracking/MASTER_PLAN.md` NEW-1/NEW-2/NEW-3; `docs/operation-clean/DECISIONS.md` D-05/D-12/D-13/D-14/D-20/D-22; `review-tracking/DEFECTS.md` E1/E1a/E1b/Q-7/Q-12 (the measured quality gaps: MX −21..−37 dB, the 8-bit K-variants losing, `Q_1` at 3.53 dB, the higher-BPW quality inversion). | §14 gates **V28**, **V32**, **V33** |

**What is *not* decided here, and stays open on purpose.** GAP-8 (SPEC-INFERNO's own 25/26/27 and
"1024 lines" contradictions — a fact problem, resolved by re-derivation, not a fork), GAP-9 (the L4
defect — **fixed**, the sibling docs are stale), GAP-10 (69 vs 60 — **D-22 already settled it**), GAP-11
(§9b.1's own staleness — **fixed in Step 1**) and GAP-12 (§16 vs §2.1b.1 — **reconciled in Step 2**) are
**fact gaps, not decision gaps**, and were closed by the audit itself. The remaining genuinely-open
research questions live in §5c.5 and §3b.4 and are **explicitly UNKNOWN**, not silently assumed.

---

## 7. Proof targets — pass/fail gates

1. **4M tokens native context** — base for every model without exception.
2. **No compaction.** When the window fills, context does **not** compress — it **extends**.
3. **Doubling on every fill:** 4M → **8M** → 16M → … always ×2.
4. **Max output limit: 2M tokens.**
5. **The PDF test.** A **300-page** PDF and a **3000-page** PDF — the model does not forget. For any single word it states **immediately** where it is: **which line, which page number**.
6. **Permanence.** Prove it never forgets. Checked on the **4B model**, **retrained as many times as needed** until results match expectations **exactly**.
7. **Live decisions + environment learning** — verified on D&CC-Bench (§9).
8. **The 32× Inferno speed floor** — `best_live_backend_GFLOPS / baseline >= 32.0`, measured live on the target device (**AMD Radeon Vega 7 / 5600GT iGPU**). **An unmeasurable ratio is reported `UNMEASURABLE`, never fabricated** (SPEC-INFERNO Appendix R.4). Decision **D-1**, gate **V30**.
9. **Every backend fails loud** — one explicit `case BackendType::` per enum member (**24** of them) in `src/backend/backend.cpp`; an unknown enum **throws**; **no silent CPU fallback while reporting GPU GFLOPS**. Decision **D-2**, gate **V31**.

---

## 8. `.idx` index and lazy context loading

- `.idx` indexes exist so that **lazy loading works on the context**.
- Indexes may be built from **`.jsonl` / `.json`** sources.
- The index lets us match **all requirements and constraints** and return the result from the model.
- Must verify the model **can make decisions at all** — and specifically that it takes **live, immediate decisions**.

### 8.1 The index infrastructure already exists in CodeFusion — extend it, don't rebuild it

Three existing pieces are the natural hosts for `.idx`:

| Existing | What it does | How `.idx` uses it |
|---|---|---|
| **`packages/session-query/session-query-sqlite`** | The SQLite-backed **full-text** session index — `session-query` searches durable history | The `.idx` for **context** is the same shape: a searchable, lazily-consulted index over session content. `session-query`'s `blockText()` currently **excludes reasoning** (`extraction.ts:70-73`) — §10P(h) — so extending the indexed content to include reasoning is the same change. |
| **`packages/session/session-persistence-sqlite`** | SQLite durable persistence backend | The **durable store** for `.idx` rows — same read/write pattern, same `session/flush` barrier semantics. |
| **`packages/context/file-reference-local`** | A **bounded, per-agent, lazily-built, invalidated-on-mutation** workspace index (`WorkspaceFileSearch`; `maxResults` 20, `maxEntries` 10000, excluded dirs `.git`/`node_modules`; invalidated by tool-result events; released on agent disposal) | **This is the exact shape the `.idx` needs** — bounded, lazily built, invalidated when the environment changes, freed with the owner. The `.idx` is the same pattern applied to *context* instead of *files*. |

**The design is therefore:** `.idx` = a per-session, bounded, lazily-built index over context, with the same invalidation and disposal semantics as `WorkspaceFileSearch`, backed by `session-query-sqlite`'s FTS machinery, and persisted through `session-persistence-sqlite`.

**Three constraints carry over from `file-reference-local` and must be honoured:**
- **Bounded advisory index** — *"very large workspaces may omit paths after `maxEntries`"*. A bounded `.idx` must **never silently drop content the model later needs** — anything evicted must go to `S`, not vanish (§3.2, §7 target 2). This is precisely the difference between an index and a compaction.
- **Invalidation on tool-result events** — the index must be invalidated when the environment mutates.
- **No ignore-file semantics** — the local provider has no `.gitignore` support; the `.idx` builder must decide its own inclusion rules.

### 8.2 Where the `.idx` is *read* — the lazy-load call site

The engine side already has the right shape: `Attention::forward` reads the KV cache via `cache.get_all(layer_idx)` (`transformer.cpp:338`), and the long path is `flash_attention_forward` for `S_full > 64` (**:385–394**).

**The Fusion design:** `S` (the never-discarded structure, §3.2) is the `.idx`. Attention consults `S` for anything outside the active window, and the active window itself is what doubles. Because `S` is index-addressed rather than densely attended, the common case stays O(n) — which is what makes a 4M window survivable at all.

**This is why the `.idx` is not an optimisation but a correctness requirement:** without it, "never forgets anything" is impossible, because a dense 4M-token attention matrix is both infeasible to compute and exactly the context-rot failure we are removing.

---

## 9. Benchmarks

All carry **100 tasks** — **MQC-Bench excepted**. CS 1.0 and 1.1 are **both hard**; same *type* of question, **not the same questions**, **zero reuse**.

| Benchmark | Full name | Size | Purpose |
|---|---|---|---|
| **CS-Bench-1.0** | Common Sense Bench 1.0 | 100 | Common sense. |
| **CS-Bench-1.1** | Common Sense Bench 1.1 | 100 | **Much harder** — must be able to **confuse humans**. Top-100 / *"maan lo"* style: *"suppose this happened — what would you do?"*, harvested from the internet. **Zero overlap with 1.0.** |
| **D&CC-Bench-1.0** | Decision and Context Check Bench 1.0 | 100 | Model decides **live**, and is **learning from the environment**. Environment learning is an explicit checked point. |
| **MQC-Bench-1.0** | Model Quality Check Bench 1.0 | — | **Runs last.** Quality after **quantization**. Reports **score / 100** and percentage. |

**Why common sense is the real bar:** *the most powerful thing in a human is common sense; only when AI has it is it worthy of being called AGI.*

**Environment learning:** the model learns from its environment the way a human learns by living with a family and behaving accordingly. **This is what the World Model (§10C) is for.**

---

## 9b. Models to train

| Property | Value |
|---|---|---|
| Name | **`sol-4-flash`** — "Sol 4 Flash" |
| Size | 4B |
| **Bit-per-weight** | **1.5 BPW** |
| When | **After the whole engine is complete** |
| Post-training | Everything evaluated, **including a common-sense test** |
| Retraining | As many times as needed until results match **exactly** |
| Also used | dense **DeepSeek V4.1 Flash** for benchmarks |

### 9b.1 The 1.5 BPW path already exists — use it, don't invent it

**RE-BASED 2026-11-10 (gap GAP-11) — the live enum, not the old note.** `format_bpw(Format f)` at **`types.h:282`** is the **wire truth** (measured canonical spend at `n%256==0`), `format_nominal_bpw` at **`:356`** is the **name-implied** label, and `format_wire_bpw` at **`:357`** simply returns `format_bpw`.

**Formats that are exactly 1.5 wire BPW today** (re-read from disk 2026-11-10):

| Format | wire BPW | line | live? |
|---|---|---|---|
| `Format::Q_1_K_H` (**pure ternary**, OC-G-2) | **1.5f** | `types.h:295` (enum `types.h:48`) | **yes** |
| `Format::Q_1_5` | — | `types.h:124` | **no (retired id)** |
| `Format::Q_G_1_5` | — | `types.h:133` | **no (retired id)** |

**The tier rule is no longer in flux — it has LANDED.** The previous version of this section claimed `Q_1_K_L` / `Q_1_K_M` / `Q_1_K_H` "all return **1.0f**" and that the rework was *"uncommitted in-flight work"*. **Both statements were stale.** The live file has `Q_1_K_H = 12, // 1.5` and `case Format::Q_1_K_H: return 1.5f;`, the ladder count is **frozen at 69** (`types.h:147`, `docs/operation-clean/DECISIONS.md` **D-22**, 2026-11-01), and the **L4 persistence defect is fixed** — all four clamp sites now call `wire_format_valid()` / `legacy_format_id_remap()` from `include/quant/format_compat.h` (`:35`, `:46`). So:

- ~~**Phase 0 must resolve the tier rule first**~~ — **RESOLVED.** (**OC-G-1**) (**GAP-1**), (**OC-G-2**), (**OC-G-3**), and (**OC-G-5**).
- **The 1.5 BPW target lands on `Q_1_K_H`** — the ternary format — and *not* on the half-BPW names, which are **retired ids** in the 69-ladder (`docs/operation-clean/LADDER.md` retire list).
- **OC-G-5: ZERO BPW violations project-wide** — any new format used for `sol-4-flash` must be exact on the wire, and the name must match the wire (`E2a` recorded 27 name-vs-wire gaps — the "rename-the-ruler" mechanism).
- `importance_factor_ = 8.0f` in `src/trainer/reward.cpp` is **never consumed** (§4.6) — dead, and it sits in the reward path, so it must go before EAIN builds on it.

**MQC-Bench-1.0 measures quality after quantization** — so this section is the measurement target for that benchmark, and the `Q_1_K_H` rule must be settled before MQC can report a number.

### 9b.2 Both quant tracks — the ladder we have, and the loop-aware quant we still need

> **User ruling, 2026-11-10:** *"Dono type ka quant bhi denge ham!"* — **both** quantisation tracks are
> delivered. This subsection states what each one is, what each one is *not*, and the one thing
> neither of them covers. (Gap **GAP-13**.)

**Track A — the implemented ladder (Operation Clean).** A **storage / wire** contract: name == wire BPW,
(**OC-G-5**), 1.0–1.5 BPW. This is what the **ruler model
`sol-4-flash` (§9b) must actually ship**, and it is the only track with **code**. Its measured
weakness is **quality, not honesty**: the MX family is **−21..−37 dB** against same-BPW references
(**E1a**), the 8-bit K-variants lose to their plain counterparts (**E1b**), `Q_1` at 1.0 bpw scores
**3.53 dB** (**Q-12**), and there is a **quality inversion** where a higher BPW scores lower
(`Q-7`: `Q_G_12` 43.77 dB < `Q_G_8` 45.30 dB). **Track A is wire-honest but not yet quality-honest.**

**Track B — loop-aware quantisation (§5d + §5f).** A **compute** contract for the §5d **looped** model.
LoopQ (`2605.16343`) at **W4A4** reports **+68.8% accuracy and −87.7% perplexity** against the strongest
static PTQ; LoopQuant (`2610.16368`) at W4A4 beats every W4A8 baseline with **−65.3% memory** and
**1.7× decode speedup**; and `2609.30820` names the real failure mode — **feedback exposure: the
loop-entry adapter (non-residual path) fails first on INT4**. That last one is the *same seam* §5f
already flags for our own routing. **But Track B's published numbers sit at ~4 BPW**, not 1.5, and
**no looped-model fix is validated above a few billion parameters** — our 4B target is above that ceiling.

**So which is "best"? Neither dominates — they are on different axes.** Track A is the one that must
**ship first** (it is the 1.5 BPW target and it has code). Track B is the one that must be **researched
in parallel**, because it only becomes relevant when the §5d looped model lands. **The honest ranking:**

| | Track A (ladder, implemented) | Track B (loop-aware PTQ) |
|---|---|---|
| Axis | **storage / wire BPW** | **compute / activation precision** |
| Point on the curve | 1.0–1.5 BPW | ~4 BPW (W4A4) |
| Status | **69 formats live**, L4 fixed, D-22 frozen | papers only — **no implementation** |
| Main risk | quality (MX catastrophic, K-variants lose, inversions) | unvalidated above a few-B params; feedback exposure at the loop-entry seam |
| Blocks | the ruler model `sol-4-flash` | the §5d looped model |

**The gap neither track closes — and the one this project actually owns:** **1.5 BPW *on a looped* model.**
Track A is designed for a dense model; Track B's evidence is at ~4 BPW on a looped one. If §5d's looped
model is to be trained at the 1.5 BPW target (§9b.1), then **the loop-entry feedback-exposure failure
(`2609.30820`) must be solved at 1.5 BPW, not at W4A4** — and no published result covers that intersection.
**This is the single highest-value research gap in the project**, and it is where Track A and Track B
must be joined.

**Consequences for the plan:**
- The Phase-0 bullet *"Put `G` in the quantisation test set from day one"* (§5f) becomes **two** bullets:
  one for Track A (the ladder's own test set) and one for Track B (the loop-entry seam at 1.5 BPW).
- MQC-Bench (§9) must measure **both**: wire-honesty + quality on Track A, and loop-aware degradation on Track B.
- The **quality floor** decisions (D-12 scale fitting, D-13 MX quarantine, D-14 bench honesty) are
  **Track A quality gates** and must be carried here — they are gap **GAP-13**.


---

## 10. Confirmed codebase facts (read from disk)

Observed, not assumed.

**A. The attention core is `transformers/src/model/transformer.cpp:295`.** Detailed in §3.3.

**B. A *dead* `AttentionResidual` at `transformer.cpp:629`** — comment at **684**: *"(AttentionResidual below is dead but out of Wave-6 scope; see ledger gap.)"*. Under §2's dead-code rule this must be **wired in or removed**.

**C. The World Model is in the ENGINE.** `transformers/include/quant/world_model.h`, `namespace quant::agi`: `WorldState`, `Transition`, `PredictionResult`, `CounterfactualResult`, `MPCPlan`, `UncertaintyEstimate`, and `class WorldModel` with `predict`, `simulate_trajectory`, `beam_search_plan`, `model_predictive_control`, `counterfactual_analysis`, `store_state`, `retrieve_most_relevant`, `consolidate_memory`. Limits `max_transition_buffer=100000`, `max_state_memory=10000`. **Already implemented** — not greenfield. Also `src/agi/world_model.cpp`, `agi_extended.cpp`, `agi_flywheel.cpp`.

**D. The CodeFusion rebrand is ~90% ALREADY DONE — the plan must not overstate it.**
- `@origin-ai/xhe` in exactly **one file**: `packages/core/agent-loop/src/runtime-context.ts:1`
- pnpm→npm **already committed**: `packageManager: "npm@12.0.2"`, CI uses `npm ci`, commit `ef4f4428`. **No `pnpm-workspace.yaml`, no `pnpm-lock.yaml`.**
- **"You are an AI agent powered by CodeFusion."** already at `packages/core/system-prompt/src/index.ts:361`, pinned by **15 test references**
- `.dsh` in **9 files** — but 4 are `examples/acp-agent/tests/snapshots/*.jsonl` recorded fixtures (**must not be edited**). Real work: `apps/cli/src/profile-boot.ts`, `packages/util/home-paths/*`, `scripts/install-lefthook.spec.ts`, `packages/subprocess/subprocess/tests/service.spec.ts`

**E. DeepSeek branding is LARGE: 7,836 occurrences / 2,217 files.** Includes an entire package `packages/llm/llm-deepseek/` (`adapter.ts`, `translate.ts`, `types.ts`, `serialize.ts`, `README.md`, 2 test files), `.github/workflows/e2e.yml` (16), `docs/user/guide/providers.md` (6), `website/.vitepress/config.ts` (2), `examples/package.json` (6), `archive/cf-legacy/src/{mad.ts,byok.ts}` (12). **Rule: keep functionality, remove branding.** Rename target decided in design.

**F. Thinking preservation is essentially UNIMPLEMENTED** — a single hit in `packages/llm/llm-pi-ai/README.md`. Genuine build task.

**G. There is NO provider-adapter harness.** Grep across `packages/` found nothing. Must be **built from scratch** — and it is the thing that produces the 99.99% vs 3–35% gap, so it is high-value.

**H. New `engines/trainer/dense/` — 80+ files, untracked.** `callbacks`, `checkpoint`, `curriculum`, `data_augment`, `distill`, `distributed`, `ema`, `flops`, `grad_utils`, `hooks`, `init`, `lora`, `losses`, `metrics_dense`, `regularizers`, `rl_align`. **In-progress — do not clobber.** Also `engines/trainer/moe/` and `engines/trainer/multimodal/{dense,moe}`.

**I. No window-extension logic exists.** RoPE scaling (None/linear/NTK/YARN) with `rope_scaling_factor` for "4× context" is present, but **no doubling, no extension**. The 4M target is **greenfield**.

**J. Benchmark infra.** `code/` has **zero** benchmark harness — all benches in §9 are greenfield. The **snapshot/replay pattern** (`packages/test-support/acp-snapshot`, `CF_SNAPSHOT=replay|record|refresh`) is the convention to follow. `transformers/` has 13 C++ **performance** micro-benchmarks (`bench/`), not quality evals; `tools/evaluate.cpp` + `include/quant/eval.h` is the closest evaluation tool.

**K. Docs.** `code/` docs system is **mature** (word budgets, bilingual EN+ZH pairing, `verify-*` gates, Agent Notes) — see `docs/AGENTS.md`. `transformers/` docs were **deleted wholesale** (commit `9c0e480`, 232 files): README, `docs/`, CHANGELOG all gone. **Start from zero; use `code/` as the template.**

**L. Uncommitted work is large.** `code/`: **307 modified files** (npm-migration churn), 9 untracked. `transformers/`: 12 modified, **84 untracked** (L/M/H refactor + new dense trainer). **Commit hygiene is a prerequisite before architecture work** — §11 Phase 1.

**M. Open defects (`review-tracking/DEFECTS.md`)** — **7 confirmed critical + 19+ high. Full register with re-verified anchors: §10M.**


**N. `fusion-full-explore` inventory** — complete: §2.1 (sweep), §4.5–4.10 (neurons), §10O–10W (CodeFusion architecture + hard constraints + interception hooks).

---


### 10M. Confirmed defects — 7 critical + 19+ high (the defect register)

> **This is the anchor every "§10M" reference in the plan points at.** Until 2026-11-12 the plan used
> "§10M" as shorthand for *item M of the §10 list*, and `review-tracking/DEFECTS.md` has **no** section
> numbered 10M either (its sections run **A–H**). Both were dangling references — nine of them. They all
> resolve here now. **Every anchor below was re-verified against disk on 2026-11-12** (Step 3:
> `fusion/.rea-tmp/step3_verify.py`, `step3_subanchors.py`, `step3_bare_check.py`).

**Critical — 7, ordered by risk:**

| # | Defect | Site (re-verified 2026-11-12) |
|---|---|---|
| 1 | **LLM-generated C++ compiled and executed with no isolation** | `src/agi/agi_flywheel.cpp` — `sandbox_compile_and_test` :1867, compile via `std::system` :1912 (cmd built :1907 / :1909), execution via `run_with_timeout` :1437-1493 (`std::system` at :1493), model-generated code entering at :2388-2405 |
| 2 | **JIT-generated attention overflows a stack buffer** | `src/trainer/code_gen.cpp` — buffer `float scores[seq_len > 2048 ? 2048 : seq_len]` at :236; three loops `j < seq_len` at :237 / :263 / :267; writes `scores[j]` at :258 / :264 / :267; the only caller :825 passes `spec.M` **unclamped**; `tests/test_code_gen.cpp:43` only ever uses `seq_len=8` ⇒ **the overflow path is untested**. Not a capability cap — a memory-safety defect. Gate **V20**. |
| 3 | **DDP all-reduce silent no-op** | `src/trainer/ddp.cpp:154` — `ctx_.all_reduce(buf, bucket.numel);` |
| 4 | **`Math.random()` used as a verification gate** | `packages/cf/src/mad/core/god-runtime.ts:3679` — `const random = Math.random()`; :3680 — `const passed = random < basePassRate[checkDef.level]` |
| 5 | **`-march=native` ships SIGILL-prone binaries** | `cmake/compiler.cmake:40` — `add_compile_options(-O3 -DNDEBUG -march=native -D_FORTIFY_SOURCE=2)` |
| 6 | **Vacuous determinism gate** | `scripts/cross_platform_check.sh:95` — `find_artifacts "$WIN_DIR" > "$TMPDIR_WIN/artifacts.txt" 2>/dev/null` with the failure swallowed by a trailing `\|\| true` |
| 7 | **Infinite synchronous spin** | `packages/cf/src/mad/utils/advanced-memory.ts:427` — `while (this.hotContext.size >= this.config.maxHotSize) {` |

**High — the ones the plan named, plus the three it missed (Step 4, 2026-11-12):**

| Defect | Site | Note |
|---|---|---|
| Fabricated readiness gates | `packages/cf/src/mad/core/god-runtime.ts:5264` | `testsPass: true, // Would check actual test status` — and `:5266` `performanceOk: true, // Would check actual performance`, `:5267` `documented: true`. **Three** fabricated gates, not one. |
| **Unauthenticated `INADDR_ANY` listener — production server** | `src/server/production_gen.cpp:212` | **MISSED by the plan.** Zero auth references in the whole 396-line file. |
| **Unauthenticated `INADDR_ANY` listener — MoE expert-parallel RPC** | `src/model/expert_parallel.cpp:134` | **MISSED by the plan.** `TCPCommBackend::listen()` (`:124`) — the distributed-training RPC listener. |
| Unauthenticated `INADDR_ANY` listener — quant server | `tools/quant_server.cpp:150` | **The plan's original citation — confirmed correct.** No `authorization`, `Bearer`, `api_key` or `401` anywhere in the 660-line file. |
| **Fabricated quality-loss metric (NEW — Step 4)** | `src/core/telemetry.cpp:283` | `estimated_quality_loss()` returns a **hardcoded `0.001f`** (*"< 0.1% typical quality loss"*) and **it is printed** at `:321` — `"  Estimated quality loss: %.2f%%"`. A constant is presented to the user as a measurement. Gate **V28**. |
| RoPE AVX2 16-byte OOB write | `src/math/simd_math.cpp:266` | Anchor **re-verified 2026-11-12**: `:266` is the `for (; i + 4 <= half_dim; i += 4)` AVX2 loop inside `rope_avx2` (function at **:259**); the 16-byte stores are `:278-279` and `:289-290`. The precise OOB mechanism is `DEFECTS.md`'s and **was not re-derived in this pass** — it stays open. |

> **CORRECTION 2026-11-12 — the plan's `serve.cpp:118` was the wrong file, the wrong line, and the wrong
> claim.** `tools/serve.cpp:118` is `quant::ModelHTTPServer http_server(&model, args.port);` — the
> *construction*, not the bind. The bind it delegates to is **`src/server/http_server.cpp:367`**, and that
> server **does enforce bearer auth** on `/v1/*` (`:262-271` — missing header → 401 `invalid_api_key`;
> `"Bearer "` + token comparison; the `:882` comment reads *"L074: bearer auth + concurrency admission for
> /v1/""*). So *"binds `INADDR_ANY` with auth disabled"* was **wrong on the file, wrong on the line and
> wrong on the auth claim**. The three genuinely unauthenticated listeners are
> `src/server/production_gen.cpp:212`, `src/model/expert_parallel.cpp:134` and
> `tools/quant_server.cpp:150`. **Three, not one.**

---

### 10O. CodeFusion architecture — explored directly

`docs/architecture.md` read in full. This is the shape the harness work must fit.

**The framework is Cordis.** Plugins contribute **services, typed events, and reversible effects** to a shared context. *Every* part of the product is a plugin — the model adapter, the tool registry, the session log, and the **agent loop itself** — so every part is replaceable from configuration.

> *"There is no privileged core to patch: you extend cf by mounting a plugin beside the others, and registrations are effects that unwind when their plugin unloads."*

**Composition.** A running `cf` is a plugin tree built at boot from ordered layers. A **profile** is a named composition (templates: `web`, `headless`) listing its **bundles**; a **bundle** is a distribution format for Cordis config rows and the code they mount. `cf-base` is the first layer of every profile — model adapters, tools, persistence, sandbox and approval policy, settings, credentials, telemetry. Each declares itself in `package.json` under a `cf` field (`cf.profile`, `cf.bundle`). Layers apply in order: profile bundles → profile `cordis.patch.yml` → home-level → `--patch` overlay. **Any row can be replaced by a patch**, and `cf --profile web --dump-config` prints the tree the machine actually boots.

**Seams — the three-role rule.** A seam needs a **Service Definition** (interface), a **Service Provider** (implementation), and a **Consumer** (typically a model-facing tool). One role alone is not a seam. This is why one provider swap changes the whole product: filesystem and subprocess providers share one execution world, so pointing them at a remote sandbox moves Bash, PTY and LSP with them, with no provider forks.

**Turn flow (verbatim from the doc):**

```text
turn/start
  claim next-step input plus one queued message
  assemble prompt sections + tool schemas
  -> agent/pre-step                   reject | enter(messages)
     reject, or a first enter rewritten empty -> close the turn with no step
     step/start
     append entered messages as user/message
     derive model history from the log
     agent/request -> llm/stream -> assistant/chunk* -> assistant/message
     tool/call* -> tools/pre-execute -> tools/execute -> tools/post-execute -> tool/result*
     step/end
     tools owe another request, or next-step input arrived -> claim -> next step
  -> agent/turn-stopping
turn/end
```

`turn/*`, `step/*`, `user/message`, `assistant/*` and `tool/*` are **durable session events**; the rest are live extension points. `agent/pre-step`, `agent/request`, `llm/stream` and the three `tools/*` events are **waterfalls** — listeners must call `next()` to delegate.

**Session log — the invariant that governs everything we add.**

> *"The session log is the source of the context the model sees. `deriveMessages()` projects model history from it... **Model-visible means logged.** Anything that reaches a model request must be reconstructable from the log, and a runtime invariant asserts it. This is why a new model-visible input requires a new session event: extend `SessionEventMap` and render from the log."*

**Implication for this project:** any neuron state, world-model state, `S` index reference, or reasoning that we want the model to see **must become a session event**. Adding learned state = extend `SessionEventMap` + declaration merge (precedent: `packages/compaction/compaction/src/types.ts:9-69`), declared in `packages/core/session/src/known-event-types.ts:1-68`. The log is append-only with **no update verb**, so state is **last-write-wins-by-new-event**.

**Where new behavior goes** (the doc's own table, relevant rows):

| Goal | Mechanism |
|---|---|
| Add a model provider | register its adapter on `ctx.llm` |
| Add a model-facing capability | register on `ctx.tools`; schema joins prompt assembly |
| Intercept a request, tool, or turn | `agent/*` or `tools/*` event; `agent/turn-stopping` stops a turn |
| Add model-facing context | `agent.inject()` → lands in the next admitted request |
| **Add durable session state** | **extend `SessionEventMap`; render and replay from the log** |
| Manage a same-session objective | `ctx.goals` |

**Provider-adapter surfaces.** `packages/llm/` holds exactly **5** packages: `llm` (the seam + `LlmRuntime` + content/stream vocabulary), `llm-deepseek`, `llm-pi-ai`, `llm-retry` (retry policy, not an adapter), `token-meter` (measurement). Only **two production provider adapters** exist: `llm-deepseek` and `llm-pi-ai`. A test-only replay adapter lives **outside** that directory at `packages/test-support/llm-replay` (`@origin-ai/cf-llm-replay`).

| Adapter | Protocol | Reasoning carry |
|---|---|---|
| `llm-pi-ai` | pi-ai normalized multi-provider (`openai-completions`, `openai-responses`, `azure-openai-responses`, `anthropic-messages`, `bedrock-converse-stream`, + hand-declared OpenAI-compatible gateways). Map: `src/context.ts` `toPiContext`/`textOnlyContext` → `Context {systemPrompt, messages, tools}`; `src/stream.ts` `toStreamChunks` maps `thinking_start`/`thinking_delta`/`thinking_end` → `block-start`/`reasoning-delta`/`block-end` (**:148, :151, :154**). | **Signature-preserving replay** — `src/replay.ts` projects into a versioned `ReplayEnvelope` with per-block `thinkingSignature`, `redacted`, `thoughtSignature` plus response-level `api`/`provider`/`model`/`responseId`/`stopReason`. `toPiReplayState` 64-103, `foreignAssistant` 144-176, `replayedAssistant` 178-221, `toPiAssistant` 237-249. The block-**count** check is at **:183**; `:207` is the type-mismatch default. `replayedAssistant` recombines text + signatures on a later request; falls back to `foreignAssistant` on validation failure with `INVALID_REPLAY_STATE`. |
| `llm-deepseek` | Direct DeepSeek chat-completions, raw `fetch` + SSE via `eventsource-parser`, no third-party lib. Map: `src/serialize.ts` (harness `Message[]` → `WireMessage[]`), `src/translate.ts` (SSE deltas → StreamChunks). | **`reasoning_content` passback** — `serializeAssistant` (`serialize.ts:198-231`) joins every `type==='reasoning'` block's text and emits `reasoning_content` on **every** reasoning-carrying turn, not only tool-call turns. Inbound: `translate.ts:132`. Text-only. |

**Correction to an earlier premise — the greps, stated precisely:**

| Term | First-party hits | Where |
|---|---|---|
| `thinking-preservation` | **0** | — |
| `arc-agi` / `arc agi` | **0** | — |
| `scratchpad` | **1** | `code-fusion/apps/web/tests/snapshots/permission-policy-context/session.jsonl` — a snapshot fixture string (*"Route file-backed scratchpads to filesystem-context, handoff summaries to context-compression…"*) |
| `extended_thinking` | **0** first-party; **3** in `node_modules/@earendil-works/pi-ai/dist/models.d.ts.map`, `models.js`, `models.js.map` (third-party vendored dep) |
| `99.9` | **25** across 10 first-party files | |
| `99.9%` | **4** files | `.agents/notes/implemented/feature/2026-08-19-high-cache-hit-decimal-display.md:38`, `packages/client/ui-conversation/tests/chat-stats.client.spec.tsx:217`, `skills/design/horizontal-craft/anti-ai-slop.md:55`, `skills/design/horizontal-craft/data-integrity.md:141` — all incidental (a high-cache-hit display, a stats test, prose). **None refers to ARC-AGI.** |

**So the accurate claim is:** the *ARC-AGI-3 pattern* has no referent in this codebase — `arc-agi` is zero, and the `99.9%` hits are incidental. It is an **external target we are building toward**, not something to extend. The earlier sentence "and so do `arc-agi` / `99.9%`" was **false for `99.9%`** and is corrected here.

---

### 10P. Thinking preservation — precise exists / partial / absent matrix

**This is the single most valuable build in the harness.**

**IMPLEMENTED:**
- **(a)** Durable storage of `ReasoningBlock { type:'reasoning'; text }` in the append-only log (`packages/llm/llm/src/types.ts:60-62`, registered in `ContentBlockMap` `:99-104`; `reasoning-delta` is a StreamChunk variant `:315`).
- **(b)** **Verbatim replay of reasoning in every request while un-compacted** — `session.deriveMessages()` on every step; `deriveEventMessage` returns `event.data.message` unfiltered (`packages/core/session/src/surface.ts:83-107`); `agent.ts:341, 392-407`.
- **(c)** DeepSeek `reasoning_content` passback.
- **(d)** pi-ai per-block thinking/tool signatures in `replayState`.
- **(e)** Reasoning effort negotiation + UI (`ReasoningRow.tsx`, `TrajectoryTable.tsx:750-753`, `usage.reasoning` counts).

**PARTIAL:**
- **(f)** Replay state is **stripped across adapter instances / providers / models** — `LlmRuntime.forAdapter()` (`packages/llm/llm/src/index.ts:877-894`) drops `source.replayState` whenever the historical `provider` route isn't currently owned by the same adapter instance. Changing adapter/provider/model degrades that message to foreign conversion: **signatures dropped, reasoning text retained.**
- **(g)** Replay metadata is **block-count-coupled** — if `envelope.blocks.length !== message.content.length` or a type mismatches, `BlockAssembler` discards the **whole** envelope and `replayedAssistant` throws `INVALID_REPLAY_STATE` for the **whole message** (`assembler.ts:136-146`, throw at `:118`; `replay.ts:183` (block-count check)). **Any block-level edit (prune, truncate, user edit, UI rewrite) invalidates signature replay.**
- **(h)** Cross-session snapshots and the search index **exclude reasoning** — `session-reference/README.md:13` (*"excludes Shadowed pre-compaction events, tools, reasoning"*), and `packages/session-query/session-query/src/extraction.ts:70-73` `blockText()` returns `[]` for `case 'reasoning'` — **durably stored but unfindable**.

**ABSENT — the gap to build:**
- **(i)** **Reasoning in compaction checkpoints.** The summarizer projects to text-only via `summaryText()` (`compaction-basic/src/summarizer.ts:217-224`: `blocks.filter(b => b.type === 'text')`), and `README.md:16` states it: *"Only returned text enters the checkpoint, excluding reasoning and tool calls..."* A reasoning-only summarizer output is an **error** (`summarizer.ts:168-171`). Reasoning does reach the summarizer as *input* (`region.ts:498-515` `buildSummarizationInput` → `deriveEventMessage`) — **only the output is text-restricted.**
  **Mechanism correction:** `summaryText()` filters purely on **`block.type === 'text'`** — a **type** test with **no role involved**. The earlier plan said reasoning is dropped *"because the checkpoint lands as user-role text"* — **the role is not the reason.** Both conclusions (reasoning excluded; checkpoint is a `user/message`) remain independently true.
- **(j)** Reasoning indexed for retrieval (see h).
- **(k)** Any effort/summary/quality feedback loop — `reasoningEffort` is static config (`agent.ts:58, 437-453`; `call-config.ts:18-53`; rejects unsupported ids with `UNSUPPORTED_REASONING_EFFORT` **before** I/O). **No feedback loop adjusts effort from outcomes.**
- **(l)** Any world model or environment learning in the harness (see §10Q).

**The self-defeating loop worth noting:** reasoning is **priced** — `estimateContent` case `'reasoning'` charges `ceil(text.length/4) + 4` (`token-meter/src/estimate.ts:30-33 (constants at :13 and :20)`) — so reasoning-heavy turns are what *trigger* compaction, and **their own reasoning is destroyed first**.

**Highest-value single build:** intercept `compaction-basic/src/summarizer.ts:217-224` (and `region.ts:462-463`) so reasoning is retained alongside the text checkpoint, respecting the block-count-alignment constraint at `assembler.ts:136-146` — and/or add reasoning to `ctx.sessionQuery` (`extraction.ts:70-73`) so durable reasoning becomes retrievable. **Neither exists today.**

---

### 10Q. Compaction strategy (implemented) and what it destroys

**Head-anchored range selection** (`compaction-basic/src/region.ts:98-134` `selectCompactableRange`): walks the priced surface backwards accumulating tokens until `retainTokens` (= `floor(window * 0.16)`, `config.ts:20, :23`), backs off to a tool-pairing-balanced cut, and returns everything **older** than that retained tail as compactable. **Pressure threshold default `floor(window * 0.8)`**; overflow recovery bypasses retention entirely and attempts one maximal balanced head reduction.

| Layer | Behaviour |
|---|---|
| **Durable log** | **Nothing destroyed.** `cf-session` is append-only ("the append-only source of truth"); `surface` `replace` only rewrites the model-visible projection and cites `sourceEventSeqs` back to originals. **No delete / truncate / GC / rewrite API exists on Session.** |
| **Model view** | Everything older than the 16% retained tail is replaced by one text checkpoint. |
| **Recovery** | **None.** Later compactions re-summarize from the *surface*, not the log — `prepareCompaction` builds input from `selection.shadowedSeqs` (`region.ts:339, :355`), and a prior checkpoint has already shadowed them. **There is no path that reads the pre-compaction log back into a request.** After N compactions, prior reasoning is unrecoverable **for the model**. |
| **Outside compaction** | Only tool output: `packages/spill/` replaces oversized tool results with a bounded preview + locator; `compaction-tool-result-pruner` head/tail-slices only `type==='text'` blocks in `tool/result` and passes non-text (including reasoning) through untouched. **Neither touches assistant reasoning.** |

**Also false earlier:** `packages/context/` and `packages/compaction/` were described as *"unrelated capability families with no shared code"*. **That is wrong.** `packages/context/session-reference` **depends on `@origin-ai/cf-compaction`** (package.json peer + devDependencies) and imports it directly: `packages/context/session-reference/src/projection.ts:3` → `import { isCompactCheckpointSource } from '@origin-ai/cf-compaction'`, used at `projection.ts:41`. This is consistent with the plan's own §10P(h) finding that session-reference recognises `cf-compaction` source markers.

**What `packages/context/` actually is:** six context injectors — `agent-instructions` (AGENTS.md chain injection), `file-reference` + `file-reference-local` (@path grammar + local fuzzy index), `session-reference` (cross-session snapshots, reasoning-excluded), `time-context` (zoned timestamp), `tmux-context` (pane layout). **None of them participates in compaction or reasoning retention** — but `session-reference` is *aware* of compaction checkpoints.

---

### 10R. World model / environment learning in the harness — ABSENT

- **World model: `code-fusion` has NONE.** It exists only in the C++ engine (`transformers/include/quant/world_model.h`, `src/agi/world_model.cpp`, wired at `CMakeLists.txt:314`, used by `tests/test_wave7_missing.cpp:31-66`, `tests/test_agi_safety.cpp:129`). **No bridge** — `native/` is landlock-run only, `python/` is SDK only.
- **The harness has no learning loop.** The only environment feedback channel is tool results flowing into history (`agent.ts:414-421` `executeToolCalls` → `tool/result` → surface → next request). **Nothing updates weights, prompts, policies or routing from outcomes.** Skill/instruction "learning" is human-authored files discovered from disk, not learned.
- **The nearest JS analogue is dead code.** `@origin-ai/cf-mad` (`packages/cf`) — `ModelRouter.reportOutcome(modelId, {success, quality, actualLatency})` maintains running averages in an in-memory `performanceCache`, and `calculateRoutingScore` uses `historicalPerf = perf ? perf.successRate * perf.qualityScore : 0.5` (`packages/cf/src/mad/core/god-runtime.ts:2317-2354`; `updatePerformanceCache` starts at **2425**, its running-average body at 2441-2450; `reportOutcome` 2453-2457). **But it is NOT in the npm workspace** — root `workspaces` is `packages/*/*`, which does **not** match the single-level `packages/cf`; `node_modules/@origin-ai/cf` is a **stale symlink**; it appears in no bundle composition. And `AdaptiveRoutingConfig.learningRate` (`packages/cf/src/mad/types.ts:1222`) has **exactly one occurrence in the entire repo — its declaration — and is never consumed**. Nothing persists `performanceCache`. (Caveat: `packages/cf/package.json` does carry a `"cf": {"skill": true, …}` field — a **skill** declaration, not a bundle/profile mount.)
- **`packages/mad/` is seven unmounted stubs**, 1833 lines total, each a single 170-452 line `src/index.ts` whose own header says *"Minimal typed stubs"* / *"sqlite/vector index stubs"*. None contains learn/reward/weight logic. **Do not count these as an existing memory or world-model layer.**

**What must be added** (from the audit, with file anchors):
1. **A reward/success signal source and a place to score it** — compaction and `token-meter` measure *cost*, `ctx.telemetry` only records.
2. **A world-model capability family following the seam pattern** — 3 packages + a `ctx` key + a `packages/bundle/base/cordis.patch.yml` mount, per `docs/capability-seams.md` and `packages/compaction/README.md:5-8`.
3. **Durable learned state** — a new event type in `packages/core/session/src/known-event-types.ts:1-68` plus an `SessionEventMap` declaration merge (precedent: `packages/compaction/compaction/src/types.ts:9-69`). Append-only log, no update verb → last-write-wins-by-new-event.
4. **An applier** — the only in-tree candidate is the unmounted MAD `ModelRouter`, which itself needs workspace wiring and persistence.
5. **Optionally a native bridge** if the C++ `quant::agi::WorldModel` is to be reused rather than reimplemented — **this is preferable**, since §7C shows a full world model already exists engine-side.

---

### 10S. Hard constraints discovered in `cf-session` (implementation-critical)

Read from `packages/core/session/README.md`. These will silently break work that ignores them.

**1. New event types can make sessions REFUSE to load.**

> *"`ignorable?: true` — marks an event a reader may safely skip when it does not recognize the type; **absent means required, so an unknown-type event refuses session reconstruction**."*

Any event we add — neuron state, world-model state, `.idx` references — **must be marked `ignorable: true`, or every existing reader must be updated in the same change.** Otherwise a session written by the new build **will not open** under an older reader. This applies to both persistence backends and to `fork()`/replay paths.

**2. `SESSION_FORMAT_VERSION` is pinned at `0`.**

> *"`SESSION_FORMAT_VERSION` stays pinned at `0` — pre-release, no broad compatibility implied: `Session` accepts only current seed shapes, and a backend refuses any other version naming the direction... **Unknown event types refuse the same way unless marked `ignorable` in the envelope.**"*

There is **no upgrade path shipped** for older formats. So this is either pre-release-compatible (we may change shape freely, knowing we break old logs) or we must introduce versioning deliberately — **a decision Phase 3 must make explicitly**, not stumble into.

**3. The compaction checkpoint is a `user/message` replacement — not an assistant message.**

> *"`cf-compaction-basic` appends a `user/message` replacement for summary checkpoints, while `cf-compaction-tool-result-pruner` appends a content-only `tool/result` replacement."*

This matters for the thinking-preservation build (§10P). The checkpoint lands as **user-role text**, which is exactly why reasoning (assistant-role blocks) is dropped by `summaryText()`. Retaining reasoning means the checkpoint must be able to carry **assistant-role content inside a `user/message` replacement**, or a new checkpoint event type is needed — **and new event types hit constraint #1.**

**4. `replace` invalidates the KV cache — which directly opposes our no-compaction goal.**

> *"A `replace` operation invalidates reuse **from the first shadowed message** even though the underlying event log stays append-only."*
> *"A `replace` surface operation removes the shadowed entries from future inputs **without deleting their raw log records**."*

Two things follow:
- Data is **never lost in the log** — only hidden from the model. So "never forgets" is partly already true at the log layer; the failure is in the *model view*.
- **Every compaction throws away reusable prefix.** Our §7 targets (no compaction, window doubles) are not just a performance goal — they are a **KV-cache-preserving** design. The existing strategy does the exact opposite.

**5. `SessionEventMap` is the sanctioned extension point — precedent exists.**

> *"Merge-extensible via `SessionEventMap` — a plugin declaration-merges its own types (the compaction seam's `compaction/*`, bounded recovery's non-surface `llm/retry`, the hook bridges' `hook/*`); merged members appear in the same catalog. A plugin owns the relational invariant for its merged events."*

So adding events is **supported and patterned** — the risk is constraints #1 and #2, not the extension mechanism.

**6. Human transcript vs model view are deliberately different.**

> *"A human transcript must project append-origin events rather than `session.surface`, because landed replacements shadow history the reader already saw; model-facing consumers continue to read `session.surface`."*

Keep this split: it means a human can always see what the model no longer can — useful for verifying "the model forgot, but the data was there".

---

### 10T. Compaction internals — read from `compaction-basic/README.md` (critical for Phase 3)

The most important discovery: **the summarizer is a separate LLM call that deliberately replays the conversation prefix to reuse the provider's warm KV cache.**

> *"a direct one-shot `ctx.llm.stream()` call that **replays the conversation prefix to reuse the provider's KV cache** (interceptable at `llm/stream`)"*
> *"The call replays the conversation's own system prompt, tools, and shadowed-region messages verbatim, including image references, and appends the compaction instruction as the final user message, so it **reuses the provider's warm prefix cache instead of invalidating it**."*

**Consequence for our §7 goal.** Compaction is not merely lossy — it is **actively expensive** and structurally opposed to the no-compaction/doubling target:

| Effect | Where |
|---|---|
| **Every checkpoint invalidates KV reuse from the first replaced token** | *"Each checkpoint invalidates reuse from the first replaced history token; the unchanged request prefix before that range remains reusable."* |
| **Compaction itself costs a full extra LLM call** | *"This is a separate model call: the replayed conversation prefix plus the fixed instruction as input, with `maxTokens`-capped output. **Convergence retries can pay this cost more than once.**"* |
| **Reasoning is priced and then destroyed** | §10P — reasoning triggers compaction, then `summaryText()` drops it |
| **Routing the summarizer elsewhere forgoes the cache benefit** | *"Routing the summarizer to a different provider/model, or compacting a non-head range, forgoes this reuse."* |

**So each compaction cycle is: pay one extra model call → lose most prefix cache → drop all reasoning → keep only prose.** Our design replaces this whole mechanism with window extension.

**The protected hook — our insertion point, and it is designed for this:**

> *"The protected `summarize()` method is the sole subclass hook. A template- or remote-summarizer subclass can override it while pressure, retention, cited source events, shrink validation, and shadowed-token accounting stay on `ctx.tokenMeter`."*

A subclass is the **sanctioned** way to change summarization — **not** a fork of `compaction-basic`. The hook returns `{ summary, rawOutput?, llmStreamCall?, provider, model, maxTokens?, usage? }`.

**The checkpoint framing (must preserve):**

Preamble the model receives on the next request:

```markdown
This is an automatically generated checkpoint condensing an earlier span of the conversation to free up context. Treat the captured context as established background and build on it without restating it. Continue the task directly from the messages that follow, without acknowledging this checkpoint.
```

…followed by `<compacted-summary>`, the summary, `</compacted-summary>`. The raw summary also lives on the `compaction/summary` event, and **later automatic cycles merge the prior checkpoint** (the instruction explicitly says: if a `<compacted-summary>` block exists, preserve still-true facts, drop stale ones, merge newer information).

**Existing limits we must respect or explicitly supersede:**

- **`compactRegion` requires an open turn** — a manual call on a fully-closed session throws.
- **Summarization failure preserves the latest durable surface** — the auto path warns and proceeds with full over-budget history.
- **Summarization truncation at `maxTokens`** — hidden reasoning tokens can consume the cap.
- **An indivisible non-tool unit can still exceed the budget.**
- **Overflow recovery cannot shrink system/tools/prefix**, split an indivisible node, or repair a tool unit whose non-prunable remainder still exceeds the window.

**Also notable:** the injection of the compaction instruction as the final user message means the summarizer sees the conversation **including reasoning** — only the *output* is text-restricted (§10P). So a custom subclass can emit reasoning-aware checkpoints **without changing what the summarizer is shown**.

---

### 10U. CodeFusion's own agent protocol — the honesty standard this work must meet

Read from `AGENTS.md` (root). It is a **binding contract** on how claims in this project are made, and it applies to every phase below.

**Required claim format** — every assertion carries role, round, task, analysis, claims with confidence, evidence IDs with hashes, assumptions, recommendation, confidence:

```markdown
**[ROLE]** [Agent Name]
**Round**: [Current Round Number]
**Task**: [Brief task reference]
**Claims**:
- Claim 1: [statement] (Confidence: X%)
**Evidence**:
- [Evidence ID]: [Description] (Hash: xxx)
**Assumptions**:
**Recommendation**:
**Confidence**: [0-100%]
```

**The prohibitions — these are exactly the failure modes this plan's audits were built to catch:**

> ❌ **Never fabricate sources or tool outputs** · **Never claim to have seen evidence you haven't** · **Never express certainty without proof** · Never hide uncertainty behind confident language

**Verification gates before accepting any claim:** for code claims — reproducible steps, a test case, runs without errors, edge cases considered. For analysis claims — data sources cited, methodology explained, counter-arguments addressed, confidence stated. For design claims — trade-offs documented, alternatives considered, risks identified, scalability analysed.

**Production-readiness checklist** (the definition of "complete"): no critical TODOs · **no FIXMEs or HACKs in production code** · tests pass including regression · security review complete · performance acceptable · documentation updated · user workflow tested.

> This aligns exactly with §2's zero-dead-code rule — *"No FIXMEs or HACKs in production code"* is the same requirement stated in this repo's own words.

**Anti-patterns named:** echo chamber, hero complex, analysis paralysis, scope creep, **silent failure**. The [DEFECTS.md §10M](file:///c:/Users/thaku/Workspaces/fusion/review-tracking/DEFECTS.md) findings (fabricated readiness gates, `Math.random()` as a verifier, hardcoded victory claims in benches) are **direct violations of this document** — which is why fixing them is Phase 1 of the plan, not cleanup deferred to the end.

**Branding defects to fix while rebranding (§10D):** `AGENTS.md:18` says *"Also Known As: CodeFusion, CodeFusion"* (the same name twice, presumably a find-replace scar), `:20` *"Fork Origin: CodeFusion"*, and `:376` *"Fork of CodeFusion"*. Also the scope is stated as `@origin-ai/cf` (`:19`) — consistent with the target — but the package manager note in §10D stands.

---

### 10V. Where compaction is intercepted — the exact hooks for §7

Read from `docs/subsystems/compaction.md`, `packages/llm/llm/README.md`, `docs/subsystems/llm-streaming.md`.

**The seam is small and well-defined.** Compaction is **one optional capability, not part of the agent-loop spine** — so it can be disabled, replaced, or extended without touching the core loop.

**The three triggers and entry points:**

| Entry | Where it fires |
|---|---|
| `compactIfNeeded(agent, trigger, signal)` | `trigger: 'pressure'` at serial **`agent/pre-step`** (before request derivation) |
| | `trigger: 'context-overflow'` on **`agent/request-error`** (canonical provider overflow) |
| `compactNow(agent, signal)` | idle-session maintenance between turns |
| `compactRegion(...)` | explicit inclusive surface range — **requires an open turn** |

`CompactionTrigger = 'pressure' | 'context-overflow'`. **Our design must make both triggers fire less often, then eventually never** — by extending instead of compacting.

**The event vocabulary — and the key structural fact:**

Compaction extends `SessionEventMap` with **three event types**, all **log-only**: `compaction/start {turn}`, `compaction/summary {summary, rawOutput?, llmStreamCall?, shadowedRange, shadowedSeqs, shadowedTokenCount, provider, model, maxTokens?, usage?}`, `compaction/end {turn, error?}`.

> *"`SurfaceEventType` is deliberately NOT extended (only message-producing events reach the model), so the summary itself rides on a separate `user/message` with `surfaceOp: { op: 'replace', start, end }` — **the only surface mutation performed by summary compaction**."*

The lock brackets the **whole** operation: start → summarize → `compaction/summary` → `user/message` replace → end. A crash mid-operation becomes a detectable orphaned `compaction/start`, not a false `compaction/end`.

**Implication:** if window extension replaces compaction, we **stop emitting `surfaceOp: replace`** entirely. The `user/message` replacement is the *single* surface mutation — remove it and the log stays purely append-only in the model view, which is what §7's "never forgets" wants.

**Sanctioned extension points (do not fork):**

| Goal | Use |
|---|---|
| Change what a summary contains (e.g. **retain reasoning**) | Subclass `BasicCompactionEngine` and override the **protected `summarize()`** — the sole subclass hook. Pressure, retention, cited source events, shrink validation and shadowed-token accounting stay on `ctx.tokenMeter`. |
| Change compaction policy/thresholds | Config: `thresholdRatio` (default **0.8**), `retainRatio` (default **0.16**), `retainTokens`, `modelPolicies`, `auto` |
| Intercept the summarize call itself | The waterfall event **`llm/stream`** — *"Intercept/wrap every streaming model call for caching, logging, or routing"* |
| Add a new compaction/summary event field | `declare module '@origin-ai/cf-session/types'` declaration merge (same pattern as `compaction/*` itself) |
| Recognise a checkpoint | `compactCheckpointSource()` / `isCompactCheckpointSource()` from `@origin-ai/cf-compaction/checkpoint` |

**Critical primitive for §7 — `CONTEXT_WINDOW_EXCEEDED_CODE`:**

> *"the provider-neutral code both DeepSeek adapters use when a request exceeds the model context window, regardless of thrown-HTTP versus in-band finish delivery. `isContextWindowExceededError(detail)` is their shared conservative classifier."*

Today this error **triggers compaction recovery**. Under our design it must instead trigger **window extension**. This is the single most important behavioral swap in Phase 3:

```
TODAY:   provider says CONTEXT_WINDOW_EXCEEDED  → agent/request-error → compact → retry
TARGET:  provider says CONTEXT_WINDOW_EXCEEDED  → extend window ×2   → retry, same history
```

**Block-type extensibility constraint** (matters if reasoning or neuron state becomes a new block):

> *"New core blocks must land with **adapter, UI, and compaction** support."* · *"A new modality belongs in the merge-extensible map only when its **adapter, UI, compaction, and durable replay paths honor it**."* · *"**`BlockAssembler` handles core block kinds only** — a plugin-added block type whose stream is never closed by `block-end` makes `blocks()` throw."*

So adding a content block is **not** a local change — four paths must be updated together, and getting `block-end` wrong **throws**.

**Also relevant:** `GenerateOptions.purpose` already classifies auxiliary calls (compaction, session-title) so adapters can apply purpose-specific transport policy — the DeepSeek adapter sends `x-cf-compact: 1`. Any new auxiliary call (e.g. an index build, an `.idx` write) should use `purpose` rather than invent a channel.

---

### 10W. Consolidated — what exists vs what we must build

| Capability | Engine (`transformers-fusion`) | Harness (`code-fusion`) |
|---|---|---|
| **World model** | ✅ **Full** — `WorldModel`, `Transition`, MPC, beam search, counterfactual, uncertainty | ❌ **None** — no bridge either |
| **Environment learning** | ✅ Reward / prediction-error / curiosity / plasticity (module-level) | ❌ **None** — tool results into history only |
| **Provider adapter** | n/a | ✅ Two (`llm-deepseek`, `llm-pi-ai`) — but **no provider-adapter harness of the ARC-AGI-3 kind** |
| **Thinking preservation** | n/a | 🟡 **Across turns ✅ / across compaction ❌** (§10P) |
| **Traditional transformer code** | ❌ **5+ full implementations** — the sweep (§2.1) | n/a |
| **Neurons (EAIN)** | ❌ **Zero** — net-new (§4.5) | ❌ **None** |
| **`.idx` lazy context** | ❌ **None** | ❌ **None** |
| **Window doubling** | ❌ **None** (`max_seq_len = 2048`) | ❌ Compaction instead (§10Q) |
| **Benchmarks** | 🟡 13 C++ *performance* benches | ❌ **Zero** eval harness |

---

## 10X. Uncovered-source coverage map (Step 1, 2026-11-10)

> **Why this section exists.** The plan was built from the ZCode session's research, the `review-tracking/` and `code/` trees, and a code sweep of `transformers/`. **Eight source documents that hold binding work were never read by it**: `SPEC-INFERNO.md` (the training-engine spec — **0 occurrences in this plan**), `review-tracking/DEFECTS.md`, `review-tracking/MASTER_PLAN.md`, `docs/operation-clean/{PLAN,LADDER,DECISIONS,WORKING-TREE}.md`, and `transformers/PROGRESS.md`. This section is the **coverage map** for all of them: one row per source heading (117 rows, machine-checked), plus the gap list it produced. **Every fact asserted here was re-derived from disk on 2026-11-10 — none from memory.**

### 10X.0 The ruling: which document is authoritative

There are **two** master plans over this repo and they are **complementary, not competing**:

| Document | Scope | Status |
|---|---|---|
| **this file** (`~/.claude/plans/pasted-content-id-43ed-ye-aur-melodic-puddle.md`) | **architecture**: the attention core, the sweep, NCM, DSpine, neurons, routing, the harness | **authoritative for architecture** |
| `review-tracking/MASTER_PLAN.md` + `docs/operation-clean/*` (**"Operation Clean"**) | **quantisation ladder**: the 69-format wire contract, codecs, benches, parity | **authoritative for the ladder** |

**This plan is the superset in scope and must reference Operation Clean for ladder detail** — which is exactly what §9b.1 does. **The 60-vs-69 conflict is already resolved**: `docs/operation-clean/DECISIONS.md` **D-22 (2026-11-01)** froze the ladder at **69**, and this plan now cites the live enum (`types.h:146-147`). **Any future "60" claim is stale.**

### 10X.1 The gaps this audit found

> **Namespace rule (2026-11-12, Step 5) — read this before using any `G-` id.** Two different things in
> this repo used to share the `G-n` ids, and *"GAP-5"* meant **both** *"zero BPW violations"* **and**
> *"MTP is absent"*. That is fixed:
>
> | Prefix | Meaning | Defined in |
> |---|---|---|
> | **`GAP-1` … `GAP-13`** | **this plan's own Step-1 audit gaps** (the 13 rows below) | this section |
> | **`OC-G-1` … `OC-G-6`** | **Operation Clean's quantisation rules** — `Q_1` binary at 1.00, `Q_1_K_H` pure ternary at 1.50, M tier = base + 0.25, GRP families follow the same L/M/H rule, zero BPW violations, and the sixth | `review-tracking/MASTER_PLAN.md:15-19` (+ `docs/operation-clean/DECISIONS.md`) |
>
> The Operation Clean ids keep their `G-n` names in their own documents; this plan cites them as
> **`OC-G-n`** so the two can never be confused again. **No id changed meaning — only the prefix.**


**GAP-1 — The 32× Inferno speed mandate is absent from this plan.**  
The plan contains **0** occurrences of "32x", "GFLOPS" or "fail-loud". SPEC-INFERNO §0.2/§2/§8 and Appendix C/R define the project's speed bar: `best_live_backend_GFLOPS / baseline >= 32.0`, measured on the target device (AMD Radeon Vega 7 / 5600GT iGPU). **Verified live:** `inferno/inferno_bench.cpp:469` prints `"Best/CUDA ratio: %.2fx (32x target needs this >= 32 on live CUDA)"` and `:471` prints `UNMEASURABLE (CUDA offline here — 32x target not verifiable on this host)`. **This is the project's headline bar and the plan does not mention it once.**

**GAP-2 — The 24-backend fail-loud contract is absent, and the plan's backend count is wrong.**  
SPEC-INFERNO §1.6/§1.7/§9 and Appendix D/P require one explicit `case BackendType::` per backend in `src/backend/backend.cpp`, an unknown enum that **throws**, and **never** a silent CPU fallback while reporting GPU GFLOPS. **Verified live:** `include/quant/backend.h:9` declares **24** enum members; `src/backend/backend.cpp` is 3,103 lines with `throw_unavailable` at `:86`. **The plan's §2.1b says "18 of 20 GPU backends" — that count is wrong.**

**GAP-3 — The *training engine* is not represented as a scope.**  
SPEC-INFERNO §0.1/§3/§4/§5/§6 define a feature-complete training engine in three libraries (`quant_dense`, `quant_moe`, `quant_multimodal`). **Verified live:** `engines/trainer/` = **112 files (56 .h + 56 .cpp), 11,878 LOC**, in `dense/` (7,019) `moe/` (1,742) `multimodal/dense/` (2,284) `multimodal/moe/` (833). The plan mentions `engines/trainer` 13 times and covers its **attention** sites, but names **none** of the three libraries (`quant_dense` = 0 hits), no `flops_attention`, no `MTPHead`.

**GAP-4 — One attention site in the training engine is missing from the sweep.**  
`engines/trainer/multimodal/dense/video.cpp:140` — `Tensor probs = softmax_rows(scores);` in the video ViT block. §2.1a rows 12/13/14 cover `vision.cpp`, `projection.cpp` and `fusion_layers.cpp` but **not** `video.cpp`. **Verified live** (56 attention-related hits across `engines/trainer/`).

**GAP-5 — Multi-token prediction (MTP) is absent.**  
SPEC-INFERNO §4.34 / §6 / Appendix L.17 define `engines/trainer/dense/mtp.{h,cpp}` — `MTPConfig`, `MTPHead`, `mtp_total_loss`, `shift_labels`. The plan has **no** `MTPHead` and no MTP discussion; §3c's **DSpine is speculative decoding**, a different mechanism with overlapping purpose.

**GAP-6 — The decisions-model / RLHF training path is absent.**  
SPEC-INFERNO §0.4, §6.9, §11.27 and Appendix M define training a model that **outputs decisions / policy / actions** (rewards, GAE, PPO/DPO/GRPO/RLVR). The plan has 3 mentions of RLHF and **0** of "decisions model", "policy head", "GRPO" or "RLVR"; §9b lists exactly **one** model to train.

**GAP-7 — The modality matrix (26 trainable types) is absent from §9.**  
SPEC-INFERNO §0.3 / §11 and Appendix E/O define 26 modality types that must each have a live training path. The plan's §9 has three text-centric benchmarks (CS-Bench, D&CC-Bench, MQC-Bench) and no modality coverage.

**GAP-8 — SPEC-INFERNO.md's own claims are internally inconsistent.**  
**Verified live:** (a) it claims "exactly 1024 lines" (K.1, 16.9, S.6) but the file is **980 lines** / 63,238 bytes; (b) the modality count is stated three different ways — **25** (§5.9 "all 25 types"), **26** (§16.5 "26 types"), and §11 lists **27** entries (11.1–11.27); (c) §12.6 says "ctest total: 75 tests" while `tests/` now holds **76** `.cpp` test files.

**GAP-9 — The L4 "live data-corruption bug" is **FIXED** — the sibling docs are stale.**  
**Verified live:** all four clamp sites now call the new helpers instead of the old predicate — `src/codec/quant_format.cpp:460` and `:616`, `src/adapters/tools/qwen35_engine.cpp:33` and `:146` use `wire_format_valid(wire_fmt) ? … : legacy_format_id_remap(wire_fmt)`, and `include/quant/format_compat.h` exists (3,444 bytes) defining `wire_format_valid` (`:35`) and `legacy_format_id_remap` (`:46`). The old `wire_fmt < FORMAT_COUNT && wire_fmt != 19` survives **only in comments**. **So `docs/operation-clean/DECISIONS.md` D-23 and `transformers/PROGRESS.md` ("L4 NOT done") are stale.**

**GAP-10 — The ladder count conflict is already resolved — 69 wins — and two docs still say 60.**  
**Verified live:** `include/quant/types.h:146` `FORMAT_ID_SLOTS = 105`, `:147` `FORMAT_COUNT = 69`, and `kFormatValid[105]` marks exactly 69 ids live. `docs/operation-clean/DECISIONS.md` **D-22 (2026-11-01)** froze the count at **69** with six pieces of evidence. `review-tracking/MASTER_PLAN.md:29` still says **"Target format ladder (60 formats)"**, and `transformers-fusion/PROGRESS.md` still lists "60 vs 69" as an open question — **it is answered.**

**GAP-11 — This plan's own §9b.1 was stale — fixed in this step.**  
§9b.1 claimed `Q_1_K_L`/`Q_1_K_M`/`Q_1_K_H` "all return **1.0f** (`types.h:200`)" and that the K-tier rework was "uncommitted in-flight work". **Verified live:** `Q_1_K_H = 12, // 1.5` at `types.h:48` and `case Format::Q_1_K_H: return 1.5f;` at `types.h:295` — the rework **has landed** (D-22, L1). §9b.1 has been re-based on the live file in this step.

**GAP-12 — §16 contradicts §2.1b.1 on the KAT inventory — tracked to Step 2.**  
§16 says "The **KAT-layer inventory** does not exist yet — it is the single largest unknown", while §2.1b.1 is titled "KAT-layer inventory — MAPPED (read from disk)" and the Phase-0 bullet says the shape is mapped and "the remaining Phase-0 work is the *decision*, not the inventory". **§16 is the stale one; it is corrected in Step 2 together with the from-disk inventory.**

**GAP-13 — **Both quant tracks are in scope** (user, 2026-11-10: "Dono type ka quant bhi denge ham!").**  
**Track A — the implemented ladder** (Operation Clean): a *storage/wire* contract at 1.0–1.5 BPW for the dense ruler model `sol-4-flash`; OC-G-5 zero-violations. **Track B — loop-aware quantisation** (§5d/§5f): a *compute* contract for the §5d **looped** model — LoopQ (`2605.16343`, W4A4: +68.8% accuracy, −87.7% perplexity vs the strongest static PTQ), LoopQuant (`2610.16368`, W4A4 beats every W4A8 baseline, −65.3% memory, 1.7× decode speedup), and `2609.30820` naming the real failure mode — **feedback exposure: the loop-entry adapter (non-residual path) fails first on INT4**. **The gap neither track closes: 1.5 BPW *on a looped* model.** Track A is designed for a dense model; Track B's published numbers sit at ~4 BPW. That intersection is ours to solve.

### 10X.2 The coverage map — every source heading, one row each

| Source | Heading | Status | Gaps | Note |
|---|---|---|---|---|
| SPEC-INFERNO | `Executive mandate` | **partial** | **GAP-1**, **GAP-3**, **GAP-6** | §0.1 engine mandate, §0.2 the 32× floor, §0.4 the decisions-model mandate — **none of the three appear in this plan.** |
| SPEC-INFERNO | `Device specification (this host)` | **missing** | **GAP-1** | Target device = AMD Radeon Vega 7 / 5600GT iGPU; the plan names no target device at all. |
| SPEC-INFERNO | `The 32x mandate` | **missing** | **GAP-1** | The project's headline speed bar. Plan has 0 hits for "32x"/"GFLOPS". |
| SPEC-INFERNO | `Architecture` | **partial** | **GAP-3** | Three engine libraries + namespace split; the plan names none of `quant_dense`/`quant_moe`/`quant_multimodal`. |
| SPEC-INFERNO | `Engine catalog — dense/ (engines/trainer/dense/)` | **partial** | **GAP-3** | 35 modules; §2.1a row 24 rules `engines/trainer/dense/` "Supporting, not CORE" — right for the *sweep*, but the training scope itself is unrecorded. |
| SPEC-INFERNO | `Engine catalog — moe/ and multimodal/` | **partial** | **GAP-4** | §2.1a rows 12–14 + 21 already carry the multimodal and MoE attention sites — but **`video.cpp:140` is missing** (GAP-4). |
| SPEC-INFERNO | `Training-system decisions` | **missing** | **GAP-3**, **GAP-5**, **GAP-6** | 23 decisions (optimiser / schedule / loss / AMP / grad-clip / EMA-SWA / RLHF / LoRA / QAT / MTP) — not represented. |
| SPEC-INFERNO | `Feature parity checklist (PyTorch -> engine)` | **partial** | **GAP-3** | Engine parity list; §9/§9b cover model training but not engine parity. |
| SPEC-INFERNO | `Performance plan (how the 32x floor is met)` | **missing** | **GAP-1** | 8 performance levers; measured ~25 → ~72 GFLOPS (~2.9×). Absent. |
| SPEC-INFERNO | `Device-coverage plan (every backend)` | **missing** | **GAP-2** | Fail-loud contract for all backends. Plan's "18 of 20" is a wrong count. |
| SPEC-INFERNO | `Verified fixes (bugs the tests found and corrected)` | **partial** | **GAP-10** | The 12 engine bugs are fixed but **unrecorded here**; §10M lists 6 *other* criticals. |
| SPEC-INFERNO | `Modality matrix (all types trainable)` | **missing** | **GAP-7** | 26 trainable modalities; §9 has three text-centric benchmarks. |
| SPEC-INFERNO | `Test & verification` | **partial** | **GAP-8** | Same test tree as §10M; SPEC's "75 tests" vs 76 `.cpp` files on disk. |
| SPEC-INFERNO | `Conventions` | **covered** | — | C++20, per-subsystem namespaces, no `#ifdef` device forks — already §2's rule. |
| SPEC-INFERNO | `Roadmap (next work)` | **missing** | **GAP-1** | 8 items (auto-gradcheck on every loss, Vulkan SPIR-V, WebGPU/HIP paths, auto-distill + LR-finder hook, per-modality eval, activation checkpointing) — absent. |
| SPEC-INFERNO | `Reference (file map)` | **covered** | — | §10 is this plan's equivalent for the model layer. |
| SPEC-INFERNO | `Manifest` | **partial** | **GAP-8** | Claims 75/75 tests, 192 numeric checks, 12 bugs fixed, "exactly 1024 lines" — the line count is wrong. |
| SPEC-INFERNO | `Appendix A — dense module function-level reference` | **partial** | **GAP-3** | Function-level list of 35 modules; the attention-relevant entries are §2.1a-covered, the rest is engine scope. |
| SPEC-INFERNO | `Appendix B — training-loop pseudocode (the engine's core)` | **missing** | **GAP-3** | The engine's canonical training step (24 lines) — not in the plan. |
| SPEC-INFERNO | `Appendix C — measured benchmark reference (this host)` | **missing** | **GAP-1** | Per-backend GFLOPS on this host — the plan has no performance baseline at all. |
| SPEC-INFERNO | `Appendix D — backend probe matrix (runtime)` | **missing** | **GAP-2** | Runtime probe per backend; no device-coverage contract in the plan. |
| SPEC-INFERNO | `Appendix E — modality encoder spec` | **missing** | **GAP-7** | Encoder spec per modality; absent. |
| SPEC-INFERNO | `Appendix F — test case index (75 CTest cases)` | **partial** | **GAP-8** | Matches the plan's breakage-surface list except the engine's 3 proof tests (80+55+57 = 192 assertions). |
| SPEC-INFERNO | `Appendix G — build and run reference` | **missing** | **GAP-3** | CMake targets `quant_dense`/`quant_moe`/`quant_multimodal` + `bench_inferno`; §11 Phase 1 lists no engine target. |
| SPEC-INFERNO | `Appendix H — naming, conventions, glossary` | **covered** | — | §1 Naming + §2 conventions cover the naming half. |
| SPEC-INFERNO | `Appendix I — session work log (chronological)` | **covered** | — | History; this plan's §16 is its own audit trail. |
| SPEC-INFERNO | `Appendix J — glossary of subsystems` | **covered** | — | Subsystem naming; covered by §1/§10. |
| SPEC-INFERNO | `Appendix K — line budget and integrity` | **partial** | **GAP-8** | "Exactly 1024 lines" is false (980). The *rule* is good — this plan needs the same discipline for its own anchors (Step 3). |
| SPEC-INFERNO | `Appendix L — engine configuration surface (defaults)` | **missing** | **GAP-3** | 32 default config structs — the engine's whole configuration surface is unrecorded. |
| SPEC-INFERNO | `Appendix M — decisions-model training system` | **missing** | **GAP-6** | Reward design, GAE, RLHF wiring recipe — absent. |
| SPEC-INFERNO | `Appendix N — MoE and multimodal detail` | **covered** | — | Router kinds, aux losses, EP layout, fusion — §2.1a rows 12–14, 21. |
| SPEC-INFERNO | `Appendix O — per-modality training recipe` | **missing** | **GAP-7** | 24 recipes, one per modality — absent. |
| SPEC-INFERNO | `Appendix P — failure taxonomy (what the engine must never do)` | **missing** | **GAP-2** | 8 forbidden engine failure modes (P.1 silent-CPU-fallback, P.2 unchecked enqueue, P.3 weight-orientation, P.4 dangling ptr, P.5 zeroed derivative, P.6 per-call recompile, P.7 invalid NDRange, P.8 metrics losing history). The plan has §2's dead-code rule but no engine failure taxonomy. |
| SPEC-INFERNO | `Appendix Q — dependency map` | **partial** | **GAP-3** | Build-graph edges; the plan lists layers but no dependency order. |
| SPEC-INFERNO | `Appendix R — 32x measurement methodology` | **missing** | **GAP-1** | The 5-step ratio methodology; the ratio must be *measured live* or reported UNMEASURABLE. |
| SPEC-INFERNO | `Appendix S — maintenance and contribution rules` | **partial** | **GAP-13** | S.1–S.7 mirror the user's own rules. **Add: "both quant tracks" here.** |
| DEFECTS | `A. Review findings (workflow wf_ce1d51d7-91d)` | **covered** | — | §10M carries the 6 criticals; the 57-finding cluster is summarised in §10M/§11. |
| DEFECTS | `A1. Confirmed by cluster reviewers (57 findings captured)` | **covered** | — | §10M + §11 Phase 1 "the 6 confirmed critical defects". |
| DEFECTS | `B. Quantization quality defects (measured, 2026-10-17)` | **missing** | **GAP-13** | Q-1..Q-12 measured quality defects. **The ladder is wire-honest but not quality-honest** — this is the half the architecture plan never carried. |
| DEFECTS | `C. Bench honesty / measurement` | **partial** | **GAP-13** | C-1..C-3; the plan has no bench-honesty gate of its own. |
| DEFECTS | `D. Environment / build` | **covered** | — | §11 Phase 1 commit hygiene + §12 CI notes. |
| DEFECTS | `E. External audit findings (user-supplied, 2026-10-18 — STALE-ISH but problems live)` | **partial** | **GAP-10** | The problems live; the *statuses* are stale (D-23 is fixed — GAP-9). |
| DEFECTS | `E1. Industrial head-to-head (measured, matched BPW): 12/14 WIN` | **partial** | **GAP-13** | The parity table §9b.1 needs — **12/14 WIN, losses concentrated in MX and the 8-bit K-variants**. |
| DEFECTS | `E2. BPW truth` | **covered** | **GAP-11** | OC-G-5 zero-violation rule — but §9b.1's own text was stale (GAP-11, fixed here). |
| DEFECTS | `E3. Provenance: borrowed names, own code` | **covered** | — | §1 Naming covers the naming half; the README truthfulness item is §11 Phase 1 (Z3). |
| DEFECTS | `F. USER RULES (2026-10-18, binding — follow exactly)` | **covered** | — | F-0/F-1/F-2/F-3 are quoted in §9b.1 and the Phase-0 tier-rule bullet. |
| DEFECTS | `G. OPERATION CLEAN — final rules (user, 2026-10-18, supersedes where conflicting)` | **covered** | **GAP-11** | OC-G-1..OC-G-6 referenced in this step. |
| DEFECTS | `H. CF plan R4–R6 status — 2026-10-27 (new CodeFusion tree)` | **covered** | — | The CodeFusion paths are retired; this plan keeps CodeFusion on the side per the user's rule. |
| OC-MASTER | `Standing rules (binding, from the user)` | **covered** | — | G-rules are quoted in §9b.1. |
| OC-MASTER | `Target format ladder (60 formats)` | **partial** | **GAP-10** | **The heading itself is stale** — D-22 froze the count at 69. Any future "60" claim is stale. |
| OC-MASTER | `The budget proof that fixes the ladder (256-weight block)` | **covered** | **GAP-11** | §9b.1 defers to it; live: `types.h:295` returns 1.5f for `Q_1_K_H`. |
| OC-MASTER | `Plain integer families (10 base + 9 M + 9 H = 28)` | **covered** | **GAP-11** | §9b.1 names the tier rule. |
| OC-MASTER | `GRP families (9 M + 9 H = 18)` | **covered** | **GAP-10** | D-22: the GRP **bases are live**, not retired — §9b.1 must not assume otherwise. |
| OC-MASTER | `MX families (14, quarantined)` | **missing** | **GAP-13** | MX quality is catastrophic (−21..−37 dB vs same-BPW refs) and the family is quarantined — the architecture plan never says so. |
| OC-MASTER | `Retired (45 names)` | **partial** | **GAP-10** | The retired count moved when the GRP bases came back (D-22). |
| OC-MASTER | `ID strategy` | **covered** | — | **Verified live:** `types.h:146` `FORMAT_ID_SLOTS = 105`, `:147` `FORMAT_COUNT = 69`. |
| OC-MASTER | `Rewire map (the 27 name-vs-wire gaps, direction = cut the layout)` | **partial** | **GAP-11** | The 27 gaps; the direction rule (OC-G-5). |
| OC-MASTER | `Codec design` | **covered** | — | §9b.1 defers to it explicitly. |
| OC-MASTER | `Per-BPW budget algebra (must be exact at n = 256 and at every tail)` | **covered** | **GAP-11** | §9b.1 defers to it; it is what makes the 1.50 claim exact rather than approximate. |
| OC-MASTER | `The M tier — shared refinement byte (engine-agnostic, provably +0.25 BPW)` | **covered** | **GAP-11** | §9b.1 names the tier rule; 8 bytes per 256-weight block = exactly +0.25 BPW. |
| OC-MASTER | `The H tier` | **covered** | **GAP-11** | §9b.1 names the tier rule; 16 bytes per 256-weight block = exactly +0.50 BPW. |
| OC-MASTER | `Ternary (`Q_1_K_H`, 1.50 exact)` | **covered** | **GAP-11** | **Verified live:** `types.h:48` `Q_1_K_H = 12, // 1.5`; `types.h:295` `case Format::Q_1_K_H: return 1.5f;`. |
| OC-MASTER | `Industrial parity (NEW-1)` | **missing** | **GAP-13** | Every format must beat or match its industrial counterpart **at the same BPW** — the quality gate this plan lacks. |
| OC-MASTER | `Workstreams (execution order)` | **covered** | — | §11 Phase 1/2 mirrors the ordering (commit hygiene → sweep → architecture). |
| OC-MASTER | `Model swap (NEW-2)` | **covered** | — | §9b: `sol-4-flash` + dense DeepSeek V4.1 Flash. |
| OC-MASTER | `Verification gates` | **covered** | — | §7 Proof targets + §11 Phase-0 gates. |
| OC-PLAN | `Non-negotiables (from the operator)` | **covered** | — | One-task-at-a-time, zero-dead-code, zero-BPW-violations — already binding in this loop. |
| OC-PLAN | `Working state at plan time` | **covered** | — | §11 Phase 1 commit hygiene (307 modified / 84 untracked). |
| OC-PLAN | `Task DAG` | **covered** | — | §11 phases mirror the DAG. |
| OC-PLAN | `Why this order` | **covered** | — | The plan states its own ordering rationale. |
| OC-PLAN | `Task register` | **covered** | **GAP-10** | The **L4 row is stale** — the defect is fixed (GAP-9). |
| OC-PLAN | `Explicit non-tasks` | **missing** | **GAP-13** | GPU-backend completion OUT OF SCOPE; Q-10/Q-11 CANCELLED — the architecture plan should honour the same cancellations. |
| OC-PLAN | `Verification commands (run verbatim at every gate)` | **missing** | **GAP-11** | The plan states *gates* but not the *commands*. |
| OC-PLAN | `Progress log` | **covered** | — | §16 is this plan's audit trail. |
| OC-LADDER | `Rules the ladder encodes` | **covered** | **GAP-11** | §9b.1 quotes OC-G-1/OC-G-2/OC-G-5. |
| OC-LADDER | `Wire-count arithmetic (n = 256 block, bytes per block = BPW × 256 / 8)` | **covered** | **GAP-11** | The exact-budget algebra behind the 1.50 claim. |
| OC-LADDER | `GRP K_G family (takes M/H tiers; K_L retires)` | **covered** | **GAP-10** | Consistent with D-22 (GRP bases live, K_L retired). |
| OC-LADDER | `Final ladder table (69 formats — L1 writes this into the enum)` | **covered** | **GAP-11** | **Verified live:** `types.h:147` `FORMAT_COUNT = 69`. |
| OC-LADDER | `Keep (69 ids — every id below survives; nothing renumbers)` | **covered** | — | **Verified live:** `kFormatValid[105]` marks exactly 69 ids live. |
| OC-LADDER | `Retire (36 id holes — format_is_valid() = false; decode maps via L4)` | **covered** | — | **Verified live:** `types.h:164` `format_is_valid()` + `legacy_format_id_remap` at `format_compat.h:46`. |
| OC-LADDER | `Q_1_K_H ternary wire contract (the operator's H example, made exact)` | **covered** | **GAP-11** | **Verified live:** `types.h:48` + `:295` = exactly 1.50. |
| OC-LADDER | `Registry means every format is REACHABLE` | **missing** | **GAP-13** | `parse_format_name` must accept all 69 canonical names and `format_to_regformat()` must be lossless — a **reachability gate** this plan does not have. |
| OC-DECISIONS | `Ladder pattern L/M/H (operator: 2026-10-22, "Info 5" + "Info 2")` | **covered** | **GAP-11** | Quoted in §9b.1. |
| OC-DECISIONS | `Q_1 = binary, Q_1_K_H = pure ternary (operator, 2026-10-22)` | **covered** | **GAP-11** | Quoted in §9b.1 + Phase-0 tier-rule bullet. |
| OC-DECISIONS | `Rewire direction (operator: "BPW ko kam karo")` | **covered** | — | GAP-5: rewire the layout down to the name, never rename the ruler. |
| OC-DECISIONS | `GRP naming normalization` | **covered** | **GAP-10** | Consistent with D-22. |
| OC-DECISIONS | `Casing: QUANT → Quant (operator, 2026-10-19)` | **missing** | **GAP-13** | Z-2 casing sweep (~60 type renames) — not in this plan's Phase 1. |
| OC-DECISIONS | `BPW granularity (operator)` | **covered** | **GAP-11** | The .00/.25/.50 grid — §9b.1. |
| OC-DECISIONS | `Zero dead code / zero stubs (operator, 2026-10-18)` | **covered** | — | §2's dead-code rule + §11 Phase-1 purge (including `importance_factor_`). |
| OC-DECISIONS | `Persistence compatibility (design decision, agent-verified)` | **covered** | **GAP-9** | **Verified live and now DONE:** `include/quant/format_compat.h` + all 4 clamp sites rewired. |
| OC-DECISIONS | `M-tier encoder (design decision, pre-authorized)` | **covered** | **GAP-11** | §9b.1 defers to it. |
| OC-DECISIONS | `Ternary tail policy (design decision)` | **covered** | **GAP-11** | Never inflate — drop to the largest tier that fits the name's budget exactly. |
| OC-DECISIONS | `K-variant honesty (design decision)` | **covered** | — | Tier logic keys off the format ID, never the name string. |
| OC-DECISIONS | `Quality floor: scale fitting (design decision)` | **missing** | **GAP-13** | The scale-fit quality floor — **the missing quality half of the 1.5 BPW path**. |
| OC-DECISIONS | `MX quarantine (design decision, agent-verified)` | **missing** | **GAP-13** | MX must be quarantined; the architecture plan does not mention MX at all. |
| OC-DECISIONS | `Bench honesty (design decision)` | **missing** | **GAP-13** | Every printed bench number must be measured, not hardcoded; one byte basis per comparison. |
| OC-DECISIONS | `Priorities (operator delegated)` | **covered** | — | Delegated to the agent — §11 sets the order. |
| OC-DECISIONS | `One task to 100% (operator)` | **covered** | — | **The binding rule of this loop** — see the plan-loop file. |
| OC-DECISIONS | `Execution gate (operator)` | **covered** | — | The "Go." gate — implementation waits. |
| OC-DECISIONS | `Execution name (operator)` | **covered** | — | "Operation Clean". |
| OC-DECISIONS | `Strictness (operator, general)` | **covered** | — | Never weaken a test to make it pass. |
| OC-DECISIONS | `Known-caught-at-test-time traps (from exploration)` | **missing** | **GAP-13** | The +1-byte allowance trap, the "test that tests another file" trap, the GGUF zero-fill trap, the `NativeFormat` separate id-space — **no equivalent trap list in this plan**. |
| OC-DECISIONS | `Operation Clean ≠ review findings only` | **covered** | — | §10M scope statement. |
| OC-DECISIONS | `Workflow reconstruction record (D-17 fallback — filled only if triggered)` | **covered** | — | Not triggered. |
| OC-DECISIONS | `How to use this file during execution` | **covered** | **GAP-12** | Same discipline as the plan-loop file (`.plan-tmp/PLAN.md`). **This plan's own §16 still contradicted §2.1b.1 on the KAT inventory — that contradiction is corrected in Step 2 (GAP-12).** |
| OC-DECISIONS | `LADDER COUNT RESOLVED: **69 wins** (Fusion Smash, 2026-11-01)` | **covered** | **GAP-11** | **Verified live:** `types.h:146-147`. §9b.1 had ignored this — now fixed. |
| OC-DECISIONS | `LIVE DEFECT found during D-22 verification (L4 is a data-corruption bug)` | **covered** | **GAP-9** | **The defect is FIXED** — all four clamp sites now call `wire_format_valid()`. D-23 needs a resolution line. |
| OC-DECISIONS | Workspace rename: `code-fusion/` → `code/`, `transformers-fusion/` → `transformers/` (operator, 2026-11-12) | covered | — | D-24. Recorded 2026-11-12 (§16 dated entry + DECISIONS D-24); product/alias vocabulary unchanged, only path-shaped refs swept. |
| OC-DECISIONS | Effort slider: DSH plugin belongs to Sonar; Zenix port parked (operator, 2026-11-12) | covered | — | D-25. Recorded 2026-11-12 (§16 dated entry + DECISIONS D-25); Sonar integration + Zenix port both parked by operator ruling. |
| OC-DECISIONS | _archive/ = reference-only port of every deleted doc (operator, 2026-11-12) | covered | — | D-26. Recorded 2026-11-12 (§16 dated entry + DECISIONS D-26); 288 files, InNova.png stays deleted. |
| OC-DECISIONS | Goal hierarchy + 1.0 BPW side goal + FP/INT research direction (operator, 2026-11-12) | covered | - | D-27. Reminder note sits at the top of every implement-facing doc; dashboard carries the GOAL LINE. |
| OC-DECISIONS | Product-name normalisation: `TransFormers-Fusion` -> `Transformers-Fusion` (operator, 2026-11-13) | covered | - | D-28. Sweep completed 2026-11-13 across the working trees (docs, code, build scripts, CI, benches, tests); writer magic lowered to `Transformers-FusionIDX` while the reader still accepts the pre-D-28 spelling, so existing `.idx` files keep decoding. `DECISIONS.md` keeps the historical spelling on purpose. |
| OC-DECISIONS | Zenix-CC -> Zenix (CC suffix removed) + alias-registry duplicate cleanup (operator, 2026-11-13) | covered | - | D-29. `Zenix-CC` -> `Zenix` across folder, registry and current-state docs; duplicate `Transformers-Fusion` alias removed from §1 and §1.1; the folder/repo `-fusion` rule is reaffirmed without renaming product vocabulary. |
| OC-DECISIONS | Wire-magic identity: engine `.idx` accepts `Transformers-FusionIDX` + `TransCenderIDX` only; `SolIDX` is model-manifest-only (operator, 2026-11-13) | covered | - | D-30. `SolIDX` and `InNovaIDX` are rejected by `QUANTIdxReader`; `TransCenderIDX` is the legacy "formerly known as" alias; `SolIDX` is specified separately in `transformers/docs/MODEL_MANIFEST.md`; Test 8 asserts the accept/reject split (28 tests, 0 failures). |
| OC-WORKTREE | `Modified files (12) — dispositions` | **partial** | **GAP-10** | The counts drifted: PROGRESS.md now records **24 modified + 90 untracked**, not 12. |
| OC-WORKTREE | `Untracked files (18+) — dispositions` | **partial** | **GAP-10** | Same drift; the 3 engine proof tests are among the untracked and they are now registered. |
| OC-WORKTREE | `What P0.0 must do (in order)` | **covered** | — | §11 Phase 1 commit hygiene. |
| OC-WORKTREE | `Baseline expectations (so regressions are attributable)` | **covered** | — | §11 Phase 1 requires a green baseline before architecture work. |
| TF-PROGRESS | `Goal` | **covered** | — | 69-format ladder + honest benches = this plan's §9b.1 target. |
| TF-PROGRESS | `Done` | **covered** | — | L1 landed — **verified live** at `types.h:146-166`. |
| TF-PROGRESS | `Next` | **partial** | **GAP-10** | The "Next" table still lists **L4 as NOT done** — it is done (GAP-9). |
| TF-PROGRESS | `Key facts (verified with evidence)` | **partial** | **GAP-9** | The "L4 NOT done — live data-corruption bug" fact is **stale**. |
| TF-PROGRESS | `Open questions` | **partial** | **GAP-10** | Q1 (60 vs 69) is **answered** by D-22; Q2 (who owns the 24 modified files) is moot; Q3 (`install_test/`) is covered by §11 Phase 1. |
| TF-PROGRESS | `Rules I am holding myself to` | **covered** | — | SOLO-only + proof-per-claim = the rules of this loop. |

**Status key:** `covered` = the plan already carries it (anchor named in the note) · `partial` = carried but incomplete or stale → a gap id · `missing` = absent from the plan → a gap id.

### 10X.3 What this changes in the plan

- **§9b.1 re-based on the live enum** (gap **GAP-11**) — the K-tier rework has landed; `Q_1_K_H` is 1.50 BPW at `types.h:295`.
- **§9b.2 added** — **both quant tracks** are in scope (gap **GAP-13**): the implemented ladder **and** loop-aware quantisation, plus the intersection neither covers.
- **New Phase-0 to-dos** for gaps GAP-1 … GAP-10, GAP-13 (below).
- **§16 updated** — the stale "still open" list is reconciled against this map.

---

## 10Y. The seven remaining trees — audited file-by-file (Step 4, 2026-11-12)

**The plan's "not yet audited" list is now closed.** Every path was walked file-by-file and grepped with
the full attention/softmax signal set. The method is reproducible and the scripts are in the workspace:

- `fusion/.rea-tmp/step4_tree_audit.py` — walks each path, classifies every file, records every hit.
- `fusion/.rea-tmp/step4_detail.py`, `step4_detail2.py`, `step4_detail3.py` — read the hits and classify them.

**Signal regex used (identical for all seven paths):**

```
attention|Attention|softmax|Softmax|SOFTMAX|q_proj|k_proj|v_proj|o_proj|flash_attn|flash_attention|FlashAttention|sdpa|scaled_dot|ScaledDot|q_norm|k_norm|rope|RoPE|rotary|Rotary|kv_cache|KVCache|paged_attention|PagedAttention|cross_attn|CrossAttention|cross_attention|num_heads|head_dim|n_heads|causal_mask|causal|qk_t|QK
```

### 10Y.1 `src/server/` — 6 files, 3,805 lines — 1 attention-relevant site, 3 socket binds

| Site | What it is | Verdict |
|---|---|---|
| `src/server/production_core.cpp:162` | `KVCache cache((int)cfg.num_layers, cfg.max_seq_len, cfg.num_heads, cfg.head_dim);` | **the serve-time attention-shape authority.** Not an attention implementation — but it fixes `num_layers` / `max_seq_len` / `num_heads` / `head_dim` at serve time, so **any** change to the attention layout (a new head count, a fused KV layout, the §5d per-token KV sets) breaks here first. **Add it to the sweep.** |

**The `INADDR_ANY` claim was wrong — see §10M.** Three binds live in or near this tree, and only one of
them is unauthenticated. Full table with the auth evidence: **§10M**, "High" table.

### 10Y.2 `src/gle/` — 2 files, 406 lines — **CLEAN**

```
$ rg -n --no-ignore --hidden "attention|Attention|softmax|Softmax|…|QK" src/gle/
(no matches — 0 hits)
```

**Verdict: no attention-relevant code.** `src/gle/` needs no sweep work.

### 10Y.3 `src/core/telemetry.cpp` — 1 file, 340 lines — **NOT CLEAN** (the plan's claim was wrong)

```
$ rg -n --no-ignore --hidden "kv_cache|KVCache|softmax|attention" src/core/telemetry.cpp
102: void MemoryTracker::track_kv_cache(int64_t bytes) {
104:   breakdown_.kv_cache_bytes += bytes;
243: // KVCacheQuantizer
246: KVCacheQuantizer::KVCacheQuantizer(const KVQuantConfig& cfg) : cfg_(cfg) {}
248: int64_t KVCacheQuantizer::quantize_old_states(Tensor& k_cache, Tensor& v_cache,
264: void KVCacheQuantizer::restore_for_attention(const Tensor& quantized_k,
276: int64_t KVCacheQuantizer::bytes_saved() const { return total_bytes_saved_; }
278: float KVCacheQuantizer::compression_ratio() const {
283: float KVCacheQuantizer::estimated_quality_loss() const {
316: KVCacheQuantizer quant;
321: printf("  Estimated quality loss: %.2f%%\n", quant.estimated_quality_loss() * 100.0f);
```

**What it actually is.** `KVCacheQuantizer` (declared `include/quant/telemetry.h:232` `KVQuantConfig`,
`:239` the class) is a **pure stub with a fabricated metric**:

| Method | What the code does | Why it is a defect |
|---|---|---|
| `quantize_old_states` :248 | comment at :255-256 — *"Simulate quantization: zero out states beyond full-precision window / (In real impl, would quantize to Q4/QUANT and store compressed)"*. It **computes a hypothetical byte saving and quantizes nothing**. | §2 zero-dead-code rule. |
| `restore_for_attention` :264 | comment at :267-268 — *"In real impl: dequantize from Q4/QUANT to FP32 / For now, just copy"*. The body is a `memcpy`. | §2 zero-dead-code rule. |
| `estimated_quality_loss` :283 | `return 0.001f;` with the comment *"< 0.1% typical quality loss"*. **And it is printed** at `:321` as `"  Estimated quality loss: 0.10%"`. | **A hardcoded constant presented to the user as a measurement** — the same defect class as `god-runtime.ts:5264` and `god-runtime.ts:3679`. Gate **V28**. |

**And it is a duplicate of a real implementation that already exists.** `src/model/kv_cache_quant4.cpp`
(420 lines) is a **real** Q4 KV cache: Lloyd-Max 16-centroid quantizer, `quantize_block_quant4` /
`dequantize_block_quant4` (`:164` / `:169`), `append` (:207), `context_len` (:368),
`compression_ratio` (:388), `clear` (:395), `resize` (:405); header `include/quant/kv_cache_quant4.h:52`
/ `:54`; and it **is** tested — `tests/test_kv_cache_quant4.cpp` (20 attention/KV hits). **So the fix is
not "implement the telemetry quantizer" — it is "delete the telemetry stub and point the report at the
real `Q4KVCache`."** That is also the §2 duplicate-code rule.

### 10Y.4 `inferno/` — 5 files, 1,324 lines — **CLEAN** (it is the speed bench, not the model)

```
$ rg -n --no-ignore --hidden "attention|Attention|softmax|Softmax|…|QK" inferno/
(no matches — 0 hits)
```

**Verdict: no attention-relevant code.** `inferno/inferno_bench.cpp` measures backend GFLOPS and prints the
32× ratio label (`:469`) and `UNMEASURABLE` (`:471`) — it is the **GAP-1 instrument**, not a model site. No
sweep work; it needs the **V-gate**, not the sweep.

### 10Y.5 `scripts/` — 9 files, 1,098 lines — **CLEAN**

```
$ rg -n --no-ignore --hidden "attention|Attention|softmax|Softmax|…|QK" scripts/
(no matches — 0 hits)
```

**Verdict: no attention-relevant code.** One *non-attention* note: `scripts/plot_comparison_charts.py:149`
still carries the leftover Plotly variable name `tracesol` for the "our formats" series — a cosmetic
rename candidate, and it is **implementation code**, so the Go gate keeps it untouched. Recorded in §6 so
nobody "cleans it up" by accident.

### 10Y.6 `tests/` — 77 files, 14,832 lines — **the conformance surface, not a clean tree**

```
$ rg -n --no-ignore --hidden "attention|Attention|softmax|Softmax|…|QK" tests/
→ 435 hits across 40 of 77 files
```

This tree is **where the attention formula is proven**, so it is the **breakage surface** the sweep must
protect. The load-bearing test sites:

| Test site | What it proves | Why it matters to this plan |
|---|---|---|
| `tests/test_protected.cpp:119-134` | `flash_attention_forward(Q, K, V, mask, 0.0f)` | The **only** direct test of the KAT fused kernel (`src/kernel/flash_attention.cpp`). §2.1b's kernel must keep passing it. |
| `tests/test_simd_math.cpp:110-124` | SIMD-vs-scalar **softmax parity**, tolerance `1e-5`, plus *"softmax dispatched row sums to 1"* | The numerical-conformance test for the **softmax primitive** every attention path calls. A changed formula is proven here or nowhere. |
| `tests/test_gpu_capability.cpp:29, 300` | *"every op throws fail-loud; gemm/gemv/softmax/norm/scale throw by …"* / *"softmax/rmsnorm/layernorm/rope/attention/reduce/moe — NO quant."* | **This is the GAP-2 fail-loud contract's test surface.** The Phase-0 GAP-2 decision lands here. |
| `tests/test_backends_realonly.cpp:260, 270` | CANN `reference_softmax(xs, ys, rows, cols)` — *"reference_softmax rows are distributions"* | The only *other-backend* numerical reference for softmax. |
| `tests/test_quant_mix.cpp:430, 559-562` · `tests/test_trainer.cpp:220-227, 337-340` · `tests/test_training.cpp:20-31` | the **attention-projection parameter enumeration** — `layers.0.attention.q_proj.weight`, `layer->attention.{q,k,v,o}_proj.{weight,bias}` | **The Track-A test surface.** Any new format used for `sol-4-flash` must be asserted to cover the attention projections here — **OC-G-5 zero-violations**, and it is the exact file set the §9b.2 "ruler model must actually ship" claim depends on. |
| `tests/test_code_gen.cpp:43` | `gen.generate_attention(8, 16, 2, SIMDTarget::AVX2)` | The JIT path — **`seq_len=8` only**. This is why the §10M critical #2 (stack overflow) is untested. Gate **V20**. |
| `tests/test_kv_cache_quant4.cpp` (20 hits) · `tests/paged_kv_4m_test.cpp` (27 hits) · `tests/test_transformer.cpp` (44) · `tests/test_protected.cpp` (42) | KV-quant4, 4M paged KV, the transformer itself, the protected surface | The regression net for everything above. |
| `tests/CMakeLists.txt` (80 hits) | `add_quant_test*` registrations | The registration surface — **every new test must be registered here or it never runs.** |

### 10Y.7 `code-fusion` (read-only sibling) — **CLEAN**, and it is **not** where the plan says it is

```
$ rg -n --no-ignore --hidden "attention|Attention|softmax|Softmax|…|QK" code/windows/sonar/merger/code-fusion-dead-20261101/
→ 5,183 raw hits — but a source-only re-scan with an implementation-shaped pattern gives 0
```

**The 5,183 raw hits are false positives**: base64 integrity hashes in `package-lock.json` (the substring
`QK`), minified CSS in `packages/client/ui-workspace/lib/client.js`, and **LaTeX typesetting prose** in
`skills/pdf/**` that literally says *"softmax, attention"* as an example of a wide fraction. A
source-only scan (`.ts`/`.tsx`/`.js`/`.mjs`/`.py`/`.rs`/`.go`/`.cpp`/`.h`, excluding `skills/`,
`examples/`, `.agents/`, `docs/`, `website/`, `archive/`, minified `lib/`, `.bundle/`) over **2,713 files**
gives **0 implementation-shaped hits** — no `class *Attention`, no `attention(...)` function, no
`softmax(`, no `q_proj`/`k_proj`/`v_proj`, no `num_attention_heads`. `native/` (**106 files**) and
`python/` (**14 files**) also give **0**. **Verdict: the CodeFusion harness has no attention or softmax
implementation** — consistent with §10R's *"the engine owns the neural substrate"* and with the plan's
decision that EAIN lives engine-side.

**And the tree moved.** The plan's §10D / §10O–§10W describe the CodeFusion **monorepo** (`packages/`,
`apps/web/`, `docs/architecture.md`, `session-reference/`, `packages/compaction/`). That monorepo is
**not** at `code/` any more:

| Path | What it is now |
|---|---|
| `code/` | the **payloads / skills** distribution repo (Code Swing owns it; the user's rule keeps it on the side, untouched) |
| `code/windows/sonar/merger/code-fusion-dead-20261101/` | **the npm-migrated CodeFusion monorepo** — the tree the plan's §10D/§10O–§10W describe (it has `package-lock.json`, `packageManager: npm@12.0.2` and **no** `pnpm-workspace.yaml`, exactly as §10D says) |
| `code/windows/sonar/merger/deepseek-harness-master/` | the upstream DSH master (still on pnpm) |

**Every §10O–§10W path in this plan therefore resolves under that root**, and the Step-3 verifier was
re-run with a multi-root index to prove it (§16, Step 3 entry). Nothing in `code/` was modified.

### 10Y.8 The verdict, in one table

| Path | Files | Lines | Attention-relevant sites | Verdict |
|---|---|---|---|---|
| `src/server/` | 6 | 3,805 | **1** — `production_core.cpp:162` (serve-time attention shape) + 3 `INADDR_ANY` binds | **add the KVCache site to the sweep** |
| `src/gle/` | 2 | 406 | **0** | **CLEAN** — no sweep work |
| `src/core/telemetry.cpp` | 1 | 340 | **12** — `KVCacheQuantizer` | **NOT CLEAN** — stub + fabricated metric (§10M) |
| `inferno/` | 5 | 1,324 | **0** | **CLEAN** — it is the GAP-1 speed instrument |
| `scripts/` | 9 | 1,098 | **0** | **CLEAN** — no sweep work |
| `tests/` | 77 | 14,832 | **435** across 40 files | **the conformance surface** — protect it, do not sweep it |
| `code-fusion` (monorepo) | 2,713 source files | — | **0** implementation-shaped | **CLEAN** — the harness owns no neural substrate |

**Net effect on the plan:** one new sweep site (`production_core.cpp:162`), one new high-severity defect
(the fabricated quality-loss metric, §10M), two additional unauthenticated listeners (§10M), one
corrected defect citation (`serve.cpp:118`), one newly-**real** section (§10M, which had nine dangling
references), and a relocation note for the whole CodeFusion tree (§10Y.7).

---


## 11. Execution phases

Research gate first, then unblock the smallest things, then the big build.

### Phase 0 — Research (BLOCKING GATE)
**No implementation of routing, `G`/`S`, EAIN, or the sweep may begin until this completes.**

- **[RESOLVED 2026-11-12]** **Discard the superseded plan.** Rewrite the comment at `include/quant/transformer.h:119-122` that still points at *"Cender/ formula (Phase 19-23, owner-gated)"* — that plan is dead; ours is authoritative (§2.1). **VERIFIED 2026-11-10 — and the plan's anchor was WRONG:** the stale note lives at **lines 119–122** (*"NOTE (owner purge 2026-09-07): attention-variant layer classes REMOVED … until the Cender/ formula (Phase 19-23, owner-gated) proves parity"*), not 116–118. **Anchor corrected.**
- **[RESOLVED 2026-11-10]** **Produce the KAT-layer inventory** (§2.1b) — the shape is now mapped: `ScaledDotProductAttentionFunction::forward` (training), `src/trainer/code_gen.cpp::attention_flash` (JIT-emitted C++), `src/kernel/flash_attention.cpp`, `src/math/math.cpp::softmax`, and **18 of 20 GPU backends**. **The remaining Phase-0 work is the *decision*, not the inventory:**
  - **How do `G` and `S` reach the hardware?** (a) a fused Fusion kernel with all paths delegating to it, (b) compute `G`/`S` outside the inner loop and pass them in, keeping the kernel contract, or (c) a separate Fusion path for train + inference, leaving the traditional kernels for legacy checkpoints. **(b) is cheapest to land; (c) is cleanest.** This is the single most important architectural decision in the project and it must be made **before any kernel work starts.**
  - **The 2048-token ceiling in generated code** (`src/trainer/code_gen.cpp:236`) must be removed or bypassed — a 4M context cannot be served by a generator that caps at 2048. **~~RE-VERIFIED 2026-11-10 … still open~~ RESOLVED 2026-11-13 (T6.3/V20 fix landed):** the buffer is now a heap `std::vector<float>` sized to the real seq_len (`:258`), the boundary rejects `seq_len > 2048` loudly, and `test_attention_v20_budget` covers 2049/8224/32768. The **capability** half (streaming/tiled softmax for 4M contexts) stays open as gate V20's second half.
  - ~~Confirm the `src/math/math_avx2*.cpp` and `math_avx512.cpp` files compute no attention.~~ **ANSWERED 2026-11-10 (live code check): they compute NO attention.** `math_avx2_tiled.cpp` has **zero** attention tokens; `math_avx2.cpp`, `math_avx2_vec.cpp` and `math_avx512.cpp` contain only **generic elementwise `softmax` primitives** (`softmax` @460, `vec_softmax_stable` @149 and @557, `softmax_avx512` @286) — not attention. That softmax is **already** a known KAT site (`src/math/math.cpp::softmax`, §2.1b), so it stays on the sweep list via that path. **These four files need no attention-sweep work.**
- **[RESOLVED 2026-11-12]** **Fix the plan's own line anchors.** The adversarial review found the first inventory conflated `.cpp` definition lines, `.h` class-declaration lines and section-banner lines, and left several wrong citations. A cleanup pass is required because the plan is a working document.
- **[RESOLVED 2026-11-13]** Deep-read the §5 papers; produce a written design note for `G` and `S`. → **Done: §5c.6** (ten papers deep-read; abstracts fetched live 2026-11-13; every fork tagged to its ledger id, nothing closed by fiat).
- **[OPEN-DECISION]** Resolve: whether transformed layers use **shared weights** (one set, both modes) or **separate weights that switch** — this sets the parameter count.
- **[OPEN-DECISION]** Decide the **loop-exit policy** (learned gate vs post-hoc confidence readout — §5 evidence favours the latter being competitive).
- **[OPEN-DESIGN]** Design **EAIN** scoped to the implementable subset only (§4.9): per-unit importance/decay + thresholded activation + local plasticity driven by reward prediction error + offline consolidation.
- **[OPEN-DECISION]** **Decide which existing continual-learning stack EAIN sits on** (§4.8a): three parallel stacks exist and are unreconciled. **This is a design choice, not a consolidation project** — the user explicitly rejected unifying them.
- **[RESOLVED 2026-11-10]** **Settle the 1.5 BPW tier rule** (§9b.1) — `Q_1_K_H` at exactly 1.50 wire BPW per GAP-2, with zero violations per GAP-5. The L/M/H K-tier rework is uncommitted in-flight work; the spec is `review-tracking/DEFECTS.md`.
- **[OPEN-RESEARCH]** **Research NCM** (§3b) — read arXiv `2610.14162` in full. **The §3b.6 spec is already extracted from the HTML through character 100000 — the remaining Phase-0 read is offset 100000 onward**, which holds the Appendix F.1.1 levels ablation, Appendix C Tables 5–6 (exact `K` and `|V_k|`), and Appendix I "Limitations & Future Work". The open questions are ours: **scale beyond 725M**, **reconstruction fidelity for names/numbers** (fatal for the PDF test — see the 98.79% WMT14 figure at §3b.6), **general-purpose variable-length output** vs task-specific configs, and whether the code (`github.com/HazyResearch/ncm`) is usable as a starting point. **Decide incremental adoption vs fused training** (§3b.5).
- **[OPEN-UNKNOWN]** **Reproduce the step-0 U-curve on a WEIGHT-TIED looped model** (§5c.2, gap 5). The `2603.10123` dead-zone result assumes distinct per-layer operators; our routing makes many layers weight-tied, so the `O(1/(H−1)!)` constant may differ. Until this is measured, `G`'s depth correction (Form C) is a hypothesis, not a fix.
- **[OPEN-DECISION]** **Decide the `G` formulation** — §5c.2 recommends **B (index-selected, `log m` normalisation) + C (depth correction)**, with **A (rectified/unnormalised normaliser) behind an experimental flag** because A breaks the V10 strict-superset property. This decision changes V10's wording and is therefore a gate on Phase 2.
- **[OPEN-DECISION]** **Pick the `S`/`G` depth-axis variant** (§5e). The Attention-Residual family (`2603.15031`, `2607.18730`, `2605.18855`, `2610.13630`, `2607.27230`, `2607.09694`) is our `G`/`S` mechanism. Two forks to close: **(a) single-stream vs multi-stream** (AttnRes/MHAR vs DAR/MSAR — changes our `TransformerBlock` residual topology, and we are pre-norm), and **(b) routing-key dimensionality** — benchmark **LR-AttnRes's low-rank key first**, because it is the only variant whose routing cost is decoupled from hidden width `d`, which is what the 1.5 BPW budget (§9b.1) makes a first-order concern. Set the `S` windowing policy from ARLoop's result that **sliding-window depth attention ≥ full-history** at larger recurrent depths — our bounded `S` is the state of the art, not a compromise.
- **[OPEN-DECISION]** **Put `G` in the quantisation test set from day one** (§5f). OASIS (`2605.17887`) shows an extra depth-wise normalisation channel amplifies outliers and low-bit error, and `2609.30820` shows the **loop-entry** path is where per-channel INT4 fails first. **Identify our loop-entry seam and give it an identity path**; and any PTQ we run must accumulate Hessians over **all** recurrence steps, not one.
- **[OPEN-DECISION]** **Default the routing to a small loop count and measure against a fixed-depth baseline** (§5d). The only two published compute-matching wins (SMELT `2609.01343`, Loopie `2607.16051`) both use **exactly two loops on an MoE backbone** — our plan is dense, so the fixed-repeat baseline must be measured before any claim (consistent with §5c.3 conclusion 2, which already flags `1803.08165`).
- **[OPEN-DECISION]** **Adopt the Loop-µP residual scaling on the looped path** (§5d.3.4, `2606.18524`): residual branch **× 1/N** with the learning rate **independent of N**. Our `TransformerBlock` is pre-norm and §5's routing **weight-ties layers**, so our residual stream grows **linearly in the loop count** instead of √L — exactly the failure Loop-µP fixes. **Add a V-gate: residual-stream norm flat across loop counts.** Cheapest concrete Phase-0 experiment in this whole plan, with a published reference result (the base LR transfers to **8 loops / 384 executed layers**).
- **[OPEN-DECISION]** **Default the loop count to 2 and measure up to 4** (§5d.3.6). Two independent sources: Ouro's **T=8 loss spikes**, and `2610.00673`'s own T=8 run showing the per-loop loss stops improving after loop 3–4 (*"the extra iterations cost compute without measurable gain"*). The two compute-matching wins (SMELT, Loopie) both use **exactly 2**. Our fixed-repeat baseline must therefore be **T = 2**, not an arbitrary one.
- **[OPEN-DECISION]** **Design the exit gate and monitor it directly** (§5d.3.2, `2510.25741`, `2610.00673`): `λ_t(x) = σ(Gate(F^(t)(x)))`, **Q-exit** at inference (a deployment knob, no retraining), **LR warmup** + **β ≥ 0.10** to prevent the step-1 collapse, **smoothed exit loss (ε = 0.05)** so no step is starved of gradient. **The LM loss will NOT show the collapse** — with a small entropy coefficient and no warmup, `p(exit at step 1)` stays **1.00 for all 2,267 steps** while the model silently trains as a plain transformer. **Assert on the exit distribution, not the loss.**
- **[OPEN-DECISION]** **Use the correctness-directed online depth mask as our loop curriculum** (§5d.3.3, `2610.00673`): compare the top-1 prediction at every active step with the target, assign unmatched tokens to the final active step, treat the mask as a **stop-gradient** routing decision, and **increase the maximum active depth one step at a time**. It is the only curriculum in the corpus that supports **more than two** steps without the intermediate-step collapse.
- **[OPEN-DECISION]** **Make §5's routing per-token AND attention-work-reducing** (§5d.2 axis 3, §5d.5 item 5): inactive tokens must skip deeper recursions **including their attention and KV work** (Mixture-of-Recursions, T-LoopFormer's recursion-wise KV cache). Our `HybridAttnKind` / `build_hybrid_schedule` seam must express *which* tokens loop, not just how many layers loop — and `T` separate KV sets per token position must be in the Phase-1 memory budget (§5d.1, item 2).
- **[OPEN-DECISION]** **Decide our residual interface for the looped path** (§5d.3.4, `2611.07226`). Loop-µP's **× 1/N** and Loopback's **per-block-update interface** are **two different fixes to the same problem**. Loopback's deeper claim — a full block output **reweights the history already carried by the input**, so input strength and update weight must be controlled separately — is exactly the §5e `G`/`S` problem, and it argues for building the **depth-attention path before** the loop-count work, not after. **Decide which, and write the V-gate for it.**
- **[OPEN-DECISION]** **Decide our KV-cache policy for `T` loops** (§5d.1 item 2, `2610.33360`). The naive choice is `T` separate KV sets per token position; the shared-KV alternative cuts **persistent cache sets from fifteen to four** and removes **81–89%** of the continuation-loss penalty using a **consistency loss in the final 10%** of training. **This changes the Phase-1 memory budget at 1.5 BPW × 4M window — decide it before the budget is written.**
- **[OPEN-UNKNOWN]** **Add an OOD-stability gate, not just a loss gate** (§5d.4). The corpus reports looped models at **~10× worse out-of-distribution standard deviations** than fixed-depth (**0.087–0.122** vs **≤0.009**), and **no looped-model stability fix has been validated above a few billion parameters** — our 4B target is above that ceiling (**UNKNOWN at our scale**). **Gate on the spread across seeds, not on the mean.**
- **[RESOLVED 2026-11-12]** **State the 32× Inferno speed bar as a V-gate** (§10X **GAP-1**, `SPEC-INFERNO` §0.2/§2/§8, Appendix C/R). The project has a non-negotiable floor — `best_live_backend_GFLOPS / baseline >= 32.0` — and **this plan never mentions it**. **Verified live:** `inferno/inferno_bench.cpp:469` prints the 32× label and `:471` prints `UNMEASURABLE` when CUDA is offline. Add the ratio as a §7 proof target, name the **target device** (AMD Radeon Vega 7 / 5600GT iGPU), and adopt the rule that an **unmeasurable ratio is reported UNMEASURABLE, never fabricated** (Appendix R.4). **RESOLVED 2026-11-12 — decision D-1** (§6.1): adopted as §7 proof target **#8** and gate **V30**.
- **[RESOLVED 2026-11-12]** **Correct the backend count and adopt the fail-loud contract** (§10X **GAP-2**). §2.1b's *"18 of 20 GPU backends"* is **wrong** — the live enum `include/quant/backend.h:9` has **24** members, and `src/backend/backend.cpp` (3,103 lines) must have one explicit `case BackendType::` each with an unknown enum that **throws**. Add the contract + `SPEC-INFERNO` Appendix P's failure taxonomy as a §7 gate — especially **P.1: never silently fall back to CPU while reporting GPU GFLOPS**. **RESOLVED 2026-11-12 — decision D-2** (§6.1): adopted as §7 proof target **#9** and gate **V31**; the three counts are now separated (24 enum members / 20 files / 4 with fused attention).
- **[RESOLVED 2026-11-12]** **Decide the training-engine scope** (§10X **GAP-3**). The plan sweeps `engines/trainer/` for attention but never states that the deliverable includes a **feature-complete training engine** — `quant_dense` / `quant_moe` / `quant_multimodal`, **112 files, 11,878 LOC** (verified live). Decide whether the Fusion attention core must also exist on the **engine's** path, and add the three CMake targets to §11 Phase 1. **RESOLVED 2026-11-12 — decision D-3** (§6.1): **in scope — all three libraries, one attention core**; the three CMake targets land in Phase 1.
- **[RESOLVED 2026-11-12]** **Add the missed sweep site** (§10X **GAP-4**): `engines/trainer/multimodal/dense/video.cpp:140` (`softmax_rows(scores)` in the video ViT block) — §2.1a covers `vision.cpp`, `projection.cpp` and `fusion_layers.cpp` but not `video.cpp`. Add it as row 22. **RESOLVED 2026-11-12 — decision D-4** (§6.1): added as §2.1a row **22**; the Step-4 server site (`src/server/production_core.cpp:162`) is row **23**.
- **[RESOLVED 2026-11-12]** **Add the second missed sweep site** (Step 4, §10Y.1): `src/server/production_core.cpp:162` — `KVCache cache((int)cfg.num_layers, cfg.max_seq_len, cfg.num_heads, cfg.head_dim);`. It is the **serve-time attention-shape authority**: any change to the attention layout breaks the server before it breaks the model. Add it as row 23. **RESOLVED 2026-11-12 — decision D-4** (§6.1): added as §2.1a row **23**.
- **[RESOLVED 2026-11-12]** **Decide MTP vs DSpine** (§10X **GAP-5**). `engines/trainer/dense/mtp.{h,cpp}` (`MTPHead`, `mtp_total_loss`, `shift_labels`) implements multi-token prediction; §3c's DSpine is speculative decoding. They overlap in purpose and both touch decoding — **one decision, not two**. **RESOLVED 2026-11-12 — decision D-5** (§6.1): **both, sequenced — MTP in Phase 6, DSpine in Phase 6c**.
- **[RESOLVED 2026-11-12]** **Decide the modality + decisions-model scope** (§10X **GAP-6**, **GAP-7**): 26 trainable modalities and a **decisions/policy model** (rewards + GAE + PPO/DPO/GRPO/RLVR) are in `SPEC-INFERNO` §0.3/§0.4/§11 but in no plan section. §9 has three text-centric benchmarks and §9b names one model. **RESOLVED 2026-11-12 — decisions D-6 and D-7** (§6.1): the decisions model is a **head + RL algorithm on the same ruler model**; the modality matrix is a **coverage table with zero silent gaps**, and its count is **re-derived from the live tree**, never quoted from SPEC-INFERNO's own contradictory 25/26/27.
- **[RESOLVED 2026-11-12]** **Carry the Operation Clean quality gates into this plan** (§10X **GAP-13**): industrial parity at equal BPW (NEW-1), the scale-fit quality floor (D-12), MX quarantine (D-13), bench honesty (D-14), format reachability (all 69 canonical names must parse), the casing sweep (D-05), and the known test-time traps (D-20). **Also add the second quantisation track** — see **§9b.2**. **RESOLVED 2026-11-12 — decision D-8** (§6.1): carried as gates **V28**, **V32**, **V33**; the MX family stays quarantined; both quantisation tracks stay in scope via **§9b.2**.
- **[OPEN-DECISION]** Decide **where the harness talks to the engine** — the C++ `quant::agi::WorldModel` is complete but has **no bridge** (§10R). Native bridge vs reimplementation is a real fork; **default to reusing the C++ one**.
- **[OPEN-ACTION]** Deliverable: a design note in `transformers/` (which has no docs system — create one modelled on `code/docs/AGENTS.md`, respecting its tier taxonomy, word budgets, and one-physical-line-per-paragraph rule).


**Phase-0 status ledger (2026-11-13).** Every bullet above carries an explicit status tag, so **nothing is silently open**. The counts: **13 RESOLVED**, **15 OPEN-DECISION**, **1 OPEN-RESEARCH**, **1 OPEN-DESIGN**, **2 OPEN-UNKNOWN**, **1 OPEN-ACTION**.

| # | Status | What it is |
|---|---|---|
| 1 | **RESOLVED 2026-11-12** | Anchor corrected to `transformer.h:119-122` (Step 3); the comment rewrite itself is Phase-1 work. |
| 2 | **RESOLVED 2026-11-10** | §2.1b.1 rebuilt from disk; the remaining work is the *decision*, not the inventory (Step 2). |
| 3 | **RESOLVED 2026-11-12** | **153/153** anchors + **79/79** continuation refs resolve; 8 drifted citations fixed (Step 3). |
| 4 | **RESOLVED 2026-11-13** | The §5 papers read end-to-end; the written `G`/`S` design note is **§5c.6**. Source: §5c.1–§5c.6. |
| 5 | **OPEN-DECISION** | Sets the parameter count. §5d.3.4 (Loop-µP) and §5e both assume **weight-tied** layers; §5d.3.4 gives the evidence. |
| 6 | **OPEN-DECISION** | Learned gate vs post-hoc confidence readout. §5 evidence favours the latter being competitive — the comparison is a Phase-0 measurement. |
| 7 | **OPEN-DESIGN** | EAIN scoped to the implementable subset only (§4.9): per-unit importance/decay + thresholded activation + local plasticity from reward prediction error + offline consolidation. |
| 8 | **OPEN-DECISION** | Three parallel continual-learning stacks exist and are unreconciled (§4.8a). **A design choice, not a consolidation project** — the user explicitly rejected unifying them. |
| 9 | **RESOLVED 2026-11-10** | §9b.1 re-based on the live enum: `Q_1_K_H` = **exactly 1.50** wire BPW (`types.h:295`), zero violations per **OC-G-5**, count frozen at **69** by D-22 (Step 1). |
| 10 | **OPEN-RESEARCH** | **Partly done** — the §3b.6 spec is already extracted from arXiv `2610.14162`. Remaining: the Appendix F.1.1 / I read plus four open questions (§3b.4), including the fatal-to-V5 reconstruction-fidelity question. |
| 11 | **OPEN-UNKNOWN** | **Explicitly UNKNOWN.** The `2603.10123` dead-zone constant assumes distinct per-layer operators; our routing weight-ties layers, so `O(1/(H−1)!)` may differ. Until it is measured, `G`'s depth correction (Form C) is a **hypothesis, not a fix**. |
| 12 | **OPEN-DECISION** | §5c.2 recommends **B (index-selected, `log m` normalisation) + C (depth correction)**, with **A** behind an experimental flag. This decision changes V10's wording, so it gates Phase 2. |
| 13 | **OPEN-DECISION** | Attention-Residual family (`2603.15031`, `2607.18730`, `2605.18855`, `2610.13630`, `2607.27230`, `2607.09694`). Two forks: single-stream vs multi-stream, and routing-key dimensionality. |
| 14 | **OPEN-DECISION** | OASIS (`2605.17887`) shows an extra depth-wise channel amplifies outliers; `2609.30820` shows the **loop-entry** path is where per-channel INT4 fails first. |
| 15 | **OPEN-DECISION** | Both published compute-matching wins use **exactly two** loops on an MoE backbone; ours is dense, so the fixed-repeat baseline must be measured before any claim. |
| 16 | **OPEN-DECISION** | Loop-µP (`2606.18524`): residual branch **× 1/N**, LR independent of N. We are pre-norm and §5 weight-ties layers, so our residual stream grows **linearly** in the loop count instead of √L. |
| 17 | **OPEN-DECISION** | **T = 2** is the default to measure against; both wins use 2. Ouro's **T=8** loss spikes and `2610.00673`'s own T=8 run say not to go higher by default. |
| 18 | **OPEN-DECISION** | **Assert on the exit distribution, not the loss** — with a small entropy coefficient and low warmup, `p(exit at step 1)` stays **1.00 for all 2,267 steps** while the model silently trains as a plain transformer. |
| 19 | **OPEN-DECISION** | The only curriculum in the corpus that supports **more than two** steps without the intermediate-step collapse (`2610.00673`). |
| 20 | **OPEN-DECISION** | Inactive tokens must skip deeper recursions **including their attention and KV work**. The `HybridAttnKind` / `build_hybrid_schedule` seam must express *which* tokens loop. |
| 21 | **OPEN-DECISION** | Loop-µP's **× 1/N** and Loopback's per-block-update are **two different fixes to the same problem**; Loopback argues for building the depth-attention path first. |
| 22 | **OPEN-DECISION** | Naive = `T` separate KV sets per token position; shared-KV cuts persistent cache sets **from fifteen to four** and removes **81–89%** of the continuation-loss penalty. Changes the Phase-1 memory budget at 1.5 BPW × 4M window. |
| 23 | **OPEN-UNKNOWN** | **Explicitly UNKNOWN.** No looped-model stability fix has been validated above a few billion parameters — our 4B target is **above that ceiling**. Gate on the spread across seeds, not the mean. |
| 24 | **RESOLVED 2026-11-12** | Decision **D-1** (§6.1): §7 proof target **#8** + gate **V30**. |
| 25 | **RESOLVED 2026-11-12** | Decision **D-2** (§6.1): §7 proof target **#9** + gate **V31**. |
| 26 | **RESOLVED 2026-11-12** | Decision **D-3** (§6.1): in scope — all three libraries, one attention core on the engine path. |
| 27 | **RESOLVED 2026-11-12** | Decision **D-4** (§6.1): §2.1a row **22**. |
| 28 | **RESOLVED 2026-11-12** | Decision **D-4** (§6.1): §2.1a row **23**. |
| 29 | **RESOLVED 2026-11-12** | Decision **D-5** (§6.1): both, sequenced — MTP in Phase 6, DSpine in Phase 6c. |
| 30 | **RESOLVED 2026-11-12** | Decisions **D-6** and **D-7** (§6.1): decisions model = a head + RL on the same ruler model; modality matrix = a coverage table with zero silent gaps. |
| 31 | **RESOLVED 2026-11-12** | Decision **D-8** (§6.1): gates **V28**, **V32**, **V33**; MX stays quarantined; both quant tracks stay in scope via §9b.2. |
| 32 | **OPEN-DECISION** | Native bridge vs reimplementation is a real fork — **default to reusing the C++ `quant::agi::WorldModel`** (§10R). |
| 33 | **OPEN-ACTION** | A deliverable, not a decision: create the `transformers/` docs system modelled on `code/docs/AGENTS.md` (tier taxonomy, word budgets, one-physical-line-per-paragraph rule). |

> **What "open" means here.** Phase 0 *is* the research phase — §11 opens with *"No implementation of routing, `G`/`S`, EAIN, or the sweep may begin until this completes."* An `OPEN-DECISION` bullet is a fork the implementer takes, and the plan already names the recommendation and the evidence behind it; an `OPEN-RESEARCH` bullet names the paper or the measurement that answers it; an `OPEN-UNKNOWN` bullet is one where **nobody knows yet** and the plan says so rather than guessing. **None of them is a missing decision in this plan** — that was Step 5's job, and it is done (D-1 … D-8).

### Phase 1 — Stabilise (fast, unblocks everything)
- Commit or explicitly park the **307 modified** `code/` files and **84 untracked** `transformers/` files. Do not start architecture on a dirty tree.
- Fix the **7 confirmed critical defects** (§10M), ordered by risk: `agi_flywheel.cpp (sandbox_compile_and_test :1867, std::system :1912)` (unsandboxed LLM-generated C++) → **~~`src/trainer/code_gen.cpp:236` JIT-generated attention stack overflow (untested path)~~ FIXED 2026-11-13 (T6.3/V20: heap buffer + loud boundary gate + `test_attention_v20_budget`, 60/60)** → **`src/server/production_gen.cpp:212` / `src/model/expert_parallel.cpp:134` / `tools/quant_server.cpp:150` (three unauthenticated `INADDR_ANY` listeners — the plan's old `serve.cpp:118` was the wrong file, wrong line and wrong claim; §10M)** → `Math.random()` verification gate → DDP no-op → `-march=native` → vacuous determinism gate.
- **Dead-code purge project-wide** (§2 rule) — including the known instances: `AttentionResidual` (zero call sites), `HybridAttnKind` all-STD stub, the **dead `inferno_hook_stability_plasticity`** and its unwired replacement (§4.6), the **dead `importance_factor_ = 8.0f`** field in `src/trainer/reward.cpp` **— RE-VERIFIED 2026-11-10: `importance_factor_` occurs exactly TWICE in the whole tree (`include/quant/reward.h:45` declaration `= 8.0f`, `src/trainer/reward.cpp:13` constructor init) and is **never read anywhere → confirmed dead**, the **dead `learningRate`** in the unmounted MAD router, the seven `packages/mad/*` stubs (either wire or delete — **wire, since §10R needs a router applier**), and the **dead MQA/GQA/SWA/ALiBi declarations** in `include/quant/inference_opt.h` (§2.1d).
- **Delete the telemetry `KVCacheQuantizer` stub and point the report at the real `Q4KVCache`** (§10Y.3). `src/core/telemetry.cpp:283` returns a **hardcoded `0.001f`** from `estimated_quality_loss()` and **prints it at `:321`** — a constant presented as a measurement. `quantize_old_states` (:248) quantizes nothing and `restore_for_attention` (:264) is a `memcpy`; the real implementation already exists at `src/model/kv_cache_quant4.cpp` (420 lines, Lloyd-Max 16-centroid, tested by `tests/test_kv_cache_quant4.cpp`). **Delete the stub, reuse the real thing** — §2 zero-dead-code and no-duplicates, one change. Gate **V28**.
- **Resolve the three ECC/continual stacks** (§4.8a) into one — this is a Phase-1 cleanup that unblocks Phase 4. **REMOVED — the user rejected ECC consolidation; the three stacks stay as they are.**
- Wire `packages/cf` into the npm workspace (`workspaces` is `packages/*/*`, which does not match `packages/cf`) or drop it — the stale `node_modules/@origin-ai/cf` symlink must not survive.
- Rebrand cleanup (§10D): the single `origin-ai/xhe` reference, `.dsh` → `.cf` with one-shot auto-migrate, DeepSeek branding pass (§10E) — **functionality preserved**. Also fix the `AGENTS.md` branding scars: `:18` *"Also Known As: CodeFusion, CodeFusion"*, `:20` *"Fork Origin: CodeFusion"*, `:376` *"Fork of CodeFusion"* (§10U).
- **Regenerate or delete `install_test/`** — it is a `cmake --install` output, 100% untracked, already drifted (126 shared names, 32 differ). Never hand-edit it (§4.8).

### Phase 2 — Architecture (the engine)

**The sweep across ALL of §2.1 — 21 model-layer sites PLUS the KAT layer.**

- **21 model-layer sites** (§2.1a rows 1-21). Beyond the anchor and the obvious MoE family, the ones most easily missed are: `hybrid_moe_model.cpp` (separate from `hybrid_block.cpp`), `mommoe_block.cpp` (a second independent `CrossModalAttention`), `native_quant_moe.cpp` (its own attention/FFN layer loop), **`adapters/tools/qwen35_engine.cpp` (a complete third Qwen3.5 decoder engine)**, `multimodal/multimodal.cpp` (five softmax-routed MoE models + `Perceiver`), `multimodal/multimodal_fusion.cpp` (`CrossAttentionFusion`), `multimodal/dense/fusion_layers.cpp` (a **second** `CrossAttentionBlock` under a colliding name), and **`src/inference/{inference_paging,inference_kv}.cpp`** (a fully implemented vLLM-style tiled `PagedAttention` and `flash_decoding`).
- **PLUS the KAT layer** (§2.1b) — `src/math/`, `src/kernel/`, `src/backend/`, `src/trainer/code_gen.cpp`. **Without this, the "definition of done" is unreachable**: those layers implement the literal `softmax(QKᵀ/√D)V`. The four duplication sites to fix: `ScaledDotProductAttentionFunction::forward` (`src/model/autograd_functions.cpp:17`, **forward and backward**), `src/trainer/code_gen.cpp::attention_flash` (:219, **plus the 2048-token score-buffer cap at :236**), `src/kernel/flash_attention.cpp` (:50), and **18 GPU backends** in `src/backend/`.
- **Header first, carefully**: `include/quant/transformer.h` is the interface contract — replacing it breaks 30+ files at once. Change the header and the `Attention` class together, then fix dependents in one pass. Also `include/quant/hybrid_scheduler.h` (`HybridAttnKind` — the routing seam) and `include/quant/moe_variants.h` (27 classes).
- **Preserve the on-disk schema.** `collect_named_tensors` (`model.cpp:138`) hardcodes `layers.N.attention.q_proj.weight` etc. Renaming weights breaks every existing checkpoint — **keep the tensor names, change the computation.**
- Implement `QK^T G(GS)` at `transformer.cpp:295`, keeping `scale = 1/√d_k` (357) intact.
- Implement **adaptive routing** (layer re-arrangement + learned gate) — the natural slot is `HybridAttnKind` / `build_hybrid_schedule`, built to **our** §5 design.
- Wire or remove the dead `AttentionResidual` (`transformer.cpp:629`).
- Resolve the dead declarations in `include/quant/inference_opt.h` — `MultiQueryAttention` (278), `GroupedQueryAttention` (296), `SlidingWindowAttention` (316), `ALiBi` (333) have **zero definitions** (§2.1d). Implement them in Fusion form or delete them.
- Build `.idx` lazy context loading (§8).
- Build window extension + doubling (§7) — greenfield (§10I).
- **Breakage surface**: 6 test TUs reference `Attention`/`flash_attention` — `test_transformer`, `test_wave6_model_feats`, `test_protected`, `test_inference_opt`, `test_multimodal`, `test_trainer_moe_multimodal`. They must be updated, not left broken.

### Phase 3 — Harness (CodeFusion) — build to the Cordis seam pattern

Every addition below follows §10O: **Service Definition + Provider + Consumer**, registered on a `ctx` key, mounted via a bundle patch, and made model-visible by extending `SessionEventMap`.

**The single most important behavioural swap (§10V):**

```
TODAY:   CONTEXT_WINDOW_EXCEEDED → agent/request-error → compact → retry
TARGET:  CONTEXT_WINDOW_EXCEEDED → extend window ×2    → retry, same history
```

1. **Window extension replaces compaction.** Intercept the two compaction triggers — `agent/pre-step` (`'pressure'`) and `agent/request-error` (`'context-overflow'`) — and route them to window extension instead. Stop emitting the `surfaceOp: { op: 'replace' }` `user/message` that is the **only** surface mutation summary compaction performs (§10V). Do **not** fork `compaction-basic`; disable or no-op the seam, since it is *one optional capability, not part of the agent-loop spine*.
2. **Provider-adapter harness** (§10G) — registered on `ctx.llm`, beside the two existing adapters.
3. **Thinking preservation across compaction** — highest-value single build (§10P). If extension is not yet complete and compaction still runs, subclass `BasicCompactionEngine` and override the **protected `summarize()`** (the sanctioned hook) so reasoning survives the checkpoint — respecting block-count alignment at `assembler.ts:136-146`. Also unblock retrieval: `packages/session-query/session-query/src/extraction.ts:70-73`.
4. **World-model capability family** (§10R) — 3 packages + `ctx` key + `packages/bundle/base/cordis.patch.yml` mount, bridging to the existing C++ `quant::agi::WorldModel`.
5. **Durable learned state** — new event type in `known-event-types.ts:1-68` + `SessionEventMap` declaration merge (precedent `packages/compaction/compaction/src/types.ts:9-69`). **Must be marked `ignorable: true`** or old readers will refuse to reconstruct (§10S). Decide `SESSION_FORMAT_VERSION` deliberately — it is pinned at `0` and there is no upgrade path (§10S).
6. **Outcome feedback loop** — wire the dormant `ModelRouter.reportOutcome` + `calculateRoutingScore` so `learningRate` is actually consumed, and persist `performanceCache`.
7. **Respect the block-type rule** — if reasoning or neuron state becomes a content block, **adapter, UI, compaction and durable replay paths must all honour it in one change**, and `block-end` must be emitted or `BlockAssembler.blocks()` throws (§10V).
8. **Build the `.idx`** (§8.1) — extend `session-query-sqlite`'s FTS machinery over context, with the bounded/lazy/invalidated/disposed semantics of `file-reference-local`'s `WorkspaceFileSearch`, persisted through `session-persistence-sqlite`. Evicted content goes to `S`, never vanishes (§8.1).

### Phase 4 — Neurons (EAIN)
- Design **Enhanced Artificial Intelligence Neurons** (§4) on top of the Phase-0 research, hosted in the existing AGI machinery (`src/agi/`, `include/quant/agi.h`).
- Reuse what exists rather than reinventing: ECC/Fisher consolidation, the stability-plasticity controller, `RewardModel` + prediction error, `StateMemoryEntry`, the MoE router as the "which unit fires" decision (§4.6).
- Build the **new unit-level layer** that is missing: per-unit time constant, threshold, refractory, local update rule, soma integration (§4.7).
- **Land in `include/quant/` only** — `install_test/` is a build output and is regenerated, never hand-edited (§4.8).
- Wire so models **train on these neurons** (V13). Benchmarks must show EAIN **defeating both humans and ordinary AI** (V15).

### Phase 5 — Benchmarks
- CS-Bench-1.0, CS-Bench-1.1, D&CC-Bench-1.0, MQC-Bench-1.0 (§9) — all greenfield. Follow the `cf-acp-snapshot` replay convention (§10J).
- **Add a benchmark gate to CI.** `code/scripts/run-gates.ts` is the existing CI gate runner (`ci-primary`, `ci-static`, `ci-coverage`, `ci-snapshot`, `ci-artifacts`, `ci-consumers`, `ci-windows-*`, `node-compat`, `check-all`, `hygiene`, `doc-sync`) — **no benchmark gate exists.** The new benchmarks need one, or they will rot like everything else the repo has no gate for.
- **Human baselines for CS-Bench** must be collected on the **identical question sets** — that is what makes V15 a real comparison rather than an assertion. The CS-1.1 questions are internet-harvested *"maan lo aisa ho gaya to kya karoge"* items, so a human response set is collectable.
- **MQC-Bench** needs the 1.5 BPW tier rule settled first (§9b.1) — otherwise it cannot report a number.

### Phase 6 — Training
- **Settle the 1.5 BPW tier rule first** (§9b.1) — `Q_1_K_H` per GAP-2, with **zero wire violations** (GAP-5). This is a live half-landed change, not something to start training against.
- Train **`sol-4-flash`** at **1.5 BPW** after the engine is complete. Retrain until results match exactly.
- Run all benchmarks on it and on **DeepSeek V4.1 Flash**; target **90%+** on Terminal-Bench-4.0-style tasks.

### Phase 6b — NCM (Next-Concept Modeling) — §3b

**Adopt incrementally, not as a rewrite.** The Fusion attention core (Phase 2) must be working first; NCM is layered onto it.

1. **Stage 1 — multiscale residual VQ-VAE tokenizer.** Train it to encode text into the discrete code hierarchy and decode back. **Freeze it.** Success criterion: reconstruction preserves **names, numbers and exact details** — because V5's PDF test needs exact line and page numbers, and §3b.4 flags reconstruction loss as fatal.
2. **Stage 2 — transformer generator**, trained with the tokenizer frozen, predicting levels in order with all codes of a level in parallel.
3. **Wire into `DenseModel::forward`** (`model.cpp:102`) — replace the next-token `lm_head` objective with per-level discrete-code logits, and replace the left-to-right generation loop with level-by-level decoding.
4. **First target: scale validity.** The paper's generators reach **725M params**; ours are **4B and 27B** (§3b.4). Prove quality holds at our size before relying on it.
5. **Measure against the 31× caveat** — benchmark NCM **against our own autoregressive baseline on the same hardware, batch size and quality checks**, not against the paper's diffusion comparison.

### Phase 7 — Docs, release, cleanup
- Naming docs (§1) — `transformers/` docs start from zero (§10K).
- Release notes, final memory cleanup (§13).

---

## 12. Standing responsibilities

Whole-project optimization · git commits and pushes · documentation · release notes · **GitHub CI fixes**.

CI notes: `code/` has 18 workflows on self-hosted pools (`cf-ubuntu-24-04-*core`, `cf-windows-2025-*core`) with Wine, bubblewrap, Playwright; `transformers/` has 4, with `-march=native` on Linux and known VS-generator fragility. Local scripts hardcode VS 2026 at `C:\Program Files\Microsoft Visual Studio\18\Community\`, and `tools/run_all_tests.ps1` expects a `build\tests\Release\` path that single-config Ninja builds do not produce.

---

## 13. Memory cleanup — DONE (moved, not deleted)

Per the user's instruction, memory was **emptied into a `temp/` folder at the workspace root** — nothing was deleted.

**Destination:** `C:\Users\thaku\temp\`

| Moved out of memory | Still in memory |
|---|---|
| `fusion-full-brief.md`<br>`fusion-transcript-1-context-rot.md`<br>`fusion-transcript-2-neurons-j-rsi.md`<br>`fusion-pending-work-neurons-astra.md`<br>`fusion-sprint-role.md`<br>`fusion-ci-fixes.md`<br>`check-before-launching-workflow.md`<br>`fusion-review-then-fix.md` | `user-prefers-hinglish.md` |

**`MEMORY.md` index trimmed to the single Hinglish line.**

This resolves the earlier caveat about losing the word-for-word transcript translations — **they are preserved, in `temp/`**, and this plan remains the single source of truth for the sprint itself.

---

## 14. Verification

Each target is pass/fail, checked by running real code — not by inspection.

| # | Target | How it is verified |
|---|---|---|
| **V1** | 4M native context | Load a 4M-token corpus; assert no truncation, no compaction, stable output quality at the far end. |
| **V2** | No compaction on fill | Fill to 4M; assert the context is **extended**, not compressed — check memory and output identity. |
| **V3** | Doubling | Fill → assert 8M; fill → assert 16M. Repeat; each fill must exactly double. |
| **V4** | 2M output limit | Generate to the cap; assert clean stop at 2M tokens. |
| **V5** | PDF test | 300-page and 3000-page PDFs. For N random words, assert exact **line + page number**. Headline demo. |
| **V6** | Never forgets | Long-run recall suite on `sol-4-flash`; retrain until it passes exactly. |
| **V7** | Live decisions + env learning | D&CC-Bench-1.0 — decisions taken live, plus measurable adaptation to environment. |
| **V8** | Sweep definition-of-done | A model trains through the **Fusion path only** — assert no traditional-attention code is reachable in a training run. |
| **V9** | Zero dead code | Static analysis / coverage: every symbol reachable, or deleted. Assert across **both** projects. |
| **V10** | Attention correctness | Unit tests at `transformer.cpp:295` proving `G`/`S` **reduce to the standard formula when disabled** — must be a strict superset of today's behaviour. **Refined by §5c.2:** the strict-superset property is required of the **multiplicative `G(GS)` term alone with `G ≡ 1`**. A Form-A (rectified / non-sum-to-one) normaliser **cannot** satisfy it and must ship behind a **separate flag** with its own gradient check (V19). |
| **V11** | Context-rot regression | Replicate the Chroma protocol (fixed Q&A, growing surrounding text); accuracy must stay **flat** where transformers decay. |
| **V12** | Lost-in-the-Middle regression | Place the answer top / middle / bottom; assert **no middle penalty**. **Refined by §5c.1:** also run on the **untrained** model — the U-curve is a geometric property present at step 0 (`2603.10123`), so testing only trained weights would mean tuning a geometric constant. Also assert the **influence-density curve is flat across positions** (`2607.17696`), not merely that accuracy matches. |
| **V13** | Neurons actually used | Assert training runs through the neuron abstraction — not a bypass path. **Refined by §5c.4:** additionally assert the **neuromodulated-plasticity path** is exercised (Backpropamine `2002.10585`-style — the modulator actually changes the update), since that paper's measured gains came from that path specifically. |
| **V14** | Benchmarks | CS-Bench-1.0/1.1, D&CC-Bench-1.0 (100 tasks each), MQC-Bench-1.0 — report **score/100** and percentage. |
| **V15** | EAIN beats **both** (§4.1a) | On every benchmark, report a **three-way comparison**: EAIN-trained model vs **human baseline** vs **ordinary-AI baseline**. Pass requires EAIN to exceed **both**. Human baselines must be collected on the identical question sets. |
| **V16** | Compaction is gone (§10V) | Assert a `CONTEXT_WINDOW_EXCEEDED` path **extends the window ×2 and retries with the same history** instead of compacting. Assert **no `surfaceOp: { op: 'replace' }`** `user/message` is emitted across a session that exceeds one full window, and **no `compaction/*` event** is appended. Assert the **reasoning block count is preserved end-to-end**. |
| **V17** | Zero dead code, re-checked after the sweep | Re-run V9 once Phase 2 completes — the sweep creates dead paths by definition, and every one must be resolved before Phase 2 closes. |
| **V18** | KAT layer actually computes the Fusion formula (§2.1b) | Grep the whole tree for the literal `softmax(QKᵀ/√D)V` construction in `src/math/`, `src/kernel/`, `src/backend/`, `src/trainer/code_gen.cpp`. **Assert zero occurrences in any path a training run can reach** — including the 18 GPU backends and the JIT-emitted C++ in `code_gen.cpp`. |
| **V19** | Forward/backward parity | The Fusion attention must have a **correct backward pass** — `ScaledDotProductAttentionFunction::backward` (`autograd_functions.cpp:107`) is a separate implementation of the same math. Assert a **finite-difference gradient check** against the forward: if `G`/`S` appear in forward, they must appear in backward, or training silently diverges. |
| **V20** | The 2048 generated-code cap is gone | `src/trainer/code_gen.cpp:236` (now **:258**) sizes the generated score buffer as `std::vector<float> scores(static_cast<size_t>(seq_len), 0.0f)` — heap, sized to the real seq_len; `generate_attention` rejects `seq_len > 2048` and non-positive shapes loudly (T6.3 fix, 2026-11-13, regression `test_code_gen::test_attention_v20_budget`). The remaining assertion: a generated kernel **at 4M context** must either stream/tile the softmax (capability work, still open) or the JIT path must not be used for long sequences. |
| **V21** | `.idx` is lazy and lossless (§8.1) | Assert: (a) a 4M-token context is **not** densely attended — the index is consulted for out-of-window content; (b) **content evicted from the active window is still retrievable** through `.idx`; (c) the index is invalidated on tool-result mutation and released on agent disposal, matching `file-reference-local` semantics. |
| **V22** | 1.5 BPW is exact on the wire (§9b.1) | Assert `format_wire_bpw(Q_1_K_H) == 1.50` exactly, and that (OC-G-5, zero BPW violations). Assert no name-vs-wire gap across the registry. |
| **V23** | NCM reconstruction fidelity (§3b.4) | Round-trip text through the multiscale VQ-VAE tokenizer: assert **names, numbers and exact strings survive reconstruction byte-for-byte** — on a corpus containing filenames, error strings, page/line references and numeric values. This gates V5 (the PDF test): if the hierarchy loses detail, the generator cannot restore it. |
| **V24** | NCM actually speeds up generation (§3b) | Benchmark NCM **vs our own autoregressive baseline on identical hardware, batch size and quality checks** (not vs the paper's diffusion baseline). Report **wall-clock per unit quality**, plus function-evaluation counts. A "speedup" measured against a different baseline does not count. |
| **V25** | NCM scales past 725M (§3b.4) | The paper's generators reach 725M params; ours are 4B/27B. Assert quality holds at target size on the same benchmarks before NCM is used for any headline result. |
| **V26** | Routing beats a fixed schedule (§5c.3) | `1803.08165` found fixed-repeat RNNs matched learned ACT. Assert our **learned routing gate beats a fixed-schedule looping baseline** on our own benchmarks. **If it does not, ship the fixed schedule and record the measurement** — the routing is not sacred, the compute saving is. |
| **V27** | Context-rot decay is flat with n (§5c.1) | The Chroma protocol (V11) shows *accuracy* is flat; also assert the **measured attention mass on the target token does not fall as `n` grows** — this is the mechanism, and Form B's `log m` normalisation exists precisely to hold it constant. |
| **V28** | **No fabricated metrics — anywhere** (§10Y.3, §10M) | Assert that no reported quality/compression/latency figure is a **hardcoded constant**. The known instance: `src/core/telemetry.cpp:283` returns `0.001f` from `estimated_quality_loss()` and `:321` prints it as *"Estimated quality loss: 0.10%"*. The rule, taken from `SPEC-INFERNO` Appendix R.4 and D-14: **a number that was not measured is reported UNMEASURABLE, never fabricated** — the same rule the 32× ratio already follows. Assert across the telemetry report, the benches and the index. |
| **V29** | **No unauthenticated network listener** (§10M) | Assert that every `INADDR_ANY` bind enforces auth or binds loopback only. The three known offenders: `src/server/production_gen.cpp:212`, `src/model/expert_parallel.cpp:134`, `tools/quant_server.cpp:150`. `src/server/http_server.cpp:367` is the **counter-example** — it binds all interfaces *and* enforces bearer auth on `/v1/*` (`:262-271`), which is the shape the other three must take. |
| **V30** | **32× Inferno speed floor** (decision **D-1**, §7 #8) | Run `inferno_bench` on the **target device** and assert `best_live_backend_GFLOPS / baseline >= 32.0`. If the ratio cannot be measured live, the harness must print **`UNMEASURABLE`** — never a number, never a pass. The instrument already behaves this way: `inferno/inferno_bench.cpp:471` prints `UNMEASURABLE` when CUDA is offline. |
| **V31** | **Fail-loud backend contract** (decision **D-2**, §7 #9) | Assert one explicit `case BackendType::` for **each of the 24** enum members in `src/backend/backend.cpp`; assert an unknown enum **throws** (never falls through); assert **no** path reports GPU GFLOPS while executing on the CPU. The known offender to fix first: `src/backend/gpu_compute_vulkan.cpp:1578` (the honest CPU fallback, `:1585`). |
| **V32** | **Industrial parity at equal BPW** (decision **D-8**) | For every format in the **69**-format ladder, assert measured quality **>= its industrial counterpart at the same BPW** (NEW-1's reference set: FP16, INT8, GGUF Q8_0/Q6_K/Q4_K, BitNet b1.58, Binary 1-bit, AWQ, GPTQ, MXFP4/6/8), **and** that the scale-fit quality floor (D-12) holds. **The MX family is quarantined (D-13)** and is exempt by being *out of the candidate set*, never by being quietly exempted. |
| **V33** | **The ladder is reachable and correctly cased** (decision **D-8**) | Assert `parse_format_name` accepts **all 69** canonical names and `format_to_regformat()` is lossless; assert the casing sweep (D-05) finds **zero** name-vs-wire mismatches project-wide, and that `format_wire_bpw(name) == format_bpw(format)` for every live id. |

**Infrastructure to reuse:** CTest via `add_quant_test_full` in `transformers/tests/CMakeLists.txt`; Vitest suites and the `CF_SNAPSHOT=replay` pattern in `code/`.

---

## 15. Source transcripts (preserve verbatim)

Full English translations exist for both — **the user demanded neither be forgotten, not one word**:

- **Transcript 1 — Context Rot:** 300-page PDF, context window as short-term memory, Chroma 18-model study, Lost-in-the-Middle, needle-in-a-haystack as a scam, 10-lakh-vs-2-lakh, attention as root cause, context engineering, RAG failure modes, recursive language model, Altman's "perfect context of your whole life".
- **Transcript 2 — Neurons / J / RSI:** Kattappa-Baahubali reasoning comparison, Einstein's three-step loop and the **"J" jump**, Google DeepMind 2026 paper, continuous self-update, **RSI**, Ilya's "It's time to scale SSI", human vs AI neuron, the Musk party, backpropagation / loss / parameters / RLHF, feelings as patterns, Hinton vs LeCun, **62.7% provider-neutral Astra**, ARC-AGI-3 mechanics, predictions aren't facts, genuine threat vs fear-mongering, AGI definition discipline.

### 15.3 Transcript 3 — Next-Concept Modeling (NCM)

The user supplied a 14-minute explainer video transcript and framed it as: *"ye ek aur transcript hai, NCM matlab Next-Concept Modeling. Isse tokens predict karne me speed badhegi! Isko bhi plan me add karne ka, ispe bhi research hoyega."*

**What the transcript covered** (21 chapters, summarised — the full text is in the conversation; the substance is captured in §3b):

1–3: the 300-page-PDF framing repeated; asking an AI to "write a short summary" produces one word at a time; the alternative is **sketch the shape of the whole answer first, then fill detail in a handful of passes** — that is NCM.
4: **autoregressive generation** — each token predicted from those before it, so step *n+1* must wait for step *n*; parallel hardware does not help because the sequence is serial.
5: **diffusion language models** generate many positions at once but trade quality for fewer refinement passes, and reprocess the whole sequence each pass.
6: **coarse-to-fine** — NCM is **not a new kind of transformer**; it uses a transformer but changes **what it predicts and in what order**. The drawing analogy: block in large shapes, then smaller shapes, then fine detail.
7: a **"concept"** is a code in a learned multiscale representation — **not** a human-readable idea.
8: two components — a **multiscale tokenizer** (multiscale residual VQ-VAE) and a **transformer generator**; **stage 1** train the tokenizer to encode/decode; **stage 2** freeze it and train the generator to predict the codes.
9: at each level the generator predicts **all codes of that level in parallel**, conditioned on earlier levels.
10: NCM vs diffusion — diffusion **revises** the sequence repeatedly; NCM **predicts a hierarchy** and moves on.
11: **function evaluations (NFE)** — one model evaluation; fewer NFEs does not automatically mean less wall-clock, so the paper also reports wall-clock.
12: the **XSum** experiment — comparable **ROUGE-L** at **31× faster**, 1,024 sequences, batch 16, single **H100 SXM**.
13: **what 31× does NOT mean** — not 31× faster than ChatGPT, not every task, not versus autoregressive models.
14: **LM1B** better generative perplexity than the strongest diffusion baseline at **21×**; **OpenWebText** competitive at **10×**.
15: **Sudoku** — global constraints; NCM beat both autoregressive and diffusion baselines at every difficulty with **fewer function evaluations**.
16: **WMT14 De→En** translation; **MBR decoding** generates candidates and picks the most-agreed one — which **costs extra compute**.
17: open questions — **scale**, **structured/bounded output format**, **reconstruction quality matters for names and numbers**, and baseline/setup dependence.
18: downloadable checkpoints exist on HuggingFace (XSUM, WMT14, Sudoku, TinyStories, LM1B; OpenWebText pending), but there is **no drop-in NCM assistant**.
19: **NCM is still an LLM** — it is an alternative text-*generation* approach, not the end of language models.
20: three lessons — the 31× is specific, the central idea is coarse-to-fine, and the right next step is **independent testing on your own baseline**.
21: it gives researchers a new way to study text generation.

**Every one of these claims was independently verified against arXiv `2610.14162v1` in §3b.6** — the numbers (31×, 21×, 10×, 8 NFE, 725M, the reconstruction percentages) all match the paper's own reported figures.

**Location:** both are preserved in `C:\Users\thaku\temp\` (moved there from the memory directory at the user's instruction — nothing was deleted), alongside `fusion-full-brief.md` and the other sprint notes.

---

## 16. Plan audit trail

The plan was verified by an adversarial review of 4 independent dimensions (workflow `wf_90a9828b-01d`, 4/4 agents). Two verdicts were **refuted** and produced material corrections, which are folded in above.

| Dimension | Verdict | What changed |
|---|---|---|
| **sweep-inventory** | 🔴 **REFUTED** | §2.1 rewritten. 5 → **21 model-layer sites**; the **KAT layer** added as a blocking deliverable (§2.1b); 6 test TUs added as breakage surface; dead MQA/GQA/SWA/ALiBi declarations surfaced; `.cpp` vs `.h` vs banner line-base confusion called out. |
| **neurons** | 🟡 **holds with corrections** | Stability-plasticity hook is **dead, not wired** (§4.6); `install_test/` is a **build output, never hand-edit** (§4.8); three parallel continual stacks noted, **not** to be consolidated (§4.8a); ~15 line anchors corrected. |
| **harness** | 🟡 **holds with corrections** | `99.9%` is **not** zero — 4 incidental hits (§10O); `packages/context/` **does** depend on `cf-compaction` (§10Q); `summaryText()` filters by **type, not role** (§10P); ~10 citation anchors corrected; `llm-replay` lives outside `packages/llm/`. |
| **scope-coherence** | 🔴 **REFUTED** | Header claim "Status: COMPLETE PLAN" was premature — the alias registry and the superseded-plan marking passed, but the sweep and the internal consistency did not. Both are now fixed. |

### Known remaining gaps (carried into Phase 0, not hidden)

- ~~The **KAT-layer inventory** does not exist yet~~ — **RESOLVED 2026-11-10.** §2.1b.1 now carries the **disk-verified** inventory: the KAT stack is `src/math/`, `src/kernel/`, `src/backend/`, `src/trainer/code_gen.cpp` (**not** a `src/code_gen/` dir — that was wrong); **20 backend files, of which exactly 4 carry a fused attention implementation** (cuda, hip, vulkan, full) — not 18; the other 16 are primitive-only. The remaining V8 work is the **decision**, not the inventory.
- `include/quant/*.h` may declare further **unimplemented attention variants** beyond the four found in `inference_opt.h`.
- **Not yet audited:** `src/server/`, `src/gle/`, `src/core/telemetry.cpp`, `inferno/`, `scripts/`, the `tests/` tree in full, and the sibling `code-fusion` project.
- The **line-anchor cleanup pass** is still outstanding — §2.1a and §10 carry only verifier-confirmed anchors.
- **External ground truth is absent** for 62.7% / 99.9% / 99.99% / 3–35% — these come from the user's transcript and the leaderboard they pasted. They are internally consistent but not independently confirmed.

### 2026-11-10 — research pass + code check, and a repair of the plan file itself

**The plan file was damaged and has been repaired.** The 2026-11-09 research pass left `pasted-content-id-43ed-ye-aur-melodic-puddle.md` in a broken state: literal junk inside the §3c.2 equations (`m_{ℓ,tm} = A·z_{**}**  — wait, correction:`), a corrupted `h_{typo}` write, six dangling duplicate fragments, a duplicated `### 3c.9` heading, a truncated transition-cache expression, a wrong `α=0`, and **the `## 4. Neurons — Req 1` H2 heading missing entirely** (H2s jumped `## 3c.` → `## 5. Architecture`, leaving `### 4.1`–`### 4.10` parentless). All of it is now repaired and re-verified: zero residual corruption markers, one `### 3c.9`, and the H2 sequence is contiguous again (`3` → `3b` → `3c` → **`4`** → `5` → `5c` → `6` …). **Pre-repair backup kept at `fusion/.rea-tmp/plan-backup-pre-repair-20261110.md`** (sha256-verified).

**Research added** — §5d (looped-LM frontier), §5e (Attention Residuals = the depth-axis mechanism for `G`/`S`), §5f (quantising looped models, the 1.5 BPW evidence). **Every arXiv ID now referenced anywhere in this plan — 56 distinct, including the 15 new ones — was re-verified live against the arXiv API on 2026-11-10: 56/56 resolve, none missing, none from memory.**

**Resolved:** §5c.5 item 1 (ASTRA) is no longer UNKNOWN — it is **reported but unconfirmed by OpenAI**, with OpenAI's own system card documenting the monitorability drop. §5c.5 item 4 (NCM appendices) is closed.

**Live code check (RESEARCH-4) — four Phase-0 items answered:** `src/math/math_avx2*.cpp` + `math_avx512.cpp` are **attention-free** (only generic elementwise softmax); the **2048-token cap** is confirmed at `src/trainer/code_gen.cpp:236`; the **stale `Cender/` comment** is confirmed at `include/quant/transformer.h:119–122` (**the plan's `116–118` anchor was wrong — corrected**); and **`importance_factor_` is confirmed dead** (two occurrences tree-wide, never read).

**Still open, and still on the critical path:** the §5d/5e/5f decisions added to Phase 0 (depth-axis variant, `G` in the quantisation set, loop-count default), the `G`/`S` formulation gate, the KAT-layer inventory, the line-anchor cleanup pass, and the outstanding audits (`src/server/`, `src/gle/`, `src/core/telemetry.cpp`, `inferno/`, `scripts/`, the `tests/` tree, the sibling `code-fusion` project).

### 2026-11-10 (later) — §5d rebuilt on the correct framing: loop vs traditional, attention, training

**The framing was corrected by the user, and the section was rebuilt.** The earlier §5d had drifted toward quantisation; the intended scope is **two kinds of transformer (traditional and loop), attention as the crux, and training as the topic.** §5d is now organised exactly that way: **§5d.0** the loop-shape taxonomy (model-loop / block-loop / layer-loop) → **§5d.1** what changes and what does not → **§5d.2** attention on three axes → **§5d.3** training → **§5d.4** the cost/quality market scan → **§5d.5** the actionable list for this engine. **§5f is demoted to a supporting deployment section** and **§5e is now labelled as axis 2 of §5d.2**.

**The single most important new result for us is Loop-µP (`2606.18524`):** loops are **not** extra depth, because the loops share weights — distinct layers add uncorrelated residual increments (sum ~√L) while a shared layer adds **positively correlated** ones at every loop (sum ~**N**, linear). The fix is **residual branch × 1/N with the learning rate independent of N**, and the LR then transfers up to **8 loops / 384 executed layers**. **Our `TransformerBlock` is pre-norm and our §5 routing weight-ties layers, so we inherit exactly this failure mode** — it is now a Phase-0 action with a V-gate.

**Also newly folded in:** the exit-gate collapse trap (`p(exit at step 1) = 1.00` for 2,267 steps with **no visible sign in the LM loss** — monitor the exit distribution, not the loss); the smoothed exit loss (**ε = 0.05**); the correctness-directed online depth curriculum; stochastic stopping (`2606.29983`); the **MR-Loop vs DR-Loop** recurrence-scheme taxonomy (`2609.33144`); and the practical recipe **`2610.00673`** (T = 4 from the start, two stages, 310B tokens instead of 7.7T, a 1.4B looped model beating a parameter-matched dense baseline on all 12 benchmarks).

**The load-bearing negative result:** the strongest open looped model (**Loopie**) **keeps its backbone's attention mechanism and sparsity pattern unchanged** — it changes the *schedule*, not the attention. So the sequence-axis work (§3.2 `G`, Softpick, the lost-in-the-middle theory) is **unchanged by looping**, and the only place looping genuinely changes attention is the **depth axis** (§5e) and the **per-token attention workload** (§5d.2 axis 3).

**Verification:** every arXiv ID now referenced anywhere in the plan — **67 distinct** — was re-verified live against the arXiv API on 2026-11-10: **67/67 resolve, none missing, none from memory.**

### 2026-11-10 (final) — §5d evidence polish: the survey is a preprint, and six more papers

**Citation correction.** The survey cited in §5d.3.1 as `202610.1404` is **not an arXiv ID** — it is a **preprints.org DOI**, `10.20944/preprints202610.1404.v1` (*Looped Language Models: A Survey and Meta-Analysis of Recurrent-Depth Transformers*, Azizi, Baghaei Potraghloo & Pedram, USC; snapshot 2026-10-06; 557 papers, 1211-claim ledger; repo `github.com/ArminAzizi98/looped-lm-survey`). It was re-checked live against the arXiv API first and **does not resolve there** (all `<YYMM>.1404` candidates return zero entries) — the plan now labels it explicitly so nobody hunts for it on arXiv again.

**Six newly surfaced papers, all live-verified and folded in:** **Loopback Transformer (`2611.07226`)** — the residual **interface** alternative to Loop-µP (per-block update vs full output; separate controls for input strength, total update weight, allocation); **LSTM-Style Looped Transformers with Shared KV Caches (`2610.33360`)** — the KV blow-up is **not inevitable** (fifteen → four persistent cache sets; 81–89% of the continuation-loss penalty removed by a final-10% consistency loss); **When Does Recurrence Become an Algorithm? (`2607.20594`)** — the budget law `v ~ n_train/T_train` and the finding that **weight tying flips the model onto a serial frontier** at the cost of extrapolation; **Stability and Generalization in Looped Transformers (`2604.15259`)** — fixed-point theory over local attractivity / input-dependence / geometry, and the proof that **without recall a looped model cannot become input-dependent**; **The Topological Trouble With Transformers (`2604.17121`)** — the complementary **depth-vs-step** recurrence-axis taxonomy; **Fully Looped Transformer (`2605.18797`)** — the two named instability sources (**gradient oscillation**, **residual explosion**), of which our plan currently addresses only the second.

**The survey's meta-findings, now in the plan:** the **risk triad** (exit-gate collapse that does **not** show in the loss, residual growth from tied updates, norm drift beyond the training horizon); **matched parameters ≠ matched inference compute** (ties on math, **trails on knowledge**); **~10× worse OOD standard deviations** across seeds; **retrofit cost ≈ 0.5% of pretraining compute** provided each iteration is anchored to the input; and the hard caveat that **no looped-model stability fix has been validated above a few billion parameters** — our 4B target is above that ceiling (**UNKNOWN at our scale**).

**Three new Phase-0 bullets** follow from this: decide the **residual interface** (Loop-µP `1/N` vs Loopback per-block update), decide the **KV-cache policy for `T` loops**, and add an **OOD-stability gate** on the spread across seeds rather than on the mean.

### 2026-11-10 (Step 1) — the eight sources the plan had never read, and a corrected §9b.1

**This step read eight source documents the master plan had never opened** and produced §10X, a
117-row coverage map (machine-checked), a 13-item gap list, and **one correction to the plan's own §9b.1**.

**The biggest gap is structural.** `transformers/SPEC-INFERNO.md` — the training-engine
specification — had **0 occurrences** in this plan. It is the document the user named explicitly
(*"ek SPEC-INFERNO.md bhi mil jaayega jo ki khud me hi ek to-do hai"*), and it defines the project's
headline bar: the **32× speed floor** over the baseline, on an **AMD Radeon Vega 7 / 5600GT iGPU**,
with the label printed at `inferno/inferno_bench.cpp:469` and `UNMEASURABLE` at `:471`. **This plan
never mentioned the 32× floor, GFLOPS, or the fail-loud backend contract — all 0 hits.** It also
never mentioned the three engine libraries (`quant_dense`/`quant_moe`/`quant_multimodal`,
**112 files / 11,878 LOC** verified live), MTP, the 26-modality matrix, or the decisions-model
training path.

**A contradiction in the plan's own §2/§16 was found and fixed.** §9b.1 stated that
`Q_1_K_L`/`Q_1_K_M`/`Q_1_K_H` "all return **1.0f**" and that the K-tier rework was *"uncommitted
in-flight work"*. **Live re-read: `types.h:48` `Q_1_K_H = 12, // 1.5` and `types.h:295`
`case Format::Q_1_K_H: return 1.5f;`** — the rework has landed, the ladder is frozen at **69**
(`types.h:147`; `DECISIONS.md` D-22), and **the L4 persistence defect is fixed** — all four clamp
sites now call `wire_format_valid()` / `legacy_format_id_remap()` from the new
`include/quant/format_compat.h` (`:35`, `:46`); the old predicate survives only in comments. **§9b.1
has been re-based on the live enum.**

**Two stale sibling documents were identified** (they are the *sources* for Operation Clean, not this
plan): `docs/operation-clean/DECISIONS.md` **D-23** still records L4 as a "LIVE DEFECT", and
`transformers/PROGRESS.md` still lists "L4 NOT done" and the "60 vs 69" question as open —
**both answered** (D-22, and the live enum).

**The user's ruling on quantisation was recorded as a first-class part of the plan** (*"Dono type ka
quant bhi denge ham!"*): **§9b.2** now separates **Track A** (the implemented 1.0–1.5 BPW wire ladder
— wire-honest but not yet quality-honest: MX **−21..−37 dB**, 8-bit K-variants lose, `Q_1` **3.53 dB**,
a quality inversion at higher BPW) from **Track B** (loop-aware PTQ — LoopQ `2605.16343` W4A4
**+68.8% acc / −87.7% ppl**, LoopQuant `2610.16368` **−65.3% memory / 1.7× decode**, and
`2609.30820`'s **feedback exposure at the loop-entry seam**) — and names the intersection **neither**
covers: **1.5 BPW on a *looped* model**.

**New Phase-0 to-dos:** the 32× bar as a V-gate · the backend count corrected to **24** and the
fail-loud contract adopted · the training-engine scope decision · the missed sweep site
`video.cpp:140` · MTP-vs-DSpine · the modality + decisions-model scope · and the Operation Clean
quality gates.

### 2026-11-10 (Step 2) — the KAT inventory re-derived from disk, and a new CRITICAL defect

**The KAT inventory is now measured, not asserted.** §2.1b.1 was rebuilt by scanning the tree
(`fusion/.rea-tmp/step2_kat_scan.py`, `step2_kat_classify.py`, `step2_read_sites.py`) and reading every
candidate site. **Three of the plan's own claims were wrong:**

1. **`src/code_gen/` does not exist.** The JIT generator is one file — `src/trainer/code_gen.cpp`
   (1,255 lines). The plan's KAT-layer list named a directory that is not on disk.
2. **"18 of 20 GPU backends" is wrong.** `src/backend/` has **20 files**, but only **4** carry a fused
   attention implementation — `src/backend/gpu_compute_cuda.cpp:296`, `src/backend/gpu_compute_hip.cpp:187`,
   `src/backend/gpu_compute_vulkan.cpp:1578`, `src/backend/gpu_compute_full.cpp:318` (whose ComputeShader literally says
   `softmax(Q*K^T/sqrt(D) + causal_mask) * V`). The other **16 are primitive-only** (they expose
   `gemm`/`gemv`/`softmax` as separate ops). **Naming trap:** `src/backend/gpu_compute_metal.cpp:88` declares a kernel
   literally called `attention_kernel` that is **not** attention — no softmax in its body (verified).
3. **`src/math/math.cpp:232` was mislabelled 🔴 CORE.** It is a **generic axis-parameterised elementwise
   softmax** — the *primitive* every attention path calls, not a duplicate of the formula. Relabelled
   🟡 SUPPORTING (plus 🟡 DEAD for the `vec_softmax_stable_avx2` wrapper that just forwards to the scalar
   version).

**A NEW CRITICAL DEFECT was found — a memory-safety bug, not a capability cap.** The plan had described
`src/trainer/code_gen.cpp:236` as *"a hard 2048-token ceiling in generated code"*. The truth is worse: the generated
score buffer is `float scores[seq_len > 2048 ? 2048 : seq_len]` (**`src/trainer/code_gen.cpp`:236**) while the generated kernel's
three loops run `j < seq_len` (**`src/trainer/code_gen.cpp`:237, 263, 267**) and write `scores[j]` (**:258**, **:264**,
**:267**). **For `seq_len > 2048` the JIT-emitted `quant_attention` overflows a stack buffer.** The path is
reachable — the only caller (`src/trainer/code_gen.cpp:825`) passes `spec.M` with **no clamp** — and
`tests/test_code_gen.cpp:43` only ever calls `generate_attention(8, …)`, so **nothing exercises
`seq_len > 2048`**. It is now §10M's **7th critical defect** and Phase 1 carries the fix (gate **V20**),
ordered second after the unsandboxed LLM-generated C++.
**UPDATE 2026-11-13 (T6.3/V20 — FIXED):** the heap `std::vector<float>` score buffer sized to the real
seq_len landed (`:258`), `generate_attention` rejects `seq_len > 2048` and non-positive shapes with a loud
`std::invalid_argument`, the `attention_basic` template got the same treatment, and `tests/test_code_gen.cpp::test_attention_v20_budget`
covers 8/2048/2049/8224/32768 plus the caller clamp — **60/60 tests pass** in build-norm, the emitted 2048
kernel compiles clean at `/W4` (clang-cl), and the gate `test_code_gen` is green. The **capability** half
(streaming/tiled softmax for >2048-token contexts) remains open as gate V20's second half.

**§16 reconciled (gap GAP-12).** The line *"The KAT-layer inventory does not exist yet — it is the single
largest unknown and the gate on V8"* contradicted §2.1b.1 and the Phase-0 bullet; it is now marked
resolved, and the remaining V8 work is stated as **the decision, not the inventory**.

### 2026-11-12 (Step 3) — every line anchor re-verified against disk, and the model identity fixed

**All 120 line references in this plan were re-resolved against disk** — 67 unique `file:line` anchors
plus 53 bare `:NN` continuation references — using `fusion/.rea-tmp/step3_verify.py`,
`step3_subanchors.py`, `step3_anchor_scan.py`. **66 of 67** anchors resolved on the first pass; **53 of 53**
continuations were in range with the cited line matching the claim. **Five claims were wrong. All five are
now corrected**, each against the live file rather than against memory:

| # | Wrong in the plan | Live truth | Site |
|---|---|---|---|
| 1 | `include/quant/transformer.h:116-118` (twice) | the stale *"Cender/ formula (Phase 19-23, owner-gated)"* note is at **`:119-122`**; `:116` is the FP8 roundtrip-error bound (`E4M3 <= 0.07`, `E5M2 <= 0.16`) | §2 "Rules for the sweep", §2.1a |
| 2 | `src/backend/gpu_compute_vulkan.cpp:1799` | `:1799` is **`vk_topk_softmax`**; the fused attention is **`VulkanBackend::flash_attention` at `:1578`** (honest-CPU-fallback comment `:1580`, *"SPIR-V not implemented"* `:1585`) | §16 Step-2 entry |
| 3 | `session-query/.../extraction.ts` (twice) — elided path | the real path is **`packages/session-query/session-query/src/extraction.ts`**; `:70-73` confirmed = `case 'text'` → `case 'reasoning': return []` | §10P(h), §11 Phase 3 |
| 4 | `src/code_gen/` (twice, still stale) | the JIT generator is **`src/trainer/code_gen.cpp`** — §2 and the Step-2 entry already said this, but the Phase-0 bullet and the **V18** gate still carried the old directory | §11 Phase 0, §14 **V18** |
| 5 | `run_with_timeout` `:1434-1493` | `:1434` is a `// ====` separator; the function opens at **`:1437`**, and the `std::system` execution point is `:1493` | §10M |

**Model identity — user ruling, 2026-11-12.** Two changes, applied everywhere they were named:

1. **Benchmark / reference model → DeepSeek V4.1 Flash** (`deepseek-v4.1-flash`). §1.1 and `review-tracking/MASTER_PLAN.md` **NEW-2** already carried this; the *machine-readable* block still said `model.bench = qwen-3.8-27b` — a stale leftover of the swap. Fixed. (The `tencent/Qwen3.8-27B-DSpine-b16` HF ids, the `Qwen3-8B` drafter policy, the `qwen35_engine.cpp` GGUF layout reader and the paper-measured Qwen baselines are **code and literature facts**, not the benchmark-model choice — they stay.)
2. **Ruler model → `sol-4-flash`** ("Sol 4 Flash") — chain `innova-x-1.1-4b` → `klawde-5-sol-4b` → `sol-5-flash-4b` → `sol-4-flash`. All **10** plan sites plus `review-tracking/MASTER_PLAN.md` **NEW-3** and **M2** now use the new name. The plan is the **architecture** authority and `MASTER_PLAN.md` is the **ladder** authority (§10X.0) — a rename that stayed only in one of the two would have re-created exactly the drift this step exists to kill.

**Two strings were subsequently renamed in that wave** (user ruling, 2026-11-12 — *"Sab rename
hoyega!"*): `SolIDX` (then treated as the `.idx` legacy magic, formerly `InNovaIDX`) and `tracesol`
(`transformers/scripts/plot_comparison_charts.py:149`, formerly `traceInnovas`). **D-30
(2026-11-13) reverted the wire-magic half:** the engine `.idx` accepts `Transformers-FusionIDX`
and `TransCenderIDX` only, while `SolIDX` is reserved for model manifests
(`transformers/docs/MODEL_MANIFEST.md`); `tracesol` stays. The old names survive only as
*attributed history* — see §6.1 and the 2026-11-12 rename-wave entry in §16.

**Method note for future passes.** Anchors were resolved against a **multi-root index** with
component-boundary suffix matching, because the plan cites three different trees by relative path:
`transformers/`, the archived CodeFusion monorepo, and the workspace itself. The CodeFusion
monorepo is **not** at `code/` root any more — `code/` is now the payloads/skills repo
(Code Swing owns it, and the user's rule keeps it on the side), while the monorepo the plan's
§10D / §10O–§10W describe lives at
**`code/windows/sonar/merger/code-fusion-dead-20261101/`** (the npm-migrated tree that matches
`packageManager: npm@12.0.2`, `package-lock.json`, and **no** `pnpm-workspace.yaml`), with
`code/windows/sonar/merger/deepseek-harness-master/` as the upstream master.

### 2026-11-12 (Step 3, addendum) — the bare-filename anchors, and a dangling section reference

**The first Step-3 regex required a directory separator, so 60 bare-filename anchors (`tools/serve.cpp:118`, `packages/cf/src/mad/core/god-runtime.ts:3679`, `packages/cf/src/mad/types.ts:1222`, `src/math/simd_math.cpp:266`, and 56 more) were silently skipped.** The regex was
widened to make the directory part optional; the anchor count went from **70 to 130**, and **129 of 130
resolve** — with one line-number mismatch that turned out to be a *file-resolution* ambiguity, not a bad
claim (`types.ts` exists in many packages; the right one is `packages/cf/src/mad/types.ts:1222`).

**Three further corrections, all confirmed against disk:**

| # | Plan said | Live truth |
|---|---|---|
| 1 | `serve.cpp:118` binds `INADDR_ANY` with auth disabled | `tools/serve.cpp:118` is `quant::ModelHTTPServer http_server(&model, args.port);` — the construction. The bind is `src/server/http_server.cpp:367`, **and that server enforces bearer auth** (`:262-271`). The genuinely unauthenticated listeners are `src/server/production_gen.cpp:212`, `src/model/expert_parallel.cpp:134` and `tools/quant_server.cpp:150`. **Three, not one.** |
| 2 | `god-runtime.ts:3679` / `:5264` / `:2317-2354` | Path disambiguated to **`packages/cf/src/mad/core/god-runtime.ts`** (6,476 lines). All three claims **verified verbatim**: :3679 `const random = Math.random()` → :3680 `const passed = random < basePassRate[checkDef.level]`; :5264 `testsPass: true, // Would check actual test status` (with :5266 `performanceOk: true` and :5267 `documented: true`); :2317 `private async calculateRoutingScore(`. |
| 3 | `packages/cf/src/mad/types.ts:1222` — `AdaptiveRoutingConfig.learningRate` has **exactly one occurrence in the entire repo** | **Confirmed true.** `packages/cf/src/mad/types.ts:1222` is `learningRate: number // How fast to update weights`, and `learningRate` occurs **exactly once** in that file — its declaration. |

**A dangling section reference, now real.** The plan referenced **§10M** nine times. There was **no §10M
in this plan** and **none in `review-tracking/DEFECTS.md`** either (its sections run **A–H**) — one
reference even pointed a `file://` link at DEFECTS.md's §10M. Item M of the §10 list has been promoted to
a **real `### 10M.` defect register** (§10M), so all nine references now resolve, and the defect list
has a proper anchor of its own.

**Final Step-3 numbers: 130 unique `file:line` anchors + 61 bare `:NN` continuation references = 191 line
references, every one resolved against disk, every cited line checked against the claim it supports.**

### 2026-11-12 (Step 4) — the seven remaining trees are audited, and the plan's "no attention found" claim was wrong for two of them

**All seven paths walked file-by-file** (`fusion/.rea-tmp/step4_tree_audit.py` + three detail scripts).
The full result is **§10Y**. Headline:

- **Clean (0 hits):** `src/gle/` (2 files / 406 lines), `inferno/` (5 / 1,324), `scripts/` (9 / 1,098),
  and the **CodeFusion monorepo** — 2,713 source files, **0** implementation-shaped hits (its 5,183 raw
  grep hits are base64 hashes in `package-lock.json`, minified CSS, and LaTeX prose in `skills/pdf/**`).
- **Not clean:** `src/core/telemetry.cpp` — the plan said *"no attention or softmax found"* and that was
  **false**: it holds a `KVCacheQuantizer` whose `estimated_quality_loss()` returns a **hardcoded
  `0.001f`** and is **printed** at `:321`. **New high-severity defect** (§10M, gate **V28**), and a
  duplicate of the real, tested `Q4KVCache` (`src/model/kv_cache_quant4.cpp`, 420 lines).
- **New sweep site:** `src/server/production_core.cpp:162` — the serve-time attention-shape authority
  (`KVCache cache(num_layers, max_seq_len, num_heads, head_dim)`). Phase-0 bullet added as row 23.
- **`tests/` is not clean and should not be** — 435 hits across 40 of 77 files. It is the **conformance
  surface**: `test_protected.cpp:134` (`flash_attention_forward`), `test_simd_math.cpp:110-124` (SIMD-vs-
  scalar softmax parity), `test_gpu_capability.cpp:29/300` (the **GAP-2 fail-loud** contract),
  `test_quant_mix.cpp` / `test_trainer.cpp` / `test_training.cpp` (the **attention-projection parameter
  enumeration** — the **Track-A** test surface for the new format), `test_code_gen.cpp` (the JIT path,
  `seq_len=8` only — why the §10M critical #2 is untested), and `tests/CMakeLists.txt` (registration).
  **A user quote in §2.1c claiming "6 test TUs" was an undercount — there are 9 strong sites — and the
  quote is preserved with the correction beside it.**
- **The CodeFusion tree moved.** The monorepo the plan's §10D / §10O–§10W describe is no longer at
  `code/` (which is now the payloads/skills repo). It is at
  **`code/windows/sonar/merger/code-fusion-dead-20261101/`** — the npm-migrated tree, matching
  §10D's `packageManager: npm@12.0.2` / no-`pnpm-workspace.yaml` facts. The Step-3 verifier was re-run
  against a multi-root index to prove every §10O–§10W path resolves. **Nothing in `code/` was
  touched.**

**New gates:** **V28** (no fabricated metrics anywhere) and **V29** (no unauthenticated network
listener). **New Phase-1 bullet:** delete the telemetry stub and point the report at the real
`Q4KVCache`.

### 2026-11-12 (Step 5) — the eight open decision gates are closed, and two id namespaces were split

**Two things happened in this step, and the second one was a defect the first one uncovered.**

**1. The `G-n` id space was colliding.** The plan's own Step-1 audit gaps ran `G-1` … `G-13`, and
**Operation Clean's quantisation rules** — the official ones, defined at
`review-tracking/MASTER_PLAN.md:15-19` (`Q_1` binary at 1.00, `Q_1_K_H` pure ternary at 1.50, M tier =
base + 0.25, GRP families follow the same rule, zero BPW violations) — *also* ran `G-1` … `G-6`. So
**"G-5" meant both "zero BPW violations" and "MTP is absent"**, and a reader had no way to tell which.
**Fixed:** the Operation Clean rules are cited as **`OC-G-1` … `OC-G-6`**; this plan's audit gaps are
**`GAP-1` … `GAP-13`**. **No id changed meaning — only the prefix** — and the namespace rule is stated
at the top of §10X.1 so it cannot drift back. (129 + 130 occurrences rewritten across the plan; the
Step-1 verifier was updated to assert the new ids and re-run green.)

**2. All eight open Phase-0 decision gates are closed — in §6.1, with the evidence for each.**

| # | Gate | Ruling in one line | Gate it lands in |
|---|---|---|---|
| **D-1** | GAP-1 — the 32× speed bar | **Hard V-gate**, target device **AMD Radeon Vega 7 / 5600GT iGPU**; unmeasurable ⇒ `UNMEASURABLE`, never fabricated | §7 #8 + **V30** |
| **D-2** | GAP-2 — backend count + fail-loud | **24 enum members, one `case` each, unknown enum throws, no silent CPU fallback.** The three counts are now separated: **24 members / 20 files / 4 with fused attention** | §7 #9 + **V31** |
| **D-3** | GAP-3 — training-engine scope | **In scope — all three libraries; one attention core on the engine path too** | Phase 1 CMake targets |
| **D-4** | GAP-4 — missed sweep sites | **Two sites: `video.cpp:140` (row 22) and `production_core.cpp:162` (row 23)** | §2.1a |
| **D-5** | GAP-5 — MTP vs DSpine | **Both, sequenced** — MTP is a training objective (Phase 6), DSpine is an inference accelerator (Phase 6c). They compose | Phase 6 → 6c |
| **D-6** | GAP-6 — decisions model | **A head + RL algorithm on the same ruler model**, starting with outcome-verified GRPO/RLVR — **not a third checkpoint** | Phase 4 + D&CC-Bench |
| **D-7** | GAP-7 — modality matrix | **A coverage table with zero silent gaps**; the count is **re-derived from the live tree**, never quoted from SPEC-INFERNO's own 25/26/27 | §9 modality axis |
| **D-8** | GAP-13 — Operation Clean gates | **Carried all** — industrial parity, quality floor, MX quarantine, bench honesty, reachability, casing | **V28**, **V32**, **V33** |

**What stays open, on purpose.** GAP-8 / 9 / 10 / 11 / 12 were **fact gaps, not forks** — they were closed
by the audit itself (SPEC-INFERNO's contradictory counts; L4 already fixed; 69-vs-60 already settled by
D-22; §9b.1's staleness fixed in Step 1; §16-vs-§2.1b.1 reconciled in Step 2). The genuinely open
**research** questions stay in §5c.5 and §3b.4 and remain **explicitly UNKNOWN**.

**Every Phase-0 bullet that carried a gap id is now marked `RESOLVED 2026-11-12` with its decision
number**, so the gate list and the decisions cannot drift apart.

### 2026-11-12 (Step 6) — the plan-loop closes: whole-plan verification, and the last honest accounting

**This is the last entry of the master-plan completion loop** (Steps 1-6). Everything below was
re-derived from disk or from a live response on 2026-11-12 — nothing from memory.

**1. Corruption scan — clean.** `.rea-tmp/step6_audit.py`: **0** U+FFFD replacement characters, **0**
mojibake sequences (the UTF-8-read-as-cp1252 family), **0** control characters, **0** double-encoded
sequences, **0** question-mark-run markers, corruption markers, or triple-angle-bracket markers (the scan looks for them by code point, so this sentence deliberately does not spell them out). **2.** H2 sequence contiguous and complete:
`Context -> 1 -> 2 -> 3 -> 3b -> 3c -> 4 -> 5 -> 5c -> 5d -> 5e -> 5f -> 6 -> 7 -> 8 -> 9 -> 9b -> 10 ->
10X -> 10Y -> 11 -> 12 -> 13 -> 14 -> 15 -> 16`; backticks balanced.

**3. Every arXiv id in the plan live-re-resolves: 67 / 67.** Checked with an HTTP `HEAD` on
`arxiv.org/abs/<id>` for each of the **67** ids (`.rea-tmp/step6_arxiv3.py`). *(The arXiv **API**
was returning HTTP 429 from this host during the check; the `arxiv.org/abs/` path is the same registry
and is not rate-limited the same way.)*

**4. Every Phase-0 bullet now carries an explicit status — 0 silently open.** All **33** bullets are
tagged and a **Phase-0 status ledger** table was added to §11: **12 RESOLVED**, **15 OPEN-DECISION**,
**2 OPEN-RESEARCH**, **1 OPEN-DESIGN**, **2 OPEN-UNKNOWN**, **1 OPEN-ACTION**. **An open bullet is not a
missing decision** — Phase 0 *is* the research phase (§11: *"No implementation of routing, `G`/`S`, EAIN,
or the sweep may begin until this completes"*), and each open bullet names the fork, the recommendation
and the evidence behind it. The two **OPEN-UNKNOWN** bullets say **UNKNOWN** in so many words — the
weight-tied U-curve constant (§5c.2 gap 5) and looped-model OOD stability above a few billion parameters
(§5d.4, our 4B target is **above** that ceiling). **Nothing is guessed.**

**5. Model identity — the user's ruling, applied everywhere.** Benchmark model = **DeepSeek V4.1
Flash** (`deepseek-v4.1-flash`); the ruler model we train = **`sol-4-flash`** ("Sol 4 Flash"),
renamed from `innova-x-1.1-4b` across all plan sites **and** in `review-tracking/MASTER_PLAN.md`
(**NEW-3** + **M2**). Two legacy strings were renamed in the same wave (user ruling, 2026-11-12 —
*"Sab rename hoyega!"*): **`SolIDX`** (then treated as the `.idx` legacy magic, formerly
`InNovaIDX`) and **`tracesol`** (`scripts/plot_comparison_charts.py:149`, formerly `traceInnovas`).
**D-30 (2026-11-13) reverted the wire-magic half:** `SolIDX` is model-manifest-only and
`TransCenderIDX` is the only accepted legacy engine alias; `tracesol` stays.

**6. The plan is implementation-ready.** Every gate is now a named, checkable thing:

| Kind | Where | Count |
|---|---|---|
| **Confirmed decisions** | §6 | 7 base + **8 new (D-1 … D-8)** in **§6.1** |
| **Proof targets** | §7 | **9** (2 new: the 32× speed floor, the fail-loud backend contract) |
| **Verification gates** | §14 | **V1 … V33** (6 new: **V28** no fabricated metrics, **V29** no unauthenticated listener, **V30** the 32× floor, **V31** fail-loud backends, **V32** industrial parity at equal BPW, **V33** ladder reachability + casing) |
| **Defect register** | §10M | **7 critical + 19+ high**, every anchor re-verified |
| **Tree audits** | §10Y | **7 paths**, each with the grep command and its output |
| **Source coverage** | §10X | **117 rows**, **13 gaps** (now **GAP-1 … GAP-13**), **0 orphans** |

**7. What the loop did *not* do, deliberately.** No implementation code was touched — the *"Go."* gate
stays closed, and this loop was research + plan only. `code/` was read, never written (it is now
the payloads/skills repo; the monorepo this plan describes is archived at
`code/windows/sonar/merger/code-fusion-dead-20261101/`). The one implementation-side change made
anywhere is the **plan-side** rename in `review-tracking/MASTER_PLAN.md`, which is a document, not code.

**8. The honest remainder.** **15 OPEN-DECISION + 2 OPEN-RESEARCH + 1 OPEN-DESIGN + 1 OPEN-ACTION
bullets remain in Phase 0** — by design, because Phase 0 *is* the research phase and closing them by
fiat would be inventing results. Each is now explicitly tagged, has its evidence named, and is
unambiguously a Phase-0 deliverable rather than a silent gap. **The plan's next action is to execute
Phase 0**, not to plan further.

### 2026-11-12 (rename waves) — **Sol 4 Flash** (né Sol 5 Flash), `SolIDX`, `tracesol`, and `.plan/` is now the workspace

**User ruling, verbatim:** *"Sab rename hoyega! … Model ka koi naam bhi suggest kar raha hu — filhaal ke liye
ham Sol 5 Flash naam choose kar rahe hai! Har jagah karne ka! Jaise ki SolIDX and tracesols ya tracesol kar
sakta hai!"* — and *"Saara ka saara plan ko /.plan/ me mai daal diya hu … sab isi folder me daal diya!"*.

**1. The model is `Sol 4 Flash`.** Wave 1 named it *Sol 5 Flash* the same morning; the user superseded that name hours later — see item 5. Rename chain, applied everywhere:

| Stage | Machine id | Display name |
|---|---|---|
| original | `innova-x-1.1-4b` | Innova X 1.1 4B |
| first rename (earlier today) | `klawde-5-sol-4b` | Klawde 5 Sol |
| second rename (same day, **superseded**) | `sol-5-flash-4b` | Sol 5 Flash |
| **now** | **`sol-4-flash`** | **Sol 4 Flash** |

Plan sites: alias registry §1.1, the machine-readable block (`model.train`), §6 row 7, §9b, §9b.2 Track A,
§10X GAP-13, the OC-MASTER coverage row, Phase 6, V6 — **plus** `review-tracking/MASTER_PLAN.md` **NEW-3**
and **M2**, and `transformers/PROGRESS.md`. **16 occurrences** of `klawde-5-sol-4b`, **7** of
"Klawde 5 Sol", **1** bare "Klawde" — all renamed, zero left.

**2. Both legacy code strings are renamed — this was explicitly overridden by the user.**

| Old | New | Where | Consequence |
|---|---|---|---|
| `InNovaIDX` | **`SolIDX`** | `include/quant/quant_format.h:206`; `src/codec/quant_format.cpp:640`, `:680`, `:687`; `install_test/include/quant/quant_format.h` | The reader's legacy branch now matches `SolIDX` at **7 bytes incl. NUL** (was 10 for `InNovaIDX`). **Any `.idx` file written by the old InNova-era writer will no longer parse.** The current writer magic `Transformers-FusionIDX` (22 B) is **untouched** — the live on-disk format is unchanged. |
| `traceInnovas` | **`tracesol`** | `transformers/scripts/plot_comparison_charts.py:149`, `:180` | Cosmetic — a Plotly series variable. No behaviour change. |

> **Correction (2026-11-13, D-30):** the `InNovaIDX -> SolIDX` wire rename in item 2 is **reverted**.
> A model name is not an engine wire identity. The `.idx` reader accepts `Transformers-FusionIDX`
> (22 B, current) and `TransCenderIDX` (15 B, the engine's former name — "formerly known as") only;
> `SolIDX` and `InNovaIDX` are rejected. `SolIDX` (7 B incl. NUL) is now the reserved magic of the
> model manifest, specified in `transformers/docs/MODEL_MANIFEST.md`. `tracesol` stays — it is
> cosmetic. The full record and the test proof are in the D-30 entry below.

The plan previously said *"Two strings must NOT be renamed … renaming them would break on-disk format
compatibility."* **The 2026-11-13 D-30 ruling restored that original compatibility rule for the engine
wire magic**: the engine keeps its own identity, and the model name moves to a separate manifest
namespace. Pre-rename copies of both code files are in `fusion/.plan/.rea-tmp/`.

**3. `~/.claude/plans/` → `.plan/` — the workspace moved, and the plan followed.** The user consolidated
**every** planning artefact into `fusion/.plan/`: the master plan, `PLAN.md`, `review-tracking/` (with
`DEFECTS.md`, `MASTER_PLAN.md`, `workflow_extracted/`), `docs/operation-clean/`, and the whole `.rea-tmp/`
script+backup set. `~/.claude/plans/` is now **empty**. Therefore:

- The authoritative path of this document is **`C:\Users\thaku\Workspaces\fusion\.plan\pasted-content-id-43ed-ye-aur-melodic-puddle.md`**.
  Every `~/.claude/plans/…` / `C:\\Users\\thaku\\.claude\\plans\\…` reference inside the plan was rewritten to the `.plan/` path.
- Every acceptance script lives in **`fusion/.plan/.rea-tmp/`** and was re-pointed at the new path.
- **No file was deleted** — this is a move, and the backups in `.plan/.rea-tmp/` preserve the pre-move state.

**4. What still names the old models, on purpose.** Three kinds of mention survive, all attributed:
(a) the rename chain itself (`innova-x-1.1-4b` → `klawde-5-sol-4b` → `sol-5-flash-4b` → `sol-4-flash`) in §6, §16 and
`MASTER_PLAN.md`; (b) `InNovaIDX` / `traceInnovas` inside this rename-wave entry and the §6.1 block, where
they are the *former* names being documented; (c) the `tencent/Qwen3.8-27B-DSpine-b16` **HuggingFace repo
ids** and the `Qwen3-8B` drafter policy in §3c — those are **third-party artifacts and literature
baselines**, not our model, and renaming them would be a factual error.


**5. Second rename, same day — the name is exactly `Sol 4 Flash`.** The user's 14:23 ruling
(*"plan updated to exact Sol 4 Flash bolne ka mood, koi 4B / 4b waala suffix ya prefix nahi chahiye!
Exact means exact! Har jagah sab kuchh change maar!"*) supersedes wave 1's *Sol 5 Flash*.

| Field | Value |
|---|---|
| Machine id | **`sol-4-flash`** |
| Display name | **`Sol 4 Flash`** |
| Forbidden | any `4b` / `4B` **in the id or the display name** (`sol-5-flash-4b`, `Sol-4-Flash-4B`, ...) |
| Not forbidden | parameter-count facts elsewhere (*"4B parameters, 1.5 BPW"*, *"our models are 4B and 27B"*) — those are measurements, not names, and renaming them would make the plan lie |
| Applied to | every live reference in this plan (alias registry §1.1, `model.train`, §6 row 7, §9b, §9b.2, §10X GAP-13, the OC-MASTER row, Phase 6, V6, §16), plus `review-tracking/MASTER_PLAN.md` **NEW-3** + **M2** and `transformers/PROGRESS.md` |
| Preserved | the verbatim user quote in §6.1 (annotated, never rewritten) and the chain rows above |


### 2026-11-12 (post-loop audit) — the holes the abandoned session left behind

The MCode session `mvs_022061eb8f2c428697f43df4a5fd8d9f` ended without answering the user's final
instruction, and an independent re-run of its own verifiers found work that was **claimed but not
landed**. Everything below was fixed in this pass; **nothing is carried forward open.**

| # | What the session claimed | What was actually true | Fix |
|---|---|---|---|
| 1 | *"`verify_step5.py` -> STEP 5 ALL CHECKS PASSED (62 checks)"* | The verifier still expected `klawde-5-sol-4b` and the **pre-move** `fusion/review-tracking/MASTER_PLAN.md`, so it **failed** (2 FAIL + `FileNotFoundError`). The script written to repair it, `fix_v5_after_rename.py`, was saved to `fusion/.rea-tmp/` (the **old** directory) and **never executed**. | verifier re-pointed and updated; **re-run green** |
| 2 | *"the other 16 are primitive-only (… + `igpu_zero_copy.cpp`)"* | **False.** `src/backend/igpu_zero_copy.cpp:1127` `IGPUZeroCopyTrainer::forward_attention` is a **naive composed attention** with an inline softmax — the 5th attention implementation in `src/backend/`, and a sweep site. The split is **4 fused + 1 composed + 15 primitive-only**. | §2.1b.1 re-based on disk; **D-4** and **GAP-4** extended to three sites |
| 3 | *"64 scripts re-pointed at `.plan/`"* | Only the **input** paths were re-pointed. `step3_verify.py` and `step3_subanchors.py` still **wrote their reports** to `fusion/.rea-tmp/`, and 8 stale artefacts stayed there. | output paths re-pointed; stale copies removed |
| 4 | `install_test/include/quant/quant_format.h:206` | The `InNovaIDX -> SolIDX` rename touched **3 of the 4** sites. This duplicate header still read `magic_size_ = 15; // 15 = TranscenderIDX, 10 = legacy SolIDX` — and in the main header the comment became *"10 = legacy **SolIDX**"*, which is nonsense: `SolIDX` is **6 chars + NUL = 7**, while 10 was the **old** `InNovaIDX` length. | both comments corrected to `7`; **superseded 2026-11-13 by D-30** — the `SolIDX` branch is removed from the engine path (`TransCenderIDX` is the only legacy alias; `SolIDX` is model-manifest-only) |
| 5 | `PLAN.md` | Its own Files table still pointed at `.plan-tmp/PLAN.md` and `fusion/.rea-tmp/` after the `.plan/` move — the loop's plan contradicted reality. | paths corrected |

**Two further corrections in this pass, both from the user's 14:23 ruling:**

- **The ruler model's name is exactly `Sol 4 Flash` / `sol-4-flash`** — no `4B`/`4b` suffix or prefix
  in the id or the display name. Wave 1 of the same day had chosen *Sol 5 Flash*; that name is
  superseded and the chain is recorded (`innova-x-1.1-4b` -> `klawde-5-sol-4b` -> `sol-5-flash-4b` ->
  `sol-4-flash`) in §6, §16 and `MASTER_PLAN.md` **NEW-3**. Parameter-count statements
  (*"4B parameters, 1.5 BPW"*) are **facts and stay** — only the *name* was narrowed.
- **"No detail may be missed" now has a mechanical backstop:** the three audit holes above were all
  found by re-running the session's own verifiers and grepping the disk, not by reading the plan. The
  verifiers are the contract; a green verifier that tests the wrong string is worse than a red one.

**6. arXiv citations re-verified against the live site, in a browser this time.** The earlier pass proved
`67/67` with `urllib` HEAD requests, although the user had explicitly asked for the **browser**
(*"arXiv ke liye browser use kar le, `/browser-use:control-in-app-browser` kar!"*). Both methods now ran:

| Method | Coverage | Result |
|---|---|---|
| In-app browser (`preview_navigate`, fresh tab) | 9 ids — every `2611.*` id, every `2610.*` id cited for the loop/quant work, `2605.16343`, `2605.20670`, `2609.36173` | **9/9 render**, page titles match the plan's claims (e.g. `2610.14162` → *"Next-Concept Modeling: Fast, Parallel Coarse-to-Fine Text Generation"*, `2611.07226` → *"Loopback Transformer: Towards a Unified View of Residual Looped Transformers"*, `2610.16368` → *"LoopQuant: Accurate and Efficient Post-Training Quantization for Looped Transformers"*, `2609.30820` → *"Quantizing Looped Transformers: Feedback Exposure and Calibration Blindness"*) |
| `urllib` HEAD, 6-way parallel, 4 retries on 429/503 | **all 67 ids** | **67/67 HTTP 200** |

**No id was removed or replaced in this pass** — the two methods agree, so the citation set is stable.
Report: `fusion/.plan/.rea-tmp/arxiv_recheck.json` (`arxiv_recheck.py` is re-runnable).


### 2026-11-12 — workspace rename (`code-fusion` → `code`, `transformers-fusion` → `transformers`) + deleted-docs archive + full re-verification

**The directories were renamed by the operator** — both repos live inside `fusion/` ("fusion to
hai hi"), so `code-fusion/` → `code/`, `transformers-fusion/` → `transformers/`, and the remotes
became `https://github.com/origin-labs-ai/code.git` / `https://github.com/origin-labs-ai/transformers.git`
(old `*-fusion.git` URLs redirect). **What changed in this plan and its tooling:** every
path-shaped reference and `.git` URL — 93 live files swept (plan, `PLAN.md`, `review-tracking/`,
`docs/operation-clean/`, every `.rea-tmp` script, `transformers/PROGRESS.md`, `code/arch`,
`code/payloads`). **What deliberately did NOT change:** verbatim operator quotes, the §1
alias-vocabulary table (CodeFusion / Transformers-Fusion / TransCender are names, not paths) and
historical evidence dumps. Full backup: `.plan/.rea-tmp/rename-sweep-backup-20261112-182006/`.

**Deleted-docs archive port (`.plan/_archive/`):** every doc ever deleted from both repos is now
recovered **once, reference-only** — 288 files / ~10.6 MB (README 5,925 lines, `docs/` 38,
`repo/memory/` 15, `TransCender.png`; **`InNova.png` stays deleted** per ruling). This port is
the reference pattern for future archived docs: *"sab bas reference ke liye uthaa raha hu"* —
future docs are redesigned fresh.

**Effort-slider decisions (merged from the *Current Strike* thread, context-only):**
`code/slider/effort` (`dsh-claude-effort-slider` 0.9.4, 6-stop, 38/38 tests) is a **DSH plugin →
Sonar (Plus)** native; **Zenix** (Claude Desktop, plain Electron + React, hooks present) would
need a port (A DOM-inject / B native rebuild). Operator: *"look waisa implement karenge, Sonar
me bhi implement karenge!"* → then *"Dono baad me karenge!"* — **both parked**. Full log:
`.plan/docs/operation-clean/DECISIONS.md` **D-24…D-26**.

**Full re-verification after the sweep — every verifier exit 0:** `verify_step1.py`
(117/117 rows · 117/117 headings · 13/13 gaps) · `step2_fix2_verify.py` (PASSED) ·
`step3_verify.py` (**156/156 anchors, 0 problems**) · `step3_subanchors.py` (**85/85, 0 out of
range, 0 unresolved**) · `verify_step5.py` (65 checks) · `step6_audit.py` (PASSED) ·
`arxiv_recheck.py` (67/67).

**No implementation code was touched — the "Go." gate stays closed.**


### 2026-11-13 - naming normalisation: `TransFormers-Fusion` -> `Transformers-Fusion` (D-28)

The engine's product name lost its capital `F`: **Transformers-Fusion**. The change is
byte-length preserving, so every size-derived fact in this plan (file sizes, archive manifest
byte counts, wire budgets) stays valid. The sweep covered the plan tree, the decision log,
the review-tracking documents, the operation-clean docs, the engine's sources, headers, tests,
benchmarks, build scripts and CI workflows, the launcher payloads and the recovered archive.

**The wire format was not broken.** The `.idx` magic moved from `TransFormers-FusionIDX` to
`Transformers-FusionIDX` - both 22 bytes, so the layout is identical - and the reader now
accepts **both** spellings, so files written by earlier builds keep decoding. The writer emits
the new spelling only. `TransCenderIDX` stays as the legacy engine alias. `SolIDX` was briefly
treated as a third engine magic during the 2026-11-12 rename wave, but **D-30 (2026-11-13)
retired it from the engine path** and reserved it for model manifests — see the D-30 entry below.

### 2026-11-13 - naming cleanup: Zenix-CC -> Zenix + alias-registry duplicates (D-29)

The native Claude Desktop seat is **Zenix** - the `CC` suffix is removed from the folder
(`windows/zenix`), registry entries and current-state docs. The component folders and GitHub
repos carry no `-fusion` suffix (`code/`, `origin-labs-ai/code`; `transformers/`,
`origin-labs-ai/transformers`) - reaffirming D-24 - while the product names **CodeFusion** and
**Transformers-Fusion** stay unchanged (D-28). The §1 accepted-variants table and the §1.1
alias registry each listed `Transformers-Fusion` twice; the duplicates are removed. Current
tooling/docs updated: `code/scripts/rebrand/fix-zenix.mjs` (renamed from `fix-zenix-cc.mjs`),
`code/scripts/rebrand/migrate-arch.mjs`, `.plan/review-tracking/FINAL_REPORT.md`,
`.plan/review-tracking/PROGRESS.md`, `.plan/telemetry/gen_dashboard.py`. Historical evidence
(the 2026-10-27 report row, the 2026-11-01 listing, `.plan/_archive/`) keeps its dated
spelling and carries a correction note instead. Full record: `DECISIONS.md` D-29.

### 2026-11-13 — wire-magic identity correction: `SolIDX` is model-only, `TransCenderIDX` is the engine alias (D-30)

**Trigger, verbatim:** *"ye TransCenderIDX kyu SolIDX banaa? Bhai, Seedha matlab ye tha ki
Transformers-FusionIDX / TransCenderIDX same cheej the yaani TF = TC tha, Sol to wo model ka naam
socha gaya jo ki train kara jaayega ya fine tune karaa jaayega, ye kya jhol ho gaya!"* — and
*"InNovaIDX bhi nahi rakhna hai naa! Hame TransCenderIDX / Transformers-FusionIDX dono is also
known as ya formerly known as bhi daal sakte hai!"*

**The defect.** The 2026-11-12 rename wave treated `SolIDX` as the new name of the `.idx` legacy
magic and shipped a 7-byte reader branch. That conflated two namespaces — **engine wire identity**
and **model identity** — and it made old 10-byte `InNovaIDX` files unreadable. The `.idx` header
identifies the engine, so a model name must never enter the magic. The correct equivalence is
`Transformers-FusionIDX` = current engine identity and `TransCenderIDX` = the same engine's
"formerly known as" alias; `Sol` is only the trained model family (`sol-4-flash`).

**Ruling (D-30).**

| Namespace | Accepted | Rejected |
|---|---|---|
| Engine `.idx` | `Transformers-FusionIDX` (22 B, current); pre-D-28 capital-F spelling (same 22 B, read-only); `TransCenderIDX` (15 B, legacy "formerly known as") | `SolIDX` (7 B), `InNovaIDX` (10 B) |
| Model manifest | `SolIDX` (7 B incl. NUL), reserved and specified — no engine consumer | — |

`tracesol` stays as the cosmetic Plotly series name; it is not a wire identity.

**Code (2026-11-13).**
- `src/codec/quant_format.cpp`: the `SolIDX` reader branch is removed; `TransCenderIDX` remains the
  only legacy engine branch. The writer still emits `Transformers-FusionIDX`.
- The pre-D-28 capital-F magic is compared **byte-wise** (`"Trans"` + `'F'` + `"ormers-FusionIDX"`)
  so the source tree never carries the old spelling.
- Reader minimum size is **23 B** (15 B legacy magic + 8 B header), replacing the 15 B guard that
  was sized for the retired 7 B magic.
- Every early return after ownership transfer nulls `data_` as well as `mapped_file_`; the
  22-byte-magic-only probe exposed a dangling `data_` that made `valid()` return true.
- `include/quant/quant_format.h` and `install_test/include/quant/quant_format.h` comments corrected
  to describe the two engine magics only.

**Tests.** `tests/test_sha256_corrupt.cpp` gained **Test 8**: `TransCenderIDX` opens and yields the
same tensor names; `SolIDX` and `InNovaIDX` are rejected. Proof:
`build-norm/tests/test_sha256_corrupt.exe` -> **28 tests, 0 failures, exit 0**;
`SHA256_TEST_LOG.md` regenerated.

**Documentation.**
- `transformers/README.md` §9 and §12 rewritten: engine wire identity vs model identity.
- `transformers/PROGRESS.md`: dated D-30 correction bullet; the 2026-11-12 rename-wave and post-loop
  records are marked superseded.
- **New** `transformers/docs/MODEL_MANIFEST.md`: normative `SolIDX` model-manifest specification —
  7-byte magic, version, JSON length, version-1 fields, compatibility rules and current status.
- `.plan/docs/operation-clean/DECISIONS.md`: D-30 appended.
- `.plan/telemetry/TODO-TREE.md`: T3.2 closed; T3.5 annotated as superseded.

**Why `SolIDX` has a spec but no implementation.** No model-manifest consumer exists in the tree
today — the only manifest artefacts are `tools/dataset_manifest.schema.json` and the `PackManifest`
test struct. The project rule is zero dead code and zero stubs, so the format is documented as
**reserved**, not implemented. The first consumer must add a writer, a reader and a regression test
before the status changes to **implemented**.

### 2026-11-13 (grind pass) — T1.1 closed: the G/S design note lands as §5c.6

The Phase-0 ledger's **OPEN-RESEARCH #4** is closed: the ten §5 papers
(`2603.10123`, `2603.15031`, `2605.18855`, `2610.13630`, `2607.27230`, `2607.09694`,
`2606.18524`, `2610.00673`, `2605.16343`, `2610.16368`) were deep-read for this design
note — abstracts fetched live from arXiv this session, bodies consolidated against the
verified §5d/§5e/§5f extraction. The written design is **§5c.6**: eight design statements
for `G` (Form-B backbone on both axes, attention-map readout instead of a new router,
r-dimensional routing keys, Form C as a labelled hypothesis, delta-based depth entries with
a contrast V-gate, the full exit-gate specification, the work-shrinking per-token policy,
and the pre-norm risk note with Form A quarantined behind a flag) and six for `S`
(bounded sliding-window index, dual sequence/depth axes, position-independence, the shared-KV
policy with its numbers, the loop-entry identity path, and quantisation-first discipline).
**Every remaining fork keeps its ledger id — #6, #11, #12, #13, #14, #16, #17, #18, #20, #21,
#22 — with recommendations stated and rulings explicitly left to the operator** (D-15
delegates priorities, not rulings). Ledger: OPEN-RESEARCH 2 → 1, RESOLVED 12 → 13;
TODO-TREE T1.1 ticked. The dashboard (`gen_dashboard.py`) was regenerated after the change.
No implementation code was touched — this is a research close-out.
