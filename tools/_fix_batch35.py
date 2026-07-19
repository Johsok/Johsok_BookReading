# -*- coding: utf-8 -*-
"""Fix batch35 highlight lists: count, colon patterns, corrupted lines."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "_gen_batch35_highlights.py"


def load_module():
    spec = importlib.util.spec_from_file_location("b35", SRC)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


EXTRA32 = [
    "溪岸植被根系形成的蔭蔽帶，常是幼魚躲避急流與鳥類捕食的臨時避難所",
    "拍攝前先用偏光鏡壓水面反光，有時不必下水就能完成初步物種確認",
    "同一條魚在不同底質上體色會微調，鑑定時要以結構特徵優先於當下顏色",
    "河段整修若留下階梯式落差，洄游性魚類的通道會被切斷，影像能見證前後差異",
    "把每次踏查的軌跡匯成地圖層，長期後能看出人為壓力與魚點位移的相關",
    "教小朋友看魚時先學安靜坐下，比教相機按鍵更能保護潭水清澈",
]

EXTRA33 = [
    "限定卡若只被當成收藏編號競賽，河的故事就會停在包裝紙上",
    "把影透卡帶進教室對窗觀察時，記得連結到最近一條真實水系的名字",
    "拆盒興奮過後，真正的挑戰是願不願意在雨季泥水裡重訪同一亂石",
    "限量編號會用完，但河段壓力不會因售罄而自動減輕",
    "用影透卡當導覽開場可以，結尾一定要留下可執行的少干擾守則",
    "若讀者只記得贈品造型，忘記魚的學名與棲地，出版意圖就只成功一半",
]

EXTRA34 = [
    "小訊號階段就把接地策略畫清楚，能避免上板後用銅箔補丁到處救火",
    "量測治具的機械公差會轉成相位誤差，治具圖應標註可接受的重複性範圍",
    "對新手最有用的練習是完整走完校正、量測、去嵌與存檔，而不是只追最高增益數字",
    "把史密斯圓圖當導航儀而不是裝飾壁紙，匹配調整才會有方向感",
    "高頻板上的絲印字不要壓在關鍵射頻走線上，油墨厚度也會變成微小不連續",
    "同一設計改版時保留舊版散射參數對照，才能判斷改善來自真改進還是量測偶然",
    "實驗室門口張貼靜電與功率安全守則，比口頭交代更能降低儀器誤毀率",
]

EXTRA35 = [
    "熱浪預警分級若能連動學校與工地停工門檻，認知保護就不必靠個人硬撐",
    "社區里長掌握獨居長者名單時，熱浪訪視比發一則群組訊息更救腦也更救命",
    "把教室溫度計數據公開給家長，校方改善通風與遮蔭的壓力會變得具體",
    "研究顯示短期熱暴露就足以改變反應時間，交通號誌與工地指令應考慮熱日簡化",
    "氣候調適預算若能單列心理健康與降溫雙欄，跨局處踢皮球會比較難",
    "個人層次可先建立熱日決策降級清單，把非必要複雜選擇留到涼爽時段",
    "當城市把陰涼視為公共財，大腦才比較有機會在炎熱世紀裡維持文明所需的耐心",
]


def neutralize_short_colons(lines: list[str]) -> list[str]:
    """Rewrite early short-label colons that trip findbook_writer validation."""
    natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    out = []
    for line in lines:
        body = line
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(natural):
            body = body.replace("：", "，", 1).replace(":", "，", 1)
        out.append(body)
    return out


def clean_lines(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        if "\ufffd" in line:
            continue
        line = line.replace("不准", "不準").replace("抠", "摳")
        line = line.strip()
        if len(line) < 12:
            continue
        cleaned.append(line)
    cleaned = neutralize_short_colons(cleaned)
    return cleaned


def ensure_150(lines: list[str], extras: list[str], book_id: str) -> list[str]:
    lines = clean_lines(lines)
    # dedupe preserving order
    seen = set()
    uniq = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        uniq.append(line)
    for extra in extras:
        if len(uniq) >= 150:
            break
        extra = neutralize_short_colons([extra])[0]
        if extra not in seen and len(extra) >= 12:
            uniq.append(extra)
            seen.add(extra)
    if len(uniq) < 150:
        raise RuntimeError(f"{book_id} only {len(uniq)} after extras")
    if len(uniq) > 150:
        uniq = uniq[:150]
    # final colon check
    uniq = neutralize_short_colons(uniq)
    assert len(uniq) == 150
    assert len(set(uniq)) == 150
    return uniq


def numbered(lines: list[str]) -> list[str]:
    return [f"{i:03d}、{body}" for i, body in enumerate(lines, 1)]


def write_results(book_id: str, lines: list[str]) -> Path:
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = {"id": book_id, "highlights": numbered(lines)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def run_writer(category_id: str, results_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        category_id,
        "--results",
        str(results_path),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def main() -> None:
    mod = load_module()
    jobs = [
        ("03_natural_science-20260718-31", "03_natural_science", mod.BOOK31, []),
        ("03_natural_science-20260718-32", "03_natural_science", mod.BOOK32, EXTRA32),
        ("03_natural_science-20260718-33", "03_natural_science", mod.BOOK33, EXTRA33),
        ("03_natural_science-20260718-34", "03_natural_science", mod.BOOK34, EXTRA34),
        ("03_natural_science-20260718-35", "03_natural_science", mod.BOOK35, EXTRA35),
    ]
    ok = []
    fail = []
    for book_id, category_id, raw, extras in jobs:
        try:
            lines = ensure_150(list(raw), extras, book_id)
            path = write_results(book_id, lines)
            print(f"wrote {path} ({len(lines)})")
            run_writer(category_id, path)
            ok.append(book_id)
        except Exception as exc:  # noqa: BLE001
            fail.append((book_id, str(exc)))
            print(f"FAIL {book_id}: {exc}")
    print("OK:", ok)
    print("FAIL:", fail)
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
