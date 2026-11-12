"""L1 fix pass C: generator repair, types.h re-apply, line-anchored test
patches, and a block_codec integrity check.

The earlier string-match patches missed because the patterns drifted from the
files; everything here is anchored on unique line content instead.

Run: python -I fix_l1c.py
"""
import os
import re
import subprocess
import sys

BASE = r"C:/Users/thaku/Workspaces/fusion/review-tracking/l1"
R = r"C:/Users/thaku/Workspaces/fusion/transformers"

report = []


def C(s):
    return s.replace("@L@", chr(60)).replace("@G@", chr(62))


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n")


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def find(lines, needle, start=0):
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    return -1


def patch_lines(path, ops, label):
    lines = read(path).split("\n")
    for op in ops:
        kind = op[0]
        if kind == "replace":
            _, anchor, new = op
            i = find(lines, anchor)
            if i < 0:
                report.append("MISS  %-26s :: %s (anchor: %s)" %
                              (os.path.basename(path), label, anchor[:40]))
                continue
            lines[i:i + 1] = new
        elif kind == "insert_after":
            _, anchor, new = op
            i = find(lines, anchor)
            if i < 0:
                report.append("MISS  %-26s :: %s (anchor: %s)" %
                              (os.path.basename(path), label, anchor[:40]))
                continue
            lines[i + 1:i + 1] = new
        elif kind == "insert_before":
            _, anchor, new = op
            i = find(lines, anchor)
            if i < 0:
                report.append("MISS  %-26s :: %s (anchor: %s)" %
                              (os.path.basename(path), label, anchor[:40]))
                continue
            lines[i:i] = new
        elif kind == "replace_block":
            _, a0, a1, new = op
            i = find(lines, a0)
            if i < 0:
                report.append("MISS  %-26s :: %s (start anchor)" %
                              (os.path.basename(path), label))
                continue
            j = find(lines, a1, i + 1)
            if j < 0:
                report.append("MISS  %-26s :: %s (end anchor)" %
                              (os.path.basename(path), label))
                continue
            lines[i:j + 1] = new
    write(path, "\n".join(lines))
    report.append("ok    %-26s :: %s" % (os.path.basename(path), label))


# ------------------------------------------------- 1. generator repair
gen = BASE + "/gen_format_section.py"
s = read(gen)
old = s
s = re.sub(
    r'def bpw_str\(v\):\n(?:[ \t].*\n)+?\n',
    'def bpw_str(v):\n'
    '    # Always keep a decimal point: "1" would emit the invalid literal "1f".\n'
    '    t = ("%.5f" % v).rstrip("0")\n'
    '    if t.endswith("."):\n'
    '        t += "0"\n'
    '    return t\n\n',
    s, count=1)
report.append("ok    gen_format_section.py :: bpw_str" if s != old else
              "MISS  gen_format_section.py :: bpw_str")
old = s
s = re.sub(
    r'    for row in range\(0, 105, 10\):\n'
    r'[ \t]*vals = ", "\.join\(\("true" if i in VALID else "false"\) for i in range\(row, row \+ 10\)\)\n'
    r'[ \t]*A\("    %s," % vals\)\n',
    '    for row in range(0, 105, 10):\n'
    '        n = min(10, 105 - row)\n'
    '        vals = ", ".join(("true" if i in VALID else "false") for i in range(row, row + n))\n'
    '        A("    %s," % vals)\n',
    s, count=1)
report.append("ok    gen_format_section.py :: validity table 105" if s != old else
              "MISS  gen_format_section.py :: validity table")
write(gen, s)

# ------------------------------------------------- 2. regenerate + apply
out = BASE + "/format_section.h"
rc = subprocess.run([sys.executable, "-I", gen, "--out", out], capture_output=True, text=True)
if rc.returncode != 0:
    report.append("FAIL  generator: " + rc.stderr.strip()[:300])
else:
    report.append("ok    generator             :: " + rc.stdout.strip())
    p = R + "/include/quant/types.h"
    src = read(p)
    start = src.find("// ============================================================\n// Format enum")
    end = src.find("struct Shape{")
    if start < 0 or end < 0:
        report.append("MISS  types.h              :: region markers")
    else:
        block = read(out)
        write(p, src[:start] + block + "\n" + src[end:])
        report.append("ok    types.h              :: section applied")

# ------------------------------------------------- 3. block_codec integrity
p = R + "/src/codec/block_codec.cpp"
s = read(p)
RET = ["Q_1_K_L", "Q_2_K_L", "Q_3_K_L", "Q_4_K_L", "Q_6_K_L", "Q_8_K_L", "Q_12_K_L",
       "Q_16_K_L", "Q_24_K_L", "Q_G_1_K_L", "Q_G_2_K_L", "Q_G_3_K_L", "Q_G_4_K_L",
       "Q_G_6_K_L", "Q_G_8_K_L", "Q_G_12_K_L", "Q_G_16_K_L", "Q_G_24_K_L",
       "Q_1_5", "Q_2_5", "Q_3_5", "Q_4_5", "Q_6_5", "Q_8_5", "Q_12_5", "Q_16_5",
       "Q_24_5", "Q_G_1_5", "Q_G_2_5", "Q_G_3_5", "Q_G_4_5", "Q_G_6_5", "Q_G_8_5",
       "Q_G_12_5", "Q_G_16_5", "Q_G_24_5"]
left = []
for name in RET:
    if re.search(r"case Format::%s:" % name, s):
        left.append(name)
if left:
    for name in left:
        s = re.sub(r"^[ \t]*case Format::%s:[^\n]*\n" % name, "", s, flags=re.M)
    report.append("ok    block_codec.cpp       :: removed %d leftover retired cases" % len(left))
else:
    report.append("ok    block_codec.cpp       :: no retired cases remain")
write(p, s)

# brace balance sanity: count braces in the file
opens = s.count("{")
closes = s.count("}")
report.append("ok    block_codec.cpp       :: braces %d/%d %s"
              % (opens, closes, "balanced" if opens == closes else "UNBALANCED"))

# ------------------------------------------------- 4. line-anchored test patches
L = "static_cast" + chr(60) + "quant::Format" + chr(62) + "(i)"

patch_lines(R + "/tests/test_all.cpp", [
    ("replace", "for (int i = 0; i < quant::FORMAT_COUNT; i++) {",
     ["    int live_formats = 0;",
      "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {"]),
    ("insert_after", "auto fmt = " + L + ";",
     ["        if (!quant::format_is_valid(fmt)) continue;",
      "        ++live_formats;"]),
    ("insert_before", 'std::cout << "  -> PASSED: All 69 live formats verified',
     ['    SYS_CHECK(live_formats == quant::FORMAT_COUNT, '
      '"live format count matches FORMAT_COUNT");']),
], "live id iteration + count assertion")

patch_lines(R + "/tests/test_format_audit.cpp", [
    ("replace", "for (int id = 0; id < FORMAT_COUNT; ++id) {",
     ["    for (int id = 0; id < FORMAT_ID_SLOTS; ++id) {",
      "        const Format f = static_cast" + chr(60) + "Format" + chr(62) + "(id);",
      "        if (!format_is_valid(f)) continue;   // retired ids are not encodable"]),
    ("replace", "        const Format f = static_cast" + chr(60) + "Format" + chr(62) + "(id);",
     ["        // (already bound above)"]),
], "audit iterates live ids")

patch_lines(R + "/tests/test_fuzz_codec.cpp", [
    ("replace", "// slots 0..104 are defined (no gaps; slot 19 = Q4_K_L).",
     ["// inside a 105-slot id space; the 36 retired ids are not encodable)."]),
    ("replace", "// Enumerate every supported codec format from the registry. v4: all 105",
     ["// Enumerate every LIVE codec format (Operation Clean ladder: 69 live ids"]),
    ("replace", "for (int v = 0; v < quant::FORMAT_COUNT; ++v) {",
     ["    for (int v = 0; v < quant::FORMAT_ID_SLOTS; ++v) {"]),
    ("insert_before", "require(quant::format_bpw(f) > 0.0f,",
     ["        if (!quant::format_is_valid(f)) continue;   // retired ids are not encodable"]),
    ("replace", '"expected 105 supported formats, got " + std::to_string(formats.size()));',
     ['"expected 69 live formats, got " + std::to_string(formats.size()));']),
    ("replace", 'std::printf("All 105 enum slots 0..104 defined, no gaps\\n");',
     ['std::printf("%d live formats in a %d-slot id space (36 retired)\\n",',
      "                kFormats, quant::FORMAT_ID_SLOTS);"]),
], "fuzz enumerates live ids")

patch_lines(R + "/tests/test_format.cpp", [
    ("replace_block",
     "// Verify half-BPW plain variants (Q1.5..Q24.5 at enum 73..81)",
     "        assert(quant::format_bpw(fmt) > 0.0f);",
     ["    // Verify the GRP M/H tiers (enum 47..72; every third id is a retired",
      "    // K_L hole): grouped, not base, and carrying a real BPW.",
      "    for (int i = 47; i <= 72; i++) {",
      "        if (!quant::format_is_valid(static_cast" + chr(60) + "quant::Format" + chr(62) + "(i))) continue;",
      "        auto fmt = static_cast" + chr(60) + "quant::Format" + chr(62) + "(i);",
      "        assert(quant::format_is_grp(fmt));",
      "        assert(!quant::format_is_base(fmt));",
      "        assert(quant::format_bpw(fmt) > 0.0f);",
      "    }",
      "    // Retired ids are never valid and never carry a BPW.",
      "    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {",
      "        auto fmt = static_cast" + chr(60) + "quant::Format" + chr(62) + "(i);",
      "        if (quant::format_is_valid(fmt)) continue;",
      "        assert(quant::format_bpw(fmt) == 0.0f);",
      "    }"]),
    ("replace", "for (int i = 0; i < quant::FORMAT_COUNT; i++) {",
     ["    for (int i = 0; i < quant::FORMAT_ID_SLOTS; i++) {"]),
    ("insert_after", "auto fmt = static_cast" + chr(60) + "quant::Format" + chr(62) + "(i);",
     ["        if (!quant::format_is_valid(fmt)) continue;"]),
], "GRP tiers + retired check + registry iteration")

for line in report:
    print(line)
misses = [l for l in report if l.startswith("MISS") or l.startswith("FAIL")]
print("\n%d actions, %d misses" % (len(report), len(misses)))