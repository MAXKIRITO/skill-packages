#!/usr/bin/env python3
"""
verify_design_spec.py - 人本設計規格書 (Design Spec) 合規性靜態校驗器

檢查設計規格書是否符合人本設計思考架構：
1. 雙鑽石前置定義（Persona、核心任務、真實文案約束）
2. 60-30-10 色彩比例與 OKLCH / 語意色票宣告
3. 模組化字階（Modular Type Scale）與行寬約束
4. 8pt / 4pt 空間網格與留白階梯
5. 必備 8 大互動狀態機完整度（Default, Hover, Focus-Visible, Active, Disabled, Loading, Error, Empty）
6. 三方頭腦互搏攻防與裁決記錄

使用方式：
    python3 verify_design_spec.py --spec path/to/design_spec.md [--json] [--strict]
"""

import argparse
import json
import re
import sys
from pathlib import Path

MANDATORY_STATES = [
    "default",
    "hover",
    "focus",  # matches focus or focus-visible
    "active",  # matches active or pressed
    "disabled",
    "loading",
    "error",
    "empty"
]

CORE_SECTIONS = {
    "persona_and_tasks": [r"persona", r"核心任務|使用者任務|core task", r"情境|情景|context"],
    "content_first": [r"content-first|內容優先", r"真實文案|文案規格|microcopy"],
    "color_system": [r"60-30-10|60/30/10", r"oklch|色彩系統|color roles"],
    "typography": [r"modular|字階|type scale|排版尺度", r"line-height|行高|行寬"],
    "spatial_grid": [r"8pt|8-point|空間網格|留白", r"宏留白|macro"],
    "adversarial_log": [r"頭腦互搏|對抗|critic|攻防|仲裁|trade-off"]
}


def audit_spec_content(text: str, strict: bool = False) -> dict:
    text_lower = text.lower()
    report = {
        "passed": True,
        "score": 100,
        "errors": [],
        "warnings": [],
        "checklist": {}
    }

    # 1. 檢查核心章節覆蓋度
    for section_name, patterns in CORE_SECTIONS.items():
        found = any(re.search(pat, text_lower) for pat in patterns)
        report["checklist"][section_name] = found
        if not found:
            msg = f"缺少核心章節或原則宣告: {section_name}"
            if strict:
                report["errors"].append(msg)
                report["score"] -= 15
            else:
                report["warnings"].append(msg)
                report["score"] -= 10

    # 2. 檢查 8 大互動狀態機完整度
    missing_states = []
    found_states = []
    for state in MANDATORY_STATES:
        # Match standalone words or markdown table cells
        pattern = rf"\b{state}\b"
        if re.search(pattern, text_lower):
            found_states.append(state)
        else:
            missing_states.append(state)

    report["checklist"]["states_found"] = found_states
    report["checklist"]["missing_states"] = missing_states

    if missing_states:
        msg = f"遺漏必備互動狀態機: {', '.join(missing_states)} (共 8 大狀態，需包含 Default, Hover, Focus-Visible, Active, Disabled, Loading, Error, Empty)"
        report["errors"].append(msg)
        report["score"] -= (len(missing_states) * 5)

    # 3. 檢查 60-30-10 配比宣告
    has_color_ratio = bool(re.search(r"60\s*[-/]\s*30\s*[-/]\s*10", text))
    report["checklist"]["has_60_30_10_budget"] = has_color_ratio
    if not has_color_ratio:
        report["warnings"].append("未明確宣告 60-30-10 色彩比例預算")
        report["score"] -= 10

    # 4. 檢查感知色彩空間 OKLCH 或語意角色
    has_oklch = "oklch" in text_lower
    report["checklist"]["uses_oklch"] = has_oklch
    if not has_oklch:
        report["warnings"].append("未採用 OKLCH 感知均勻色彩模型定義色票")
        report["score"] -= 5

    # 5. 檢查 8pt 空間網格規則
    has_8pt = bool(re.search(r"8pt|8px|\b8-point\b", text_lower))
    report["checklist"]["uses_8pt_grid"] = has_8pt
    if not has_8pt:
        report["warnings"].append("未明確採用 8pt / 4pt 空間系統約束佈局間距")
        report["score"] -= 5

    # 6. 檢查是否存在頭腦互搏 / Critic 攻防反思紀錄
    has_adversarial = bool(re.search(r"頭腦互搏|critic|對抗|質疑|trade-off|攻防", text_lower))
    report["checklist"]["has_adversarial_critique"] = has_adversarial
    if not has_adversarial:
        report["errors"].append("未記錄 Critic (審查質疑員) 之對抗審查或 Lead 之仲裁過程，缺乏頭腦互搏閉環")
        report["score"] -= 15

    # 判定最終通過與否
    report["score"] = max(0, report["score"])
    if report["errors"] or (strict and report["warnings"]):
        report["passed"] = False

    return report


def main():
    parser = argparse.ArgumentParser(description="Verify Human Design Spec compliance.")
    parser.add_argument("--spec", required=True, help="Path to markdown design spec file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Strict mode (warnings treated as failures)")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: Spec file not found at {spec_path}", file=sys.stderr)
        sys.exit(2)

    content = spec_path.read_text(encoding="utf-8")
    report = audit_spec_content(content, strict=args.strict)
    report["file"] = str(spec_path)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status_icon = "✅ PASS" if report["passed"] else "❌ FAIL"
        print(f"\n==================================================")
        print(f" 人本設計規格書校驗報告: {status_icon} (得分: {report['score']}/100)")
        print(f" 檔案: {spec_path.name}")
        print(f"==================================================")

        if report["errors"]:
            print("\n🚨 嚴重缺陷 (Errors):")
            for err in report["errors"]:
                print(f"  - ❌ {err}")

        if report["warnings"]:
            print("\n⚠️ 改善建議 (Warnings):")
            for warn in report["warnings"]:
                print(f"  - ⚠️ {warn}")

        print("\n📋 核心檢查指標摘要:")
        for k, v in report["checklist"].items():
            if isinstance(v, list):
                val_str = f"{len(v)} 項" if v else "無"
                print(f"  • {k}: {val_str}")
            else:
                icon = "✓" if v else "✗"
                print(f"  • {k}: {icon}")
        print(f"==================================================\n")

    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
