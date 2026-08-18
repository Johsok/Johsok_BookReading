# -*- coding: utf-8 -*-
from pathlib import Path

TMP = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")

BOOKS = {
    "05_food_wellness-20260724-01.json": (TMP / "hl_20260724_01.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-02.json": (TMP / "hl_20260724_02.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-03.json": (TMP / "hl_20260724_03.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-04.json": (TMP / "hl_20260724_04.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-05.json": (TMP / "hl_20260724_05.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-06.json": (TMP / "hl_20260724_06.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-07.json": (TMP / "hl_20260724_07.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-08.json": (TMP / "hl_20260724_08.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-09.json": (TMP / "hl_20260724_09.txt").read_text(encoding="utf-8-sig").splitlines(),
    "05_food_wellness-20260724-10.json": (TMP / "hl_20260724_10.txt").read_text(encoding="utf-8-sig").splitlines(),
}

for k, v in BOOKS.items():
    BOOKS[k] = [ln.strip() for ln in v if ln.strip()]
