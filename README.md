# Claude Code 状态栏 — 显示对话进度

在 Claude Code 终端底部实时显示：

```
my-project | deepseek-v4-pro[1m] | ███░░░░░░░░░░░░░░░░░ 15% used / 85% remaining | cost ¥1.08 / bal ¥110.00
```

## 显示内容

| 部分 | 示例 | 说明 |
|------|------|------|
| 目录名 | `my-project` | 当前工作目录 |
| 模型名 | `deepseek-v4-pro[1m]` | 当前模型 display_name |
| 进度条 | `███░░░░░░░░░░░░░░░░░` | 20 格，█=已用（每格 5%），░=剩余 |
| 上下文 | `15% used / 85% remaining` | 已用/剩余百分比 |
| 累计费用 | `cost ¥1.08` | 当前会话 API 累计消费（USD→CNY，汇率 7.2） |
| 剩余余额 | `bal ¥110.00` | DeepSeek 账户余额，每 60 秒自动刷新 |

## 版本

| 版本 | 文件 | 类型 | 功能 |
|------|------|------|------|
| **v2.1** (最新) | `statusline.py` | Python | 进度条 + 累计费用 + DeepSeek 余额 |
| v1.1 | `statusline.sh` | Bash + jq | 基础进度条 + 百分比 |

## v2.1 安装（推荐）

**前置要求：** Python 3，DeepSeek API Key 已配置在环境变量 `ANTHROPIC_AUTH_TOKEN` 中。

```bash
# 下载脚本
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.py -o ~/.claude/statusline.py
```

在 `~/.claude/settings.json` 中添加：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

> **Windows 用户**：将 `python3` 替换为 Python 完整路径，格式如 `/c/Users/用户名/AppData/Local/Programs/Python/Python313/python.exe`。

## v1.1 安装（Bash + jq）

**前置要求：** bash、jq

```bash
# 安装 jq
brew install jq          # macOS
sudo apt install jq      # Linux
winget install jqlang.jq # Windows

# 下载脚本
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.sh -o ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

在 `~/.claude/settings.json` 中添加：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  }
}
```

## 工作原理

Claude Code 每次刷新状态栏时，将会话 JSON 通过 stdin 传给脚本：

| 字段 | 说明 |
|------|------|
| `.cwd` | 当前工作目录 |
| `.model.display_name` | 模型名 |
| `.context_window.used_percentage` | 上下文已用% |
| `.context_window.remaining_percentage` | 上下文剩余% |
| `.cost.total_cost_usd` | 累计费用（USD） |

v2.1 额外调用 `GET https://api.deepseek.com/user/balance` 获取余额，60 秒缓存。

## 自定义

修改脚本中的变量：

```python
bar_width = 20     # 进度条宽度
USD_CNY_RATE = 7.2 # 汇率
```

## 许可

MIT
