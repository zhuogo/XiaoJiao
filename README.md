# 小角 · 卓越构建

DraftGo、RouterGo、SelfGo、BenchGo 的图标展厅与完整数字产品 VI 资产库。

- 展厅：https://zhuogo.github.io/XiaoJiao/
- 静态资产索引：https://zhuogo.github.io/XiaoJiao/vi-manifest.json
- 版本下载：https://github.com/zhuogo/XiaoJiao/releases
- 当前版本：`vi-v1.0.0`。公开访问不代表开放品牌授权。

## 本地运行

```sh
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

访问 http://127.0.0.1:5173/ 。静态页面不需要 Python 后端，不包含项目管理、登录或数据库访问。

## 给其他项目取用

稳定静态入口：

```text
vi-manifest.json
vi/draftgo/logo.svg
vi/routergo/horizontal.svg
vi/selfgo/icon-512.png
vi/benchgo/favicon.svg
vi/benchgo/tokens.json
vi/benchgo/variables.css
logos/vi/go-family-vi-assets.zip
```

示例（把 `ASSET_SITE` 替换为实际部署地址，末尾保留 `/`）：

```js
const manifestURL = new URL('vi-manifest.json', ASSET_SITE)
const manifest = await fetch(manifestURL).then(r => {
  if (!r.ok) throw new Error(`Asset index: ${r.status}`)
  return r.json()
})
const logo = manifest.products.benchgo.files['logo.svg']
const logoURL = new URL(logo.path, manifestURL).href
```

- **Pages** 适合展厅、图片、JSON 与 CSS 的静态分发；支持根目录和项目子路径。
- **Release** 适合完整 ZIP。推送 `vi-v*` tag 后自动校验并发布四产品包、合集、规范与校验和。
- **Raw** 可直接取仓库文件；生产依赖固定 tag 或 commit，而非 `main`：
  `https://raw.githubusercontent.com/zhuogo/XiaoJiao/<commit>/frontend/public/vi/benchgo/logo.svg`
- 所有者已授权公开此仓库。取用这些公开资产不需要 GitHub token；不要把任何私有仓库的 token 嵌入前端。
- `vi-manifest.json` 的文件路径相对于清单 URL，带字节数和 SHA256。固定版本建议在构建时下载、校验并纳入目标项目，不把第三方网络作为运行时硬依赖。
- 公开访问不等于开放授权，见 [品牌使用说明](BRAND-USAGE.md)。

## GitHub 配置

- `ci.yml`：push/PR 时检查交付包、TypeScript 和 `/XiaoJiao/` 子路径构建。
- `pages.yml`：main 推送或手动触发部署；仓库 Settings → Pages 使用 GitHub Actions。工作流本身不会改变仓库可见性。
- `release.yml`：推送版本 tag 时发布已有交付文件。私有仓库的 Release 仍需认证。

Pages 只上传 `frontend/dist`，不包含后端、数据库或历史生成器源码。仓库与静态资产库保留已确认的历史设计；首次公开时按所有者要求将当前状态作为唯一根提交，不保留旧的可达 Git 提交历史。

## 目录与清理边界

| 目录 | 用途 |
| --- | --- |
| `frontend/src` | 当前唯一 React 单页及样式 |
| `frontend/public/vi` | 供其他项目直接取用的稳定资产入口 |
| `frontend/public/logos` | 当前品牌、完整 VI 与历史设计资产 |
| `frontend/public/assets` | 通用资产索引与派生预览 |
| `小角IP` | 正式素材真源，只读 |
| `scripts` | 有实际用途的资产构建、维护与验证脚本 |
| `backend` | 生成器复用的核心渲染能力，不部署到 Pages |
| `archive/legacy-generator` | 原样保存用户修改的旧生成器，不参与构建 |
| `Design` | 设计规格与历史决策 |

不提交 `node_modules`、`dist`、`out`、环境文件、日志、字节码及用户 SQLite 数据库。历史图标和可复现它们的脚本不是垃圾，不按“未被首页引用”删除。

## 构建与验证

```sh
# 已提交的交付文件可跨平台直接校验，无需安装字体或 Python 第三方依赖。
python scripts/check_distribution.py
cd frontend
npm ci
npm run typecheck
npm run build
```

重新生成 VI 时在具备合法 Segoe UI / 微软雅黑字体的 Windows 环境运行：

```sh
python scripts/build_vi_boards.py
python scripts/build_vi_packages.py
python scripts/build_distribution.py
python scripts/build_asset_library.py
```

详细交互验收、Python 依赖和完整交付内容见 [单页维护说明](README-STUDIO.md)、[核心渲染器维护](README-REBUILD.md)、[GitHub 分发设计](Design/06-生成器设计/GitHub发布与资产分发.md)。
