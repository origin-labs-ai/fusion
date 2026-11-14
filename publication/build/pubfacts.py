#!/usr/bin/env python3
"""Shared live facts for the publication build."""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", ".."))
DG = os.path.join(WS, ".plan", "telemetry", "docgen")

F = json.load(open(os.path.join(DG, "facts.json"), encoding="utf-8"))
TF = F["transformers"]
CF = F["code"]
FF = F["fusion"]

FORMATS = TF["formats_valid"]
RETIRED = TF["formats_retired"]
TESTS = TF["tests"]
LIBS = TF["libs"]
TARGETS = TF["targets"]
BACKENDS = TF["backends"]
SRC = TF["src_tree"]
SEATS = CF["seats"]
DECISIONS = FF["decisions"]
RESEARCH = FF["research"]
REG = CF["registry"]
LAY = CF["layouts"]

N_FORMATS = len(FORMATS)
N_RETIRED = len(RETIRED)
N_TESTS = len(TESTS)
N_LIBS = len(LIBS)
N_TARGETS = len(TARGETS)
N_BACKENDS = len(BACKENDS)
N_SEATS = len(SEATS)
N_DECISIONS = len(DECISIONS)
N_RESEARCH = len(RESEARCH)
N_CASES = sum(len(t["cases"]) for t in TESTS)
N_ASSERTS = sum(t["asserts"] for t in TESTS)
N_SRC = len(SRC)
N_FILES = TF["stats"]["files"]
N_LOC = TF["stats"]["loc"]
CODE_FILES = CF["stats"]["files"]
CODE_BYTES = CF["stats"]["bytes"]
TF_HEAD = TF["git"]["head"].split()[0]
CODE_HEAD = CF["git"]["head"].split()[0]
FUSION_HEAD = FF["git"]["head"].split()[0]


def fill(body: list[str], pad: list[str], target: int = 30) -> list[str]:
    """Pad a page body to exactly `target` lines without looping forever."""
    body = [l for l in body if l.strip()]
    seen = set(body)
    i = 0
    while len(body) < target:
        if i < len(pad):
            cand = pad[i]
        else:
            cand = f"The page is part of the generated edition; closing note {i - len(pad) + 1}."
        i += 1
        if cand not in seen:
            seen.add(cand)
            body.append(cand)
    return body[:target]


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.1f} GB"
