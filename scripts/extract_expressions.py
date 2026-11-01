#!/usr/bin/env python3
"""从小角IP素材库提取表情图层，供生成器使用。

用法：
  python scripts/extract_expressions.py                # 校验并打印 JSON
  python scripts/extract_expressions.py --inject archive/legacy-generator/index.html
                                                       # 仅维护历史生成器的
                                                       # <!-- DATA:EXPRESSIONS --> /
                                                       # <!-- DATA:GEOMETRY --> 标记之间

原理：12 个贴纸 SVG 结构统一（见 Design/02-拆解体系/图层拆解规范.md），
基板四层（软阴影/接触阴影/身体/切角）逐字节一致；剥离基板后剩下的
<g> 子组即为表情图层（身体坐标系，无需再换算）。
校验：基板前缀 + 表情图层 + 后缀 与源文件全文比对，必须完全一致。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "小角IP" / "04-表情包" / "SVG"

NAMES = {
    "01": ("standard", "标准"),
    "02": ("happy", "开心"),
    "03": ("wink", "眨眼"),
    "04": ("laugh", "大笑"),
    "05": ("cry", "哭"),
    "06": ("angry", "生气"),
    "07": ("wow", "惊讶"),
    "08": ("love", "爱心眼"),
    "09": ("sleepy", "困"),
    "10": ("cool", "酷"),
    "11": ("dizzy", "晕"),
    "12": ("cheer", "欢呼"),
}

# 表情图层起止标记：贴纸 body 内，基板层结束于切角 path，其后皆为表情子组
BASE_END = re.compile(r'<ns0:path d="M410 380H505A95 95 0 0 0 600 285V190Z" fill="#D44A36" />')
TAIL = "</ns0:g></ns0:svg>"


def extract(path: Path):
    text = path.read_text(encoding="utf-8")
    m = BASE_END.search(text)
    if not m:
        raise ValueError(f"{path.name}: 找不到切角基板标记")
    head = text[: m.end()]  # xml 声明 + svg 开标签 + defs + 基板四层
    tail_at = text.rfind(TAIL)
    if tail_at < 0:
        raise ValueError(f"{path.name}: 找不到收尾标记")
    expr = text[m.end() : tail_at]  # 表情图层（原样保留缩放补偿变换）
    # 校验 1：重合成与源文件逐字节一致
    if head + expr + TAIL != text:
        raise ValueError(f"{path.name}: 重合成校验失败")
    no = path.name[8:10]
    en, zh = NAMES[no]
    # 供生成器内联使用：去掉 ns0: 前缀（浏览器内嵌于 <svg> 默认命名空间）
    clean = expr.replace("ns0:", "").replace(":ns0", "")
    return {
        "id": f"expr-{no}-{en}",
        "no": int(no),
        "name": zh,
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
        "fragment": clean,
    }


def main():
    items = []
    bases = set()
    for svg in sorted(SRC_DIR.glob("sticker-*.svg")):
        text = svg.read_text(encoding="utf-8")
        m = BASE_END.search(text)
        bases.add(text[: m.end()])
        items.append(extract(svg))
    # 校验 2：12 个贴纸的基板前缀完全一致（「同一只小角」的判据）
    if len(bases) != 1:
        raise ValueError(f"基板前缀不一致：{len(bases)} 种")
    data = {"generator": "extract_expressions.py", "expressions": items}
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    geometry = json.loads((ROOT / "小角IP" / "geometry.json").read_text(encoding="utf-8"))
    geometry_payload = json.dumps(geometry, ensure_ascii=False, indent=2)

    if "--inject" in sys.argv:
        target = ROOT / sys.argv[sys.argv.index("--inject") + 1]
        html = target.read_text(encoding="utf-8")

        def inject(html, marker, statement):
            begin, end = f"<!-- DATA:{marker} BEGIN -->", f"<!-- DATA:{marker} END -->"
            return re.sub(rf"{begin}.*?{end}", begin + "\n" + statement + "\n" + end, html, flags=re.S)

        html = inject(html, "EXPRESSIONS", "window.EXPRESSIONS = " + payload)
        html = inject(html, "GEOMETRY", "window.GEOMETRY = " + geometry_payload)
        target.write_text(html, encoding="utf-8")
        print(f"已注入 {target.name}：{len(items)} 个表情 + 几何参数")
    else:
        print(payload)


if __name__ == "__main__":
    main()
