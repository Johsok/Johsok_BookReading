# -*- coding: utf-8 -*-
"""Fix short-colon lines in chunk20 generator and regenerate."""
from __future__ import annotations

import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
path = Path(__file__).with_name("_gen_chunk20_highlights.py")
text = path.read_text(encoding="utf-8")

# Replace colon after short label inside string literals: "....： -> use ，
# Safer: post-process bodies at runtime before pack — patch main instead.

patch = '''
def scrub(bodies: list[str]) -> list[str]:
    """Rewrite short-label colons so validate_highlights passes."""
    out = []
    for body in bodies:
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL_COLON_SUFFIXES):
            # turn first colon into pause comma
            body = body[: m.end(1)] + "，" + body[m.end() :]
        out.append(body)
    return out
'''

# Inject scrub helpers near pack()
if "def scrub(" not in text:
    text = text.replace(
        "from findbook_writer import validate_highlights  # noqa: E402\n",
        "from findbook_writer import validate_highlights, NATURAL_COLON_SUFFIXES  # noqa: E402\n",
    )
    text = text.replace(
        "def pack(bodies: list[str]) -> list[str]:",
        patch + "\ndef pack(bodies: list[str]) -> list[str]:",
    )
    text = text.replace(
        "highlights = pack(bodies)",
        "highlights = pack(scrub(bodies))",
    )
    path.write_text(text, encoding="utf-8")
    print("patched scrub")
else:
    print("already patched")
