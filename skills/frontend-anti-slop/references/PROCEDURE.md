# 前端去 AI 味實戰操作手冊 (Procedure)

本手冊提供在前端開發與介面生成過程中，從根源改寫模型搜尋空間、消除「AI 味」（AI Slop）的具體操作規格、提示詞範本與工程規範。

---

## 1. 持久化設計系統檔（`DESIGN.md`）

為了杜絕長對話中的「上下文稀釋（Context Drift）」，所有 UI 決策必須錨定於專案根目錄的 `DESIGN.md`。

### 1.1 `DESIGN.md` 標準範本

```markdown
# 專案設計系統規範 (DESIGN SYSTEM CONSTRAINTS)

本專案拒絕預設「AI 公版風格」（AI Slop）。所有介面產出必須嚴格遵守以下數值硬約束：

## 1. 字體與階層 (Typography)
- 標題字體：`Fraunces`, serif（或 `Plus Jakarta Sans`, sans-serif）
- 內文字體：`Newsreader`, serif（或 `Noto Sans TC`, sans-serif）
- 程式碼字體：`JetBrains Mono`, monospace
- 嚴禁字體：禁止使用 `Inter`, `Roboto`, `Arial`，以及作為次高備案的 `Space Grotesk`, `Poppins`, `Manrope`。
- 字級跳躍比 (Size Jump Ratio)：標題與內文字級比必須 ≥ 3.0 倍。
  - Hero Display: `clamp(40px, 4vw, 64px)`
  - Section Title: `clamp(24px, 2.5vw, 36px)`
  - Body Text: `16px` (1rem), line-height: 1.7
  - Small / Caption: `13px` (0.8125rem)
- 字重約束 (Font Weight)：
  - Display / H1：最高 `500`（靠尺寸撐開氣場，嚴禁使用 700/800 粗體硬撐）。
  - Section H2 / H3：`500` 或 `700`。
  - Body：`400`。

## 2. 色彩預算 (Color Budget & OKLCH)
- 預算上限：全頁最多 3 個強調色；每個強調色整頁最多出現 3 次（全頁總強調點 ≤ 9 個）。
- 基準色票 (採用 OKLCH / CSS 變數)：
  - `--paper`: oklch(0.99 0.005 90) /* 暖白手工紙質背景 */
  - `--ink`: oklch(0.18 0.015 260) /* 濃黑炭墨文字 */
  - `--ink-mute`: oklch(0.45 0.02 260) /* 輔助灰字 */
  - `--hairline`: oklch(0.88 0.01 90) /* 極細分割線 */
  - `--accent-1`: oklch(0.48 0.12 180) /* 深海青 (功能主強調) */
  - `--accent-2`: oklch(0.58 0.16 50) /* 陶土赭 (次級警示/標記) */
- 漸層禁令：
  - 嚴禁使用 `from-violet-600 via-purple-600 to-indigo-700` 等多段高飽和漸層。
  - 嚴禁霓虹發光（Glow）、滿版毛玻璃（backdrop-blur）。
  - 背景僅限純色，或角落單一極低透明度（≤ 8%）微弱徑向光（radial-gradient）。

## 3. 空間與留白 (Spacing & Layout)
- 區塊垂直內距 (Section Padding)：
  - 桌面端：`160px`（`py-40` / `10rem`）以上。
  - 行動端：`96px`（`py-24` / `6rem`）以上。
  - 嚴禁使用 64–96px 的擁擠模板留白。
- 版面結構：
  - 嚴禁全頁 `text-center` 置中。
  - 嚴禁均分三欄卡片網格（`grid-cols-3`）。
  - 強制採用 `60/40 不對稱分割`、`交錯圖文列表` 或 `單一主視覺 Tab 切換`。

## 4. 幾何與圓角階層 (Component Radii Matrix)
- 嚴禁按鈕、卡片與輸入框全數套用相同的 `16px` (`rounded-2xl`)。
- 圓角矩陣規範：
  - 按鈕 (Button)：`4px` (`rounded-sm`) 或 `0px`。
  - 輸入框 (Input)：`4px` (`rounded-sm`)。
  - 卡片 (Card)：`8px` (`rounded-md`) 或 `0px`（配合極細分割線 border-hairline）。
  - 對話框 (Modal)：`12px` (`rounded-lg`)。

## 5. 動效預算 (Motion Budget)
- 全頁動效上限：最多 2 處。
  1. 初次載入之微幅錯落進場 (Staggered fade-up, 200ms)。
  2. 主要 CTA 懸停色彩切換 (Hover state, 150ms ease-out)。
- 其餘元件保持靜止，嚴禁無意義的浮動、旋轉或發光動畫。
```

### 1.2 在專案規則中持久化引用

在專案的 `CLAUDE.md`、`.cursorrules` 或 System Prompt 中加入：

```markdown
<!-- 前端 UI 生成強制規則 -->
所有前端介面生成、HTML/CSS 修改與元件重構，必須在產出前先讀取根目錄的 `DESIGN.md`。
產出之程式碼若包含 `DESIGN.md` 明令禁止之字體、色彩、三欄卡片或等距留白，視為嚴重格式違規。
```

---

## 2. 注入「負向黑名單」提示詞（含次高機率防滑落）

大型語言模型在推理時具備極佳的負向排除能力，但若只禁止第一層預設，會觸發「次高機率滑落現象」（例如禁了 `Inter` 就滑向 `Space Grotesk`）。必須連同替代品一併封鎖。

### 2.1 複製即用提示詞區塊 (`<anti_slop_constraints>`)

```xml
<anti_slop_constraints>
1. 禁止字體與字重：
   - 嚴禁使用：Inter, Roboto, Arial, system-ui。
   - 同時嚴禁次高機率備案：Space Grotesk, Poppins, Manrope。
   - 嚴禁在 Hero / Display 大標題一律硬套 font-weight: 700 / 800；必須採用 400-500 字重配合 3 倍以上字級跳躍。

2. 禁止色彩與背景：
   - 嚴禁使用 violet / purple / indigo 多段漸層 (如 from-violet-600 to-indigo-700)。
   - 嚴禁在深色模式套用亮青色 (Cyan) 霓虹發光或模糊背景彩球 (blurred blobs)。
   - 嚴禁點陣網格背景 (dot grid background)。
   - 嚴禁滿版彩虹標籤與漸層按鈕。

3. 禁止版面與序列：
   - 嚴禁全頁 text-center 置中排版（大標題可置中，但副標、內文與說明必須左對齊）。
   - 嚴禁「頂部小膠囊標籤 → 置中大標題 → 灰字副標 → 雙按鈕 → 懸浮儀表板截圖」之固定八股序列。
   - 嚴禁 grid-cols-3 等寬圖示卡片排列。
   - 嚴禁區塊垂直留白小於 120px（桌面端強制 160px 以上）。

4. 禁止元件與裝飾套路：
   - 嚴禁所有組件無差別套用 16px (rounded-2xl) 圓角；按鈕、卡片與輸入框必須有差異化圓角或採 0px 銳利工藝風。
   - 嚴禁使用淺色圓圈包覆 Lucide 打勾圖示 (如 bg-emerald-500/10 text-emerald-500 p-2 rounded-full)。
   - 嚴禁使用紫粉漸層之「Most Popular」或「Best Value」膠囊標籤。
   - 嚴禁裝飾性幾何 SVG 波浪 (wave divider) 與 Blob。

5. 禁止假文案與虛構評價：
   - 嚴禁使用「Unlock the power of...」、「簡單、快速、強大」等萬用空洞標語。
   - 嚴禁在無真實用戶授權時放置五顆琥珀色滿分星星與 DiceBear 幾何頭像；改用真實簡報資料、文字縮寫圓標或直接省略該區塊。
</anti_slop_constraints>
```

---

## 3. 維度隔離提示（Isolated Prompting）與排版張力

不要在單一提示詞中混入「現代、高級、排版好看」等寬鬆形容詞，應將「字體排版」、「色彩預算」、「留白佈局」與「動效」拆開下達精確參數。

### 3.1 推薦字體組合表（建立鮮明個性）

| 風格定位 | 標題字體 (Display) | 內文字體 (Body) | 等寬/代碼 (Mono) | 視覺性格與適用領域 |
| --- | --- | --- | --- | --- |
| **雜誌編輯風**<br>(Editorial) | `Fraunces` 或 `Playfair Display` (Weight: 400–500) | `Newsreader` 或 `Noto Serif TC` (Weight: 400) | `JetBrains Mono` | 深度閱讀、專業智庫、精品電商、文化評論 |
| **技術工藝風**<br>(Utilitarian Tech) | `IBM Plex Sans` 或 `Plus Jakarta Sans` (Weight: 500) | `Noto Sans TC` (Weight: 400) | `IBM Plex Mono` | 開發者工具、基礎架構、資料科學、金融系統 |
| **瑞士現代主義**<br>(Swiss Modern) | `Cabinet Grotesk` 或 `General Sans` (Weight: 500) | `Satoshi` 或 `Noto Sans TC` (Weight: 400) | `Space Mono` | 設計工具、SaaS 平台、建築與工業設計 |
| **典雅學術風**<br>(Literary Academic) | `Cinzel` 或 `Cormorant Garamond` (Weight: 400) | `EB Garamond` 或 `Source Han Serif` (Weight: 400) | `Courier Prime` | 法律合約、研究報告、歷史文獻、學術刊物 |

### 3.2 排版張力計算規則

1. **字級跳躍公式**：
   $$\text{Jump Ratio} = \frac{\text{Display Title Size}}{\text{Body Font Size}} \ge 3.0$$
   - 例：內文為 `16px` 時，Display Title 至少為 `48px`（建議 `56px–64px`）。
   - 區塊標題（H2）與內文比應維持在 `1.8–2.2 倍`（約 `28px–36px`）。
2. **字重對比兩極化**：
   - 模式 A（古典舒展）：Display `400`（大尺寸襯線體）+ Body `400`。
   - 模式 B（現代張力）：Display `200`（極細大字）+ Subhead `800`（極粗小標）+ Body `400`。
   - 嚴禁平庸的中間值：400 vs 600（層級模糊，泥濘不清）。
3. **行高與字距 (Tracking & Leading)**：
   - 大字級（≥ 40px）：`letter-spacing: -0.02em` 至 `-0.03em`，`line-height: 1.1–1.2`。
   - 內文字（16px）：`letter-spacing: 0`，`line-height: 1.65–1.75`。
   - 小標/標籤（12–13px）：`text-transform: uppercase`，`letter-spacing: 0.08em`。

---

## 4. 參考驅動（Reference-Driven）與跨界美學混血

AI 無法憑空發明品味，但擅長在明確座標下執行。人類開發者應擔任「藝術總監（Art Director）」，提供真實世界的參考錨點。

### 4.1 拆解人類作品三步驟（複製大法）

1. **截取版面骨架**：至 Mobbin、Awwwards 或 Dribbble 挑選 1–2 個優秀人類作品，測量其格線比例（如 12 欄不對稱分欄：左 4 欄固定導航、右 8 欄主內容）。
2. **萃取色彩與留白**：吸取其背景與文字底色（如 `#0F1419` 墨黑配 `#F8FAFC` 紙白），測量其 Section 垂直留白（如 160px）。
3. **餵入模型作為格式約束**：
   ```text
   請依照以下參考架構製作產品介紹頁：
   - 網格：採用 12 欄不對稱網格，左側 4 欄放 Sticky 標題與簡介，右側 8 欄放條目清單。
   - 留白：每個 Section 垂直間距設為 180px。
   - 配色：紙白色背景 (#FFFFFF)、深墨色文字 (#0F1419)，唯一的強調色為深海青 (#0F766E)。
   ```

### 4.2 跨界美學混血提示詞公式

要徹底跳脫「科技新創 SaaS 公版」，最有效的方式是**將目標領域與異質美學進行跨界混血**：

- **配方 1（SaaS 工具 × 1970 年代植物圖鑑海報）**：
  > 「為這款 API 監控工具設計著陸頁，採用 1970 年代植物學圖鑑海報的排版語言：米黃暖調手工紙背景、古典襯線字體、細墨線邊框、手繪風格的圖表註解與不對稱圖文排列，禁止任何現代紫藍漸層與懸浮卡片。」
- **配方 2（金融儀表板 × 日本文具品牌型錄）**：
  > 「設計這個資產管理儀表板，借鑑日本文具型錄的極簡編排：高密度文字表格、精準緊湊的 1px 分割線、低彩度土色標記點、直角無圓角（0px radius），強調功能性與紙張般的安靜質感。」
- **配方 3（開發者平台 × 瑞士國際主義網格手冊）**：
  > 「建立本開源專案的首頁，完全遵循瑞士國際主義風格（Swiss Style）：嚴格的非對稱數學網格、大字級左對齊無襯線標題、零裝飾性陰影、唯一的色彩為瑞士紅強調標籤，以純粹的文字排版形成視覺節奏。」

---

## 5. 內容優先（Content-First）與分段逐區推進

「單一大提示詞一次生成整頁」是產生 AI 味的最大溫床。真實世界的排版取決於文字長短與資訊層級。

### 5.1 文案長度驅動排版決策

| 標題長度 | 推薦版面結構 | 留白與字級調整 |
| --- | --- | --- |
| **超短標題**<br>(2–5 個詞 / 6–10 字) | 巨大字級 Display（`clamp(48px, 6vw, 80px)`）+ 60/40 雙欄橫向佈局 | 標題獨佔左欄，右欄放置說明與行動按鈕 |
| **中長標題**<br>(8–14 個詞 / 15–25 字) | 左對齊單欄 + 不對稱左側留白（grid offset 1 col） | 字級適度收斂（`36–48px`），斷行採 `text-wrap: balance` |
| **陳述性長句**<br>(超過 25 字) | 雜誌引文風格（Pull-Quote），上下加雙細線 | 採優雅襯線體，左右留白加寬，文字置中或大幅縮進 |

### 5.2 分段逐區推進流程

1. **第一回合：定調 Hero 區塊**：
   - 確定字體組合、主副標級比、背景底色與單一主 CTA。
   - 確保 Hero 留白充裕（螢幕高度的 70%–80%），檢核是否有預設膠囊或多餘陰影。
2. **第二回合：核心功能區（拒絕連續卡片）**：
   - 檢討第一個功能區的結構。若第一區使用了圖文分割，第二區**強制切換為表格或清單**，嚴禁連續兩區使用卡片。
3. **第三回合：真實數據與社會證明**：
   - 拒絕五星評分與假頭像。改用「客戶引文標題＋純文字職稱」，或「3 個關鍵量化數據＋1px 細線隔開」。
4. **第四回合：轉換與頁尾**：
   - 定價區改採「開放式乾淨清單（Open table/list）」而非三張等高並排卡片。
   - 頁尾採低彩度極簡單欄或不對稱 4 欄純文字導航。

---

## 6. 雙重審查閉環（Dual-Review Critique Loop）

生成初版後，必須執行兩道獨立的審查程序，確保同時通過「視覺美學」與「工程功能」檢驗。

### 6.1 第一道：視覺截圖批判審查 (Visual Critique Pass)

將渲染頁面截圖（或提供渲染後的 DOM / CSS），依據以下檢查點進行反思重構：

1. **遠看測試（Squint Test）**：將視線模糊或縮小至 25%，整頁是否有單一清晰的視覺錨點？若全頁有 10 個發光亮點或彩色彩球，代表色彩預算超標，立即將非核心元素降為灰階。
2. **3 秒 AI 味辨識**：頁面是否一眼能看出 shadcn/ui 或 Tailwind 預設？檢查是否有紫藍漸層、rounded-2xl 泛濫或均分三欄。
3. **節奏檢查**：垂直滾動時，各區塊的高度與留白是否均等死板？若有，將某一區垂直內距拉大至 200px，或將橫向寬度收窄至單欄。

### 6.2 第二道：功能性與無障礙補齊 (a11y & Engineering Pass)

AI 最常偷懶的是表單互動與無障礙屬性，必須逐項補齊：

- [ ] **表單必填標示**：所有必填輸入框必須有明確標示（如紅星 `*` 或「必填」文字），且不可僅依賴 placeholder。
- [ ] **行內驗證與錯誤提示**：輸入錯誤時，提供包含 `text-red-600`、`text-sm`、`role="alert"` 的具體錯誤提示，並將輸入框邊框高亮。
- [ ] **鍵盤導航焦點框**：按鈕、連結與輸入框不可移除 outline；必須提供清晰的 `:focus-visible` 樣式（如 `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-accent`）。
- [ ] **無障礙屬性 (ARIA)**：圖示按鈕必須包含 `aria-label`；展開折疊組件必須有 `aria-expanded`；載入狀態必須有 `aria-busy`。
- [ ] **對比度標準**：內文與背景對比度必須符合 WCAG AA 標準（常態文字 ≥ 4.5:1，大標題 ≥ 3:1）。
