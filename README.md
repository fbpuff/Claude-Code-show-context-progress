# Claude Code 显示对话进度

一个 Claude Code 状态栏脚本，在终端底部实时显示：**当前目录** | **模型名称** | **上下文进度条** | **已用/剩余百分比**。

## 效果预览

```
my-project | claude-sonnet-4-6 | ███░░░░░░░░░░░░░░░░░ 15% used / 85% remaining
```

| 部分 | 示例 | 说明 |
|------|------|------|
| 目录名 | `my-project` | 当前工作目录的 basename |
| 模型名 | `claude-sonnet-4-6` | 当前使用的模型 display_name |
| 进度条 | `███░░░░░░░░░░░░░░░░░` | 20 格，█=已用，░=剩余。超 100% 显示 `(overflow)` |
| 百分比 | `15% used / 85% remaining` | 已用/剩余百分比 |

---

## 安装

### Windows：独立 .exe（推荐，无需安装 Python）

1. 下载 [statusline.exe](https://github.com/fbpuff/Claude-Code-show-context-progress/releases/latest/download/statusline.exe) 到 `~/.claude/`

2. 在 `~/.claude/settings.json` 中添加：

```json
{
  "statusLine": {
    "type": "command",
    "command": "/c/Users/<用户名>/.claude/statusline.exe"
  }
}
```

> ⚠️ 路径必须使用 Unix 格式 `/c/Users/...`，详见下方 [Windows 配置详解](#windows-配置详解)。

### macOS / Linux：Python 脚本

**前置要求：** Python 3

```bash
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.py -o ~/.claude/statusline.py
```

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

### Bash 脚本（需要 jq）

**前置要求：** bash、jq

```bash
# 安装 jq: brew install jq (macOS) / sudo apt install jq (Linux) / winget install jqlang.jq (Windows)
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.sh -o ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  }
}
```

---

## Windows 配置详解

### 关键：Unix 路径格式

> ⚠️ Claude Code 在 Windows 上使用 **Git Bash** 执行命令，路径必须使用 Unix 格式
> `/c/Users/xxx/...`，**不能**使用 `C:\Users\xxx\...`（反斜杠在 bash 中会被当作转义符）。

### 如果你使用 ccswitch

ccswitch 切换供应商时会覆盖 `settings.json`。推荐以下方法：

**方法 A：使用 `settings.local.json`（推荐）**

将配置放在 `~/.claude/settings.local.json`，ccswitch **永远不会**覆盖此文件：

```json
{
  "permissions": {
    "allow": [
      "Bash(/c/Users/<用户名>/AppData/Local/Programs/Python/Python313/python.exe *)"
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "/c/Users/<用户名>/.claude/statusline.exe"
  }
}
```

**方法 B：在 ccswitch 通用配置中添加**

ccswitch → Claude 设置 → 通用配置（Common Config），添加上述 `statusLine` JSON 片段。

---

## 常见问题

### Q: 状态栏不显示？

1. **验证 JSON 格式** — 用 Python 验证 `settings.json` 语法
2. **测试脚本**：
   ```bash
   echo '{"cwd":"test","model":{"display_name":"test"},"context_window":{"used_percentage":10,"remaining_percentage":90}}' | ~/.claude/statusline.exe
   ```
3. **检查路径格式** — Windows 上必须是 Unix 路径（`/c/Users/...`）

### Q: ccswitch 切换后状态栏消失？

使用 `settings.local.json`（见上方"方法 A"）。

### Q: 中文文件夹名显示乱码？

v1.0.0 已修复 stdin/stdout 编码问题。如仍有问题请升级到最新版。

## 工作原理

Claude Code 每次刷新状态栏时，将当前会话 JSON 通过 stdin 传给脚本，脚本解析后输出一行文本显示在终端底部。

| 字段 | 说明 |
|------|------|
| `.cwd` | 当前工作目录 |
| `.model.display_name` | 模型显示名称 |
| `.context_window.used_percentage` | 上下文已用百分比 |
| `.context_window.remaining_percentage` | 上下文剩余百分比 |

## 文件

| 文件 | 说明 | 适合 |
|------|------|------|
| `statusline.exe` | Windows 独立可执行文件，零依赖 | Windows 用户 |
| `statusline.py` | Python 脚本，跨平台 | macOS / Linux |
| `statusline.sh` | Bash 脚本 | 需要 jq 的环境 |

## 许可

MIT
