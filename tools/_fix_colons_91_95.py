# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).with_name("_gen_91_95.py")
text = p.read_text(encoding="utf-8")


def repl(match: re.Match[str]) -> str:
    return match.group(1) + match.group(2).replace("：", "，").replace(":", "，") + match.group(3)


new = re.sub(
    r"(bodies\": r''' )(.*?)('''\.strip\(\)\.splitlines\(\))",
    repl,
    text,
    flags=re.S,
)
# The pattern above has a mistaken space. Use exact pattern.
new = re.sub(
    r"(\"bodies\": r''')(.*?)('''\.strip\(\)\.splitlines\(\))",
    repl,
    text,
    flags=re.S,
)
p.write_text(new, encoding="utf-8")
print("done")
