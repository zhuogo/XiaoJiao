# BenchGo · 晴空蓝定稿

定稿日期：2026-10-31。BenchGo 是本地 AI 开发工作台与全天候个人助手，域名 benchgo.cn。

## 正式配色

| 用途 | 颜色 |
| --- | --- |
| 身体主色 · 晴空蓝 | `#89B9D8` |
| 切角、活动标签 · 奶油黄 | `#F3D89B` |
| 双眼、字标 · 深蓝 | `#29465C` |
| 光标 · 奶白 | `#FFF6E4` |
| 次级标签、分隔线 | `#6094B5` |
| 应用图标背景 | `#F6F0E4` |
| 展示背景 | `#EDF3F6` |

保留顶部编辑器标签、分隔线与光标；没有左右箭头或代码括号。彩色版本使用深蓝双眼。

## 文件使用

- `benchgo-mark.svg` / `.png`：透明背景标志。
- `benchgo-app.svg` / `.png`：应用图标，PNG 为 1024 × 1024。
- `benchgo-mono.svg` / `.png`：深色单色版，双眼为透明负形。
- `benchgo-reverse.svg` / `.png`：白色单色版，供深色背景使用，双眼为透明负形。
- `benchgo-favicon.svg` / `.png` / `.ico`：网站 favicon，ICO 包含 16、32、48、64px。
- `benchgo-icon-16/32/48/64/180/192/512.png`：各尺寸应用资源。
- `palette.json`：正式配色清单，`paper` 字段为双眼色。

favicon 与 16–64px 图标去除顶部细节，以保持小尺寸清晰度。正式导出与配色研究中的 `benchgo-sky-*` 对应文件一致。

## 小角基准

身体 600 × 380、R95；双眼各 90 × 130、R45，中心为 (168,190)、(306,190)；切角连接 (410,380) 与 (600,190)。标志画布为 840 × 760，本体位于 translate(120 190)。请等比缩放整图，不要单独拉伸、旋转或移动身体、眼睛、切角。

工程真源为 `scripts/go_identity_geometry.py`，默认配色 ID 为 `sky`；执行 `python scripts/build_go_identities.py` 可重新导出正式资源。
