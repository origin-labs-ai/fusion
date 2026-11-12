// ============================================================
// Format enum - Fusion canonical quantization formats (Operation Clean).
//
// Contract (docs/operation-clean/LADDER.md): 69 live formats, every
// name == nominal == wire BPW, every wire BPW on the .0 / .25 / .50 grid.
//   base (L) = exact integer BPW | M = base + 0.25 | H = base + 0.50
//   Q_1 = binary at exact 1.00 (G-1)
//   Q_1_K_H = PURE TERNARY at exact 1.50 - ternary's only home (G-2)
//   GRP base is rewired DOWN to its exact integer BPW (G-5: the layout
//   comes down to the name, never the name up to the wire)
//   MX formats are QUARANTINED (below industrial parity, D-13)
//
// 36 ids are RETIRED: they stay addressable (ids are stored raw in
// .quant files with no version tag) but are not valid formats - writers
// never emit them, readers remap or reject (include/quant/format_compat.h).
// The 98 legacy spellings (Q1, QG2, Q1_5, QG_MX_*, ...) are REMOVED:
// canonical names only.
// ============================================================
enum class Format : uint8_t {
    // --- Plain base (L tier) - exact integer BPW (10) ---
    Q_1              = 0,   // 1.0
    Q_2              = 1,   // 2.0
    Q_3              = 2,   // 3.0
    Q_4              = 3,   // 4.0
    Q_6              = 4,   // 6.0
    Q_8              = 5,   // 8.0
    Q_12             = 6,   // 12.0
    Q_16             = 7,   // 16.0
    Q_24             = 8,   // 24.0
    Q_32             = 9,   // 32.0
    // --- Plain M / H tiers - base + 0.25 / + 0.50 (18) ---
    Q_1_K_M         = 11,   // 1.25
    Q_1_K_H         = 12,   // 1.5
    Q_2_K_M         = 14,   // 2.25
    Q_2_K_H         = 15,   // 2.5
    Q_3_K_M         = 17,   // 3.25
    Q_3_K_H         = 18,   // 3.5
    Q_4_K_M         = 20,   // 4.25
    Q_4_K_H         = 21,   // 4.5
    Q_6_K_M         = 23,   // 6.25
    Q_6_K_H         = 24,   // 6.5
    Q_8_K_M         = 26,   // 8.25
    Q_8_K_H         = 27,   // 8.5
    Q_12_K_M         = 29,   // 12.25
    Q_12_K_H         = 30,   // 12.5
    Q_16_K_M         = 32,   // 16.25
    Q_16_K_H         = 33,   // 16.5
    Q_24_K_M         = 35,   // 24.25
    Q_24_K_H         = 36,   // 24.5
    // --- GRP base - rewired down to exact integer BPW (9) ---
    Q_G_1          = 37,   // 1.0
    Q_G_2          = 38,   // 2.0
    Q_G_3          = 39,   // 3.0
    Q_G_4          = 40,   // 4.0
    Q_G_6          = 41,   // 6.0
    Q_G_8          = 42,   // 8.0
    Q_G_12         = 43,   // 12.0
    Q_G_16         = 44,   // 16.0
    Q_G_24         = 45,   // 24.0
    // --- GRP M / H tiers - base + 0.25 / + 0.50 (18) ---
    Q_G_1_K_M     = 47,   // 1.25
    Q_G_1_K_H     = 48,   // 1.5
    Q_G_2_K_M     = 50,   // 2.25
    Q_G_2_K_H     = 51,   // 2.5
    Q_G_3_K_M     = 53,   // 3.25
    Q_G_3_K_H     = 54,   // 3.5
    Q_G_4_K_M     = 56,   // 4.25
    Q_G_4_K_H     = 57,   // 4.5
    Q_G_6_K_M     = 59,   // 6.25
    Q_G_6_K_H     = 60,   // 6.5
    Q_G_8_K_M     = 62,   // 8.25
    Q_G_8_K_H     = 63,   // 8.5
    Q_G_12_K_M     = 65,   // 12.25
    Q_G_12_K_H     = 66,   // 12.5
    Q_G_16_K_M     = 68,   // 16.25
    Q_G_16_K_H     = 69,   // 16.5
    Q_G_24_K_M     = 71,   // 24.25
    Q_G_24_K_H     = 72,   // 24.5
    // --- MX 4-tier mixes (14) - QUARANTINED: below industrial parity,
    //     excluded from dominance claims until the tier allocator is
    //     reworked (D-13). ---
    Q_MX_3_5         = 91, Q_MX_4_5         = 92, Q_MX_6_5         = 93,
    Q_MX_8_5         = 94, Q_MX_12_5        = 95, Q_MX_16_5        = 96, Q_MX_24_5        = 97,
    Q_G_MX_3_5       = 98, Q_G_MX_4_5       = 99, Q_G_MX_6_5       = 100,
    Q_G_MX_8_5       = 101, Q_G_MX_12_5     = 102, Q_G_MX_16_5     = 103, Q_G_MX_24_5     = 104,

    // --- Retired ids (36): addressable, never valid ---
    // plain K_L - the base id IS the L tier
    Q_1_K_L       = 10,
    Q_2_K_L       = 13,
    Q_3_K_L       = 16,
    Q_4_K_L       = 19,
    Q_6_K_L       = 22,
    Q_8_K_L       = 25,
    Q_12_K_L       = 28,
    Q_16_K_L       = 31,
    Q_24_K_L       = 34,
    // GRP K_L - retired with the K_L tier
    Q_G_1_K_L    = 46,
    Q_G_2_K_L    = 49,
    Q_G_3_K_L    = 52,
    Q_G_4_K_L    = 55,
    Q_G_6_K_L    = 58,
    Q_G_8_K_L    = 61,
    Q_G_12_K_L    = 64,
    Q_G_16_K_L    = 67,
    Q_G_24_K_L    = 70,
    // half-BPW families - superseded by the M/H tiers
    Q_1_5         = 73,
    Q_2_5         = 74,
    Q_3_5         = 75,
    Q_4_5         = 76,
    Q_6_5         = 77,
    Q_8_5         = 78,
    Q_12_5         = 79,
    Q_16_5         = 80,
    Q_24_5         = 81,
    Q_G_1_5      = 82,
    Q_G_2_5      = 83,
    Q_G_3_5      = 84,
    Q_G_4_5      = 85,
    Q_G_6_5      = 86,
    Q_G_8_5      = 87,
    Q_G_12_5      = 88,
    Q_G_16_5      = 89,
    Q_G_24_5      = 90,
};

// FORMAT_ID_SLOTS: size of the raw id address space - never shrinks.
// FORMAT_COUNT: number of LIVE formats (the ladder).
constexpr int FORMAT_ID_SLOTS = 105;
constexpr int FORMAT_COUNT    = 69;

// Validity table - the single truth for "is this a live format". Replaces
// every id-range predicate and every `wire_fmt < FORMAT_COUNT` clamp site.
constexpr bool kFormatValid[FORMAT_ID_SLOTS] = {
    true, true, true, true, true, true, true, true, true, true,
    false, true, true, false, true, true, false, true, true, false,
    true, true, false, true, true, false, true, true, false, true,
    true, false, true, true, false, true, true, true, true, true,
    true, true, true, true, true, true, false, true, true, false,
    true, true, false, true, true, false, true, true, false, true,
    true, false, true, true, false, true, true, false, true, true,
    false, true, true, false, false, false, false, false, false, false,
    false, false, false, false, false, false, false, false, false, false,
    false, true, true, true, true, true, true, true, true, true,
    true, true, true, true, true,
};
inline bool format_is_valid(Format f) {
    const int v = (int)f;
    return v >= 0 && v < FORMAT_ID_SLOTS && kFormatValid[v];
}

inline const char* format_name(Format f) {
    switch (f) {
        case Format::Q_1: return "Q_1";
        case Format::Q_2: return "Q_2";
        case Format::Q_3: return "Q_3";
        case Format::Q_4: return "Q_4";
        case Format::Q_6: return "Q_6";
        case Format::Q_8: return "Q_8";
        case Format::Q_12: return "Q_12";
        case Format::Q_16: return "Q_16";
        case Format::Q_24: return "Q_24";
        case Format::Q_32: return "Q_32";
        case Format::Q_1_K_L: return "Q_1_K_L";
        case Format::Q_1_K_M: return "Q_1_K_M";
        case Format::Q_1_K_H: return "Q_1_K_H";
        case Format::Q_2_K_L: return "Q_2_K_L";
        case Format::Q_2_K_M: return "Q_2_K_M";
        case Format::Q_2_K_H: return "Q_2_K_H";
        case Format::Q_3_K_L: return "Q_3_K_L";
        case Format::Q_3_K_M: return "Q_3_K_M";
        case Format::Q_3_K_H: return "Q_3_K_H";
        case Format::Q_4_K_L: return "Q_4_K_L";
        case Format::Q_4_K_M: return "Q_4_K_M";
        case Format::Q_4_K_H: return "Q_4_K_H";
        case Format::Q_6_K_L: return "Q_6_K_L";
        case Format::Q_6_K_M: return "Q_6_K_M";
        case Format::Q_6_K_H: return "Q_6_K_H";
        case Format::Q_8_K_L: return "Q_8_K_L";
        case Format::Q_8_K_M: return "Q_8_K_M";
        case Format::Q_8_K_H: return "Q_8_K_H";
        case Format::Q_12_K_L: return "Q_12_K_L";
        case Format::Q_12_K_M: return "Q_12_K_M";
        case Format::Q_12_K_H: return "Q_12_K_H";
        case Format::Q_16_K_L: return "Q_16_K_L";
        case Format::Q_16_K_M: return "Q_16_K_M";
        case Format::Q_16_K_H: return "Q_16_K_H";
        case Format::Q_24_K_L: return "Q_24_K_L";
        case Format::Q_24_K_M: return "Q_24_K_M";
        case Format::Q_24_K_H: return "Q_24_K_H";
        case Format::Q_G_1: return "Q_G_1";
        case Format::Q_G_2: return "Q_G_2";
        case Format::Q_G_3: return "Q_G_3";
        case Format::Q_G_4: return "Q_G_4";
        case Format::Q_G_6: return "Q_G_6";
        case Format::Q_G_8: return "Q_G_8";
        case Format::Q_G_12: return "Q_G_12";
        case Format::Q_G_16: return "Q_G_16";
        case Format::Q_G_24: return "Q_G_24";
        case Format::Q_G_1_K_L: return "Q_G_1_K_L";
        case Format::Q_G_1_K_M: return "Q_G_1_K_M";
        case Format::Q_G_1_K_H: return "Q_G_1_K_H";
        case Format::Q_G_2_K_L: return "Q_G_2_K_L";
        case Format::Q_G_2_K_M: return "Q_G_2_K_M";
        case Format::Q_G_2_K_H: return "Q_G_2_K_H";
        case Format::Q_G_3_K_L: return "Q_G_3_K_L";
        case Format::Q_G_3_K_M: return "Q_G_3_K_M";
        case Format::Q_G_3_K_H: return "Q_G_3_K_H";
        case Format::Q_G_4_K_L: return "Q_G_4_K_L";
        case Format::Q_G_4_K_M: return "Q_G_4_K_M";
        case Format::Q_G_4_K_H: return "Q_G_4_K_H";
        case Format::Q_G_6_K_L: return "Q_G_6_K_L";
        case Format::Q_G_6_K_M: return "Q_G_6_K_M";
        case Format::Q_G_6_K_H: return "Q_G_6_K_H";
        case Format::Q_G_8_K_L: return "Q_G_8_K_L";
        case Format::Q_G_8_K_M: return "Q_G_8_K_M";
        case Format::Q_G_8_K_H: return "Q_G_8_K_H";
        case Format::Q_G_12_K_L: return "Q_G_12_K_L";
        case Format::Q_G_12_K_M: return "Q_G_12_K_M";
        case Format::Q_G_12_K_H: return "Q_G_12_K_H";
        case Format::Q_G_16_K_L: return "Q_G_16_K_L";
        case Format::Q_G_16_K_M: return "Q_G_16_K_M";
        case Format::Q_G_16_K_H: return "Q_G_16_K_H";
        case Format::Q_G_24_K_L: return "Q_G_24_K_L";
        case Format::Q_G_24_K_M: return "Q_G_24_K_M";
        case Format::Q_G_24_K_H: return "Q_G_24_K_H";
        case Format::Q_1_5: return "Q_1_5";
        case Format::Q_2_5: return "Q_2_5";
        case Format::Q_3_5: return "Q_3_5";
        case Format::Q_4_5: return "Q_4_5";
        case Format::Q_6_5: return "Q_6_5";
        case Format::Q_8_5: return "Q_8_5";
        case Format::Q_12_5: return "Q_12_5";
        case Format::Q_16_5: return "Q_16_5";
        case Format::Q_24_5: return "Q_24_5";
        case Format::Q_G_1_5: return "Q_G_1_5";
        case Format::Q_G_2_5: return "Q_G_2_5";
        case Format::Q_G_3_5: return "Q_G_3_5";
        case Format::Q_G_4_5: return "Q_G_4_5";
        case Format::Q_G_6_5: return "Q_G_6_5";
        case Format::Q_G_8_5: return "Q_G_8_5";
        case Format::Q_G_12_5: return "Q_G_12_5";
        case Format::Q_G_16_5: return "Q_G_16_5";
        case Format::Q_G_24_5: return "Q_G_24_5";
        case Format::Q_MX_3_5: return "Q_MX_3_5";
        case Format::Q_MX_4_5: return "Q_MX_4_5";
        case Format::Q_MX_6_5: return "Q_MX_6_5";
        case Format::Q_MX_8_5: return "Q_MX_8_5";
        case Format::Q_MX_12_5: return "Q_MX_12_5";
        case Format::Q_MX_16_5: return "Q_MX_16_5";
        case Format::Q_MX_24_5: return "Q_MX_24_5";
        case Format::Q_G_MX_3_5: return "Q_G_MX_3_5";
        case Format::Q_G_MX_4_5: return "Q_G_MX_4_5";
        case Format::Q_G_MX_6_5: return "Q_G_MX_6_5";
        case Format::Q_G_MX_8_5: return "Q_G_MX_8_5";
        case Format::Q_G_MX_12_5: return "Q_G_MX_12_5";
        case Format::Q_G_MX_16_5: return "Q_G_MX_16_5";
        case Format::Q_G_MX_24_5: return "Q_G_MX_24_5";
        default: return "unknown";
    }
}

// format_bpw = WIRE truth (G-5: the name says X => the wire costs exactly
// X). Retired ids report 0: they are not selectable, encodable or writable.
inline float format_bpw(Format f) {
    switch (f) {
        case Format::Q_1: return 1.0f;
        case Format::Q_2: return 2.0f;
        case Format::Q_3: return 3.0f;
        case Format::Q_4: return 4.0f;
        case Format::Q_6: return 6.0f;
        case Format::Q_8: return 8.0f;
        case Format::Q_12: return 12.0f;
        case Format::Q_16: return 16.0f;
        case Format::Q_24: return 24.0f;
        case Format::Q_32: return 32.0f;
        case Format::Q_1_K_M: return 1.25f;
        case Format::Q_1_K_H: return 1.5f;
        case Format::Q_2_K_M: return 2.25f;
        case Format::Q_2_K_H: return 2.5f;
        case Format::Q_3_K_M: return 3.25f;
        case Format::Q_3_K_H: return 3.5f;
        case Format::Q_4_K_M: return 4.25f;
        case Format::Q_4_K_H: return 4.5f;
        case Format::Q_6_K_M: return 6.25f;
        case Format::Q_6_K_H: return 6.5f;
        case Format::Q_8_K_M: return 8.25f;
        case Format::Q_8_K_H: return 8.5f;
        case Format::Q_12_K_M: return 12.25f;
        case Format::Q_12_K_H: return 12.5f;
        case Format::Q_16_K_M: return 16.25f;
        case Format::Q_16_K_H: return 16.5f;
        case Format::Q_24_K_M: return 24.25f;
        case Format::Q_24_K_H: return 24.5f;
        case Format::Q_G_1: return 1.0f;
        case Format::Q_G_2: return 2.0f;
        case Format::Q_G_3: return 3.0f;
        case Format::Q_G_4: return 4.0f;
        case Format::Q_G_6: return 6.0f;
        case Format::Q_G_8: return 8.0f;
        case Format::Q_G_12: return 12.0f;
        case Format::Q_G_16: return 16.0f;
        case Format::Q_G_24: return 24.0f;
        case Format::Q_G_1_K_M: return 1.25f;
        case Format::Q_G_1_K_H: return 1.5f;
        case Format::Q_G_2_K_M: return 2.25f;
        case Format::Q_G_2_K_H: return 2.5f;
        case Format::Q_G_3_K_M: return 3.25f;
        case Format::Q_G_3_K_H: return 3.5f;
        case Format::Q_G_4_K_M: return 4.25f;
        case Format::Q_G_4_K_H: return 4.5f;
        case Format::Q_G_6_K_M: return 6.25f;
        case Format::Q_G_6_K_H: return 6.5f;
        case Format::Q_G_8_K_M: return 8.25f;
        case Format::Q_G_8_K_H: return 8.5f;
        case Format::Q_G_12_K_M: return 12.25f;
        case Format::Q_G_12_K_H: return 12.5f;
        case Format::Q_G_16_K_M: return 16.25f;
        case Format::Q_G_16_K_H: return 16.5f;
        case Format::Q_G_24_K_M: return 24.25f;
        case Format::Q_G_24_K_H: return 24.5f;
        case Format::Q_MX_3_5: return 3.5f;
        case Format::Q_MX_4_5: return 4.5f;
        case Format::Q_MX_6_5: return 6.5f;
        case Format::Q_MX_8_5: return 8.5f;
        case Format::Q_MX_12_5: return 12.5f;
        case Format::Q_MX_16_5: return 16.5f;
        case Format::Q_MX_24_5: return 24.5f;
        case Format::Q_G_MX_3_5: return 3.5f;
        case Format::Q_G_MX_4_5: return 4.5f;
        case Format::Q_G_MX_6_5: return 6.5f;
        case Format::Q_G_MX_8_5: return 8.5f;
        case Format::Q_G_MX_12_5: return 12.5f;
        case Format::Q_G_MX_16_5: return 16.5f;
        case Format::Q_G_MX_24_5: return 24.5f;
        default: return 0.0f;
    }
}
inline float format_nominal_bpw(Format f) { return format_bpw(f); }
inline float format_wire_bpw(Format f)     { return format_bpw(f); }

// Class predicates. All gated on format_is_valid (retired ids are not
// selectable, enumerable, or writable).
inline bool format_is_base(Format f) {
    const int v = (int)f;
    return v >= 0 && v <= 9 && format_is_valid(f);
}
inline bool format_is_k(Format f) {
    const int v = (int)f;
    const bool plain = (v >= 11 && v <= 36) && ((v - 11) % 3 != 2);
    const bool grp = (v >= 47 && v <= 72) && ((v - 47) % 3 != 2);
    return (plain || grp) && format_is_valid(f);
}
inline bool format_is_grp(Format f) {
    const int v = (int)f;
    return ((v >= 37 && v <= 72) || (v >= 98 && v <= 104)) && format_is_valid(f);
}
inline bool format_is_half(Format f) { (void)f; return false; }
inline bool format_is_mx(Format f) {
    const int v = (int)f;
    return v >= 91 && v <= 104 && format_is_valid(f);
}
inline bool format_is_mx_plain(Format f) {
    const int v = (int)f;
    return v >= 91 && v <= 97 && format_is_valid(f);
}
inline bool format_is_mixed(Format f) { return format_is_mx(f); }
inline bool format_is_twi_mix(Format f) { (void)f; return false; }
inline bool format_is_quad_mix(Format f) { return format_is_mx(f); }

// Base-family bit width of a format (0 for the MX mixes).
inline int format_family_bits(Format f) {
    switch (f) {
        case Format::Q_1: return 1;
        case Format::Q_2: return 2;
        case Format::Q_3: return 3;
        case Format::Q_4: return 4;
        case Format::Q_6: return 6;
        case Format::Q_8: return 8;
        case Format::Q_12: return 12;
        case Format::Q_16: return 16;
        case Format::Q_24: return 24;
        case Format::Q_32: return 32;
        case Format::Q_1_K_M: case Format::Q_1_K_H: return 1;
        case Format::Q_2_K_M: case Format::Q_2_K_H: return 2;
        case Format::Q_3_K_M: case Format::Q_3_K_H: return 3;
        case Format::Q_4_K_M: case Format::Q_4_K_H: return 4;
        case Format::Q_6_K_M: case Format::Q_6_K_H: return 6;
        case Format::Q_8_K_M: case Format::Q_8_K_H: return 8;
        case Format::Q_12_K_M: case Format::Q_12_K_H: return 12;
        case Format::Q_16_K_M: case Format::Q_16_K_H: return 16;
        case Format::Q_24_K_M: case Format::Q_24_K_H: return 24;
        case Format::Q_G_1: return 1;
        case Format::Q_G_2: return 2;
        case Format::Q_G_3: return 3;
        case Format::Q_G_4: return 4;
        case Format::Q_G_6: return 6;
        case Format::Q_G_8: return 8;
        case Format::Q_G_12: return 12;
        case Format::Q_G_16: return 16;
        case Format::Q_G_24: return 24;
        case Format::Q_G_1_K_M: case Format::Q_G_1_K_H: return 1;
        case Format::Q_G_2_K_M: case Format::Q_G_2_K_H: return 2;
        case Format::Q_G_3_K_M: case Format::Q_G_3_K_H: return 3;
        case Format::Q_G_4_K_M: case Format::Q_G_4_K_H: return 4;
        case Format::Q_G_6_K_M: case Format::Q_G_6_K_H: return 6;
        case Format::Q_G_8_K_M: case Format::Q_G_8_K_H: return 8;
        case Format::Q_G_12_K_M: case Format::Q_G_12_K_H: return 12;
        case Format::Q_G_16_K_M: case Format::Q_G_16_K_H: return 16;
        case Format::Q_G_24_K_M: case Format::Q_G_24_K_H: return 24;
        default: return 0;
    }
}

inline int format_codebook_size(Format f) {
    switch (format_family_bits(f)) {
        case 1: return 1;
        case 2: return 4;
        case 3: return 8;
        case 4: return 16;
        case 6: return 64;
        case 8: return 256;
        case 12: return 4096;
        default: return 0;
    }
}

enum class DType : uint8_t { I64,I32,U8,U4,U16,F16,F32 };
inline size_t dtype_size(DType dt){ switch(dt){case DType::I64:return 8;case DType::I32:return 4;case DType::U8:return 1;case DType::U4:return 1;case DType::U16:return 2;case DType::F16:return 2;case DType::F32:return 4;default:return 0;}}
inline DType format_to_dtype(Format f) {
    switch (format_family_bits(f)) {
        case 1: case 2: case 3: case 6: case 8: return DType::U8;
        case 4: return DType::U4;
        case 12: return DType::U16;
        case 16: case 24: return DType::F16;
        case 32: return DType::F32;
        default: return DType::U8;
    }
}
