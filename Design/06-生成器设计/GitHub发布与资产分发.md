# GitHub 发布与资产分发

## 当前事实与公开边界

本地 origin 的旧地址 draftgo/XiaoJiao 重定向到 zhuogo/XiaoJiao。

用户明确选择：公开现有仓库，清除先前可达提交历史，以当前完整版本作为唯一根提交。执行顺序为敏感文件检查与验证 → 创建无父提交 → 使用 force-with-lease 替换 main → 确认仅一个可达提交 → 公开仓库 → 启用 Pages 与 Release。正式/历史图标文件保留，删除的是 Git 提交历史，不是资产。

旧克隆、fork、外部缓存与 GitHub 未回收的不可达对象不保证立即消失。数据库、环境文件及临时日志不进入提交或部署。

## 服务拆分

- GitHub Pages：静态展厅与可直接引用的图标/JSON/CSS，不运行 Python/FastAPI，不保存用户数据。
- GitHub Releases：按 `vi-v*` tag 分发四品牌独立 ZIP、合集、清单及校验和。只有公开仓库的 Release 可匿名访问。
- Raw：可直接读取公开仓库中 `frontend/public/vi/` 文件，正式项目固定 tag 或完整 commit SHA，不依赖 main。
- 私有仓库不能将 GitHub token 放进浏览器；在 CI/服务器端认证下载或转到经授权的公开资产仓库。

## 稳定接口

`vi-manifest.json` 位于静态站根部，包含 schemaVersion、资产版本、产品、角色、署语、文件相对路径、SHA256、字节数及完整包地址。
`vi/<product>/` 提供独立彩色/单色/反白标志、横向组合、应用图标、favicon、JSON/CSS 变量。数据从已校验的完整 VI 包派生，避免重新绘制。
路径相对 manifest URL 解析，适配根站点与 GitHub Pages 的 `/XiaoJiao/` 项目子路径。只有静态资源，无新 API 或 MCP。

## 清理边界

- 删除可再生缓存与过期验证输出，不删除正式/历史资产、用户数据库、资产生成器。
- 旧根 index.html 含用户修改，原样迁到 archive/legacy-generator/index.html，仅作为历史资产与实现记录；当前唯一入口是 frontend/index.html。
- 删除失效的前端后端代理配置；保留维护用核心渲染 API，因为生成器和测试仍直接依赖。
- 构建依赖移到 devDependencies；补全 .gitignore，避免数据库、环境变量和缓存提交。
- 构建产物 dist/node_modules 不进入仓库；字体依赖的 VI 生成仍在 Windows 本地进行，CI 只校验并部署已生成资产，不伪装 Linux 字体等价。

## 流水线

CI：push / pull_request 时 npm ci、TypeScript、生产子路径构建、静态资产与路径校验。
Pages：main 推送或 workflow_dispatch 触发，使用 Pages artifact 与 GitHub 原生部署 action；用户已授权公开部署。
Release：推送 vi-v* tag 时校验交付索引、创建带版本的 Release 并上传既有压缩包，不重新生成有字体依赖的资产。

部署路径由 VITE_BASE_PATH 注入；所有图片、图标、索引和下载使用同一 base。新增功能只涉及路径与发布，不更改页面视觉。
