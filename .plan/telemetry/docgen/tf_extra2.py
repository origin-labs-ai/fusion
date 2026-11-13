# -*- coding: utf-8 -*-
"""Batch 1b - the remaining narrative lines for each Transformers-Fusion README section.

Counts are chosen so every section lands on exactly 30 narrative lines.
"""

EXTRA = {
"## 3. Repository layout": [
    "The generated table is the reason this document can be rebuilt at any time",
    "without a human recounting anything.",
    "The generator lives in the superproject, not in this repository, because the",
    "superproject is what owns cross-repository claims.",
],

"## 4. The two engine trees": [
    "A reader who wants to know which tree a feature lives in should grep, and this",
],

"## 6. The executables": [
    "The evaluation tool is the one that matters most for this project's claims.",
    "It compares a quantised model against its reference and reports the error, which",
    "is the measurement the format decisions are actually made on.",
    "The quantisation tool is the one that matters most for the ladder.",
    "It writes files through the codec and reports the resulting budget, so a format's",
    "claimed ratio is produced by the same code that writes the file.",
    "The format list tool is the one that matters most for a newcomer.",
    "It prints the live ladder, which answers the question a new contributor asks",
    "first.",
    "The train tools cover the training path that the Inferno work will eventually",
    "serve.",
],

"## 7. The libraries": [
    "The `quant_config` library holds the generated configuration header's consumers,",
    "and it is where a build-time constant becomes a runtime policy.",
],

"## 8. The test suite": [
    "The suite is registered as CTest targets, so a single command runs everything the",
    "project considers a test, and the list is in the build file rather than in a",
    "script that could drift.",
],

"## 14. The codebook": [
    "The codebook header is five kilobytes, which for a vocabulary implementation",
    "means it carries the construction, the lookup and the serialisation together.",
    "Serialisation is the part that has to be exact, because the encoder runs on the",
    "training machine and the decoder may run anywhere.",
    "A codebook that is rebuilt rather than stored is a codebook that cannot be",
    "trusted across a save and load.",
    "The project stores it.",
    "The STE path adds one more constraint, because the codebook must also be usable",
    "inside a differentiable graph.",
    "That combination - serialised exactly and differentiable at training time - is",
    "what makes the low-bit formats hard, and it is why they are worth the trouble.",
    "The formats that reach the best compression on this project all pay this cost.",
],

"## 15. The quantization engines": [
    "Adding an engine for a new width is therefore a small, well-understood piece of",
],

"## 16. Quantization-aware training": [
    "Calibration is the third pillar, and it exists because a scale computed from a",
    "single batch is a bad scale for the next batch.",
    "Moving-average calibration exists to fix exactly that.",
],

"## 17. The integer path": [
    "The engine's integer path is honest about this, which is the important part.",
],

"## 19. The FP8 special-value problem": [
    "The E5M2 format does have an infinity encoding, and the disagreement there is",
    "narrower but still real.",
    "Two of the three paths treat the upper exponent range as special values, and one",
    "of them maps them to zero.",
    "A zero where an infinity belongs is the more damaging of the two errors, because",
    "a silent zero propagates through a computation instead of stopping it.",
    "The fix is the same in both cases, which is why the project proposes one",
    "canonical implementation rather than three fixes.",
    "The exhaustive test then becomes the permanent guard.",
],

"## 20. FP8 in the attention path": [
    "The same caution applies to the KV cache, whose FP8-named helper stores integer",
    "codes.",
    "That helper is on the inference hot path, so its cost is real.",
    "A correctly named integer path there would cost nothing and mislead nobody.",
    "Renaming and reimplementing are separate decisions, and the plan keeps them",
    "separate.",
],

"## 21. The backends": [
    "The list also shows how much of this project is about reach.",
    "A format that only runs on one vendor's accelerator is a research result.",
    "A format that runs on a scalar CPU is a feature, because the scalar path is the",
    "one that every machine has.",
    "That is the argument for keeping the reference path fast enough to be usable,",
    "not merely correct.",
    "The engine's benchmark suite measures the scalar and vector paths alongside the",
    "accelerator paths for exactly this reason.",
    "A reader comparing numbers should check which row of the backend table produced",
    "them.",
    "The table is the first place to look when a benchmark number looks too good.",
],

"## 22. The GPU capability contract": [
    "The contract has a third half that is easy to forget: the bench harness.",
    "Every benchmark the project publishes names the backend that produced it, and",
    "refuses to print a performance number for a capability-flagged fallback.",
    "A benchmark that cannot produce a number is more useful than a benchmark that",
    "produces a wrong one.",
    "The engine's own tool set includes the report generator that writes the backend",
    "into the report.",
    "This is the difference between a harness that measures the engine and one that",
    "measures the machine it runs on.",
    "The project's rule is that the second kind is not published.",
],

"## 25. The KV cache": [
    "Both of those defects are recorded with gates, so neither can be forgotten.",
],

"## 26. The inference engine": [
    "The count also feeds the memory budget, because a fused attention is a fused",
    "attention only if the fused path is the one that actually runs.",
    "The four fused implementations are the ones the optimised inference paths use.",
    "The one composed implementation is the hybrid path, which builds an attention out",
    "of smaller pieces because the routing needs that flexibility.",
    "The fifteen primitive-only backends are the ones that expose operations and let",
    "the model layer compose them.",
    "That third group is the largest, and it is the group that carries the risk of a",
    "wrong claim.",
],

"## 27. The trainer": [
    "The trainer is also the largest surface for the audit's attention-shape sweep.",
],

"## 28. The code generator": [
    "The generator's own test file is the right place for the regression, because a",
],

"## 29. Training engines, MoE and multimodal": [
    "The multimodal headers also carry the video and audio paths, which are the",
    "heaviest of the five modalities.",
    "A video tensor is orders of magnitude larger than a text tensor, so the memory",
    "budget analysis for multimodal is a different problem from the text case.",
    "The project has not yet published a multimodal budget, and that gap is recorded",
    "rather than estimated.",
    "The MoE expert-parallel header and the prefetch header exist because the",
    "expert weights are the largest thing in the model.",
    "Moving them is a bandwidth problem before it is a compute problem.",
],

"## 31. The telemetry layer": [
    "The telemetry header is ten kilobytes, which is a lot for measurement code, and",
    "the reason is that it measures a lot.",
    "Token accounting, throughput windows, error surfaces and quality estimates all",
    "live there, and each of them has a different notion of what a sample is.",
    "That variety is where a bug hides: a token counter that double counts on a retry",
    "would make a throughput number wrong without failing any test.",
    "The plan treats telemetry as part of the correctness surface, not as part of the",
    "observability surface.",
    "That is the reason the hardcoded quality-loss defect was graded high rather than",
    "low.",
    "It sits in the same trust boundary as the quantization claims.",
],

"## 32. Production and serving": [
    "The server's authentication correction is a good example of why the anchor",
    "verifier exists.",
    "The plan had claimed the server did not enforce authentication, which would have",
    "been a serious finding if true.",
    "The anchor pass found the bearer-authentication code at lines 262 to 271 and",
    "corrected the claim.",
    "A wrong security claim in a published document is as damaging as a wrong",
    "optimisation claim, and the same tool catches both.",
],

"## 33. The tokenizer": [
    "The tokeniser's own vocabulary file is part of the model artefact, and the",
    "project treats the pair as one thing to be versioned together.",
],

"## 34. Distributed training and parallelism": [
    "The zero-offload path is also where the LoRA adapter path intersects with the",
    "quantised base weights, because the base is frozen and therefore the obvious",
    "candidate for offload.",
    "That combination is what makes the project's stated target - adapting a",
    "one-bit-per-weight model - plausible on consumer hardware.",
    "It also makes the memory accounting much harder, because the frozen base, the",
    "trainable adapter and the optimiser state now occupy three different places.",
    "The project has not published a single number for that configuration yet, and",
    "the plan records the absence rather than filling it with an estimate.",
    "Publishing an estimated peak memory figure would be exactly the kind of claim",
    "the bench-honesty rules forbid.",
],

"## 35. The optimizer": [
    "The trainer also owns the learning-rate schedules and the precision policy that",
    "decides which parts of a mixed-precision model train in which dtype.",
    "That policy is where the INT and FP families meet in training, because a",
    "mixed-precision run has to decide per tensor whether it holds an integer code",
    "or a floating-point value.",
    "The existing decision is mostly structural - the model decides - and the research",
    "draft's planner proposal is about making that decision measurable.",
    "The tests `test_mixed_precision_proof` and `test_mix_components` guard the",
    "current behaviour, so the proposal can be measured against a known baseline.",
    "That baseline is what makes the proposal a research question rather than a",
    "rewrite.",
],

"## 36. Continual learning": [
    "The stack question has three candidate answers and each of them changes what the",
    "layer can do.",
    "The first candidate is the flywheel loop, which is built around repeated",
    "improvement cycles.",
    "The second is the meta-cognition layer, which is built around the system",
    "observing its own state.",
    "The third is the plain trainer, which is built around gradient updates and has no",
    "notion of self-observation at all.",
    "An EAIN built on the third would be a different animal from an EAIN built on the",
    "first, and the cost difference is not just engineering effort.",
    "It is a difference in what the resulting system could ever claim.",
    "That is why the plan refuses to decide it by default and asks instead.",
],

"## 37. Inference optimisation": [
    "The flash-attention header is small because the implementation is expected to",
    "change shape between backends.",
    "The production kernel header is the one that holds the contract that every",
    "backend has to satisfy.",
    "When a backend cannot satisfy it, the honest move is to declare the capability",
    "absent, which is the rule the capability test enforces.",
    "The inference-optimisation header is thirteen kilobytes, and most of it is",
    "documentation of what each path is allowed to assume about numerics.",
    "Those assumptions are the contract.",
    "A fused path that assumes pre-scaled inputs, for example, has to say so, because",
    "a caller that forgets to scale gets numbers that look plausible.",
    "The header states the preconditions so the mistake becomes a compile-time",
    "argument rather than a numerical mystery.",
    "This is the difference between an optimisation layer and an optimisation that",
    "happens to work.",
],

"## 38. The math library": [
    "The math header declares the operations the rest of the engine is allowed to",
    "assume.",
    "That list is short on purpose, because every entry is a promise about rounding,",
    "about accumulation order and about what happens at the edges.",
    "The tiled header adds the decomposition strategy on top of that list.",
    "Tiling is where numerical behaviour can change with a configuration value, which",
    "makes it a place where a test matrix matters.",
    "The Step-4 sweep checked these trees for attention and softmax specifically,",
    "because a softmax in a supposedly primitive file would invalidate the",
    "primitive-only claim that the inference plan depends on.",
    "The result was clean, and that clean result is what allows the plan to treat the",
    "vector paths as supporting infrastructure rather than as unexamined code.",
    "The same sweep found the opposite in the telemetry file, which is how a",
    "hardcoded quality estimate became a defect with a severity.",
    "One sweep, two very different outcomes, both recorded.",
],

"## 39. The GLE tree": [
    "The report path is what the publishability work will lean on.",
    "A research report that has to be assembled by hand from terminal output is a",
    "report that will not survive being regenerated.",
    "The GLE tree exists to make the engine's own numbers reproducible as a document.",
    "Its two files are enough for that, because the format is fixed and the inputs",
    "are the engine's outputs.",
    "The tree was audited during the Step-4 sweep along with every other tree in the",
    "repository, and it came back clean.",
    "That is a smaller claim than it sounds.",
    "A clean result means no attention or softmax hides there, which is exactly what",
    "was being looked for.",
    "It does not mean the report is correct.",
    "It means the report path contains no hidden numerical behaviour, so the numbers",
    "in the report are the numbers the engine computed.",
    "That distinction is the difference between a report that can be checked and one",
    "that has to be trusted.",
    "The GLE report tool is the engine's answer to the publishability requirement,",
    "and it is already wired into the build.",
    "Using it costs one command.",
],

"## 40. The native weight path": [
    "The measurement that will decide whether the native path is worth extending is",
    "the one the bench harness already takes: equal workload, equal effective",
    "storage budget, same hardware.",
    "That is the comparison rule the whole project uses, and it applies to formats",
    "exactly as it applies to backends.",
    "A format that wins only by compressing more is not winning if the extra",
    "compression costs quality or time.",
    "The five-dimension evaluation framework in the INT and FP research draft -",
    "accuracy, storage, performance, stability and compatibility - is the same",
    "framework, written down.",
    "Every new format proposed for this project will be judged on those five",
    "dimensions and on nothing else.",
    "That is the standard that makes a ladder a contract rather than a list.",
],
}
