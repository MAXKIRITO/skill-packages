#!/usr/bin/env python3
"""
audit_slop.py - Static scanner for AI design slop anti-patterns.
Inspects HTML, JSX, TSX, Vue, and CSS files for common AI-generated UI signatures.
No external dependencies required (uses standard library re, sys, argparse, pathlib).
"""

import argparse
from pathlib import Path
import re
import sys

# Define 16 AI Slop detection patterns
SLOP_PATTERNS = [
    {
        "id": "SLOP-01",
        "name": "紫藍多段漸層 (Violet/Indigo Gradient)",
        "category": "色彩與背景",
        "regex": re.compile(
            r"(from-violet|to-indigo|via-purple|from-purple|to-violet|linear-gradient\([^)]*(#7c3aed|#6366f1|#8b5cf6|violet|indigo))",
            re.IGNORECASE,
        ),
        "fix": "改用純色、OKLCH 色票或低彩度中性色 (如 neutral-900 / white)。",
    },
    {
        "id": "SLOP-02",
        "name": "預設字體 Inter / Roboto",
        "category": "字體與字重",
        "regex": re.compile(r"font-family:[\s\"']*['\"]?(Inter|Roboto|Arial)['\"]?", re.IGNORECASE),
        "fix": "引入具備品牌個性的字體 (如 Fraunces, Plus Jakarta Sans, IBM Plex Sans)。",
    },
    {
        "id": "SLOP-03",
        "name": "次高機率滑落字體 Space Grotesk",
        "category": "字體與字重",
        "regex": re.compile(r"font-family:[\s\"']*['\"]?Space Grotesk['\"]?", re.IGNORECASE),
        "fix": "避免模型退回第二常見預設；改用經典襯線或工藝等寬體。",
    },
    {
        "id": "SLOP-04",
        "name": "全頁過度置中 (text-center Overuse)",
        "category": "版面與序列",
        "regex": re.compile(r"\btext-center\b", re.IGNORECASE),
        "threshold": 4,  # Over 4 occurrences indicates full-page centering
        "fix": "內文、副標與說明一律靠左對齊 (text-left)，僅大標題允許置中。",
    },
    {
        "id": "SLOP-05",
        "name": "均分三欄卡片 (grid-cols-3)",
        "category": "版面與序列",
        "regex": re.compile(r"\bgrid-cols-(?:1\s+md:)?3\b|\bmd:grid-cols-3\b", re.IGNORECASE),
        "fix": "改用 60/40 不對稱分割、交錯圖文列或單一主視覺 Tab 切換。",
    },
    {
        "id": "SLOP-06",
        "name": "圓圈包覆打勾圖示 (Checkmark Circle)",
        "category": "裝飾與佔位",
        "regex": re.compile(r"bg-(?:emerald|green|indigo|purple)-500\/10[^>]*rounded-full", re.IGNORECASE),
        "fix": "去除無意義裝飾性底色圓圈，改為純文字列表或極細 1px 線條隔開。",
    },
    {
        "id": "SLOP-07",
        "name": "懸浮發光假儀表板截圖",
        "category": "版面與序列",
        "regex": re.compile(r"(?:rotate-\[-?\d+deg\]|shadow-(?:2xl|purple|indigo))[^>]*(?:dashboard|mockup|screenshot)", re.IGNORECASE),
        "fix": "放置真實產品功能展示或互動式 Live Demo，避免傾斜發光假截圖。",
    },
    {
        "id": "SLOP-08",
        "name": "頂部小膠囊標籤 (Pill Badges)",
        "category": "裝飾與佔位",
        "regex": re.compile(r"rounded-full\s+border[^>]*\b(?:text-xs|text-sm)\b[^>]*>(?:New|v\d|Announcing|Introducing|Beta)", re.IGNORECASE),
        "fix": "非必要時直接移除，或以簡約次標題取代膠囊標籤。",
    },
    {
        "id": "SLOP-09",
        "name": "滿版毛玻璃 (backdrop-blur Overuse)",
        "category": "元件與圓角",
        "regex": re.compile(r"\bbackdrop-blur-(?:md|lg|xl|sm)\b", re.IGNORECASE),
        "threshold": 3,
        "fix": "改用乾淨實色背景配 1px 極細邊框 (border-hairline)。",
    },
    {
        "id": "SLOP-10",
        "name": "點陣網格背景 (Dot Grid / Mesh)",
        "category": "色彩與背景",
        "regex": re.compile(r"radial-gradient\([^)]*1px[^)]*transparent|bg-\[radial-gradient|dot-pattern", re.IGNORECASE),
        "fix": "回歸紙張質感的乾淨純色背景，杜絕模板化網格點陣。",
    },
    {
        "id": "SLOP-11",
        "name": "模糊霓虹光暈 (Blurred Blobs)",
        "category": "色彩與背景",
        "regex": re.compile(r"blur-(?:2xl|3xl)[^>]*(?:bg-purple|bg-indigo|bg-violet|bg-cyan)", re.IGNORECASE),
        "fix": "移除角落彩色高斯模糊光球，避免視覺雜訊。",
    },
    {
        "id": "SLOP-12",
        "name": "無差別 rounded-2xl 圓角",
        "category": "元件與圓角",
        "regex": re.compile(r"\brounded-2xl\b|\brounded-3xl\b", re.IGNORECASE),
        "threshold": 4,  # If used indiscriminately on buttons, cards and containers
        "fix": "建立圓角階層 (按鈕 4px / 卡片 8px / 容器 0px)，或全頁採 0px 銳利工藝風。",
    },
    {
        "id": "SLOP-13",
        "name": "假五星好評與幾何頭像",
        "category": "裝飾與佔位",
        "regex": re.compile(r"(?:dicebear|avatar-placeholder|api\.dicebear\.com|text-amber-400[^>]*★|yellow-400[^>]*★)", re.IGNORECASE),
        "fix": "改用真實客戶引文與文字姓名縮寫；無真實資料時直接省略評價區。",
    },
    {
        "id": "SLOP-14",
        "name": "萬用空洞標語文案 (Generic Copy)",
        "category": "文案與功能",
        "regex": re.compile(
            r"(Unlock the (?:power|future) of|Supercharge your|All-in-one platform|簡單[、，]快速[、，]強大|打造新一代|一站式解決方案)",
            re.IGNORECASE,
        ),
        "fix": "由真實產品功能、量化數字與品牌故事出發撰寫微文案。",
    },
    {
        "id": "SLOP-15",
        "name": "缺乏鍵盤 Focus 狀態 (Focus Removed)",
        "category": "文案與功能",
        "regex": re.compile(r"focus:outline-none(?!.*focus-visible:ring)", re.IGNORECASE),
        "fix": "補齊 focus-visible:ring-2 樣式，符合 WCAG 無障礙鍵盤導航規範。",
    },
    {
        "id": "SLOP-16",
        "name": "區塊留白狹窄擁擠 (Tight Section Padding)",
        "category": "版面與序列",
        "regex": re.compile(r"<section[^>]*\b(?:py-12|py-16|py-20)\b", re.IGNORECASE),
        "fix": "主要 Section 垂直留白拉大至 py-36 或 py-40 (≥ 160px)。",
    },
]


def audit_content(content: str, filename: str = "input") -> dict:
    hits = []
    lines = content.splitlines()

    for pattern in SLOP_PATTERNS:
        matches = []
        regex = pattern["regex"]
        threshold = pattern.get("threshold", 1)

        for line_idx, line in enumerate(lines, 1):
            for match in regex.finditer(line):
                matches.append((line_idx, match.group(0)))

        if len(matches) >= threshold:
            hits.append(
                {
                    "id": pattern["id"],
                    "name": pattern["name"],
                    "category": pattern["category"],
                    "count": len(matches),
                    "fix": pattern["fix"],
                    "locations": matches[:5],  # First 5 locations
                }
            )

    score = len(hits)
    if score >= 4:
        grade = "HEAVY AI SLOP (重度 AI 味 - 強烈建議全面重構)"
        status = "FAIL"
    elif score >= 2:
        grade = "MILD AI SLOP (中度 AI 味 - 建議針對性修正)"
        status = "WARN"
    else:
        grade = "CLEAN (乾淨無公版痕跡 - 符合高標準人類設計規範)"
        status = "PASS"

    return {
        "filename": filename,
        "score": score,
        "total_rules": len(SLOP_PATTERNS),
        "status": status,
        "grade": grade,
        "hits": hits,
    }


def print_report(result: dict):
    print("=" * 72)
    print("  FRONTEND ANTI-SLOP AUDIT REPORT (前端去 AI 味檢測報告)")
    print("=" * 72)
    print(f"檔案名稱 : {result['filename']}")
    print(f"命中特徵 : {result['score']} / {result['total_rules']} 項")
    print(f"評定等級 : [{result['status']}] {result['grade']}")
    print("-" * 72)

    if not result["hits"]:
        print("🎉 未偵測到明顯 AI 公版特徵，版面與樣式符合人類設計系統規範！")
    else:
        print("檢測出之違規特徵與改善建議：\n")
        for hit in result["hits"]:
            loc_str = ", ".join(f"L{loc[0]}" for loc in hit["locations"])
            if hit["count"] > len(hit["locations"]):
                loc_str += f" 等 {hit['count']} 處"
            print(f"[{hit['id']}] {hit['name']} ({hit['category']}) - 命中 {hit['count']} 次")
            print(f"  位置 : {loc_str}")
            print(f"  解法 : {hit['fix']}")
            print()

    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="Audit source files (HTML/JSX/TSX/Vue/CSS) for AI design slop anti-patterns."
    )
    parser.add_argument("paths", nargs="*", help="File or directory paths to audit")
    args = parser.parse_args()

    if not args.paths:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
            res = audit_content(content, filename="stdin")
            print_report(res)
            sys.exit(1 if res["score"] >= 4 else 0)
        else:
            parser.print_help()
            sys.exit(1)

    total_slop = 0
    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="ignore")
            res = audit_content(content, filename=str(path))
            print_report(res)
            total_slop += res["score"]
        elif path.is_dir():
            for ext in [".html", ".jsx", ".tsx", ".vue", ".css"]:
                for file_path in path.rglob(f"*{ext}"):
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    res = audit_content(content, filename=str(file_path))
                    print_report(res)
                    total_slop += res["score"]
        else:
            print(f"錯誤：找不到檔案或路徑 {path_str}", file=sys.stderr)

    sys.exit(1 if total_slop >= 4 else 0)


if __name__ == "__main__":
    main()
