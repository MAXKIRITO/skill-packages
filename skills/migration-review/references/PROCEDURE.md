# Migration 作業規範

索引：環境與基準、schema 與資料、runner、部署、驗證、執行方案與交付。按本次變更選讀。

## 1. 環境與基準

最低確認資料庫 engine／版本、schema／tenant、migration 工具與 runner、目前基準版本、預計 target、是否只有審查。具體連線或執行前再確認已授權環境，不在審查期間順便探測正式站。

檢查單位為「migration ID＋操作／表＋應用相容性階段＋環境假設」。同一操作在空 DB、既有資料 DB 與不同 engine 不能共用通過結論。

讀目前 migration、必要前置 schema、model／query、runner 與部署文件。工具 `status`、config generator 或 import 都可能連 DB／建表；先讀行為，不以命令名稱推論唯讀。

資料量、lock timeout、replica topology 或版本未知時，明確列為假設；可完成靜態檢查，不需要先索取全部環境資訊。

## 2. Schema 與資料檢查

| 操作 | 必查問題 | 最小代表資料 |
| --- | --- | --- |
| 新增 NOT NULL | 舊資料如何填值，default 是否符合語意 | 舊 rows、null、未指定欄位 |
| 型別轉換 | cast、溢位、精度、時區、不可轉值 | 邊界、非法字串、精度值 |
| unique／FK | 現有重複、孤兒、null 與驗證方式 | 重複與孤兒 rows |
| rename／drop | 舊 app、背景 job、報表、raw SQL 使用方 | 舊版讀寫 |
| index | 命名、順序、filter、唯一性、建立方式 | 代表查詢與資料分布 |
| backfill | 分批、checkpoint、重跑、與線上寫入競態 | 中途失敗後續跑 |
| enum／default | app 新舊版本是否理解新值 | 舊 client／舊 worker |

檢查資料變更是否可逆、是否會丟失內容，以及回填是否應獨立於 DDL。不要只檢查「SQL 語法有效」。避免為了讓 migration 通過而刪除真實衝突資料。

## 3. Runner 與交易

逐步核對 discovery、排序、載入、開始 transaction、執行操作、記錄 metadata、commit／rollback、connection close。不能從 runner 建立 transaction 推論每個操作都被包住。

- ORM API 是否真正傳 transaction，raw SQL 是否使用同一 connection？
- metadata 與 schema 變更是否一致提交，失敗會不會已寫 schema 但沒記錄？
- engine 是否支援交易式 DDL，特定 index／DDL 是否禁止放 transaction？
- 多個 runner 會否同時選到待執行項目？有 lock 或外部序列化嗎？
- migration 是完整成功才記錄，還是存在過早成功標示？
- retry、部分成功與重跑的語意是否清楚？`IF EXISTS` 是否掩蓋意外 schema 差異？
- 已套用檔案有 checksum 或其他追蹤嗎？不要任意編輯歷史 migration 讓環境分歧。

只有來源明確證明的問題才能作靜態確認；涉及 engine 行為時查相符版本的官方資料或在已授權的隔離 DB 驗證，不以其他 engine 的經驗代替。

## 4. 鎖、效能與部署順序

考慮表重寫、constraint validation、index build、長交易、replica lag、儲存空間、statement／lock timeout。靜態審查只能指出風險條件，沒有實際資料量或量測時不能聲稱停機幾分鐘。

相容性需要分階段時採適合專案的 expand → backfill → app 切換 → contract；不是每個 migration 都需要所有階段。確認舊版 app、rolling deploy、worker 與 rollback window 是否仍可操作新 schema。

程式 rollback 不會自動回復 DB；schema down 也不會復活已刪資料。備份存在不等於可還原，需確認工具版本、權限、加密材料、目標、恢復時間與實際演練證據。

## 5. 驗證方案

優先隔離、可丟棄、版本相符的 DB。選擇符合此次操作的案例：

1. 從上一版真實 schema 升級，不只測空庫。
2. 加入 null、重複、孤兒與型別邊界等代表資料，確認預期處置。
3. 驗證 schema、關鍵資料與新舊 app 查詢，不只看 exit code。
4. 依 runner 宣告檢查再執行、失敗恢復、metadata 一致性與必要的並行控制。
5. 只有產品需要且可安全驗證時測 down／restore；不可逆變更明確標示。

沒有隔離 DB 時仍可完成來源審查與命令方案，但標示未執行。不要拿測試站或正式站補足未授權的驗證。

## 6. 執行方案契約

使用者要求實際執行時，在動作前形成可審閱的具體方案；已有明確授權不重複請求同一權限。方案至少包含：

- 目標環境／schema／基準、將執行的 migration ID。
- 影響表與資料、應用部署順序、相容性窗口。
- 必要前置檢查、backup／restore 條件與執行身份；秘密以環境變數名稱表示。
- 確切命令、timeout／lock 策略、成功後驗證。
- 失敗或鎖等待時的停止條件、是否可重試、如何識別部分完成。
- 回復方式與不可逆資料損失；未演練的回復不能說已可用。

若目標與授權不符、出現未知 pending migration、基準不符或非預期錯誤，停止依賴該條件的變更，交代已執行部分。不要清 metadata、強行重跑、改連線目標或自動殺 session 來「繼續」。

## 7. 候選與交付

每個問題列操作、前提、來源證據、實際影響、最小修正及驗證。查反證：引擎是否原生避免重寫、部署是否已序列化、舊 schema 是否已先清理、transaction 是否由框架注入？

完成結論須分「靜態檢查完成」「隔離環境驗證完成」「指定環境已套用」；它們不能互相替代。範圍未包含的歷史 migration 不能宣稱無問題。

### 案例：runner 有 transaction 但 migration 沒傳入

追實際 query API 與框架傳播設定，確認每個 DDL／DML 及 metadata 的 connection。沒有隱式傳播才判交易未涵蓋，並在隔離 DB 觀察中途失敗結果。

### 案例：drop column 有 down

down 新增同名欄位不會恢復原內容。交付時明確區分結構重建與資料還原，提供適當分階段部署或備份還原方案。
