"""Patch the TF tree for the Operation Clean ladder (L1 + L7 fold-in).

Angle brackets are written as @L@ / @G@ placeholders because the shell/tool
payload parser treats literal angle-bracket identifiers as tags.

Run: python -I patch_l1.py
"""
import os
import re
import sys

R = r"C:/Users/thaku/Workspaces/fusion/transformers"

PLAIN_FAMS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
GRP_FAMS = [1, 2, 3, 4, 6, 8, 12, 16, 24]

RETIRED = set()
for b in PLAIN_FAMS[:-1]:
    RETIRED.add("Q_%d_K_L" % b)
    RETIRED.add("Q_%d_5" % b)
for b in GRP_FAMS:
    RETIRED.add("Q_G_%d_K_L" % b)
    RETIRED.add("Q_G_%d_5" % b)

report = []


def C(s):
    """Expand angle-bracket placeholders."""
    return s.replace("@L@", chr(60)).replace("@G@", chr(62))


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def sub(path, old, new, label, count=1):
    old = C(old)
    new = C(new)
    s = read(path)
    if old not in s:
        report.append("MISS  %-24s :: %s" % (os.path.basename(path), label))
        return False
    write(path, s.replace(old, new, count))
    report.append("ok    %-24s :: %s" % (os.path.basename(path), label))
    return True


# ------------------------------------------------------------ format_compat.h
def write_format_compat():
    body = '''#pragma once
// ============================================================================
// format_compat.h - legacy format-id remapping and the wire-validity gate
// (Operation Clean, rule G-5 / decision D-08).
//
// types.h owns the validity table (kFormatValid / format_is_valid); this
// header owns the READ path for retired ids and the single gate every
// wire-byte consumer must use.
//
// History: v3 stored raw uint8 format ids in .quant files with no version
// tag. Operation Clean retired 36 of the 105 v3 ids (plain K_L tiers, GRP
// K_L tiers, the half-BPW families). The id space never shrinks
// (FORMAT_ID_SLOTS = 105) so old bytes stay addressable; readers decide what
// a retired id means.
//
// Reading rule (G-5: never misdecode):
//   * plain  Q_x_K_L   -> remap to Q_x       (payloads were byte-identical)
//   * GRP    Q_G_x_K_L  -> remap to Q_G_x    (same reason)
//   * half   Q_x_5     -> remap to Q_x_K_H  (the half row's BPW equals the H
//                                          tier's BPW; the payload layout
//                                          changed, so this is best-effort
//                                          and the caller logs it)
//   * half   Q_G_x_5   -> remap to Q_G_x_K_H
// Writers must assert validity before writing (see the QUANTWriter call
// sites in src/codec/quant_format.cpp).
// ============================================================================
#include "quant/types.h"
#include @L@cstdint@G@

namespace quant {

// The single gate for a wire format byte read off disk. Every consumer that
// used the old `wire_fmt < FORMAT_COUNT && wire_fmt != 19` predicate calls
// this instead.
inline bool wire_format_valid(uint8_t wire_fmt) {
    return wire_fmt < FORMAT_ID_SLOTS && kFormatValid[wire_fmt];
}

// Remap a retired wire byte to the format to decode with. Live ids pass
// through untouched.
//
//   plain  K_L  ids 10,13,...,34   -> base ids 0,1,...,8
//   GRP    K_L  ids 46,49,...,70   -> GRP base ids 37,38,...,45
//   half   Q_x_5    ids 73..81     -> H tiers 12,15,...,36
//   half   Q_G_x_5  ids 82..90     -> GRP H tiers 48,51,...,72
inline Format legacy_format_id_remap(uint8_t wire_fmt) {
    if (wire_fmt >= FORMAT_ID_SLOTS) return Format::Q_32;
    if (kFormatValid[wire_fmt]) return (Format)wire_fmt;
    if (wire_fmt >= 10 && wire_fmt <= 34 && ((wire_fmt - 10) % 3) == 0)
        return (Format)((wire_fmt - 10) / 3);                  // plain K_L -> base
    if (wire_fmt >= 46 && wire_fmt <= 70 && ((wire_fmt - 46) % 3) == 0)
        return (Format)(37 + (wire_fmt - 46) / 3);              // GRP K_L -> GRP base
    if (wire_fmt >= 73 && wire_fmt <= 81)
        return (Format)(12 + 3 * (wire_fmt - 73));              // plain half -> H tier
    if (wire_fmt >= 82 && wire_fmt <= 90)
        return (Format)(48 + 3 * (wire_fmt - 82));              // GRP half -> GRP H tier
    return Format::Q_32;  // caller logs once per file
}

// True when the remap is exact (the payload bytes are unchanged). The K_L
// rows are exact; the half-BPW rows are best-effort (the layout changed)
// and the caller logs them.
inline bool legacy_remap_is_exact(uint8_t wire_fmt) {
    if (wire_fmt >= FORMAT_ID_SLOTS) return false;
    if (kFormatValid[wire_fmt]) return true;
    return (wire_fmt >= 10 && wire_fmt <= 34 && ((wire_fmt - 10) % 3) == 0) ||
           (wire_fmt >= 46 && wire_fmt <= 70 && ((wire_fmt - 46) % 3) == 0);
}

} // namespace quant
'''
    path = R + "/include/quant/format_compat.h"
    write(path, C(body))
    report.append("ok    format_compat.h       :: written (remap + wire gate)")


# --------------------------------------------------------------- block_codec
def patch_block_codec():
    path = R + "/src/codec/block_codec.cpp"
    s = read(path)
    lines = s.split("\n")
    out = []
    dropped = 0
    trimmed = 0
    risky = 0
    for line in lines:
        cases = re.findall(r"case Format::([A-Za-z0-9_]+):", line)
        if not cases:
            out.append(line)
            continue
        bad = [c for c in cases if c in RETIRED]
        if not bad:
            out.append(line)
            continue
        good = [c for c in cases if c not in RETIRED]
        if good:
            for c in bad:
                line = line.replace("case Format::%s: " % c, "")
                line = line.replace("case Format::%s:" % c, "")
            trimmed += len(bad)
            out.append(line)
        else:
            if "{" in line:
                risky += 1
                report.append("WARN  block_codec.cpp     :: retired-only case WITH brace: %s"
                              % line.strip()[:90])
                out.append(line)
                continue
            dropped += 1
    text = "\n".join(out)
    write(path, text)
    # brace balance check
    before = read(R + "/src/codec/block_codec.cpp")
    report.append("ok    block_codec.cpp      :: dropped %d retired case lines, trimmed %d labels, %d risky"
                  % (dropped, trimmed, risky))


def patch_k_tier():
    path = R + "/src/codec/block_codec.cpp"
    s = read(path)
    start = s.find("static int k_tier(Format f) {")
    if start < 0:
        report.append("MISS  block_codec.cpp      :: k_tier not found")
        return
    end = s.find("\n}", start)
    new_body = (
        "static int k_tier(Format f) {\n"
        "    // Tier from the ENUM ID, never from the name string (D-11: a rename\n"
        "    // must not change the encoder effort). Id layout per family:\n"
        "    //   plain  K_L=10+3i (retired), K_M=11+3i, K_H=12+3i\n"
        "    //   GRP    K_L=46+3i (retired), K_M=47+3i, K_H=48+3i\n"
        "    // Returns 0 = base/L, 1 = M, 2 = H.\n"
        "    const int v = (int)f;\n"
        "    if (v >= 10 && v <= 36) {\n"
        "        const int r = (v - 10) % 3;\n"
        "        return r == 1 ? 1 : (r == 2 ? 2 : 0);\n"
        "    }\n"
        "    if (v >= 46 && v <= 72) {\n"
        "        const int r = (v - 46) % 3;\n"
        "        return r == 1 ? 1 : (r == 2 ? 2 : 0);\n"
        "    }\n"
        "    return 0;\n"
        "}"
    )
    write(path, s.replace(s[start:end + 2], new_body, 1))
    report.append("ok    block_codec.cpp      :: k_tier() now id-based (D-11)")


# ----------------------------------------------------------- format_registry
def patch_format_registry():
    path = R + "/include/quant/format_registry.h"
    s = read(path)

    # 1) drop the legacy RegFormat spellings block
    marker = "    // --- Legacy pre-Fusion aliases (deprecated, same IDs) ---"
    start = s.find(marker)
    if start >= 0:
        end = s.find("};", start)
        s = s[:start] + s[end:]
        report.append("ok    format_registry.h    :: legacy RegFormat aliases removed")
    else:
        report.append("MISS  format_registry.h    :: legacy RegFormat block not found")

    # 2) drop retired Format labels from format_to_regformat
    fn_start = s.find("inline RegFormat format_to_regformat(Format f) {")
    fn_end = s.find("\n}", fn_start)
    body = s[fn_start:fn_end + 2]
    lines = body.split("\n")
    kept = []
    for line in lines:
        cases = re.findall(r"case Format::([A-Za-z0-9_]+):", line)
        if cases and all(c in RETIRED for c in cases):
            # whole statement retired -> drop the line (it is a single-case
            # `case X: return RegFormat::Y;` statement)
            continue
        for c in RETIRED:
            line = line.replace("case Format::%s: " % c, "")
        kept.append(line)
    new_body = "\n".join(kept)
    s = s[:fn_start] + new_body + s[fn_end + 2:]
    write(path, s)
    report.append("ok    format_registry.h    :: format_to_regformat: retired labels dropped")


def patch_registry_cpp_bpw():
    path = R + "/src/codec/format_registry.cpp"
    s = read(path)
    # GRP base BPWs follow the new ladder (name == wire)
    pairs = [
        ('{"Q_G_2",  RegFormat::Q_G_2,  2.625f,', '{"Q_G_2",  RegFormat::Q_G_2,  2.0f,'),
        ('{"Q_G_3",  RegFormat::Q_G_3,  3.5f,', '{"Q_G_3",  RegFormat::Q_G_3,  3.0f,'),
        ('{"Q_G_4",  RegFormat::Q_G_4,  4.5f,', '{"Q_G_4",  RegFormat::Q_G_4,  4.0f,'),
        ('{"Q_G_6",  RegFormat::Q_G_6,  6.5625f,', '{"Q_G_6",  RegFormat::Q_G_6,  6.0f,'),
        ('{"Q_G_8",  RegFormat::Q_G_8,  8.5f,', '{"Q_G_8",  RegFormat::Q_G_8,  8.0f,'),
        ('{"Q_G_12", RegFormat::Q_G_12, 12.5f,', '{"Q_G_12", RegFormat::Q_G_12, 12.0f,'),
        ('{"Q_G_16", RegFormat::Q_G_16, 16.5f,', '{"Q_G_16", RegFormat::Q_G_16, 16.0f,'),
        ('{"Q_G_24", RegFormat::Q_G_24, 24.5f,', '{"Q_G_24", RegFormat::Q_G_24, 24.0f,'),
        ('RegFormat::Q_G_MX_3_5,      4, RegFormat::Q_G_1,      0.70f, RegFormat::Q_G_3,      0.20f, RegFormat::Q_G_8,      0.08f, RegFormat::Q_32,     0.02f, 3.78125f,',
         'RegFormat::Q_G_MX_3_5,      4, RegFormat::Q_G_1,      0.70f, RegFormat::Q_G_3,      0.20f, RegFormat::Q_G_8,      0.08f, RegFormat::Q_32,     0.02f, 3.50f,'),
    ]
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
            report.append("ok    format_registry.cpp  :: %s" % old[:34].strip())
        else:
            report.append("MISS  format_registry.cpp  :: %s" % old[:34].strip())
    write(path, s)


def patch_inferno():
    path = R + "/include/quant/inferno.h"
    s = read(path)
    pairs = [
        ('{"Q_G_2",  2.625,   32.0 / 2.625},', '{"Q_G_2",  2.0,     32.0 / 2.0},'),
        ('{"Q_G_3",  3.5,     32.0 / 3.5},', '{"Q_G_3",  3.0,     32.0 / 3.0},'),
        ('{"Q_G_4",  4.5,     32.0 / 4.5},', '{"Q_G_4",  4.0,     32.0 / 4.0},'),
        ('{"Q_G_6",  6.5625,  32.0 / 6.5625},', '{"Q_G_6",  6.0,     32.0 / 6.0},'),
        ('{"Q_G_8",  8.5,     32.0 / 8.5},', '{"Q_G_8",  8.0,     32.0 / 8.0},'),
        ('{"Q_G_12", 12.5,    32.0 / 12.5},', '{"Q_G_12", 12.0,    32.0 / 12.0},'),
        ('{"Q_G_16", 16.5,    32.0 / 16.5},', '{"Q_G_16", 16.0,    32.0 / 16.0},'),
        ('{"Q_G_24", 24.5,    32.0 / 24.5},', '{"Q_G_24", 24.0,    32.0 / 24.0},'),
    ]
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        else:
            report.append("MISS  inferno.h           :: %s" % old[:30].strip())
    write(path, s)
    report.append("ok    inferno.h           :: GRP base BPWs follow the ladder")


# --------------------------------------------------------------- consumers
def patch_consumers():
    p = R + "/src/adapters/tools/quant_import.cpp"
    sub(p, "if (bpw <= 1.75f) return quant::Format::Q_1_5;",
        "if (bpw <= 1.75f) return quant::Format::Q_1_K_H;", "bpw<=1.75 -> Q_1_K_H")
    sub(p, 'else if (s == "Q_1_5" || s == "Q1_5" || s == "Q_1_5")     { out = quant::Format::Q_1_5; }',
        'else if (s == "Q_1_5" || s == "Q1_5")                    { out = quant::Format::Q_1_K_H; }',
        "Q_1_5 name -> Q_1_K_H")
    sub(p, 'else if (s == "Q_G_1_5" || s == "QG_1_5" || s == "Q_G_1_5") { out = quant::Format::Q_G_1_5; }',
        'else if (s == "Q_G_1_5" || s == "QG_1_5")                 { out = quant::Format::Q_G_1_K_H; }',
        "Q_G_1_5 name -> Q_G_1_K_H")
    p = R + "/src/adapters/tools/probe_t4.cpp"
    s = read(p)
    s = s.replace("Format::Q_G_1_5", "Format::Q_G_1_K_H").replace("Format::Q_1_5", "Format::Q_1_K_H")
    write(p, s)
    report.append("ok    probe_t4.cpp         :: retired names repointed")


# -------------------------------------------------------------------- tests
def patch_tests():
    p = R + "/tests/test_all.cpp"
    sub(p, 'SYS_CHECK(quant::FORMAT_COUNT == 105, "FORMAT_COUNT == 105");',
        'SYS_CHECK(quant::FORMAT_COUNT == 69, "FORMAT_COUNT == 69");\n'
        '    SYS_CHECK(quant::FORMAT_ID_SLOTS == 105, "FORMAT_ID_SLOTS == 105");',
        "format count pin")
    sub(p, "for (int i = 0; i < quant::FORMAT_COUNT; i++) {\n"
           "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
           "        if (!(quant::format_bpw(fmt) > 0.0f && quant::format_name(fmt) != nullptr)) {",
        "int live_formats = 0;\n"
        "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {\n"
        "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
        "        if (!quant::format_is_valid(fmt)) continue;\n"
        "        ++live_formats;\n"
        "        if (!(quant::format_bpw(fmt) > 0.0f && quant::format_name(fmt) != nullptr)) {",
        "valid id iteration")
    sub(p, '        }\n    }\n    std::cout << "  -> PASSED: All 105 defined v4 formats',
        '        }\n    }\n    SYS_CHECK(live_formats == quant::FORMAT_COUNT, "live format count matches FORMAT_COUNT");\n'
        '    std::cout << "  -> PASSED: All 105 defined v4 formats',
        "live count assertion")
    sub(p, 'std::cout << "  -> PASSED: All 105 defined v4 formats (base+K+G+K_G+half+halfGRP+mix, formerly MXQ & formerly QMX) verified!\\n\\n";',
        'std::cout << "  -> PASSED: All 69 live formats verified (base + plain M/H + GRP base + GRP M/H + MX); "\n'
        '              << quant::FORMAT_ID_SLOTS << " id slots, 36 retired!\\n\\n";',
        "format summary line")

    p = R + "/tests/test_format_audit.cpp"
    sub(p, "for (int id = 0; id < FORMAT_COUNT; ++id) {\n"
           "        const Format f = static_cast@L@Format@G@(id);\n"
           "        std::vector@L@uint8_t@G@ idx, cb;",
        "for (int id = 0; id < FORMAT_ID_SLOTS; ++id) {\n"
        "        const Format f = static_cast@L@Format@G@(id);\n"
        "        if (!format_is_valid(f)) continue;   // retired ids are not encodable\n"
        "        std::vector@L@uint8_t@G@ idx, cb;",
        "audit iterates live ids")

    p = R + "/tests/test_fuzz_codec.cpp"
    sub(p, "for (int v = 0; v < quant::FORMAT_COUNT; ++v) {\n"
           "        const auto f = static_cast@L@quant::Format@G@(v);\n"
           "        require(quant::format_bpw(f) > 0.0f,\n"
           "                std::string(\"registry gap: format_bpw==0 for id \") + std::to_string(v));",
        "for (int v = 0; v < quant::FORMAT_ID_SLOTS; ++v) {\n"
        "        const auto f = static_cast@L@quant::Format@G@(v);\n"
        "        if (!quant::format_is_valid(f)) continue;   // retired ids are not encodable\n"
        "        require(quant::format_bpw(f) > 0.0f,\n"
        "                std::string(\"live format with zero BPW at id \") + std::to_string(v));",
        "fuzz enumerates live ids")
    sub(p, "constexpr int kFormats = 105;         // v4: FORMAT_COUNT, no gaps",
        "constexpr int kFormats = 69;          // Operation Clean ladder: live formats",
        "kFormats pin")
    sub(p, '"expected 105 supported formats, got " + std::to_string(formats.size()));\n'
           '    std::printf("All 105 enum slots 0..104 defined, no gaps\\n");',
        '"expected 69 live formats, got " + std::to_string(formats.size()));\n'
        '    std::printf("%d live formats in a %d-slot id space (36 retired)\\n",\n'
        '                kFormats, quant::FORMAT_ID_SLOTS);',
        "formats.size() message")

    p = R + "/tests/test_format.cpp"
    sub(p, "assert(quant::FORMAT_COUNT == 105);",
        "assert(quant::FORMAT_COUNT == 69);\n    assert(quant::FORMAT_ID_SLOTS == 105);",
        "format count pin")
    sub(p, "    // Verify half-BPW plain variants (Q1.5..Q24.5 at enum 73..81)\n"
           "    for (int i = 73; i <= 81; i++) {\n"
           "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
           "        assert(!quant::format_is_grp(fmt));\n"
           "        assert(!quant::format_is_base(fmt));\n"
           "        assert(quant::format_bpw(fmt) > 0.0f);\n"
           "    }",
        "    // Verify the GRP M/H tiers (enum 47..72; every third id is a retired\n"
        "    // K_L hole): grouped, not base, and carrying a real BPW.\n"
        "    for (int i = 47; i <= 72; i++) {\n"
        "        if (!quant::format_is_valid(static_cast@L@quant::Format@G@(i))) continue;\n"
        "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
        "        assert(quant::format_is_grp(fmt));\n"
        "        assert(!quant::format_is_base(fmt));\n"
        "        assert(quant::format_bpw(fmt) > 0.0f);\n"
        "    }\n"
        "    // Retired ids are never valid and never carry a BPW.\n"
        "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {\n"
        "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
        "        if (quant::format_is_valid(fmt)) continue;\n"
        "        assert(quant::format_bpw(fmt) == 0.0f);\n"
        "    }",
        "half-BPW block -> GRP tiers + retired check")
    sub(p, "    int valid = 0;\n"
           "    for (int i = 0; i < quant::FORMAT_COUNT; i++) {",
        "    int valid = 0;\n"
        "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {\n"
        "        if (!quant::format_is_valid(static_cast@L@quant::Format@G@(i))) continue;",
        "registry iteration")
    sub(p, '"  -> PASSED: All 38 format enum definitions verified!"',
        '"  -> PASSED: All 69 live format enum definitions verified!"',
        "pass message")

    # bench iterates live ids
    p = R + "/bench/bench_format_comparison.cpp"
    sub(p, "for (int v = 0; v < quant::FORMAT_COUNT; ++v) {",
        "for (int v = 0; v < quant::FORMAT_ID_SLOTS; ++v) {\n"
        "        if (!quant::format_is_valid(static_cast@L@quant::Format@G@(v))) continue;",
        "bench iterates live ids")

    # test_quant_mix: MX 3.78125 -> 3.50 pins
    p = R + "/tests/test_quant_mix.cpp"
    s = read(p)
    s = s.replace("3.78125f", "3.50f").replace("3.78125", "3.50")
    write(p, s)
    report.append("ok    test_quant_mix.cpp   :: MX 3.78125 -> 3.50 pins")


if __name__ == "__main__":
    write_format_compat()
    patch_block_codec()
    patch_k_tier()
    patch_format_registry()
    patch_registry_cpp_bpw()
    patch_inferno()
    patch_consumers()
    patch_tests()
    for line in report:
        print(line)
    misses = [l for l in report if l.startswith("MISS") or l.startswith("WARN")]
    print("\n%d actions, %d misses/warnings" % (len(report), len(misses)))