#!/usr/bin/env python3
"""Live fact extraction for the Fusion documentation programme (D-31).

Every number the README/book generators print comes from this module.  Nothing is
typed by hand.  Run directly to refresh ``facts.json``:

    python .plan/telemetry/docgen/facts.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PLAN = os.path.join(WS, ".plan")
TR = os.path.join(WS, "transformers")
CD = os.path.join(WS, "code")
OUT = os.path.join(os.path.dirname(__file__), "facts.json")

SKIP_DIRS = {".git", "node_modules", "build", "build-norm", "build-gate", "build-eng2",
             ".venv", "__pycache__", ".cache", "SOURCE", "dist", "out"}


def read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def nlines(path: str) -> int:
    try:
        with open(path, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def run(cmd: list[str], cwd: str) -> str:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        return (p.stdout + p.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return str(e)


TEXT_EXTS = {".cpp", ".h", ".hpp", ".c", ".cu", ".py", ".md", ".json", ".mjs",
             ".js", ".ts", ".tsx", ".sh", ".ps1", ".bat", ".cmake", ".txt", ".xml",
             ".yml", ".yaml", ".toml", ".css", ".html", ".svg"}


def walk_stats(root: str, exts: tuple[str, ...] | None = None,
               max_depth: int | None = None, loc: bool = True) -> dict:
    """Count files / lines / bytes under *root*, skipping generated trees."""
    files = 0
    line_count = 0
    size = 0
    by_ext: dict[str, int] = {}
    base_depth = root.rstrip(os.sep).count(os.sep)
    for cur, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if max_depth is not None and cur.count(os.sep) - base_depth >= max_depth:
            dirs[:] = []
        for n in names:
            p = os.path.join(cur, n)
            ext = os.path.splitext(n)[1].lower()
            if exts and ext not in exts:
                continue
            try:
                st = os.stat(p)
            except OSError:
                continue
            files += 1
            size += st.st_size
            by_ext[ext] = by_ext.get(ext, 0) + 1
            if loc and ext in TEXT_EXTS:
                line_count += nlines(p)
    return {"files": files, "loc": line_count, "bytes": size, "by_ext": by_ext}


def tracked_stats(root: str, repo: str, prefix: str = "") -> dict:
    """Fast stats from ``git ls-files`` (tracked files only)."""
    cmd = ["git", "ls-files", "-z"]
    if prefix:
        cmd += ["--", prefix]
    out = run(cmd, repo)
    names = [n for n in out.replace("\r", "").split("\0") if n]
    files = 0
    size = 0
    line_count = 0
    by_ext: dict[str, int] = {}
    for rel in names:
        p = os.path.join(root, rel.replace("/", os.sep))
        try:
            st = os.stat(p)
        except OSError:
            continue
        files += 1
        size += st.st_size
        ext = os.path.splitext(rel)[1].lower()
        by_ext[ext] = by_ext.get(ext, 0) + 1
    return {"files": files, "loc": line_count, "bytes": size, "by_ext": by_ext}


# ------------------------------------------------------------------ .plan facts
def parse_decisions() -> list[dict]:
    txt = read(os.path.join(PLAN, "docs", "operation-clean", "DECISIONS.md"))
    parts = re.split(r"^## (D-\d+)\s*·\s*(.*)$", txt, flags=re.M)
    out = []
    for i in range(1, len(parts), 3):
        did, title, body = parts[i], parts[i + 1].strip(), parts[i + 2]
        clean = []
        for line in body.splitlines():
            s = line.strip()
            if not s or s == "---" or s.startswith("## "):
                continue
            clean.append(s)
        out.append({"id": did, "title": title, "body": clean,
                    "chars": len(" ".join(clean))})
    return out


def parse_research() -> list[dict]:
    txt = read(os.path.join(PLAN, "RESEARCH-INDEX.md"))
    parts = re.split(r"^### (R-\d+)\s*·\s*(.*)$", txt, flags=re.M)
    out = []
    for i in range(1, len(parts), 3):
        rid, title, body = parts[i], parts[i + 1].strip(), parts[i + 2]
        clean = [l.strip() for l in body.splitlines()
                 if l.strip() and not l.strip().startswith("---")
                 and not l.strip().startswith("#")]
        out.append({"id": rid, "title": title, "body": clean,
                    "chars": len(" ".join(clean))})
    return out


def parse_todo() -> dict:
    txt = read(os.path.join(PLAN, "telemetry", "TODO-TREE.md"))
    items = re.findall(r"^- \[( |x)\] (T\d+(?:\.\d+)?)\s+\*\*(.*?)\*\*", txt, flags=re.M)
    done = sum(1 for s, *_ in items if s == "x")
    return {"total": len(items), "done": done,
            "items": [{"state": s, "id": i, "title": t} for s, i, t in items]}


def parse_doc_inventory() -> list[dict]:
    rows = []
    for name in sorted(os.listdir(PLAN)):
        p = os.path.join(PLAN, name)
        if os.path.isfile(p) and name.endswith(".md"):
            rows.append({"file": f".plan/{name}", "lines": nlines(p),
                         "bytes": os.path.getsize(p)})
    for sub in ("docs/operation-clean", "telemetry", "review-tracking"):
        d = os.path.join(PLAN, *sub.split("/"))
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if os.path.isfile(p) and name.endswith(".md"):
                rows.append({"file": f".plan/{sub}/{name}", "lines": nlines(p),
                             "bytes": os.path.getsize(p)})
    return rows


# --------------------------------------------------------- transformers facts
def parse_formats() -> tuple[list[dict], list[dict]]:
    txt = read(os.path.join(TR, "include", "quant", "types.h"))
    enum = re.search(r"enum class Format\s*:\s*uint8_t\s*\{(.*?)\n\};", txt, re.S)
    valid, retired = [], []
    if not enum:
        return valid, retired
    in_retired = False
    for line in enum.group(1).splitlines():
        if "Retired ids" in line:
            in_retired = True
        cm = re.search(r"//\s*(.*)$", line)
        comment = cm.group(1).strip() if cm else ""
        for m in re.finditer(r"\b(Q_[A-Za-z0-9_]+)\s*=\s*(\d+)", line):
            name, fid = m.group(1), int(m.group(2))
            rec = {"name": name, "id": fid, "comment": comment}
            (retired if in_retired else valid).append(rec)
    # BPW from the comment, then from the canonical name.
    def bpw(name: str, comment: str) -> float:
        m = re.search(r"(\d+(?:\.\d+)?)", comment)
        if m:
            return float(m.group(1))
        if "_MX_" in name:
            return float(name.rsplit("_", 2)[-2] + "." + name.rsplit("_", 1)[-1])
        m = re.match(r"Q_G?_(\d+)", name)
        base = float(m.group(1)) if m else 0.0
        if name.endswith("_K_M"):
            return base + 0.25
        if name.endswith("_K_H"):
            return base + 0.50
        return base
    for rec in valid + retired:
        rec["bpw"] = bpw(rec["name"], rec["comment"])
        rec["family"] = "GRP" if "_G_" in rec["name"] else ("MX" if "_MX_" in rec["name"] else "plain")
    return valid, retired


def parse_registry() -> list[dict]:
    txt = read(os.path.join(TR, "src", "codec", "format_registry.cpp"))
    out = []
    for line in txt.splitlines():
        m = re.search(r'v\.push_back\(\{"(Q_[A-Za-z0-9_]+)".*?"([^"]*)"\}\);', line)
        if not m:
            continue
        out.append({"name": m.group(1), "description": m.group(2)})
    return out


def parse_tests() -> list[dict]:
    d = os.path.join(TR, "tests")
    out = []
    for name in sorted(os.listdir(d)):
        if not name.endswith(".cpp"):
            continue
        p = os.path.join(d, name)
        txt = read(p)
        cases = re.findall(r"\bvoid\s+(test_[A-Za-z0-9_]+)\s*\(", txt)
        cases += re.findall(r"\bTEST\s*\(\s*([^)]+)\)", txt)
        asserts = len(re.findall(r"\bassert\s*\(", txt))
        out.append({"file": name, "lines": nlines(p), "cases": sorted(set(cases)),
                    "asserts": asserts})
    return out


def parse_cmake() -> tuple[list[str], list[str]]:
    txt = read(os.path.join(TR, "CMakeLists.txt"))
    targets = sorted(set(re.findall(r"add_executable\s*\(\s*([A-Za-z0-9_]+)", txt)))
    libs = sorted(set(re.findall(r"add_library\s*\(\s*([A-Za-z0-9_]+)", txt)))
    return targets, libs


def parse_backends() -> list[str]:
    txt = read(os.path.join(TR, "include", "quant", "backend.h"))
    m = re.search(r"enum class BackendType[^{]*\{(.*?)\}", txt, re.S)
    if not m:
        return []
    return [v.strip().split("=")[0].strip() for v in m.group(1).split(",")
            if v.strip() and not v.strip().startswith("//")]


def parse_spec() -> dict:
    p = os.path.join(TR, "SPEC-INFERNO.md")
    txt = read(p)
    heads = re.findall(r"^(#{1,3})\s+(.*)$", txt, re.M)
    return {"lines": nlines(p), "headings": [h[1] for h in heads]}


def transformers_facts() -> dict:
    src_tree = []
    src = os.path.join(TR, "src")
    for d in sorted(os.listdir(src)):
        p = os.path.join(src, d)
        if os.path.isdir(p):
            st = walk_stats(p, exts=(".cpp", ".h", ".cu"))
            src_tree.append({"dir": d, **st})
    tests = parse_tests()
    valid, retired = parse_formats()
    registry = parse_registry()
    targets, libs = parse_cmake()
    return {
        "stats": walk_stats(TR, exts=(".cpp", ".h", ".cu", ".py", ".md", ".sh", ".ps1",
                                      ".bat", ".json", ".cmake", ".txt")),
        "git": {"head": run(["git", "log", "--oneline", "-1"], TR),
                "commits": run(["git", "rev-list", "--count", "HEAD"], TR),
                "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"], TR)},
        "src_tree": src_tree,
        "tests": tests,
        "formats_valid": valid,
        "formats_retired": retired,
        "registry": registry,
        "targets": targets,
        "libs": libs,
        "backends": parse_backends(),
        "spec": parse_spec(),
    }


# --------------------------------------------------------------- code facts
def top_entries(folder: str, limit: int = 24) -> list[dict]:
    out = []
    if not os.path.isdir(folder):
        return out
    for name in sorted(os.listdir(folder))[:limit]:
        p = os.path.join(folder, name)
        try:
            st = os.stat(p)
            out.append({"name": name, "dir": os.path.isdir(p), "bytes": st.st_size})
        except OSError:
            out.append({"name": name, "dir": os.path.isdir(p), "bytes": 0})
    return out


def code_facts() -> dict:
    reg = json.loads(read(os.path.join(CD, "arch", "windows.json")))
    layouts = json.loads(read(os.path.join(CD, "arch", "layouts.json")))
    seats = []
    for part in reg.get("parts", []):
        folder = os.path.join(CD, part["folder"].replace("/", os.sep))
        seats.append({**part, "top": top_entries(folder),
                      "exists": os.path.isdir(folder)})
    extra = []
    for name in ("merger", "vs-ext"):
        folder = os.path.join(CD, "windows", name)
        extra.append({"codename": name.title(), "alias": None,
                      "folder": f"windows/{name}", "status": "present" if os.path.isdir(folder) else "missing",
                      "contents": "Reserved support folder; not a launcher part.",
                      "top": top_entries(folder), "exists": os.path.isdir(folder)})
    launcher = tracked_stats(CD, CD, "launcher/")
    scripts = tracked_stats(CD, CD, "scripts/")
    payloads = tracked_stats(CD, CD, "payloads/")
    return {
        "registry": reg,
        "layouts": layouts,
        "brand": read(os.path.join(CD, "BRAND.md")),
        "seats": seats + extra,
        "launcher": launcher,
        "scripts": scripts,
        "payloads": payloads,
        "stats": tracked_stats(CD, CD),
        "git": {"head": run(["git", "log", "--oneline", "-1"], CD),
                "commits": run(["git", "rev-list", "--count", "HEAD"], CD),
                "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"], CD)},
    }


# --------------------------------------------------------------- fusion facts
def fusion_facts() -> dict:
    plan_stats = walk_stats(os.path.join(PLAN, "docs"), exts=(".md",))
    for sub in ("telemetry",):
        st = walk_stats(os.path.join(PLAN, sub), exts=(".md", ".py"))
        for k in ("files", "loc", "bytes"):
            plan_stats[k] += st[k]
        for ext, n in st["by_ext"].items():
            plan_stats["by_ext"][ext] = plan_stats["by_ext"].get(ext, 0) + n
    return {
        "stats": plan_stats,
        "git": {"head": run(["git", "log", "--oneline", "-1"], WS),
                "commits": run(["git", "rev-list", "--count", "HEAD"], WS),
                "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"], WS)},
        "submodules": run(["git", "submodule", "status"], WS),
        "decisions": parse_decisions(),
        "research": parse_research(),
        "todo": parse_todo(),
        "doc_inventory": parse_doc_inventory(),
    }


def extract() -> dict:
    data = {"generated": "live", "workspace": WS,
            "fusion": fusion_facts(),
            "transformers": transformers_facts(),
            "code": code_facts()}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    return data


if __name__ == "__main__":
    d = extract()
    f = d["fusion"]
    print(f"wrote {OUT}")
    print(f"decisions={len(f['decisions'])} research={len(f['research'])} "
          f"todo={f['todo']['done']}/{f['todo']['total']} docs={len(f['doc_inventory'])}")
    print(f"formats={len(d['transformers']['formats_valid'])} "
          f"retired={len(d['transformers']['formats_retired'])} "
          f"tests={len(d['transformers']['tests'])} "
          f"targets={len(d['transformers']['targets'])} libs={len(d['transformers']['libs'])}")
    print(f"seats={len(d['code']['seats'])} code_files={d['code']['stats']['files']:,}")
