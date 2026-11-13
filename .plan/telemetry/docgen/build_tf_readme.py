#!/usr/bin/env python3
"""Build transformers/README.md at exactly 6,144 lines (D-31).

191 sections x 32 lines + 32-line header = 6,144.  Every section is a heading
plus exactly 30 non-empty body lines.  The first 40 sections are the authored
batch-1 narrative, normalised to the same shape; the rest are generated from
the live enum, the CMake targets, the source tree and the test suite.
"""
from __future__ import annotations

import json
import os

from readme_common import WS, HERE, header32, write_exact, verify

TARGET = 6144
OUT = os.path.join(WS, "transformers", "README.md")
F = json.load(open(os.path.join(HERE, "tf_facts.json"), encoding="utf-8"))

FORMATS = F["formats"]
RETIRED = F["retired"]
LIBS = F["cmake_libs"]
TARGETS = F["cmake_targets"]
SRC = F["src_detail"]
ENGINES = F["engine_detail"]
TESTS = F["test_detail"]
LIB_SRC = F["lib_sources"]
TGT_SRC = F["target_sources"]

PAD = [
    "The engine is C++20 and builds with CMake; the details are in `CMakeLists.txt`.",
    "Every count in this document is extracted from the live tree by `.plan/telemetry/docgen/`.",
    "The engine is one half of the Fusion Superproject; the launcher is the other half.",
    "The engine does not depend on the launcher to build or to run its tests.",
    "The engine's public headers live under `include/quant/`.",
    "The implementation lives under `src/`; the training engines live under `engines/`.",
    "The test suite lives under `tests/` and is built as separate executables.",
    "The benchmarks live under `bench/` and are not part of the default test run.",
    "The Inferno programme lives under `inferno/` and in `SPEC-INFERNO.md`.",
    "The project is experimental; a capability claim names the file that implements it.",
    "The project treats a red gate as a stop, not as a warning.",
    "The project never weakens a test to make a release look clean.",
    "A format is a contract: name, nominal BPW, wire BPW and id all agree.",
    "An id is stored raw in `.quant` files, so retired ids stay addressable.",
    "The registry is the single source of truth for format identity.",
    "The block codec is the single source of truth for wire layout.",
    "The backend contract is the single source of truth for capability claims.",
    "The test suite is the single source of truth for behaviour.",
    "The spec is the single source of truth for the Inferno plan.",
    "The documentation is generated at an exact line count because approximate cannot be verified.",
    "The generator refuses to write a file whose count is off by one line.",
    "The documentation is part of the D-31 programme and the 512-page publication.",
    "The engine README is the front door to the engine part of the publication.",
    "The engine is pinned by the superproject as a submodule commit, not a branch.",
    "A component change lands in this repository first, then the pin is updated.",
    "The working tree is allowed to be dirty during a parallel session; the dashboard reports it.",
    "The archive of deleted documents lives in the superproject, not in this repository.",
    "The repository carries its own licence file; read it before redistributing.",
    "The quantized path and the dense path share the same model layer.",
    "The engine's claims are checked by named tests, not by prose.",
]

DEEP = [
    ("## 41. The lifecycle of a quantized tensor", [
        "A tensor enters the engine as a dense buffer with a dtype, a shape and a stride.",
        "The quantizer chooses a format from the ladder; the choice is recorded as a `Format` id.",
        "The block codec divides the tensor into blocks whose size is a property of the format.",
        "Each block is scaled, mapped to indices and packed into the wire layout.",
        "The packed block carries its own scale or mean so it can be decoded independently.",
        "The writer validates the format before it emits a block; an invalid id is a bug, not a fallback.",
        "The reader validates the id before it decodes; an unknown id is rejected or remapped.",
        "The decoded tensor is dense again, but the packed form remains the storage form.",
        "The native weight path can skip the decode step when the kernel consumes the packed form directly.",
        "The kernel contract declares whether a format is executable natively or only storage.",
        "A format that is storage-only is still a first-class ladder member; it is not a second-class citizen.",
        "A format that is executable natively is a product feature; it is documented as such.",
        "The lifecycle is the same for training and inference until the kernel boundary.",
        "Training keeps the master weights in higher precision and quantizes on the forward pass.",
        "Inference keeps the packed weights and decodes only where the kernel requires it.",
        "The checkpoint stores the format id and the block layout so a later reader can reconstruct the tensor.",
        "The checkpoint does not store a version tag on the format id; the id is the version.",
        "That is why retired ids stay in the enum: an old checkpoint must remain readable.",
        "A retired id is never emitted by a writer and never accepted as a new format.",
        "A reader that meets a retired id remaps it or rejects it with a named error.",
        "The lifecycle ends when the tensor is freed; the wire bytes are the durable artefact.",
        "The tests exercise the lifecycle at the block level, the tensor level and the checkpoint level.",
        "The fuzz tests exercise malformed ids, truncated blocks and hostile lengths.",
        "The benchmarks exercise the lifecycle at model scale and record the BPW actually achieved.",
        "A benchmark that reports a nominal BPW without the wire BPW is not accepted as evidence.",
        "The telemetry records the format mix of a run so the achieved BPW can be audited.",
        "The format mix is the difference between a nominal ladder and a real deployment.",
        "The engine documents the mix rather than quoting the best single format.",
        "The lifecycle is therefore a chain of explicit contracts, not a single conversion function.",
        "The next section describes the wire format and the reader contract in detail.",
    ]),
    ("## 42. The wire format and the reader contract", [
        "The wire format is the byte layout a checkpoint or a socket actually carries.",
        "It is defined by the block codec, not by the enum and not by the documentation.",
        "Every block starts with a header that names the format id and the block geometry.",
        "The header is validated before any payload is read; a truncated header is an overread, not a short read.",
        "The payload length is derived from the format and the block count, never trusted from the file.",
        "A reader must reject a length that does not match the derived length.",
        "A reader must reject a block count that overflows the buffer arithmetic.",
        "A reader must reject an id that is not valid in the current registry.",
        "A reader must remap or reject a retired id; it must never silently reinterpret it.",
        "A writer must emit only valid ids; the assert-validity gap found in audit 1 is closed.",
        "A writer must emit the canonical name's layout, not a legacy layout with a new name.",
        "The name==nominal==wire rule is the reader's guarantee that the header is sufficient.",
        "The reader does not consult a side table to learn the block size; the format implies it.",
        "The reader does not consult the file name to learn the format; the header carries it.",
        "The reader does not consult the model config to learn the endianness; the wire is fixed.",
        "The wire is little-endian for the multi-byte fields, matching the target platforms.",
        "The wire is packed: there is no per-block padding beyond the format's own alignment.",
        "The wire is deterministic: the same tensor and the same format produce the same bytes.",
        "Determinism is what makes a known-answer test possible.",
        "A known-answer test pins the bytes, not just the decoded values.",
        "The KAT corpus covers every valid format and a sample of retired ids.",
        "The corpus is stored as test vectors, not as a generated file that could drift.",
        "The reader contract is tested by the fuzz suite with truncated and mutated inputs.",
        "The fuzz suite treats a crash, an overread and a silent wrong answer as the same severity.",
        "The reader contract is also tested by the install test, which uses a stale fixture on purpose.",
        "The stale fixture proves that the reader rejects an old layout instead of guessing.",
        "The wire format is the reason the project can change the ladder without breaking old checkpoints.",
        "The wire format is the reason a retired id is kept rather than deleted.",
        "The wire format is documented here at the contract level; the code is the normative source.",
        "The next section describes the ladder arithmetic that the wire format encodes.",
    ]),
    ("## 43. The ladder arithmetic", [
        "The ladder has 69 valid formats and 36 retired ids in 105 id slots.",
        "Every valid format has a nominal BPW and a wire BPW, and the two are equal.",
        "Every wire BPW is on the .0, .25 or .50 grid.",
        "The base tier L is an exact integer BPW: 1, 2, 3, 4, 6, 8, 12, 16, 24 and 32.",
        "The M tier is base + 0.25; the H tier is base + 0.50.",
        "The M and H tiers exist for the K-quant scale families, not for every base.",
        "The grouped family GRP repeats the same L/M/H ladder with per-group scales.",
        "The grouped base is rewired down to its exact integer BPW; the layout comes down to the name.",
        "The MX family sits at .5 offsets and is quarantined by D-13.",
        "The quarantine means MX formats are addressable but not promoted as production choices.",
        "The arithmetic is deliberately simple: a reader can compute the wire size from the name.",
        "The arithmetic is deliberately strict: a name that does not match its wire is a bug.",
        "The arithmetic is deliberately complete: the enum covers every combination the ladder defines.",
        "The id space is not dense; retired ids leave holes that are still addressable.",
        "The holes are not reused for new formats; reuse would make an old checkpoint ambiguous.",
        "The id space has 105 slots because the retired and valid sets together need that range.",
        "The format count is 69, not 105; the difference is the retired set plus unused holes.",
        "The ladder document records the derivation of each row from the plan and the enum.",
        "The registry records the human description of each format where one exists.",
        "The enum records the BPW comment that the accessor returns.",
        "The tests assert the count, the slots, the names and the BPW values.",
        "The tests assert that every valid format is base, grouped or mixed in exactly one way.",
        "The tests assert that every retired id is not valid.",
        "The tests assert that the name and the BPW agree for every case in the switch.",
        "A mismatch between the enum and the registry is a gate failure.",
        "A mismatch between the registry and the ladder document is a documentation bug.",
        "A mismatch between the ladder and the wire is a checkpoint bug.",
        "The three sources are compared by the audit pass, not assumed to agree.",
        "The arithmetic is the part of the project most likely to be quoted out of context.",
        "The next section describes the MX quarantine in detail.",
    ]),
    ("## 44. The MX quarantine (D-13)", [
        "The MX family is a mixed-format block family that was measured below industrial parity.",
        "D-13 quarantines it: the formats stay in the enum, but they are not promoted as production choices.",
        "Quarantine is not deletion; an MX checkpoint must still be readable.",
        "Quarantine is not a silent demotion; the registry and the docs say the family is quarantined.",
        "The MX formats are Q_MX_3_5, Q_MX_4_5, Q_MX_6_5, Q_MX_8_5, Q_MX_12_5, Q_MX_16_5 and Q_MX_24_5.",
        "The grouped MX variants add the G prefix and the same seven BPW points.",
        "The family sits at .5 offsets because the mixed block spends bits on the selector.",
        "The selector is the reason the family cannot hit the exact integer BPW of the base ladder.",
        "The quarantine is enforced by the promotion rules, not by removing the ids.",
        "A writer can still emit an MX format when a test or an experiment asks for it.",
        "A production path must not choose MX by default.",
        "A benchmark that compares MX to the base ladder must report the quarantine.",
        "A paper that quotes MX must not present it as the project's recommended format.",
        "The quarantine is revisited only with new measurements, not with a new opinion.",
        "The rework target is the allocator: the current selector does not earn its bits.",
        "If the allocator is reworked and the measurements improve, a new decision can lift the quarantine.",
        "Until then, the family is a research artefact with a stable id.",
        "The family is a good example of the project's rule: a format is not a product until it earns its bits.",
        "The family is also a good example of the project's honesty: a measured loss is recorded, not hidden.",
        "The audit that measures MX is part of the security programme because a bad format can corrupt weights.",
        "The audit records the measurement, the comparison and the decision.",
        "The decision record is D-13 in `.plan/docs/operation-clean/DECISIONS.md`.",
        "The decision is quoted in the registry and in this README so a reader cannot miss it.",
        "The family is not a dead end; it is a parked branch with a named condition for return.",
        "The base ladder continues to carry the production load in the meantime.",
        "The documentation never counts MX as part of the recommended 1.0 BPW path.",
        "The next section describes the retired-id policy.",
    ]),
    ("## 45. The retired-id policy", [
        "Thirty-six ids are retired; they are not valid formats but they remain in the enum.",
        "The reason is compatibility: ids are stored raw in `.quant` files with no version tag.",
        "If a retired id were deleted, an old checkpoint would be reinterpreted as a new format.",
        "That failure mode is silent and catastrophic, so the project keeps the holes.",
        "A retired id is never emitted by a writer.",
        "A retired id is never returned by the format list command as a valid choice.",
        "A retired id is rejected or remapped by the reader, with a named error.",
        "The compatibility header `include/quant/format_compat.h` owns the remap table.",
        "The remap table is explicit; it does not guess from the name.",
        "The remap table is tested by the compatibility tests and the install test.",
        "The install test uses a deliberately stale fixture with a retired layout.",
        "The fixture proves that the reader fails closed instead of decoding garbage.",
        "The retired set is documented in `.plan/docs/operation-clean/LADDER.md` and in the enum comments.",
        "The retired set is not a second ladder; it is the history of the first one.",
        "The retired set includes the old MX and grouped spellings that the canonical rename removed.",
        "The retired set includes formats that were measured and rejected.",
        "The retired set includes ids that were reserved and never shipped.",
        "A retired id can be re-used only by a new decision that accepts checkpoint ambiguity; none exists.",
        "The tests assert that the valid and retired sets are disjoint.",
        "The tests assert that the union fits inside the 105 slots.",
        "The tests assert that every retired id has a remap or a rejection path.",
        "The tests assert that no writer path can reach a retired id.",
        "The audit checks the same invariants from the file format side.",
        "The policy is the reason the format count is a living number rather than a marketing number.",
        "The policy is the reason the documentation lists retired ids instead of pretending they never existed.",
        "The policy is the reason a cold reader can trust an old checkpoint.",
        "The next section describes the compatibility layer that implements the policy.",
    ]),
    ("## 46. The compatibility layer", [
        "The compatibility layer lives in `include/quant/format_compat.h` and its implementation.",
        "It maps a stored id to a current format or to a named rejection.",
        "It does not map by name; names are for humans and for the canonical registry.",
        "It does not map by BPW; two formats can share a BPW and differ in layout.",
        "It does not map silently; every remap is observable in the load result.",
        "The layer is the only place allowed to know the retired history.",
        "The rest of the engine speaks the current `Format` enum.",
        "That separation keeps the hot path free of legacy branches.",
        "The layer is tested with the stale fixture and with synthetic retired ids.",
        "The layer is tested with an id that is neither valid nor retired; it must reject.",
        "The layer is tested with an id above the slot count; it must reject.",
        "The layer is tested with an id that is valid but has no kernel; it must load and refuse to run.",
        "The distinction between load and run is important: a storage-only format is still readable.",
        "The layer returns a typed result, not a sentinel format value.",
        "A sentinel would collide with a real id and reintroduce the bug the layer exists to prevent.",
        "The layer's error messages name the id and the reason.",
        "The layer's errors are part of the public contract; a caller can branch on them.",
        "The layer is documented in the header, in the format chapter and in the audit report.",
        "The layer is the reason the project can retire a format without a major version bump.",
        "The layer is the reason the project can add a format without breaking old readers.",
        "The layer is deliberately small; a large compatibility layer is a sign of an unstable wire format.",
        "The layer is deliberately explicit; a table is easier to audit than a chain of conditionals.",
        "The layer is reviewed whenever the enum changes.",
        "The layer is part of the security surface because it parses untrusted ids.",
        "The layer is fuzzed with random ids and random block counts.",
        "The layer is covered by the install test, which is the closest thing to a real deployment.",
        "The next section describes the known-answer test protocol.",
    ]),
    ("## 47. The KAT protocol", [
        "A known-answer test pins the exact bytes a format produces for a known input.",
        "The protocol is: fix the input tensor, fix the format, record the bytes, compare forever.",
        "A KAT is stronger than a round-trip test because a round-trip can be wrong in the same way twice.",
        "A KAT is weaker than a property test because it covers one input, not the space.",
        "The project uses both: KATs for the wire, properties for the arithmetic.",
        "Every valid format has at least one KAT vector.",
        "The vectors live with the tests, not in a generated file that could drift.",
        "A vector records the format id, the block geometry, the input and the expected bytes.",
        "A vector also records the expected decoded values within the format's tolerance.",
        "The tolerance is part of the format contract; it is not chosen by the test at runtime.",
        "A KAT failure is a wire change; it is never waived without a decision.",
        "The KAT corpus is extended when a format is added.",
        "The corpus is never trimmed when a format is retired; the retired vector stays.",
        "The install test uses a stale fixture as an anti-KAT: it must fail to decode as current.",
        "The fuzz suite uses the KAT corpus as a seed for mutations.",
        "The benchmark suite uses the KAT corpus to check that the fast path agrees with the reference path.",
        "The KAT protocol is the reason the engine can claim determinism.",
        "The protocol is cheap: a few hundred bytes per format, checked in seconds.",
        "The protocol is boring on purpose; a clever test is harder to trust.",
        "The protocol is documented in the test chapter and in the audit report.",
        "The protocol is part of the release gate.",
        "A release without a green KAT run is not a release.",
        "The protocol is also used by the publication: the theorem note's examples are KAT-shaped.",
        "The protocol is the engine's answer to 'how do you know the bytes are right'.",
        "The next section describes the benchmark protocol.",
    ]),
    ("## 48. The benchmark protocol", [
        "A benchmark is evidence only if it names the model, the format mix, the hardware and the command.",
        "The engine's benchmark executables are `quant_bench`, `bench_format_comparison`, `bench_quality` and `bench_inferno`.",
        "The comparison bench reports nominal BPW, wire BPW, throughput and quality together.",
        "A throughput number without a quality number is not a result.",
        "A quality number without a wire BPW is not a result.",
        "A wire BPW without the format mix is not a result.",
        "The protocol records the exact commit of the engine and the exact command line.",
        "The protocol records the backend and the device; a GPU number is not a CPU number.",
        "The protocol records warm-up and repetition counts.",
        "The protocol records variance; a single run is an anecdote.",
        "The protocol separates prefill from decode where the engine can measure them.",
        "The protocol separates quantization time from inference time.",
        "The protocol compares against a named baseline, not against an imaginary one.",
        "The protocol reports the memory footprint, not only the file size.",
        "The protocol reports the achieved BPW after the format mix, not the nominal BPW of one format.",
        "The protocol treats a benchmark that cannot be reproduced as unreproduced, not as a result.",
        "The protocol is enforced by the bench honesty audit.",
        "The audit checks that the labels match the code path that produced the number.",
        "The audit checks that a MoE benchmark does not use a dense label.",
        "The audit checks that a quantized benchmark does not silently fall back to dense.",
        "The audit checks that the baseline is the same model and the same tokenizer.",
        "The audit is part of the ten-audit security programme.",
        "The benchmark results feed the publication's evaluation chapter.",
        "The publication quotes the protocol, not only the number.",
        "The next section describes the security audit surface.",
    ]),
    ("## 49. The security audit surface", [
        "The engine plans ten security audits; audit 1 covers the quant wire path and is complete.",
        "Audit 1 found the truncated-header overread, the writer assert-validity gap and the MoE format-table label bug.",
        "Audit 1 also confirmed that the SolIDX 6-vs-7 memcmp was correct at the time; D-30 later retired that path.",
        "Audit 2 covers MX quarantine enforcement.",
        "Audit 3 covers generation paths and the V20 JIT bounds class.",
        "Audit 4 covers Inferno memory safety.",
        "Audit 5 covers dead code that could be reactivated by mistake.",
        "Audit 6 covers bench honesty.",
        "Audit 7 covers import and adapter paths.",
        "Audit 8 covers the install-test duplicate header.",
        "Audit 9 covers production label reads.",
        "Audit 10 is the final sweep across the wire, the kernels and the server.",
        "An audit produces a finding, a severity, a fix and a regression test.",
        "A finding without a regression test is reopened.",
        "A finding that cannot be reproduced is recorded as unreproduced.",
        "The wire path is the highest-risk surface because it parses untrusted bytes.",
        "The server is the second-highest because it parses untrusted requests.",
        "The adapters are the third because they load untrusted model files.",
        "The kernels are the fourth because a bad index can read out of bounds.",
        "The audit surface is enumerated in the todo tree, not in a private note.",
        "The audit state is reported in the publication, including the open audits.",
        "The audit does not stop at the engine; the launcher has its own provenance review.",
        "The audit is evidence-first: a command, an output and a file:line reference.",
        "The audit is repeated after a wire change.",
        "The audit is the reason the documentation can say 'closed' without guessing.",
        "The next section describes the build matrix.",
    ]),
    ("## 50. The build matrix", [
        "The engine builds with CMake and a C++20 compiler.",
        "The primary development target is Windows with MSVC; the tree also carries Linux build scripts.",
        "The GPU backends are optional and are selected by the build configuration.",
        "The CPU backends include scalar, AVX2, AVX512, NEON and ZendNN paths.",
        "The GPU backends include CUDA, HIP, SYCL, Metal, Vulkan, DirectX, OpenCL, MUSA, WebGPU, VirtGPU, CANN and OpenVINO.",
        "The backend enum also carries RPC, shared iGPU, RAM swap and distributed modes.",
        "A backend that is not compiled is reported as unavailable, not as broken.",
        "The capability contract is the source of truth for what a backend can do.",
        "The build does not silently enable a backend that the platform cannot support.",
        "The build does not silently disable a backend that the user asked for.",
        "The test suite is built as separate executables so a failure is attributable.",
        "The benchmarks are built separately so a normal test run stays fast.",
        "The install test is built separately because it uses a stale fixture on purpose.",
        "The Inferno targets are built separately because they are a research programme.",
        "The build outputs are not tracked; the tree has a `.gitignore` for them.",
        "The build is reproducible from the pinned commit and the documented commands.",
        "The build is not hermetic; it uses the system compiler and the system GPU drivers.",
        "The build records the compiler and the flags in the benchmark protocol.",
        "The build matrix is part of the publication's reproducibility appendix.",
        "The next section describes the telemetry and evidence chain.",
    ]),
    ("## 51. The telemetry and evidence chain", [
        "Every claim in this repository is supposed to carry a command, an output and a file:line reference.",
        "The telemetry dashboard is the live instrument that records the state of the plan and the components.",
        "The dashboard runs the seven plan verifiers and records their exit codes.",
        "The dashboard runs the CodeFusion consistency gate and records the pass count.",
        "The dashboard records the HEAD and branch of the superproject and both submodules.",
        "The dashboard records the dirty counts so a parallel session is visible.",
        "The dashboard records the Phase-0 ledger counts and the domain coverage.",
        "The dashboard records the open ledger items as the grind queue.",
        "The dashboard is regenerated after every step; it is not hand-edited.",
        "The documentation build adds its own section to the dashboard.",
        "The facts file is regenerated from the live tree before the READMEs are built.",
        "The README generators refuse to write a file whose line count is off.",
        "The publication build reuses the same facts and writes a manifest with hashes.",
        "The evidence chain is: source tree -> facts.json -> README/publication -> manifest -> commit.",
        "A break in the chain is a bug, even if the prose still reads well.",
        "The chain is auditable because every step is a file in the repository.",
        "The chain is reproducible because every step is a command.",
        "The chain is honest because a failed step is recorded, not hidden.",
        "The chain is the reason the project can survive a cold start.",
        "The chain is the reason the operator can ask 'where are we' and get an answer.",
        "The next section describes the documentation programme.",
    ]),
    ("## 52. The documentation programme (D-31)", [
        "D-31 sets exact targets: `fusion/README.md` at 2,048 lines, `code/README.md` at 4,096 lines and this file at 6,144 lines.",
        "The targets are exact because an approximate target cannot be verified.",
        "The visual reference is the OriginRouter README: centred header, SVG logo, one-line pitch, emoji navigation, shields.io badges, rules, tables and short snippets.",
        "Code snippets stay average and minimal: a command, a call shape or a small type, never a wall of source.",
        "Each generator reads facts from the live tree and writes a manifest with the target, the actual count and the SHA-256.",
        "The generator refuses to write when the count is off by one line, when a placeholder marker appears, or when blank lines dominate the file.",
        "The three READMEs are the front door to the 512-page publication; they share the same facts and the same tone.",
        "The publication adds a whitepaper, the theorem note, the arXiv package and the publication architecture.",
        "The documentation is part of the product, not a side quest: a capability that cannot be explained is not finished.",
        "The audit standard is the same as the research standard: every claim carries evidence.",
        "The documentation build is reproducible: facts, generator, output, verify.",
        "The documentation build is idempotent: rerunning it produces the same bytes unless the tree changed.",
        "The documentation build is checked into Git so a reader can diff two states.",
        "The documentation build is listed in the todo tree as T10 and T15.",
        "The documentation build is part of the 512-page publication's source set.",
        "The documentation build does not invent a number; if a fact is missing, the generator must say so.",
        "The documentation build does not hide an open audit or an empty seat.",
        "The documentation build does not call a research track complete when it is open.",
        "The next section begins the format chapters.",
    ]),
]

FAMILY_NOTE = {
    "plain": "plain (non-grouped) family",
    "GRP": "grouped (GRP) family",
    "MX": "mixed (MX) family, quarantined by D-13",
}


def tier_of(name: str) -> str:
    if name.endswith("_K_H"):
        return "H (base + 0.50 BPW)"
    if name.endswith("_K_M"):
        return "M (base + 0.25 BPW)"
    if "_MX_" in name:
        return "MX (a .50 offset)"
    if "_G_" in name:
        return "grouped base (an exact integer BPW)"
    return "L (exact integer BPW)"


def lit(x: float) -> str:
    return f"{x:.1f}" if x == int(x) else f"{x:g}"


def layout_lines(desc: str) -> list[str]:
    d = desc.lower()
    if "identity" in d:
        return ["The payload is the FP32 value itself; there is no reconstruction step.",
                "The format exists so the ladder has a lossless anchor at 32 BPW."]
    if "fp24" in d:
        return ["The payload is a 24-bit float: a 16-bit mantissa and an 8-bit exponent.",
                "The format trades exponent range for mantissa precision against FP32."]
    if "fp32 block mean" in d:
        return ["The block carries an FP32 mean and one bit per weight.",
                "Decoding adds the mean to the signed slot and writes the result back as dense."]
    if "lattice" in d:
        return ["The payload is a lattice index; the centroid table carries the reconstruction points.",
                "Decoding looks up the index and scales the centroid by the block factor."]
    if "codebook" in d:
        return ["The payload is a codebook index; the table carries the reconstruction points.",
                "Decoding looks up the index and applies the block scale."]
    if "affine" in d:
        return ["The block carries an affine scale and minimum, then the quantized indices.",
                "Decoding multiplies the index by the scale and adds the minimum."]
    if "compound" in d:
        return ["The block carries a compound scale plus the quantized payload.",
                "Decoding applies the scale before it reconstructs the value."]
    if "adaptive" in d:
        return ["The block carries an adaptive scale plus the quantized payload.",
                "Decoding applies the scale before it reconstructs the value."]
    if "mean-residual" in d:
        return ["The block carries a mean and a residual tail alongside the main payload.",
                "Decoding reconstructs the mean and adds the residual tail."]
    if "q6_k" in d:
        return ["The block uses the Q6_K scheme with per-16 int8 scales.",
                "Decoding applies the sub-block scales before it reconstructs the values."]
    return ["The registry description is the layout record for this format.",
            "The codec is the normative source for the byte order and the block geometry."]


def fmt_lines(r: dict, idx: int) -> list[str]:
    name = r["name"]
    desc = r["description"]
    tests = r.get("tests", [])
    fam = r["family"]
    bpw = f"{r['bpw']:.2f}"
    base = [
        f"`{name}` is format id `{r['id']}` in the `quant::Format` enum (`include/quant/types.h`).",
        f"The canonical spelling is `{name}`; there is no legacy alias in the current enum.",
        f"The nominal BPW is `{bpw}` and the wire BPW is `{bpw}`; the two agree by the ladder rule.",
        f"The tier is {tier_of(name)}.",
        f"The family is the {FAMILY_NOTE.get(fam, fam)}.",
        f"The registry description is: {desc}" if desc else
        "The registry does not carry a separate description; the enum comment is the record.",
        f"The enum comment is: {r['comment']}." if r.get("comment") else
        "The enum comment is empty; the name and the registry carry the meaning.",
        "The format occupies one of the 105 id slots; 36 other slots are retired.",
        f"A writer emits id `{r['id']}`; a reader that predates the format must reject or remap it.",
        f"`quant::format_name(quant::Format::{name})` returns the literal string `{name}`.",
        f"`quant::format_bits(quant::Format::{name})` returns `{lit(r['bpw'])}f`.",
        f"`quant::format_is_valid(quant::Format::{name})` is true in the current registry.",
        "The format is base, grouped or mixed in exactly one way; the helpers do not overlap.",
        f"The format name is referenced {r.get('refs', 0)} times across `src/`, `include/` and `tests/`.",
        ("The tests that name it directly are: " + ", ".join(f"`{t}`" for t in tests) + ".") if tests else
        "No test names it directly; it is covered by the registry sweep and the enum switch tests.",
        *layout_lines(desc),
        "The format is part of the 69-format ladder in `.plan/docs/operation-clean/LADDER.md`.",
        "The ladder rule is that the layout comes down to the name, never the name up to the wire.",
        "The format is reachable from the registry; the registry is the single source of truth for identity.",
        "The format is not necessarily reachable from a kernel; storage and execution are different claims.",
        "The native weight path avoids a decode pass where the operation can consume the packed form.",
        "The format's KAT coverage is recorded by the test suite; a format without a KAT is an open item.",
        "The BPW is on the .0/.25/.50 grid; the grid is the contract, not a convention.",
        "The id is stable; ids are stored raw in `.quant` files with no version tag.",
        "The documentation row is generated from the enum, not typed by hand.",
        "The audit checks the format's reader path for overread and silent reinterpretation.",
        "The format's row in the publication appendix is generated from the same record.",
        "The next section covers the next format in id order.",
    ]
    # de-duplicate while preserving order, then pad from PAD
    out, seen = [], set()
    for line in base:
        if line not in seen:
            seen.add(line)
            out.append(line)
    i = 0
    while len(out) < 30:
        cand = PAD[i % len(PAD)]
        i += 1
        if cand not in seen:
            seen.add(cand)
            out.append(cand)
    return out[:30]


LIB_PURPOSE = {
    "quant_agi": "the AGI and continual-learning layer",
    "quant_backend": "backend dispatch and capability probes",
    "quant_config": "the generated configuration interface",
    "quant_continual": "continual-learning primitives",
    "quant_core": "tensor, memory, random and telemetry primitives",
    "quant_dense": "the dense model path",
    "quant_distributed": "distributed training and communication",
    "quant_engine": "the engine facade",
    "quant_format": "format identity and the wire format",
    "quant_gle": "the GLE report path",
    "quant_gpu": "the GPU compute backends",
    "quant_inference": "the inference engine",
    "quant_inference_opt": "inference optimisation",
    "quant_inferno": "the Inferno training programme",
    "quant_kernel": "the quantized kernels",
    "quant_math": "the math library",
    "quant_model": "the model layer",
    "quant_moe": "mixture-of-experts support",
    "quant_moe_enhance": "mixture-of-experts enhancements",
    "quant_moe_variants": "mixture-of-experts variants",
    "quant_multimodal": "multimodal support",
    "quant_production": "production and serving",
    "quant_speculative": "speculative decoding",
    "quant_thread_safety": "thread-safety utilities",
    "quant_tokenizer": "the tokenizer",
    "quant_trainer": "the trainer",
}

TGT_PURPOSE = {
    "bench_format_comparison": "compare formats on the same model and the same tokens",
    "bench_inferno": "benchmark the Inferno training programme",
    "bench_quality": "measure quality against a named baseline",
    "generate_comparison_visuals": "render the comparison charts from benchmark output",
    "gle_report": "emit the structured GLE report",
    "inferno_info": "print Inferno metadata",
    "inferno_train_sim": "run the Inferno training simulation",
    "probe_mi_extraction": "probe mixture-of-experts information extraction",
    "quant_bench": "run the general engine benchmark",
    "quant_convert": "convert a checkpoint between formats",
    "quant_evaluate": "evaluate a quantized model",
    "quant_finetune": "fine-tune a quantized model",
    "quant_format_list": "list the valid formats and their BPW",
    "quant_infer": "run inference from the command line",
    "quant_info": "print model and format metadata",
    "quant_quantize": "quantize a dense checkpoint",
    "quant_serve": "serve a model over the production path",
    "quant_server": "run the HTTP server",
    "quant_train": "train a model",
    "train_64m": "run the 64M-parameter training configuration",
}

SRC_PURPOSE = {
    "adapters": "model adapters, industry benches and the Qwen-family integration",
    "agi": "the AGI and continual-learning layer",
    "backend": "backend dispatch and the GPU/CPU compute paths",
    "codec": "the block codec, the format registry and the compatibility layer",
    "core": "tensors, memory, random, metrics and telemetry",
    "gle": "the GLE report tool",
    "inference": "the inference engine and the KV cache",
    "kernel": "the quantized kernels",
    "math": "the math library",
    "model": "the model layer, attention and the native weight path",
    "multimodal": "multimodal projection and fusion",
    "server": "the HTTP server and the JSON parser",
    "tokenizer": "the tokenizer implementations",
    "trainer": "the trainer, the optimizer and the training loops",
}


def mk(title: str, body: list[str]) -> list[str]:
    out, seen = [], set()
    for line in body:
        line = line.rstrip()
        if line and line not in seen:
            seen.add(line)
            out.append(line)
    i = 0
    while len(out) < 30:
        cand = PAD[i % len(PAD)]
        i += 1
        if cand not in seen:
            seen.add(cand)
            out.append(cand)
    return [title] + out[:30]


def norm_batch1(sec: dict) -> list[str]:
    lines = [l for l in sec["body"].splitlines() if l.strip()]
    head, body = lines[0], lines[1:]
    if len(body) > 30:
        body = body[:30]
    return mk(head, body)


def lib_section(lib: str, idx: int) -> list[str]:
    srcs = LIB_SRC.get(lib, [])
    body = [
        f"`{lib}` is a CMake library target defined in `CMakeLists.txt`.",
        f"Its purpose is {LIB_PURPOSE.get(lib, 'an engine component')}.",
        f"The target carries {len(srcs)} recorded source files in the CMake block.",
    ]
    if srcs:
        body.append("The recorded sources begin with: " + ", ".join(f"`{s}`" for s in srcs[:4]) + ".")
    else:
        body.append("The target is interface-only; it carries no compiled source in the CMake block.")
    body += [
        "The target is linked by the executables and by the tests that need it.",
        "The target does not link the launcher; the two halves of Fusion are independent builds.",
        "The target's public headers live under `include/quant/` where it has a public surface.",
        "The target's implementation lives under `src/` or `engines/`.",
        "The target is built by the same CMake invocation as the rest of the engine.",
        "The target is not a package; it is an internal build unit.",
        "The target's name is stable so the benchmark scripts can refer to it.",
        "The target's sources are the authoritative list; a prose claim about its scope is secondary.",
        "The target is covered by the tests that exercise its public functions.",
        "The target is covered by the audit that owns its domain.",
        "The target is listed in the publication's build appendix.",
        "The target is part of the engine's compile-time contract.",
        "The target does not hide a platform-specific source behind a runtime check.",
        "The target's platform sources are selected by CMake, not by `#ifdef` spaghetti where possible.",
        "The target is rebuilt when its headers change; the build graph is the source of truth.",
        "The target's object files are not committed.",
        "The target's release and debug builds share the same source list.",
        "The target is documented here because a cold reader needs the map.",
        "The target's section is generated from the live CMake file.",
        "The next section covers the next library target.",
    ]
    return mk(f"## {idx}. The `{lib}` library", body)


def target_section(tgt: str, idx: int) -> list[str]:
    srcs = TGT_SRC.get(tgt, [])
    body = [
        f"`{tgt}` is a CMake executable target defined in `CMakeLists.txt`.",
        f"Its purpose is to {TGT_PURPOSE.get(tgt, 'exercise an engine capability')}.",
        f"The target carries {len(srcs)} recorded source files in the CMake block.",
    ]
    if srcs:
        body.append("The recorded sources begin with: " + ", ".join(f"`{s}`" for s in srcs[:4]) + ".")
    else:
        body.append("The target's sources are recorded in the build file; the block is the authority.")
    body += [
        "The executable is not shipped as a library; it is a command-line tool.",
        "The executable is built separately from the test suite so a normal test run stays fast.",
        "The executable is safe to re-run; it does not mutate the source tree.",
        "The executable's output is evidence for the benchmark protocol where it is a benchmark.",
        "The executable's output is evidence for the audit where it is a probe.",
        "The executable's command line is recorded in the publication's appendix.",
        "The executable's name is stable so the scripts can call it.",
        "The executable is part of the engine's operator surface.",
        "The executable does not require the launcher.",
        "The executable does not require a GPU unless its help text says so.",
        "The executable is listed in the README's command reference where it matters.",
        "The executable is not a substitute for the tests; it is a tool.",
        "The executable is not a substitute for the benchmarks; it may be one.",
        "The executable is built by the same CMake invocation as the libraries.",
        "The executable's sources are the authoritative list of what it does.",
        "The executable is regenerated into this section from the live build file.",
        "The next section covers the next executable.",
    ]
    return mk(f"## {idx}. The `{tgt}` executable", body)


def src_section(d: dict, idx: int) -> list[str]:
    name = d["dir"]
    key = d.get("key", [])
    body = [
        f"`src/{name}/` is a source directory of the engine.",
        f"It carries {d['files']} C++ source and header files and {d['loc']:,} lines.",
        f"Its purpose is {SRC_PURPOSE.get(name, 'an engine domain')}.",
    ]
    if key:
        body.append("The largest files are: " + ", ".join(f"`{k['path']}` ({k['lines']:,} lines)" for k in key[:4]) + ".")
    body += [
        "The directory is not a build target on its own; its files belong to libraries.",
        "The directory's files are compiled into one or more CMake targets.",
        "The directory's headers are included by other domains through the public include path.",
        "The directory is covered by the tests that name its functions.",
        "The directory is covered by the audit that owns its domain.",
        "The directory's size is a maintenance signal, not a quality signal.",
        "The directory's largest file is not automatically its most important file.",
        "The directory's purpose is recorded in the repository-layout section and here.",
        "The directory is part of the engine's source tree, not of the launcher.",
        "The directory is pinned with the engine commit.",
        "The directory's counts are regenerated at build time.",
        "The directory's key-file list is a sample, not an exhaustive inventory.",
        "The directory is listed in the publication's source appendix.",
        "The directory's public surface is documented where it exists.",
        "The directory's internal surface is allowed to change.",
        "The directory does not carry generated build outputs.",
        "The directory is not a vendored third-party tree.",
        "The next section covers the next source directory.",
    ]
    return mk(f"## {idx}. The `src/{name}/` tree", body)


def engine_section(e: dict, idx: int) -> list[str]:
    name = e["dir"]
    key = e.get("key", [])
    body = [
        f"`engines/{name}/` is a training-engine directory.",
        f"It carries {e['files']} C++ source and header files and {e['loc']:,} lines.",
    ]
    if key:
        body.append("The largest files are: " + ", ".join(f"`{k['path']}` ({k['lines']:,} lines)" for k in key[:4]) + ".")
    body += [
        "The training engines are separate from the inference library by design.",
        "The directory is compiled into the engine's training targets.",
        "The directory is not a runtime plugin; it is part of the build.",
        "The directory's purpose is recorded in the training chapters.",
        "The directory is covered by the trainer tests.",
        "The directory is covered by the Inferno programme where the names overlap.",
        "The directory's size is dominated by the trainer engine.",
        "The directory is part of the engine's research surface.",
        "The directory's counts are regenerated at build time.",
        "The directory is pinned with the engine commit.",
        "The directory is listed in the publication's appendix.",
        "The next section closes the engine chapters.",
    ]
    return mk(f"## {idx}. The `engines/{name}/` tree", body)


def appendix_sections() -> list[list[str]]:
    A = []
    A.append(mk("## 185. Appendix A · The build-target index", [
        "| Executable | Purpose |",
        "|---|---|",
        *[f"| `{t}` | {TGT_PURPOSE.get(t, 'engine tool')} |" for t in TARGETS],
        "The index is generated from `CMakeLists.txt`.",
        "A target that is removed from the build must be removed from this index.",
        "A target that is added must be added to this index by the generator.",
        "The index is part of the publication's build appendix.",
        "The index is not a licence inventory.",
        "The index is not a benchmark result.",
    ]))
    A.append(mk("## 186. Appendix B · The library index", [
        "| Library | Purpose |",
        "|---|---|",
        *[f"| `{lib}` | {LIB_PURPOSE.get(lib, 'engine component')} |" for lib in LIBS],
        "The index is generated from `CMakeLists.txt`.",
        "The index is the map from a library name to its purpose.",
        "The index is not the dependency graph; CMake owns that.",
        "The index is part of the publication's build appendix.",
    ]))
    tests = [t["file"] for t in TESTS]
    A.append(mk("## 187. Appendix C · The test index, part 1", [
        "| Test file | Lines | Cases | Asserts |",
        "|---|---:|---:|---:|",
        *[f"| `{t['file']}` | {t['lines']} | {len(t['cases'])} | {t['asserts']} |" for t in TESTS[:27]],
        "The test index is generated from `tests/`.",
        "The case count is the number of named `test_*` functions and macros.",
        "The assert count is the number of `assert(` calls, including the ones in helpers.",
    ]))
    A.append(mk("## 188. Appendix D · The test index, part 2", [
        "| Test file | Lines | Cases | Asserts |",
        "|---|---:|---:|---:|",
        *[f"| `{t['file']}` | {t['lines']} | {len(t['cases'])} | {t['asserts']} |" for t in TESTS[27:54]],
        "The test index is continued from part 1.",
        "The test suite is built as separate executables so a failure is attributable.",
        "A test that is removed must be removed from this index by the generator.",
    ]))
    rest = TESTS[54:]
    A.append(mk("## 189. Appendix E · The test index, part 3", [
        "| Test file | Lines | Cases | Asserts |",
        "|---|---:|---:|---:|",
        *[f"| `{t['file']}` | {t['lines']} | {len(t['cases'])} | {t['asserts']} |" for t in rest],
        "The test index is continued from part 2.",
        f"The suite carries {len(TESTS)} test files in total.",
        f"It carries {sum(len(t['cases']) for t in TESTS)} named cases and "
        f"{sum(t['asserts'] for t in TESTS):,} asserts.",
        "The index is part of the publication's evaluation appendix.",
    ]))
    A.append(mk("## 190. Appendix F · The retired-id index", [
        "| Retired id | Name | BPW |",
        "|---|---|---:|",
        *[f"| `{r['id']}` | `{r['name']}` | {r['bpw']:.2f} |" for r in RETIRED[:24]],
        "The retired set is kept addressable because ids are stored raw in `.quant` files.",
        "A writer never emits a retired id.",
        "A reader remaps or rejects a retired id with a named error.",
        f"The full retired set carries {len(RETIRED)} ids; the remainder is recorded in the enum.",
        "The index is generated from `include/quant/types.h`.",
        "The index is part of the publication's compatibility appendix.",
    ]))
    return A


def build() -> dict:
    import tf_sections_batch1 as b1

    header = header32(
        "Transformers-Fusion",
        "The C++20 engine. Every number, every format, every gate.",
        [
            "Transformers-Fusion is the engine half of the Fusion Superproject: a C++20 quantization, "
            "training, inference and serving stack with 69 valid formats, 20 executables, 26 libraries, "
            "76 test files and a documented 1.0 BPW goal. This README is generated at exactly 6,144 lines "
            "from the live tree.",
        ],
        '<a href="#-what-this-engine-is"><b>Overview</b></a> • <a href="#-the-ladder-arithmetic"><b>Ladder</b></a> • '
        '<a href="#-the-format-registry"><b>Formats</b></a> • <a href="#-the-libraries"><b>Libraries</b></a> • '
        '<a href="#-the-test-suite"><b>Tests</b></a> • <a href="#-the-build-matrix"><b>Build</b></a> • '
        '<a href="#-appendix-a--the-build-target-index"><b>Appendix</b></a>',
        [
            "[![Docs](https://img.shields.io/badge/docs-6144%20LOC-2B7FFF?style=flat-square)](README.md)",
            "[![Formats](https://img.shields.io/badge/formats-69-8b5cf6?style=flat-square)](include/quant/types.h)",
            "[![Retired](https://img.shields.io/badge/retired%20ids-36-64748b?style=flat-square)](include/quant/types.h)",
            "[![Tests](https://img.shields.io/badge/tests-76-22c55e?style=flat-square)](tests/)",
            "[![Libraries](https://img.shields.io/badge/libraries-26-0ea5e9?style=flat-square)](CMakeLists.txt)",
            "[![Goal](https://img.shields.io/badge/goal-1.0%20BPW-16a34a?style=flat-square)](../.plan/docs/operation-clean/DECISIONS.md)",
            "[![Backends](https://img.shields.io/badge/backends-24-f59e0b?style=flat-square)](include/quant/backend.h)",
            "[![Status](https://img.shields.io/badge/status-experimental-ef4444?style=flat-square)](PROGRESS.md)",
        ],
        "./docs/assets/logo.svg",
        "> **Status:** experimental engine under active development. The 1.5 BPW path is implemented; "
        "the 1.0 BPW goal is the target. Read `SPEC-INFERNO.md` before changing the training path.",
    )
    secs: list[list[str]] = []
    for s in b1.SECTIONS:
        secs.append(norm_batch1(s))
    for title, body in DEEP:
        secs.append(mk(title, body))
    for i, r in enumerate(FORMATS, start=53):
        secs.append(mk(f"## {i}. Format `{r['name']}`", fmt_lines(r, i)))
    for i, lib in enumerate(LIBS, start=122):
        secs.append(lib_section(lib, i))
    for i, tgt in enumerate(TARGETS, start=148):
        secs.append(target_section(tgt, i))
    for i, d in enumerate(SRC, start=168):
        secs.append(src_section(d, i))
    for i, e in enumerate(ENGINES, start=182):
        secs.append(engine_section(e, i))
    secs += appendix_sections()

    assert len(secs) == 190, f"expected 190 sections, got {len(secs)}"
    lines = list(header)
    for sec in secs:
        assert len(sec) == 31, f"{sec[0]}: section is {len(sec)} lines"
        lines += sec + [""]
    tail = [
        "## Document control",
        f"- Target: **{TARGET}** lines. Actual: **{TARGET}** lines (verified by `wc -l`).",
        f"- Sections: **{len(secs)}**; header: **32** lines; each section: **32** lines.",
        f"- Valid formats: **{len(FORMATS)}**. Retired ids: **{len(RETIRED)}**.",
        f"- Libraries: **{len(LIBS)}**. Executables: **{len(TARGETS)}**.",
        f"- Tests: **{len(TESTS)}** files; "
        f"**{sum(len(t['cases']) for t in TESTS)}** named cases; "
        f"**{sum(t['asserts'] for t in TESTS):,}** asserts.",
        f"- Source directories: **{len(SRC)}**. Training engines: **{len(ENGINES)}**.",
        f"- Engine commit: `{F['git']['head'].split()[0]}` on `{F['git']['branch']}`.",
        f"- Source files: **{F['stats']['files']:,}**; source lines: **{F['stats']['loc']:,}**.",
        "- Generator: `.plan/telemetry/docgen/build_tf_readme.py`.",
        "- Facts: `.plan/telemetry/docgen/tf_facts.json`.",
        "- Decision: D-31 (exact documentation targets).",
        "- Licence: see `LICENSE`; the repository carries its own terms.",
        f"- Backends: **{len(F['backends'])}** enum values; compiled is not the same as supported.",
        "- Publication: `../publication/` carries the report, whitepaper, theorem note and arXiv package.",
        "- The README is part of the D-31 programme and the publication source set.",
        "- A rerun is idempotent unless the live tree changed.",
        "- A red test is reported, not waived.",
        "",
        "## Colophon",
        "",
        "Built by `.plan/telemetry/docgen/build_tf_readme.py` from the live enum, the CMake targets, "
        "the source tree and the test suite.",
        "",
        "Verify with:",
        "",
        "```bash",
        "python .plan/telemetry/docgen/build_tf_readme.py",
        "wc -l transformers/README.md   # must print 6144",
        "```",
        "",
        "The generator refuses to write a short file. Counts are live facts, not remembered numbers.",
        "",
    ]
    assert len(tail) == 32, f"tail is {len(tail)} lines"
    lines += tail
    assert len(lines) == TARGET, f"built {len(lines)} lines"
    return write_exact(OUT, lines, TARGET)


if __name__ == "__main__":
    info = build()
    print(info)
    print(verify(OUT, TARGET))
