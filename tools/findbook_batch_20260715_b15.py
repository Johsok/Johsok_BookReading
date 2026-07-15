from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b14 as prior


batch = prior.batch
batch.BATCH_NAME = "b15"
batch.WORK_ID = "findbook-20260715-233205-b15"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b15.json"
)
batch.CATEGORY_REJECT_TITLES.setdefault("02_psychology_growth", set()).update(
    {
        "massage therapy",
        "the age of unreason",
        "between death and life",
        "phantoms in the brain : probing the mysteries of the human mind",
        "only the paranoid survive",
        "making connections",
        "electrotherapy explained",
        "living the seven habits cd",
        "baby treatment based on ndt principles",
        "crystals",
        "organization theory for public administration",
        "corporate lifecycles",
    }
)

quotas = {
    "01_business_startup": 20,
    "02_psychology_growth": 20,
    "03_natural_science": 10,
    "04_healthcare": 5,
    "05_food_wellness": 5,
    "06_computer_info": 5,
    "07_other": 5,
}
batch.CATEGORIES = tuple(
    batch.CategorySpec(spec.category_id, spec.label, quotas[spec.category_id], spec.queries)
    for spec in batch.CATEGORIES
)


if __name__ == "__main__":
    batch.main()
