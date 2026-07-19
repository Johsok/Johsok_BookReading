# -*- coding: utf-8 -*-
from pathlib import Path

HERE = Path(__file__).parent


def load_lines(module_name: str) -> list[str]:
    text = (HERE / module_name).read_text(encoding="utf-8")
    start = text.index("LINES = [")
    end = text.index("\nassert ")
    ns: dict = {}
    exec(text[start:end], ns, ns)
    return list(ns["LINES"])


def write(name: str, lines: list[str]) -> None:
    assert len(lines) == 150, (name, len(lines))
    assert len(set(lines)) == 150, (name, "dup")
    (HERE / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", name, len(lines))


write("b37", load_lines("make_b37.py")[:150])
write("b38", load_lines("make_b38.py"))

b39 = load_lines("make_b39.py")
extra39 = [
    "低卡韓式雞胸沙拉杯，醬汁分裝避免生菜提早軟掉",
    "微波嫩蛋豆腐，用筷子劃開再淋低糖醬油芝麻",
    "鮪魚泡菜豆腐煲杯，午間加熱香氣足但不油",
    "豆芽香菇雞絲，纖維與蛋白同口，飽足來得快",
    "韓式黃瓜冷湯加雞胸絲，夏天消暑又不空洞",
    "低脂起司蘑菇杯，融化後鹹香能壓住嘴饞",
]
assert len(b39) + len(extra39) >= 150, len(b39)
write("b39", (b39 + extra39)[:150])

b40 = load_lines("make_b40.py")
if len(b40) < 150:
    b40.append("平底鍋洋蔥蘑菇炒蛋，十五種核心裡最快的營養晚餐之一")
write("b40", b40[:150])
