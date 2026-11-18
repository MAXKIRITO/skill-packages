# 前端去 AI 味與頂級視覺工藝實戰操作手冊 (Procedure)

本手冊提供在前端開發與介面生成過程中，從根源改寫模型搜尋空間、消除「AI 味」（AI Slop）與「過度禁慾論文風」的具體操作規格、設計諮詢矩陣、工藝方法代碼庫與工程規範。

---

## 1. 設計資產盤點、高槓桿諮詢矩陣與八大先鋒流派庫

為了杜絕「每次生成都長得一模一樣」或退回預設公版（不論是 Tailwind 紫藍漸層，或是暖白底加陶土紅的乾癟學術論文），UI 生成必須遵循**「設計資產優先 $\rightarrow$ 無文件時高槓桿諮詢 $\rightarrow$ 八大先鋒流派動態配對 $\rightarrow$ 注入 6 項實體工藝」**的原則，並錨定於專案根目錄的 `DESIGN.md`。

### 1.1 設計資產盤點與 3 維度設計諮詢流程

1. **第一步：搜尋現有設計工程資產**
   - 檢查專案是否具備：`DESIGN.md`、`design-tokens.json`、`tailwind.config.*`、`src/theme/`、Figma Tokens 或全域 CSS 變數。
   - 若存在：**無條件繼承專案已有之色票、字體與規範**，直接載入為生成基準。
2. **第二步：無文件時的主動高槓桿設計諮詢**
   - 若專案無任何設計文件，且使用者未指定風格，**在回覆開頭主動提供「設計諮詢選擇卡」**：
     > 「💡 檢測到專案目前尚未配置設計系統文件（DESIGN.md）。為打造具備品牌識別度與實體工藝感的介面，請確認以下 3 個維度的取向（或由我依業務屬性為您推導最適配型）：
     > 1. **物料質感 (Materiality)**：`[A]` 工業硬體儀器 (Teenage Engineering) / `[B]` 晶體黑曜石高光 (Linear) / `[C]` 現代紙質微噪點 / `[D]` 前衛波普新粗獷 / `[E]` 東方極簡禪境
     > 2. **空間張力 (Spatial Dynamics)**：`[A]` 高密終端資料流 / `[B]` 破格層疊與外溢 / `[C]` 劇院式大器留白
     > 3. **互動態度 (Interaction)**：`[A]` 實體按壓物理阻尼 / `[B]` 精密磁吸光澤 / `[C]` 即時遙測脈衝燈」
3. **第三步：持久化至 `DESIGN.md`**
   - 將確認之設計規範寫入專案根目錄 `DESIGN.md`，杜絕長對話中的上下文稀釋。

---

### 1.2 八大先鋒設計流派完整代碼配方

當專案無既有規範時，自以下八個性格極度鮮明的流派中動態選型：

#### 流派 1：工業硬體儀器風 (Industrial Hardware / Teenage Engineering)
- **氣質**：合成器、硬體終端、精密設備、音訊工程、極客硬體控制台
- **色票**：`--paper: #E5E5E2; --ink: #1C1D1F; --ink-mute: #68696B; --accent: #FF5500; --hairline: #1C1D1F;`
- **字體**：`font-display: 'JetBrains Mono', monospace; font-sans: 'IBM Plex Sans', sans-serif;`
- **物料與幾何**：消光塑料面板、段碼 LED、刻度滾輪、純黑 1px 實線、機械微開關。
- **按鈕語言**：實體機械按鍵（`active:translate-y-1 shadow-[0_3px_0_#1C1D1F]`）。

#### 流派 2：晶體黑曜石高光 (Layered Obsidian & Specular Glass / Linear & Raycast)
- **氣質**：專業開發者工具、高階資安平台、現代生產力應用、新一代 AI 引擎
- **色票**：`--paper: #090A0F; --surface: #12131A; --ink: #F1F3F7; --ink-mute: #717684; --accent: #6366F1;`
- **字體**：`font-sans: 'Plus Jakarta Sans', sans-serif; font-mono: 'JetBrains Mono', monospace;`
- **物料與幾何**：多層黑曜石色階、頂部 1px 內切光學高光 (`box-shadow: inset 0 1px 0 rgba(255,255,255,0.12)`)、結晶微光邊框。
- **按鈕語言**：半透明晶體細框鈕，懸停微反光。

#### 流派 3：前衛波普新粗獷 (Neo-Brutalist Pop / ReadCV & Gumroad)
- **氣質**：青年創意社群、獨立開發者、Web3、前沿設計機構、個人旗艦作品
- **色票**：`--paper: #FEF9EF; --ink: #000000; --hairline: #000000; --accent: #2563EB; --accent-2: #FACC15;`
- **字體**：`font-display: 'Syne', sans-serif; font-mono: 'Space Grotesk', monospace;`
- **物料與幾何**：2.5px 粗黑輪廓、實黑 4px 位移硬陰影、微傾斜貼紙徽章 (`transform: rotate(-2deg)`)。
- **按鈕語言**：粗黑邊框配實黑位移陰影（點擊時位移消除陰影）。

#### 流派 4：現代高奢動態雜誌 (High-Fashion Contemporary Editorial)
- **氣質**：旗艦精品發表、頂級建築與室內設計、文化藝術策展、高階沙龍
- **色票**：`--paper: #0E0E10; --ink: #F5F5F7; --ink-mute: #8E8E93; --accent: #D4AF37;`（亦可為純白反轉）
- **字體**：`font-serif: 'Playfair Display', serif; font-sans: 'General Sans', sans-serif;`
- **物料與幾何**：巨幅襯線大字、全幅攝影邊緣外溢、同句斜體混搭、不對稱跨欄裁剪。
- **按鈕語言**：純文字加粗底線箭頭按鈕，懸停時箭頭右移。

#### 流派 5：科技終端數據流 (Bloomberg HUD & Technical Telemetry)
- **氣質**：金融高頻交易、即時遙測雲端監控、網路安全獵殺、資料管線儀表
- **色票**：`--paper: #0A0E14; --ink: #B3C0D1; --ink-mute: #4E5A6B; --accent: #00F0FF; --accent-warn: #FFB454;`
- **字體**：`font-mono: 'JetBrains Mono', monospace; font-sans: 'IBM Plex Sans', sans-serif;`
- **物料與幾何**：全頁 Mono 驅動、緊湊雙層標籤、ASCII 邊框、即時呼吸脈衝小燈、零浪費空間。
- **按鈕語言**：終端微型線框鈕 (`[ EXECUTE ]`)，懸停翻轉為青光填滿。

#### 流派 6：東方極簡禪境 (Japanese Ma & Wabi-Sabi / MUJI & 原研哉)
- **氣質**：生活哲學、文化展演、冥想音訊、東方茶道與極致慢生活
- **色票**：`--paper: #F4F2EB; --ink: #222421; --ink-mute: #6C7069; --accent: #C23E2B;`
- **字體**：`font-serif: 'Zen Old Mincho' / 'Noto Serif TC', serif; font-sans: 'Noto Sans TC', sans-serif;`
- **物料與幾何**：極限「間」留白、極細纖維線條、手工朱印落款徽章、垂直排版標籤 (`writing-mode: vertical-rl`)。
- **按鈕語言**：極致微弱灰色底色塊，配深墨色沉穩文字。

#### 流派 7：瑞士國際現代網格 (Swiss International Grid / Otl Aicher)
- **氣質**：現代建築、B2B SaaS 核心基礎架構、設計系統工具、先鋒出版
- **色票**：`--paper: #FFFFFF; --ink: #0A0A0A; --ink-mute: #52525B; --accent: #DC2626;`
- **字體**：`font-sans: 'General Sans', sans-serif; font-mono: 'Space Mono', monospace;`
- **物料與幾何**：嚴格非對稱數學網格比例、冷黑白絕對高反差、0px 銳利直角純平幾何塊。
- **按鈕語言**：純黑幾何色塊鈕，懸停切換為瑞士國旗鮮紅，零陰影。

#### 流派 8：北歐溫潤工藝 (Warm Scandinavian Craft)
- **氣質**：永續生活、環保材料、身心健康、教育與自然社群
- **色票**：`--paper: #F5F3ED; --ink: #18291F; --ink-mute: #4D6153; --accent: #65796D;`
- **字體**：`font-serif: 'Newsreader', serif; font-sans: 'Satoshi', sans-serif;`
- **物料與幾何**：微噪點紙質鋪底、4–6px 溫潤微弧度 (`rounded-md`)、低彩度有機自然色塊。
- **按鈕語言**：深苔蘚綠微圓角填色鈕，觸感沉穩自然。

---

### 1.3 人類頂級設計師的 6 項實體工藝方法代碼庫 (Craft Code Recipes)

為徹底打破「純文字枯萎論文感」，介面生成中應積極注入以下工藝組件：

#### 1. 微噪點物料層 (Organic Noise Overlay)
```html
<!-- 全域微噪點物料層：消除數位生硬感，賦予有機物料質地 -->
<div class="fixed inset-0 pointer-events-none z-50 opacity-[0.035] mix-blend-overlay"
     style="background-image: url('data:image/svg+xml;utf8,<svg viewBox=\"0 0 200 200\" xmlns=\"http://www.w3.org/2000/svg\"><filter id=\"n\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.8\" numOctaves=\"3\" stitchTiles=\"stitch\"/></filter><rect width=\"100%\" height=\"100%\" filter=\"url(%23n)\"/></svg>');">
</div>
```

#### 2. 頂部 1px 內切光學高光 (Specular Inset Highlights)
```html
<!-- 模擬物理研磨玻璃與金屬倒角：頂部 1px 內切光澤 + 低瀰散物理陰影 -->
<div class="bg-[#12131A] text-[#F1F3F7] p-8 rounded-lg border border-white/10"
     style="box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12), 0 20px 40px -15px rgba(0, 0, 0, 0.6);">
  <span class="font-mono text-xs text-[#6366F1] uppercase tracking-wider">// Specular Edge</span>
  <h3 class="text-xl font-medium mt-2">精密結晶容器</h3>
</div>
```

#### 3. 複合混搭排版與浮水印 (Mixed Typography & Typographic Watermark)
```html
<!-- 標題同句混搭 + 巨幅幾何背景浮水印 -->
<div class="relative overflow-hidden py-16">
  <!-- 巨幅裝飾浮水印 -->
  <span class="absolute -right-8 -bottom-12 font-mono text-[140px] font-bold text-black/[0.03] select-none pointer-events-none leading-none">
    01
  </span>

  <!-- 複合混搭標題：Grotesk 無襯線中刻意嵌入 Italic Serif -->
  <h2 class="text-4xl md:text-5xl font-sans tracking-tight leading-tight">
    Engineering <span class="font-serif italic font-normal text-[#2563EB]">fault-tolerant</span> architectures for scale.
  </h2>
  
  <!-- 側邊垂直排版時間戳記 -->
  <div class="hidden md:block absolute left-0 top-16 text-xs font-mono text-neutral-400 select-none" style="writing-mode: vertical-rl;">
    REV 2026.11 // SYSTEM SPEC
  </div>
</div>
```

#### 4. 破格與非對稱縱深 (Breaking the Grid & Pinned Rail)
```html
<!-- 黏性側欄導覽 + 右側獨立滑動 + 跨區塊層疊覆蓋 -->
<div class="grid grid-cols-1 md:grid-cols-12 gap-12 relative">
  <!-- 左側 4 欄黏性錨定 -->
  <aside class="md:col-span-4 md:sticky md:top-24 self-start">
    <div class="font-mono text-xs uppercase tracking-widest text-[#FF5500] mb-2">[ TELEMETRY RAIL ]</div>
    <h3 class="text-2xl font-bold tracking-tight">即時節點遙測</h3>
    <p class="text-sm text-neutral-500 mt-4 leading-relaxed">左側固定指標與狀態，右側持續滾動詳細日誌。</p>
  </aside>

  <!-- 右側 8 欄主滾動區 -->
  <div class="md:col-span-8 space-y-16">
    <!-- 跨區塊層疊浮動晶片 (負邊距製造縱深) -->
    <div class="-mt-8 md:-ml-8 bg-[#E5E5E2] border-2 border-black p-4 z-10 relative shadow-[4px_4px_0_#000]">
      <span class="font-mono text-xs font-bold uppercase">✦ Active Pipeline: Node-04 Online</span>
    </div>
    
    <!-- 正常內容清單 -->
    <div class="border-t border-black/20 pt-8">
      <p class="text-base leading-relaxed">長篇業務細節與技術規範在此流暢呈現...</p>
    </div>
  </div>
</div>
```

#### 5. 工藝細節標記與座標戳記 (Bespoke Engineered Signage)
```html
<!-- 工程結構標尺與呼吸燈 -->
<div class="flex items-center justify-between border-t border-b border-black/20 py-2 font-mono text-xs text-neutral-500">
  <div class="flex items-center gap-2">
    <span class="relative flex h-2 w-2">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
    </span>
    <span>SYS.OK [ 10:42:01 UTC ]</span>
  </div>
  <span>+── 25.0330° N // 121.5654° E ──+</span>
  <span class="hidden sm:inline">SCALE: 1:1</span>
</div>
```

#### 6. 實體物理阻尼按鍵 (Tactile Physics Button)
```html
<!-- 具備真實下壓物理手感的按鍵 -->
<button class="border-2 border-black bg-white text-black px-6 py-3 text-xs font-mono font-bold tracking-wider uppercase shadow-[3px_3px_0px_#000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-75">
  Deploy Core System
</button>
```

---

### 1.4 六大非 AI 公版按鈕設計語言庫

嚴禁每次生成都輸出千篇一律的按鈕！依據選定之流派切換以下具備鮮明個性的按鈕形式：

```html
<!-- 形式 A：機械實體下壓鈕 (Industrial Mechanical - 適用 Teenage Engineering) -->
<button class="bg-[#FF5500] text-white border-2 border-[#1C1D1F] px-6 py-2.5 text-xs font-mono uppercase font-bold tracking-widest shadow-[0_3px_0_#1C1D1F] active:translate-y-[3px] active:shadow-none transition-all">
  ENGAGE SWITCH →
</button>

<!-- 形式 B：晶體半透高光鈕 (Specular Glass Inset - 適用 Linear / Raycast) -->
<button class="bg-[#1A1D27] text-[#F1F3F7] border border-white/10 px-5 py-2.5 text-xs font-sans tracking-wide rounded-md hover:border-white/30 hover:bg-[#222634] transition-all"
        style="box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);">
  Launch Workspace
</button>

<!-- 形式 C：雙線反轉線框鈕 (Invertible Outline - 適用 Technical Utilitarian) -->
<button class="border border-slate-900 bg-transparent text-slate-900 px-5 py-2.5 text-xs font-mono tracking-wider rounded-sm hover:bg-slate-900 hover:text-white transition-all">
  [ VIEW SOURCE ]
</button>

<!-- 形式 D：雜誌標題箭頭鈕 (Text Arrow / Underlined - 適用 High-Fashion / Editorial) -->
<a href="#" class="inline-flex items-center gap-2 text-sm font-serif border-b border-[#141413] pb-1 hover:border-[#D4AF37] hover:text-[#D4AF37] transition-colors group">
  <span>探索架構白皮書</span>
  <span class="font-mono text-xs transition-transform group-hover:translate-x-1">→</span>
</a>

<!-- 形式 E：實體硬陰影撞色鈕 (Hard-Shadow Neo-Brutalist - 適用 Neo-Brutalist) -->
<button class="border-2 border-black bg-white text-black px-6 py-2.5 text-xs font-mono uppercase font-bold tracking-wider shadow-[3px_3px_0px_#000] hover:bg-[#2563EB] hover:text-white active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all">
  Deploy Cluster
</button>

<!-- 形式 F：溫潤低飽和微弧度鈕 (Soft Warm Pill - 適用 Warm Scandinavian) -->
<button class="bg-[#18291F] text-[#F5F3ED] px-6 py-3 text-sm font-medium rounded-md hover:bg-[#2A4235] transition-colors">
  開啟專案對話
</button>
```

---

### 1.5 `DESIGN.md` 標準持久化範本

```markdown
# 專案設計系統規範 (DESIGN SYSTEM CONSTRAINTS)

本專案拒絕預設「AI 公版風格」（AI Slop）與「過度禁慾論文風」。所有介面產出必須嚴格遵守以下數值硬約束：

## 1. 字體與階層 (Typography)
- 選定流派：[依據流派庫或專案資產填入]
- 標題字體：`Noto Serif TC` / `Fraunces` / `Playfair Display`（支援同句混搭 Italic Serif）
- 內文字體：`Plus Jakarta Sans` / `IBM Plex Sans` / `Satoshi`
- 程式碼/標記字體：`JetBrains Mono` / `Space Mono`
- 嚴禁字體：禁止使用 `Inter`, `Roboto`, `Arial`，以及次高備案 `Space Grotesk`, `Poppins`, `Manrope`（除非新粗獷流派指定）。
- 字級跳躍比 (Size Jump Ratio)：標題與內文字級比必須 ≥ 3.0 倍。
  - Hero Display: `clamp(40px, 4vw, 64px)`
  - Section Title: `clamp(24px, 2.5vw, 36px)`
  - Body Text: `16px` (1rem), line-height: 1.7
- 字重約束 (Font Weight)：Display 最高 `500`（靠尺寸撐開氣場，嚴禁 700 粗體硬撐）。

## 2. 色彩預算與物料質感 (Color & Materiality)
- 預算上限：全頁最多 3 個強調色；每個強調色整頁最多出現 3 次（全頁總強調點 ≤ 9 個）。
- 基準色票 (採用 OKLCH / CSS 變數)：
  - `--paper`: [依流派選用之底色]
  - `--ink`: [依流派選用之主文字色]
  - `--hairline`: [依流派選用之細線分割色]
  - `--accent`: [依流派選用之單一強調色]
- 物料工藝：[微噪點 SVG 紋理 / 頂部 1px 內切光學高光 / 消光塑料 / 實黑位移陰影 / 純平紙質]
- 漸層禁令：嚴禁紫藍與紫粉多段高飽和漸層，嚴禁霓虹發光與滿版毛玻璃。

## 3. 空間與版面張力 (Spacing & Spatial Dynamics)
- 區塊垂直內距 (Section Padding)：
  - 桌面端：`160px`（`py-40` / `10rem`）以上。
  - 行動端：`96px`（`py-24` / `6rem`）以上。
- 版面結構：
  - 嚴禁全頁 `text-center` 置中。
  - 嚴禁均分三欄卡片網格（`grid-cols-3`）。
  - 強制採用 0-Card 開放式畫布：以 `60/40 不對稱分割`、`破格層疊覆蓋`、`視窗外溢展示` 或 `黏性側欄滑動導覽 (Pinned Rail)`。

## 4. 按鈕與組件幾何
- 按鈕形式：[機械實體下壓 / 晶體半透高光 / 線框反轉 / 雜誌標題箭頭 / 實體硬陰影 / 溫潤微弧度]
- 嚴禁全頁按鈕與容器統一套用 `16px` (`rounded-2xl`)。
```

### 1.6 在專案規則中持久化引用

在專案規則檔（如專案根目錄規格說明、Prompt Rules 或系統設定）中加入：

```markdown
<!-- 前端 UI 生成強制規則 -->
所有前端介面生成、HTML/CSS 修改與元件重構，必須在產出前先讀取根目錄的 `DESIGN.md`。
產出之程式碼若包含 `DESIGN.md` 明令禁止之字體、色彩、三欄卡片或等距留白，視為嚴重格式違規。
```

### 1.7 兩階段強制前置閘門與 7 行合約

在從零建立任何新介面時，模型必須先在輸出開頭寫下 `[設計合約鎖定]` 七行約定，再輸出代碼：

```plaintext
[設計合約鎖定]
- 設計資產來源：Industrial Hardware（消光塑料面板、機械按鍵手感、安全警示橘）
- 色彩表：底色 #E5E5E2 / 主墨 #1C1D1F / 強調 #FF5500（嚴禁紫粉漸層與光暈）
- 字體與級距：JetBrains Mono (56px, weight 500) / IBM Plex Sans (16px, weight 400) -> 3.5x（支援同句混搭）
- 物料與質感：微噪點物料層 (Film Grain 3%) + 消光塑料實黑 1px 線條，無虛浮發光
- 版面骨架與張力：0-Card 開放式畫布，左側 4 欄黏性遙測錨定，右側 8 欄主條目，段落間以工程標尺符號分割
- 按鈕與互動語言：實體機械按鍵（shadow-[0_3px_0_#1C1D1F] active:translate-y-1）
- 禁用確認：無白底圓角卡片堆疊、無 Emoji 標籤、無發光光環、無偽狀態綠點、無樣板套話、無單一暖白枯燥論文複讀
```

#### 0-Card 開放式畫布通用代碼模式（對照白底卡片套路）

此架構通用於各類產品介紹、規格手冊、條目清單與內容介面：

```html
<!-- ❌ 錯誤：AI 常見的「卡片套卡片」垂直堆疊與等寬三欄套路 -->
<div class="bg-slate-100 p-8 flex justify-center">
  <div class="bg-white rounded-2xl shadow-sm p-8 max-w-xl">
    <div class="bg-white rounded-xl shadow-sm p-4 border flex items-center">
      <span class="rounded-full bg-blue-50 p-2">📍</span>
      <p>核心特性：即時分散式串流</p>
    </div>
  </div>
</div>

<!-- ✅ 正確：0-Card 開放式畫布（單一紙色底、1px 細線分割、靠左不對稱，通用各類內容） -->
<main class="min-h-screen bg-[#F5F4F0] text-[#141413] px-8 py-24 md:py-40">
  <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-12 items-start">
    <!-- 左側 4 欄：固定核心識別／導航區塊 -->
    <header class="md:col-span-4 border-t-2 border-[#141413] pt-6 md:sticky md:top-24">
      <h1 class="font-serif text-5xl md:text-6xl font-normal tracking-tight leading-none">Apex Engine</h1>
      <p class="font-mono text-xs uppercase tracking-widest text-neutral-500 mt-2">High-Throughput Stream Pipeline</p>
      <p class="text-sm text-neutral-600 mt-6 leading-relaxed">
        專注於低延遲分散式資料流處理與高頻時序監控。以零記憶體拷貝架構支撐每秒數十萬筆即時訊息吞吐。
      </p>
    </header>

    <!-- 右側 8 欄：主條目列表（以 1px hairline 分割，無圓角白卡） -->
    <div class="md:col-span-8 space-y-16">
      <section class="border-t border-neutral-300 pt-6">
        <h2 class="font-mono text-xs uppercase tracking-widest text-[#B84A2E] mb-6">系統規格與效能指標</h2>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-y-8 gap-x-12 text-sm">
          <div>
            <dt class="font-mono text-xs text-neutral-500 uppercase">Throughput</dt>
            <dd class="font-medium mt-1">250,000 ops / sec</dd>
          </div>
          <div>
            <dt class="font-mono text-xs text-neutral-500 uppercase">Latency</dt>
            <dd class="font-medium mt-1">p99 < 1.2ms (Zero-Copy Buffer)</dd>
          </div>
        </dl>
      </section>
    </div>
  </div>
</main>
```

---

## 2. 注入「負向黑名單」提示詞（含次高機率防滑落與裝飾性套路）

大型語言模型在推理時具備極佳的負向排除能力，但若只禁止第一層預設，會觸發「次高機率滑落現象」（例如禁了紫藍漸層就滑向紫粉漸層、禁了 SaaS 卡片就滑向置中 Bento 盒）。必須連同替代品一併封鎖。

### 2.1 複製即用提示詞區塊 (`<anti_slop_constraints>`)

```xml
<anti_slop_constraints>
1. 禁止色彩與光影變種：
   - 嚴禁使用紫藍漸層 (violet-to-indigo) 及任何紫粉漸層 (pink/fuchsia/purple/rose)。
   - 嚴禁千篇一律複讀單一暖白陶土色調（純暖白底 #F5F4F0 配陶土赭紅 #B84A2E，通篇無物料感無深度）。
   - 嚴禁頭像、圖標或容器外圍套上紫色/粉色發光圓環 (glowing rings)。
   - 嚴禁在深色模式套用亮青色 (Cyan) 霓虹發光，嚴禁背景散落高斯模糊彩色光球 (blur-2xl / blur-3xl blobs)。
   - 嚴禁點陣網格背景 (dot grid) 與滿版毛玻璃 (backdrop-blur)。

2. 禁止容器結構與排版套路：
   - 嚴禁「卡片套卡片」垂直堆疊結構（白底大圓角卡片包多張白底小圓角卡片，外加微弱陰影）。
   - 強制採用「0-Card 開放式畫布」：內容直接坐在單一紙色背景上，僅以留白與 1px 實線細線 (hairline) 分隔。
   - 嚴禁全頁 text-center 置中（大標題可置中，但副標、內文與說明一律靠左對齊）。
   - 嚴禁 grid-cols-3 等寬圖示卡片；嚴禁在項目旁放置藍底、黃底、紫底的淺色圓圈線條小圖示。
   - 嚴禁區塊垂直留白小於 120px（桌面端強制 ≥ 160px）。
   - 嚴禁通篇死板遵循 12 欄且毫無層疊外溢的乾枯平面排版（缺乏深度與主次呼吸）。

3. 裝飾性假元素與微元件禁令：
   - 嚴禁無功能意義的懸浮偽狀態指示器（如帶綠點的 🟢「探索新機會中/Available/Live/Active」等無實際狀態綁定的偽 Badge）。
   - 嚴禁孤立的圓形圖示按鈕無端堆疊。
   - 嚴禁在標籤、按鈕或條目中塞入純裝飾性 Emoji 藥丸海（如 💻、🎨、⚡、🤖、☕、🚀、🔥 等）。

4. 禁止字體與字重套路：
   - 嚴禁使用：Inter, Roboto, Arial, system-ui，且嚴禁次高備案：Space Grotesk, Poppins, Manrope。
   - 嚴禁在 Hero / Display 大標題一律硬套 font-weight: 700 / 800；必須採用 400-500 字重配合 3 倍以上字級跳躍。

5. 禁止假文案與 AI 萬用樣板套話：
   - 嚴禁任何無個性的模板空話（如「熱衷於打造優雅、直覺且具備極佳體驗…」、「在技術與美感之間找到平衡」、「Unlock the power of...」、「簡單、快速、強大」等換成任何主題皆通用的套話）。
   - 第一句文案必須直接陳述具體的系統功能、業務事實或實際解決的工程/產品問題。
   - 無真實數據時嚴禁放置 5 顆黃星與抽象幾何頭像。
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

## 6. 反覆直接觀看與雙重審查閉環 (Iterative Visual Critique Loop)

「代碼只是假設，渲染才是事實」。生成初版後，嚴禁僅憑原始碼推論樣式，必須建立**「啟動預覽 → 直接觀看 → 批判反思 → 修改代碼 → 再次觀看」**的反覆視覺閉環。完整技術細節請參閱 [VISUAL_INSPECTION.md](VISUAL_INSPECTION.md)。

### 6.1 啟動預覽與瀏覽器直接觀看

1. **啟動預覽服務**：
   - 專案已有開發伺服器時：執行 `npm run dev` 或 `vite`。
   - 靜態 HTML 頁面時：執行 `python3 skills/frontend-anti-slop/scripts/serve_preview.py path/to/page.html`。
2. **調度瀏覽器直接觀看**：
   - 在 Antigravity 環境下：立即調度 **`browser` subagent** 導航至 `http://localhost:PORT`，直接檢視視覺呈現、截取全頁長截圖，並讀取 DOM 節點實際渲染樣式。
   - 在本機環境下：打開瀏覽器訪問該網址，或執行無頭瀏覽器截圖腳本捕捉高解析度全頁視圖。
3. **受保護頁面（需登入）處置**：
   - 若目標頁面受 Auth Guard 保護會自動重導至登入頁：
     - **優先推薦（策略 A）**：在開發環境建立 Mock Auth 預覽路由（如 `src/pages/preview/dashboard.tsx`，以 Mock Context 直接渲染目標組件），徹底解耦後端與認證。
     - **真實會話（策略 B）**：調度 `browser` subagent 打開登入頁，由人類使用者在可見視窗中登入（支援 2FA/SSO/CAPTCHA），完成後 Agent 刷新目標頁面直接觀看。
     - **快速注入（策略 C）**：在 Console 注入測試 `localStorage` Token。詳細規範見 [VISUAL_INSPECTION.md](VISUAL_INSPECTION.md) 第 5 節。

### 6.2 第一道：視覺批判審查與反覆迭代 (Visual Critique Pass)

依據實際渲染的像素畫面，執行以下批判檢驗：

1. **遠看測試（Squint Test）**：將視線模糊或縮小至 25%，整頁是否有單一清晰的視覺錨點？若全頁有 10 個發光亮點或彩色彩球，代表色彩預算超標，立即將非核心元素降為中性灰墨色。
2. **3 秒 AI 味辨識**：頁面是否一眼能看出 shadcn/ui 或 Tailwind 預設？檢查是否有紫藍漸層、rounded-2xl 泛濫或均分三欄。
3. **節奏檢查**：垂直滾動時，各區塊的高度與留白是否均等死板？實際測量 Section 垂直內距是否達到 **160px** 以上；若有壓迫感，將某一區拉大至 200px，或將橫向寬度收窄為單欄。
4. **提取真實計算樣式 (Computed Styles)**：
   - 在瀏覽器 Console 中執行測量腳本（見 [VISUAL_INSPECTION.md](VISUAL_INSPECTION.md) 第 4 節），核對實際計算之 `font-size`、`padding-top` 與 `border-radius`。
5. **代碼修改後「再次直接觀看」**：
   - 每次修改 CSS 或組件結構後，**必須重新整理頁面並直接觀看改動後的截圖**。
   - 進行前後像素疊加對比，確認 AI 味特徵逐項消退，直到 16 項標誌降至 0–1 項。

### 6.3 跨斷點響應式巡檢 (Responsive Multi-Breakpoint Check)

切換瀏覽器視窗寬度，反覆直接觀看三個標準斷點：
- **桌面端（1440px / 1280px）**：確認 12 欄不對稱網格展開流暢，呼吸留白充裕。
- **平板端（768px）**：確認欄位折疊順序正確，圖表與數據未破版。
- **行動端（375px）**：確認主標題折行自然（避免孤字落單）、留白收縮至 96px、按鈕觸控區域 ≥ 44×44px。

### 6.4 第二道：功能性與無障礙補齊 (a11y & Engineering Pass)

AI 最常偷懶的是表單互動與無障礙屬性，在視覺收斂後逐項補齊：

- [ ] **表單必填標示**：所有必填輸入框必須有明確標示（如紅星 `*` 或「必填」文字），且不可僅依賴 placeholder。
- [ ] **行內驗證與錯誤提示**：輸入錯誤時，提供包含 `text-red-600`、`text-sm`、`role="alert"` 的具體錯誤提示，並將輸入框邊框高亮。
- [ ] **鍵盤導航焦點框**：按鈕、連結與輸入框不可移除 outline；必須提供清晰的 `:focus-visible` 樣式（如 `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-accent`）。
- [ ] **無障礙屬性 (ARIA)**：圖示按鈕必須包含 `aria-label`；展開折疊組件必須有 `aria-expanded`；載入狀態必須有 `aria-busy`。
- [ ] **對比度標準**：內文與背景對比度必須符合 WCAG AA 標準（常態文字 ≥ 4.5:1，大標題 ≥ 3:1）。
