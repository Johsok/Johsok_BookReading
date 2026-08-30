# -*- coding: utf-8 -*-
import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
COLON_RE = re.compile(r"^([^：:]{1,12})([：:])")

EXTRA04 = [
    "吉竹伸介畫的離開貼紙只是視覺鉤子，鉤子要配上鬆臉，才不會變成新的裝飾。",
    "裝飾再可愛，若沒有離開的動作，貼紙只是另一張冰箱風景。",
    "風景改成制約要兩到三個月，期間關節痛減輕就算成績，不必等零接觸才慶祝。",
]


def fix_body(body: str) -> str:
    body = body.replace("整本書", "整冊")
    body = body.replace("同一本書", "同一冊")
    body = body.replace("第一本書", "第一冊")
    body = body.replace("三本書", "三冊")
    body = body.replace("一本書", "一冊")
    body = body.replace("本書", "冊子")
    match = COLON_RE.match(body)
    if match and not match.group(1).endswith(NATURAL):
        body = body[: match.start(2)] + "，" + body[match.end(2) :]
    return body


def rewrite(name: str) -> None:
    path = Path(__file__).resolve().parent / name
    namespace: dict = {}
    exec(path.read_text(encoding="utf-8"), namespace)
    bodies = [fix_body(item) for item in namespace["BODIES"]]
    if name == "_hl_g04.py":
        bodies.extend(EXTRA04)
    seen: set[str] = set()
    unique: list[str] = []
    for item in bodies:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    lines = ["# -*- coding: utf-8 -*-", "BODIES = ["]
    for item in unique:
        lines.append(f"    {item!r},")
    lines.append("]")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(name, len(unique))


if __name__ == "__main__":
    for filename in ("_hl_g12.py", "_hl_g13.py", "_hl_g14.py", "_hl_g04.py"):
        rewrite(filename)
