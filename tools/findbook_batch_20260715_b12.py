from __future__ import annotations

from pathlib import Path

import findbook_batch_20260715_b11 as prior


batch = prior.batch
batch.BATCH_NAME = "b12"
batch.WORK_ID = "findbook-20260715-211259-b12"
batch.MASTER_CANDIDATES = (
    Path(__file__).resolve().parent / ".findbook_candidates_20260715_b12.json"
)
batch.REJECT_TITLES.update(
    {
        "group counseling",
        "deterring terrorism",
        "library and information sciences",
        "tourism resilience and adaptation to environmental change",
        "the slow down diet",
        "pain free",
        "organization change",
        "organisational resilience",
        "why organizational change fails",
        "managing and leading people through organizational change",
        "the hormone connection",
        "eat well, move well, live well",
        "resilient leadership",
        "feminism, interrupted",
        "laws of ux",
        "pathways to well-being in design",
        "yin yoga",
        "levers of organization design",
        "organization and architecture of innovation",
        "evidence-based initiatives for organizational change and development",
        "institutional theory and organizational change",
        "harvard business review on bringing your whole self to work",
        "research in organizational change and development",
    }
)


if __name__ == "__main__":
    batch.main()
