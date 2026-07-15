from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b9 as prior


batch = prior.batch
batch.BATCH_NAME = "b10"
batch.WORK_ID = "findbook-20260715-205830-b10"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b10.json"
)
batch.REJECT_TITLES.update(
    {
        "the convoluted universe, book two",
        "same soul, many bodies",
        "enabling occupation ii",
        "appreciative inquiry handbook",
        "the clarity cleanse",
        "hungry planet",
        "progress in inorganic chemistry",
        "ecotourism",
        "the quick clean diet",
        "implementing organizational change",
        "dryden's outlines of chemical technology for the 21st century",
    }
)


if __name__ == "__main__":
    batch.main()
