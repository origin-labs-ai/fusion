"""Fix the L1 generator output and finish the L1 patches.

Fixes:
  1. gen_format_section.py: bpw_str must keep a decimal point (1 -> "1.0f");
     the validity table must have exactly 105 entries (10 rows of 10 + 5).
  2. Re-apply the corrected section to types.h.
  3. block_codec.cpp: remove the four remaining retired cases (the ones that
     carried a brace, so the first pass kept them).
  4. The eight test patches that missed on the first pass (exact current text
     now known).

Run: python -I fix_l1.py
"""
import os
import sys
import re

BASE = r"C:/Users/thaku/Workspaces/fusion/review-tracking/l1"
R = r"C:/Users/thaku/Workspaces/fusion/transformers"

report = []


def C(s):
    return s.replace("@L@", chr(60)).replace("@G@", chr(62))


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def sub(path, old, new, label):
    old, new = C(old), C(new)
    s = read(path)
    if old not in s:
        report.append("MISS  %-28s :: %s" % (os.path.basename(path), label))
        return False
    write(path, s.replace(old, new, 1))
    report.append("ok    %-28s :: %s" % (os.path.basename(path), label))
    return True


# ------------------------------------------------- 1. fix the generator
gen = BASE + "/gen_format_section.py"
s = read(gen)
old_bpw = '''def bpw_str(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")'''
new_bpw = '''def bpw_str(v):
    # Always keep a decimal point: "1" would emit the invalid literal "1f".
    t = ("%.5f" % v).rstrip("0")
    if t.endswith("."):
        t += "0"
    return t'''
if old_bpw in s:
    s = s.replace(old_bpw, new_bpw, 1)
    report.append("ok    gen_format_section.py :: bpw_str keeps a decimal point")
else:
    report.append("MISS  gen_format_section.py :: bpw_str pattern")

old_tbl = '''    for row in range(0, 105, 10):
        vals = ", ".join(("true" if i in VALID else "false") for i in range(row, row + 10))
        A("    %s," % vals)'''
new_tbl = '''    for row in range(0, 105, 10):
        n = min(10, 105 - row)
        vals = ", ".join(("true" if i in VALID else "false") for i in range(row, row + n))
        A("    %s," % vals)'''
if old_tbl in s:
    s = s.replace(old_tbl, new_tbl, 1)
    report.append("ok    gen_format_section.py :: validity table has exactly 105 entries")
else:
    report.append("MISS  gen_format_section.py :: validity table pattern")
write(gen, s)

# ------------------------------------------------- 2. regenerate + re-apply
import subprocess
out = BASE + "/format_section.h"
rc = subprocess.run([sys.executable, "-I", gen, "--out", out],
                    capture_output=True, text=True)
if rc.returncode != 0:
    report.append("FAIL  generator: " + rc.stderr.strip()[:200])
else:
    report.append("ok    generator             :: " + rc.stdout.strip())
    p = R + "/include/quant/types.h"
    src = read(p)
    start = src.find("// ============================================================\n// Format enum")
    end = src.find("struct Shape{")
    if start < 0 or end < 0:
        report.append("MISS  types.h              :: region markers not found")
    else:
        new_block = read(out)
        merged = src[:start] + new_block + "\n" + src[end:]
        write(p, merged)
        report.append("ok    types.h              :: corrected section applied")

# ------------------------------------------------- 3. block_codec retired cases
p = R + "/src/codec/block_codec.cpp"
s = read(p)
before = len(s.split("\n"))
drop = [
    "        case Format::Q_16_5: { quant_q16_enhanced(w,n,indices); indices.resize((size_t)std::ceil(16.5*(double)n/8.0),0); return true; }",
    "        case Format::Q_24_5: { quant_q24(w,n,indices); indices.resize((size_t)std::ceil(24.5*(double)n/8.0),0); return true; }",
    "        case Format::Q_G_16_5: { quant_q16_enhanced(w,n,indices); indices.resize((size_t)std::ceil(16.5*(double)n/8.0),0); return true; }",
    "        case Format::Q_G_24_5: { quant_q24(w,n,indices); indices.resize((size_t)std::ceil(24.5*(double)n/8.0),0); return true; }",
]
removed = 0
for d in drop:
    if d in s:
        s = s.replace(d + "\n", "")
        removed += 1
    else:
        report.append("MISS  block_codec.cpp      :: retired case not found: %s" % d[:46])
write(p, s)
report.append("ok    block_codec.cpp       :: %d retired cases removed" % removed)

# the half-BPW block comment above the removed cases
s = read(p)
s = s.replace("        // --- Half BPW plain (Q1.5 etc.) ---\n",
              "        // --- Half-BPW plain formats are RETIRED (ids 73..81) ---\n")
s = s.replace("        // --- Half BPW GRP (Q_G_X_Y) ---\n",
              "        // --- Half-BPW GRP formats are RETIRED (ids 82..90) ---\n")
write(p, s)

# the dequant side has the same four cases
s = read(p)
removed_d = 0
for d in drop:
    dq = d.replace("quant_q16_enhanced(w,n,indices); indices.resize((size_t)std::ceil(16.5*(double)n/8.0),0); return true; }",
                    "dequant_q16_enhanced(indices,idx_bytes,n,out); return; }")
    dq = dq.replace("quant_q24(w,n,indices); indices.resize((size_t)std::ceil(24.5*(double)n/8.0),0); return true; }",
                    "dequant_q24(indices,idx_bytes,n,out); return; }")
    if dq in s:
        s = s.replace(dq + "\n", "")
        removed_d += 1
write(p, s)
report.append("ok    block_codec.cpp       :: %d retired dequant cases removed" % removed_d)

# ------------------------------------------------- 4. the eight test patches
p = R + "/tests/test_all.cpp"
sub(p, "    for (int i = 0; i < quant::FORMAT_COUNT; i++) {\n"
       "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
       "        if (!(quant::format_bpw(fmt) > 0.0f && quant::format_name(fmt) != nullptr)) {",
    "    int live_formats = 0;\n"
    "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {\n"
    "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
    "        if (!quant::format_is_valid(fmt)) continue;\n"
    "        ++live_formats;\n"
    "        if (!(quant::format_bpw(fmt) > 0.0f && quant::format_name(fmt) != nullptr)) {",
    "valid id iteration")
sub(p, "        }\n    }\n    std::cout << \"  -> PASSED: All 69 live formats verified",
    "        }\n    }\n    SYS_CHECK(live_formats == quant::FORMAT_COUNT, \"live format count matches FORMAT_COUNT\");\n"
    "    std::cout << \"  -> PASSED: All 69 live formats verified",
    "live count assertion")

p = R + "/tests/test_format_audit.cpp"
sub(p, "    for (int id = 0; id < FORMAT_COUNT; ++id) {\n"
       "        const Format f = static_cast@L@Format@G@(id);\n"
       "        std::vector@L@uint8_t@G@ idx, cb;",
    "    for (int id = 0; id < FORMAT_ID_SLOTS; ++id) {\n"
    "        const Format f = static_cast@L@Format@G@(id);\n"
    "        if (!format_is_valid(f)) continue;   // retired ids are not encodable\n"
    "        std::vector@L@uint8_t@G@ idx, cb;",
    "audit iterates live ids")

p = R + "/tests/test_fuzz_codec.cpp"
sub(p, "// Enumerate every supported codec format from the registry. v4: all 105\n"
       "// slots 0..104 are defined (no gaps; slot 19 = Q4_K_L).",
    "// Enumerate every LIVE codec format (Operation Clean ladder: 69 live ids\n"
    "// inside a 105-slot id space; the 36 retired ids are not encodable).",
    "fuzz header comment")
sub(p, "    for (int v = 0; v < quant::FORMAT_COUNT; ++v) {\n"
       "        const auto f = static_cast@L@quant::Format@G@(v);\n"
       "        require(quant::format_bpw(f) > 0.0f,\n"
       "                std::string(\"registry gap: format_bpw==0 for id \") + std::to_string(v));",
    "    for (int v = 0; v < quant::FORMAT_ID_SLOTS; ++v) {\n"
    "        const auto f = static_cast@L@quant::Format@G@(v);\n"
    "        if (!quant::format_is_valid(f)) continue;   // retired ids are not encodable\n"
    "        require(quant::format_bpw(f) > 0.0f,\n"
    "                std::string(\"live format with zero BPW at id \") + std::to_string(v));",
    "fuzz enumerates live ids")
sub(p, '"expected 105 supported formats, got " + std::to_string(formats.size()));\n'
       '    std::printf("All 105 enum slots 0..104 defined, no gaps\\n");',
    '"expected 69 live formats, got " + std::to_string(formats.size()));\n'
    '    std::printf("%d live formats in a %d-slot id space (36 retired)\\n",\n'
    '                kFormats, quant::FORMAT_ID_SLOTS);',
    "formats.size() message")

p = R + "/tests/test_format.cpp"
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
       "    for (int i = 0; i < quant::FORMAT_COUNT; i++) {\n"
       "        auto fmt = static_cast@L@quant::Format@G@(i);",
    "    int valid = 0;\n"
    "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {\n"
    "        auto fmt = static_cast@L@quant::Format@G@(i);\n"
    "        if (!quant::format_is_valid(fmt)) continue;",
    "registry iteration")

for line in report:
    print(line)
misses = [l for l in report if l.startswith("MISS") or l.startswith("FAIL")]
print("\n%d actions, %d misses" % (len(report), len(misses)))