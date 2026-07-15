from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b4 as batch


batch.BATCH_NAME = "b8"
batch.WORK_ID = "findbook-20260715-201722-b8"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b8.json"
)
batch.CATEGORY_REJECT_TITLES.setdefault("02_psychology_growth", set()).add(
    "the coming wave"
)
batch.CATEGORY_REJECT_TITLES["02_psychology_growth"].update(
    {
        "history of witchcraft: sorcerers, heretics & pagans",
        "numerology",
        "warren buffett's management secrets",
        "primal leadership",
        "emotional intelligence for sales success",
        "you can sell",
        "aleph-tav body system",
        "a happy pocket full of money",
        "cunningham's encyclopedia of wicca in the kitchen",
        "gastrophysics",
        "losing eden",
        "money, and the law of attraction",
        "fat land",
    }
)
batch.CATEGORY_REJECT_TITLES.setdefault("03_natural_science", set()).add(
    "data science"
)
batch.CATEGORY_REJECT_TITLES.setdefault("04_healthcare", set()).add(
    "green witchcraft"
)
batch.CATEGORY_REJECT_TITLES.setdefault("07_other", set()).add(
    "mycelium running"
)
batch.CATEGORIES = tuple(
    batch.CategorySpec(
        spec.category_id,
        spec.label,
        spec.quota,
        spec.queries
        + (
            ("habits", "習慣"),
            ("self-esteem", "自尊"),
            ("resilience", "韌性"),
            ("well-being", "幸福感"),
        ),
    )
    if spec.category_id == "02_psychology_growth"
    else spec
    for spec in batch.CATEGORIES
)


if __name__ == "__main__":
    batch.main()
