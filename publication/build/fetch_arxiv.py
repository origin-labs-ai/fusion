#!/usr/bin/env python3
"""Fetch live arXiv metadata for the research compendium.

Writes publication/report/arxiv.json with title, authors, year, id, abstract and
the topic bucket that requested it.  The script is deterministic: the id list is
fixed, the cache is reused, and failed lookups are reported instead of invented.
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "report", "arxiv.json"))
API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

TOPICS = {
    "quantization": [
        "2210.17323", "2306.00978", "2211.10438", "2305.14314", "2208.07339",
        "2307.13304", "2308.13137", "2402.17764", "2209.05433", "2206.01861",
        "2306.03078", "2306.07629", "2402.02750",
    ],
    "training": [
        "2106.09685", "2402.09353", "2402.04396", "2307.05695", "2203.15556",
        "1910.02054", "2205.01068", "2302.13971", "2307.09288", "2407.21783",
        "2310.06825", "1706.03762", "1810.04805", "2005.14165",
    ],
    "attention": [
        "2205.14135", "2104.09864", "2312.00752", "2305.13048", "2307.08621",
        "2306.15794", "2310.01889", "2004.05150", "2103.03206", "2203.08913",
        "2112.04426", "2309.06180",
    ],
    "long-context": [
        "2307.03172", "2404.06654", "2406.17419", "2406.16008", "2412.13663",
        "2402.19473", "2403.05530",
    ],
    "agents": [
        "2302.04761", "2210.03629", "2005.11401", "2004.04906", "2303.08774",
        "2203.02155", "2212.08073", "2402.03300", "2501.12948", "2405.04434",
        "2412.19437",
    ],
    "serving": [
        "2211.17192", "2302.01318", "2309.06180", "2312.07104", "2401.10774",
        "2401.15077", "2101.03961", "2401.04088",
    ],
}

# A small number of post-2026 reports that matter to the long-context argument.
QUERIES = [
    ("long-context", 'all:"context rot"'),
    ("long-context", 'all:"lost in the middle" AND all:"long context"'),
    ("quantization", 'all:"post-training quantization" AND all:"large language model"'),
    ("serving", 'all:"speculative decoding" AND all:"inference"'),
    ("attention", 'all:"linear attention" AND all:"language model"'),
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Fusion-Report/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def parse(xml: str, topic: str) -> list[dict]:
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", NS):
        aid = e.findtext("a:id", default="", namespaces=NS)
        m = re.search(r"abs/([0-9.]+)(?:v\d+)?$", aid)
        if not m:
            continue
        authors = [a.findtext("a:name", default="", namespaces=NS)
                   for a in e.findall("a:author", NS)]
        pub = e.findtext("a:published", default="", namespaces=NS)
        out.append({
            "id": m.group(1),
            "title": " ".join((e.findtext("a:title", default="", namespaces=NS) or "").split()),
            "authors": authors,
            "year": pub[:4],
            "published": pub[:10],
            "abstract": " ".join((e.findtext("a:summary", default="", namespaces=NS) or "").split()),
            "topic": topic,
        })
    return out


def main() -> int:
    papers: dict[str, dict] = {}
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT, encoding="utf-8"))
            for p in old.get("papers", []):
                papers[p["id"]] = p
        except Exception:
            pass

    ids = sorted({i for v in TOPICS.values() for i in v})
    for start in range(0, len(ids), 20):
        chunk = ids[start:start + 20]
        url = API + "?" + urllib.parse.urlencode({
            "id_list": ",".join(chunk), "max_results": len(chunk)})
        try:
            for p in parse(fetch(url), "core"):
                papers[p["id"]] = p
            print(f"ids {start + 1}-{start + len(chunk)}: ok")
        except Exception as exc:
            print(f"ids {start + 1}-{start + len(chunk)}: {type(exc).__name__}: {exc}")

    for topic, query in QUERIES:
        url = API + "?" + urllib.parse.urlencode({
            "search_query": query, "start": 0, "max_results": 8,
            "sortBy": "relevance", "sortOrder": "descending"})
        try:
            found = parse(fetch(url), topic)
            for p in found:
                p.setdefault("topic", topic)
                papers.setdefault(p["id"], p)
            print(f"query {topic}: {len(found)}")
        except Exception as exc:
            print(f"query {topic}: {type(exc).__name__}: {exc}")

    # topic assignment from the curated buckets wins over the generic fetch
    for topic, bucket in TOPICS.items():
        for aid in bucket:
            if aid in papers:
                papers[aid]["topic"] = topic

    ordered = sorted(papers.values(), key=lambda p: (p.get("topic", ""), p.get("year", ""), p["id"]))
    data = {"source": "arXiv API", "count": len(ordered), "papers": ordered}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(ordered)} papers")
    by = {}
    for p in ordered:
        by[p.get("topic", "?")] = by.get(p.get("topic", "?"), 0) + 1
    print(by)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
