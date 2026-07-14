# FindBook Skill：書籍重點整理 SOP

## 使用時先確認

先從使用者指令解析下列 4 項，只詢問缺少且沒有預設值的項目；不得重問已提供的資訊。需要詢問時，必須一次問完所有缺項，避免多次往返：

1. 這次要找哪些主題？
2. 每個主題各需要幾本新書？
3. 要搜尋哪一段日期區間？
4. 是否限制為單工；未指定時自動使用目前已知的穩定多工上限。

日期區間格式：

- 開始日期：`YYYY-MM-DD`
- 結束日期：`YYYY-MM-DD`
- 若使用者沒有指定，預設找最近 30 天內的新書、暢銷書或熱門書。
- 若使用者沒有指定多工方式，預設啟用穩定多工，不另外停下詢問。

主題固定為：

- `01_商業理財`
- `02_心理勵志`
- `03_自然科學`
- `04_醫療保健`
- `05_飲食養生`
- `06_電腦資訊`
- `07_其他`

## 快速執行總流程

1. 啟動時讀取 `data.json`，再依各索引列的 `file` 讀取本次涉及的 `Books/{categoryId}/{book-id}.json` 單書檔，建立正規化「書名 + 作者」索引、ID 索引及 Codex 狀態索引。`data.json` 是跨 worker 去重的權威來源；每次新書登記成功後立即更新共享索引，worker 不得長期使用啟動時的舊快照。
2. 先做狀態式續跑：Codex 重點已驗收完成的書直接略過；仍為 pending 的書只排入 Codex 佇列。只有可明確判定為中斷造成的索引缺漏可依 checkpoint 修復，其他結構異常先隔離回報，不得自動覆寫。
3. 若同一批次已存在，只續跑尚未完成的 Codex 工作，不得重建或重複附加。若是全新的找書要求，既有書不計入新書配額，改找下一個新候選。
4. 全流程採流水線：候選書通過日期、去重及分類後，先完成 `data.json` 即時登記 checkpoint；只有登記成功的書才能送入 Codex 佇列。搜尋剩餘書籍、Codex 產生、驗收與寫入可同步推進。
5. worker 只回傳隔離結果；Codex 取得並驗收完整 150 點後，立即交由單一 writer 寫入相應單書 JSON，不得為了湊批次延後保存。
6. 每次即時寫入後只驗證受影響資料；全部工作結束後才做一次全庫驗證與一次 UI 冒煙測試。

## 找資料

1. 依「主題 × 來源網站」平行讀取博客來、灰熊愛讀書、momo、讀冊等榜單或列表頁，但必須遵守網站限制。
2. 先從列表取得書名、作者及來源網址，立即用正規化「書名 + 作者」比對最新 `data.json` 索引與本批次暫時 reservation set；只有暫時保留成功的新候選才開啟詳細頁，避免重複抓取。此階段只是減少重複請求，不代表已正式登記。
3. 每類先準備「需求數 + 20%（至少 2 本）」候選緩衝；有效新書達到指定配額後，立即停止該類其餘搜尋。若候選因日期、重複或資料不足被淘汰，再按缺額補找，不要求遍歷所有網站。
4. 若網站提供出版日期、上架日期、榜單日期或文章發布日期，必須優先用該日期判斷是否落在日期區間內。
5. 若網站沒有明確日期，仍可列入候選，但 `sourceDateNote` 要標註「來源未提供明確日期」。
6. 每筆至少記錄：書名、作者、來源網站、來源網址、榜單名稱、擷取日期、日期區間、來源日期說明。
7. 候選通過日期、去重、分類及基本來源資料檢查後，立即依「多工新書即時登記」建立單書 pending 檔並寫入 `data.json` 索引；writer 回覆 `committed` 後才加入 Codex 整理佇列，不必等所有主題搜尋完成。
8. 單一來源連續失敗或遭限制時，暫停該來源並切換其他來源；不得用無限重試阻塞整批工作。

## 分類規則

1. 每本書只能歸到 7 大主題中的 1 類。
2. 若可跨類，選最主要閱讀目的作主題，其餘放入 `tags`。
3. 投資、創業、職涯、管理優先歸 `01_商業理財`。
4. 習慣、情緒、人際、自我成長優先歸 `02_心理勵志`。
5. 物理、宇宙、生物、數學、科普優先歸 `03_自然科學`。
6. 疾病、醫療、心理健康、照護優先歸 `04_醫療保健`。
7. 食譜、營養、減脂、代謝、養生優先歸 `05_飲食養生`。
8. AI、程式、資料、演算法、軟體工具優先歸 `06_電腦資訊`。
9. 歷史、文化、文學、生活雜學或不適合前六類者歸 `07_其他`。

## 多工新書即時登記

1. `data.json` 是新書去重與 reservation 的唯一權威來源；共享 reservation set 只能作為最新 `data.json` 的記憶體鏡像，不得成為另一套獨立資料。
2. 每個搜尋 worker 找到合格新書後，只能把候選交給單一 reservation writer。worker 不得自行執行「先查再寫」，避免兩個 worker 同時判定不存在而重複新增。
3. reservation writer 在同一個串行臨界區執行 `reload → normalize → check → allocate ID → prepare → write → verify`：重新載入最新 `data.json`，以正規化「書名 + 作者」檢查；已存在就回傳既有 ID 並拒絕新增，不存在才配置唯一 ID。
4. `data.json.books` 必須立即寫入完整有效索引列，至少包含 `id`、`title`、`author`、`categoryId`、`tags`、`sourceName`、`sourceUrl`、`file`，並同步更新 `totalBooks`、`generatedFrom` 與 `generatedAt`；不得只寫書名、作者或其他半成品。
5. 同一 checkpoint 先建立並驗證 `Books/{categoryId}/{book-id}.json` pending 骨架，再原子寫入並驗證 `data.json` 索引；索引列必須包含單書檔 `file` 路徑，pending 骨架需包含完整基本資料、`categoryId`、空的 highlights 及相容 pending 狀態。`data.json` 最後寫入，作為 reservation 已提交的標記。
6. 只有 writer 重新讀取 `data.json`、確認該組「書名 + 作者」只出現一次，並回傳 `committed + book ID` 後，Codex worker 才能開始產生重點；後續所有工作都以該 ID 為主鍵。
7. 每次 committed 後立即更新並通知所有 worker 使用最新索引。下一個候選仍必須交給 reservation writer 原子檢查，不得只相信自己的舊快照。
8. 若 writer 回傳已存在：Codex 重點已完成就略過；若屬同一批次且仍為 pending，只排入 Codex 佇列；全新找書配額則改找下一本，不得新增第二筆。

## 多工整理規則

1. 中央排程器維護 Codex 與 retry 兩個佇列；每個工作至少包含：書名、作者、分類、來源資訊、`searchDateRange`、`workId`、`attemptCount`、最後錯誤及 `queued → submitted → captured → validated → written` 狀態。
2. Codex 依穩定上限啟動 worker；每本書使用獨立工作與獨立結果暫存。worker 不得直接寫正式 JSON。
3. 必須以 reservation writer 已提交到 `data.json` 的 book ID 防止本批次重複；共享 reservation set 只快取 committed 索引。後續用「book ID + workId」追蹤結果，避免跨書寫入。
4. 同一執行階段只確認一次 `codexMaxWorkers`，後續沿用最後穩定值；不得每本書或每個批次重新從 1 開始測試。
5. 若沒有已知穩定值，以正式佇列中的工作直接探測，不另發測試提示；Codex 先用 `min(2, 待處理數)`，第一輪穩定後才逐次增加。出現限流、品質下降或工作錯置時立即回退 1，且只有狀況改變才重測。
6. 多工上限以實際 Codex 執行環境、帳號穩定性與速率限制為準；不得繞過服務限制、建立額外帳號或用會觸發封鎖的方式提高併發。
7. 排程採 `dispatch → collect → validate/repair`：先填滿所有可用生成槽，再輪詢所有進行中的工作；先完成者先驗收並補入下一個工作，不得停在第一個慢回覆上等待。
8. 不使用固定長時間 sleep。Codex 回覆連續兩次讀取內容相同且已通過 150 點驗收，就視為可擷取；若內容已完整，不必繼續等待不可靠的 busy/idle 指示。
9. 擷取逾時或工作狀態不明時，先重新讀取同一工作最後回覆並驗收，確認沒有可回收結果後才重送，避免重複產生。
10. 格式不合格時，一次列出全部錯誤行號與原因，回原工作要求重新輸出完整 150 行。每個工作最多 1 次格式修正與 1 次傳輸重試；仍失敗就移到 retry 佇列尾端，先釋放 worker 處理其他書。
11. 主佇列清空後再處理 retry 佇列；仍無法完成者保留誠實的 pending 狀態，下次只續跑該 Codex 工作。
12. Codex 結果進入 `validated` 後，writer 必須立即建立 checkpoint 並寫入；多筆同時完成時依完成順序串行寫入，可合併已經在等待的結果，但不得等待更多結果來湊批次。

## 中斷保護與即時寫入

1. Codex 取得並驗收完整 150 點後，立即寫入該書自己的單書 JSON；不得等整個分類或整批工作完成。
2. 新書在 Codex 工作開始前就必須已完成 reservation checkpoint，亦即 `data.json` 已有唯一索引且 `file` 指向的單書 JSON 已有 pending 骨架。150 點完成時只更新既有骨架，不得再次新增索引。
3. 每次只更新本次完成的 `chatgptHighlights`、`chatgptStatus` 與必要來源欄位；其他既有資料不得重寫、清空或重新產生。
4. writer 寫入前先在記憶體建立完整的新 JSON 內容並確認可解析，再透過同目錄暫存檔替換正式檔，避免中斷時留下只寫一半的 JSON。
5. 寫入後立即重新讀取該單書 JSON，確認 book ID 與 `categoryId` 正確、Codex 重點剛好 150 點、編號正確且 `chatgptStatus` 已更新；全部通過後，工作狀態才可從 `validated` 改為 `written`。
6. 若寫入或寫後驗證失敗，保留已驗收結果並只重試 writer，不得要求 Codex 重新產生。下次執行以正式 JSON 的狀態為準，只補尚未 `written` 或仍為 pending 的 Codex 工作。
7. 若中斷發生在單書 pending 檔已成功寫入、但新書尚未加入 `data.json` 之間，下次啟動先驗證單書檔，再只補上缺少的索引；不得重新找書。若發現 `data.json` 已有索引但單書檔缺少，必須先依 reservation 工作資料補回 pending 單書檔，確認兩檔一致後才可啟動 Codex。

## Codex 重點提示詞

Codex 使用下列固定提示詞，只替換書名與作者；完整限制放在第一次提示，減少後續修正：

```text
書名：{書名}
作者：{作者}
請整理本書 150 個重點，只輸出剛好 150 行，不要加入任何其他文字或空行。
第 1 至 150 行都使用固定三位數編號：001、002、……、150、；第一行必須是 001、，最後一行必須是 150、。
每行只能是「編號、完整重點句」。禁止前言、結語、Markdown、項目符號、模型自述、分類名稱、固定小標、短標籤加冒號及符號「｜」。
```

## Codex 重點

1. 每本書建立獨立 Codex 工作，輸入「Codex 重點提示詞」；本流程不使用 ChatGPT 網頁版。
2. 回覆完成後立即在本地驗收；不合格時依「多工整理規則」回原工作修正。
3. 驗收通過後，將結果存入 `chatgptHighlights` 相容欄位並將 `chatgptStatus` 設為 `complete`；欄位名稱不代表使用 ChatGPT。
4. 寫入時只保留 `001、` 到 `150、` 的 150 個重點行，不得混入其他文字。
5. 多本書依 `codexMaxWorkers` 平行處理，每本書使用獨立提示與獨立結果暫存，避免內容交叉污染。
6. 既有 `chatgptStatus: complete` 的舊版 100 點資料保持相容且不自動重做；本次新完成或使用者指定重做的書籍一律產生 150 點。

## 重點格式驗收

1. Codex 回覆先用本地驗收器檢查，通過後才交給 writer。
2. 必須剛好 150 個非空白行。第 `i` 行應直接比對固定三位數預期前綴：`f"{i:03d}、"`，亦即從 `001、` 逐行連續到 `150、`；不得只用兩位數 regex 或只檢查部分行。
3. 每行只允許「預期編號前綴 + 完整重點句」；不得使用 `001_`、`001.`、`01、`、`1、` 或其他格式。
4. 任一行包含 `｜`、正文開頭使用短標籤加冒號、只是分類名稱或提示詞欄位，或包含模型自述、前言、結語，視為不合格。
5. 擷取當下將解析的 150 行與 Codex 最終回覆逐行完整比對，不得只抽查部分編號。
6. 若輸出不合格，只能依有限重試規則回同一個 Codex 工作，要求重新輸出完整 150 行；不得由本地改寫正文，也不得把不合格內容寫成 `complete`。

## 寫入 JSON

1. 新書找到並通過基本檢查後，由 reservation writer 立即建立 `Books/{categoryId}/{book-id}.json` pending 單書檔及 `data.json` 索引；這一步必須早於任何 Codex 工作。正式流程使用 `tools/findbook_writer.py reserve --category-id <categoryId> ...`，不得再向根目錄分類大檔附加資料。
2. 新書單書檔先寫入空的 `chatgptHighlights` 與相容的 pending `chatgptStatus`。Codex 驗收完成後，結果 writer 立即更新該單書 JSON。
3. 結果 writer 每次寫入前確認 book ID 已 committed、索引列含正確 `file`、單書 pending 檔存在且正規化「書名 + 作者」唯一；只更新受影響單書 JSON，不重寫其他書籍或未變動的 `data.json`。
4. Codex 重點完成時，將 `highlightsSource` 設為 `codex` 並寫入 `highlightsCapturedAt`；未完成時必須使用明確的 pending 狀態，不得套用完成來源值。
5. 每本完整書籍格式：

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
  "highlightsSource": "codex",
  "highlightsCapturedAt": "YYYY-MM-DDTHH:mm:ss+08:00"
}
```

`chatgptHighlights` 與 `chatgptStatus` 為 `index.html` 既有相容欄位；內容由 Codex 產生，不使用 ChatGPT。

## 驗證

1. 不需另開 server。每個 Codex 回覆只做局部 150 行驗收；每次即時 checkpoint 後只 parse 受影響的單書 JSON，新書另檢查 `data.json` 的 `file` 索引一致。
2. 工作開始時可用現有 `tools/findbook_guard.py queue` 快速列出待處理來源；工作結束時只執行一次 `tools/findbook_guard.py validate` 全庫驗證。若系統的 `python` 不在 PATH，使用工作環境既有的 Python runtime，不得為此新增依賴。
3. 所有 JSON 必須能被 JSON parser 讀取；`data.json.totalBooks`、索引筆數與 `Books/` 單書檔數必須一致，每筆 ID、分類、`file`、書名、作者及來源欄位也必須一致。
4. 不得重複同一組正規化「書名 + 作者」，也不得出現同批次 reservation 衝突。
5. 本次新完成或重做且 `chatgptStatus` 為 `complete` 的 Codex 重點必須剛好 150 點，並通過 `001、` 至 `150、` 的逐行前綴檢查；既有舊版 100 點只作歷史相容。
6. 若 Codex 已修正，最終完整 150 點必須來自同一個工作，不得拼接不同回覆。
7. 全批次結束後只開啟一次 `index.html`，確認主題下拉選單能顯示新書、書名下拉選單能切換資料，並確認不可有亂碼。
