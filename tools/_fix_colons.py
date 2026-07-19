# -*- coding: utf-8 -*-
"""Replace short-label colons at line starts inside RAW blocks of a gen script."""
import re
import sys
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def fix_raw(text: str) -> str:
    start = text.index('RAW = """') + len('RAW = """')
    end = text.index('"""', start)
    raw = text[start:end]
    lines = raw.splitlines()
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append(ln)
            continue
        m = re.match(r"^([^：:]{1,12})[：:]", s)
        if m and not m.group(1).endswith(NATURAL):
            s = re.sub(r"^([^：:]{1,12})[：:]", r"\1，", s, count=1)
            # preserve original indent if any
            indent = ln[: len(ln) - len(ln.lstrip("\n"))]
            # simpler: just use the stripped fixed line
            out.append(s)
        else:
            out.append(ln if not ln.strip() else s if ln.strip() == s else ln)
    # rebuild carefully
    fixed_lines = []
    for ln in lines:
        if not ln.strip():
            fixed_lines.append("")
            continue
        s = ln.strip()
        m = re.match(r"^([^：:]{1,12})[：:]", s)
        if m and not m.group(1).endswith(NATURAL):
            s = re.sub(r"^([^：:]{1,12})[：:]", r"\1，", s, count=1)
        fixed_lines.append(s)
    new_raw = "\n" + "\n".join(fixed_lines) + "\n"
    return text[: start] + new_raw + text[end:]


def main() -> None:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    path.write_text(fix_raw(text), encoding="utf-8")
    print("fixed", path)


if __name__ == "__main__":
    main()
