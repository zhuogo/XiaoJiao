# Render sheets from the shared backend catalog.
import json
import re
import sys
from pathlib import Path

import resvg_py

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def die(code: int, msg: str):
    print(msg, file=sys.stderr)
    sys.exit(code)


def parse_index():
    from backend.app import CATALOG
    return CATALOG['expressions'], CATALOG['geometry'], CATALOG['decorations'], CATALOG['palettes']


from backend.renderer import compose


def sheet(cells, cols, cell_w, cell_h, out_path):
    pitch_x, pitch_y = cell_w + 24, cell_h + 24
    rows = (len(cells) + cols - 1) // cols
    W, H = cols * pitch_x + 24, rows * pitch_y + 24
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    parts.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
    for i, content in enumerate(cells):
        cx, cy = 24 + (i % cols) * pitch_x, 24 + (i // cols) * pitch_y
        parts.append(f'<rect x="{cx}" y="{cy}" width="{cell_w}" height="{cell_h}" rx="14" fill="#C8CAC7"/>')
        parts.append(f'<svg x="{cx}" y="{cy}" width="{cell_w}" height="{cell_h}" viewBox="0 0 780 560" preserveAspectRatio="xMidYMid meet">{content.split(">", 1)[1].rsplit("<", 1)[0]}</svg>')
    parts.append("</svg>")
    svg = "".join(parts)
    if "{{" in svg:
        die(2, "门禁失败：合成结果存在未解析令牌\n" + svg[:500])
    png = resvg_py.svg_to_bytes(svg_string=svg, width=W, height=H)
    out_path.write_bytes(bytes(png))


def main():
    if len(sys.argv) != 2:
        die(1, "用法：python scripts/render_sheet.py <输出目录>")
    out = ROOT / sys.argv[1]
    out.mkdir(parents=True, exist_ok=True)
    expressions, geometry, decorations, colorways = parse_index()

    # 表情接触表：22+ 个表情，原味
    orig = colorways[0]
    expr_cells = [compose(expressions, geometry, decorations, orig, e["id"], []) for e in expressions]
    sheet(expr_cells, 4, 358, 257, out / "expressions.png")

    # 装饰接触表：基板 + 每件装饰，原味 + 标准表情
    deco_cells = [compose(expressions, geometry, decorations, orig, "expr-01-standard", [])]
    deco_cells += [compose(expressions, geometry, decorations, orig, "expr-01-standard", [d["id"]]) for d in decorations]
    sheet(deco_cells, 4, 358, 257, out / "decorations.png")

    # 色板接触表：8 套 ×（眨眼 + 毛线帽 + 围巾）
    pal_cells = [compose(expressions, geometry, decorations, p, "expr-03-wink", ["deco-hat-beanie", "deco-scarf"]) for p in colorways]
    sheet(pal_cells, 4, 358, 257, out / "palettes.png")

    # 主视觉：四组代表组合，全尺寸
    combos = [
        (orig, "expr-01-standard", []),
        (next(c for c in colorways if c["id"] == "nightline"), "expr-03-wink", ["deco-hat-beanie", "deco-scarf"]),
        (next(c for c in colorways if c["id"] == "sakura"), "expr-03-wink", ["deco-bow"]),
        (next(c for c in colorways if c["id"] == "matcha"), "expr-10-cool", ["deco-hat-cap"]),
    ]
    hero_cells = [compose(expressions, geometry, decorations, p, e, d) for p, e, d in combos]
    sheet(hero_cells, 2, 780, 560, out / "hero.png")

    (out / "manifest.json").write_text(
        json.dumps({"expressions": [e["id"] for e in expressions],
                    "decorations": [d["id"] for d in decorations]}, ensure_ascii=False),
        encoding="utf-8")
    print(f"OK: {len(expressions)} expressions, {len(decorations)} decorations, {len(colorways)} palettes -> {out}")
    for f in ["expressions.png", "decorations.png", "palettes.png", "hero.png"]:
        print((out / f).as_posix())


if __name__ == "__main__":
    main()
