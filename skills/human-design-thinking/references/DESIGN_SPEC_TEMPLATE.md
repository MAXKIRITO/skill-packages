# 人本設計規格藍圖範本 (Human Design Spec Template)

當設計推演與三方頭腦互搏完成後，**Lead (設計總監)** 將所有共識與系統化度量收斂為本份標準規格書。此文件作為上游設計決策與下游工程實作（如 `frontend-anti-slop` 或前端代碼編寫）之間的唯一事實來源（Single Source of Truth）。

---

# 《專案名稱》人本設計規格藍圖 (Human Design Spec)

## 1. 雙鑽石前期定義 (Double Diamond Discovery & Definition)

### 1.1 目標 Persona 與情境
- **核心角色 (Primary Persona)**：[例如：高頻操作的倉儲調度員 / 需快速審閱報告的高階主管]
- **使用場景與設備環境**：[例如：行動平板單手操作 / 雙螢幕工作站 / 強光倉庫環境]
- **核心痛點與心智模型**：[描述使用者目前的摩擦點與期望預期]

### 1.2 核心任務 (Core User Tasks)
1. **任務一 (Primary Task)**：[使用者進入畫面必須在 3 秒內完成的最高優先級動作]
2. **任務二 (Secondary Task)**：[次要輔助操作，如篩選、匯出或切換檢視]

### 1.3 內容優先約束 (Content-First Constraints)
- **代表性真實文案**：
  - 典型標題：`[例如：2026 年度第一季企業雲端架構遷移驗證評估報告]`
  - 極限長度邊界：`[預計最長 48 字元，中英文混排，超長需 truncate 並給予 Tooltip]`
  - 核心數值範例：`[例如：$1,248,500.00 USD，防破行]`
- **微文案規格**：
  - 主要行動 CTA：`[例如：「確認並啟動部署流程」 (嚴禁寫純「送出」)]`
  - 取消/返回操作：`[例如：「放棄變更並返回清單」]`

---

## 2. 系統化美學與視覺度量 (Systematic Aesthetics)

### 2.1 60-30-10 感知色彩系統 (OKLCH 空間)
- **視覺焦點預算配比**：
  - **60% 主基調色 (Surface)**：大面積畫布背景，安靜承載內容。
  - **30% 輔助色 (Surface Container / Secondary)**：側欄、卡片底層與結構分隔。
  - **10% 強調色 (Primary Accent)**：僅用於核心 CTA 與關鍵狀態。

| 語意角色 (Token) | 淺色模式 OKLCH / Hex | 深色模式 OKLCH / Hex | 設計職責與限制 |
| :--- | :--- | :--- | :--- |
| `color.surface.default` | `oklch(0.98 0.005 240)` | `oklch(0.14 0.01 240)` | 全頁 60% 畫布底層 |
| `color.surface.container` | `oklch(0.95 0.008 240)` | `oklch(0.18 0.015 240)` | 30% 卡片與模組底層 (Tonal Elevation) |
| `color.surface.elevated` | `oklch(0.92 0.01 240)` | `oklch(0.24 0.02 240)` | 浮動彈窗與下拉選單 |
| `color.text.primary` | `oklch(0.20 0.02 240)` | `oklch(0.96 0.005 240)` | 主要文字 (對比度 ≥ 7:1) |
| `color.text.secondary` | `oklch(0.48 0.02 240)` | `oklch(0.72 0.01 240)` | 輔助說明文字 (對比度 ≥ 4.5:1) |
| `color.action.primary` | `oklch(0.55 0.22 255)` | `oklch(0.72 0.19 255)` | 10% 核心強調色 Primary CTA |
| `color.action.on-primary`| `oklch(0.99 0 0)` | `oklch(0.12 0.02 255)` | Primary CTA 內部標籤文字 |
| `color.border.subtle` | `oklch(0.85 0.01 240)` | `oklch(0.32 0.01 240)` | 低調結構線 (非必要不畫) |
| `color.feedback.error` | `oklch(0.58 0.22 28)` | `oklch(0.70 0.20 28)` | 警示錯誤狀態 |

### 2.2 模組化字階系統 (Modular Type Scale: Major Third 1.25)
- **基準字級 (Base)**：`16px (1rem)`
- **行寬約束 (Measure)**：內文寬度限制 `560px ~ 680px`（英文 45~75 字元，中文 25~40 字）。

| 字階 Token | 尺寸 (px / rem) | 行高 (Leading) | 字重 (Weight) | 適用範圍 |
| :--- | :--- | :--- | :--- | :--- |
| `typography.display` | `40px (2.5rem)` | `1.15` | `Bold (700)` | Hero 大標題 |
| `typography.h1` | `32px (2.0rem)` | `1.20` | `Semibold (600)` | 頁面主要 H1 標題 |
| `typography.h2` | `24px (1.5rem)` | `1.25` | `Semibold (600)` | 模組 Section 標題 |
| `typography.h3` | `20px (1.25rem)` | `1.30` | `Medium (500)` | 卡片與彈窗標題 |
| `typography.body` | `16px (1.0rem)` | `1.50` | `Regular (400)` | 核心段落內文 |
| `typography.caption` | `13px (0.8125rem)`| `1.40` | `Regular (400)` | 標籤、時間戳、提示文字 |

### 2.3 8pt 空間網格與留白階梯
- **微留白 (Micro)**：`4px` (圖標文字間隔), `8px` (內部 Padding), `16px` (標準內距)
- **宏留白 (Macro)**：`48px` (卡片組與標題間隔), `72px~96px` (區塊 Section 垂直呼吸間隔)
- **鐵律檢驗**：宏留白尺寸（`72px`）達到微留白（`16px`）的 4.5 倍，確保格式塔接近性自然生效。

---

## 3. 核心元件解剖學與 8 大互動狀態矩陣

### 3.1 核心元件：[例如：PrimaryActionGroup / DataFilterCard]
- **結構插槽 (Slots)**：
  - `[Leading]`：[16x16 向量圖示]
  - `[Core Label]`：[單行自適應文字，超出截斷]
  - `[Supporting]`：[輔助說明或快捷鍵標記]
  - `[Trailing]`：[計數徽章或狀態指示燈]

### 3.2 必備 8 大互動狀態機規格表

| 狀態 (State) | 觸發條件 | 視覺表現與 Token 綁定 | 無障礙與防呆行為 |
| :--- | :--- | :--- | :--- |
| **1. Default** | 初始常態 | 背景 `color.action.primary`，高對比白字 | 清晰邊界與 48px 熱區 |
| **2. Hover** | 游標進入 | 背景明度微調 +5%，游標變 `pointer` | 平滑過渡 150ms |
| **3. Focus-Visible** | 鍵盤 Tab 聚焦 | 雙層焦點環（2px 外擴 offset，高對比藍） | 嚴禁取消 outline |
| **4. Active** | 滑鼠點擊/觸控按下 | 模擬物理按壓位移 `translate-y-0.5` | 即時觸覺反饋 |
| **5. Disabled** | 條件不符 | `opacity: 0.45; cursor: not-allowed` | 懸停出現 Tooltip 解釋原因 |
| **6. Loading** | 異步提交中 | 寬高維持原狀，文字轉為 Spinner | 禁用點擊防重複發送 |
| **7. Error** | 提交驗證失敗 | 紅色邊框 + 警示圖標 + 具體錯誤文案 | `aria-invalid="true"` |
| **8. Empty** | 資料為空 | 呈現空狀態圖示、說明與 Primary CTA | 指引第一步建立行動 |

---

## 4. 三方頭腦互搏攻防與裁決記錄 (Adversarial Log)

### 4.1 對抗攻防摘要 (Critic vs. Designer)
- **交鋒點一 (邊界崩潰質疑)**：
  - *Critic 質疑*：若使用者組織名稱超過 35 字元，頂部導航欄會將 Primary CTA 擠出螢幕，違反 Content-First 與 Fitts's Law。
  - *Designer 修正*：在組織名稱加上 `max-w-[240px] truncate`，並在懸停時以 Tooltip 顯示全稱，保障 CTA 絕對穩固在右側固定佈局。
- **交鋒點二 (對比度不足質疑)**：
  - *Critic 質疑*：次要標籤文字原設計為 `gray-400 (#9CA3AF)`，在白底對比度僅 3.2:1，違反 WCAG AA 4.5:1。
  - *Designer 修正*：提升至 `color.text.secondary (oklch 0.48)`，對比度達到 5.1:1，並縮小 1 級字階區分層級。

### 4.2 👑 Lead 總監最終裁定 (Trade-offs Arbitration)
- **裁定一**：[記錄 Lead 針對懸而未決議題之權衡決策與最終拍板依據]

---

## 5. 下游工程交接指南 (Handshake to Downstream)

- **直接前端實作**：依據第 2 節之 Token 表與第 3 節之 8 狀態矩陣直接實作。
- **銜接 `frontend-anti-slop`**：
  1. 本規格書作為 `DESIGN.md` 資產，優先級最高。
  2. 依據第 2 節色彩與佈局，選定配合之物料質感（如 Industrial Hardware 或 Layered Obsidian）。
  3. 執行 6 大實體工藝方法注入（微噪點、內切高光、物理阻尼）。
  4. 啟動瀏覽器實機渲染觀看閉環驗收。
