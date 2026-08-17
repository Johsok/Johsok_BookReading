# -*- coding: utf-8 -*-
"""Dump first N pending books for batch prompts."""
import json
import sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
data = json.load(open("tmp_pending_06.json", encoding="utf-8"))
batch = data["pending"][start : start + n]
out = []
for item in batch:
    out.append(
        {
            "id": item["id"],
            "title": item["title"],
            "author": item["author"],
            "file": item["file"],
            "tags": item["tags"],
            "summary": item["summary"],
        }
    )
path = f"tmp_batch_{start+1:03d}_{start+len(batch):03d}.json"
with open(path, "w", encoding="utf-8") as handle:
    json.dump(out, handle, ensure_ascii=False, indent=2)
print(path, len(out))
