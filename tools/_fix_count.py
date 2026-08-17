# -*- coding: utf-8 -*-
from pathlib import Path
import ast

path = Path(__file__).with_name("_gen_12.py")
src = path.read_text(encoding="utf-8")
mod = ast.parse(src)
bodies = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
print("count", len(bodies))
# drop last duplicate-ish if 151
if len(bodies) == 151:
    bodies = bodies[:150]
# rewrite BODIES assignment by regenerating file ending
# Instead patch: replace list via exec rebuild
helper = path.read_text(encoding="utf-8")
# find BODIES = [ ... ] before # fix
start = helper.index("BODIES = [")
end = helper.index("]\n# fix") + 1
new_list = "BODIES = [\n" + ",\n".join(repr(b) for b in bodies) + "\n]"
helper = helper[:start] + new_list + helper[end:]
# also remove broken fix line dependency - keep fix
path.write_text(helper, encoding="utf-8")
print("rewrote", len(bodies))
