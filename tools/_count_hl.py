from collections import Counter
from pathlib import Path
import ast

text = Path(__file__).with_name("_gen_pg_181_185.py").read_text(encoding="utf-8")
mod = ast.parse(text)
for node in mod.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.startswith("BOOK"):
                values = ast.literal_eval(node.value)
                print(target.id, "count", len(values), "unique", len(set(values)))
                dups = [b for b, c in Counter(values).items() if c > 1]
                print(" dups", dups[:5])
                starts = Counter(b[:18] for b in values)
                print(" top18", [(k, v) for k, v in starts.most_common(8) if v >= 2])
                print(" minlen", min(len(b) for b in values))
                print(" short", [i + 1 for i, b in enumerate(values) if len(b) < 12])
                s8 = Counter(b[:8] for b in values)
                print(" top8", [(k, v) for k, v in s8.most_common(12) if v >= 2])
