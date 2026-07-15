from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b12 as prior


batch = prior.batch
batch.BATCH_NAME = "b13"
batch.WORK_ID = "findbook-20260715-230753-b13"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b13.json"
)
batch.REJECT_TITLES.update(
    {
        "opportunities in estate planning for professional advisors",
        "tenbizplan",
        "pensions in the health and retirement study",
        "management dilemmas",
        "the routledge companion to advertising and promotional culture",
        "estate planning for the healthy wealthy family",
        "business agreements - instructor guide",
        "the 21 irrefutable laws of leadership workbook",
        "financial planners, investment advisers and broker-dealers",
        "corporate strategy toolkit",
        "paradox of organizational change",
        "the convoluted universe, book one",
        "radiating feminism",
        "nutritional medicine",
        "two turns from zero",
        "geographies of comfort",
        "the miracle club",
        "müdigkeitsgesellschaft",
        "canadian professional engineering and geoscience",
        "get out of my head",
        "woke doesn't mean broke",
        "radical simplicity",
        "estoicismo",
        "resilience from the heart",
        "i am great!",
        "develop your medical intuition",
        "javascript",
        "empathy and business transformation",
        "boundary-spanning in organizations",
    }
)


if __name__ == "__main__":
    batch.main()
