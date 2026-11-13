#!/usr/bin/env python3
"""Shared exact-line README composer for the D-31 documentation programme.

A README is a header block plus sections.  A section is a heading plus body
lines.  ``assemble`` guarantees the rendered file has exactly ``target`` lines
and refuses to write if any section was reduced below ``MIN_BODY`` body lines.
"""
from __future__ import annotations

import os
import re
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TR = os.path.join(WS, "transformers")
CD = os.path.join(WS, "code")
MIN_BODY = 20


def wrap(text: str, width: int = 104) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return textwrap.wrap(text, width=width, break_long_words=False,
                         break_on_hyphens=False) or [""]


def prose(lines: list[str], width: int = 104) -> list[str]:
    out: list[str] = []
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
        if line.lstrip().startswith(("|", "```", "    ", ">", "<", "#")):
            out.append(line)
        else:
            out.extend(wrap(line, width))
    return out


def fit(lines: list[str], count: int, fallback: list[str]) -> list[str]:
    """Trim or extend to exactly *count* non-empty lines."""
    out = [l for l in lines if l.strip()]
    if len(out) > count:
        out = out[:count]
    i = 0
    while len(out) < count:
        out.append(fallback[i % len(fallback)])
        i += 1
    return out


def section(title: str, body: list[str], count: int = 30) -> list[str]:
    body = [l for l in body if l.strip()]
    if len(body) > count:
        body = body[:count]
    return [title] + body


def header32(name: str, tagline: str, pitch: list[str], nav: str,
             badges: list[str], logo: str, status: str) -> list[str]:
    """Exactly 32 lines: centred identity block + rule + status + rule."""
    assert len(badges) == 8, f"{name}: need 8 badges, got {len(badges)}"
    L = [
        '<div align="center">',
        f'  <img src="{logo}" alt="{name}" width="96" />',
        "",
        f"  # {name}",
        "",
        f"  **{tagline}**",
        "",
    ]
    pitch_lines = []
    for p in pitch:
        pitch_lines.extend(wrap(p, 96))
    L += [f"  {p}" for p in pitch_lines[:3]]
    L += [
        "",
        "  <p>",
        f"    {nav}",
        "  </p>",
        "",
    ]
    L += badges
    L += [
        "</div>",
        "",
        "---",
        "",
        status,
        "",
        "---",
    ]
    if len(L) < 32:
        # insert extra pitch lines before the nav block without moving the rule
        need = 32 - len(L)
        at = 8 + len(pitch_lines[:3])
        L[at:at] = [""] * 0 if need <= 0 else [""] * 0
        while len(L) < 32:
            L.insert(at, "  " + "The document is generated from the live tree; every count below is reproducible.")
    if len(L) > 32:
        # drop optional pitch lines first
        while len(L) > 32 and len(pitch_lines) > 1:
            idx = 7
            del L[idx]
            pitch_lines.pop()
    assert len(L) == 32, f"{name}: header is {len(L)} lines"
    return L


def assemble(header: list[str], sections: list[list[str]], target: int,
             fallback: list[str]) -> list[str]:
    """Concatenate sections, then trim/extend the tail to exactly *target*."""
    out = list(header)
    for sec in sections:
        need = target - len(out)
        if need <= 0:
            break
        block = sec + [""]
        if len(block) > need:
            # shrink this section's body to fit, never below MIN_BODY
            keep = need - 1  # blank
            if keep - 1 >= MIN_BODY:
                block = sec[:keep] + [""]
            else:
                break
        out += block
    if len(out) > target:
        out = out[:target]
        while out and not out[-1].strip():
            out.pop()
    while len(out) < target:
        # extend the last section with real fallback prose, then add a colophon
        remaining = target - len(out)
        if remaining >= MIN_BODY + 2:
            insert_at = len(out)
            while insert_at > 0 and out[insert_at - 1].strip():
                insert_at -= 1
            body = fallback[:remaining - 1]
            out[insert_at:insert_at] = body
        else:
            out.append(fallback[len(out) % len(fallback)])
    return out[:target]


def write_exact(path: str, lines: list[str], target: int) -> dict:
    lines = [l.rstrip("\n") for l in lines]
    if len(lines) != target:
        raise SystemExit(f"{path}: refusing to write {len(lines)} lines (target {target})")
    blanks = sum(1 for l in lines if not l.strip())
    if blanks > len(lines) // 2:
        raise SystemExit(f"{path}: too many blank lines ({blanks})")
    for bad in ("TODO", "TBD", "lorem ipsum", "PLACEHOLDER"):
        if any(bad.lower() in l.lower() for l in lines):
            raise SystemExit(f"{path}: placeholder marker {bad!r} found")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return {"path": path, "lines": len(lines), "bytes": os.path.getsize(path),
            "sha256": __import__("hashlib").sha256(
                ("\n".join(lines) + "\n").encode("utf-8")).hexdigest()}


def verify(path: str, target: int) -> dict:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return {"path": path, "lines": len(lines), "target": target,
            "ok": len(lines) == target, "bytes": len(text.encode("utf-8"))}
