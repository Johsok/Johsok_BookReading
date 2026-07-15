from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b4 as batch


batch.BATCH_NAME = "b5"
batch.WORK_ID = "findbook-20260715-195429-b5"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b5.json"
)


if __name__ == "__main__":
    batch.main()
