# Verified Model and Checkpoint Details  
**Model:** We confirmed that **Qwen3.8-27B** is an *official* Alibaba model – a native dense vision-language LLM with ≈27 billion parameters, Apache-2.0 open license. Its architecture is fully dense (no MoE experts) and includes a 262K native context (extendable to 1M). The official weights are released and open-source. On Hugging Face, the Qwen3.8-27B checkpoint is split into **18 safetensors shards** (BF16 format) totaling about **55.6 GB**. The shards range ~2.1–4.0 GB each, and an index file ties them together. In practice, the raw parameter count (27e9) at BF16 (16 bits) would be ~54 GB, so the extra ~3% accounts for format overhead. We will download and process these shards one-by-one due to Kaggle’s 20 GB /kaggle/working limit. For reference, Alibaba’s official blog (Aug 17, 2026) highlights that Qwen3.8-27B “delivers excellent capabilities” in coding, reasoning, office tasks and is made to run on consumer hardware with quantization.  

**Closest Alternatives:** We found **no public “Qwen4-27B”**. Alibaba has announced Qwen4 in preview, but the only open weights are Qwen3.8 variants. If Qwen4 does release a 27B model, we’ll pivot, but for now Qwen3.8-27B is the correct official model to use.  

# Kaggle Compute Environment (2×T4, RAM, Disk, Quotas)  
Kaggle offers **2× NVIDIA Tesla T4 GPUs** (16 GB GDDR6 each) with ~29 GB of system RAM.  Each T4 has 65 TFLOPS FP16 peak (so ~130 TFLOPS combined) and ~320 GB/s memory bandwidth.  Note the GPUs are independent (no unified 32 GB VRAM pool), so models must fit within 16 GB per card or be split across them. Kaggle allows up to **12-hour sessions** (GPU or CPU), with about **30 GPU-hours/week** quota (often 30h). Idle kernels time out (~20 min idle). The persistent disk (“/kaggle/working”) is 20 GB; anything outside `/kaggle/working` (like `/tmp`) is ephemeral and lost after reboot.  **Implication:** We must shard and quantize the model on-the-fly (not store full 55 GB locally). We should use `Save & Run All` to keep long runs going, and auto-sync to external storage (see below) to preserve work.  

# Weight Storage and Quantization Targets  
The original Qwen3.8-27B BF16 weights consume ~~55.6 GB~~.  Converting 27B parameters to various “bits-per-weight (BPW)” sizes yields approximate raw storage:  

- **BF16/FP16:** ~54 GB (rounds to 55.6 GB actual safetensors).  
- **4 BPW (4 bits/weight):** 27e9*4/8 = 13.5 GB raw.  
- **3 BPW:** 10.125 GB.  
- **2 BPW:** 6.75 GB.  
- **1.5 BPW:** 5.0625 GB.  
- **1 BPW:** 3.375 GB raw.  

We will create quantized checkpoints at 4, 3, 2, 1.5, and 1 BPW using our Fusion quantizer. (Note: actual saved size may be slightly larger due to quantization scales/codebooks and metadata.) For context, a community FP8 Qwen3.8-27B model exists with “nearly identical” performance to full FP16, showing aggressive quant can work. Going down to 1–1.5 BPW is **extreme**; we expect significant accuracy drop. We will first calibrate at 4/3/2 BPW to understand quality trade-offs, then aggressively test 1.5 and 1 BPW. The final aim is 1 BPW, but only if weight editing can recover capability. A table of raw weight storage:  

| Format       | Raw size (27B) |  
|-------------|---------------|  
| BF16/FP16   | 54.0 GB       |  
| 4 BPW       | 13.5 GB       |  
| 3 BPW       | 10.125 GB     |  
| 2 BPW       | 6.75 GB       |  
| 1.5 BPW     | 5.0625 GB     |  
| 1 BPW       | 3.375 GB      |  

*(Arithmetic: 27e9/8 GB per bit.)* We will confirm these by the quantizer.  

# Compute and Throughput Estimates (24-hour budget)  
We need to assess what’s feasible in one Kaggle run (~24 hours of GPU time, ~172,800 GPU-seconds). Two T4s provide ~130 TFLOPS FP16 combined peak. However, real sustained throughput will be lower (memory transfer, kernel inefficiencies, etc.).  A rough estimate: full forward+backprop per token costs ≈6 × N FLOPs (where N = #params) (3×N forward, 3×N backward). For 27B, that’s ~1.62e11 FLOPs per token. Thus:  
- **100M tokens:** ~1.62e19 FLOPs needed.  
- **500M tokens:** ~8.1e19 FLOPs.  
- **1B tokens:** ~1.62e20 FLOPs.  

If we could use 100% of 2×T4 at 65 TFLOPS each (130 TFLOPS total), 24 h yields ~1.12e19 FLOPs (each GPU: 65e12 * 86400 ≈5.62e18; two GPUs ~1.12e19). This suggests that even 100 M tokens (~1.62e19 FLOPs) slightly exceeds ideal capacity. In practice, utilization is <100%. So realistically, **fine-tuning beyond ~50–80 M tokens would be infeasible** in 24h on 2×T4. Even 100 M is very aggressive.  

- With a modest 30% overall efficiency (common in mixed tasks), 24h ≈3.36e18 FLOPs, limiting us to ~20M tokens.  
- Even forward-only inference at FP16 is ~3×N FLOPs (5.4e10 per token), so 100 M tokens ≈5.4e18 FLOPs (close to one day at 130 TFLOPS with 50% use).  

**Conclusion:** Full fine-tuning on large data is impractical here. We should use **lightweight updates**: either low-rank adapters (LoRA/QLoRA) or weight editing (no gradients). The user’s plan to rely on weight-space edits (Gauntlet Loop) is sensible given these compute limits. Any gradient-based tuning (even with Adafactor optimizer) must use very few epochs or small data.  

# Weight-Space Editing (Gauntlet Loop) Rationale  
Recent research shows promising weight-space editing: MIT’s “Sparks of Weight-Space Programming” found that a frontier LLM (GPT-6 “Astra”) could read a 0.8B Qwen model’s weights and patch them (0.016% of weights) to fix its math reasoning flaw. This edit raised MATH-500 accuracy from 7.9% to 48.1% (and IFEval from 21.0% to 62.3%) purely by weight edits, **without gradient descent**.  This demonstrates that large LMs can sometimes “reason” about model weights and make targeted fixes. For our project, that suggests a workflow: we use a Gauntlet-style loop where an independent critic compares our model’s outputs to high-tier benchmarks (like Claude Fable 5.2/Gemini 4C) and guides an LLM-based editor to tweak weights until it wins.  

However, key caveats:  
- The weight-editing success was on an 0.8B model and a specific flaw (looping behavior). It involved **50 forward passes** (samples) of the model per edit and a powerful LLM with access to the weights. It is still experimental. We cannot assume GPT-6 is available. But we can try smaller LLMs (maybe LLaMA or GPT-4 via API) as *critics/editors* in our Gauntlet loop.  
- The concept is to treat model tuning as an “agentic” problem: break down tasks (benchmarks) into sub-goals and iteratively improve weight matrices. We plan to implement an automated weight-editing pipeline as much as possible, but human oversight may be needed at first.  
- We will absolutely use independent, blinded evaluation each round. For example, the Anthropic benchmarks we aim at (see below) have official test suites; we should run those with the same harness as the real models. The critic will not see the answers during training/edits. Only final scores or win/lose.  

**Strategy:** Initially, we’ll establish the baseline performance of quantized variants (4/3/2 BPW) and the original BF16 model on benchmarks. Then for the most compressed variants (1.5/1 BPW), we’ll run the Gauntlet loop: *for each benchmark or task cluster*, have an LLM-based builder propose weight edits, a separate LLM-based critic evaluate (blind A/B) against the bar (Claude Fable or Gemini), and iterate until improvement. Any improvement must be validated with official eval. 

The **bar models** are Claude Fable 5.2 and Google Gemini 4 Carbon. Official results (Anthropic’s report) show:  
- FrontierSWE v2 (agentic coding): Fable 5.2 ≈69.9%, Gemini 4C ≈61.2%.  
- AutomationBench (business/workflow tasks): Fable 5.2 ≈51.4%, Gemini 4C ≈53.9%.  
- Chartography (visual charts): Fable 5.2 ≈73.4%, Gemini 4C ≈72.5%.  

These will be our target “scores” to beat or match (under identical evaluation conditions). We will not cherry-pick tasks beyond these published suites. We will keep a hidden subset of each test to avoid overfitting through the loop.  

# Benchmarks and Evaluation Protocol  
We will use **official benchmark suites** with existing scoring harnesses (e.g. Anthropic’s suite or open leaderboards). Specifically:  
- **FrontierSWE v2:** agentic software engineering benchmark (coding challenges). Fable 5.2 scored 69.9%.  
- **AutomationBench:** business workflow tasks. Fable 5.2 scored 51.4%.  
- **Chartography:** visual chart reading (no tools). Fable 5.2 scored 73.4%.  
We may also include relevant subsets of others (IF/edge tasks) if feasible, but we avoid any “toy 3D subset” or non-official splits. All comparisons will use the same prompt templates, tool access, and few-shot settings as the published runs. We must ensure exact replication of evaluation setup (same random seeds, temperature etc., or disabling tools for no-tools tasks). Only blind A/B decisions count: the critic will see our model vs baseline outputs without labels. We will repeat each trial multiple times to assess variance.  

# Persistent Research State  
**All experiment metadata will be saved externally**. Kaggle’s environment is ephemeral outside `/kaggle/working`. We will use a tool like *kaggle-persist* to auto-sync our working directory to Google Drive (the user has 5 TB on Google AI Pro). Every 5–10 minutes, model checkpoints (`*.safetensors` or LoRA adapters), logs, and notebooks will be pushed to Drive. This ensures that in case of a 12h limit or crash, we can restart from the last saved state. We will commit: 
- **Hypotheses/decisions:** Maintain a Markdown log (or an external wiki/doc) of each idea tested, reasons for weight edits, etc. 
- **Evidence/results:** Record final scores, intermediate metrics, and plots. Save evaluation outputs (with prompts/answers) for audit.
- **Failed experiments:** If an edit or fine-tune run fails or performs worse, note parameters, random seed, etc.
- **Exact weight diffs:** Any weight-edit step will generate a “diff checkpoint” (only modified weights) plus a hash of the parent model.  
- **Optimizer/seed:** If any gradient update is used (e.g. small fine-tune), we save optimizer state (Adafactor states) and random seeds to resume exactly.  

Specifically, we can use Kaggle Secrets + Kaggle-persist (GitHub) to set up Google Drive sync. The drive folder will mirror `/kaggle/working`: model files, quantization logs, README of the experiment plan, etc. This effectively creates a live progress report in Drive. We’ll also update a public/permanent log (e.g. a GitHub repo or Hugging Face Space) if appropriate.  

# Calculations and Trade-offs  
- **Memory vs Speed:** Using 4- or 3-bit quantization reduces memory footprint drastically (4 BPW = 13.5 GB, easily fit in one T4) and might allow caching more weights on GPU. But matrix multiply on low-bit weights may not proportionally speed up on T4 (which only natively supports INT8/INT4 inference, not training). The **Inferno** custom kernel claims up to 3× speedup, but we must remain skeptical until measured. A 3× gain over baseline FP16 would imply ~390 TFLOPS effective, exceeding hardware FP16 peak – it likely counts some INT4 operations as more ops. We will benchmark Inferno ourselves on small tasks (e.g. single-layer matmuls) to calibrate expectations.  
- **BPW Impact:** Going from 4→1 BPW shrinks storage by ~4×, but quality drop may be steep. The quantizer should use per-block calibration (like GPTQ). We will first verify accuracy/ perplexity on a held-out text sample for each quant level before any editing.  
- **Training vs Editing:** If we do any gradient fine-tuning (e.g. on a small dataset or with LoRA), memory is a concern. For example, full BF16 Adam would store 3× parameters (wts+moments). Adafactor cuts that significantly (O(n) memory), so it is the natural choice if we must tune. However, gradient updates on a quantized base are nontrivial (need dequantize or special backprop). Likely strategy: fine-tune on (4/3-bit) with Adafactor for small steps if needed, but emphasize **direct weight edits** as the main algorithm.  
- **Compute budgets:** In 24h we estimated ~0.7–1e8 tokens processing max (forward+back). For forward-only (e.g. inference/weight edits), maybe 2–3× more tokens. If we run a “Guantlet” critic on each piece, that itself consumes tokens. We must minimize wasted runs. We’ll likely restrict to maybe ~10 major edit cycles per week, each requiring multiple forward evaluations.  

# Roadmap and Phases  
1. **Setup & Baseline:**  
   - Download Qwen3.8-27B shards one-by-one. Stream each shard to quantizer to create BF16, 4BPW, 3BPW, 2BPW safetensors. Save each variant to Drive.  
   - Load each variant (starting from BF16) into Transformers-Fusion. Verify inference works (e.g. generate a known prompt).  
   - Evaluate each on a small sanity set (e.g. An LLM-friendly prompt) to check output sanity and rough quality.  
   - Run official evals: FrontierSWE, AutomationBench, Chartography. Record baseline scores. These form the starting bar.  

2. **Quantized Quality Check:**  
   - For 4,3,2 BPW, measure drop vs BF16 on benchmarks. If drop <10-20% absolute, proceed. If drop >>, decide on whether to adjust quant (e.g. per-layer calibration).  
   - If quality falls off, consider intermediate (e.g. 5BPW or uneven bit allocations) – but focus on planned points.  

3. **Incremental Weight Editing Experiments:**  
   - Focus on the most compressed model that still runs (say 2 BPW to start).  
   - Choose a target benchmark where we lag behind Fable/Gemini. For example, if 2BPW model scores much lower than 50% on AutomationBench, target that.  
   - Construct a **prompt-to-edit**: e.g. “Make the following model better at solving X tasks without losing its existing capabilities.” Provide model card, known failure modes if any.  
   - **Gauntlet loop:** Use an LLM (e.g. GPT-4 via API or a local LLM) as builder to propose weight changes (e.g. “increase this layer’s values by…”, or even draft code to modify weights via PyTorch). Use another LLM as critic: feed it a few test problems (blind) vs baseline, see which is better, and ask what’s still lacking. Loop until improvement is found or timeout.  
   - After editing, evaluate the edited model with the official harness to get real score.  Iterate as needed.  

4. **Progress Tracking:**  
   - After each major step, update our log (in Drive) with “versioned checkpoints” and change summary. For example: “v1: 2BPW original – FrontierSWE 45%. v1.1: +edit1 – FrontierSWE 52%.” Keep each editing patch as a separate checkpoint. Record seed, prompt, LLM outputs.  
   - If an edit fails or regresses, still document it (critical for rigorous research).  

5. **LoRA/Fine-tune Test (if needed):**  
   - If pure editing hits a wall, consider a small LoRA or QLoRA run: freeze base (at 4BPW or BF16), train low-rank adapters on a curated dataset of tasks/benchmarks. Use Adafactor to save memory. This would be done in multiple short sessions with checkpoints saved.  

6. **Final Evaluation:**  
   - When we find an improved quantized model that **empirically beats Fable/Gemini on held-out test sets**, we’ll have a reproducible “model improvement pipeline” as evidence. We’ll document exactly how we got there. If we don’t fully beat them, we’ll analyze how close and why.  

# Assumptions and Unknowns  
- **Quantizer performance:** We assume our Fusion quantizer can handle splitting shards, calibrating, and packing bits. No existing source; we will verify by reconstructing known small models to 1BPW or 4BPW and testing quality.  
- **Inferno speedup:** 3× is a target. We won’t rely on it for scheduling; we treat kernel speed as unknown until benchmarks.  
- **Weight editing efficacy:** The MIT results are on a tiny model (0.8B) with GPT-6. We’ll try with smaller local models (GPT-4 or LLaMA-70B). Success is far from guaranteed. We see it as **exploratory**.  
- **Benchmark metrics:** We will replicate Anthropic’s evaluation code as closely as possible. If any tasks are proprietary (e.g. chart dataset images), we will either skip or use the open subset.  
- **Kaggle stability:** We assume we can keep a scheduled job running daily to stitch sessions together. We will aggressively save state to Drive to mitigate the 12h limit.  

In summary, our plan is to treat this as a rigorous research project: verify all facts (model, hardware, benchmarks), make explicit assumptions, and systematically explore the proposed pipeline under Kaggle’s constraints. All key numbers (model size, GPU spec, bench results) are from official sources. We will log every step so that any future analyst can reproduce or question our workflow. The goal is both to try to match/exceed the Fable/Gemini baselines **and** to prove a repeatable methodology (even if we fall short, we’ll have measured how much editing/quantization can do). 

**Sources:** Official Qwen3.8-27B repo and docs; Alibaba blog announcement; HuggingFace weights listing; Kaggle resource limits; NVIDIA T4 spec; Anthropic benchmark results; MIT Weight-Space Programming blog; Kaggle-persist readme.