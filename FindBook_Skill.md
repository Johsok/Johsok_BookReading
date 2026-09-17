# FindBook Skill：書籍重點整理 SOP

本文件是找中文書、登記索引、以 Cursor Grok Extra High 產出 150 點的唯一操作規格。只跑這一份，不要另開 SOP、不要開平行計畫。

執行模型：Cursor Agent（Grok Extra High）。不用 Codex、不用 ChatGPT 網頁、不用較快但較弱的子模型寫重點。`chatgptHighlights`、`chatgptStatus` 只是 `index.html` 相容欄位名。

目標：4 類 × 5 本（20 本）應在約 5 分鐘內完成，品質與既有 150 點規格相同。時間不夠時先砍搜尋與調度開銷，不得減點數、不得改用英文書、不得叫較弱模型。

## 5 分鐘路徑（預設照做）

| 分鐘 | 動作 | 禁止 |
|---|---|---|
| 0–1 | 只讀 `data.json` 建去重索引；解析主題／本數／日期／`workId` | 讀 `Books/**`、問已能推得的問題 |
| 1–2 | 一次 `scraper.py --commit --hant`（經典長區間自動走讀冊經典榜） | `--out`、候選檔、瀏覽器、`WebFetch`、手補書單 |
| 2–5 | 同一則訊息啟動**全部** committed 書的 Task（1 本 = 1 路 = 150 點） | 父 agent 自己寫 150 點、分波等待、子 agent 回傳全文、再探路數 |

父 agent 只做：解析 → scrape+commit → 派 Task → 收 `WRITTEN id 150` → 抽查本批 ID 的索引連結。不要在找書階段整理重點。

## 解析指令（缺了才問，一次問完）

從當次指令讀 4 項；能推得就不要問：

1. 主題：「前 N 個主題」= `01` 起連續 N 類。未寫則 7 類都做。
2. 每類本數：未寫則 1。
3. 日期：`YYYY-MM-DD`～`YYYY-MM-DD`。相對「N 年前–M 年前」→ `from=今天-M 年`、`to=今天-N 年`（同月日；2/29 改 2/28）。未寫則最近 30 天。
4. 單工：只有使用者寫「單工」才單工；否則一次派完全部書。

指定「繁體」時：只收繁中書名，scraper 加 `--hant`，不要改走簡中站補額。

主題對照：

- `01_商業理財` → `01_business_startup`
- `02_心理勵志` → `02_psychology_growth`
- `03_自然科學` → `03_natural_science`
- `04_醫療保健` → `04_healthcare`
- `05_飲食養生` → `05_food_wellness`
- `06_電腦資訊` → `06_computer_info`
- `07_其他` → `07_other`

`workId`：`findbook-YYYYMMDD-HHMM`（台北時間，本批只建一次）。

## 加速硬規則

1. **禁止全庫讀檔**：只讀 `data.json` 建「書名+作者」、ISBN（若有）、`id`、`file` 索引。只有本批 pending／續跑的單書檔可開。
2. **禁止人工抓書**：找書只准跑 `tools/findbook_scraper.py`。禁止瀏覽器、禁止對候選 `WebFetch`、禁止手寫書單、禁止再掃 B–E 組網站。scraper 不足就再跑**同一命令一次**；仍不足則據實回報缺額並結束，不得降級收英文或新書。
3. **禁止額外檔**：不要寫 `tools/.findbook_*`、不要 `--out`、不要暫存 `.py`／`.txt` 重點檔。正式輸出只有 `data.json` 與 `Books/{categoryId}/{book-id}.json`。
4. **禁止父 agent 寫 150 點**：必須 Task 子 agent、`model` 與父層相同（Extra High）。同一則訊息一次丟出本批全部書；`run_in_background=true`。同時上限 `min(20, 待處理書數)`。超過 20 本才允許第二波。不要從 2 或 6 路試上去。
5. **禁止子 agent 回傳 150 行全文**：子 agent 寫入該書 JSON 後只回 `WRITTEN {id} 150`。父層禁止把重點全文讀進對話。
6. **禁止雙讀等待、禁止為摘要再開模型**：編號行到齊就擷取；`summary` 用固定句。
7. **禁止收尾全庫掃描**：只核對本批 committed ID。不要 `rglob Books/`。
8. **禁止慣例驗證**：不要跑 `findbook_guard.py queue`、內容 `validate`、150 點格式檢查、HTTP 檢查、UI 測試。只有使用者當次要求「驗證／測試」才加做。寫入走 `findbook_highlights.py write`，不要走會做內容驗收的 `complete`。

## 中文書籍

1. 只收中文書；書名至少一個漢字。指定繁體時，簡體獨有字形不合格。作者或必要術語可用英文；純英文／羅馬拼音書名不合格。
2. 必須用來源頁實際中文書名，不得自翻英文書名，也不得用英文版湊額。
3. 單一平台缺書不代表可改收英文書。

## 找書與登記（一次命令）

經典／長區間（跨度 ≥ 2 年，或截止日期早於一年前）由 scraper 走讀冊歷年／年度暢銷百大；達 `quota+1` 即停，不打新書榜。新書 30 天模式才走博客來列表。

```text
python tools/findbook_scraper.py --root . --category-ids <id1,id2,...> --quota <每類本數> --from-date YYYY-MM-DD --to-date YYYY-MM-DD --commit --work-id <workId> [--hant]
```

stdout 的 `committed` 陣列就是本批書單。不要再呼叫 `findbook_writer.py reserve`，除非 `--commit` 不可用。

去重鍵：ISBN（有則優先）→ 正規化「書名+作者」。已在庫的書不抵扣新批次配額，改收下一本。`data.json` 是 reservation 唯一權威來源。

每次把新書寫入 `data.json` 後，必須立刻依出版日期重排再落盤，不得維持抓取順序。規則：

1. 先依 `categories` 的系列順序（`01`→`07`）分組。
2. 同一系列內依 `published` 由新到舊（完整 `YYYY-MM-DD` 優先於僅年份 `YYYY`；僅年份視為該年 `01-01`）。無出版日期的書排在該系列最後。
3. 索引列與單書 JSON 都必須寫入 `published`（`YYYY-MM-DD` 或僅年份 `YYYY`）。來源依序：scraper 出版日期 → `sourceDateNote` → 博客來商品頁／書名搜尋 → momo 圖書搜尋。必須對到同一書名（短書名還要比對作者），不得套用書名相近的其他書。兩邊都找不到就留空並排該系列最後，據實回報，不得捏造日期。
4. 只准透過 `findbook_writer.py` 的 reservation 寫入；writer 已內建 `sort_manifest_books`，禁止手改 `data.json` 順序。

新批次：使用者再說「找新書／新增」就是新 `workId`，即使條件與上次相同也要重新湊滿配額。只有「續跑／驗證／不新增」或同一 `workId` 仍 pending 才續跑。`chatgptStatus: complete` 略過；pending 只補缺的 150 點。

## 分類

每本只歸 7 類之一；其餘放 `tags`。

1. 投資、創業、職涯、管理 → `01_business_startup`
2. 習慣、情緒、人際、自我成長 → `02_psychology_growth`
3. 物理、宇宙、生物、數學、科普 → `03_natural_science`
4. 疾病、醫療、心理健康、照護 → `04_healthcare`
5. 食譜、營養、減脂、代謝、養生 → `05_food_wellness`
6. AI、程式、資料、演算法、軟體工具 → `06_computer_info`
7. 歷史、文化、文學、生活雜學或不屬前六類 → `07_other`

## 亂碼閘門

適用書名、作者、來源、摘要、標籤、Grok 每一行。有亂碼必須先修，才能 reservation／送 Grok／寫正式檔。

快路徑：通順中文且無下列特徵 → 直接過。

判定：`U+FFFD`、大量 `?`／`□`／`锟斤拷`／`ï¿½`；UTF-8 當 Latin-1（`ÃÂåæç`）；Big5／GBK 錯解；未還原 `&#x`／`&amp;`；`\uXXXX`、控制字元。僅繁簡／全半形／標點差異不算。

修正（成功即停）：HTML 實體 → charset 重解（utf-8／big5／gbk）→ latin-1 再 utf-8 → 原 URL 重抓一次。Grok 亂碼：該書 Task 重派 1 次；仍失敗則誠實 pending，不得用亂碼湊 150。

## 150 點：1 本 1 Task

未指定單工時：**1 本書 = 1 個 Task = 1 次產出 150 點**。兩段焦點寫在同一提示裡（維持舊品質，但少一半調度）。不要切成 001–075／076–150 兩個 Task，除非使用者要求切段或該書缺號重跑。

子 agent 規格（整段放進 Task `prompt`；把該本 committed 物件的欄位填進去，父層不必再開單書檔）：

```text
你只處理一本書的 150 個重點。禁止 Read、Grep、Glob、WebFetch、瀏覽器，禁止讀 data.json，禁止開其他書，禁止另存檔。
用 Write 覆寫這個檔，寫入完整合法 JSON（含下列欄位，不得省略）：
path={file}
id={id}；categoryId={categoryId}；title={title}；author={author}
sourceName、sourceUrl、sourceDateNote、searchDateRange、tags、summary、workId 用父層提供的值。
chatgptHighlights 必須剛好 150 條字串；chatgptStatus=complete；highlightsSource=grok；highlightsCapturedAt=台北時間 ISO；updatedAt=YYYY-MM-DD。

書名：{title}
作者：{author}
用繁體中文輸出本書剛好 150 個互不重複的具體重點。
只把這 150 行放進 chatgptHighlights，不要寫進對話。
每行格式：三位數編號、頓號、完整重點句。第一行必須是 001、最後一行必須是 150、。
001–075：核心定義、原理、架構、判斷標準、方法工具。
076–150：情境案例、風險例外、行動復盤、取捨與應用。
編號後直接寫觀念、方法、因果、情境、行動或例子。
禁止分類標籤、步驟標籤、「X面第N步」、「第N步，」、短標籤加冒號、符號「｜」、「本書」、「作者指出」、「本章」。
不要重複書名、作者、章名或固定開頭；不要同義改寫湊數。

寫入後設定 chatgptStatus=complete、highlightsSource=grok、highlightsCapturedAt=台北時間 ISO、updatedAt=YYYY-MM-DD。
最後只回一行：WRITTEN {id} 150
若寫入失敗，改把 150 行當純文字回傳，仍不要加前言。
```

單工（僅使用者指定時）由父 agent 用同一提示產出 150 行，再：

```text
python tools/findbook_highlights.py write --root . --book-id {id}
```

stdin 為 150 行。不要用 `findbook_writer.py complete`。

擷取規則：只留 `001、` 到 `150、`。缺號只重跑該書 1 次。不跑本地內容驗收器；亂碼仍要擋。

## 寫入 JSON

reservation 已由 scraper `--commit` 寫入 pending 骨架。150 點完成時只更新該書檔，不新增索引、不重寫其他書。`summary` 固定：

```text
整理「{書名}」在{分類中文名}領域的核心觀念、判斷方法、適用情境與可實踐行動。
```

```json
{
  "id": "book-id",
  "categoryId": "01_business_startup",
  "title": "書名",
  "author": "作者",
  "sourceName": "來源榜單",
  "sourceUrl": "https://example.com",
  "sourceDateNote": "出版日期、上架日期、榜單日期或來源未提供明確日期",
  "published": "YYYY-MM-DD",
  "searchDateRange": { "from": "YYYY-MM-DD", "to": "YYYY-MM-DD" },
  "tags": ["標籤"],
  "summary": "短摘要",
  "updatedAt": "YYYY-MM-DD",
  "chatgptHighlights": ["001、...", "...", "150、..."],
  "chatgptStatus": "complete",
  "highlightsSource": "grok",
  "highlightsCapturedAt": "YYYY-MM-DDTHH:mm:ss+08:00"
}
```

索引連結：`file` 必須是 `Books/{categoryId}/{book-id}.json`（正斜線、大小寫一致）。單書與索引的 `id`、`categoryId`、`title`、`author` 必須相同；該 ID 與 `file` 在 `data.json` 各只出現一次。索引列需含 `published`（有來源日期時）。批次結束只核對本批 committed ID，確認 `totalBooks === data.json.books.length`，並確認各系列已依 `published` 由新到舊排列。異常先保留現況並回報，不得用別本書覆寫。

同一 `workId` 的 pending 檔還沒進索引時，只能依原 checkpoint 補原列；相反則補回 pending 檔。不得從檔名猜書名或分類。
