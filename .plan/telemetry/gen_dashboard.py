#!/usr/bin/env python3
"""Fusion Superproject telemetry - regenerates .plan/telemetry/DASHBOARD.md from LIVE state.

Run after every step:  python .plan/telemetry/gen_dashboard.py
Captures: 7 plan verifiers (live run + exit codes), code gate, git status of both repos,
Phase-0 ledger counts, domain coverage (from the 2026-11-12 audit), parked items.
"""
import os, re, subprocess, datetime, sys

WS = r"C:\Users\thaku\Workspaces\fusion"
PLAN = os.path.join(WS, ".plan", "pasted-content-id-43ed-ye-aur-melodic-puddle.md")
OUT = os.path.join(WS, ".plan", "telemetry", "DASHBOARD.md")

VERIFIERS = ["verify_step1.py", "step2_fix2_verify.py", "step3_verify.py",
             "step3_subanchors.py", "verify_step5.py", "step6_audit.py", "arxiv_recheck.py"]

DOMAINS = [
    ("Loop Transformers", "DONE", "5d taxonomy/attention/training + 5e attention-residuals + papers (Loopback/LoopQuant/OASIS/ASTRA/2603.10123) verified 2026-11-10"),
    ("Traditional Transformers", "DONE", "5d same pass - baseline/attention/training comparison + market scan"),
    ("Traditional Quantization (Track A)", "DONE", "69-format ladder contract (LADDER.md), 1.5 BPW path (9b.1), Operation Clean implemented"),
    ("Loop Quantization (Track B)", "RESEARCH-DONE / TRACK-OPEN", "5f+9b.2 evidence read (LoopQ/LoopQuant W4A4); implementation track open; ~4BPW->1.5BPW gap + few-B-param ceiling flagged"),
    ("Mix Quantization", "PARTIAL", "MX family (14 formats) measured + quarantined (D-13, -21..-37 dB); no dedicated mix-strategy literature pass yet"),
    ("DSpine x NCM merger", "RESEARCH-DONE / NCM-READ-OPEN", "3c DSpine full implementable spec (2026-11-09); NCM 3b spec extracted; Appendix F.1.1/I read remaining"),
    ("EAIN", "LIT-DONE / DESIGN-OPEN", "5c.4 literature basis + honest ceiling; OPEN-DESIGN (implementable subset) + OPEN-DECISION (which of 3 stacks)"),
]


def run(cmd, cwd, timeout=300):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout + p.stderr)
    except Exception as e:
        return 99, str(e)


def git_counts(repo):
    code, out = run(["git", "status", "--short"], repo, timeout=60)
    mod = len([l for l in out.splitlines() if l[:2].strip() and not l.startswith("??")])
    untracked = len([l for l in out.splitlines() if l.startswith("??")])
    return mod, untracked


def main():
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    L = ["# Fusion Superproject - Telemetry Dashboard", "",
         "> **GOAL LINE (D-27):** MAIN goal = the ENTIRE Fusion Superproject. SIDE goal = MAXIMUM at "
         "**EXACT 1.0 BPW** (not 1.5 - that path is the stepping stone). FP + INT both research. "
         "Loop Quant never implemented anywhere before - Track B is the first. Details: "
         "`.plan/docs/operation-clean/DECISIONS.md` D-27.", "",
         "> **CONTEXT-RECOVERY (one-shot handoff):** read this file -> `.plan/telemetry/TODO-TREE.md` "
         "-> `.plan/docs/operation-clean/DECISIONS.md` -> OPERATOR REMINDER at the top of the master "
         "plan. Full workflow: `.plan/BLUEPRINT.md`.", "",
         "> Generated: **%s** - regen: `python .plan/telemetry/gen_dashboard.py`" % ts, ""]

    # 0. superproject git (fusion repo itself)
    L += ["## 0. Superproject git (fusion repo)", ""]
    code, out = run(["git", "log", "--oneline", "-1"], WS)
    code2, out2 = run(["git", "status", "--short", "-b"], WS)
    head = out.strip()
    branch = out2.splitlines()[0].strip() if out2.strip() else "?"
    dirty = max(0, len([l for l in out2.splitlines()[1:] if l.strip()]))
    code3, out3 = run(["git", "status", "-sb"], os.path.join(WS, "code"))
    code4, out4 = run(["git", "status", "-sb"], os.path.join(WS, "transformers"))
    L.append("- HEAD: `%s`" % head)
    L.append("- branch: `%s` (dirty entries: %d)" % (branch, dirty))
    L.append("- submodule `code`: %s" % out3.splitlines()[0].strip() if out3.strip() else "- submodule code: ?")
    L.append("- submodule `transformers`: %s" % out4.splitlines()[0].strip() if out4.strip() else "- submodule transformers: ?")
    L.append("- push: NOT ordered yet (hold)", )
    L.append("")

    # 1. verifiers (live)
    L += ["## 1. Plan verifiers (live run)", "", "| Verifier | Exit | Verdict |", "|---|---|---|"]
    all_ok = True
    for v in VERIFIERS:
        code, out = run([sys.executable, v], os.path.join(WS, ".plan", ".rea-tmp"))
        verdict = "**PASS**" if code == 0 else "**FAIL**"
        if code != 0:
            all_ok = False
        tail = [l for l in out.splitlines() if l.strip()]
        tail = tail[-1][:70] if tail else ""
        L.append("| `%s` | %d | %s %s |" % (v, code, verdict, tail))
    L += ["", "**Gate: %s**" % ("ALL GREEN" if all_ok else "RED"), ""]

    # 2. code gate
    L += ["## 2. Code repo gate", ""]
    code, out = run(["node", r"scripts\rebrand\check-consistency.mjs"], os.path.join(WS, "code"))
    m = re.search(r"(\d+)/(\d+) checks passed", out)
    L.append("check-consistency: exit=%d %s" % (code, ("**" + m.group(0) + "**") if m else out[-80:]))
    L.append("")

    # 3. git
    L += ["## 3. Repos (working tree)", "", "| Repo | Modified | Untracked | Remote |", "|---|---|---|---|"]
    for name, remote in [("code", "origin-labs-ai/code.git"), ("transformers", "origin-labs-ai/transformers.git")]:
        mod, un = git_counts(os.path.join(WS, name))
        L.append("| `%s` | %d | %d | `%s` |" % (name, mod, un, remote))
    L += ["", "> Working tree holds peer-session work - **no commits without operator order.**",
          ">", "> `code/windows` shows tracked-file deletions by design/history: chromix 3,687",
          "> (intentional, integrated browser = Codeix), gsx-cli 2,053 (peer seat refresh in",
          "> flight - disk has 1,503 files + 2,093 untracked, HEAD recoverable), zenix-cc/codeix",
          "> renames. Disk intact: 239,227 files, all 9 seats present.", ""]

    # 4. ledger
    L += ["## 4. Phase-0 ledger (master plan)", ""]
    try:
        plan = open(PLAN, encoding="utf-8").read()
        for tag in ["OPEN-DECISION", "OPEN-RESEARCH", "OPEN-DESIGN", "OPEN-UNKNOWN", "OPEN-ACTION"]:
            n = len(re.findall(r"\*\*\[%s\]\*\*" % tag, plan))
            L.append("- %s: **%d**" % (tag, n))
        nres = len(re.findall(r"RESOLVED 2026-11-12", plan))
        L.append("- RESOLVED (tagged 2026-11-12): **%d**" % nres)
        L += ["", "> Bullet tags in the Phase-0 section (ledger table in 11 mirrors them)."]
    except OSError as e:
        L.append("(plan unreadable: %s)" % e)
    L.append("")

    # 5. domain coverage
    L += ["## 5. Research domain coverage (audit 2026-11-12)", "",
          "| Domain | Status | Evidence |", "|---|---|---|"]
    for name, status, ev in DOMAINS:
        L.append("| %s | **%s** | %s |" % (name, status, ev))
    L.append("")

    # 6. parked
    L += ["## 6. Parked (operator: 'Dono baad me karenge!')", "",
          "- Sonar (DSH) effort-slider integration - D-25",
          "- Zenix (Claude Desktop) effort-slider port (A DOM-inject / B native) - D-25",
          "- Git commits for both repos - awaiting order", ""]

    # 7. open ledger items (grind queue)
    L += ["## 7. Open ledger items (the grind queue)", ""]
    try:
        items = re.findall(r"\*\*\[(OPEN-[A-Z]+)\]\*\*\s*(.{0,100})", plan)
        for i, (tag, txt) in enumerate(items[:30], 1):
            L.append("%d. **[%s]** %s" % (i, tag, txt.strip().rstrip("*").strip()))
        if not items:
            L.append("(no OPEN tags found)")
    except OSError:
        L.append("(unreadable)")
    L.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
