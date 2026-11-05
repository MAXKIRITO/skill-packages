# 時序圖表診斷作業規範

索引：案例與基準、時間語意、資料流、聚合、效能、驗證與交付。依症狀選讀，不先通讀資料平台。

## 1. 案例與基準

記錄環境、序列／裝置、時間區間、預期點值或圖形、實際症狀、重現操作、是否最近變更。使用不含秘密的測試識別，沒有已知正確結果時先建立可驗證樣本。

檢查單位為「序列＋區間＋查詢選項＋資料階段」。歷史圖、最新值、匯出與即時圖可能讀不同來源，不預設彼此應逐點相同。

變更前後比較需固定資料範圍、序列數、點數上限、cache 與環境；無法固定時列出限制。不要用不同日期的測量推論某次修改有效。

## 2. 時間語意

| 項目 | 要確認的事實 | 常見誤判 |
| --- | --- | --- |
| 時間來源 | event／device／received／stored time | 裝置慢時鐘不代表伺服器時區錯 |
| 表示法 | ISO offset、UTC、本地字串、epoch 秒或毫秒 | 數值大小猜單位只能作線索 |
| 查詢邊界 | `[start,end)` 或其他規則 | 相鄰區間雙含 end 會重複 |
| 日期解析 | server、driver、browser 的解析行為 | 無 offset 字串依工具可能有不同語意 |
| 時區與 DST | 儲存、bucket、顯示各自時區 | 一個本地日不必然是 24 小時 |
| 精度 | 秒／毫秒／微秒、rounding | 多個事件被轉成同一毫秒後重合 |
| 時鐘偏差 | clock sync、future timestamp、late arrival | 不能用固定減八小時通用修正 |

挑一到三個已知時間點，列出來源值、儲存值、API 值與顯示值；只轉換一次並註明單位。任何加減 offset 的修正先證明是哪一層誤解時間。

## 3. 資料流定位

### UI 與請求

核對時間選擇器、預設區間、使用者時區、filter、request cancellation、並行請求覆蓋、watcher、刷新與快取。先看實際送出的參數，不只看 UI label。

### 查詢與儲存

追實際 table／hypertable／bucket／view、tenant filter、retention、歷史回填、去重與排序。model 名稱不能證明查詢用的是該資料來源；必要時查看 repository 與 SQL 生成路徑。

### API 與轉換

比較小樣本原始數值與回應：序列 ID、單位、null、無效數字、排序及欄位映射。JSON 轉成字串或 BigInt 的精度損失、前端再次聚合及 formatter 都可能造成差異。

### Renderer

檢查 x 軸資料型別、series mapping、資料集更新、connectNulls、stack、axis scale、decimation、zoom 與 tooltip。renderer 問題需先證明輸入資料正確，不透過改查詢掩蓋顯示錯誤。

## 4. 聚合與降採樣

確認聚合函式、window 大小、對齊 origin、timezone、排序、每序列／總點數限制，以及是查詢前還是查詢後套 limit。

- `avg` 可能隱藏尖峰；`min/max`、last、LTTB 等有不同目的，不能互換後只說「點數一樣」。
- 沒資料與真實零值不同，gap fill 及 interpolation 需有明確業務語意。
- 多序列採不同 bucket 時，前端按 index 對齊可能錯位；以時間戳與規則確認。
- 最新 snapshot 與歷史 last event 可能使用不同亂序策略，先查定義再判錯。
- 回應 metadata 的 bucket size、truncated、downsampled 等需與實際點數相符。

選已知小資料集，手算或用獨立測試 oracle 驗證邊界、順序與聚合；不以與待測實作完全相同的程式重算當成獨立證據。

## 5. 效能量測

先分層：client 排隊／網路、server、DB、serialize、payload、前端 mapping 與 rendering。可以使用現有 timing 工具，但先讀請求副作用、預設併發與目標環境。

| 階段 | 基準項目 | 後續依證據決定 |
| --- | --- | --- |
| 初步 | 固定小區間、單一序列、低請求量 | 有無明顯固定延遲 |
| 查詢 | 實際 SQL／plan、filter、index 定義 | 是否掃描／排序超出預期 |
| 回應 | 點數、bytes、序列數、serialize 耗時 | 降採樣／格式調整 |
| 前端 | mapping、render、互動時間 | 資料集更新與渲染瓶頸 |

同時報 sample count、warmup、concurrency、cache 條件、成功率及耗時分布；少量樣本的 p95 只供初步比較。錯誤或 timeout 不可從平均中悄悄移除。

讀取 query plan 前先確認工具行為；`EXPLAIN ANALYZE` 會執行。不得為診斷擅自加索引、清 cache、變更 retention、補資料或對共享環境壓測。當小樣本已能證實原因即停止，不為追求更多數字繼續加負載。

## 6. 驗證矩陣

依變更選取相關案例，沒有產品支援的情境不強迫建立：

- 單點／空區間／多序列，確認無資料不等於零。
- 起點、終點、相鄰區間、跨日；支援本地時區時加 DST。
- 亂序、重複、null、精度與不同單位。
- 點數上限、bucket 對齊、尖峰與降採樣結果。
- 區間切換中的慢請求競態，以及快取後顯示。
- 同等條件前後量測，確認效能修正沒有改變必要資料語意。

## 7. 結論與案例

候選原因要查反證：資料是否根本未產生、retention 是否依設計、時間 filter 是否正確、其他請求是否覆蓋、圖表是否刻意採平均。文件差異不自動代表程式壞掉。

交付範圍與基準、問題所在層、最小樣本證據、修正、正確性測試與效能比較、未查證階段。來源推論與 runtime 觀察分開；沒有寫入再讀回就不宣稱 ingestion 端到端已通過。

### 案例：圖表固定差八小時

依序比較來源 epoch、API ISO 值與 browser parser；如果 API 已含 `Z`，再補時差可能是二次轉換。修正真正誤解的層，並用 UTC 與本地顯示驗證同一瞬間。

### 案例：只顯示 1,000 點

先查 max points 與 metadata，確認是否預期降採樣。若產品要求保留極值，再評估聚合方法；不要直接刪 limit 造成未量測的大回應。
