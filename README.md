# 開發與診斷 Skills

一組可跨專案使用的開發工作流程，協助維護人與 AI 共用的專案摘要及開發要求、定位程式，以及檢查跨端契約、多語系、時序圖表、MQTT 資料流與資料庫 migration。

主要目標是減少不必要的文件閱讀、搜尋與重複分析，同時保留判斷所需的證據及驗證。各 skill 不限定特定框架或專案目錄，可分別安裝，也可一起使用。

PS.我只是把我平常做的事情和一些東東弄成skill方便我偷懶，另外東西都是codex寫的

## Skills 清單

本安裝包包含以下七個 skills：

| Skill | 解決什麼問題 | 主要檢查內容 |
| --- | --- | --- |
| [project-context](skills/project-context/SKILL.md) | 接手專案要重新摸索、專案摘要與固定要求分散或過期 | 人與 AI 共用的摘要、架構地圖、規則分類、文件入口及增量維護 |
| [efficient-code-navigation](skills/efficient-code-navigation/SKILL.md) | 不知道實作在哪、反覆讀取與搜尋太多內容 | 任務入口、搜尋範圍、呼叫關係、資訊重用與探索停止條件 |
| [api-contract-check](skills/api-contract-check/SKILL.md) | API 修改後使用方不相容、前後端欄位或錯誤格式不一致 | 路由、輸入、認證範圍、回應、序列化、分頁、重試及版本相容性 |
| [i18n-check](skills/i18n-check/SKILL.md) | 缺漏翻譯、語系 key 不一致、文字或語系切換異常 | 靜態／動態 key、fallback、插值、plural、硬編碼 UI 與格式化 |
| [timeseries-chart-debug](skills/timeseries-chart-debug/SKILL.md) | 圖表缺點、時間偏移、聚合錯誤或查詢緩慢 | 時間語意、資料來源、區間邊界、降採樣、API、圖表轉換與效能分層 |
| [mqtt-dataflow-check](skills/mqtt-dataflow-check/SKILL.md) | 裝置送出訊息但資料未出現、最新值不更新或重複／亂序 | 連線、訂閱、topic、consumer、queue、commit、snapshot、API 與 UI |
| [migration-review](skills/migration-review/SKILL.md) | schema 升級不相容、交易不完整、重跑或失敗恢復不明確 | 舊資料、constraint、runner、metadata、鎖、部署順序與回復方案 |

只有 `i18n-check` 附帶執行腳本，其餘以工作流程與檢查規範為主。安裝 skill 不會啟動專案服務或執行檢查。

## 快速安裝

需要可執行 `npx` 的 Node.js／npm。首次使用 Skills CLI 時可能需要下載套件。

### 從本機資料夾安裝

在這個 README 所在的資料夾執行，將七個 skills 安裝給 Codex 跨專案使用：

```sh
npx skills add . --skill '*' -g -a codex
```

若目前在上一層目錄：

```sh
npx skills add ./skill-packages --skill '*' -g -a codex
```

只安裝需要的 skill：

```sh
npx skills add . --skill api-contract-check -g -a codex
```

| 參數 | 用途 |
| --- | --- |
| `--skill '*'` | 選擇來源中的所有 skills；保留引號以避免 shell 展開 |
| `--skill 名稱` | 只選擇指定 skill |
| `-g` | 安裝到個人範圍，供不同專案使用 |
| `-a codex` | 指定安裝給 Codex |

要安裝到某個專案，請在該專案目錄執行，移除 `-g`，來源使用本安裝包的實際絕對路徑，例如：

```sh
npx skills add /path/to/skill-packages --skill '*' -a codex
```

請將 `/path/to/skill-packages` 替換成實際位置。若環境已有同名的專案版與個人版，可能出現重複項目，先確認需要保留的版本。

### 從 GitHub 安裝

將本資料夾的內容發布為獨立 repository 後，可使用：

```sh
npx skills add YOUR_ACCOUNT/YOUR_REPO --skill '*' -g -a codex
```

`YOUR_ACCOUNT/YOUR_REPO` 為範例，需替換成實際來源；本包尚未發布 GitHub。不需要額外製作 npm 套件或 Python 安裝器。

## 如何使用

在支援的環境中，以 `$skill-name` 搭配具體任務，例如：

```text
$api-contract-check 檢查這次 API 欄位修改是否影響呼叫端。
```

Agent 也可依任務與 skill 描述選用適合的流程。通常先選最貼近問題的一個，不必每次要求載入全部 skills。

| 情境 | 提問範例 |
| --- | --- |
| 專案摘要與要求 | `$project-context 沿用現有文件，整理人與 AI 共用的專案摘要和固定開發要求，補上閱讀入口。` |
| 找實作 | `$efficient-code-navigation 找出這個錯誤的實際入口，只追相關呼叫鏈。` |
| API 串接 | `$api-contract-check 核對這個 endpoint 的請求、回應與前端解包方式，修正不相容處。` |
| 多語系 | `$i18n-check 檢查這個頁面在目前支援語系中的 key、插值與 fallback。` |
| 圖表異常 | `$timeseries-chart-debug 排查指定序列在這個時間區間缺點的原因。` |
| 裝置資料 | `$mqtt-dataflow-check 依現有來源與 log，找出訊息在哪一段中斷。` |
| Migration | `$migration-review 審查這次 migration 的舊資料相容性與失敗恢復，先不連資料庫。` |

提供已知檔案、錯誤、時間區間、預期行為或 diff，通常能更快縮小範圍。不需要一開始提供整個專案或完整 log；避免貼入憑證、token 或真實個資。

### 工作模式

七個 skills 使用一致的模式選擇方式：

| 模式 | 適合需求 | 執行範圍 |
| --- | --- | --- |
| 說明 | 詢問方法、規則或概念 | 回答必要部分，沒有定位需求時不掃 repo |
| 定向處理 | 指定錯誤、檔案、diff 或局部修改 | 預設模式，只展開與問題有關的檢查 |
| 範圍審查 | 明確檢查一個模組、介面集合或指定範圍 | 先定義檢查單位與排除項，再記錄覆蓋及缺口 |

例如，要檢查整個裝置模組，可明確指定「範圍審查：只檢查裝置 API 與其前端使用方」。要產生文件則再指定報告位置；一般局部任務不強制寫報告。

### 維護人與 AI 共用的專案文件

`project-context` 用於建立或更新可長期重用的專案知識；`efficient-code-navigation` 用於完成當前任務時的定向探索。一般程式修改不會自動觸發整套文件重建。

共用文件依內容分工，優先沿用專案既有位置：

| 內容 | 主要用途 | 沒有合適既有位置時的範例 |
| --- | --- | --- |
| 專案入口 | 用途、快速開始與重要連結 | `README.md` |
| 詳細摘要 | 架構、模組地圖、資料流、指令、限制與來源 | `docs/PROJECT_CONTEXT.md` |
| 開發要求 | 固定要求、適用範圍、觸發條件與驗證方式 | `docs/DEVELOPMENT_RULES.md` |
| 常駐規則與任務導覽 | 必要常駐約束及按任務閱讀指引 | `AGENTS.md` |

這些是文件角色，不是必須建立的四個檔案。已有 overview、開發指南或 `docs/ai/` 時直接維護原位置，詳細內容只保留一個主要來源，不另外產生人類版與 AI 版。

```text
$project-context 只更新這次資料流變更影響的摘要與入口，保留其他內容。
$project-context 把我明確指定的固定要求整理成規則，區分單次條件與建議，保留 AGENTS.md 必要常駐約束。
```

新增或更新前會核對來源，單次要求不自動成為永久規則；不明確的事實與要求會列為待確認。共用文件的詳細分工與範本見 [project-context 文件契約](skills/project-context/references/REPORTING.md)。

## 文件結構與按需閱讀

```text
skills/
├── project-context/
├── efficient-code-navigation/
├── api-contract-check/
├── i18n-check/
│   ├── SKILL.md
│   ├── references/
│   │   ├── PROCEDURE.md
│   │   └── REPORTING.md
│   └── scripts/
│       └── compare_locales.py
├── timeseries-chart-debug/
├── mqtt-dataflow-check/
└── migration-review/
tests/
└── test_compare_locales.py
```

每個 skill 都包含 `SKILL.md` 與兩份 reference；上圖以 `i18n-check` 展開示範。各 skill 的必要資源都放在自己的資料夾內，沒有其他 skill 的隱含依賴。

| 檔案 | 內容 | 讀取時機 |
| --- | --- | --- |
| `SKILL.md` | 觸發描述、工作模式、輸入、五階段流程與完成條件 | 啟用該 skill 時 |
| `references/PROCEDURE.md` | 領域檢查矩陣、操作細節、測試案例、反例與停止條件 | 只讀本次相關章節 |
| `references/REPORTING.md` | 檢查紀錄與報告模板；`project-context` 另含共用文件分工、摘要及固定要求範本 | 範圍審查、文件建立或需要報告時 |

減少 token 消耗的方式包括先限制搜尋範圍、分段讀取、重用已確認位置，以及只在需要時展開參考文件。安裝或載入不會自動精簡專案的 `AGENTS.md`；明確要求時可用 `project-context` 維護它，保留有效規則與作用範圍。節省效果依任務而異，不保證固定比例。

## 檢查結果如何判讀

覆蓋狀態與問題結論分開記錄：

| 類別 | 狀態 | 意義 |
| --- | --- | --- |
| 覆蓋 | 已檢查 | 已按聲明的方法完成判讀，不代表沒有問題 |
| 覆蓋 | 待驗證 | 有會影響結論的具體缺口 |
| 覆蓋 | 未檢查 | 尚未處理或不在本次範圍 |
| 覆蓋 | 不適用 | 已確認不適用，需說明理由 |
| 問題 | 已確認／待判定／已排除 | 區分有證據的問題、缺關鍵事實的候選與已被反證的候選 |

證據另外標示 `source`、`test` 或 `runtime`。靜態檢查不能描述為已執行觀察，build 通過也不能直接代表 API、MQTT 或 migration 行為通過。

各流程會核對可能推翻候選的條件，例如 API 中介轉換、i18n fallback、圖表預期降採樣、MQTT retained 訊息或 runner 已有的交易傳播。缺口未解決時，交付具體下一步，而不是用更多搜尋代替證據。

`project-context` 的文件維護結果依內容標示「已核對、待確認、未涵蓋」，並區分來源、明確要求及實際驗證。寫進摘要的指令不代表已執行成功，建議也不會被改寫成強制規則。

## JSON 語系比較工具

`i18n-check` 附帶唯讀的 JSON 比較腳本，需要 Python 3，無第三方依賴。在本資料夾執行：

```sh
python3 skills/i18n-check/scripts/compare_locales.py \
  --base /project/locales/en.json \
  --locale /project/locales/zh.json \
  --locale /project/locales/ja.json \
  --limit 20
```

將範例路徑替換為實際語系檔；`--base` 是比較基準，不限定英文。`--locale` 可重複指定，`--limit` 控制每類顯示筆數，預設為 20。

輸出為 JSON，列出缺少、多出及型別不同的 leaf 路徑，每類同時保留總數與有限筆明細。路徑使用 JSON Pointer，沒有輸出翻譯值；key 本身仍可能含敏感資訊。

| Exit code | 意義 |
| --- | --- |
| `0` | 指定檔案的 leaf 路徑與型別一致 |
| `1` | 存在結構差異 |
| `2` | 參數、讀檔或 JSON 輸入錯誤 |

此工具拒絕重複 key，要求各檔案頂層為 object。它不檢查翻譯品質、程式引用、插值、ICU 或 UI，也不處理 YAML／JS；部分非空容器差異需另用原生工具確認。完整限制見 [i18n 作業規範](skills/i18n-check/references/PROCEDURE.md)。

## 驗證與使用界限

在本資料夾執行腳本行為測試：

```sh
python3 -B -m unittest discover -s tests -v
```

目前涵蓋翻譯值不影響結構判斷、缺少／多出／型別差異、多語系與輸出筆數限制、JSON Pointer、array／null／空容器，以及無效輸入與重複 key。

文件格式、連結與封裝檢查，只能確認資源結構。腳本測試只驗證 JSON 比較工具；七個流程仍需搭配目標專案的工具與環境驗證，尚未因此完成真實服務的端到端演練。

載入 skill 不會擴張使用者授權。資料庫變更、MQTT 主動發布、負載測試及其他環境操作，依原任務授權執行；已有明確授權的操作不重複要求確認。

