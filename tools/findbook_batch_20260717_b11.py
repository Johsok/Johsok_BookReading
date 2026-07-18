from __future__ import annotations

import json
from pathlib import Path

import findbook_batch_20260717_b10 as previous


batch = previous.batch
FROM_DATE = "2026-06-18"
TO_DATE = "2026-07-17"
WORK_ID = "findbook-20260717-151949-b11"
CANDIDATE_PATH = Path(__file__).with_name(
    ".findbook_browser_candidates_20260717_b11.json"
)


def candidate_rows(items: list[list[str]]) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (
            str(title).strip(),
            str(author).strip(),
            str(date).replace("/", "-").strip(),
            str(url).strip(),
        )
        for title, author, date, url in items
        if title and author and url
    )


raw_candidates = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
CANDIDATES = {
    category_id: candidate_rows(items)
    for category_id, items in raw_candidates.items()
}


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


if __name__ == "__main__":
    batch.main()
