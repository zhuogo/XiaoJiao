# 小角 · 图标展厅

轻量单页：四个产品、12 款形态案例、完整资产索引。没有账户、项目管理、AI 配置或套装流程。所有现有资产及历史方案保留。

## 启动

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev -- --host 127.0.0.1
```

访问 http://127.0.0.1:5173/ 。页面完全使用本地静态资产，不需要启动后端。

## 操作

- 点击首屏产品图标，进入同页展台；切换四个产品、品牌标志 / 应用图标 / 单色，直接下载 SVG / PNG。
- BenchGo 支持全部 17 套配色；单色模式不应用配色。
- 点击形态案例，查看大图、对照小角基准、切换形式及下载；Escape 关闭并返回触发按钮。
- 资产索引包含基准、21 个当前表情、装饰、配色、历史方案与展板，支持分类、搜索及下载。
- “展板”分类收录四产品完整 VI 资产包，每品牌 85 个文件：六页规范、独立标识、平台图标、开发变量、辅助视觉与可编辑模板。支持完整 ZIP、规范 PDF、单独展板文件下载；页脚可下载四品牌合集。
- 完整资产包保留源文件和历史资产，但不含私有项目数据库。
- 可暂停动态；系统减少动态偏好自动生效。

## 构建与验证

```powershell
python scripts/build_vi_boards.py
python scripts/build_vi_packages.py
python scripts/build_distribution.py
python scripts/build_asset_library.py
python -m unittest backend.test_app -v
cd frontend
npm.cmd run typecheck
npm.cmd run build
npm.cmd run preview -- --host 127.0.0.1 --port 4173
```

生产预览运行后执行 `python scripts/check_gallery.py`；验证交互、资源、下载和移动端布局边界，不进行视觉截图。另用 `python scripts/check_vi_packages.py` 检查 VI 内容矩阵、SVG 引用、透明性、PDF 页数、图标安全区与完整校验和（需测试依赖 pypdf）。

`frontend/dist` 可直接部署为静态站。项目子路径通过 `VITE_BASE_PATH=/XiaoJiao/` 构建；所有资源与下载统一使用该路径。GitHub Pages 与版本化资产接口见根 `README.md`。更新原始资产后重新运行资产构建脚本与前端构建。

## 文件边界

- `frontend/src/main.tsx` / `gallery.css`：唯一页面及样式。
- `frontend/src/data`：案例与 BenchGo 配色元数据。
- `frontend/public/logos`：现有品牌资产，全部保留。
- `frontend/public/assets`：派生预览、索引与完整下载包。
- `小角IP`：正式源素材，只读。
- `backend/data/catalog.json`：组合模块源数据；`studio.sqlite3` 是保留的用户数据，不再被页面或 API 使用。
- 原根 `index.html` 已原样移至 `archive/legacy-generator/index.html`，用户修改完整保留，不参与构建。
- `backend/app.py`：维护用核心渲染 API，无 `/api/studio/*`。

设计真源：[轻量单页](Design/06-生成器设计/轻量单页.md)、[四产品 VI 展板](Design/07-品牌延展/四产品VI展板.md)、[VI 资产交付规范](Design/07-品牌延展/VI资产交付规范.md)。VI 为 RGB 展示稿，PDF 使用高清栅格嵌入；新增净空、字标组合及字体层级为使用建议，界面与物料为应用示意。
