from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b4 as batch


batch.BATCH_NAME = "b7"
batch.WORK_ID = "findbook-20260715-201336-b7"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b7.json"
)
batch.CATEGORY_REJECT_TITLES.setdefault("02_psychology_growth", set()).add(
    "the coming wave"
)
batch.CATEGORY_REJECT_TITLES.setdefault("03_natural_science", set()).add(
    "data science"
)
batch.CATEGORY_REJECT_TITLES.setdefault("04_healthcare", set()).add(
    "green witchcraft"
)


if __name__ == "__main__":
    batch.main()
