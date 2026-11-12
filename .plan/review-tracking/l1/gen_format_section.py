"""Generate the Operation-Clean Format section for types.h from the LADDER
contract (docs/operation-clean/LADDER.md).

Ladder: 69 live ids, 36 retired holes, no renumbering.
  10 plain base : ids 0..9
  18 plain M/H  : ids 11,12,14,15,17,18,20,21,23,24,26,27,29,30,32,33,35,36
   9 GRP base   : ids 37..45   (rewired down to exact integer BPW)
  18 GRP M/H    : ids 47,48,50,51,53,54,56,57,59,60,62,63,65,66,68,69,71,72
  14 MX         : ids 91..104  (quarantined)

Retired (36): plain K_L {10,13,16,19,22,25,28,31,34}, GRP K_L
{46,49,52,55,58,61,64,67,70}, half-BPW {73..90}.
The 98 legacy spellings are removed: canonical names only.

Usage: python -I gen_format_section.py --out FILE
"""
import sys

PLAIN_FAMS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]   # Q_32 has no tiers
GRP_FAMS = [1, 2, 3, 4, 6, 8, 12, 16, 24]
MX_TAGS = ["3_5", "4_5", "6_5", "8_5", "12_5", "16_5", "24_5"]
MX_BPW = {"3_5": 3.5, "4_5": 4.5, "6_5": 6.5, "8_5": 8.5,
          "12_5": 12.5, "16_5": 16.5, "24_5": 24.5}

live = []
for i, b in enumerate(PLAIN_FAMS):
    live.append((i, "Q_%d" % b, float(b), "base"))
for i, b in enumerate(PLAIN_FAMS[:-1]):
    live.append((11 + 3 * i, "Q_%d_K_M" % b, b + 0.25, "mh"))
    live.append((12 + 3 * i, "Q_%d_K_H" % b, b + 0.50, "mh"))
for i, b in enumerate(GRP_FAMS):
    live.append((37 + i, "Q_G_%d" % b, float(b), "grp"))
for i, b in enumerate(GRP_FAMS):
    live.append((47 + 3 * i, "Q_G_%d_K_M" % b, b + 0.25, "grpmh"))
    live.append((48 + 3 * i, "Q_G_%d_K_H" % b, b + 0.50, "grpmh"))
for i, t in enumerate(MX_TAGS):
    live.append((91 + i, "Q_MX_%s" % t, MX_BPW[t], "mx"))
for i, t in enumerate(MX_TAGS):
    live.append((98 + i, "Q_G_MX_%s" % t, MX_BPW[t], "mx"))

retired = []
for i, b in enumerate(PLAIN_FAMS[:-1]):
    retired.append((10 + 3 * i, "Q_%d_K_L" % b))
for i, b in enumerate(GRP_FAMS):
    retired.append((46 + 3 * i, "Q_G_%d_K_L" % b))
for i, b in enumerate(PLAIN_FAMS[:-1]):
    retired.append((73 + i, "Q_%d_5" % b))
for i, b in enumerate(GRP_FAMS):
    retired.append((82 + i, "Q_G_%d_5" % b))

by_id = dict((t[0], t) for t in live)
ret_by_id = dict((t[0], t[1]) for t in retired)
assert len(live) == 69 and len(retired) == 36
assert sorted(list(by_id.keys()) + list(ret_by_id.keys())) == list(range(105))
VALID = set(by_id.keys())


def is_base(i):
    return i <= 9


def is_k(i):
    return (11 <= i <= 36 and (i - 11) % 3 != 2) or (47 <= i <= 72 and (i - 47) % 3 != 2)


def is_grp(i):
    return 37 <= i <= 72 or 98 <= i <= 104


def bpw_str(v):
    # Always keep a decimal point: "1" would emit the invalid literal "1f".
    t = ("%.5f" % v).rstrip("0")
    if t.endswith("."):
        t += "0"
    return t


def gen():
    o = []
    A = o.append
    A("// ============================================================")
    A("// Format enum - Fusion canonical quantization formats (Operation Clean).")
    A("//")
    A("// Contract (docs/operation-clean/LADDER.md): 69 live formats, every")
    A("// name == nominal == wire BPW, every wire BPW on the .0 / .25 / .50 grid.")
    A("//   base (L) = exact integer BPW | M = base + 0.25 | H = base + 0.50")
    A("//   Q_1 = binary at exact 1.00 (G-1)")
    A("//   Q_1_K_H = PURE TERNARY at exact 1.50 - ternary's only home (G-2)")
    A("//   GRP base is rewired DOWN to its exact integer BPW (G-5: the layout")
    A("//   comes down to the name, never the name up to the wire)")
    A("//   MX formats are QUARANTINED (below industrial parity, D-13)")
    A("//")
    A("// 36 ids are RETIRED: they stay addressable (ids are stored raw in")
    A("// .quant files with no version tag) but are not valid formats - writers")
    A("// never emit them, readers remap or reject (include/quant/format_compat.h).")
    A("// The 98 legacy spellings (Q1, QG2, Q1_5, QG_MX_*, ...) are REMOVED:")
    A("// canonical names only.")
    A("// ============================================================")
    A("enum class Format : uint8_t {")
    A("    // --- Plain base (L tier) - exact integer BPW (10) ---")
    for i, b in enumerate(PLAIN_FAMS):
        A("    Q_%-14s = %d,   // %s" % (b, i, bpw_str(float(b))))
    A("    // --- Plain M / H tiers - base + 0.25 / + 0.50 (18) ---")
    for i, b in enumerate(PLAIN_FAMS[:-1]):
        A("    Q_%d_K_M%-8s = %d,   // %s" % (b, "", 11 + 3 * i, bpw_str(b + 0.25)))
        A("    Q_%d_K_H%-8s = %d,   // %s" % (b, "", 12 + 3 * i, bpw_str(b + 0.50)))
    A("    // --- GRP base - rewired down to exact integer BPW (9) ---")
    for i, b in enumerate(GRP_FAMS):
        A("    Q_G_%-10s = %d,   // %s" % (b, 37 + i, bpw_str(float(b))))
    A("    // --- GRP M / H tiers - base + 0.25 / + 0.50 (18) ---")
    for i, b in enumerate(GRP_FAMS):
        A("    Q_G_%d_K_M%-4s = %d,   // %s" % (b, "", 47 + 3 * i, bpw_str(b + 0.25)))
        A("    Q_G_%d_K_H%-4s = %d,   // %s" % (b, "", 48 + 3 * i, bpw_str(b + 0.50)))
    A("    // --- MX 4-tier mixes (14) - QUARANTINED: below industrial parity,")
    A("    //     excluded from dominance claims until the tier allocator is")
    A("    //     reworked (D-13). ---")
    A("    Q_MX_3_5         = 91, Q_MX_4_5         = 92, Q_MX_6_5         = 93,")
    A("    Q_MX_8_5         = 94, Q_MX_12_5        = 95, Q_MX_16_5        = 96, Q_MX_24_5        = 97,")
    A("    Q_G_MX_3_5       = 98, Q_G_MX_4_5       = 99, Q_G_MX_6_5       = 100,")
    A("    Q_G_MX_8_5       = 101, Q_G_MX_12_5     = 102, Q_G_MX_16_5     = 103, Q_G_MX_24_5     = 104,")
    A("")
    A("    // --- Retired ids (36): addressable, never valid ---")
    A("    // plain K_L - the base id IS the L tier")
    for i, b in enumerate(PLAIN_FAMS[:-1]):
        A("    Q_%d_K_L%-6s = %d," % (b, "", 10 + 3 * i))
    A("    // GRP K_L - retired with the K_L tier")
    for i, b in enumerate(GRP_FAMS):
        A("    Q_G_%d_K_L%-3s = %d," % (b, "", 46 + 3 * i))
    A("    // half-BPW families - superseded by the M/H tiers")
    for i, b in enumerate(PLAIN_FAMS[:-1]):
        A("    Q_%d_5%-8s = %d," % (b, "", 73 + i))
    for i, b in enumerate(GRP_FAMS):
        A("    Q_G_%d_5%-5s = %d," % (b, "", 82 + i))
    A("};")
    A("")
    A("// FORMAT_ID_SLOTS: size of the raw id address space - never shrinks.")
    A("// FORMAT_COUNT: number of LIVE formats (the ladder).")
    A("constexpr int FORMAT_ID_SLOTS = 105;")
    A("constexpr int FORMAT_COUNT    = 69;")
    A("")
    A("// Validity table - the single truth for \"is this a live format\". Replaces")
    A("// every id-range predicate and every `wire_fmt < FORMAT_COUNT` clamp site.")
    A("constexpr bool kFormatValid[FORMAT_ID_SLOTS] = {")
    for row in range(0, 105, 10):
        n = min(10, 105 - row)
        vals = ", ".join(("true" if i in VALID else "false") for i in range(row, row + n))
        A("    %s," % vals)
    A("};")
    A("inline bool format_is_valid(Format f) {")
    A("    const int v = (int)f;")
    A("    return v >= 0 && v < FORMAT_ID_SLOTS && kFormatValid[v];")
    A("}")
    A("")
    A("inline const char* format_name(Format f) {")
    A("    switch (f) {")
    for i in range(105):
        if i in by_id:
            nm = by_id[i][1]
        else:
            nm = ret_by_id[i]
        A('        case Format::%s: return "%s";' % (nm, nm))
    A('        default: return "unknown";')
    A("    }")
    A("}")
    A("")
    A("// format_bpw = WIRE truth (G-5: the name says X => the wire costs exactly")
    A("// X). Retired ids report 0: they are not selectable, encodable or writable.")
    A("inline float format_bpw(Format f) {")
    A("    switch (f) {")
    for i in range(105):
        if i in by_id:
            A("        case Format::%s: return %sf;" % (by_id[i][1], bpw_str(by_id[i][2])))
    A("        default: return 0.0f;")
    A("    }")
    A("}")
    A("inline float format_nominal_bpw(Format f) { return format_bpw(f); }")
    A("inline float format_wire_bpw(Format f)     { return format_bpw(f); }")
    A("")
    A("// Class predicates. All gated on format_is_valid (retired ids are not")
    A("// selectable, enumerable, or writable).")
    A("inline bool format_is_base(Format f) {")
    A("    const int v = (int)f;")
    A("    return v >= 0 && v <= 9 && format_is_valid(f);")
    A("}")
    A("inline bool format_is_k(Format f) {")
    A("    const int v = (int)f;")
    A("    const bool plain = (v >= 11 && v <= 36) && ((v - 11) % 3 != 2);")
    A("    const bool grp = (v >= 47 && v <= 72) && ((v - 47) % 3 != 2);")
    A("    return (plain || grp) && format_is_valid(f);")
    A("}")
    A("inline bool format_is_grp(Format f) {")
    A("    const int v = (int)f;")
    A("    return ((v >= 37 && v <= 72) || (v >= 98 && v <= 104)) && format_is_valid(f);")
    A("}")
    A("inline bool format_is_half(Format f) { (void)f; return false; }")
    A("inline bool format_is_mx(Format f) {")
    A("    const int v = (int)f;")
    A("    return v >= 91 && v <= 104 && format_is_valid(f);")
    A("}")
    A("inline bool format_is_mx_plain(Format f) {")
    A("    const int v = (int)f;")
    A("    return v >= 91 && v <= 97 && format_is_valid(f);")
    A("}")
    A("inline bool format_is_mixed(Format f) { return format_is_mx(f); }")
    A("inline bool format_is_twi_mix(Format f) { (void)f; return false; }")
    A("inline bool format_is_quad_mix(Format f) { return format_is_mx(f); }")
    A("")
    A("// Base-family bit width of a format (0 for the MX mixes).")
    A("inline int format_family_bits(Format f) {")
    A("    switch (f) {")
    for b in PLAIN_FAMS:
        A("        case Format::Q_%d: return %d;" % (b, b))
    for b in PLAIN_FAMS[:-1]:
        A("        case Format::Q_%d_K_M: case Format::Q_%d_K_H: return %d;" % (b, b, b))
    for b in GRP_FAMS:
        A("        case Format::Q_G_%d: return %d;" % (b, b))
    for b in GRP_FAMS:
        A("        case Format::Q_G_%d_K_M: case Format::Q_G_%d_K_H: return %d;" % (b, b, b))
    A("        default: return 0;")
    A("    }")
    A("}")
    A("")
    A("inline int format_codebook_size(Format f) {")
    A("    switch (format_family_bits(f)) {")
    A("        case 1: return 1;")
    A("        case 2: return 4;")
    A("        case 3: return 8;")
    A("        case 4: return 16;")
    A("        case 6: return 64;")
    A("        case 8: return 256;")
    A("        case 12: return 4096;")
    A("        default: return 0;")
    A("    }")
    A("}")
    A("")
    A("enum class DType : uint8_t { I64,I32,U8,U4,U16,F16,F32 };")
    A("inline size_t dtype_size(DType dt){ switch(dt){case DType::I64:return 8;case DType::I32:return 4;case DType::U8:return 1;case DType::U4:return 1;case DType::U16:return 2;case DType::F16:return 2;case DType::F32:return 4;default:return 0;}}")
    A("inline DType format_to_dtype(Format f) {")
    A("    switch (format_family_bits(f)) {")
    A("        case 1: case 2: case 3: case 6: case 8: return DType::U8;")
    A("        case 4: return DType::U4;")
    A("        case 12: return DType::U16;")
    A("        case 16: case 24: return DType::F16;")
    A("        case 32: return DType::F32;")
    A("        default: return DType::U8;")
    A("    }")
    A("}")
    return "\n".join(o)


if __name__ == "__main__":
    text = gen()
    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        fh = open(path, "w", encoding="utf-8", newline="\n")
        fh.write(text + "\n")
        fh.close()
        print("wrote %s (%d lines)" % (path, len(text.splitlines())))
    else:
        sys.stdout.write(text + "\n")