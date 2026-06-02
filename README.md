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
| 进度条 | `███░░░░░░░░░░░░░░░░░` | 20 格，█=已用（每格 5%），░=剩余 |
| 百分比 | `15% used / 85% remaining` | 已用和剩余的精确百分比 |

---

## 安装

### Python 脚本（推荐，跨平台，零依赖）

**前置要求：** Python 3

1. 下载脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/fengzb7-cyber/Claude-Code-show-context-progress/master/statusline.py -o ~/.claude/statusline.py
```

2. 在 `~/.claude/settings.json` 中添加：

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

1. 安装 jq：
   - Windows: `winget install jqlang.jq`
   - macOS: `brew install jq`
   - Linux: `sudo apt install jq`

2. 下载脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/fengzb7-cyber/Claude-Code-show-context-progress/master/statusline.sh -o ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

3. 配置 `settings.json`：

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

> ⚠️ Claude Code 在 Windows 上使用 **Git Bash** 执行命令，所以路径必须使用 Unix 格式
> `/c/Users/xxx/...`，**不能**使用 `C:\Users\xxx\...`（反斜杠在 bash 中会被当作转义符）。

**正确格式：**

```json
{
  "statusLine": {
    "type": "command",
    "command": "/c/Users/<用户名>/AppData/Local/Programs/Python/Python313/python.exe /c/Users/<用户名>/.claude/statusline.py"
  }
}
```

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
    "command": "/c/Users/<用户名>/AppData/Local/Programs/Python/Python313/python.exe /c/Users/<用户名>/.claude/statusline.py"
  }
}
```

**方法 B：在 ccswitch 通用配置中添加**

ccswitch → Claude 设置 → 通用配置（Common Config），添加上述 `statusLine` JSON 片段，会对所有供应商生效。

---

## 常见问题

### Q: 状态栏完全不显示？

1. **验证 JSON 格式** — 用 `python -c "import json; json.load(open('~/.claude/settings.json'))"` 检查
2. **测试脚本**：
   ```bash
   echo '{"cwd":"test","model":{"display_name":"test"},"context_window":{"used_percentage":10,"remaining_percentage":90}}' | python3 ~/.claude/statusline.py
   ```
3. **检查路径格式** — Windows 上必须是 Unix 路径 (`/c/Users/...`)

### Q: ccswitch 切换后状态栏消失？

使用 `settings.local.json`（见上方"方法 A"）。

### Q: 进度条字符显示乱码（Windows 中文环境）？

Python 脚本已内置 UTF-8 输出修复。如果遇到 `UnicodeEncodeError: 'gbk' codec can't encode character`，确认使用的是最新的 `statusline.py`。

### Q: 显示 `bash: command not found`？

配置中使用了 `bash` 但系统执行的是 WSL bash。改用 Python 脚本，或指定完整 Git Bash 路径。

---

## 工作原理

Claude Code 每次刷新状态栏时，将当前会话 JSON 通过 stdin 传给脚本，脚本解析后输出一行文本显示在终端底部。

JSON 输入字段：

| 字段 | 说明 |
|------|------|
| `.cwd` | 当前工作目录 |
| `.model.display_name` | 模型显示名称 |
| `.context_window.used_percentage` | 上下文已用百分比 |
| `.context_window.remaining_percentage` | 上下文剩余百分比 |

## 自定义

- **进度条宽度**：修改 `statusline.py` 中的 `bar_width = 20`
- **输出格式**：修改最后一行的 `print` 语句
- **去掉进度条**：改为 `print(f"{dir_name} | {model} | {used}% used / {remaining}% remaining")`

## 文件

| 文件 | 说明 | 推荐 |
|------|------|------|
| `statusline.py` | Python 版本 | ✅ 推荐，无外部依赖，跨平台 |
| `statusline.sh` | Bash 版本 | Linux/macOS，需要 jq |

## 许可

MIT
