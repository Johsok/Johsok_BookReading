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


def build_prompt(title: str, author: str) -> str:
    return f"""書名：{title}
作者：{author}
請用繁體中文，以 ChatGPT 電腦版常見的直接重點整理方式，由 Cursor Grok 4.6 整理本書 150 個重點；每點直接陳述一個具體且有資訊量的觀念、方法、因果、情境、行動或例子，且 150 點各自提供新的內容。
只輸出剛好 150 行，不要加入任何其他文字或空行。
第 1 至 150 行都使用固定三位數編號：001、002、……、150、；第一行必須是 001、，最後一行必須是 150、。
每行只能是「編號、完整重點句」。編號後立刻寫書籍重點正文，中間不得插入任何分類標籤、步驟標籤、面向標籤或包裝前綴。
禁止前言、結語、Markdown、項目符號、模型自述、分類名稱、固定小標、短標籤加冒號及符號「｜」。
嚴格禁止任何「X面第N步」或同型贅詞，例如「實作面第65步，」「決策面第74步，」「復盤面第70步，」「風險面第71步，」「溝通面第72步，」「節奏面第73步，」「指標面第74步，」「資源面第75步，」「驗證面第76步，」「習慣面第77步，」「邊界面第78步，」「回饋面第79步，」「優先面第80步，」「備援面第81步，」「學習面第82步，」；也禁止「第N步，」「XX面向，」「面向N，」等變體。
正確示例：065、釐清納瓦爾寶典情境中的關鍵取捨時，記住先界定要解決的價值問題，再選擇工具與資源配置方式。
錯誤示例：065、實作面第65步，釐清納瓦爾寶典情境中的關鍵取捨時，記住先界定要解決的價值問題，再選擇工具與資源配置方式。
正文不要重複書名、作者或章節名稱，不要使用「本書」、「作者指出」、「本章」、「這一章」、「第X章」等來源前綴，也不要讓多點使用相同開頭或固定句型。
同一本書的 150 點不得反覆出現相同的包裝字眼或句段，例如「從《書名》的閱讀情境……的課題時」、「在《書名》的脈絡中」、「以……為閱讀線索」、「處理《書名》相關選擇時特別容易被忽略」、「釐清核心課題時，記住」；每點必須直接從該點獨有的核心內容開始。
不得用同義改寫、重排字句、輪替標籤或反覆說明同一觀念來湊滿 150 點；相鄰或分散的重點都不可語意重複。"""


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
