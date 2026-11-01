# Go 家族 · 小角品牌延展

当前修正版的基准：小角身体、双眼、切角的几何保持一致，产品特征通过配色和外围结构表达。

- DraftGo：保留既有轨道与橙色模块；当前彩色版本增加淡阴影，原文件在完整包的 `DraftGo-original/` 中。
- RouterGo：沿用原版暖红、浅色双眼、分流线路、箭头和连接端点，只增加淡阴影。
- SelfGo：纸白小角、松绿切角，前后错落的画布位于身体后方。双眼保持原始眼距。
- BenchGo：使用小角原配色，暖米白身体、砖红切角与深墨双眼，展示与应用图标使用浅暖灰底 `#E8EAE5`。保留顶部活动标签、分隔线与光标，没有左右代码括号。首页默认展示原配色，并保留此前 16 款完整配色供回看，共 17 款。身体、双眼与切角保持标准几何；顶部细节避开双眼与切角。

本轮 RouterGo 线路与眼睛颜色、SelfGo 叠层与底色的修改未采用，两者已恢复修改前的造型与配色。按最新要求，四款产品的彩色标志、应用图标统一增加一层淡阴影，BenchGo 配色研究也同步处理。单色、反白、favicon 与 16–64px PNG 保持平面版本，以保留小尺寸清晰度。

阴影位于整组图形下方、应用底板上方：颜色 `#1F2925`，不透明度 10%，向下偏移 8，模糊标准差 10（840 单位画布）。SVG、PNG 与下载包一致。修改前的资产和工程脚本保存在 `logos/go/history/before-line-layer-lightening/`。

## BenchGo 当前版本

2026-10-31 当前默认配色为小角原配色（`original`）：身体 `#F3EBDF`、切角与活动标签 `#D44A36`、双眼与字标 `#222222`。展示与应用图标底色由 `#C8CAC7` 调浅为 `#E8EAE5`；身体、双眼与切角仍对应 `小角IP/geometry.json`。光标沿用砖红，次级标签与分隔线为暖灰 `#B6B1A7`，保留编辑器细节。

`benchgo-final.zip` 是当前原配色的交付包，包含彩色标志、应用图标、单色、反白、favicon、7 种尺寸的 PNG、配色清单与使用说明。`benchgo-identity.zip` 包含原配色与此前 16 款配色研究，共 17 款。切换网页预览不会改变当前默认版本。

## 文件用途

| 后缀 | 用途 |
| --- | --- |
| `-mark.svg` / `.png` | 透明背景彩色标志 |
| `-app.svg` / `.png` | 应用图标，PNG 为 1024 × 1024 |
| `-mono.svg` / `.png` | 黑色单色版，眼睛为透明负形 |
| `-reverse.svg` / `.png` | 白色反白版，用于深色背景 |
| `-icon-16/32/48/64.png` | 网站及小尺寸使用 |
| `-icon-180/192/512.png` | 移动设备及 Web 应用使用 |
| `-favicon.svg` / `.ico` | 网站 favicon，ICO 含 16、32、48、64 像素 |

SVG 可自由缩放。请等比缩放整图，不要单独挪动或拉伸双眼、身体、切角。16 像素主要保留小角和品牌色，外围细节在 32 像素以上更清晰。BenchGo 的 favicon 与 16–64 像素 PNG 使用简化版：保留标准身体、双眼与切角，去掉顶部标签与光标。

身体为 600 × 380，圆角 R95；双眼各 90 × 130、R45，中心分别为 (168,190)、(306,190)；切角连接 (410,380) 与 (600,190)。

`palette.json` 包含品牌色。`go-family-board.png` 是四款横向对比图。

BenchGo 配色展区位于首页 `#benchgo-palettes`，17 款均直接展示。支持品牌标志 / 应用图标切换、统一底色 / 配套底色比较、点选同步上方大图、单款 SVG / PNG 下载和整套下载。所有配色的单色与反白版本共用。

各配色文件前缀固定。`benchgo-mark/app/favicon` 与 `benchgo-icon-*` 是小角原配色的正式导出，与对应的 `benchgo-original-*` 文件一致。此前的 `benchgo-sky-*` 晴空蓝造型与配色保留，彩色大图同步增加淡阴影。

| 配色 | 文件前缀 | 身体 / 切角 / 光标 |
| --- | --- | --- |
| 小角原配色（当前方案） | `benchgo-original-` | `#F3EBDF` / `#D44A36` / `#D44A36` |
| 深海蓝 | `benchgo-ice-` | `#30496B` / `#8ACEDA` / `#EAC793` |
| 牛仔蓝 | `benchgo-denim-` | `#426F9C` / `#F0C884` / `#A8D4D8` |
| 钴蓝 | `benchgo-cobalt-` | `#3856A6` / `#A0BFE8` / `#F1C880` |
| 鸢尾蓝 | `benchgo-iris-` | `#716BAD` / `#C4DCC8` / `#ECCAAC` |
| 孔雀青 | `benchgo-teal-` | `#347D83` / `#BCDCA9` / `#E9C786` |
| 松石绿 | `benchgo-jade-` | `#478774` / `#E5D08B` / `#BDE1C1` |
| 橄榄绿 | `benchgo-olive-` | `#727E4E` / `#E7CB7F` / `#BBCFA5` |
| 石墨黑 | `benchgo-mint-` | `#26363B` / `#78CBA8` / `#E3B96F` |
| 陶土橙 | `benchgo-terracotta-` | `#BC7958` / `#E8CAA0` / `#A7C4BC` |
| 莓果紫 | `benchgo-berry-` | `#825879` / `#E9B496` / `#CFBBDD` |
| 奶油杏 | `benchgo-apricot-` | `#F2C8A9` / `#99B9B0` / `#77998D` |
| 柔雾紫 | `benchgo-lilac-` | `#B8AFD8` / `#F0CCA9` / `#F8E8CA` |
| 晴空蓝 | `benchgo-sky-` | `#89B9D8` / `#F3D89B` / `#FFF6E4` |
| 鼠尾草绿 | `benchgo-sage-` | `#ABC5B1` / `#EDDCAD` / `#E0BA8D` |
| 雾蓝灰 | `benchgo-mist-` | `#829AA8` / `#C5DDE0` / `#F4D49F` |
| 暖砂白 | `benchgo-sand-` | `#E5DACA` / `#8B9EAD` / `#B98455` |

`benchgo-palettes.json` 包含全部配色与文件前缀，仅小角原配色的 `default` 为 `true`。`benchgo-palette-board.png` 使用统一底色展示全部 17 款，并标注当前方案。`benchgo-comparison.png` 展示去掉左右括号前后的设计。BenchGo 全配色图标包包含 17 款配色的标志、应用图标、favicon、多尺寸 PNG 及共用的单色、反白版本。

BenchGo 的彩色方案均采用深色双眼。原配色使用深墨 `#222222`；此前 16 款使用与主色协调的深色双眼，已替换此前 11 款的白色、奶白色眼睛。双眼尺寸、位置不变。`benchgo-palettes.json` 的 `paper` 字段记录双眼色。单色与反白版沿用透明负形。

历史版本位于网站资产目录 `logos/go/history/`：`benchgo-v2/` 为紫色停靠线版本，`benchgo-editor-mint/` 为带左右括号的薄荷色编辑器版本，`benchgo-accent-palettes/` 为深色主调的配色研究，`benchgo-body-palettes/` 为首次推荐深海蓝时的导出，`benchgo-soft-palettes/` 为柔和配色阶段的完整导出，`benchgo-light-eyes/` 为改深色眼睛前的 16 款配色。

此前晴空蓝交付包及说明保存在 `logos/go/history/benchgo-sky-final/`。

工程源文件：`scripts/go_identity_geometry.py`。导出：`python scripts/build_go_identities.py`。正式小角素材库未改动。
