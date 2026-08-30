# FindBook Skill：書籍重點整理 SOP

本文件是找中文書、登記索引、以 Cursor Grok 4.6 產出 150 點的唯一操作規格。重複敘述已合併；執行時依本文件一次跑完，不要另開平行 SOP。

本流程使用 Cursor Agent（Grok 4.6）。不使用 Codex，也不使用 ChatGPT 網頁版。`chatgptHighlights`、`chatgptStatus` 只是 `index.html` 相容欄位名稱。

## 預設原則

1. 找書、下載資料與重點整理完成後，直接修改 `data.json` 與對應的 `Books/{categoryId}/{book-id}.json`。
2. 平時不得主動執行 `queue`、`validate`、重點格式檢查、去重報告、HTTP 檢查或 UI 冒煙測試。輸出格式、分類、日期、中文書名、去重、亂碼修正與「索引連結完整性」是產生／提交資料時必須直接遵守的規格，不是額外內容驗收階段。
3. 只有使用者當次明確要求「驗證」、「測試」或指定檢查項目時，才做相應的額外驗證；不得因慣例、風險或先前批次而自行追加。
4. 若 helper 或 writer 入口會自動跑內容驗收，改用不含內容驗收的原子寫入；不得略過亂碼閘門與索引連結完整性。
5. 不執行 `tools/findbook_guard.py queue`、內容型 `validate`、150 點格式檢查、HTTP 檢查或 `index.html` UI 測試。JSON 可解析性、數量核對、索引一致性與 ID／路徑唯一性只依「索引連結完整性」執行。

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
3. 單一平台缺書不代表可改收英文書。候選在開啟詳細頁與 reservation 前都要檢查中文書名；不合格就淘汰並補找。既有資料中的純英文書名不得作為新批次候選或配額成果。

## 書籍名稱來源（加速、去重）

目標是儘快湊滿中文書配額，不是掃完所有網站。列表頁已有「中文書名 + 作者 + 連結」就夠用；同一本書只保留一個來源頁。

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

### 查詢順序（每類平行，達配額即停）

**A 組（優先、可平行）**：博客來、金石堂、讀冊、誠品、momo 圖書。這五站列表頁通常已有書名與作者，是主來源。

**B 組（A 組不足才開）**：三民、國家書店、讀墨、BookWalker、Pubu、HyRead、Kobo 繁中。

**C 組（B 組仍不足）**：豆瓣讀書、當當、京東圖書、文軒；香港商務印書館／三聯新書（繁中補缺）。

**D 組（不找新書）**：國圖書目、Google Books。只在書名亂碼、作者缺漏、ISBN 對照時使用。

規則：

1. 同一分類先平行抓 A 組列表頁；有效新書達到該類配額後，立刻停止該類其餘搜尋。
2. 不要依站點串行「博客來全部失敗才換下一個」。A 組可同時抓，但每站要限流；連續失敗或被限制就暫停該站、改用同組其他站。
3. 跨平台去重鍵依序為：ISBN（有則優先）→ 正規化「書名 + 作者」。同一本書出現在多站時，保留最先通過亂碼閘門且資料最完整的一筆，不要開第二個詳情頁。
4. 每類先準備「需求數 + 20%（至少 2 本）」列表候選緩衝；因日期、重複、亂碼修不好或資料不足被淘汰時，再按缺額補找，不要求遍歷所有網站。
5. 有出版日期、上架日期、榜單日期或文章發布日期時，必須用來判斷是否落在搜尋區間。沒有明確日期仍可列入，但 `sourceDateNote` 標註「來源未提供明確日期」。
6. 每筆至少記錄：書名、作者、來源網站、來源網址、榜單名稱、擷取日期、日期區間、來源日期說明。有 ISBN 就一併記下，供跨站去重與亂碼校正。

## 亂碼文字閘門

抓到任何文字後，**必須先判斷是否有亂碼；有亂碼就要先修正，才能進入下一步**。這是資料可用性條件，不是內容驗收，不得略過。

適用欄位：書名、作者、來源名稱、日期說明、摘要、標籤、Grok 回覆的每一行。適用時機：列表擷取後、詳情擷取後、Grok 回覆擷取後、寫入 JSON 前。任一步仍有亂碼，就停在該步，不得 reservation、不得送 Grok、不得把亂碼寫進正式檔。

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
5. 書名／作者仍亂碼時，用 ISBN 或可辨識片段到 D 組（國圖書目、Google Books）或 A 組另一站取正確中文書名與作者，再寫回本筆。
6. Grok 重點亂碼時：不得寫入；視為傳輸失敗，最多重送該書 1 次。仍亂碼則保持 pending，改找或稍後續跑，不得用亂碼湊 150 點。

修正後必須再跑一次判定；仍不合格就淘汰該候選並補找下一本，不得把「看起來差不多」的亂碼書名送進去重或提示詞。

## 新批次與續跑判定

1. 使用者每次重新提出「找新書」或「新增新書」，都是全新批次；即使主題、配額、日期與先前相同，也必須重新完成本次全部新書配額。
2. 每個全新批次啟動時配置唯一 `workId`。是否同一批次只依 `workId` 判斷，不得用日期、主題、配額、提示詞、`queue=0`、`generatedFrom` 或既有完成數量推定。
3. 既有書籍只用於正規化「書名 + 作者」（及 ISBN）去重，不得抵扣新批次配額；已存在就改找下一本，直到各分類配額完成。
4. 只有使用者明確要求「續跑」、「驗證」或「不新增」，或目前存在同一 `workId` 的 pending 工作時，才可停止建立新批次並改為續跑。

## 快速執行總流程

1. 啟動時讀取 `data.json`，再依各索引列的 `file` 讀取本次涉及的單書 JSON，建立正規化「書名 + 作者」索引、ISBN 索引、ID 索引及 Grok 狀態索引。`data.json` 是跨 worker 去重的權威來源；每次新書登記成功後立即更新共享索引，worker 不得長期使用啟動時的舊快照。
2. 依「新批次與續跑判定」確認意圖：全新找書先配置 `workId` 並建立完整新書配額；只有明確續跑或同一 `workId` 尚有 pending 時才進入狀態式續跑。
3. 續跑時，`chatgptStatus: complete` 的書直接略過；仍為 pending 的書只排入 Grok 佇列。只有可明確判定為中斷造成的索引缺漏可依 checkpoint 修復；其他結構異常先隔離回報，不得自動覆寫。
4. 全流程採流水線，各分類可平行：列表擷取 → 亂碼閘門 → 日期／中文書名／去重 → reservation → Grok。搜尋剩餘書籍、Grok 產生與寫入可同步推進；不必等所有主題搜尋完成。
5. 候選通過後立即交給單一 reservation writer；`committed` 後才送 Grok。worker 只回傳隔離結果；Grok 取得完整 150 點並通過亂碼閘門後，立即交由單一 result writer 寫入該書 JSON，不得為了湊批次延後保存。
6. 全部 writer 停止寫入後，依「索引連結完整性」做穩定快照檢查再結束。

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
2. 搜尋 worker 找到合格新書後，只能把已通過亂碼閘門的候選交給單一 reservation writer。worker 不得自行「先查再寫」。
3. reservation writer 在同一個串行臨界區執行 `reload → 亂碼複檢 → normalize → dedupe → allocate ID → prepare → write`：重新載入最新 `data.json`；依中文書名、ISBN 與正規化「書名 + 作者」處理。已存在就回傳既有 ID 並拒絕新增；不存在才配置唯一 ID。
4. 同一 checkpoint 以同一份不可變 reservation payload 建立單書資料與索引列。先原子建立 `Books/{categoryId}/{book-id}.json` pending 骨架，再原子寫入 `data.json`。`data.json.books` 必須立刻寫入完整有效索引列，至少包含 `id`、`title`、`author`、`categoryId`、`tags`、`sourceName`、`sourceUrl`、`file`，並同步更新 `totalBooks`、`generatedFrom`、`generatedAt`。索引列的 `file` 必須精確等於 `Books/{categoryId}/{book-id}.json`。pending 骨架需包含相同的 `id`、`categoryId`、`title`、`author`、完整基本資料、空的 highlights 及相容 pending 狀態。`data.json` 最後寫入，作為 reservation 已提交的標記。
5. writer 只有在該筆索引連結提交檢查通過後才能回傳 `committed + book ID`。Grok worker 收到 committed 後才開始產生重點，後續都以該 ID 為主鍵。
6. 每次 committed 後立即通知所有 worker 使用最新索引。下一個候選仍必須交給 reservation writer 原子檢查。
7. 若 writer 回傳已存在：只有同一 `workId` 且仍為 pending 才排入 Grok 佇列；其他 `workId` 的既有書不計入本次配額，必須改找下一本。
8. 正式流程使用 `tools/findbook_writer.py reserve --category-id <categoryId> ...`，不得再向根目錄分類大檔附加資料。

## 索引連結完整性

`index.html` 只透過 `data.json` 的 `file` 載入單書 JSON。唯一合法路徑為 `Books/{categoryId}/{book-id}.json`；一律使用 `/`、保留實際檔名大小寫，不得使用根目錄分類大檔、反斜線、推算路徑或共用另一筆書籍的檔案。

1. 單筆 reservation writer 在串行臨界區完成 `reload → dedupe → allocate ID → build one payload → write book atomically → write manifest atomically → check link → committed`。單書 JSON 與索引列必須從同一份 payload 產生，不得分別重新組合書名、作者、分類或 ID。
2. 單筆 `check link` 只檢查提交完整性：索引路徑存在且可解析、路徑精確符合規則、索引與單書 JSON 的 `id`、`categoryId`、`title`、`author` 完全一致，且該 ID 與 `file` 在 `data.json` 中各自唯一。任一項失敗都不得 committed，也不得送 Grok。
3. 批次結束時先停止派送並等待所有 reservation／result writer 完成，再取得穩定快照。若檢查期間 `data.json` 的 `generatedAt`、檔案修改時間或書籍數量改變，代表仍有 writer 寫入，必須捨棄該次結果並重新檢查。
4. 穩定快照必須確認：`totalBooks === data.json.books.length`、所有索引檔存在且欄位一致、沒有重複 ID、沒有重複 `file`、所有 `Books/**/*.json` 都被一筆索引連結，且實際 JSON 數量與索引數量一致。全部通過才可宣告批次完成。
5. 同一 `workId` 的 pending 單書檔尚未進入 `data.json` 時，只能依原 reservation checkpoint 補上原索引列；索引已存在但單書檔缺少時，只能依同一 checkpoint 補回 pending 檔。不得從檔名猜測作者、書名或分類，也不得套用其他書的路徑。
6. 欄位不一致、JSON 無法解析、ID／路徑重複或缺少可信 checkpoint 時，先保留現況並回報書名、ID、目前路徑與預期路徑；不得以第一筆搜尋結果或相似書籍自動覆寫。

## 多工整理與即時寫入

1. 中央排程器維護 Grok 與 retry 兩個佇列。同一批次每個工作都必須帶入該批次 `workId`，並至少包含：書名、作者、分類、來源資訊、`searchDateRange`、`attemptCount`、最後錯誤及 `queued → submitted → captured → written` 狀態。
2. 以 Cursor Agent（Grok 4.6）依穩定上限啟動 worker；每本書使用獨立工作與獨立結果暫存。worker 不得直接寫正式 JSON。
3. 必須以 reservation writer 已提交到 `data.json` 的 book ID 防止本批次重複；後續用「book ID + workId」追蹤結果。
4. 同一執行階段只確認一次 `grokMaxWorkers`，後續沿用最後穩定值。若沒有已知穩定值，以正式佇列直接探測：先用 `min(2, 待處理數)`，第一輪穩定後才逐次增加。出現限流、品質下降或工作錯置時立即回退 1。多工上限以實際 Cursor／Grok 環境為準，不得繞過服務限制。
5. 排程採 `dispatch → collect → write`：先填滿可用生成槽，再輪詢進行中的工作；先完成者先寫入並補下一個，不得停在第一個慢回覆上。不使用固定長時間 sleep。Grok 回覆連續兩次讀取內容相同，就視為可擷取。
6. 擷取後先過亂碼閘門，再交給 result writer。不檢查內容格式，也不因格式問題要求重做；只有傳輸失敗或亂碼修不好時最多重試 1 次，仍失敗就移到 retry 佇列尾端，先釋放 worker。主佇列清空後再處理 retry；仍無法完成者保留誠實的 pending，下次只續跑該 Grok 工作。
7. 新書在 Grok 開始前就必須已有 reservation checkpoint。150 點完成時只更新既有骨架，不得再次新增索引。每次只更新本次完成的 `chatgptHighlights`、`chatgptStatus` 與必要來源欄位。
8. writer 先在記憶體組好完整新 JSON（含亂碼複檢），再以同目錄暫存檔替換正式檔。寫入後先做該筆索引連結提交檢查，再把工作狀態改為 `written`。寫入失敗時保留已取得結果並只重試 writer，不得要求 Grok 重新產生。
9. 中斷發生在單書 pending 檔已寫、但尚未加入 `data.json` 時，下次依 checkpoint 補索引；相反則補回 pending 單書檔。修復後必須通過該筆索引連結提交檢查。
10. 既有 `chatgptStatus: complete` 的舊版 100 點資料保持相容且不自動重做；本次新完成或使用者指定重做的書籍一律產生 150 點。完成寫入時將 `highlightsSource` 設為 `grok`，並寫入 `highlightsCapturedAt`。未完成時必須使用明確 pending 狀態。

## Grok 重點提示詞

只替換書名與作者（必須已通過亂碼閘門）。完整限制放在第一次提示：

```text
書名：{書名}
作者：{作者}
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
不得用同義改寫、重排字句、輪替標籤或反覆說明同一觀念來湊滿 150 點；相鄰或分散的重點都不可語意重複。
```

寫入時只保留 `001、` 到 `150、` 的 150 個重點行。格式規則只作為產生時的提示，不執行本地驗收器；擷取後直接寫入，但亂碼仍須先修正。編號後必須直接進入書籍重點內容，不得帶入「X面第N步」這類贅詞。

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
