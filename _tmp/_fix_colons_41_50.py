# -*- coding: utf-8 -*-
import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
PAT = re.compile(r'^"([^：:]{1,12})[：:](.*)",\s*$')
ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
FILES = [
    "_tmp/hl_06_46.py",
    "_tmp/hl_06_47.py",
    "_tmp/hl_06_48.py",
    "_tmp/hl_06_49.py",
    "_tmp/hl_06_50.py",
    "_tmp/write_06_41_50.py",
]


def main() -> None:
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        changed = 0
        out = []
        for line in path.read_text(encoding="utf-8").splitlines(True):
            raw = line.rstrip("\r\n")
            match = PAT.match(raw)
            if match and not match.group(1).endswith(NATURAL):
                label, rest = match.group(1), match.group(2)
                new = f'"談到{label}，{rest}",'
                nl = "\n" if line.endswith("\n") else ""
                out.append(new + nl)
                changed += 1
            else:
                out.append(line)
        path.write_text("".join(out), encoding="utf-8")
        print(rel, changed)


if __name__ == "__main__":
    main()
