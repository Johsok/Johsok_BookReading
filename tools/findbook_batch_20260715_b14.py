from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b13 as prior


batch = prior.batch
batch.FROM_DATE = "1985-06-01"
batch.BATCH_NAME = "b14"
batch.WORK_ID = "findbook-20260715-231837-b14"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b14.json"
)
batch.REJECT_TITLES.update(
    {
        "financial management",
        "rich dad, poor dad 2 (rich dad)",
        "acca study text",
        "marketing research",
        "business",
        "the secret language of birthdays",
        "tidy's physiotherapy",
        "david kibbe's metamorphosis",
        "comprehensive classroom management",
        "studies in natural products chemistry",
        "reviews of environmental contamination and toxicology",
        "health and personal social services",
        "contemporary nutrition",
        "prescription for nutritional healing",
        "managerial accounting",
        "the silva mind control method",
        "behold a pale horse",
        "managing change",
        "va health care",
        "the power of color",
        "african holistic health",
        "basics of acupuncture",
        "blood counts and differentials evaluation/includes book, ibm pc disk and instruction booklet",
        "industrial therapy",
        "the secret language of relationships",
    }
)

quotas = {
    "01_business_startup": 30,
    "02_psychology_growth": 30,
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
