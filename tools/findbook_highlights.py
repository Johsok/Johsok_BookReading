# -*- coding: utf-8 -*-
"""Build the Grok prompt, call xAI, and keep only 001、–150、 lines."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

import findbook_writer as writer

LINE_RE = re.compile(r"^(\d{3})、")
XAI_URL = "https://api.x.ai/v1/chat/completions"
DEFAULT_MODEL = "grok-3"


CHUNK_FOCUS = {
    (1, 75): "核心定義、原理、架構、判斷標準、方法工具",
    (76, 150): "情境案例、風險例外、行動復盤、取捨與應用",
}


def build_prompt(title: str, author: str, start: int = 1, end: int = 150) -> str:
    count = end - start + 1
    start3 = f"{start:03d}、"
    end3 = f"{end:03d}、"
    focus = CHUNK_FOCUS.get((start, end), "本書互不重複的具體重點")
    range_line = (
        f"用繁體中文輸出本書剛好 {count} 個互不重複的具體重點。"
        if start == 1 and end == 150
        else f"用繁體中文輸出本書第 {start} 至 {end} 個互不重複的具體重點，共 {count} 行。"
    )
    focus_line = "" if start == 1 and end == 150 else f"本段聚焦：{focus}。不要寫其他段會覆蓋的內容。\n"
    return f"""書名：{title}
作者：{author}
{range_line}
只輸出 {count} 行，無空行、無前言結語、無 Markdown。
每行格式：三位數編號、頓號、完整重點句。第一行必須是 {start3} 最後一行必須是 {end3}。
編號後直接寫觀念、方法、因果、情境、行動或例子。
{focus_line}禁止分類標籤、步驟標籤、「X面第N步」、「第N步，」、短標籤加冒號、符號「｜」、「本書」、「作者指出」、「本章」。
不要重複書名、作者、章名或固定開頭；不要同義改寫湊數。"""


def extract_highlights(text: str) -> list[str]:
    found: dict[int, str] = {}
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("```"):
            continue
        match = LINE_RE.match(line)
        if not match:
            continue
        number = int(match.group(1))
        if 1 <= number <= 150:
            found[number] = line
    return [found[index] for index in range(1, 151) if index in found]


def call_xai(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }
    request = urllib.request.Request(
        XAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"xAI HTTP {exc.code}: {detail[:400]}") from exc
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError(f"xAI 沒有回傳內容：{body}")
    message = choices[0].get("message") or {}
    return str(message.get("content") or "")


def generate_highlights(
    title: str,
    author: str,
    api_key: str = "",
    model: str = DEFAULT_MODEL,
) -> list[str]:
    key = (api_key or os.environ.get("XAI_API_KEY") or "").strip()
    if not key:
        raise RuntimeError("未提供 xAI API Key，無法呼叫 Grok")
    text = call_xai(build_prompt(title, author), key, model=model or DEFAULT_MODEL)
    return extract_highlights(text)


def write_highlights(root: Path, book_id: str, highlights: list[str]) -> dict:
    """Write extracted lines without running findbook_writer.complete()."""
    root = Path(root).resolve()
    manifest = writer.read_json(root / "data.json")
    matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
    if len(matches) != 1:
        raise RuntimeError(f"{book_id} 在 data.json 必須剛好出現一次")
    relative_file = str(matches[0]["file"])
    book_path = root / relative_file
    book = writer.read_json(book_path)
    cleaned = extract_highlights("\n".join(highlights if isinstance(highlights, list) else []))
    if not cleaned:
        cleaned = extract_highlights("\n".join(str(item) for item in highlights))
    if len(cleaned) != 150:
        raise RuntimeError(f"{book_id} 擷取到 {len(cleaned)} 點，必須剛好 150")
    book["chatgptHighlights"] = cleaned
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "grok"
    book["highlightsCapturedAt"] = writer.now_iso()
    book["updatedAt"] = writer.now_iso()[:10]
    writer.write_json_atomic(book_path, book)
    writer.check_index_link(root, book_id)
    saved = writer.read_json(book_path)
    return {
        "id": book_id,
        "file": relative_file,
        "count": len(saved.get("chatgptHighlights") or []),
    }
