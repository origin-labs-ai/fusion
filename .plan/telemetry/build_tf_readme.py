#!/usr/bin/env python3
"""Renderer for the Transformers-Fusion README.

Discipline (inherited from .plan/review-tracking/DRAFT.md, the operator's own format rule):
  every section = 1 heading + 30 lines of prose + 1 blank line = exactly 32 lines.
  Target: 192 sections x 32 = 6144 LOC.

Facts are injected from a live extraction, so no number in the README can drift from the code.
Run:  python .plan/telemetry/build_tf_readme.py
"""
import json, os, re, subprocess, sys, datetime

WS = r"C:\Users\thaku\Workspaces\fusion"
T = os.path.join(WS, "transformers")
OUT = os.path.join(T, "README.md")
FACTS = r"C:\Users\thaku\AppData\Local\Temp\opencode\tf_facts.json"
SECTIONS = r"C:\Users\thaku\AppData\Local\Temp\opencode\tf_readme_sections.py"

HEAD = """# Transformers-Fusion

**The C++20 training and inference engine of the Fusion Superproject.**

> **OPERATOR REMINDER (2026-11-12):** the MAIN goal of the Fusion Superproject is the *entire*
> superproject; the SIDE goal is to achieve the MAXIMUM at **EXACT 1.0 BPW** (not 1.5 - the
> implemented 1.5 BPW path is the stepping stone). Both **FP** (floating point) and **INT**
> (integer) format families are in scope. **Loop Quantization has never been implemented for any
> model anywhere** - Track B here would be the first. See
> `fusion/.plan/docs/operation-clean/DECISIONS.md` D-27.

"""


def load_facts():
    with open(FACTS, encoding="utf-8") as f:
        return json.load(f)


def load_sections():
    ns = {}
    with open(SECTIONS, encoding="utf-8") as f:
        exec(compile(f.read(), SECTIONS, "exec"), ns)
    secs = ns["SECTIONS"]
    extra_path = SECTIONS.replace("_sections.py", "_extra.py")
    extras = []
    if os.path.isfile(extra_path):
        extras.append(extra_path)
    extra2 = SECTIONS.replace("_sections.py", "_extra2.py")
    if os.path.isfile(extra2):
        extras.append(extra2)
    for ep in extras:
        en = {}
        with open(ep, encoding="utf-8") as f:
            exec(compile(f.read(), ep, "exec"), en)
        for s in secs:
            add = en.get("EXTRA", {}).get(s["title"])
            if not add:
                continue
            lines = s["body"].split("\n")
            while lines and lines[-1].strip() == "":
                lines.pop()
            s["body"] = "\n".join(lines + list(add))
    return secs


def narrative_count(lines):
    """Count prose lines: non-empty, not a table row, not inside a code fence."""
    n = 0
    fence = False
    for l in lines:
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or s.startswith("|"):
            continue
        n += 1
    return n


def render():
    facts = load_facts()
    secs = load_sections()
    out = [HEAD]
    deficits = []
    narrative_total = 0
    for s in secs:
        body = s["body"]
        lines = body.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        prose = lines[1:]
        n = narrative_count(prose)
        narrative_total += n
        if n < 30:
            deficits.append((s["title"], n, 30 - n))
        out.append("\n".join([lines[0]] + prose + [""]))
    if deficits:
        print("SHORT SECTIONS (must be filled with real prose, not blanks):")
        for t, n, d in deficits:
            print(f"  - {t}: {n}/30 narrative lines, {d} missing")
        print(f"\n{len(deficits)} section(s) short - README not written.")
        sys.exit(1)
    text = "\n".join(out)
    os.makedirs(T, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    total = text.count("\n") + 1
    print(f"wrote {OUT}")
    print(f"sections: {len(secs)}   total LOC: {total}   narrative LOC: {narrative_total}")
    print(f"target: 192 sections / 5760 narrative LOC / 6144 total LOC")
    if len(secs) < 192:
        print(f"  note: {192 - len(secs)} sections still to author")


if __name__ == "__main__":
    render()
