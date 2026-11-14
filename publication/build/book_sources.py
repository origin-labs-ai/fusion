#!/usr/bin/env python3
"""Curated source map and cleaning rules for the continuous-flow report.

Every chapter names the project records it draws from.  The cleaner removes
build chatter, local paths, decorative HTML and duplicated boilerplate, then
hands the surviving Markdown to booktex.convert().
"""
from __future__ import annotations

import os
import re
from collections import Counter

import booktex

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", ".."))

BANNED = [
    r"[A-Za-z]:[\\/]", r"/c/Users/", r"\\Users\\",
    r"\.plan[/\\]", r"publication[/\\]build", r"docgen", r"facts\.json",
    r"telemetry[/\\]docgen", r"\.rea-tmp", r"\.extract-tmp",
    r"generated from the live tree", r"generated at exactly",
    r"this README is generated", r"generator re-reads",
    r"the number is checked by the documentation verifier",
    r"the document is part of the D-31 programme",
    r"a cold reader can reproduce the claim",
    r"the live source is the repository",
    r"the rule is recorded in the decision log",
    r"the superproject records the component pins",
    r"a claim that cannot be checked is not repeated",
    r"the dashboard is the live instrument",
    r"the decision log is the constitution",
    r"the research index is the evidence shelf",
    r"the grind tree is the queue",
    r"the publication package is the long-form edition",
    r"the engine and the launcher are pinned independently",
    r"generated:", r"last updated:", r"maintained by:",
    r"language policy:", r"this file is the single source of truth",
    r"operator speaks casual hinglish", r"read this context-recovery",
    r"docs-only", r"no build, no code", r"pdf and docx",
    r"512-page docx", r"512-page pdf", r"winword", r"pdflatex",
    r"lualatex", r"xelatex", r"pdfinfo", r"python-docx",
]
BANNED_RE = re.compile("|".join(BANNED), re.I)
TAG_RE = re.compile(r"<[^>]+>")
BADGE_RE = re.compile(r"img\.shields\.io|shields\.io/badge|badge/", re.I)
RULE_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")


def read(path: str) -> str:
    full = os.path.join(WS, path)
    if os.path.isdir(full):
        parts: list[str] = []
        for root, dirs, files in os.walk(full):
            dirs.sort()
            for name in sorted(files):
                if name.endswith(".md"):
                    parts.append(open(os.path.join(root, name),
                                      encoding="utf-8", errors="replace").read())
        return "\n\n".join(parts)
    return open(full, encoding="utf-8", errors="replace").read()


def normalize_line(line: str) -> str:
    line = line.replace("\r", "")
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
    line = TAG_RE.sub("", line)
    line = line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    line = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", line)
    line = re.sub(r"^\s*>\s?", "", line)
    return line.rstrip()


def clean_text(text: str, drop_title: bool = True) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1 and end < 2000:
            text = text[end + 4:]
    raw = text.split("\n")
    out: list[str] = []
    title_dropped = False
    in_fence = False
    for line in raw:
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if BADGE_RE.search(line):
            continue
        if s.startswith("<") and (s.endswith(">") or s.startswith(("<div", "<p", "<img", "<a ", "<br", "</"))):
            continue
        if s.startswith("!["):
            continue
        if RULE_RE.match(line):
            continue
        if BANNED_RE.search(line):
            continue
        line = normalize_line(line)
        s = line.strip()
        if s.startswith("#"):
            if drop_title and not title_dropped:
                title_dropped = True
                continue
            if re.fullmatch(r"#+\s*[=\-#]{3,}\s*", s):
                continue
        if s.startswith("#") and not s.lstrip("#").strip():
            continue
        out.append(line)
    # collapse repeated blank lines
    cleaned: list[str] = []
    blank = False
    for line in out:
        if not line.strip():
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False
    return cleaned


def drop_repeated(lines: list[str], counts: Counter) -> list[str]:
    out = []
    for line in lines:
        s = line.strip()
        if (len(s) > 70 and not s.startswith(("#", "|", "```", "-", "*", ">"))
                and counts[re.sub(r"\s+", " ", s)] >= 4):
            continue
        out.append(line)
    return out


CHAPTERS = [
    # Part I
    dict(id="mission", part="I", title="Mission, goal line, and the operating contract",
         sources=[".plan/BLUEPRINT.md", ".plan/PLAN.md"]),
    dict(id="master-plan", part="I", title="The master plan: from transformer to Fusion",
         sources=[".plan/pasted-content-id-43ed-ye-aur-melodic-puddle.md"]),
    dict(id="operation-clean", part="I", title="Operation Clean: the quantization overhaul",
         sources=[".plan/cuddly-yawning-lamport.md"]),
    dict(id="int-fp", part="I", title="The INT and FP research programme",
         sources=[".plan/DRAFT.md"]),
    dict(id="decisions", part="I", title="The decision register",
         sources=[".plan/docs/operation-clean/DECISIONS.md"]),
    dict(id="research-index", part="I", title="The research index",
         sources=[".plan/RESEARCH-INDEX.md"]),
    dict(id="operator-record", part="I", title="The operator, the iron rules, and the mission",
         sources=[".plan/_archive/repo/memory/01-user-profile.md",
                  ".plan/_archive/repo/memory/02-iron-rules.md",
                  ".plan/_archive/repo/memory/04-philosophy-mean.md",
                  ".plan/_archive/repo/memory/05-transcender-mission.md"]),
    dict(id="project-map", part="I", title="Project map, repository layout, and file inventory",
         sources=[".plan/_archive/repo/memory/03-project-map.md",
                  ".plan/_archive/repo/memory/09-repo-layout.md",
                  ".plan/_archive/repo/memory/12-file-inventory.md"]),
    dict(id="session-history", part="I", title="Session history, current state, and the replan",
         sources=[".plan/_archive/repo/memory/06-zcode-sessions-history.md",
                  ".plan/_archive/repo/memory/07-opencode-session00.md",
                  ".plan/_archive/repo/memory/08-current-state-20260831.md",
                  ".plan/_archive/repo/memory/10-code-review-findings.md",
                  ".plan/_archive/repo/memory/11-verdent-session-log.md",
                  ".plan/_archive/repo/memory/13-replan-20260901.md",
                  ".plan/_archive/repo/memory/14-todos-cender-20260906.md",
                  ".plan/_archive/repo/memory/MEMORY.md"]),
    dict(id="review-record", part="I", title="The CodeFusion review record",
         sources=[".plan/review-tracking/MASTER_PLAN.md",
                  ".plan/review-tracking/FINAL_REPORT.md",
                  ".plan/review-tracking/DEFECTS.md",
                  ".plan/review-tracking/QODER_REPO_WIKI_RE.md",
                  ".plan/review-tracking/PROGRESS.md"]),
    dict(id="archive-transcript", part="I", title="The archive transcript",
         sources=[".plan/_archive/repo/TRANSCRIPT.md"]),
    dict(id="telemetry", part="I", title="Telemetry, the grind queue, and the working tree",
         sources=[".plan/telemetry/TODO-TREE.md", ".plan/telemetry/DASHBOARD.md",
                  ".plan/docs/operation-clean/WORKING-TREE.md",
                  ".plan/docs/operation-clean/PLAN.md"]),
    dict(id="fusion-readme", part="I", title="The superproject in its own words",
         sources=["README.md"]),

    # Part II
    dict(id="codefusion", part="II", title="CodeFusion: product research and session forensics",
         sources=[".plan/review-tracking/DRAFT.md"]),
    dict(id="code-readme", part="II", title="The launcher and the nine seats",
         sources=["code/README.md"]),
    dict(id="slider", part="II", title="The effort slider: a reverse-engineering case study",
         sources=["code/slider/effort/PUBLISHING.md", "code/slider/effort/ANIMATION.md"]),
    dict(id="harness-models", part="II", title="Harness engineering: models and methods",
         sources=["code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/models",
                  "code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/README.md"]),
    dict(id="harness-practices", part="II", title="Harness engineering: agent practices",
         sources=["code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/coding-agent-practices",
                  "code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/ai-friendly"]),
    dict(id="harness-loops", part="II", title="Harness engineering: loops and reliable delivery",
         sources=["code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/loop-engineering",
                  "code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/reliable-delivery",
                  "code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/finding-bound-fix.md",
                  "code/windows/onyx/resources/app/resources/plugins/bundle-plugins/better-harness/references/findings-review.md"]),
    dict(id="skill-payload", part="II", title="The agent-skill payload",
         sources=["code/.agents/skills/agent-browser",
                  "code/.agents/skills/feature-boundary-planner",
                  "code/.agents/skills/cf-popular-skills",
                  "code/.agents/skills/cf-find-simplifications",
                  "code/.agents/skills/cf-code-review",
                  "code/.agents/skills/cf-prose-standard",
                  "code/.agents/skills/dogfood",
                  "code/.agents/skills/record-browser-gif",
                  "code/.agents/skills/architecture-governance",
                  "code/.agents/skills/session-management"]),

    # Part III
    dict(id="engine-spec", part="III", title="The training engine specification",
         sources=["transformers/SPEC-INFERNO.md"]),
    dict(id="engine-arch", part="III", title="Engine architecture",
         sources=[".plan/_archive/docs/ARCHITECTURE.md"]),
    dict(id="engine-api", part="III", title="The engine API",
         sources=[".plan/_archive/docs/API_REFERENCE.md"]),
    dict(id="engine-tensor", part="III", title="Tensors, autograd, and numerical kernels",
         sources=[".plan/_archive/docs/MODULES/tensor.md"]),
    dict(id="engine-usage", part="III", title="Using and building the engine",
         sources=[".plan/_archive/docs/USAGE.md", ".plan/_archive/docs/BUILD.md"]),
    dict(id="engine-manifest", part="III", title="Model manifests, wire identity, and progress",
         sources=["transformers/docs/MODEL_MANIFEST.md", "transformers/PROGRESS.md"]),
    dict(id="engine-release", part="III", title="The engine release record",
         sources=[".plan/_archive/README.md"]),
    dict(id="engine-strategy", part="III", title="Strategy, scorecard, and launch record",
         sources=[".plan/_archive/docs/COMPETITOR_ANALYSIS.md",
                  ".plan/_archive/docs/STRATEGY.md",
                  ".plan/_archive/docs/PRODUCTION_SCORECARD.md",
                  ".plan/_archive/docs/LAUNCH_KIT.md",
                  ".plan/_archive/docs/FUNDING_COMPUTE.md",
                  ".plan/_archive/docs/PMEC_PROPOSAL_DRAFT.md",
                  ".plan/_archive/docs/K3_MXFP4_BRIDGE.md",
                  ".plan/_archive/docs/P13_SPECULATIVE_V2_REMOVED.md",
                  ".plan/_archive/docs/P1P73_REPORT.md",
                  ".plan/_archive/docs/CONTRIBUTING.md",
                  ".plan/_archive/docs/GOOD_FIRST_ISSUES.md"]),
    dict(id="tf-readme", part="III", title="The engine in its own words",
         sources=["transformers/README.md"]),

    # Part IV
    dict(id="whitepaper", part="IV", title="Native mixed-precision training via quantization barriers",
         sources=[".plan/_archive/docs/WHITEPAPER.md"]),
    dict(id="ladder", part="IV", title="The format ladder and the bit-per-weight contract",
         sources=[".plan/docs/operation-clean/LADDER.md"]),
    dict(id="claims", part="IV", title="The claim verification ledger",
         sources=[".plan/_archive/research/claim_ledger.md"]),
    dict(id="phase0", part="IV", title="Phase-0 research dossiers",
         sources=[".plan/_archive/repo/sessions/phase0"]),
    dict(id="audit-record", part="IV", title="Audit records and research protocols",
         sources=[".plan/_archive/research/ahm-iwm-vision-20260906.md",
                  ".plan/_archive/research/audit_full_20260825.md",
                  ".plan/_archive/research/transcender-satyam-thakur-protocol-v01.md",
                  ".plan/_archive/research/workbench.md",
                  ".plan/_archive/research/claims"]),
    dict(id="charts", part="IV", title="Comparison charts and measured quality",
         sources=[".plan/_archive/docs/COMPARISON_CHARTS.md"]),
    dict(id="proofs", part="IV", title="Proof expansions and formal notes",
         sources=[".plan/_archive/docs/PROOF_EXPANSIONS.md"]),
    dict(id="research-notes", part="IV", title="Research notes on formats, agents, and systems",
         sources=[".plan/_archive/docs/RESEARCH.md", ".plan/_archive/docs/INTERNAL/README.md",
                  ".plan/_archive/docs/RESEARCH"]),
    dict(id="gsx-mods", part="IV", title="Security modules and agent policies",
         sources=["code/windows/gsx-cli/mods"]),

    # Part V is generated from arXiv (see book_extra.py)
    # Part VI is the theorem note (see book_extra.py)
    # Part VII is method and evidence (see book_extra.py)
    # Part VIII is the reference apparatus (see book_extra.py)
]

PART_TITLES = {
    "I": ("The programme", "Mission, governance, the master plan, decisions, and the live queue."),
    "II": ("CodeFusion", "The launcher, the seats, the registry, and the reverse-engineering record."),
    "III": ("Transformers-Fusion", "The engine specification, architecture, API, and release record."),
    "IV": ("Quantization science", "Formats, training, proofs, and the measured claim ledger."),
    "V": ("Research compendium", "Live arXiv metadata and structured digests across six research lines."),
    "VI": ("Theorem note", "Constant-memory context, the Cender design, and the wire-identity theorem."),
    "VII": ("Method and evidence", "How claims are produced, checked, and bounded."),
    "VIII": ("Reference apparatus", "Registers, tables, glossary, bibliography, and index."),
}


def load_all() -> list[dict]:
    """Return cleaned source lines per chapter, with global boilerplate removed."""
    raw: dict[str, list[str]] = {}
    counts: Counter = Counter()
    for ch in CHAPTERS:
        lines: list[str] = []
        for src in ch["sources"]:
            if not os.path.exists(os.path.join(WS, src)):
                print(f"missing source: {src}", file=__import__("sys").stderr)
                continue
            text = read(src)
            part = clean_text(text, drop_title=True)
            if lines:
                lines.append("")
            lines.extend(part)
        raw[ch["id"]] = lines
        for line in lines:
            s = line.strip()
            if len(s) > 70 and not s.startswith(("#", "|", "```", "-", "*", ">")):
                counts[re.sub(r"\s+", " ", s)] += 1
    out = []
    for ch in CHAPTERS:
        lines = drop_repeated(raw[ch["id"]], counts)
        out.append({**ch, "lines": lines})
    return out


if __name__ == "__main__":
    chapters = load_all()
    total = 0
    for ch in chapters:
        chars = sum(len(l) for l in ch["lines"])
        total += chars
        print(f"{ch['part']} {ch['id']:18} {len(ch['lines']):5} lines {chars:9,} chars")
    print(f"TOTAL {total:,} chars in {len(chapters)} chapters")
