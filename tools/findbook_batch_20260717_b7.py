from __future__ import annotations

import json
from pathlib import Path

import findbook_batch_20260717_b6 as previous


batch = previous.batch
FROM_DATE = "2026-06-18"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-145941-b7"
NATURAL_CANDIDATE_PATH = Path(__file__).with_name(
    ".findbook_natural_candidates_20260717_b7.json"
)


def candidate_rows(items: list[dict]) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (
            str(item["title"]).strip(),
            str(item["author"]).strip(),
            str(item.get("date", "")).replace("/", "-").strip(),
            str(item["url"]).strip(),
        )
        for item in items
        if item.get("title") and item.get("author") and item.get("url")
    )


raw_natural_candidates = json.loads(
    NATURAL_CANDIDATE_PATH.read_text(encoding="utf-8")
)
CANDIDATES = dict(previous.CANDIDATES)
CANDIDATES["03_natural_science"] = candidate_rows(
    raw_natural_candidates["03_natural_science"]
)


def load_candidate_pools():
    batch.FROM_DATE = FROM_DATE
    batch.TO_DATE = TO_DATE
    batch.WORK_ID = WORK_ID
    return CANDIDATES


batch.FROM_DATE = FROM_DATE
batch.TO_DATE = TO_DATE
batch.WORK_ID = WORK_ID
batch.EXTRA_POOLS = CANDIDATES
batch.load_candidate_pools = load_candidate_pools
batch.source_name = previous.source_name
batch.highlights_for = previous.highlights_for


if __name__ == "__main__":
    batch.main()
