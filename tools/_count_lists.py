# -*- coding: utf-8 -*-
import ast
from pathlib import Path

text = Path(__file__).with_name("_gen_grok_211_215.py").read_text(encoding="utf-8")
module = ast.parse(text)
for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.startswith("BOOK_"):
                value = ast.literal_eval(node.value)
                print(target.id, len(value))
