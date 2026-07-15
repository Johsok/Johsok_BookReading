from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b10 as prior


batch = prior.batch
batch.BATCH_NAME = "b11"
batch.WORK_ID = "findbook-20260715-210600-b11"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b11.json"
)
batch.REJECT_TITLES.update(
    {
        "the bullies",
        "the advantage",
        "biblical and theological visions of resilience",
        "mughal feast",
        "goodman & gilman's the pharmacological basis of therapeutics",
        "the technology fallacy",
        "evolve your brain",
        "the wizard and the prophet",
        "the law of attraction experiment",
        "the leading brain",
        "rewire your anxious brain",
    }
)


if __name__ == "__main__":
    batch.main()
