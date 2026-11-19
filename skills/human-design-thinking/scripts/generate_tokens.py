#!/usr/bin/env python3
"""
generate_tokens.py - W3C DTCG 2025.10 & OKLCH 人本設計 Token 生成器

依據主品牌種子色與模組化比例，自動生成三層架構的 Design Tokens：
1. Primitive Tokens (色相色階、8pt 空間、字階)
2. Semantic Tokens (M3 語意角色：Surface, On-Surface, Primary, Secondary, Outline, Feedback)
3. Component Tokens (Button, Input, Card 基礎狀態映射)

輸出支援：
- W3C DTCG JSON 規範
- CSS 變數（包含淺色與深色模式）

使用方式：
    python3 generate_tokens.py --brand "#2563EB" --scale 1.25 --format css
    python3 generate_tokens.py --brand "#2563EB" --format json --output tokens.json
"""

import argparse
import json
import math
import re
import sys


def hex_to_rgb(hex_code: str):
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    if len(hex_code) != 6:
        raise ValueError(f"Invalid Hex color: {hex_code}")
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0
    return r, g, b


def srgb_to_oklch(r: float, g: float, b: float):
    # sRGB to linear sRGB
    def to_linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    lr = to_linear(r)
    lg = to_linear(g)
    lb = to_linear(b)

    # linear RGB to LMS
    l = 0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb
    m = 0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb
    s = 0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb

    l_ = math.pow(l, 1 / 3) if l > 0 else 0
    m_ = math.pow(m, 1 / 3) if m > 0 else 0
    s_ = math.pow(s, 1 / 3) if s > 0 else 0

    # LMS to OKLab
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_val = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    # OKLab to OKLCH
    C = math.sqrt(a * a + b_val * b_val)
    H = math.degrees(math.atan2(b_val, a)) % 360

    return round(L, 3), round(C, 3), round(H, 1)


def generate_tonal_palette(hue: float, chroma: float):
    """依據 Hue 與 Chroma 生成 50~950 均勻感知色階"""
    levels = {
        "50": (0.97, min(chroma * 0.15, 0.03)),
        "100": (0.93, min(chroma * 0.35, 0.06)),
        "200": (0.86, min(chroma * 0.65, 0.11)),
        "300": (0.76, min(chroma * 0.85, 0.16)),
        "400": (0.66, chroma),
        "500": (0.56, chroma),
        "600": (0.47, chroma),
        "700": (0.38, chroma * 0.9),
        "800": (0.28, chroma * 0.8),
        "900": (0.20, chroma * 0.6),
        "950": (0.13, chroma * 0.4),
    }
    palette = {}
    for stop, (L, C) in levels.items():
        palette[stop] = f"oklch({round(L, 3)} {round(C, 3)} {hue})"
    return palette


def generate_type_scale(ratio: float = 1.25, base: int = 16):
    steps = {
        "caption": round(base / ratio),
        "body": base,
        "h3": round(base * (ratio ** 1)),
        "h2": round(base * (ratio ** 2)),
        "h1": round(base * (ratio ** 3)),
        "display": round(base * (ratio ** 4)),
    }
    line_heights = {
        "caption": 1.4,
        "body": 1.5,
        "h3": 1.3,
        "h2": 1.25,
        "h1": 1.2,
        "display": 1.15,
    }
    return steps, line_heights


SPACING_SCALE = {
    "space-0.5": "2px",
    "space-1": "4px",
    "space-2": "8px",
    "space-3": "12px",
    "space-4": "16px",
    "space-6": "24px",
    "space-8": "32px",
    "space-12": "48px",
    "space-16": "64px",
    "space-24": "96px",
}


def build_tokens(brand_hex: str, scale_ratio: float = 1.25):
    r, g, b = hex_to_rgb(brand_hex)
    bL, bC, bH = srgb_to_oklch(r, g, b)

    primary_palette = generate_tonal_palette(bH, bC)
    neutral_palette = generate_tonal_palette(bH, 0.01)
    error_palette = generate_tonal_palette(28.0, 0.22)
    success_palette = generate_tonal_palette(145.0, 0.18)

    type_sizes, type_leadings = generate_type_scale(scale_ratio)

    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/2025.10/",
        "primitive": {
            "color": {
                "primary": primary_palette,
                "neutral": neutral_palette,
                "error": error_palette,
                "success": success_palette,
            },
            "space": SPACING_SCALE,
            "typography": {
                "scale_ratio": scale_ratio,
                "size": {k: f"{v}px" for k, v in type_sizes.items()},
                "line_height": type_leadings,
            }
        },
        "semantic": {
            "light": {
                "color.surface": neutral_palette["50"],
                "color.surface.container": neutral_palette["100"],
                "color.surface.elevated": neutral_palette["200"],
                "color.text.primary": neutral_palette["950"],
                "color.text.secondary": neutral_palette["700"],
                "color.text.tertiary": neutral_palette["500"],
                "color.action.primary": primary_palette["500"],
                "color.action.primary.hover": primary_palette["600"],
                "color.action.on-primary": "oklch(0.99 0 0)",
                "color.action.secondary": neutral_palette["200"],
                "color.border.subtle": neutral_palette["200"],
                "color.border.default": neutral_palette["300"],
                "color.feedback.error": error_palette["500"],
                "color.feedback.success": success_palette["500"],
            },
            "dark": {
                "color.surface": neutral_palette["950"],
                "color.surface.container": neutral_palette["900"],
                "color.surface.elevated": neutral_palette["800"],
                "color.text.primary": neutral_palette["50"],
                "color.text.secondary": neutral_palette["300"],
                "color.text.tertiary": neutral_palette["400"],
                "color.action.primary": primary_palette["400"],
                "color.action.primary.hover": primary_palette["300"],
                "color.action.on-primary": neutral_palette["950"],
                "color.action.secondary": neutral_palette["800"],
                "color.border.subtle": neutral_palette["800"],
                "color.border.default": neutral_palette["700"],
                "color.feedback.error": error_palette["400"],
                "color.feedback.success": success_palette["400"],
            }
        },
        "component": {
            "button": {
                "hit_target_min": "40px",
                "padding_x": "{space.4}",
                "padding_y": "{space.2}",
                "radius": "8px",
                "focus_ring": "2px solid {color.action.primary}",
                "focus_offset": "2px",
            }
        }
    }
    return tokens


def tokens_to_css(tokens: dict) -> str:
    lines = [
        "/* Generated by human-design-thinking token engine (OKLCH & 8pt Grid) */",
        ":root {"
    ]

    # Spacing
    for k, v in tokens["primitive"]["space"].items():
        lines.append(f"  --{k}: {v};")

    # Typography
    for k, v in tokens["primitive"]["typography"]["size"].items():
        lines.append(f"  --font-size-{k}: {v};")
    for k, v in tokens["primitive"]["typography"]["line_height"].items():
        lines.append(f"  --line-height-{k}: {v};")

    # Light Semantic Colors
    lines.append("\n  /* Semantic Color Roles (Light Mode) */")
    for k, v in tokens["semantic"]["light"].items():
        css_var = "--" + k.replace(".", "-")
        lines.append(f"  {css_var}: {v};")

    lines.append("}\n")

    # Dark Mode
    lines.append("@media (prefers-color-scheme: dark) {")
    lines.append("  :root {")
    lines.append("    /* Semantic Color Roles (Dark Mode / Tonal Elevation) */")
    for k, v in tokens["semantic"]["dark"].items():
        css_var = "--" + k.replace(".", "-")
        lines.append(f"    {css_var}: {v};")
    lines.append("  }")
    lines.append("}\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate W3C & CSS Design Tokens with OKLCH.")
    parser.add_argument("--brand", default="#2563EB", help="Seed brand color in Hex (e.g. #2563EB)")
    parser.add_argument("--scale", type=float, default=1.25, help="Modular Type Scale ratio (e.g. 1.25 for Major Third)")
    parser.add_argument("--format", choices=["json", "css"], default="json", help="Output format")
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    tokens = build_tokens(args.brand, args.scale)

    if args.format == "css":
        output_text = tokens_to_css(tokens)
    else:
        output_text = json.dumps(tokens, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
        print(f"Tokens written to {args.output}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
