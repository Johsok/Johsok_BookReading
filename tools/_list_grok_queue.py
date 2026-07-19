"""List pending Grok highlight queue batches."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "tools" / ".findbook_grok_queue_20260719.json"


def main() -> int:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    batch = queue[start : start + count]
    for item in batch:
        print(f"{item['id']}\t{item['categoryId']}\t{item['title']}\t{item['author']}\t{item['file']}")
    print(f"# batch {start}:{start + len(batch)} of {len(queue)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
