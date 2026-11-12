"""Extract every workflow run's data from the Claude Code workflow store.

Reads ~/.claude/projects/**/workflows/wf_*/ (journal.jsonl + agent-*.jsonl +
agent-*.meta.json) and writes one consolidated JSON per run plus a combined
summary. Read-only over the store; writes only under this directory.

Run:  python -I extract_workflow.py
"""

import json
import os
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

STORE = Path(os.environ.get("CLAUDE_HOME", r"C:/Users/thaku/.claude"))
PROJECTS = STORE / "projects"
OUT = Path(__file__).resolve().parent.parent / "workflow_extracted"
OUT.mkdir(parents=True, exist_ok=True)


def jloads(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def read_jsonl(path):
    out = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = jloads(line)
            if obj is not None:
                out.append(obj)
    return out


def find_workflow_runs():
    runs = {}
    # <project>/<session>/workflows/wf_*/  and  <project>/<session>/subagents/workflows/wf_*/
    for journal in PROJECTS.glob("*/*/workflows/wf_*/journal.jsonl"):
        run = journal.parent.name
        sid = journal.parents[2].name
        runs.setdefault(run, []).append((sid, journal.parent))
    for journal in PROJECTS.glob("*/*/subagents/workflows/wf_*/journal.jsonl"):
        run = journal.parent.name
        sid = journal.parents[3].name
        runs.setdefault(run, []).append((sid, journal.parent))
    return runs


def agent_result(path):
    """Pull the agent's final payload out of a transcript jsonl."""
    entries = read_jsonl(path)
    if not entries:
        return None
    # explicit result entry wins
    for e in reversed(entries):
        if isinstance(e, dict) and e.get("type") == "result" and "result" in e:
            return e["result"]
    # last assistant text block
    for e in reversed(entries):
        if not isinstance(e, dict):
            continue
        msg = e.get("message")
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            content = msg.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text" and block.get("text"):
                        return block["text"]
            elif isinstance(content, str) and content:
                return content
    return None


def agent_meta(path):
    return jloads(path.read_text(encoding="utf-8", errors="replace"))


def label_of(meta, fallback=None):
    if not isinstance(meta, dict):
        return fallback
    for key in ("description", "label"):
        val = meta.get(key)
        if isinstance(val, str) and val:
            return val
    return fallback


def parse_run(run_id, stores):
    labels = OrderedDict()
    for sid, store in stores:
        journal = store / "journal.jsonl"
        for entry in read_jsonl(journal):
            if not isinstance(entry, dict):
                continue
            etype = entry.get("type")
            label = entry.get("label")
            phase = entry.get("phase")
            if label is None:
                # result/failed entries carry no label: attribute via agentId
                label = ""
            rec = labels.setdefault(
                label,
                {
                    "label": label,
                    "phases": [],
                    "started": 0,
                    "result_events": 0,
                    "failed_events": 0,
                    "other_events": Counter(),
                    "results": [],
                    "failures": [],
                    "agents": [],
                },
            )
            if phase and phase not in rec["phases"]:
                rec["phases"].append(phase)
            if etype == "started":
                rec["started"] += 1
            elif etype == "result":
                rec["result_events"] += 1
                rec["results"].append(
                    {
                        "store": sid,
                        "agentId": entry.get("agentId"),
                        "key": entry.get("key"),
                        "payload": entry.get("result"),
                    }
                )
            elif etype == "failed":
                rec["failed_events"] += 1
                rec["failures"].append(
                    {
                        "store": sid,
                        "agentId": entry.get("agentId"),
                        "key": entry.get("key"),
                        "error": entry.get("error") or entry.get("message"),
                    }
                )
            else:
                rec["other_events"][etype] += 1

        # agents on disk (authoritative for payload when journal has none)
        for meta_path in sorted(store.glob("agent-*.meta.json")):
            agent_id = meta_path.name[len("agent-") : -len(".meta.json")]
            meta = agent_meta(meta_path)
            jsonl_path = store / f"agent-{agent_id}.jsonl"
            payload = agent_result(jsonl_path) if jsonl_path.exists() else None
            rec = labels.setdefault(
                label_of(meta, ""),
                {
                    "label": label_of(meta, ""),
                    "phases": [],
                    "started": 0,
                    "result_events": 0,
                    "failed_events": 0,
                    "other_events": Counter(),
                    "results": [],
                    "failures": [],
                    "agents": [],
                },
            )
            if isinstance(meta, dict) and meta.get("workflowPhase") and meta["workflowPhase"] not in rec["phases"]:
                rec["phases"].append(meta["workflowPhase"])
            rec["agents"].append(
                {
                    "agentId": agent_id,
                    "phase": (meta or {}).get("workflowPhase"),
                    "store": sid,
                    "hasPayload": payload is not None,
                    "payload": payload,
                }
            )

    for rec in labels.values():
        rec["other_events"] = dict(rec["other_events"])
        rec["agentCount"] = len(rec["agents"])
        rec["withPayload"] = sum(1 for a in rec["agents"] if a["hasPayload"])
    return labels


def main():
    runs = find_workflow_runs()
    combined = {}
    for run_id, stores in sorted(runs.items()):
        labels = parse_run(run_id, stores)
        combined[run_id] = labels
        (OUT / f"{run_id}.json").write_text(
            json.dumps(labels, indent=1, ensure_ascii=False, default=str), encoding="utf-8"
        )
        total = sum(r["started"] for r in labels.values())
        res = sum(r["result_events"] for r in labels.values())
        fail = sum(r["failed_events"] for r in labels.values())
        print(f"{run_id}: labels={len(labels)} started={total} result_events={res} failed_events={fail}")

    # markdown index
    lines = ["# Workflow runs extracted", ""]
    for run_id, labels in combined.items():
        lines.append(f"## {run_id}")
        lines.append("")
        lines.append("| label | phase | started | results | failed | agents w/ payload |")
        lines.append("|---|---|---|---|---|---|")
        for lab, r in sorted(labels.items(), key=lambda kv: kv[0]):
            lines.append(
                f"| {lab or '(unlabeled)'} | {','.join(r['phases'])} | {r['started']} | "
                f"{r['result_events']} | {r['failed_events']} | {r['withPayload']}/{r['agentCount']} |"
            )
        lines.append("")
    (OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
