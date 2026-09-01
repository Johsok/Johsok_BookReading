# FindBook Skill：書籍重點整理 SOP

本文件是找中文書、登記索引、以 Cursor Grok 4.6 產出 150 點的唯一操作規格。重複敘述已合併；執行時依本文件一次跑完，不要另開平行 SOP。

本流程使用 Cursor Agent（Grok 4.6）。不使用 Codex，也不使用 ChatGPT 網頁版。`chatgptHighlights`、`chatgptStatus` 只是 `index.html` 相容欄位名稱。

## 預設原則

1. 找書、下載資料與重點整理完成後，直接修改 `data.json` 與對應的 `Books/{categoryId}/{book-id}.json`。
2. 平時不得主動執行 `queue`、`validate`、重點格式檢查、去重報告、HTTP 檢查或 UI 冒煙測試。輸出格式、分類、日期、中文書名、去重、亂碼修正與「索引連結完整性」是產生／提交資料時必須直接遵守的規格，不是額外內容驗收階段。
3. 只有使用者當次明確要求「驗證」、「測試」或指定檢查項目時，才做相應的額外驗證；不得因慣例、風險或先前批次而自行追加。
4. 若 helper 或 writer 入口會自動跑內容驗收，改用不含內容驗收的原子寫入；不得略過亂碼閘門與索引連結完整性。
5. 不執行 `tools/findbook_guard.py queue`、內容型 `validate`、150 點格式檢查、HTTP 檢查或 `index.html` UI 測試。JSON 可解析性、數量核對、索引一致性與 ID／路徑唯一性只依「索引連結完整性」執行。

## 加速硬規則

速度優先於掃站完整度。下列禁止事項會把整批拖慢，執行時必須遵守：

1. **禁止全庫讀檔**：啟動只讀 `data.json` 建立正規化「書名 + 作者」、ISBN（若有）、`id`、`file` 索引。不得依索引把 `Books/**/*.json` 全部讀進記憶體。只有本批次 pending／續跑的單書檔才許開啟。
2. **禁止逐頁人工抓書**：找書必須先跑 `tools/findbook_scraper.py`（可一次多分類、列表頁平行）。不得用瀏覽器點選，也不得對每本候選 `WebFetch` 詳情頁。scraper 達配額後立刻 reservation，不得再掃其餘站。
3. **禁止等搜尋結束才整理**：第一本 `committed` 後，同一回合就啟動該書 150 點；搜尋、reservation、Grok 必須流水線重疊。
4. **禁止父 agent 逐本自己寫 150 點**：必須用 Cursor Task 子 agent 平行產出；同一則訊息一次啟動本回合全部生成槽。
5. **禁止從 2 路探測多工**：未指定單工時，`grokMaxWorkers` 直接用 `min(6, 待處理書數 × 2)`，不從 2 開始加。
6. **禁止雙讀等待**：Grok 回覆已含該段應有編號行就擷取，不必連續兩次內容相同。
7. **禁止批次結束全庫掃描**：結束只檢查本批次 committed ID。不得 `rglob` 整個 `Books/`，不得讀未涉及的單書 JSON。全庫檢查只在使用者要求驗證時執行。
8. **禁止為摘要再開模型**：`summary` 用固定一句模板即可，不另請 Grok 寫摘要。

## 使用時先確認

從使用者指令解析下列 4 項；只問缺少且沒有預設值的項目，缺項必須一次問完：

1. 這次要找哪些主題？
2. 每個主題各需要幾本新書？
3. 要搜尋哪一段日期區間？
4. 是否限制為單工；未指定時自動使用目前已知的穩定多工上限。

日期區間：`YYYY-MM-DD` 至 `YYYY-MM-DD`。未指定時預設最近 30 天內的新書、暢銷書或熱門書。未指定多工時預設啟用穩定多工，不另外詢問。

主題（標籤 → `categoryId`）：

- `01_商業理財` → `01_business_startup`
- `02_心理勵志` → `02_psychology_growth`
- `03_自然科學` → `03_natural_science`
- `04_醫療保健` → `04_healthcare`
- `05_飲食養生` → `05_food_wellness`
- `06_電腦資訊` → `06_computer_info`
- `07_其他` → `07_other`

## 中文書籍硬性規則

1. 只收中文書，繁體與簡體皆可；書名至少必須有一個漢字。作者、品牌或必要英文術語可用英文；純英文、羅馬拼音或其他非中文書名不合格。
2. 必須使用來源頁實際刊載的中文版本書名，不得把英文原書名自行翻譯成中文書名，也不得用英文版補足配額。
3. 單一平台缺書不代表可改收英文書。列表頁就要檢查中文書名；不合格就淘汰。既有資料中的純英文書名不得作為新批次候選或配額成果。

## 書籍名稱來源（加速、去重）

目標是儘快湊滿中文書配額，不是掃完所有網站。列表頁已有「中文書名 + 作者 + 連結」就夠用；同一本書只保留一個來源頁。沒有作者的列表列直接跳過，不要為它開詳情，除非該類仍缺額且 scraper 已聲明需要補作者。

### 同一平台只查一次（別名）

下列名稱指向同一通路，查過其中一個就不要再查別名：

| 正規名稱 | 勿重複查的別名 |
|---|---|
| 博客來 | books.com.tw、博客來電子書、博客來暢銷／新書／週榜／月榜（同一 ISBN 只取一筆） |
| 金石堂 | Kingstone |
| 讀冊 | TAAZE、taaze.tw |
| 誠品 | 誠品線上、誠品書店、誠品人、eslite |
| momo 圖書 | momoshop 圖書類（只抓圖書，不抓一般商品） |
| 讀墨 | Readmoo、灰熊愛讀書 |
| 三民 | 三民書局、sanmin |
| 國家書店 | 政府出版品、govbooks |
| BookWalker | 書行者繁中 |
| 豆瓣讀書 | 豆瓣書、book.douban.com |
| 當當 | dangdang 圖書 |
| 京東圖書 | jd.com 圖書頻道 |
| 文軒 | 文軒網、winxuan |
| 國圖書目 | 國家圖書館、NBINet、全國圖書書目（只校正書名／ISBN，不當配額來源） |
| Google Books | Google 圖書（只校正書名／作者／ISBN，不當配額來源） |

出版社官網（天下、遠流、時報、聯經、中信等）常與通路重複，只在通路配額不足時補缺。

### 查詢順序（達配額即停）

找書入口固定為一次呼叫 scraper，分類可平行：

```text
python tools/findbook_scraper.py --root . --category-ids <id1,id2,...> --quota <每類本數> --from-date YYYY-MM-DD --to-date YYYY-MM-DD --out tools/.findbook_candidates_<workId>.json
```

**A 組**：scraper 內建博客來 →（不足才）金石堂／讀冊。博客來列表通常已有書名與作者，是主來源；該類達配額後 scraper 必須立刻停，不得再打其他站。

**B 組（scraper 仍不足才開）**：誠品、momo 圖書列表頁。仍只抓列表，不開詳情。

**C 組（B 組仍不足）**：三民、國家書店、讀墨、BookWalker、Pubu、HyRead、Kobo 繁中。

**D 組（C 組仍不足）**：豆瓣讀書、當當、京東圖書、文軒；香港商務印書館／三聯新書（繁中補缺）。

**E 組（不找新書）**：國圖書目、Google Books。只在書名亂碼、作者缺漏、ISBN 對照時使用。

規則：

1. 各分類平行；有效新書達到該類配額後，立刻停止該類其餘搜尋。不要五站同時打滿。
2. 跨平台去重鍵依序為：ISBN（有則優先）→ 正規化「書名 + 作者」。同一本書出現在多站時，保留最先通過亂碼快路徑且資料最完整的一筆，不要開第二個詳情頁。
3. 候選緩衝最多「需求數 + 1」。因日期、重複、亂碼修不好或資料不足被淘汰時，只按缺額補找。
4. 列表已有日期才用來判斷搜尋區間；沒有日期仍可列入，`sourceDateNote` 標註「來源未提供明確日期」。不要為了補日期而開詳情。
5. 每筆至少記錄：書名、作者、來源網站、來源網址、榜單名稱、擷取日期、日期區間、來源日期說明。列表沒有 ISBN 就不要另查。

## 亂碼文字閘門

抓到任何文字後，**必須先判斷是否有亂碼；有亂碼就要先修正，才能進入下一步**。這是資料可用性條件，不是內容驗收，不得略過。

適用欄位：書名、作者、來源名稱、日期說明、摘要、標籤、Grok 回覆的每一行。適用時機：列表擷取後、詳情擷取後、Grok 回覆擷取後、寫入 JSON 前。任一步仍有亂碼，就停在該步，不得 reservation、不得送 Grok、不得把亂碼寫進正式檔。

### 快路徑

書名／作者已是通順中文（繁或簡），且沒有下列亂碼特徵時，直接通過，不要做重解碼、重抓或 E 組對照。

### 判定

出現任一情況即視為亂碼：

1. 替換字 `U+FFFD`、大量 `?`／`□`／`¿`，或可見的 `锟斤拷`、`ï¿½`。
2. 中文書名或作者出現典型錯碼：UTF-8 被當成 Latin-1／CP1252（`Ã`、`Â`、`å`、`æ`、`ç` 等夾在應為漢字的位置）；Big5／GBK 錯解（`涓`、`鍙`、`鏌` 這類無意義連續漢字）；或 HTML 實體未還原（`&#x`、`&amp;` 出現在書名正文）。
3. 可見的 `\uXXXX`、控制字元、或同一欄位正常漢字與無意義拉丁亂碼混雜。
4. 解碼後書名仍無法讀成通順中文（繁或簡），或漢字被拆成無意義片段。

僅有繁簡轉換、全形半形、常見標點差異，不算亂碼。

### 修正（依序，成功即停止）

1. HTML 實體還原，去掉 BOM 與多餘空白。
2. 用該次回應的 `Content-Type` charset、頁面 `meta charset` 重解 bytes；依序嘗試 `utf-8`、`utf-8-sig`、`big5`、`big5hkscs`、`gbk`、`gb18030`。
3. 嘗試常見雙重編碼：先當 `latin-1`／`cp1252` 編碼再以 `utf-8` 解碼。
4. 以原 URL 重抓一次，強制正確 charset。
5. 書名／作者仍亂碼時，用 ISBN 或可辨識片段到 E 組或 A 組另一站取正確中文書名與作者，再寫回本筆。
6. Grok 重點亂碼時：不得寫入；視為傳輸失敗，只重送該段 1 次。仍亂碼則保持 pending，改找或稍後續跑，不得用亂碼湊 150 點。

修正後必須再跑一次判定；仍不合格就淘汰該候選並補找下一本，不得把「看起來差不多」的亂碼書名送進去重或提示詞。

## 新批次與續跑判定

1. 使用者每次重新提出「找新書」或「新增新書」，都是全新批次；即使主題、配額、日期與先前相同，也必須重新完成本次全部新書配額。
2. 每個全新批次啟動時配置唯一 `workId`。是否同一批次只依 `workId` 判斷，不得用日期、主題、配額、提示詞、`queue=0`、`generatedFrom` 或既有完成數量推定。
3. 既有書籍只用於正規化「書名 + 作者」（及 ISBN）去重，不得抵扣新批次配額；已存在就改找下一本，直到各分類配額完成。
4. 只有使用者明確要求「續跑」、「驗證」或「不新增」，或目前存在同一 `workId` 的 pending 工作時，才可停止建立新批次並改為續跑。

## 快速執行總流程

1. 啟動只讀 `data.json`，建立正規化「書名 + 作者」索引、ISBN 索引、ID 索引。Grok 狀態只看本批次即將處理的單書檔（全新批次在 reservation 後才讀該檔）。每次新書登記成功後立即更新共享索引。
2. 依「新批次與續跑判定」確認意圖：全新找書先配置 `workId` 並建立完整新書配額；只有明確續跑或同一 `workId` 尚有 pending 時才進入狀態式續跑。
3. 續跑時，`chatgptStatus: complete` 的書直接略過；仍為 pending 的書只排入 Grok 佇列。只有可明確判定為中斷造成的索引缺漏可依 checkpoint 修復；其他結構異常先隔離回報，不得自動覆寫。
4. 立刻跑 scraper（多分類平行）。合格候選按類一次交給 reservation writer；`committed` 的書同一回合送 Grok 兩段並行。搜尋缺額、Grok 與寫入必須重疊。
5. worker 只回傳隔離結果；一段或全書 150 點通過亂碼快路徑後，立即交由單一 result writer 寫入該書 JSON，不得為了湊批次延後保存。
6. 全部 writer 停止寫入後，只對本批次 committed ID 做索引連結提交檢查再結束。

## 分類規則

1. 每本書只能歸到 7 大主題中的 1 類。可跨類時選最主要閱讀目的，其餘放入 `tags`。
2. 投資、創業、職涯、管理 → `01_business_startup`。
3. 習慣、情緒、人際、自我成長 → `02_psychology_growth`。
4. 物理、宇宙、生物、數學、科普 → `03_natural_science`。
5. 疾病、醫療、心理健康、照護 → `04_healthcare`。
6. 食譜、營養、減脂、代謝、養生 → `05_food_wellness`。
7. AI、程式、資料、演算法、軟體工具 → `06_computer_info`。
8. 歷史、文化、文學、生活雜學或不適合前六類 → `07_other`。

## 多工新書即時登記

1. `data.json` 是去重與 reservation 的唯一權威來源；共享 reservation set 只能當它的記憶體鏡像。
2. 搜尋 worker 找到合格新書後，只能把已通過亂碼快路徑的候選交給單一 reservation writer。worker 不得自行「先查再寫」。
3. reservation writer 在同一個串行臨界區執行 `reload → 亂碼複檢 → normalize → dedupe → allocate ID → prepare → write`：重新載入最新 `data.json`；依中文書名、ISBN 與正規化「書名 + 作者」處理。已存在就回傳既有 ID 並拒絕新增；不存在才配置唯一 ID。
4. 同一 checkpoint 以同一份不可變 reservation payload 建立單書資料與索引列。先原子建立 `Books/{categoryId}/{book-id}.json` pending 骨架，再原子寫入 `data.json`。`data.json.books` 必須立刻寫入完整有效索引列，至少包含 `id`、`title`、`author`、`categoryId`、`tags`、`sourceName`、`sourceUrl`、`file`，並同步更新 `totalBooks`、`generatedFrom`、`generatedAt`。索引列的 `file` 必須精確等於 `Books/{categoryId}/{book-id}.json`。pending 骨架需包含相同的 `id`、`categoryId`、`title`、`author`、完整基本資料、空的 highlights 及相容 pending 狀態。`data.json` 最後寫入，作為 reservation 已提交的標記。
5. writer 只有在該筆索引連結提交檢查通過後才能回傳 `committed + book ID`。Grok worker 收到 committed 後才開始產生重點，後續都以該 ID 為主鍵。
6. 每次 committed 後立即通知所有 worker 使用最新索引。下一個候選仍必須交給 reservation writer 原子檢查。
7. 若 writer 回傳已存在：只有同一 `workId` 且仍為 pending 才排入 Grok 佇列；其他 `workId` 的既有書不計入本次配額，必須改找下一本。
8. 正式流程使用 `tools/findbook_writer.py reserve --category-id <categoryId> ...`。同一分類把本回合候選一次交給 writer，不要一本呼叫一次。不得再向根目錄分類大檔附加資料。

## 索引連結完整性

`index.html` 只透過 `data.json` 的 `file` 載入單書 JSON。唯一合法路徑為 `Books/{categoryId}/{book-id}.json`；一律使用 `/`、保留實際檔名大小寫，不得使用根目錄分類大檔、反斜線、推算路徑或共用另一筆書籍的檔案。

1. 單筆 reservation writer 在串行臨界區完成 `reload → dedupe → allocate ID → build one payload → write book atomically → write manifest atomically → check link → committed`。單書 JSON 與索引列必須從同一份 payload 產生，不得分別重新組合書名、作者、分類或 ID。
2. 單筆 `check link` 只檢查提交完整性：索引路徑存在且可解析、路徑精確符合規則、索引與單書 JSON 的 `id`、`categoryId`、`title`、`author` 完全一致，且該 ID 與 `file` 在 `data.json` 中各自唯一。任一項失敗都不得 committed，也不得送 Grok。
3. 批次結束時先停止派送並等待本批次 reservation／result writer 完成。只核對本批次 committed ID：索引列存在、對應單書檔存在、四欄一致。不要掃整個 `Books/`。
4. 另確認 `totalBooks === data.json.books.length`。結構異常先保留現況並回報書名、ID、目前路徑與預期路徑；不得以第一筆搜尋結果或相似書籍自動覆寫。
5. 同一 `workId` 的 pending 單書檔尚未進入 `data.json` 時，只能依原 reservation checkpoint 補上原索引列；索引已存在但單書檔缺少時，只能依同一 checkpoint 補回 pending 檔。不得從檔名猜測作者、書名或分類，也不得套用其他書的路徑。

## 多工整理與即時寫入

1. 中央排程器維護 Grok 與 retry 兩個佇列。同一批次每個工作都必須帶入該批次 `workId`，並至少包含：書名、作者、分類、來源資訊、`searchDateRange`、`attemptCount`、最後錯誤及 `queued → submitted → captured → written` 狀態。
2. 以 Cursor Task 子 agent（Grok 4.6）啟動 worker；每本書切成兩段獨立工作與獨立結果暫存。worker 不得直接寫正式 JSON。
3. 必須以 reservation writer 已提交到 `data.json` 的 book ID 防止本批次重複；後續用「book ID + workId + 段號」追蹤結果。
4. 同一執行階段只設定一次 `grokMaxWorkers`：預設 `min(6, 待處理書數 × 2)`。使用者指定單工時才改為 1 且不切段。出現限流、品質下降或工作錯置時立即回退 2（一次少一本書）。多工上限以實際 Cursor／Grok 環境為準，不得繞過服務限制。
5. 未指定單工時，每本固定切 2 段並行：`001–075` 與 `076–150`。同時進行的書數 = `max(1, grokMaxWorkers // 2)`。排程採 `dispatch → collect → write`：同一則訊息填滿生成槽，先完成的段先收；兩段齊了立刻合併寫入並補下一本。不得停在第一本慢回覆上，不使用固定長時間 sleep。
6. 該段應有編號行已到齊就擷取，不必等連續兩次相同。擷取後先過亂碼快路徑，再交給 result writer。不檢查內容格式，也不因格式問題要求重做；只有傳輸失敗或亂碼修不好時最多重試該段 1 次，仍失敗就移到 retry 佇列尾端，先釋放 worker。主佇列清空後再處理 retry；仍無法完成者保留誠實的 pending，下次只續跑缺的段。
7. 新書在 Grok 開始前就必須已有 reservation checkpoint。150 點完成時只更新既有骨架，不得再次新增索引。每次只更新本次完成的 `chatgptHighlights`、`chatgptStatus` 與必要來源欄位。
8. writer 先在記憶體組好完整新 JSON（含亂碼複檢），再以同目錄暫存檔替換正式檔。寫入後先做該筆索引連結提交檢查，再把工作狀態改為 `written`。寫入失敗時保留已取得結果並只重試 writer，不得要求 Grok 重新產生。正式寫入使用 `tools/findbook_highlights.py` 的 `write_highlights`，不要走會做內容驗收的 `complete`。
9. 中斷發生在單書 pending 檔已寫、但尚未加入 `data.json` 時，下次依 checkpoint 補索引；相反則補回 pending 單書檔。修復後必須通過該筆索引連結提交檢查。
10. 既有 `chatgptStatus: complete` 的舊版 100 點資料保持相容且不自動重做；本次新完成或使用者指定重做的書籍一律產生 150 點。完成寫入時將 `highlightsSource` 設為 `grok`，並寫入 `highlightsCapturedAt`。未完成時必須使用明確 pending 狀態。

## Grok 重點提示詞

只替換書名、作者與段範圍。提示要短，完整限制只送一次。

全書（僅單工時使用）：

```text
書名：{書名}
作者：{作者}
用繁體中文輸出本書剛好 150 個互不重複的具體重點。
只輸出 150 行，無空行、無前言結語、無 Markdown。
每行格式：三位數編號、頓號、完整重點句。第一行必須是 001、最後一行必須是 150、。
編號後直接寫觀念、方法、因果、情境、行動或例子。
禁止分類標籤、步驟標籤、「X面第N步」、「第N步，」、短標籤加冒號、符號「｜」、「本書」、「作者指出」、「本章」。
不要重複書名、作者、章名或固定開頭；不要同義改寫湊數。
```

兩段並行（預設；各段只輸出自己的編號範圍）：

```text
書名：{書名}
作者：{作者}
用繁體中文輸出本書第 {start} 至 {end} 個互不重複的具體重點，共 {count} 行。
只輸出這 {count} 行，無空行、無前言結語、無 Markdown。
每行格式：三位數編號、頓號、完整重點句。第一行必須是 {start3}、最後一行必須是 {end3}、。
編號後直接寫觀念、方法、因果、情境、行動或例子。
本段聚焦：{focus}。不要寫其他段會覆蓋的內容。
禁止分類標籤、步驟標籤、「X面第N步」、「第N步，」、短標籤加冒號、符號「｜」、「本書」、「作者指出」、「本章」。
不要重複書名、作者、章名或固定開頭；不要同義改寫湊數。
```

段焦點：

- `001–075`：核心定義、原理、架構、判斷標準、方法工具
- `076–150`：情境案例、風險例外、行動復盤、取捨與應用

寫入時只保留 `001、` 到 `150、` 的 150 個重點行。兩段結果按編號合併；缺號只重跑缺的段。格式規則只作為產生時的提示，不執行本地驗收器；擷取後直接寫入，但亂碼仍須先修正。

## 寫入 JSON

結果 writer 依 book ID 與索引列的 `file` 直接更新受影響單書 JSON，不重寫其他書籍或未變動的 `data.json`。新書單書檔先寫入空的 `chatgptHighlights` 與 `pending_grok`；Grok 完成後立即更新。每本完整書籍格式：

```json
{
  "id": "book-id",
  "categoryId": "01_business_startup",
  "title": "書名",
  "author": "作者",
  "sourceName": "來源榜單",
  "sourceUrl": "https://example.com",
  "sourceDateNote": "出版日期、上架日期、榜單日期或來源未提供明確日期",
  "searchDateRange": {
    "from": "YYYY-MM-DD",
    "to": "YYYY-MM-DD"
  },
  "tags": ["標籤"],
  "summary": "短摘要",
  "updatedAt": "YYYY-MM-DD",
  "chatgptHighlights": ["001、...", "...", "150、..."],
  "chatgptStatus": "complete",
  "highlightsSource": "grok",
  "highlightsCapturedAt": "YYYY-MM-DDTHH:mm:ss+08:00"
}
```
