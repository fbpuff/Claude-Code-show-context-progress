# Claude Code 显示对话进度

一个 Claude Code 状态栏脚本，在终端底部实时显示：**当前目录** | **模型名称** | **上下文进度条** | **已用/剩余百分比**。

## 效果预览

```
my-project | claude-sonnet-4-6 | ███░░░░░░░░░░░░░░░░░ 15% used / 85% remaining
```

### 显示内容说明

| 部分 | 示例 | 说明 |
|------|------|------|
| 目录名 | `my-project` | 当前工作目录的 basename |
| 模型名 | `claude-sonnet-4-6` | 当前使用的模型 display_name |
| 进度条 | `███░░░░░░░░░░░░░░░░░` | 20 格，█=已用（每格 5%），░=剩余 |
| 百分比 | `15% used / 85% remaining` | 已用和剩余的精确百分比 |

## 前置要求

- **jq** — JSON 解析工具
- **bash** — 运行脚本

### 安装 jq

| 系统 | 命令 |
|------|------|
| Windows (winget) | `winget install jqlang.jq` |
| macOS (Homebrew) | `brew install jq` |
| Linux (apt) | `sudo apt install jq` |

## 安装步骤

### 1. 下载脚本

将 `statusline.sh` 放到 `~/.claude/` 目录下：

```bash
mkdir -p ~/.claude
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

### 2. 配置 settings.json

在 `~/.claude/settings.json` 中添加 `statusLine` 配置：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  }
}
```

如果已存在其他配置，只需将 `statusLine` 部分合并进去即可。

> **Windows 用户**：如果 `bash` 不在 PATH 中，将路径改为 `"C:\\Program Files\\Git\\bin\\bash.exe"` 或 Git Bash 的实际安装路径。

### 3. 重启 Claude Code

重启后即可在终端底部看到状态栏。

## 工作原理

Claude Code 每次刷新状态栏时，会将当前会话的 JSON 数据通过 stdin 传给脚本，脚本用 jq 提取字段并格式化输出。

JSON 字段参考：
- `.cwd` — 当前工作目录
- `.model.display_name` — 模型显示名称
- `.context_window.used_percentage` — 上下文已用百分比
- `.context_window.remaining_percentage` — 上下文剩余百分比

## 自定义

修改 `statusline.sh` 中的变量即可调整显示：

```bash
bar_width=20   # 进度条宽度（格数）
```

也可以调整 `echo` 行的输出格式，比如去掉进度条只保留百分比：

```bash
echo "${dir} | ${model} | ${used}% used / ${remaining}% remaining"
```

## 许可

MIT
