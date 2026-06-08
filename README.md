# Claude Code Statusline

Claude Code 终端状态栏，实时显示上下文用量、token 统计，带颜色进度条。

```
[Sonnet 4.6] │ my-project │ ↓170k ↑290 │ ███░░░░░░░░░░░░░░░░░ 15% │ 80k/1M
```

## 功能

| 显示 | 示例 | 说明 |
|------|------|------|
| 模型 | `[Sonnet 4.6]` | 当前模型 display_name |
| 目录 | `my-project` | 当前工作目录名 |
| 输入 | `↓170k` | 会话累计输入 token |
| 输出 | `↑290` | 最近一次响应输出 token |
| 进度条 | `████████░░░░░░░░░░░░` | 20 格，颜色随用量变化 |
| 百分比 | `15%` | 上下文已用百分比 |
| 占用 | `80k/1M` | 当前占用 / 窗口总大小 |

进度条颜色自动切换：**< 60% 绿** → **60–85% 黄** → **> 85% 红**。

## 安装

**前置要求：** Python 3。

```bash
# 下载脚本
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.py -o ~/scripts/statusline.py
```

在 `~/.claude/settings.local.json` 中配置（建议用 `settings.local.json`，避免被 ccswitch 等工具覆盖）：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/scripts/statusline.py"
  }
}
```

Windows 用户将 `python3` 替换为完整 Python 路径，如：

```json
"command": "/c/Users/用户名/AppData/Local/Programs/Python/Python313/python.exe /c/Users/用户名/scripts/statusline.py"
```

重启 Claude Code 即生效。

## 工作原理

Claude Code 每次刷新状态栏时（约 300ms），通过 stdin 传入会话 JSON。本脚本纯本地解析，无网络请求。

读取的字段：

| 字段 | 用途 |
|------|------|
| `.model.display_name` | 模型名 |
| `.cwd` | 工作目录 |
| `.context_window.used_percentage` | 上下文用量% |
| `.context_window.total_input_tokens` | 会话累计输入 token |
| `.context_window.total_output_tokens` | 最近输出 token |
| `.context_window.current_usage.input_tokens` | 当前上下文输入占用 |
| `.context_window.current_usage.output_tokens` | 当前上下文输出占用 |
| `.context_window.context_window_size` | 窗口总大小 |

## 自定义

```python
bar_width = 20    # 进度条宽度
```

颜色阈值在 `Color threshold` 段调整。

## 对比

| | 本脚本 | ccstatusline | claude-hud |
|------|--------|--------------|------------|
| 体积 | 60 行 Python | 大型 npm 包 | Claude Code 插件 |
| 安装 | 单文件下载 | npx / npm | /plugin install |
| 配置 | 改源码 | TUI | slash command |
| 零网络依赖 | ✓ | — | — |
| 工具/Agent 追踪 | — | — | ✓ |
| 颜色进度条 | ✓ | ✓ | ✓ |
| I/O token | ✓ | — | — |

## 许可

MIT
