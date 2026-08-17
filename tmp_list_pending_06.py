# -*- coding: utf-8 -*-
"""List computer_info books still using template highlights."""
import json
import glob

files = sorted(glob.glob(r"Books\06_computer_info\06_computer_info-*.json"))
pending = []
done_grok = []
other = []

for path in files:
    raw = open(path, encoding="utf-8-sig").read()
    data = json.loads(raw)
    highlights = data.get("chatgptHighlights", [])
    joined = "".join(highlights[:5]) if highlights else ""
    is_template = False
    if highlights:
        if "為閱讀線索" in joined or "以閱讀線索" in joined:
            is_template = True
        elif (
            "先定義使用情境與成功指標" in highlights[0]
            and "閱讀時可先確認作者如何定義問題" in highlights[0]
        ):
            is_template = True
        elif (
            "閱讀時可先確認作者如何定義問題" in joined
            and "可把觀點轉成一個具體案例" in joined
        ):
            is_template = True
    src = data.get("highlightsSource")
    info = {
        "id": data.get("id"),
        "title": data.get("title"),
        "author": data.get("author"),
        "file": path.replace("\\", "/"),
        "src": src,
        "n": len(highlights),
        "tags": data.get("tags", []),
        "summary": data.get("summary", ""),
    }
    if is_template:
        pending.append(info)
    elif src == "grok":
        done_grok.append(info)
    else:
        other.append(info)

out = {
    "pending": pending,
    "done_grok_count": len(done_grok),
    "other": other,
}
with open("tmp_pending_06.json", "w", encoding="utf-8") as handle:
    json.dump(out, handle, ensure_ascii=False, indent=2)

lines = [f"pending={len(pending)} done_grok={len(done_grok)} other={len(other)}"]
for index, item in enumerate(pending, 1):
    lines.append(f"{index:03d}\t{item['id']}\t{item['title']}")
with open("tmp_pending_06.txt", "w", encoding="utf-8") as handle:
    handle.write("\n".join(lines))
print(lines[0])
print(f"wrote tmp_pending_06.json and tmp_pending_06.txt")
