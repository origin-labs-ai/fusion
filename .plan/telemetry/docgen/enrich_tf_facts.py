#!/usr/bin/env python3
"""Enrich facts.json into the exact shape build_tf_readme.py consumes."""
from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TR = os.path.join(WS, "transformers")

f = json.load(open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
T = f["transformers"]


def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def nlines(p):
    try:
        with open(p, "rb") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


# ---------------------------------------------------------------- cmake blocks
cm = read(os.path.join(TR, "CMakeLists.txt"))


def blocks(kind: str) -> dict[str, list[str]]:
    out = {}
    for m in re.finditer(rf"add_{kind}\s*\(\s*([A-Za-z0-9_]+)(.*?)\)", cm, re.S):
        name, rest = m.group(1), m.group(2)
        srcs = [s for s in re.findall(r"[A-Za-z0-9_./+-]+\.(?:cpp|h|cu|hpp)", rest)]
        out[name] = srcs
    return out


lib_blocks = blocks("library")
exe_blocks = blocks("executable")

# --------------------------------------------------------------- format refs
src_files: list[str] = []
for root in ("src", "include", "tests"):
    base = os.path.join(TR, root)
    for cur, dirs, names in os.walk(base):
        dirs[:] = [d for d in dirs if d not in {".git", "build"}]
        for n in names:
            if n.endswith((".cpp", ".h", ".cu")):
                src_files.append(os.path.join(cur, n))

texts = {}
for p in src_files:
    texts[p] = read(p)

for rec in T["formats_valid"]:
    name = rec["name"]
    pat = re.compile(rf"\b{re.escape(name)}\b")
    hits = [p for p, t in texts.items() if pat.search(t)]
    test_hits = [os.path.basename(p) for p in hits if os.sep + "tests" + os.sep in p]
    rec["refs"] = len(hits)
    rec["tests"] = sorted(set(test_hits))[:4]
    rec["family"] = "MX" if "_MX_" in name else ("GRP" if "_G_" in name else "plain")

desc = {r["name"]: r["description"] for r in T["registry"]}
for rec in T["formats_valid"]:
    rec["description"] = desc.get(rec["name"], "")

# ---------------------------------------------------------------- lib sources
for lib in T["libs"]:
    srcs = lib_blocks.get(lib, [])
    T.setdefault("lib_sources", {})[lib] = srcs[:12]
for tgt in T["targets"]:
    T.setdefault("target_sources", {})[tgt] = exe_blocks.get(tgt, [])[:12]

# ------------------------------------------------------------ key files/dirs
def key_files(folder: str, limit: int = 6) -> list[dict]:
    base = os.path.join(TR, folder)
    rows = []
    for cur, dirs, names in os.walk(base):
        dirs[:] = [d for d in dirs if d not in {"build", ".git"}]
        for n in names:
            if n.endswith((".cpp", ".h", ".cu")):
                p = os.path.join(cur, n)
                rows.append({"path": os.path.relpath(p, TR).replace("\\", "/"),
                             "lines": nlines(p)})
    rows.sort(key=lambda r: (-r["lines"], r["path"]))
    return rows[:limit]


for d in T["src_tree"]:
    d["key"] = key_files("src/" + d["dir"], 5)

engines = []
eng_root = os.path.join(TR, "engines")
for name in sorted(os.listdir(eng_root)):
    p = os.path.join(eng_root, name)
    if not os.path.isdir(p):
        continue
    files = []
    for cur, dirs, names in os.walk(p):
        dirs[:] = [x for x in dirs if x not in {"build", ".git"}]
        for n in names:
            if n.endswith((".cpp", ".h", ".cu")):
                files.append(os.path.join(cur, n))
    engines.append({"dir": name, "files": len(files),
                    "loc": sum(nlines(x) for x in files),
                    "key": key_files("engines/" + name, 5)})
T["engines"] = engines

# ------------------------------------------------------------------ registry
T["backends"] = T["backends"]

out = {
    "src_tree": [(d["dir"], d["files"], d["loc"]) for d in T["src_tree"]],
    "src_detail": T["src_tree"],
    "format_names": [r["name"] for r in T["formats_valid"]],
    "formats": T["formats_valid"],
    "retired": T["formats_retired"],
    "backends": T["backends"],
    "cmake_targets": T["targets"],
    "cmake_libs": T["libs"],
    "lib_sources": T["lib_sources"],
    "target_sources": T["target_sources"],
    "tests": [t["file"] for t in T["tests"]],
    "test_detail": T["tests"],
    "engines": [(e["dir"], e["files"]) for e in engines],
    "engine_detail": engines,
    "FORMAT_COUNT": "69",
    "FORMAT_ID_SLOTS": "105",
    "git": T["git"],
    "stats": T["stats"],
    "spec": T["spec"],
}

with open(os.path.join(HERE, "tf_facts.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)

print(f"formats={len(out['formats'])} libs={len(out['cmake_libs'])} "
      f"targets={len(out['cmake_targets'])} engines={len(out['engines'])} "
      f"src={len(out['src_tree'])}")
