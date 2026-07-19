# -*- coding: utf-8 -*-
import json
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "fw",
    Path(__file__).resolve().parent / "findbook_writer.py",
)
fw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fw)

ids = ["187", "188", "189", "190", "194", "195", "199", "200", "220"]
base = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"

for i in ids:
    path = base / f"01_business_startup-20260717-{i}.json"
    d = json.loads(path.read_text(encoding="utf-8-sig"))
    hs = d.get("chatgptHighlights") or []
    src = d.get("highlightsSource")
    st = d.get("chatgptStatus")
    title = d.get("title", "")
    author = d.get("author", "")
    print(f"=== {i} | src={src} status={st} n={len(hs)}")
    print(f"  title={title}")
    print(f"  author={author}")
    try:
        fw.validate_highlights(d["id"], hs, title, author)
        qualified = src == "grok" and st == "complete" and len(hs) == 150
        print(f"  validate: OK | skip_as_qualified={qualified}")
    except Exception as e:
        print(f"  validate FAIL: {e}")
        print("  need_regen=True")
