# Zotero MCP Server 离线依赖缓存

本目录缓存了 `zotero-mcp-server` (v0.4.1) 及其全部 Python 依赖的 wheel 文件。

## 📦 内容

- **76 个文件**，共约 15 MB
- **74 个** `py3-none-any.whl` — 纯 Python 包，跨平台通用
- **2 个** `.tar.gz` — 源码包（`bibtexparser`, `sgmllib3k`）

## ✅ 平台兼容性

所有 wheel 文件均为 **纯 Python**（`py3-none-any`），可在以下平台直接使用：

| 平台 | 兼容性 |
|------|--------|
| macOS ARM64 (Apple Silicon) | ✅ |
| macOS x86_64 (Intel) | ✅ |
| Linux x86_64 | ✅ |
| Linux ARM64 | ✅ |
| Windows x86_64 | ✅ |
| Windows ARM64 | ✅ |

## 🔧 使用方式

`setup_zotero.py --install` 自动使用本目录：

```bash
# 优先使用本地 wheel（离线），平台依赖自动从 PyPI 补全
python3 scripts/setup_zotero.py --install
```

安装逻辑：
1. `pip install zotero-mcp-server --find-links scripts/packages/` — pip 优先用本地 `.whl`
2. 若本地缺失某些包的匹配版本，pip 自动从 PyPI 下载
3. 若上述均失败，尝试直接安装本地 `zotero_mcp_server-*.whl`
4. 最终回退：`pip install zotero-mcp-server`（全量从 PyPI 下载）

## ⚠️ 注意事项

- **本目录由原作者维护**，升级 `zotero-mcp-server` 版本时需同步更新 wheel
- **断网环境**：只要 `scripts/packages/` 完整，可完全离线安装
- **更新依赖**：
  ```bash
  pip download zotero-mcp-server --dest scripts/packages/
  ```

## 📄 许可证

本目录中的软件包遵循各自的原始许可证。上游项目：
- [zotero-mcp-server](https://github.com/54yyyu/zotero-mcp) (MIT)
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) (MIT)
