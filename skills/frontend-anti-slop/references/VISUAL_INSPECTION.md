# 網頁即時觀看與視覺閉環指南 (Visual Inspection)

> **核心準則**：代碼只是假設，渲染才是事實（Code is hypothesis, rendered pixels are the ground truth）。
> 消除「AI 味」不能僅靠閱讀原始碼或憑空想像樣式，必須建立**「修改代碼 → 渲染呈現 → 直接觀看 → 批判反思 → 再次微調 → 再次觀看」**的反覆視覺閉環。

---

## 1. 為什麼必須「反覆直接觀看網頁」？

AI 模型在撰寫 CSS 與 Tailwind 時，極易產生「視覺幻覺」（Hallucinated Visuals）：
1. **CSS 特異度與繼承失效**：代碼中寫了樣式，但在真實 DOM 樹中可能被第三方庫覆蓋或未被編譯生效。
2. **文字斷行與節奏錯亂**：18 個字的大標題在 1440px 桌面端與 375px 手機端的文字折行（Line-wrapping）完全不同；不看渲染結果，無法判斷是否造成字體落單（Widows/Orphans）或破壞閱讀節奏。
3. **留白感知壓迫**：代碼裡的 `py-16`（64px）看起來有留白，但實際在大螢幕渲染時，視覺壓迫感極重，唯有遠看才能體會呼吸感是否充裕。
4. **色彩預算失控**：多個元件各自帶有一點紫藍或青色發光，累積到全頁時會形成嚴重的色彩雜訊；靜態審查難以量化全頁總彩度，必須直接觀看整頁渲染。

---

## 2. 直接觀看的四大維度

在每一次觀看頁面時，必須依序檢驗以下四個維度：

### 2.1 遠看測試 (Squint Test) 與首屏視覺錨點
- **操作方式**：將視線模糊、將頁面縮小至 25%–33%，或觀看整體全景截圖。
- **檢驗重點**：
  - 整頁是否具備**單一且清晰的主視覺焦點**（通常是 Display 大標題或單一主行動 CTA）？
  - 是否有均勻散布的 5–8 個發光卡片或彩虹標籤在搶奪注意力？若是，立即將次要元素的彩度歸零（降為中性灰墨色）。

### 2.2 垂直節奏與留白呼吸感
- **操作方式**：從頁首緩慢向下滑動至頁尾，觀察區塊交界處。
- **檢驗重點**：
  - 各 Section 之間是否有「豁然開朗」的大器留白？實際測量垂直內距是否達到 **160px** 以上。
  - 各區塊的高度是否完全均等死板？如果是「卡片區高 400px → 輪播區高 400px → 定價區高 400px」，立刻打破節奏，將其中一區拉大為長卷軸，或另一區收窄為緊湊單列。

### 2.3 字級跳躍比與字重張力
- **操作方式**：聚焦於標題與其緊鄰的副標題／內文。
- **檢驗重點**：
  - 主標題是否達到內文的 **3.0 倍以上**（例如大標 56px 對比內文 16px）？
  - 大標題是否被硬套了 700/800 粗體而顯得笨重？嘗試將字重降為 `400`（襯線體）或 `500`（無襯線體），改以尺寸拉開層級。
  - 內文是否一律靠左對齊？檢視是否還有殘留的 `text-center` 導致閱讀視線反覆跳躍。

### 2.4 跨斷點響應式觀看 (Responsive Breakpoint Inspection)
- **操作方式**：在三種標準視窗寬度下反覆切換觀看：
  - **桌面端（1440px / 1280px）**：檢驗 12 欄不對稱網格（60/40 分割）與超大留白表現。
  - **平板端（768px）**：檢驗雙欄佈局是否合理降級，圖表與表格是否維持可讀性。
  - **行動端（375px）**：檢驗文字斷行是否自然、留白是否收斂至 `96px`（避免手機端過度浪費螢幕空間）、按鈕是否具備足夠點擊面積（≥ 44×44px）。

---

## 3. 反覆觀看與迭代重構的標準閉環

```
  ┌─────────────────────────────────────────────────────────┐
  │ 1. 啟動預覽 (Local Dev Server / Static HTTP Server)     │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. 瀏覽器直接觀看 (Browser Subagent / DevTools / 截圖)  │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. 視覺診斷與特徵標記 (Squint Test + 16 項 Slop 檢查)   │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. 取得真實計算樣式 (Computed Styles: padding, font)    │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. 執行局部代碼重構 (改寫 CSS / Tailwind / HTML 結構)    │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 6. 重新直接觀看 (驗證改善成果，進行前後截圖對比)        │
  └────────────────────────────┬────────────────────────────┘
                               │
                     [是否達到 Clean 等級?]
                    /                      \
               (否, 仍有 AI 味)          (是, 0–1 項)
                  /                          \
                 ▼                            ▼
        回到步驟 3 再次迭代              跨斷點巡檢並交付
```

### 操作細節說明：

1. **啟動預覽**：
   - 專案已有建置工具時：啟動 `npm run dev` 或 `vite`。
   - 純靜態 HTML 時：執行 `python3 -m http.server 8080` 或直接載入檔案。
2. **直接觀看與截圖**：
   - 在 Antigravity 環境中，若需要觀看本機或線上網頁，可立即調度 **`browser` subagent** 導航至 `http://localhost:PORT`，直接檢視視覺外觀、DOM 結構與 Computed Styles。
   - 捕捉關鍵視角截圖（包含全頁完整滾動長截圖、首屏 Hero 截圖、行動端 375px 截圖）。
3. **定位違規節點並提取計算樣式**：
   - 不只猜測代碼，直接從瀏覽器獲取實際渲染值：
     ```javascript
     // 在瀏覽器 Console 中快速測量實際渲染數據
     const h1 = document.querySelector('h1');
     const p = document.querySelector('p');
     const h1Size = parseFloat(window.getComputedStyle(h1).fontSize);
     const pSize = parseFloat(window.getComputedStyle(p).fontSize);
     console.log('字級跳躍比 (Jump Ratio):', (h1Size / pSize).toFixed(2));
     console.log('主標題實際字重 (Weight):', window.getComputedStyle(h1).fontWeight);
     ```
4. **代碼修改與重載**：
   - 依據視覺診斷，修改對應元件原始碼（例如：將 `py-16` 改為 `py-40`，將 `rounded-2xl` 改為 `rounded-sm`）。
5. **再次直接觀看**：
   - 重新刷新瀏覽器頁面或重新截圖，將改動後的像素與前一版本直接對照。
   - 確保違規特徵逐項消退，直到 16 項標誌降至 0–1 項。

---

## 4. 瀏覽器自動化視覺診斷腳本 (Console Overlay Script)

可將以下 JavaScript 代碼直接貼入瀏覽器 DevTools 控制台（或由代理人在瀏覽器頁面中執行），腳本會在畫面上**以視覺高亮標記所有 AI Slop 違規元素**，並在控制台輸出即時數據報告：

```javascript
(function auditAiSlopInBrowser() {
  console.clear();
  console.log("%c🔍 正在執行前端 AI Slop 視覺掃描...", "font-weight: bold; font-size: 14px; color: #0F766E;");
  
  const report = {
    slopCount: 0,
    issues: []
  };

  // 1. 檢測 Section 垂直留白
  document.querySelectorAll('section, main > div').forEach((sec, idx) => {
    const cs = window.getComputedStyle(sec);
    const pt = parseFloat(cs.paddingTop);
    const pb = parseFloat(cs.paddingBottom);
    if ((pt < 120 || pb < 120) && sec.offsetHeight > 200) {
      report.slopCount++;
      report.issues.push(`Section #${idx + 1} 垂直內距過小 (PT: ${pt}px, PB: ${pb}px，標準需 ≥ 160px)`);
      sec.style.outline = "2px dashed #B45309";
    }
  });

  // 2. 檢測字級跳躍比與字重
  const h1 = document.querySelector('h1');
  const bodyP = document.querySelector('p');
  if (h1 && bodyP) {
    const h1Size = parseFloat(window.getComputedStyle(h1).fontSize);
    const pSize = parseFloat(window.getComputedStyle(bodyP).fontSize);
    const ratio = h1Size / pSize;
    const weight = window.getComputedStyle(h1).fontWeight;
    
    if (ratio < 2.5) {
      report.slopCount++;
      report.issues.push(`字級跳躍比不足 (${ratio.toFixed(2)} 倍，標準需 ≥ 3.0 倍)`);
      h1.style.outline = "2px solid #EF4444";
    }
    if (parseInt(weight) >= 700) {
      report.slopCount++;
      report.issues.push(`主標題字重過重 (${weight}，建議降至 400-500 靠尺寸撐開)`);
    }
  }

  // 3. 檢測 rounded-2xl (16px) 泛濫
  let r16Count = 0;
  document.querySelectorAll('*').forEach(el => {
    const cs = window.getComputedStyle(el);
    if (cs.borderRadius === '16px' || cs.borderRadius === '24px') {
      r16Count++;
      if (r16Count > 4) {
        el.style.outline = "1px solid #8B5CF6";
      }
    }
  });
  if (r16Count > 4) {
    report.slopCount++;
    report.issues.push(`全頁泛濫套用 16px/24px 圓角 (發現 ${r16Count} 處，需建立圓角階層)`);
  }

  // 4. 檢測全頁置中 text-center
  let centerCount = 0;
  document.querySelectorAll('p, li, span, h2, h3').forEach(el => {
    if (window.getComputedStyle(el).textAlign === 'center') {
      centerCount++;
    }
  });
  if (centerCount > 6) {
    report.slopCount++;
    report.issues.push(`內文過度置中 (發現 ${centerCount} 個置中文字元素，內文建議左對齊)`);
  }

  // 5. 輸出視覺檢測報告
  console.log(`%c檢測結果：命中 ${report.slopCount} 項違規特徵`, "font-size: 16px; font-weight: bold; color: " + (report.slopCount >= 4 ? "#DC2626" : report.slopCount >= 2 ? "#D97706" : "#059669"));
  report.issues.forEach(msg => console.warn("⚠️ " + msg));
  console.log("%c違規元素已在頁面中加上彩色虛線外框標記（紅色：字級，橘色：留白，紫色：圓角）。", "color: #6B7280;");
})();
```

---

## 5. 受保護頁面（需登入）的視覺觀看與應對方案 (Inspecting Auth-Protected Pages)

當需要審查的介面屬於受權限保護的後台（如 Dashboard、管理後台、帳號設定頁），未登入會自動重導至 `/login` 或觸發 401/403 時，依據工程優先級提供以下 4 種標準處置方案：

### 5.1 策略 A：前端 Mock Auth 獨立預覽路由（最推薦：解耦、高效、零資安風險）
- **核心思維**：UI 視覺審查的重點是**「排版張力、留白節奏、字級對比與組件幾何」**，不需要依賴真實的後端 API、生產資料庫或 OAuth 服務。
- **實作步驟**：
  1. 在開發環境建立一個獨立的預覽包裝器（Preview Wrapper），例如在 `src/pages/preview/dashboard.tsx` 或 Storybook 中包覆假資料上下文：
     ```tsx
     // 範例：使用 Mock 上下文直接渲染目標受保護元件
     export default function PreviewDashboard() {
       const mockUser = { id: "u-dev-01", name: "Alex Chen", role: "admin" };
       return (
         <AuthContext.Provider value={{ isAuthenticated: true, user: mockUser }}>
           <DashboardLayout>
             <DashboardOverviewPage />
           </DashboardLayout>
         </AuthContext.Provider>
       );
     }
     ```
  2. 或在前端路由守衛（Auth Guard）中加入僅限開發模式生效的旁路參數（如 `?mockAuth=true`）。
- **優勢**：完全靜態化、免後端依賴、無 Token 過期問題，Agent 與開發者隨時可直接觀看並極速熱重載。

### 5.2 策略 B：人機協同登入 (Human-in-the-Loop Auth Session)
- **核心思維**：若系統包含 2FA 雙重驗證、第三方 OAuth（社群登入/SSO）或人機驗證（CAPTCHA），Agent 絕不可嘗試破解，應交由人類在同一個瀏覽器分頁中完成登入。
- **操作步驟**：
  1. Agent 調度 **`browser` subagent** 打開登入頁面（如 `http://localhost:3000/login`）。
  2. Agent 在對話中主動提示使用者：「**已為您在瀏覽器開啟登入頁面，請您在可見分頁中完成登入；完成後請回覆『已登入』，我將接續進行視覺排版審查。**」
  3. 使用者完成登入後，瀏覽器保留 Session Cookie 與 LocalStorage。
  4. Agent 使用 `send_message` 接續原 `browser` subagent，直接導航至目標受保護網址（如 `http://localhost:3000/dashboard`），即可直接觀看登入後的完整排版畫面。

### 5.3 策略 C：開發環境 Session / Token 快速注入
- **核心思維**：現代 SPA 應用多將登入狀態存放在 `localStorage` 或 Cookie。
- **操作步驟**：
  - 在調度瀏覽器開啟目標頁面前，或在 DevTools 控制台中直接執行注入腳本：
    ```javascript
    // 注入測試用 JWT Token 或認證旗標
    localStorage.setItem("auth_token", "mock_dev_jwt_token_for_ui_audit");
    localStorage.setItem("user_profile", JSON.stringify({ id: 1, name: "Test Admin", role: "admin" }));
    // 重新整理以觸發前端狀態載入
    location.reload();
    ```
  - 若使用 Playwright / Puppeteer，可直接載入預存之 `storageState.json`。

### 5.4 策略 D：測試環境 Seed 帳號自動登入
- **核心思維**：本機或 Staging 環境若配備固定的假資料種子帳號（如 `test@example.dev / password123`）。
- **操作步驟**：
  - Agent 透過 `browser` subagent 自動定位 `input[type="email"]` 與 `input[type="password"]`，填入測試憑證並點擊提交按鈕，等待導航完成後自動展開視覺審查。

### 5.5 安全與合規底線（Security Red Lines）
1. **嚴禁索取真實密碼**：絕對不要求使用者在對話中提供真實個人密碼或正式生產環境憑證。
2. **絕不繞過 CAPTCHA 驗證**：若遇 Cloudflare Turnstile、reCAPTCHA 或 hCaptcha，必須由使用者在可見視窗中手動點擊完成，遵守安全規範。

---

## 6. 跨環境觀看作業指引

### 5.1 在 Antigravity 環境中
- 當需要直接觀看頁面時，委派給 **`browser` subagent**：
  - 「請開啟 `http://localhost:3000`，截取目前首頁的全頁長截圖，並檢查 H1 的計算字級與各 Section 的 paddingTop。」
  - 收到 browser agent 回傳的截圖或 DOM 數據後，直接進行視覺批判。
  - 修改代碼後，再次傳送訊息請 browser agent 重新整理頁面並截圖，反覆觀看直到確認排版合格。

### 5.2 在一般終端機或程式輔助環境（CLI / Terminal）中
- 啟動本地靜態預覽：
  ```sh
  python3 skills/frontend-anti-slop/scripts/serve_preview.py path/to/index.html --port 8080
  ```
- 若安裝有 Playwright 或 Puppeteer，可執行自動化無頭截圖並由模型直接讀取截圖圖片檔進行多模態視覺判讀。
- 開發者亦可直接在本機瀏覽器打開該網址，貼入上述 Console Inspector 腳本進行輔助校驗。
