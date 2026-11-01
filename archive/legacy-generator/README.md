# 历史生成器（非当前入口）

`index.html` 是此前位于仓库根目录的自包含生成器，本轮整理时原样移动，保留用户已有修改。

- 文件长度：54121 字节。
- SHA256：`5a81304302c8804d25a9056442de3468a2f28d5f86cb08fc009856d06e45b87c`。
- 不参与 Vite 构建、GitHub Pages 或当前页面加载。
- 保存历史表情、装饰与旧版交互的实现记录，不作为新功能开发入口。
- 当前入口是 `frontend/index.html`，使用说明见根 `README.md`。

历史维护命令：`python scripts/extract_expressions.py --inject archive/legacy-generator/index.html`。当前资产构建不需要此命令。
