# -*- coding: utf-8 -*-
"""Trim Book B to 150 unique points and strip leftover English."""
from __future__ import annotations

from pathlib import Path

PATH = Path(__file__).resolve().parent / "_gen_hl_04_healthcare_06_07.py"
text = PATH.read_text(encoding="utf-8")
text = text.replace("比週末才 commuter 去健身房", "比週末才特地跑去健身房")
PATH.write_text(text, encoding="utf-8")
print("replaced commuter")
