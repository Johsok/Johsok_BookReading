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

- `01_商業創業`
- `02_心理勵志`
- `03_自然科學`
- `04_醫療保健`
- `05_飲食養生`
- `06_電腦資訊`
- `07_其他`

## 快速執行總流程

1. 啟動時讀取 `data.json` 與本次涉及的分類 JSON，建立正規化「書名 + 作者」索引、ID 索引及 Codex/Gemini 狀態索引。`data.json` 是跨 worker 去重的權威來源；每次新書登記成功後立即更新共享索引，worker 不得長期使用啟動時的舊快照。
2. 先做狀態式續跑：兩個來源都已驗收完成的書直接略過；只缺 Codex 就只排 Codex；只缺 Gemini 網頁驗證就只排 Gemini；新書才排兩個來源。只有可明確判定為中斷造成的索引缺漏可依 checkpoint 修復，其他結構異常先隔離回報，不得自動覆寫。
3. 若同一批次已存在，續跑缺少的來源，不得重建或重複附加。若是全新的找書要求，既有書不計入新書配額，改找下一個新候選。
4. 全流程採流水線：候選書通過日期、去重及分類後，先完成 `data.json` 即時登記 checkpoint；只有登記成功的書才能送入 Codex 與 Gemini 獨立佇列。搜尋剩餘書籍、模型產生、驗收與寫入可同步推進。
5. worker 只回傳隔離結果；任一來源取得並驗收完整 100 點後，立即交由單一 writer 寫入相應分類 JSON，不得等待另一來源，也不得為了湊批次延後保存。
6. 每次即時寫入後只驗證受影響資料；全部工作結束後才做一次全庫驗證與一次 UI 冒煙測試。

## 找資料

1. 依「主題 × 來源網站」平行讀取博客來、灰熊愛讀書、momo、讀冊等榜單或列表頁，但必須遵守網站限制。
2. 先從列表取得書名、作者及來源網址，立即用正規化「書名 + 作者」比對最新 `data.json` 索引與本批次暫時 reservation set；只有暫時保留成功的新候選才開啟詳細頁，避免重複抓取。此階段只是減少重複請求，不代表已正式登記。
3. 每類先準備「需求數 + 20%（至少 2 本）」候選緩衝；有效新書達到指定配額後，立即停止該類其餘搜尋。若候選因日期、重複或資料不足被淘汰，再按缺額補找，不要求遍歷所有網站。
4. 若網站提供出版日期、上架日期、榜單日期或文章發布日期，必須優先用該日期判斷是否落在日期區間內。
5. 若網站沒有明確日期，仍可列入候選，但 `sourceDateNote` 要標註「來源未提供明確日期」。
6. 每筆至少記錄：書名、作者、來源網站、來源網址、榜單名稱、擷取日期、日期區間、來源日期說明。
7. 候選通過日期、去重、分類及基本來源資料檢查後，立即依「多工新書即時登記」寫入 `data.json` 與分類 pending 骨架；writer 回覆 `committed` 後才加入整理佇列，不必等所有主題搜尋完成。
8. 單一來源連續失敗或遭限制時，暫停該來源並切換其他來源；不得用無限重試阻塞整批工作。

## 分類規則

1. 每本書只能歸到 7 大主題中的 1 類。
2. 若可跨類，選最主要閱讀目的作主題，其餘放入 `tags`。
3. 投資、創業、職涯、管理優先歸 `01_商業創業`。
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
4. `data.json.books` 必須立即寫入完整有效索引列，至少包含 `id`、`title`、`author`、`categoryId`、`tags`、`sourceName`、`sourceUrl`，並同步更新 `totalBooks`、`generatedFrom` 與 `generatedAt`；不得只寫書名、作者或其他半成品。
5. 同一 checkpoint 先建立並驗證相應分類 JSON 的 pending 骨架，再原子寫入並驗證 `data.json` 索引；pending 骨架需包含完整基本資料、空的 highlights 及相容 pending 狀態。`data.json` 最後寫入，作為 reservation 已提交的標記。
6. 只有 writer 重新讀取 `data.json`、確認該組「書名 + 作者」只出現一次，並回傳 `committed + book ID` 後，Codex/Gemini worker 才能開始產生重點；後續所有工作都以該 ID 為主鍵。
7. 每次 committed 後立即更新並通知所有 worker 使用最新索引。下一個候選仍必須交給 reservation writer 原子檢查，不得只相信自己的舊快照。
8. 若 writer 回傳已存在：兩側都完成就略過；若屬同一批次且仍有 pending，只排入缺少的來源；全新找書配額則改找下一本，不得新增第二筆。

## 多工整理規則

1. 中央排程器維護 Codex、Gemini、retry 三個佇列；每個工作至少包含：書名、作者、分類、來源資訊、`searchDateRange`、來源模型、對話識別、`attemptCount`、最後錯誤及 `queued → submitted → captured → validated → written` 狀態。
2. Codex 與 Gemini 使用獨立 worker pool，不互相等待；同一本書可以同時啟動兩個來源工作。worker 不得直接寫正式 JSON。
3. 必須以 reservation writer 已提交到 `data.json` 的 book ID 防止本批次重複；共享 reservation set 只快取 committed 索引。後續用「book ID + 來源模型」追蹤結果，避免跨書寫入。
4. 同一執行階段只確認一次 `codexMaxWorkers` 與 `geminiMaxWorkers`，後續沿用最後穩定值；不得每本書或每個批次重新從 1 開始測試。
5. 若沒有已知穩定值，以正式佇列中的工作直接探測，不另發測試提示；Codex 先用 `min(2, 待處理數)`、Gemini 先用 1 個已確認可用的對話，第一輪穩定後才逐次增加。出現限流、品質下降、對話錯置或驗證頁時立即回退 1，且只有狀況改變才重測。
6. 多工上限以實際服務、帳號、Chrome 操作穩定性與速率限制為準；不得繞過服務限制、建立額外帳號或用會觸發封鎖的方式提高併發。
7. 排程採 `dispatch → collect → validate/repair`：先填滿所有可用生成槽，再輪詢所有進行中的工作；先完成者先驗收並補入下一個工作，不得停在第一個慢回覆上等待。
8. 不使用固定長時間 sleep。遠端回覆連續兩次讀取內容相同且已通過 100 點驗收，就視為可擷取；若內容已完整，不必繼續等待不可靠的 busy/idle 指示。
9. 擷取逾時或頁面狀態不明時，先重新讀取同一對話最後回覆並驗收，確認沒有可回收結果後才重送，避免重複產生。
10. 格式不合格時，一次列出全部錯誤行號與原因，回原對話要求重新輸出完整 100 行。每個來源最多 1 次格式修正與 1 次傳輸重試；仍失敗就移到 retry 佇列尾端，先釋放 worker 處理其他書。
11. 主佇列清空後再處理 retry 佇列；仍無法完成者保留誠實的 pending 狀態，下次只續跑該來源，不得重做另一個已完成來源。
12. 任一來源進入 `validated` 後，writer 必須立即建立 checkpoint 並寫入；多筆同時完成時依完成順序串行寫入，可合併已經在等待的結果，但不得等待更多結果來湊批次。

## 中斷保護與即時寫入

1. Codex 或 Gemini 任一來源取得並驗收完整 100 點後，立即寫入該書所屬分類 JSON；不得等另一來源完成，也不得等整個分類或整批工作完成。
2. 新書在模型工作開始前就必須已完成 reservation checkpoint，亦即 `data.json` 已有唯一索引且分類 JSON 已有 pending 骨架。第一個 100 點完成時只更新既有骨架，不得再次新增索引。
3. 每次只更新本次完成來源的 highlights、status 與必要來源欄位；另一個已完成來源及其他既有資料不得重寫、清空或重新產生。
4. writer 寫入前先在記憶體建立完整的新 JSON 內容並確認可解析，再透過同目錄暫存檔替換正式檔，避免中斷時留下只寫一半的 JSON。
5. 寫入後立即重新讀取該 JSON，確認目標書籍存在、該來源剛好 100 點、編號正確且 status 已更新；全部通過後，工作狀態才可從 `validated` 改為 `written`。
6. 若寫入或寫後驗證失敗，保留已驗收結果並只重試 writer，不得要求模型重新產生。下次執行以正式 JSON 的狀態為準，只補尚未 `written` 或仍為 pending 的來源。
7. 若中斷發生在 pending 骨架已成功寫入、但新書尚未加入 `data.json` 之間，下次啟動先驗證骨架，再只補上缺少的索引；不得重新找書。若發現 `data.json` 已有索引但分類骨架缺少，必須先依 reservation 工作資料補回 pending 骨架，確認兩檔一致後才可啟動模型。

## 共用重點提示詞

Codex 與 Gemini 都使用下列固定提示詞，只替換書名與作者；完整限制放在第一次提示，減少後續修正：

```text
書名：{書名}
作者：{作者}
請整理本書 100 個重點，只輸出剛好 100 行，不要加入任何其他文字或空行。
第 1 至 9 行使用 01、至 09、，第 10 至 99 行使用 10、至 99、，最後一行必須是 100、。
每行只能是「編號、完整重點句」。禁止前言、結語、Markdown、項目符號、模型自述、分類名稱、固定小標、短標籤加冒號及符號「｜」。
```

## Gemini 網頁版來源要求

1. `geminiHighlights` 必須來自 Chrome 裡的 Gemini 網頁版實際最終回覆。
2. 不得用 Codex 自行生成、本地模板、快取舊結果、API 回覆、摘要改寫或未經網頁驗證的文字替代網頁版 Gemini 的重點整理。
3. 每本書都必須在 Gemini 網頁版的獨立對話送出提示詞；送出後可切換到其他對話工作，不必停留等待，但只能擷取該對話最後一則 model 回覆。
4. 寫入 JSON 的 `geminiHighlights` 必須和 Gemini 網頁版最後驗收通過的回覆逐行一致；只允許移除前後空白、拆成 JSON array，不得改寫正文。
5. 若回覆格式不合格，必須回到同一個網頁版對話要求 Gemini 修正；修正後寫入的版本也必須是網頁版實際回覆。
6. 若無法確認已送出到 Gemini 網頁版、無法確認模型、無法取得完整回覆，或無法證明內容來自 Gemini 網頁版，不得標記為 `complete`。
7. 同一 Gemini 頁面工作階段只確認登入與模型一次；只有頁面重載、模型顯示改變或發生來源疑義時才重查。
8. 未完成網頁版驗證時，`geminiStatus` 必須標記為 `pending_web_verification`，且不得宣稱已取得 Gemini 網頁版重點整理。

## Codex 重點

1. 每本書建立獨立 Codex 工作，輸入「共用重點提示詞」；本流程不使用 ChatGPT 網頁版。
2. 回覆完成後立即在本地驗收，不必等待 Gemini；不合格時依「多工整理規則」回原工作修正。
3. 驗收通過後，將結果存入 `chatgptHighlights` 相容欄位並將 `chatgptStatus` 設為 `complete`；欄位名稱不代表使用 ChatGPT。
4. 寫入時只保留 `01、` 到 `100、` 的 100 個重點行，不得混入其他文字。
5. 多本書依 `codexMaxWorkers` 平行處理，每本書使用獨立提示與獨立結果暫存，避免內容交叉污染。

## Gemini 重點
1. 必須操作使用者 Chrome 裡已登入的 Gemini 網頁版，不得使用 Codex 本身回答、Gemini API、其他瀏覽器、其他網頁外掛或本地模板替代 Gemini 網頁版輸出。
2. 進入 Chrome 的單一 Gemini 頁面並啟用最高階 Pro model；不得用多個 Gemini 分頁模擬多工。
3. 依 `geminiMaxWorkers` 連續建立獨立新對話、輸入「共用重點提示詞」，並保存「book ID + 對話識別」映射，直到填滿可用槽或佇列耗盡。
4. 送滿後以輪詢方式切換對話，優先擷取已完成者；某對話仍在產生時，立即處理其他對話、本地驗收或寫入工作。
5. 每本書必須保留獨立提示、獨立對話及獨立結果暫存；不得以頁面標題或目前最後一則回覆猜測對應書籍。
6. 擷取該對話最後一則 model 回覆後立即驗收；不合格時回同一對話要求重新輸出完整 100 行。
7. 驗收通過後，將逐行一致的結果存入 `geminiHighlights` 並將 `geminiStatus` 設為 `complete`。
8. 確認同一本書保留 `chatgptHighlights` 與 `geminiHighlights`，讓 `index.html` 可以同時顯示 Codex 和 Gemini 的重點整理。

## 重點格式驗收

1. Codex 與 Gemini 回覆都先用同一個本地驗收器檢查，通過後才交給 writer。
2. 必須剛好 100 個非空白行。第 `i` 行應直接比對預期前綴：`1..99` 使用兩位數 `01、..99、`，第 100 行使用 `100、`；不得只用兩位數 regex，以免漏掉第 100 點。
3. 每行只允許「預期編號前綴 + 完整重點句」；不得使用 `001_`、`001、`、`01.`、`1、` 或其他格式。
4. 任一行包含 `｜`、正文開頭使用短標籤加冒號、只是分類名稱或提示詞欄位，或包含模型自述、前言、結語，視為不合格。
5. 擷取當下即將解析後的 100 行與來源最終回覆逐行完整比對，不再於最後逐本重開對話只抽查第 1、50、100 點。
6. 若輸出不合格，只能依有限重試規則回對應 Codex 或 Gemini 網頁版同一對話，要求重新輸出完整 100 行；不得由本地改寫正文，也不得把不合格內容寫成 `complete`。

## 寫入 JSON

1. 新書找到並通過基本檢查後，由 reservation writer 立即建立分類 pending 骨架及 `data.json` 索引；這一步必須早於任何 Codex/Gemini 工作。
2. 新書骨架的缺少來源使用相容 pending 狀態，其中 Gemini 必須使用 `pending_web_verification`。任一來源驗收完成後，結果 writer 立即更新分類 JSON，另一來源保持 pending，讓使用者可以先查看，之後再補齊。
3. 結果 writer 每次寫入前確認 book ID 已 committed、分類骨架存在且正規化「書名 + 作者」唯一；只更新受影響分類 JSON，不重寫無關分類或未變動的 `data.json`。
4. 只有 Codex 與 Gemini 兩側都完成時，才可將 `highlightsSource` 設為 `codex_and_web_gemini` 並寫入 `highlightsCapturedAt`；未完成時必須使用明確的 pending 狀態，不得套用完成來源值。
5. 每本完整書籍格式：

```json
{
  "id": "book-id",
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
  "chatgptHighlights": ["01、..."],
  "chatgptStatus": "complete",
  "geminiHighlights": ["01、..."],
  "geminiStatus": "complete",
  "highlightsSource": "codex_and_web_gemini",
  "highlightsCapturedAt": "YYYY-MM-DDTHH:mm:ss+08:00"
}
```

`chatgptHighlights` 與 `chatgptStatus` 為 `index.html` 既有相容欄位；內容由 Codex 產生，不使用 ChatGPT。

## 驗證

1. 不需另開 server。每個模型回覆只做局部 100 行驗收；每次即時 checkpoint 後只 parse 受影響的分類 JSON，新書另檢查 `data.json` 索引一致。
2. 工作開始時可用現有 `tools/findbook_guard.py queue` 快速列出待處理來源；工作結束時只執行一次 `tools/findbook_guard.py validate` 全庫驗證。若系統的 `python` 不在 PATH，使用工作環境既有的 Python runtime，不得為此新增依賴。
3. 所有 JSON 必須能被 JSON parser 讀取，`data.json` 與分類 JSON 的書籍數、ID、分類及索引必須一致。
4. 不得重複同一組正規化「書名 + 作者」，也不得出現同批次 reservation 衝突。
5. 狀態為 `complete` 的 Codex 與 Gemini 重點都必須剛好 100 點，並通過 `01、` 至 `100、` 的逐行前綴檢查。
6. `geminiStatus: complete` 只能用於已確認來自 Gemini 網頁版最後回覆的內容，且 100 行必須與擷取時的已驗收結果逐行一致。
7. 若 Codex 或 Gemini 已修正，最終完整 100 點必須來自該來源同一個工作／對話；另一個已完成來源不得重做。
8. 全批次結束後只開啟一次 `index.html`，確認主題下拉選單能顯示新書、書名下拉選單能切換資料，並確認不可有亂碼。
