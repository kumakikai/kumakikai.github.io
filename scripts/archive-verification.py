#!/usr/bin/env python3
"""Keep large browser traces losslessly, with readable JSON summaries in Git.

Run after QA completes, never while a browser script is writing its report.
The .json.gz contains the exact original report, including all per-page results.
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

directory = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/watch-typography")
for file in sorted(directory.glob("*.json")):
    raw = file.read_bytes()
    if len(raw) < 128 * 1024:
        continue
    report = json.loads(raw)
    if not isinstance(report.get("results"), list):
        continue
    if report.get("pending"):
        raise SystemExit(f"Still running; do not archive {file}")
    archive = file.with_suffix(".json.gz")
    compressed = gzip.compress(raw, mtime=0)
    assert gzip.decompress(compressed) == raw
    archive.write_bytes(compressed)
    summary = {key: value for key, value in report.items() if key != "results"}
    summary.update(fullEvidence=archive.name,
                   fullEvidenceSHA256=hashlib.sha256(raw).hexdigest(),
                   resultCount=len(report["results"]))
    file.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(f"{file.name}: {len(report['results'])} results preserved in {archive.name}")
