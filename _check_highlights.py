# -*- coding: utf-8 -*-
"""Quick integrity check for regenerated highlight JSON files."""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

files = [
    r"Books\04_healthcare\04_healthcare-20260717-%d.json" % n
    for n in range(40, 56)
]

for path in files:
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        h = data.get("chatgptHighlights", [])
        numbered = all(
            isinstance(x, str) and x.startswith("%03d、" % (i + 1))
            for i, x in enumerate(h)
        )
        print(
            "%s | count=%d | numbered=%s | distinct=%d | src=%s | captured=%s"
            % (
                path.split("\\")[-1],
                len(h),
                numbered,
                len(set(h)),
                data.get("highlightsSource"),
                data.get("highlightsCapturedAt"),
            )
        )
    except Exception as e:
        print("%s | ERROR: %s" % (path.split("\\")[-1], e))
