#!/usr/bin/env python3
"""Appendices (20), glossary (8), bibliography (6), index (4), closing (2)."""
from __future__ import annotations

from pubfacts import (FORMATS, RETIRED, TESTS, LIBS, TARGETS, BACKENDS,
                      SRC, SEATS, DECISIONS, RESEARCH, REG, LAY,
                      N_FORMATS, N_RETIRED, N_TESTS, N_CASES, N_ASSERTS,
                      N_FILES, N_LOC, CODE_FILES, CODE_BYTES, TF_HEAD, CODE_HEAD,
                      FUSION_HEAD, human)


def raw(title: str, body: list[str], kind: str = "page") -> dict:
    return {"title": title, "body": body, "kind": kind}


def tab(title: str, header: list[str], rows: list[str], notes: list[str]) -> dict:
    body = ["| " + " | ".join(header) + " |",
            "|" + "|".join(["---"] * len(header)) + "|"] + rows + notes
    return raw(title, body[:30])


def appendix_pages() -> list[dict]:
    A = []
    docs = __import__("json").load(open(
        __import__("os").path.join(__import__("os").path.dirname(__file__),
                                   "..", "..", ".plan", "telemetry", "docgen", "facts.json"),
        encoding="utf-8"))["fusion"]["doc_inventory"]
    A.append(tab("A. Repository inventory",
                 ["Document", "Lines", "Bytes"],
                 [f"| `{d['file']}` | {d['lines']:,} | {d['bytes']:,} |" for d in docs],
                 ["The inventory lists authored Markdown in `.plan/`.",
                  "The archive and the scratch trees are excluded.",
                  "The inventory is generated from the live tree.",
                  "The superproject pins the two components."]))
    A.append(tab("B. Engine source tree",
                 ["Directory", "Files", "Lines"],
                 [f"| `src/{d['dir']}/` | {d['files']} | {d['loc']:,} |" for d in SRC],
                 ["The tree is generated from `transformers/src/`.",
                  "The counts include C++, headers and CUDA sources.",
                  "The tree is part of the engine commit.",
                  "The next appendix lists the libraries."]))
    A.append(tab("C. Library index",
                 ["Library", "Purpose"],
                 [f"| `{x}` | engine component |" for x in LIBS],
                 ["The index is generated from `CMakeLists.txt`.",
                  "A library is an internal build unit, not a package.",
                  "The next appendix lists the executables."]))
    A.append(tab("D. Executable index",
                 ["Executable", "Kind"],
                 [f"| `{x}` | command-line tool |" for x in TARGETS],
                 ["The index is generated from `CMakeLists.txt`.",
                  "The tools are safe to re-run.",
                  "The benchmarks are part of the evidence protocol.",
                  "The next appendix lists the backends."]))
    A.append(tab("E. Backend index",
                 ["Backend", "Class"],
                 [f"| `{b.split('=')[0].strip()}` | compute backend |" for b in BACKENDS],
                 ["The index is generated from `include/quant/backend.h`.",
                  "A compiled backend is not the same as a supported backend.",
                  "The capability contract is the source of truth.",
                  "The next appendices index the formats."]))
    f = [f"| `{x['name']}` | {x['id']} | {x['bpw']:.2f} | {x['family']} |" for x in FORMATS]
    A.append(tab("F. Valid formats, part 1",
                 ["Format", "Id", "BPW", "Family"], f[:24],
                 ["The table is generated from the enum.",
                  "The BPW is nominal and wire.",
                  "The next page continues the list."]))
    A.append(tab("G. Valid formats, part 2",
                 ["Format", "Id", "BPW", "Family"], f[24:48],
                 ["The list continues from the previous page.",
                  "The grouped family repeats the base ladder.",
                  "The next page continues the list."]))
    A.append(tab("H. Valid formats, part 3",
                 ["Format", "Id", "BPW", "Family"], f[48:],
                 ["The list continues from the previous page.",
                  f"The ladder carries {N_FORMATS} valid formats.",
                  "The next appendices index the retired ids."]))
    rr = [f"| `{x['id']}` | `{x['name']}` | {x['bpw']:.2f} |" for x in RETIRED]
    A.append(tab("I. Retired ids, part 1",
                 ["Id", "Name", "BPW"], rr[:18],
                 ["Retired ids stay addressable.",
                  "A writer never emits them.",
                  "The next page continues the list."]))
    A.append(tab("J. Retired ids, part 2",
                 ["Id", "Name", "BPW"], rr[18:],
                 ["The list continues from the previous page.",
                  f"The retired set carries {N_RETIRED} ids.",
                  "The next appendices index the tests."]))
    t = [f"| `{x['file']}` | {x['lines']} | {len(x['cases'])} | {x['asserts']} |" for x in TESTS]
    A.append(tab("K. Test index, part 1",
                 ["Test file", "Lines", "Cases", "Asserts"], t[:26],
                 ["The index is generated from `tests/`.",
                  "The case count is the number of named tests.",
                  "The next page continues the list."]))
    A.append(tab("L. Test index, part 2",
                 ["Test file", "Lines", "Cases", "Asserts"], t[26:52],
                 ["The list continues from the previous page.",
                  "The suite is built as separate executables.",
                  "The next page continues the list."]))
    A.append(tab("M. Test index, part 3",
                 ["Test file", "Lines", "Cases", "Asserts"], t[52:],
                 ["The list continues from the previous page.",
                  f"The suite carries {N_TESTS} files, {N_CASES} cases and {N_ASSERTS:,} asserts.",
                  "The next appendix lists the seats."]))
    A.append(tab("N. Seat registry",
                 ["Codename", "Alias", "Folder", "Status"],
                 [f"| **{s['codename']}** | {s.get('alias') or '—'} | `{s['folder']}` | {s['status']} |"
                  for s in SEATS],
                 ["The table is generated from `arch/windows.json`.",
                  "Seven rows are registry parts; two are support folders.",
                  "The next appendix lists the layouts."]))
    A.append(tab("O. Layout index",
                 ["#", "Layout", "Part"],
                 [f"| {l['n']} | {l['name']} | {l['part']} |" for l in LAY.get("layouts", [])],
                 ["The table is generated from `arch/layouts.json`.",
                  "The Editor window is a singleton available from every layout.",
                  "The Fusion window carries the layout picker.",
                  "The next appendix lists the decisions."]))
    A.append(tab("P. Research index",
                 ["Item", "Title"],
                 [f"| **{r['id']}** | {r['title']} |" for r in RESEARCH],
                 ["The index is generated from `.plan/RESEARCH-INDEX.md`.",
                  "The item's evidence status is recorded in the index.",
                  "The next appendix lists the verifiers."]))
    A.append(raw("Q. Verifier register", [
        "| Verifier | Scope | Expected |",
        "|---|---|---|",
        "| `verify_step1.py` | coverage rows and headings | exit 0 |",
        "| `step2_fix2_verify.py` | Step-2 fixes | exit 0 |",
        "| `step3_verify.py` | anchor report | exit 0 |",
        "| `step3_subanchors.py` | sub-anchor report | exit 0 |",
        "| `verify_step5.py` | 65 checks | exit 0 |",
        "| `step6_audit.py` | final report audit | exit 0 |",
        "| `arxiv_recheck.py` | arXiv identifiers | exit 0 |",
        "| `check-consistency.mjs` | launcher registry | 13/13 |",
        "The verifiers run from `.plan/.rea-tmp/`.",
        "The launcher gate runs from the `code` repository.",
        "A failure is a red gate.",
        "The next appendix lists the audits.",
    ]))
    A.append(raw("R. Audit register", [
        "| Audit | Scope | State |",
        "|---|---|---|",
        "| 1 | quant wire path | complete |",
        "| 2 | MX quarantine enforcement | open |",
        "| 3 | generation paths and V20 JIT bounds | open |",
        "| 4 | Inferno memory safety | open |",
        "| 5 | dead code | open |",
        "| 6 | bench honesty | open |",
        "| 7 | import and adapter paths | open |",
        "| 8 | install-test duplicate header | open |",
        "| 9 | production label reads | open |",
        "| 10 | final sweep | open |",
        "Audit 1 produced a finding, a fix and a regression test.",
        "An open audit is not a failure; a hidden audit is.",
        "The next appendix is the manifest.",
    ]))
    A.append(raw("S. Publication manifest", [
        f"Report: `report/Fusion-Report-512.pdf` and `.docx`, 512 pages each.",
        "Whitepaper: `whitepaper/WHITEPAPER.pdf` and `.docx`, 28 pages.",
        "Theorem note: `theorem/THEOREM-CENDER.pdf` and `.docx`, 14 pages.",
        "arXiv: `arxiv/main.tex` and `arxiv/references.bib`.",
        "Architecture: `ARCHITECTURE.md`.",
        "Index: `README.md`. Manifest: `MANIFEST.json`.",
        f"Fusion README: 2,048 lines. CodeFusion README: 4,096 lines.",
        "Transformers README: 6,144 lines.",
        f"Engine commit: `{TF_HEAD}`. Launcher commit: `{CODE_HEAD}`.",
        f"Superproject commit: `{FUSION_HEAD}`.",
        "The hashes are recorded in `MANIFEST.json`.",
        "The next appendix is the edition record.",
    ]))
    A.append(raw("T. Edition record", [
        "Edition 2026.11.",
        "Generated from the live tree.",
        f"Engine source files: {N_FILES:,}; engine source lines: {N_LOC:,}.",
        f"Launcher tracked files: {CODE_FILES:,}; tracked bytes: {human(CODE_BYTES)}.",
        f"Valid formats: {N_FORMATS}. Retired ids: {N_RETIRED}.",
        f"Tests: {N_TESTS} files, {N_CASES} cases, {N_ASSERTS:,} asserts.",
        "PDF engine: pdfLaTeX, TeX Live 2026.",
        "DOCX engine: python-docx, verified through Word.",
        "Cover mark: project-authored TikZ.",
        "The edition is reproducible with the command in the colophon.",
    ]))
    return A


def glossary_pages() -> list[dict]:
    groups = [
        ("A–C", [
            ("Alias", "An edition label such as Lite, Plus, Pro, Studio, Max or Ultra."),
            ("Attention", "The softmax-weighted lookup at the core of the transformer."),
            ("Backend", "A compute path selected by the engine, such as AVX2, CUDA or Metal."),
            ("Bit width", "The number of bits a format spends per weight."),
            ("Block", "The unit a format encodes, with its own scale or mean."),
            ("Block codec", "The component that maps a tensor block to wire bytes and back."),
            ("BPW", "Bits per weight; the wire cost of one quantized parameter."),
            ("Canonical name", "The one spelling of a format, such as Q_4 or Q_G_8_K_H."),
            ("Checkpoint", "A file that stores model weights and their format identities."),
            ("Codename", "The address of a launcher part, such as Ingot or Onyx."),
            ("Codebook", "A table of reconstruction points used by a format."),
        ]),
        ("D–F", [
            ("Decision", "A binding rule recorded in the decision log with an id."),
            ("Delta rule", "The recurrence that updates the Cender state."),
            ("Determinism", "The property that the same input and format produce the same bytes."),
            ("DSpine", "Adjacent causal injection for speculative decoding."),
            ("EAIN", "The neuron-level continual-learning design."),
            ("Evidence standard", "A command, an output and a file:line reference."),
            ("Fact extractor", "The script that turns the live tree into `facts.json`."),
            ("Format id", "The stable integer that names a format on the wire."),
            ("Format registry", "The table that maps a canonical name to an id and a description."),
            ("FP8", "An eight-bit floating-point format with a small exponent range."),
            ("Fusion", "The superproject that pins the engine and the launcher."),
        ]),
        ("G–I", [
            ("Gate", "A check that stops the step when it fails."),
            ("GLE", "The engine's structured report path."),
            ("GRP", "The grouped quantization family with per-group scales."),
            ("H tier", "A K-quant tier at base + 0.50 BPW."),
            ("Identity contract", "The name, nominal, wire and id agreement."),
            ("Inferno", "The kernel and training-engine programme."),
            ("Integer path", "The quantization path that stores indices rather than floats."),
            ("iGPU", "An integrated GPU backend mode."),
            ("Imprint", "The page that records the edition and the commits."),
        ]),
        ("J–L", [
            ("KAT", "A known-answer test that pins the exact bytes."),
            ("KV cache", "The inference-time state that grows with context length."),
            ("Ladder", "The 69-format quantization grid."),
            ("Latency", "The time a request takes from arrival to response."),
            ("Layout", "An in-app choice that maps an edition to a launcher part."),
            ("Lite", "The first alias in the edition ladder, mapped to Zingma."),
            ("Loop transformer", "A transformer that reuses layers across depth."),
            ("Loop quantization", "Quantization aware of the looped execution graph."),
            ("L tier", "The base tier at an exact integer BPW."),
        ]),
        ("M–O", [
            ("M tier", "A K-quant tier at base + 0.25 BPW."),
            ("MX", "The mixed-format block family quarantined by D-13."),
            ("MoE", "Mixture of experts."),
            ("NCM", "Next-Concept Modeling, a generation mechanism."),
            ("Nominal BPW", "The BPW a format's name advertises."),
            ("Onyx", "The VS Code OSS seat of the launcher."),
            ("Operator", "The human owner of the project and its decisions."),
            ("Orthogonal write", "A state write whose key is projected away from the frozen core."),
        ]),
        ("P–R", [
            ("Page block", "A heading plus at most thirty body lines, sized to one page."),
            ("Pin", "A submodule commit, not a branch."),
            ("Plain family", "The base formats and their K-quant scale variants."),
            ("QAT", "Quantization-aware training."),
            ("Quantization", "Storing weights in fewer bits than the dense dtype."),
            ("Reader contract", "The rules a decoder must follow for untrusted bytes."),
            ("Retired id", "An identifier that stays addressable but is not a valid format."),
            ("Roofline", "The memory or compute bound that limits a kernel."),
        ]),
        ("S–U", [
            ("Seat", "The folder and metadata reserved for a launcher part."),
            ("Sonar", "The reserved DeepSeek Harness seat."),
            ("Submodule", "A repository pinned by the superproject."),
            ("Telemetry", "The generated dashboard that records the live state."),
            ("Ternary", "A three-level format at 1.5 BPW."),
            ("Theorem note", "The 14-page formal extract of the report."),
            ("Track A", "The implemented traditional quantization ladder."),
            ("Track B", "The open loop-quantization research track."),
            ("Ultra", "The last alias in the edition ladder, mapped to Zenix."),
        ]),
        ("V–Z", [
            ("Verifier", "A script that checks the plan against the tree."),
            ("Whitepaper", "The 28-page argument extract of the report."),
            ("Wire BPW", "The bits a block actually spends per weight."),
            ("Wire format", "The byte layout a checkpoint or socket carries."),
            ("Zenix", "The native Claude Desktop seat."),
            ("Zingma", "The Qoder Quest/agents seat."),
            ("Zero-copy", "A path that avoids an intermediate decode or copy."),
            ("ZendNN", "The AMD Zen deep-learning backend."),
            ("Block geometry", "The block size and field layout implied by a format."),
            ("Quarantine", "A state in which a format is addressable but not promoted."),
        ]),
    ]
    out = []
    for name, terms in groups:
        body = []
        for term, definition in terms:
            body.append(f"**{term}** — {definition}")
        out.append(raw(f"Glossary {name}", body))
    return out


REFS = [
    ("Vaswani et al., Attention Is All You Need", "NeurIPS 2017 · arXiv:1706.03762",
     "The baseline attention formulation used throughout the engine."),
    ("Dehghani et al., Universal Transformers", "ICLR 2019 · arXiv:1807.03819",
     "The looped-transformer line that the loop research extends."),
    ("Dettmers et al., LLM.int8()", "NeurIPS 2022 · arXiv:2208.07339",
     "Mixed-precision matrix multiplication for large language models."),
    ("Frantar et al., GPTQ", "ICLR 2023 · arXiv:2210.17323",
     "Post-training quantization by layer-wise error compensation."),
    ("Lin et al., AWQ", "MLSys 2024 · arXiv:2306.00978",
     "Activation-aware weight quantization."),
    ("Xiao et al., SmoothQuant", "ICML 2023 · arXiv:2211.10438",
     "Smoothing activation outliers for post-training quantization."),
    ("Dettmers et al., QLoRA", "NeurIPS 2023 · arXiv:2305.14314",
     "Fine-tuning of quantized models with low-rank adapters."),
    ("Ma et al., The Era of 1-bit LLMs", "arXiv:2402.17764 · 2024",
     "The 1.58-bit ternary line that the 1.5 BPW path touches."),
    ("Wang et al., BitNet", "arXiv:2310.11453 · 2023",
     "Scaling 1-bit transformers."),
    ("Micikevicius et al., FP8 Formats for Deep Learning", "arXiv:2209.05433 · 2022",
     "The FP8 format family and its special values."),
    ("Rouhani et al., Microscaling Data Formats", "arXiv:2310.10537 · 2023",
     "The MX block family that D-13 quarantines."),
    ("Yang et al., Parallelizing Linear Transformers with the Delta Rule",
     "NeurIPS 2024 · arXiv:2406.06484", "The delta-rule line behind the Cender recurrence."),
    ("Behrouz et al., Titans: Learning to Memorize at Test Time", "arXiv:2501.00663 · 2024",
     "A fixed-state memory module related to the Cender design."),
    ("Katharopoulos et al., Transformers are RNNs", "ICML 2020 · arXiv:2006.16236",
     "Linear attention as a recurrent formulation."),
    ("Dao et al., FlashAttention", "NeurIPS 2022 · arXiv:2205.14135",
     "IO-aware exact attention and the kernel tradition the engine follows."),
    ("Shazeer, Fast Transformer Decoding", "arXiv:1911.02150 · 2019",
     "Multi-query attention and the KV-cache pressure it addresses."),
    ("Ainslie et al., GQA", "EMNLP 2023 · arXiv:2305.13245",
     "Grouped-query attention."),
    ("Su et al., RoFormer", "arXiv:2104.09864 · 2021",
     "Rotary position embeddings."),
    ("Zhang & Sennrich, Root Mean Square Layer Normalization", "NeurIPS 2019 · arXiv:1910.07467",
     "RMSNorm, used in the model layer."),
    ("Shazeer, GLU Variants Improve Transformer", "arXiv:2002.05202 · 2020",
     "Gated linear units in the feed-forward path."),
    ("Hoffmann et al., Training Compute-Optimal Large Language Models",
     "NeurIPS 2022 · arXiv:2203.15556", "Scaling-law context for the training programme."),
    ("Kaplan et al., Scaling Laws for Neural Language Models", "arXiv:2001.08361 · 2020",
     "The earlier scaling-law reference."),
    ("Rajbhandari et al., ZeRO", "SC 2020 · arXiv:1910.02054",
     "Memory optimisation for distributed training."),
    ("Micikevicius et al., Mixed Precision Training", "ICLR 2018 · arXiv:1710.03740",
     "Loss scaling and mixed-precision training."),
    ("Loshchilov & Hutter, Decoupled Weight Decay Regularization",
     "ICLR 2019 · arXiv:1711.05101", "AdamW."),
    ("Kingma & Ba, Adam", "ICLR 2015 · arXiv:1412.6980", "The base optimizer."),
    ("Fedus et al., Switch Transformers", "JMLR 2022 · arXiv:2101.03961",
     "Sparse mixture-of-experts routing."),
    ("Shazeer et al., Outrageously Large Neural Networks", "ICLR 2017 · arXiv:1701.06538",
     "The sparsely-gated MoE layer."),
    ("Hu et al., LoRA", "ICLR 2022 · arXiv:2106.09685", "Low-rank adaptation."),
    ("Kirkpatrick et al., Overcoming Catastrophic Forgetting", "PNAS 2017 · arXiv:1612.00796",
     "Elastic weight consolidation and the continual-learning line."),
    ("NIST, FIPS 180-4 Secure Hash Standard", "2015",
     "The SHA-256 used by the index format."),
    ("IEEE 754-2019, Standard for Floating-Point Arithmetic", "2019",
     "The floating-point semantics the FP path depends on."),
    ("ISO/IEC 14882:2020, Programming Languages — C++", "2020",
     "The C++20 language standard used by the engine."),
    ("Fusion, D-31: exact documentation targets", ".plan/docs/operation-clean/DECISIONS.md",
     "The decision that defines this edition."),
    ("Fusion, LADDER.md", ".plan/docs/operation-clean/LADDER.md",
     "The derivation of the 69-format ladder."),
    ("Fusion, THEOREM_CENDER.md", ".plan/_archive/docs/THEOREM_CENDER.md",
     "The archived statement of the Cender theorem."),
]


def bibliography_pages() -> list[dict]:
    out = []
    per = 6
    for i in range(0, len(REFS), per):
        chunk = REFS[i:i + per]
        body = []
        for title, where, note in chunk:
            body.append(f"**{title}.** {where}.")
            body.append(note)
            body.append("")
        out.append(raw(f"Bibliography {i // per + 1}", [l for l in body if l.strip()]))
    return out


def closing_pages() -> list[dict]:
    return [
        {"title": "Colophon", "kind": "page", "body": [
            "This edition was generated from the live tree.",
            f"Superproject commit: `{FUSION_HEAD}`.",
            f"Engine commit: `{TF_HEAD}`. Launcher commit: `{CODE_HEAD}`.",
            "The report is exactly 512 pages in PDF and DOCX.",
            "The three READMEs are exactly 2,048, 4,096 and 6,144 lines.",
            "The facts come from `.plan/telemetry/docgen/facts.json`.",
            "The PDF is typeset with pdfLaTeX from TeX Live 2026.",
            "The DOCX is generated with python-docx and verified through Word.",
            "The cover mark is project-authored TikZ.",
            "The body type is Latin Modern.",
            "The code type is Inconsolata.",
            "The report is a documentation deliverable, not a peer-reviewed publication.",
            "The report does not relicense the code it describes.",
            "The archive is reference-only.",
            "The next edition is a new commit, not an edit in place.",
        ]},
        {"title": "End", "kind": "end", "body": [
            "Fusion · The Superproject Technical Report",
            "Edition 2026.11 · 512 pages",
            "Generated from the live tree.",
        ]},
    ]
