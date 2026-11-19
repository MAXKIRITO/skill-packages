# 元件解剖學與 Design Tokens 架構手冊 (Components & Tokens)

從成熟的設計工程角度來看，元件（Component）從來不是單純的一段 HTML 標籤或隨機 CSS，而是「由語意化 Token 驅動、具備明確插槽解剖結構，且涵蓋完整 8 大互動狀態機」的系統化單元。

---

## 1. W3C Design Tokens 三層架構規範 (DTCG 2025.10)

依據 W3C Design Tokens Community Group (DTCG) 規範與 Brad Frost 的 Atomic Design 延伸模型，Design Tokens 是比「原子」更基礎的「亞原子粒子（Subatomic Particles）」。設計系統嚴格遵循三層抽象解耦：

```
+--------------------------------------------------------------------------+
| Level 1: 原始層 (Primitive Tokens / Global)                              |
| - 無業務語意的客觀數值庫，直接對應色相或物理尺度                            |
| - 範例: { "color.blue.500": "#2563EB" }, { "space.4": "16px" }           |
| - 規則: 元件嚴禁直接引用此層！                                             |
+--------------------------------------------------------------------------+
                                    |
                                    v (映射與語意化)
+--------------------------------------------------------------------------+
| Level 2: 語意層 (Semantic Tokens / System-wide)                           |
| - 賦予設計決策與業務角色的上下文意義                                       |
| - 範例: { "color.action.primary": "{color.blue.500}" }                   |
|         { "color.surface.card": "{color.neutral.50}" }                   |
| - 規則: 切換深淺色或多品牌主題時，僅需重新映射此層變數！                    |
+--------------------------------------------------------------------------+
                                    |
                                    v (特化與插槽綁定)
+--------------------------------------------------------------------------+
| Level 3: 元件層 (Component Tokens / Scoped)                               |
| - 針對單一元件各部位與狀態的精細覆寫                                       |
| - 範例: { "button.primary.bg.default": "{color.action.primary}" }         |
|         { "button.primary.bg.hover": "{color.action.primary.hover}" }     |
| - 規則: 保障個別元件升級與自定義，不干擾全域系統                         |
+--------------------------------------------------------------------------+
```

---

## 2. 元件結構解剖學（Component Anatomy & Slots）

為避免 AI 生成元件時遺漏關鍵部位，所有複合互動元件（按鈕、輸入框、卡片、清單項目、通知條）必須依循以下結構插槽（Slots）進行推演：

```
+-------------------------------------------------------------------------+
| Container (容器: 底色、邊框、圓角、內外距、高光/陰影)                    |
|                                                                         |
|  [Leading Slot]   [Core Content Slot]                 [Trailing Slot]   |
|   前導圖示/狀態點     主要標籤 (Label)                      狀態徽章/計數器   |
|   (16x16 / 20x20)    輔助說明 (Supporting Text)            展開箭頭/清除按鈕 |
|                                                                         |
|  [Bottom / Feedback Slot]                                               |
|   錯誤驗證訊息 (Error Message) / 輸入字數統計 (Character Counter)       |
+-------------------------------------------------------------------------+
```

### 插槽職責說明：
1. **Container（容器外框）**：定義背景填充、輪廓邊框（Outline）、圓角半徑與點擊熱區範圍（Minimum Hit Target: 桌面端 $\ge 36\text{px}$，行動端 $\ge 48\text{px}$）。
2. **Leading Slot（前導插槽）**：放置輔助辨識圖示、狀態指示燈或頭像，協助使用者在掃描標籤前快速辨認語意。
3. **Core Content Slot（核心內容插槽）**：包含主文字（Label）與輔助文字（Supporting/Description）。**必須預設處理超長文字之折行或省略（Text Truncation）**。
4. **Trailing Slot（尾端插槽）**：放置次要操作（如密碼顯隱眼睛、下拉箭頭、快捷鍵提示 `⌘K` 或清除按鈕 `✕`）。
5. **Feedback Slot（底層回饋插槽）**：專門承載驗證錯誤（Error）、警告提示或進度條，**容器高度應保留過渡空間，避免錯誤出現時版面劇烈下推跳動**。

---

## 3. 必備 8 大互動狀態矩陣（The 8-State Interaction Matrix）

AI 生成前端代碼時最常犯的毛病，就是只寫了「Default」靜態樣式，忽略了真實世界中使用者操作與網路通訊時的各種邊界狀態。

**任何可互動元件必須具備以下完整 8 大狀態機定義**：

| 狀態 (State) | 觸發時機與人機交互意義 | 視覺規範與設計要求 | 程式碼/Token 映射示例 |
| :--- | :--- | :--- | :--- |
| **1. Default (預設)** | 元件就緒、未受干擾之常態 | 具備清晰的邊界符標（Signifier），足夠的文字對比度，讓人一眼辨認其可點擊性。 | `btn-bg: var(--color-primary)`<br>`btn-text: var(--color-on-primary)` |
| **2. Hover (懸停)** | 游標滑入目標命中區 | 提供細微但明確的視覺反饋（如感知亮度微升或微降 5%、輕微位移），確認目標已鎖定。 | `btn-bg: var(--color-primary-hover)`<br>`cursor: pointer;` |
| **3. Focus-Visible (鍵盤聚焦)** | 使用者透過 Tab 鍵或輔助科技導航至該元素 | **無障礙絕對強制**！外層具備高對比、不被裁切的雙層焦點環（Focus Ring），絕對禁止直接寫 `outline: none` 而不補替代樣式！ | `outline: 2px solid var(--color-focus);`<br>`outline-offset: 2px;` |
| **4. Active / Pressed (按下)** | 滑鼠點擊瞬間或觸控下壓 | 模擬物理彈簧或開關反饋，產生按壓位移（如 `transform: scale(0.98)` 或 `translate-y-0.5`）與暗化。 | `transform: scale(0.98);`<br>`btn-bg: var(--color-primary-active)` |
| **5. Disabled (停用)** | 前置條件未滿足，暫不可用 | 降低整體透明度（通常 `opacity: 0.4~0.5`），游標設為 `not-allowed`。**必須搭配 Tooltip 或說明文字解釋「為什麼停用、如何解鎖」**。 | `opacity: 0.45;`<br>`cursor: not-allowed; pointer-events: none;` |
| **6. Loading (載入中)** | 異步請求進行中、已發送表單 | **鎖定重複點擊**；保留按鈕原有寬高避免版面跳動；內容替換為旋轉指示器（Spinner）或骨架屏（Skeleton Shimmer）。 | `aria-busy="true";`<br>`btn-icon: spinner; pointer-events: none;` |
| **7. Error / Validation (驗證錯誤)** | 輸入不符合規範、後端回傳失敗 | **禁止純靠顏色**！必須同時呈現紅色邊框、警示圖示（Leading/Trailing）與具體修復建議文字（如「密碼需包含至少 8 碼」）。 | `border-color: var(--color-error);`<br>`aria-invalid="true";` |
| **8. Empty (空狀態)** | 資料庫為空、篩選無結果、首次進入 | 嚴禁留出死白空白！必須包含情境插畫/圖示、友好解釋文案，以及**關鍵下一步行動引導按鈕**（Primary Call to Action）。 | `<EmptyState icon="..." title="尚無專案" action="建立第一個專案" />` |

---

## 4. 極端情境與防脆弱檢查清單（Stress-Testing Checklist）

在完成元件推演後，設計師必須對元件進行「真實世界破壞測試」：

1. **極端文字溢出測試**：
   - 如果使用者的名字長達 30 個字元（如包含多個中間名）？
   - 解決：核心標籤是否宣告 `truncate`（單行省略）或 `line-clamp-2`？是否有 Tooltip 顯示全名？
2. **多語系長度膨脹測試**：
   - 英文轉為德文（German）或法文時，文字長度常會膨脹 30%~50%。
   - 解決：按鈕寬度是否寫死固定像素（如 `width: 120px`）導致破字？必須採用自適應內距（`px-4 min-w-[...px]`）。
3. **無障礙點擊熱區（Touch Targets）**：
   - 在行動裝置上，即便圖示僅有 `16x16px`，其外圍點擊熱區是否擴展至至少 `44x44px` 或 `48x48px`？
4. **網路延遲與連續點擊（Debounce & Optimistic UI）**：
   - 使用者連續狂按按鈕會不會發出多次請求？
   - 解決：按下後立即切入 `Loading` 狀態並鎖定 `disabled`，或採用樂觀更新（Optimistic UI）。
5. **深淺色高對比切換**：
   - 語意 Token 是否在 Dark Mode 下自動適配？是否有任何硬編碼的 `#FFFFFF` 或 `#000000`？
