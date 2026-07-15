from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b8 as prior


batch = prior.batch
batch.BATCH_NAME = "b9"
batch.WORK_ID = "findbook-20260715-205005-b9"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b9.json"
)
batch.REJECT_TITLES.update(
    {
        "think like a billionaire, become a billionaire",
        "dodging energy vampires",
        "curry",
        "transcend",
        "passing of temporal well-being",
        "food matters",
        "textbook of astronomy and astrophysics with elements of cosmology",
        "campbell biology in focus",
        "finding god in the waves",
        "de bron :",
        "quantum physics for beginners",
        "horizons in neuroscience research",
        "community/public health nursing",
        "the apprentice",
        "cannibalism",
        "textbook of medical pharmacology",
        "holacracy",
        "the convoluted universe, book three",
        "five lives remembered",
        "organisation theory",
        "encyclopedia of positive psychology",
        "essentials of organizational behavior",
        "one simple idea",
        "visualizing psychology",
        "outlines of dairy technology",
    }
)

extra_queries = {
    "01_business_startup": (
        ("business strategy", "商業策略"),
        ("financial planning", "財務規畫"),
    ),
    "02_psychology_growth": (
        ("therapy", "心理治療"),
        ("behavior change", "行為改變"),
        ("positive psychology", "正向心理學"),
    ),
    "03_natural_science": (
        ("evolution", "演化"),
        ("ecology", "生態學"),
        ("earth science", "地球科學"),
        ("chemistry", "化學"),
    ),
    "04_healthcare": (("patient care", "病人照護"),),
    "05_food_wellness": (
        ("food science", "飲食科學"),
        ("healthy cooking", "健康料理"),
    ),
    "07_other": (
        ("world history", "世界史"),
        ("cultural history", "文化史"),
        ("archaeology", "考古學"),
    ),
}
batch.CATEGORIES = tuple(
    batch.CategorySpec(
        spec.category_id,
        spec.label,
        spec.quota,
        spec.queries + extra_queries.get(spec.category_id, ()),
    )
    for spec in batch.CATEGORIES
)


if __name__ == "__main__":
    batch.main()
