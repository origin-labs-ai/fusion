#!/usr/bin/env python3
"""Reference apparatus: registers, glossary, bibliography, and index."""
from __future__ import annotations

import json
import os
import re

import booktex
import pubfacts as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.abspath(os.path.join(HERE, "..", "report"))
ARXIV = json.load(open(os.path.join(REPORT, "arxiv.json"), encoding="utf-8"))


def tex(text: str) -> str:
    return booktex.inline(str(text))


def table(header: list[str], rows: list[list[str]]) -> str:
    return "\n".join(booktex.table([header] + rows))


def section(sid: str, title: str, body: list[str]) -> dict:
    head = r"\section{" + tex(title) + r"}\label{ch:" + sid + "}"
    return {"id": sid, "part": "VIII", "title": title,
            "body": "\n".join([head] + body)}


def format_rows(items: list[dict], retired: bool = False) -> list[list[str]]:
    rows = []
    for f in items:
        bpw = f.get("bpw", 0)
        b = f"{bpw:.2f}".rstrip("0").rstrip(".") if isinstance(bpw, (int, float)) else str(bpw)
        note = f.get("comment", "") or ""
        if len(note) > 42:
            note = note[:39] + "..."
        rows.append([str(f.get("id", "")), f.get("name", ""), f.get("family", ""),
                     b, "retired" if retired else "wire", note])
    return rows


def appendix_sections() -> list[dict]:
    out: list[dict] = []

    # ---------------------------------------------------------------- formats
    body = [tex(
        "The format register is the contract between a name, a nominal bit width, and a wire "
        "identifier. The table is generated from the same register that the engine reads, so a "
        "row that is absent here is absent from the engine. The identifier is the integer written "
        "into the format table; the name is the stable API spelling; the family groups codecs "
        "that share a decoder shape.") + r"\par"]
    body.append(r"\subsection{Valid formats}")
    body.append(table(["ID", "Name", "Family", "BPW", "State", "Note"],
                      format_rows(F.FORMATS)))
    body.append(r"\subsection{Retired formats}")
    body.append(tex(
        "A retired format keeps its identifier reserved. The reader may still decode old files "
        "where the compatibility table allows it, but the writer refuses to emit a retired id. "
        "Retirement is a state change, not a deletion: an id that is reused is a data-corruption "
        "bug waiting for a cold file.") + r"\par")
    body.append(table(["ID", "Name", "Family", "BPW", "State", "Note"],
                      format_rows(F.RETIRED, retired=True)))
    out.append(section("format-register", "Format register", body))

    # ---------------------------------------------------------------- tests
    rows = []
    for t in sorted(F.TESTS, key=lambda x: x["file"]):
        cases = len(t.get("cases") or [])
        rows.append([t["file"], str(t.get("lines", "")), str(cases), str(t.get("asserts", ""))])
    body = [tex(
        "The test register lists the engine's standing test files, their physical line count, "
        "the declared case count, and the declared assertion count. The columns are static "
        "facts about the files; they are not a coverage percentage. A test file with zero "
        "declared cases is still listed because the file exists and the suite runs it.") + r"\par"]
    body.append(table(["Test file", "Lines", "Cases", "Asserts"], rows))
    out.append(section("test-register", "Test register", body))

    # ---------------------------------------------------------------- libraries
    body = [r"\subsection{Libraries}"]
    body.append(table(["Library"], [[x] for x in F.LIBS]))
    body.append(r"\subsection{Targets}")
    body.append(table(["Target"], [[x] for x in F.TARGETS]))
    body.append(r"\subsection{Compute backends}")
    body.append(tex(
        "The backend list is the set of compute paths the engine can name. Availability is "
        "decided at runtime; a backend that is compiled but unavailable must fail loudly rather "
        "than fall back to the CPU and report a GPU number. The 24 names below are the complete "
        "enumeration, not a claim that all 24 run on this host.") + r"\par")
    body.append(table(["Backend"], [[x] for x in F.BACKENDS]))
    out.append(section("library-register", "Libraries, targets, and backends", body))

    # ---------------------------------------------------------------- seats
    rows = []
    for s in F.SEATS:
        contents = s.get("contents", "")
        if len(contents) > 180:
            contents = contents[:177].rstrip() + "..."
        rows.append([s.get("codename", ""), s.get("alias") or "--", s.get("folder", ""),
                     s.get("status", ""), contents])
    body = [tex(
        "A seat is a desktop surface that the launcher can start. The codename is identity; the "
        "alias is an edition label that can be reassigned. The table records the registry state, "
        "not the runtime state: a seat marked present has a folder and a manifest, while a seat "
        "marked empty is a reserved slot.") + r"\par"]
    body.append(table(["Codename", "Alias", "Folder", "State", "Contents"], rows))
    out.append(section("seat-register", "Seat register", body))

    # ---------------------------------------------------------------- decisions
    rows = []
    for d in F.DECISIONS:
        title = d["title"]
        if len(title) > 105:
            title = title[:102].rstrip() + "..."
        rows.append([d["id"], title, r"\pageref{dec:" + d["id"] + "}"])
    body = [tex(
        "The decision register is append-only. Each row points to the page where the full ruling, "
        "its trace, and its executed evidence are recorded. A decision is never deleted; a later "
        "decision may supersede an earlier one, and the earlier row keeps its history.") + r"\par"]
    body.append(table(["ID", "Ruling", "Page"], rows))
    out.append(section("decision-register", "Decision register", body))

    # ---------------------------------------------------------------- research
    rows = []
    for r in F.RESEARCH:
        title = r["title"]
        if len(title) > 105:
            title = title[:102].rstrip() + "..."
        rows.append([r["id"], title, r"\pageref{res:" + r["id"] + "}"])
    body = [tex(
        "The research register is the audit shelf. A row is not a claim that the research is "
        "finished; it records the scope, the source document, the evidence status, and the audit "
        "slots. The page reference points to the full entry in Part I.") + r"\par"]
    body.append(table(["ID", "Topic", "Page"], rows))
    out.append(section("research-register", "Research register", body))

    # ---------------------------------------------------------------- glossary
    out.append(section("glossary", "Glossary", glossary_body()))

    # ---------------------------------------------------------------- bibliography
    out.append(section("bibliography", "Bibliography", bibliography_body()))

    # ---------------------------------------------------------------- index
    out.append(section("index", "Index of chapters", index_body()))
    return out


GLOSSARY = [
    ("Activation quantization", "Quantizing the outputs of a layer rather than only its weights. The difficulty is that activations have a wider dynamic range and are input-dependent."),
    ("AWQ", "Activation-aware Weight Quantization. A post-training method that protects a small set of salient weight channels with a per-channel scale."),
    ("Backend", "A compute path (CPU scalar, AVX2, AVX-512, DirectX, OpenCL, and others) that implements the engine's tensor operations. Availability is probed at runtime."),
    ("Bit per weight (BPW)", "The number of bits used per weight, including scales and metadata when the format is considered as a whole. A nominal BPW that ignores metadata is not a wire BPW."),
    ("Cender", "The design name for the engine's constant-memory sequence core: a decay state plus an exact paged store. It is a design, not an implemented module in the current tree."),
    ("Chinchilla scaling", "The empirical finding that model size and training tokens should be scaled together under a fixed compute budget."),
    ("CodeFusion", "The product name for the launcher and its nine seats. The folder and repository are named code, without the product suffix."),
    ("Context rot", "The degradation of a model's ability to use relevant information as the surrounding context grows, even when the information is present."),
    ("CUDA", "NVIDIA's compute platform. It is unavailable on the AMD integrated GPU that this project targets."),
    ("Decay state", "A fixed-size recurrent summary of the past, updated by a decayed sum of key-value outer products."),
    ("DoRA", "Weight-Decomposed Low-Rank Adaptation. A fine-tuning method that separates magnitude from direction before applying a low-rank update."),
    ("E4M3", "An 8-bit floating-point format with 4 exponent bits and 3 mantissa bits. More precision, less range than E5M2."),
    ("E5M2", "An 8-bit floating-point format with 5 exponent bits and 2 mantissa bits. More range, less precision than E4M3."),
    ("EAIN", "Enhanced Artificial Intelligence Neurons. A research direction for per-unit importance, decay, thresholded activation, and local plasticity."),
    ("Embedding", "A lookup table that maps discrete token ids to vectors. The table is a matrix and is often quantized with a different format from the transformer blocks."),
    ("Epoch", "One pass over the training data. The engine's schedule is step-based; an epoch is a reporting unit, not an optimizer primitive."),
    ("FP8", "An 8-bit floating-point family used for training and inference. The two common variants are E4M3 and E5M2."),
    ("Format ladder", "The ordered set of format families and tiers (L, M, H) that the engine promises to encode and decode."),
    ("GPTQ", "A post-training quantization method that uses an approximate Hessian to round weights column by column while propagating the residual."),
    ("GRPO", "Group Relative Policy Optimisation. A policy-gradient method that compares completions within a group rather than against a learned value function."),
    ("Hessian", "The matrix of second derivatives of the loss with respect to the weights. Quantization methods use an approximation of it to decide rounding order."),
    ("Inferno", "The engine's kernel and training subsystem: a C++20 implementation of dense, MoE, and multimodal training paths."),
    ("KV cache", "The stored keys and values of past tokens that attention reads during autoregressive decoding. Its size grows with the sequence length and the number of layers."),
    ("LoRA", "Low-Rank Adaptation. A fine-tuning method that freezes the base weights and learns a low-rank update."),
    ("Lost in the middle", "The empirical U-shaped curve in which information at the beginning or end of a long context is used more reliably than information in the middle."),
    ("MoE", "Mixture of Experts. A sparse layer that routes each token to a subset of expert feed-forward networks."),
    ("NCM", "Next-Concept Modeling. A generation mechanism studied as a possible extension of next-token prediction."),
    ("Page table", "A map from sequence positions to fixed-size blocks in an external KV store. It enables exact retrieval without a contiguous allocation."),
    ("PagedAttention", "An attention implementation that reads the KV cache through a block table, reducing fragmentation and enabling sharing."),
    ("Quantization barrier", "The dead zone created when a gradient is smaller than the codebook gap divided by the learning rate; the parameter update is identically zero."),
    ("QAT", "Quantization-Aware Training. Training with a simulated quantization operation in the forward pass so that the model adapts to the codebook."),
    ("QLoRA", "A fine-tuning recipe that keeps a frozen base model in 4-bit and trains small adapters in higher precision."),
    ("Quantization", "The mapping of a continuous-valued tensor onto a finite set of codes, usually with a scale and sometimes a zero point."),
    ("Retrieval-augmented generation", "A system that retrieves passages from an external index and conditions a generator on them."),
    ("RMSNorm", "Root-mean-square normalisation. A normalisation layer that divides by the root mean square of the activations and applies a learned scale."),
    ("RoPE", "Rotary Position Embedding. A position encoding that rotates query and key pairs by an angle proportional to the position."),
    ("Speculative decoding", "A decoding method that proposes tokens with a small model and verifies them with the target model, preserving the target distribution."),
    ("Superproject", "The repository that records the component pins, the cross-repository decisions, and the publishable documentation."),
    ("TransCender", "The engine's former name, kept as a legacy wire identity and as a historical alias."),
    ("Transformers-Fusion", "The canonical product name for the engine. The folder and repository are named transformers, without the product suffix."),
    ("Wire identity", "The magic string at the start of a stored file that identifies the format family and therefore the reader that may parse it."),
    ("Zero point", "The integer code that represents zero in an asymmetric quantization scheme."),
    ("Ablation", "An experiment that removes or changes one component to measure its contribution."),
    ("Attention", "The operation that mixes value vectors with weights computed from query-key similarities."),
    ("Autograd", "Automatic differentiation. The engine builds a graph of tensor operations and propagates gradients backward."),
    ("Bootstrap interval", "A confidence interval estimated by resampling the observed data. It is used when the distribution of the statistic is unknown."),
    ("Calibration", "A pass over representative data used to choose scales, codebooks, or format assignments."),
    ("Codebook", "A finite set of reconstruction values shared by a block of weights."),
    ("Continuous batching", "A serving technique that admits and retires sequences at every decoding step instead of waiting for a fixed batch to finish."),
    ("Dead zone", "The region of gradient magnitudes below the quantization gap where the update is zero."),
    ("Deterministic", "A computation whose output is reproducible from the same inputs and the same order of operations."),
    ("Distillation", "Training a smaller model to match the outputs or representations of a larger one."),
    ("Expert", "One feed-forward network inside a mixture-of-experts layer."),
    ("Falsifier", "An observation that would prove a design claim false. A claim without a falsifier is not testable."),
    ("FlashAttention", "An exact attention kernel that tiles the computation to avoid materialising the full attention matrix in high-bandwidth memory."),
    ("Floating point", "A number representation with a sign, an exponent, and a significand. Its precision varies with magnitude."),
    ("Gate", "A consistency check that compares generated surfaces against a registry or a contract."),
    ("Gradient", "The derivative of the loss with respect to a parameter, used by the optimizer to update it."),
    ("Integer quantization", "A representation that maps values to integer codes with an external scale and optionally a zero point."),
    ("Kernel", "A low-level compute routine, often written to exploit SIMD lanes or a GPU."),
    ("Latency", "The wall-clock time to complete one request or one decoding step."),
    ("Manifest", "A file that records identity, versions, and the list of artifacts in a package."),
    ("Mixed precision", "Using more than one numeric format in a single model or training step."),
    ("Nominal BPW", "The bit width implied by the format name, before metadata and grouping overhead are counted."),
    ("Outlier", "A value whose magnitude is far from the rest of the tensor and therefore dominates a scale or an error bound."),
    ("Per-channel scale", "A separate quantization scale for each output channel of a matrix."),
    ("Per-token scale", "A separate quantization scale for each token or row of an activation matrix."),
    ("Post-training quantization", "Quantizing a model after it has been trained, usually with a small calibration set."),
    ("Quantization error", "The difference between the original tensor and its reconstructed value."),
    ("Reconstruction", "The dequantized value produced by decoding a code and a scale."),
    ("Register", "A table of record in this report: formats, tests, seats, decisions, or research items."),
    ("Retired", "A format or identifier that is no longer written but may still be read for compatibility."),
    ("Scale", "A positive factor that maps integer codes to real values."),
    ("Seat", "A desktop surface that the launcher can start; it has a codename and optionally an alias."),
    ("Sparse attention", "An attention pattern that omits some query-key pairs to reduce cost."),
    ("State space model", "A sequence model that updates a finite state with a linear or input-dependent recurrence."),
    ("Tensor", "A multi-dimensional array with a dtype, a shape, and a stride."),
    ("Throughput", "The amount of work completed per unit time, such as tokens per second."),
    ("Token", "The atomic unit of text or modality input consumed by a model."),
    ("Top-k routing", "A mixture-of-experts rule that sends each token to the k highest-scoring experts."),
    ("Verifier", "A script that checks a documented invariant and exits non-zero when it fails."),
    ("Zero-shot", "Evaluation on a task without task-specific training examples."),
]


def glossary_body() -> list[str]:
    body = [tex(
        "The glossary defines the terms that recur across the report. A definition is written for "
        "a reader who has the tree open: it names the artifact or the operation, not only the "
        "concept. Where a term has a product spelling and a historical spelling, both are listed.") + r"\par"]
    rows = [[t, d] for t, d in GLOSSARY]
    body.append(table(["Term", "Definition"], rows))
    return body


def bibliography_body() -> list[str]:
    body = [tex(
        "The bibliography has two parts. The first lists the arXiv records used in the research "
        "compendium, with the identifier that resolves the paper. The second lists the project "
        "records that supplied the architecture, the decisions, the claim ledger, and the "
        "release history. Web links are omitted where the identifier is sufficient.") + r"\par"]
    body.append(r"\subsection{arXiv records}")
    rows = []
    for p in sorted(ARXIV["papers"], key=lambda x: (x.get("topic", ""), x.get("year", ""), x["id"])):
        first = p["authors"][0] if p.get("authors") else "--"
        rows.append([p["id"], p.get("year", ""), first, p["title"]])
    body.append(table(["arXiv", "Year", "First author", "Title"], rows))
    body.append(r"\subsection{Project records}")
    records = [
        ("Master plan", "Architecture, naming, sweeps, loop research, and the decision gates."),
        ("Decision register", "The append-only rulings D-01 through D-31."),
        ("Research index", "The audit shelf R-01 through R-18 with evidence status."),
        ("Claim ledger", "The row-level verification record for the engine."),
        ("Engine specification", "The training-engine mandate, catalog, and verification plan."),
        ("Engine architecture", "The source layout, component hierarchy, and design philosophy."),
        ("API reference", "The public tensor, autograd, model, and training interfaces."),
        ("Tensor module", "The tensor, shape, dtype, and kernel contract."),
        ("Usage and build", "The operator-facing commands and the build contract."),
        ("Whitepaper", "The QUANT training argument, the barrier mechanism, and the bounds."),
        ("Comparison charts", "The measured format comparisons and quality tables."),
        ("Proof expansions", "The formal expansions behind the whitepaper."),
        ("CodeFusion research record", "The sixty-four-section product and provenance record."),
        ("Launcher README", "The registry, the seats, the gates, and the launcher contract."),
        ("Engine README", "The engine's own description of formats, targets, and tests."),
    ]
    body.append(table(["Record", "Scope"], [[a, b] for a, b in records]))
    return body


def index_body() -> list[str]:
    body = [tex(
        "The index lists every chapter with the page on which it starts. The page numbers are "
        "resolved by the typesetter, so the index and the contents always agree. The decision and "
        "research registers in this part provide the corresponding row-level indexes.") + r"\par"]
    body.append(r"\subsection{Chapters}")
    # filled by book.py through CHAPTER_INDEX placeholder
    body.append("@@CHAPTER_INDEX@@")
    body.append(r"\subsection{How to use the index}")
    body.append(tex(
        "A chapter entry points to the first page of the chapter, not to every page on which the "
        "chapter is mentioned. For a row-level lookup, use the decision register, the research "
        "register, or the format register. The three registers are ordered by identifier, so a "
        "reader who knows the identifier does not need the chapter index.") + r"\par")
    return body
