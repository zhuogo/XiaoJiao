# React / Python 重构（2026-10-26）

本文替代第一版规格中无后端、单文件入口及界面实现约定；IP 几何、素材和配色约束仍以原规范为准。

## 范围与体验
保留全部现有 22 表情、11 装饰、8 色板与几何资产。Python FastAPI 统一管理目录、合成、校验、随机及 SVG/PNG 导出。React + TypeScript + Vite 提供画布工作台：顶部品牌与导出入口，中央完整预览，侧边表情/装饰/配色选项卡，底部随机/撤销/重做/重置。小屏上下布局，所有容器 min-width:0，画布不溢出。使用小角暖白、墨色、砖红品牌体系；借鉴 Peeps 的画布优先与分类编辑，不引入其人物资产。当前只取得参考站公开 HTML，未完成实际交互观察，不宣称完整复刻。

## 数据与边界
正式素材目录只读。旧 index.html 内原创表情、装饰及色板迁到 backend/data/catalog.json，记录原始文件 SHA256；12 个基础表情仍从正式 SVG 提取。旧入口保留用户修改、标记为历史，不作为新运行依赖；验收脚本改用统一目录与合成服务。无账号、数据库或新 MCP 服务。

## 接口契约
GET /api/health -> {status,service}
GET /api/catalog -> {geometry,expressions:[{id,name,fragment,...}],decorations:[{id,name,group,bbox,bboxes?,covers_eyes,fragment}],palettes:[Palette],default_state:State}
State = {expression:string,decorations:string[],palette:Palette}
Palette = {id?:string,name?:string,body,corner,ink,accent,scene:string|null,blush,fluid,panel}; 色值必须六位十六进制。
POST /api/compose (State) -> image/svg+xml，必须使用统一坐标 translate(90 90)，有效 SVG 命名空间，完整阴影与背景。
POST /api/validate (State) -> {warnings:string[]}，检查保护区、眼部、安全区、重叠、对比度。无效 ID/重复挂点/格式返回 422。
POST /api/random -> State，生成合法组合。
POST /api/export?format=svg|png&size=240|512|1024 (State) -> 文件，PNG 宽度=size，高度按 560/780 比例。
前端相对 /api 请求，Vite 代理到后端 127.0.0.1:4760；可通过环境配置覆盖。预览请求取消过期结果，所有失败有重试与文字反馈。导出禁止空白或过期结果。本地保存版本化 State 和收藏预设；损坏缓存回退默认。OpenAPI 由 FastAPI 生成并落盘供验收。

## 完成条件
目录数量与旧资产一致；所有表情和装饰可生成合法 XML，无 ns0 残留或未解析令牌；默认几何与原 renderer 一致；测试错误输入、配色透明背景、PNG尺寸和随机合法性；TypeScript 检查与构建通过；实际 HTTP 验证前端代理、目录、预览及导出。用户执行视觉验收。
