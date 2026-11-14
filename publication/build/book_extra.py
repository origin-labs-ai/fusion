#!/usr/bin/env python3
"""Generated sections: research compendium, theorem note, method, appendices."""
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


def paper_rows(papers: list[dict], claim: bool = True) -> list[list[str]]:
    rows = []
    for p in papers:
        first = p["authors"][0].split()[-1] if p.get("authors") else "--"
        title = p["title"]
        if len(title) > 95:
            title = title[:92].rstrip() + "..."
        row = [p["id"], p.get("year", ""), title, first]
        if claim:
            a = p.get("abstract", "")
            first_sentence = re.split(r"(?<=[.!?])\s+", a)[0] if a else ""
            if len(first_sentence) > 130:
                first_sentence = first_sentence[:127].rstrip() + "..."
            row.append(first_sentence)
        rows.append(row)
    return rows


TOPIC_INTRO = {
    "quantization": (
        "Quantization is the compression layer of the stack: it maps floating-point weights and "
        "activations onto a finite codebook while trying to preserve the output of the layer. The "
        "papers below span post-training weight quantization, activation-aware scaling, low-rank "
        "adapters trained in quantized space, extreme low-bit formats, and KV-cache compression. "
        "The recurring lesson is that the best method depends on where the error is measured: "
        "weight reconstruction, layer output, perplexity, or a downstream task."
    ),
    "training": (
        "Training research supplies the optimisation and scaling laws that the engine has to "
        "respect. The selection covers low-rank adaptation, memory-efficient optimisation, "
        "scaling-law fits, distributed state sharding, and the model families that define the "
        "current baseline. The practical question for this project is not whether a method is "
        "elegant but whether it can be implemented without a Python runtime and whether its "
        "memory claim survives a real optimizer step."
    ),
    "attention": (
        "Attention is the operation the Fusion programme is trying to replace or extend. The "
        "papers here cover exact attention kernels, positional encoding, linear and recurrent "
        "sequence mixers, long-context retrieval, and serving-time paging. They are the evidence "
        "base for the claim that the cost of attention is not a single quadratic term but a "
        "family of memory, bandwidth, and scheduling costs."
    ),
    "long-context": (
        "Long-context evaluation is where the context-rot argument becomes empirical. The "
        "selected work measures position sensitivity, needle retrieval, multi-hop reasoning, and "
        "the gap between a marketed context window and the length at which a model still "
        "reasons. These results motivate a constant-memory design that keeps an exact index "
        "beside a compressive state rather than relying on a larger attention window."
    ),
    "agents": (
        "Agent research is the harness layer: retrieval, tool use, reasoning traces, instruction "
        "tuning, preference optimisation, and the model families that the launcher is expected to "
        "drive. The common thread is that capability is partly in the weights and partly in the "
        "loop around them, which is why CodeFusion treats the harness as a first-class artifact."
    ),
    "serving": (
        "Serving research turns a model into a system: speculative decoding, continuous "
        "batching, paged KV cache, speculative trees, and sparse mixture-of-experts routing. The "
        "numbers that matter are tokens per second, time to first token, memory per sequence, and "
        "the tail latency under concurrent load."
    ),
}

DETAIL = {
    "2210.17323": "GPTQ treats layer-wise quantization as a sequence of small least-squares problems and uses an approximate Hessian to decide the order in which weights are rounded. Its contribution is not the rounding rule alone but the observation that the residual from earlier columns can be propagated into later ones, which is why a one-shot 3--4 bit model can remain usable. The method is post-training: it assumes an FP16 teacher and calibration data.",
    "2306.00978": "AWQ starts from the observation that a small number of activation-salient weight channels dominate the output error. It protects those channels with a per-channel scale instead of keeping them in higher precision, so the hardware still runs a uniform low-bit kernel. The paper is a useful counterexample to the idea that mixed precision must mean mixed data types.",
    "2211.10438": "SmoothQuant moves the quantization difficulty from activations to weights by applying a mathematically equivalent per-channel scaling. The important engineering point is that the transformation is folded into the preceding layer, so inference pays no extra kernel. It is the canonical example of a quantization method designed around the deployment graph rather than around a standalone matrix.",
    "2305.14314": "QLoRA combines a frozen 4-bit base model with low-rank adapters trained in higher precision. The paper's real contribution is the memory accounting: the base weights dominate, the adapters are small, and the optimizer state is the remaining cost. It is the closest published design to a fine-tuning path that can run on a single device.",
    "2208.07339": "LLM.int8() separates outlier dimensions from the rest of the matrix and keeps the outliers in higher precision while the bulk runs in INT8. The result is a mixed-precision kernel whose branching is data-dependent, which makes it a useful case study in the difference between nominal bits and effective bits.",
    "2402.17764": "BitNet b1.58 constrains weights to ternary values and trains from scratch rather than quantizing a finished model. The paper matters because it shows that the training dynamics, not only the inference kernel, have to be designed for the format; a post-hoc projection into ternary values is a different and weaker procedure.",
    "2209.05433": "The FP8 formats paper defines E4M3 and E5M2 and explains the trade-off between mantissa and exponent range. E4M3 has more precision and less range; E5M2 has more range and less precision. The choice is workload-dependent, which is why a format ladder should not collapse every FP8 use into one identifier.",
    "2402.02750": "KIVI quantizes the key cache per channel and the value cache per token, matching the observation that keys have channel-wise outliers while values are more uniformly distributed along the token axis. The paper is a clean example of a cache layout driving the quantization granularity.",
    "2106.09685": "LoRA freezes the pretrained weights and learns a low-rank update. The method is attractive because the update can be merged into the base matrix at inference time, so the deployed model has the same shape as the original. The rank and the target modules are the real hyperparameters.",
    "2402.09353": "DoRA decomposes a weight update into magnitude and direction and applies the low-rank adaptation to the direction. The reported gains are largest at low rank, which is exactly where a naive low-rank update loses the most expressive power.",
    "2402.04396": "GaLore projects the gradient into a low-rank subspace before applying the optimizer state. The memory saving comes from never materialising the full second moment, not from a smaller model. It is relevant to any training path that is bandwidth-bound rather than compute-bound.",
    "2203.15556": "Chinchilla re-fits the scaling law and concludes that most large models were undertrained relative to their parameter count. The practical rule is that parameter count and token count should scale together; the exact constants depend on the compute budget and the data distribution.",
    "2205.14135": "FlashAttention tiles the attention computation so that the softmax normaliser is accumulated without writing the full attention matrix to high-bandwidth memory. The mathematical result is exact; the gain is a memory-hierarchy gain. It is the clearest example of an algorithm whose speed comes from avoiding a materialised intermediate.",
    "2309.06180": "PagedAttention stores the KV cache in fixed-size blocks and maps a sequence to a block table. The win is not a better attention kernel but a better allocator: fragmentation falls, sequences can share blocks, and continuous batching becomes practical. This is the serving-side analogue of a paged virtual-memory system.",
    "2104.09864": "Rotary position embedding encodes position by rotating query and key vectors in pairs. The relative-position property falls out of the dot product, and the decay behaviour can be tuned by the base frequency. It is now a default in open-weight transformer families.",
    "2312.00752": "Mamba replaces attention with a selective state-space recurrence whose parameters depend on the input. The selection mechanism is what separates it from a linear time-invariant system: the model can choose to remember or forget along the sequence. The paper is the strongest recent argument that a constant-memory sequence mixer can be competitive.",
    "2305.13048": "RWKV combines a linear-attention-like recurrence with a transformer-shaped training path. Its importance here is architectural: it demonstrates that a recurrent state can be trained in parallel over the sequence during training while running in constant memory at inference.",
    "2307.08621": "RetNet proposes a retention mechanism with three computation paradigms: parallel, recurrent, and chunkwise. The paper is a template for how to present a sequence mixer: the same operator should have a training form and an inference form with a stated memory cost.",
    "2310.01889": "Ring Attention distributes the attention computation across devices arranged in a ring and overlaps communication with computation. It shows that long context is often a systems problem: the arithmetic is unchanged, but the memory per device is not.",
    "2004.05150": "Longformer combines a local window with a small set of global tokens. The design is a useful baseline for any claim that a new architecture solves long context: the comparison should include a sparse-attention model with a comparable token budget, not only a dense transformer.",
    "2103.03206": "Perceiver maps an arbitrarily large input to a fixed-size latent array through cross-attention. It is the cleanest demonstration that a fixed-size state can summarise a variable-length input, and it also shows the cost: the latent bottleneck limits fine-grained retrieval unless the input is revisited.",
    "2203.08913": "Memorizing Transformers add a non-differentiable external memory of past keys and values and retrieve the top-k entries at inference. The paper is a direct ancestor of the index-plus-state design: the model keeps a small working state and an exact store for the long tail.",
    "2112.04426": "RETRO combines a retrieval database with a transformer and shows that retrieval can substitute for some parameters. The key engineering detail is the chunked cross-attention over retrieved neighbours, which keeps the retrieval cost from dominating the sequence length.",
    "2307.03172": "Lost in the Middle measures accuracy as a function of the position of the relevant passage. The result is a U-shaped curve: information at the beginning or end is used more reliably than information in the middle. The effect persists across model families and is not fixed by a larger context window.",
    "2404.06654": "RULER builds a suite of long-context tasks with controllable length and complexity. It separates effective context length from the advertised window and shows that many models degrade well before their nominal limit. It is the evaluation protocol this report recommends for any long-context claim.",
    "2406.17419": "This study stress-tests long-context models on realistic tasks rather than needle retrieval. The finding is that strong needle performance can coexist with weak reasoning over the same context, which is why a single retrieval score is not enough.",
    "2302.04761": "Toolformer teaches a model to insert API calls into its own text and then filters the calls by whether they reduce the language-modelling loss. The paper is a clean example of self-supervised tool use without a human-labelled trajectory.",
    "2210.03629": "ReAct interleaves reasoning traces with actions. The important claim is not that the model becomes correct but that the trace makes the policy inspectable, which is what a harness needs in order to retry or recover.",
    "2005.11401": "RAG combines a dense retriever with a generator and marginalises over retrieved passages. The paper established the retrieval-augmented template that most agent stacks still use; its weakness is that retrieval quality and generation quality are evaluated separately.",
    "2302.01318": "Speculative sampling uses a small draft model to propose tokens and the large model to accept or reject them with a correction that preserves the target distribution. The method is exact under its assumptions, which is why it is a better baseline than a heuristic early-exit.",
    "2211.17192": "This speculative-decoding paper makes the same accept/reject argument with a focus on latency. The practical lesson is that the speedup depends on the acceptance rate and on the cost of the draft model, not on the size of the target alone.",
    "2312.07104": "SGLang introduces a frontend language for structured generation and a runtime with RadixAttention for prefix sharing. The system contribution is the cache reuse across requests, which is often larger than the kernel-level gain.",
    "2401.10774": "Medusa adds multiple decoding heads to the target model and verifies candidate continuations with a tree attention mask. It removes the separate draft model, at the cost of extra parameters and a more complex verifier.",
    "2401.15077": "EAGLE uses a small autoregressive draft head and a tree-structured verification step. The reported speedups come from a high acceptance rate at low draft cost, which is the right trade-off to optimise.",
    "2101.03961": "Switch Transformer simplifies mixture-of-experts routing to top-1 and studies the stability tricks needed at scale. The paper is a reminder that routing is a load-balancing problem as much as a modelling problem.",
    "2401.04088": "Mixtral 8x7B is a sparse mixture of experts with top-2 routing. The paper reports that a 47B-parameter model with 13B active parameters can match a much larger dense model on several benchmarks, which is the strongest public evidence for conditional compute.",
    "2312.00752": "Mamba's selective state-space layer is the closest published relative of the Cender recurrence. The difference is that Cender keeps an exact paged store beside the decay state, so the recurrent state does not have to carry the entire context.",
    "2405.04434": "DeepSeek-V2 introduces multi-head latent attention and a sparse MoE, with a KV cache that is compressed into a latent vector. The design is directly relevant to the memory accounting in this report.",
    "2412.19437": "DeepSeek-V3 reports a 671B-parameter MoE with 37B active parameters and a training recipe built around FP8 and load balancing. The paper is a reference point for the scale at which format and routing decisions interact.",
    "2501.12948": "DeepSeek-R1 studies reinforcement learning for reasoning and shows that a base model can develop long chains of thought under a verifiable reward. The result is relevant to the harness: the reward and the verifier are part of the system.",
}


def research_sections() -> list[dict]:
    papers = ARXIV["papers"]
    by_topic: dict[str, list[dict]] = {}
    for p in papers:
        by_topic.setdefault(p.get("topic", "other"), []).append(p)
    order = ["quantization", "training", "attention", "long-context", "agents", "serving"]
    out = []
    for topic in order:
        group = sorted(by_topic.get(topic, []), key=lambda p: (p.get("year", ""), p["id"]))
        if not group:
            continue
        title = {
            "quantization": "Quantization: formats, scaling, and low-bit training",
            "training": "Training: adaptation, scaling, and optimisation memory",
            "attention": "Attention and sequence mixers",
            "long-context": "Long context, position, and retrieval",
            "agents": "Agents, tools, and instruction following",
            "serving": "Inference serving and speculative decoding",
        }[topic]
        body = [r"\section{" + tex(title) + r"}\label{ch:research-" + topic + "}"]
        body.append(tex(TOPIC_INTRO[topic]) + r"\par")
        body.append(r"\subsection{The register}")
        body.append(tex(
            f"This line of research contains {len(group)} papers in the live arXiv register. "
            f"The table lists the identifier, year, title, first author, and the first claim "
            f"of the abstract. Identifiers resolve on arXiv; the register is a reading aid, not "
            f"a substitute for the papers.") + r"\par")
        rows = paper_rows(group)
        body.append(table(["arXiv", "Year", "Title", "First author", "Opening claim"], rows))
        body.append(r"\subsection{Structured digests}")
        for p in group:
            if p["id"] not in DETAIL:
                continue
            body.append(r"\subsubsection{" + tex(p["title"]) + "}")
            meta = (f"arXiv:{p['id']} &middot; {p.get('year','')} &middot; "
                    f"{len(p.get('authors', []))} authors &middot; topic: {topic}.")
            body.append(tex(meta) + r"\par")
            body.append(tex(DETAIL[p["id"]]) + r"\par")
            body.append(tex("The paper is listed in the register above; the digest records the "
                            "mechanism that matters to this project, not a benchmark score.") + r"\par")
        out.append({"id": "research-" + topic, "part": "V", "title": title,
                    "body": "\n".join(body)})
    return out


THEOREM_CENDER = r"""
\section{Context, memory, and the cost of attention}\label{ch:theorem-cender}
The Fusion programme starts from a simple observation: a transformer's context window is a
memory system, and a memory system that grows with the input is not the same thing as a memory
system that remembers. This section states the design theorem behind Cender, the engine's
constant-memory sequence core. The theorem is deliberately modest. It does not claim that a
fixed-size state can store an arbitrary sequence; it proves the opposite, and then shows how an
exact paged store beside the state recovers the information the state cannot hold.

\subsection{Definitions}
Let $\Sigma$ be a finite alphabet and let $x_{1:n}\in\Sigma^n$ be an input sequence. An online
summarizer is a pair $(f,g)$ with state $s_t=f(s_{t-1},x_t)$, $s_t\in\mathcal{S}$, and output
$y_t=g(s_t,q_t)$ for a query $q_t$. A paged store is a map $\pi$ from token positions to
addresses in an external array; it is exact if $\pi(i)$ returns $x_i$ for every stored $i$.
The context-rot functional is
\[
  \Delta(n)=\sup_{q}\;\bigl|\,\mathbb{P}(y\mid x_{1:n},q)-\mathbb{P}(y\mid x_{1:n})\,\bigr|,
\]
the change in the next-token distribution when a query is placed at position $n$. A model has
context rot when $\Delta(n)$ grows with $n$ for a fixed query and a fixed amount of relevant
evidence.

\subsection{A finite-state bound}
\begin{theorem}[finite-state context bound]
Let $|\mathcal{S}|\le 2^m$. For every $n>2^m$ there exist two sequences $x_{1:n}$ and $x'_{1:n}$
with $s_n=s'_n$ but different suffix distributions. Consequently no online summarizer with
$m$ bits of state can answer every context-dependent query exactly for unbounded $n$.
\end{theorem}
\begin{proof}
The number of length-$n$ sequences over a non-empty alphabet is at least $2^n$. If $n>m$, the
map from sequences to states cannot be injective. Choose two sequences that collide. The future
is a function of the state alone, so the two sequences induce the same distribution over every
suffix; if the sequences differ on a position that a query can address, that distribution is
wrong for at least one of them.
\end{proof}
The bound is elementary, and that is the point. A larger context window does not escape it:
the window is still a finite state, and the collision argument applies at the window boundary.
What changes with a larger window is the constant, not the asymptotics. This is the formal
content of the empirical observation that long-context models degrade before their advertised
limit.

\subsection{The attention output is a low-rank read}
For a single attention head, let $Q=XW_Q$, $K=XW_K$, $V=XW_V$ with $X\in\mathbb{R}^{n\times d}$.
The output is $O=\operatorname{softmax}(QK^\top/\sqrt{d})\,V$. The softmax matrix is generally
full rank, but the output is a linear combination of the rows of $V$:
\[
  O = A V,\qquad A\in\mathbb{R}^{n\times n},\qquad \operatorname{rank}(O)\le \operatorname{rank}(V)\le d.
\]
Thus every attention output lies in a subspace of dimension at most $d$, regardless of $n$.
The observation does not bound the information in the coefficients; it bounds the number of
independent value directions that can be mixed. A model that needs to represent $r>d$ independent
value directions must widen the value projection, add heads, or route through an external store.

\subsection{The Cender recurrence}
Cender replaces the quadratic attention read with a decay state and an exact page table. For a
token $t$ with key $k_t\in\mathbb{R}^d$ and value $e_t\in\mathbb{R}^d$,
\begin{equation}
  s_t=\lambda s_{t-1}+k_t e_t^\top,\qquad 0<\lambda<1,
  \label{eq:cender}
\end{equation}
with $s_0=0$. Unrolling gives
\[
  s_t=\sum_{i=1}^{t}\lambda^{t-i}k_i e_i^\top.
\]
For a query $q$, the state read is
\[
  q^\top s_t=\sum_{i=1}^{t}\lambda^{t-i}(q^\top k_i)(e_i).
\]
The contribution of token $i$ decays geometrically. If $\|q^\top k_i\|\le B$ and $\|e_i\|\le E$,
the tail beyond a window of length $W$ is bounded by
\begin{equation}
  \left\|q^\top\!\left(s_t-\sum_{i=t-W+1}^{t}\lambda^{t-i}k_i e_i^\top\right)\right\|
  \le \frac{B E\,\lambda^{W}}{1-\lambda}.
  \label{eq:tail}
\end{equation}
Choosing $W=\lceil \log(\varepsilon(1-\lambda)/(BE))/\log\lambda\rceil$ makes the tail at most
$\varepsilon$. The state therefore handles local smoothing with a controlled approximation,
while the page table returns any indexed token exactly. The design does not pretend that the
state remembers everything; it separates the two jobs.

\begin{theorem}[decay-window bound]
For the recurrence \eqref{eq:cender}, the tail error after a window of length $W$ is at most
$BE\lambda^W/(1-\lambda)$. If a token is present in the page table, its contribution can be
retrieved with zero approximation error, independent of $W$.
\end{theorem}
\begin{proof}
The first claim is the geometric series in \eqref{eq:tail}. The second is the definition of the
page table: a lookup returns the stored value, not a function of the state.
\end{proof}

\subsection{What is implemented, and what is not}
The wire identity in the next section is implemented and covered by a regression test. The
Cender recurrence is a design: the engine still runs transformer attention, and the Cender
module is not in the tree. The theorem above is therefore a design contract, not a measured
result. The protocol in the final subsection is the experiment that would turn the contract into
evidence.

\subsection{Experimental protocol}
A credible test needs four baselines: dense attention at the same width, a sparse-attention
model with a comparable token budget, a recurrent mixer without a page table, and the full
Cender design. The metrics are next-token loss, exact retrieval accuracy at controlled
distances, multi-hop accuracy under distractors, and memory per sequence. The position of the
relevant evidence is varied factorially across the beginning, middle, and end of the context.
The seeds are fixed and the confidence intervals are reported. A result is admissible only if
the full design beats the recurrent baseline on retrieval and the dense baseline on memory at
the same loss.
"""

THEOREM_WIRE = r"""
\section{The wire identity theorem}\label{ch:theorem-wire}
The engine's index format begins with a magic string. The magic is not decoration: it is the
only evidence a reader has that a file claims to be an engine index rather than a model
manifest, a foreign container, or a truncated copy. The project resolved the identity in D-30:
the current engine magic is \texttt{Transformers-FusionIDX}, the legacy engine magic is
\texttt{TransCenderIDX}, and \texttt{SolIDX} is reserved for model manifests.

\subsection{The accepted set}
Let $M_1$ be the 22-byte string \texttt{Transformers-FusionIDX} followed by a NUL, let $M_2$ be
the pre-normalisation spelling with a capital \texttt{F} in \texttt{Formers}, also 22 bytes
including the NUL, and let $M_3$ be the 15-byte string \texttt{TransCenderIDX} followed by a NUL.
The reader accepts exactly
\[
  \mathcal{M}=\{M_1,M_2,M_3\}.
\]
The writer emits $M_1$ only. $M_2$ is read-only for files written before the spelling was
normalised. $M_3$ is the engine's former name, kept because old files still exist. The strings
\texttt{SolIDX} (7 bytes including the NUL) and \texttt{InNovaIDX} (10 bytes) are not in
$\mathcal{M}$.

\subsection{No prefix ambiguity}
\begin{theorem}[unique magic class]
No element of $\mathcal{M}$ is a proper prefix of another element. Consequently a reader that
compares the longest candidate first assigns every accepted file to exactly one magic class.
\end{theorem}
\begin{proof}
$M_1$ and $M_2$ have the same length and differ only in the case of one byte, so neither is a
prefix of the other. $M_3$ differs from both at the sixth byte: $M_3$ has \texttt{C}, while
$M_1$ and $M_2$ have \texttt{f}. A prefix of length six therefore separates the legacy magic
from the current family. The remaining comparisons are within a family of equal-length strings.
\end{proof}

\subsection{The parser state machine}
The reader proceeds in four states. In state $S_0$ it requires at least 23 bytes; 15 bytes for the
legacy magic plus 8 bytes of header is the minimum accepted file. In $S_1$ it compares the first
22 bytes against $M_1$ and $M_2$. In $S_2$, if that comparison fails, it compares the first 15
bytes against $M_3$. In $S_3$ it reads the 8-byte header and validates the bounds before any
payload access. A failure in $S_1$, $S_2$, or $S_3$ is a hard error; there is no scalar fallback
and no silent reinterpretation.

\begin{theorem}[soundness of the parser]
Every file accepted by the state machine has a unique magic class, a complete 8-byte header, and
a payload length consistent with the header. Every file whose magic is \texttt{SolIDX} or
\texttt{InNovaIDX} is rejected.
\end{theorem}
\begin{proof}
The first claim follows from the prefix theorem and the length gate. The second follows from the
header read in $S_3$ and the bounds check. The third follows because neither string is in
$\mathcal{M}$ and the state machine has no other accepting branch.
\end{proof}

\subsection{Why the distinction matters}
A model name is not a wire identity. \texttt{Sol} names the trained model family; \texttt{SolIDX}
is reserved for model manifests, and no engine consumer exists today. Treating the model name as
the engine magic would make old engine files unreadable and would conflate two namespaces that
have different owners and different lifetimes. The theorem is small, but it protects a large
amount of stored data.

\subsection{Regression evidence}
The wire test suite exercises the accept/reject split directly. It opens a file with the legacy
magic, asserts that the current magic is emitted by the writer, asserts that the retired
identifiers are rejected, and checks the minimum-size guard. The test is part of the engine's
standing suite, not a one-off script. The exact case count is recorded in the test register in
Part VIII.
"""

THEOREM_PROTOCOL = r"""
\section{Evidence, falsification, and the limits of the theorem}\label{ch:theorem-protocol}
A theorem is only as useful as the experiment that can falsify its assumptions. This section
records the protocol that the Cender design must satisfy, the measurements that would count as
evidence, and the claims that the current tree cannot support.

\subsection{The three evidence classes}
The project uses three labels. \textbf{Disk-verified} means a claim was re-read from the tree on
a stated date and a command or test reproduces it. \textbf{Paper-only} means the claim comes from
the literature and has not been re-run on this hardware. \textbf{Operator-supplied} means the
claim is a requirement or a ruling, not a measurement. The label is part of the claim. A sentence
without a label inherits the weakest label in its paragraph.

\subsection{Falsifiers}
The Cender design fails if any of the following is observed. First, the decay state alone matches
the full design on exact retrieval at distances beyond the window; that would mean the page table
is unnecessary. Second, the page table costs more memory than the attention cache it replaces at
the target sequence length. Third, the full design loses more than two points of next-token
accuracy relative to dense attention at the same width. Fourth, the retrieval gain disappears
when distractors are added. Each falsifier is a stop condition, not a tuning opportunity.

\subsection{Statistics}
The protocol uses at least five seeds per configuration. The primary metric is the mean loss with
a bootstrap confidence interval. Retrieval is reported as exact-match accuracy with a Wilson
interval. Memory is reported as bytes per sequence at 4k, 16k, 64k, and 256k tokens. Latency is
reported as median and 95th percentile. A result is not called an improvement unless the
confidence intervals separate.

\subsection{What the current tree supports}
The tree supports the wire theorem, the format ladder, the test inventory, and the engine
specification. It does not support a claim that Cender has been trained, that the recurrent core
is faster than attention on this device, or that the 1.0 BPW goal has been reached. Those are
design targets. The report states them as targets and keeps the measured facts separate.
"""


def theorem_sections() -> list[dict]:
    import book_sources
    frozen = book_sources.clean_text(
        book_sources.read(".plan/_archive/docs/THEOREM_CENDER.md"))
    frozen_body = (r"\section{The frozen Cender theorem note}\label{ch:theorem-frozen}"
                   + "\n" + booktex.convert(frozen) + "\n")
    return [
        {"id": "theorem-cender", "part": "VI", "title": "Context, memory, and the cost of attention",
         "body": THEOREM_CENDER},
        {"id": "theorem-wire", "part": "VI", "title": "The wire identity theorem",
         "body": THEOREM_WIRE},
        {"id": "theorem-protocol", "part": "VI", "title": "Evidence, falsification, and limits",
         "body": THEOREM_PROTOCOL},
        {"id": "theorem-frozen", "part": "VI", "title": "The frozen Cender theorem note",
         "body": frozen_body},
    ]


METHOD = r"""
\section{The research method}\label{ch:method}
The project runs one loop for every domain: research, design, implement, audit, fix, verify, and
close. The loop is deliberately boring. Research collects the literature and the shipped
artifacts; design writes the contract before the code; implementation lands in the component that
owns the behaviour; the audit passes are independent; every found defect is fixed; verification
runs the standing suite; and closure updates the queue and the dashboard. A phase that skips a
step is not a shorter phase, it is a phase with an unrecorded debt.

\subsection{Research is evidence collection}
The research step has two outputs: a source map and a claim list. The source map names the papers,
the shipped binaries, the registry entries, and the files that were actually read. The claim list
separates what was observed from what was inferred. A claim that cannot be tied to a source is
kept as a question, not promoted to a fact. This is why the research index has an evidence status
column and why the claim ledger is longer than the prose chapters.

\subsection{Design writes the contract}
The design step produces a short contract: the inputs, the outputs, the invariants, the failure
modes, and the test that proves the contract. The format ladder is the clearest example. A format
name is not a label of convenience; it promises a nominal bit width, a wire identifier, and a
decode path. If the promise is broken, the format is retired rather than renamed.

\subsection{Implementation lands in the owner}
A cross-repository change lands in the component first. The superproject records the pin and the
consequence. This rule prevents the superproject from becoming a second source of truth and makes
a cold start possible: a reader can reconstruct which engine and which launcher produced a given
document.

\subsection{The audit passes}
The audit is not a review of style. Each pass has a distinct target: memory safety, wire-format
compatibility, path and gate consistency, numerical honesty, and the Inferno breakdown. A pass
that finds nothing still produces a line in the ledger, because the absence of a finding is
evidence only if the pass actually ran. The audit frequency is five to ten passes per domain; the
number is a floor, not a target.

\subsection{Closure is a state change}
A task closes when the queue row is updated, the dashboard is regenerated, and the evidence is
linked. A commit without a queue update is not closure. A dashboard without a delta is not a
status report. The project has paid for this rule more than once: a task that looked complete in
chat but had no row in the tree drifted back into the queue within a day.
"""

EVIDENCE = r"""
\section{The evidence register}\label{ch:evidence}
The report separates the evidence that can be re-run from the evidence that can only be read.
This section is the bridge between the two: it lists the standing instruments, the counts they
produce, and the claims they support.

\subsection{The standing instruments}
The project keeps seven verifiers and one consistency gate. The verifiers cover the plan headings,
the anchors, the sub-anchors, the corruption scan, the phase ledger, the arXiv re-resolution, and
the documentation line counts. The gate compares the registry against the launcher HTML, the
launcher manifest, the card order, the alias ladder, the resolve map, and the part folders. A
green gate is not a proof of quality; it is a proof that the data and the generated surfaces
agree.

\subsection{The counts}
\begin{center}
\footnotesize
\begin{tabular}{@{}lr@{}}
\toprule
Instrument & Count \\
\midrule
Valid wire formats & @@FORMATS@@ \\
Retired formats & @@RETIRED@@ \\
Test files & @@TESTS@@ \\
Declared assertions & @@ASSERTS@@ \\
Engine libraries & @@LIBS@@ \\
Engine targets & @@TARGETS@@ \\
Compute backends & @@BACKENDS@@ \\
Launcher seats & @@SEATS@@ \\
Decisions & @@DECISIONS@@ \\
Research items & @@RESEARCH@@ \\
Archived documents & 81 \\
\bottomrule
\end{tabular}
\end{center}

\subsection{What the numbers mean}
A format count is a contract count, not a marketing count. A test-file count is a file count, not
a coverage percentage. An assertion count is a static count of declared assertions, not a count
of executed assertions. The report keeps these distinctions because the project has already been
burned by a number that was true in one sense and false in another.

\subsection{The claim ledger}
The claim ledger is the longest evidence table in the report. Each row records a claim, a verdict,
the file and line that support it, and the round in which it was checked. The verdict vocabulary
is small: verified, partial, fake, retired, and open. A row marked fake is not deleted; it is kept
so that a later reader can see what was believed and why it failed.
"""

VALIDITY = r"""
\section{Threats to validity}\label{ch:validity}
Every report has a boundary. This section names the boundary before a reader finds it.

\subsection{Source drift}
The tree moves while the report is being written. Counts can change between the extraction and
the render. The report mitigates this by stating counts as edition facts and by naming the
register that produced them; it does not claim that a count will be true tomorrow. A reader who
needs the current count should read the register, not the prose.

\subsection{Generated prose}
Some project documents were produced by a generator from live facts. Those documents are useful
because their numbers are tied to the tree, but their prose can repeat. This report treats the
repetition as a defect to be removed, not as volume to be preserved. Where a generated sentence
was only a restatement of the previous sentence, it was dropped.

\subsection{Unverified literature}
The research compendium reports arXiv metadata and short digests. It does not claim that every
paper was reproduced on this hardware. A digest is a reading note, not an experimental result.
The experiment that would validate a paper for this project is named where it matters, and the
absence of that experiment is stated.

\subsection{Hardware limits}
The engine targets an AMD Radeon Vega 7 integrated GPU on Windows. CUDA, HIP, Vulkan GEMM, and
WebGPU are unavailable or unproven on this host. A speed claim that depends on those backends is
therefore unmeasurable here. The report does not convert an unavailable backend into a zero; it
labels the measurement as unmeasurable.

\subsection{The 1.0 BPW goal}
The implemented path is 1.5 bits per weight. The goal is 1.0. The gap is a research target, not a
rounding error. Any sentence that presents 1.5 as the goal is wrong, and any sentence that presents
1.0 as achieved is also wrong. The report keeps both statements visible.
"""


def method_sections() -> list[dict]:
    ev = (EVIDENCE.replace("@@FORMATS@@", str(F.N_FORMATS))
          .replace("@@RETIRED@@", str(F.N_RETIRED))
          .replace("@@TESTS@@", str(F.N_TESTS))
          .replace("@@ASSERTS@@", f"{F.N_ASSERTS:,}")
          .replace("@@LIBS@@", str(F.N_LIBS))
          .replace("@@TARGETS@@", str(F.N_TARGETS))
          .replace("@@BACKENDS@@", str(F.N_BACKENDS))
          .replace("@@SEATS@@", str(F.N_SEATS))
          .replace("@@DECISIONS@@", str(F.N_DECISIONS))
          .replace("@@RESEARCH@@", str(F.N_RESEARCH)))
    return [
        {"id": "method", "part": "VII", "title": "The research method", "body": METHOD},
        {"id": "evidence", "part": "VII", "title": "The evidence register", "body": ev},
        {"id": "validity", "part": "VII", "title": "Threats to validity", "body": VALIDITY},
    ]
