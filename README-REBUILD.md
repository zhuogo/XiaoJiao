# 小角核心渲染器维护

当前产品是轻量静态单页，启动、操作、构建与验收见 [README-STUDIO.md](README-STUDIO.md)。页面不依赖 Python 服务。

## 保留的核心能力

- `backend/app.py`：目录、组合、校验、随机状态、SVG / PNG 导出。
- `backend/renderer.py`：统一基板几何与阴影渲染。
- `backend/models.py`：组合状态与色板校验。
- `backend/scene_assets.py`：场景道具。
- `backend/data/catalog.json`：表情、装饰、色板源数据。
- `scripts/extract_expressions.py`：从正式素材提取基础表情。
- `scripts/build_asset_library.py`：生成单页资产索引、预览及完整下载包。
- `scripts/render_sheet.py`：通过共享渲染器导出验收图。

工作台、AI 分析、项目管理及 `/api/studio/*` 已移除。`backend/data/studio.sqlite3` 作为用户既有数据保留，不再读写，也不放入公开资产包。

## 可选维护服务

```powershell
python -m pip install fastapi uvicorn pydantic resvg-py httpx
python -m uvicorn backend.app:app --host 127.0.0.1 --port 4760
```

- API 文档：http://127.0.0.1:4760/docs
- OpenAPI 快照：`backend/openapi.json`
- 核心测试：`python -m unittest backend.test_app -v`
- 无新增 MCP 服务或配置。

## 资产保护

`小角IP/` 为正式素材与几何真源，只读。`frontend/public/logos/` 的当前及历史方案全部保留。原根 `index.html` 包含用户已有修改，已原样归档到 `archive/legacy-generator/index.html`，不是当前运行入口；提取脚本的 `--inject` 仅服务该历史文件。

当前设计真源：[轻量单页](Design/06-生成器设计/轻量单页.md)。
