# Claude Code Statusline

在 Claude Code 终端底部实时显示上下文用量、token 统计，带颜色进度条。

```
[Sonnet 4.6] │ my-project │ ↓170k ↑290 │ ███░░░░░░░░░░░░░░░░░ 15% │ 80k/1M
```

## 显示内容

| 元素 | 示例 | 说明 |
|------|------|------|
| 模型名 | `[Sonnet 4.6]` | 当前模型 display_name |
| 目录名 | `my-project` | 当前工作目录（basename） |
| 累计输入 | `↓170k` | 会话累计输入 token 数（自动换算 k/M） |
| 最近输出 | `↑290` | 最近一次响应输出 token 数 |
| 进度条 | `███░░░░░░░░░░░░░░░░░` | 20 格，绿 → 黄 → 红随用量变化 |
| 百分比 | `15%` | 上下文已用百分比，颜色与进度条同步 |
| Token 占用 | `80k/1M` | 当前占用 / 上下文窗口大小 |

### 颜色阈值

| 区间 | 颜色 | 含义 |
|------|------|------|
| < 60% | 绿色 | 宽松 |
| 60% – 85% | 黄色 | 注意 |
| > 85% | 红色 | 接近上限 |

## 安装

### 1. 下载脚本

```bash
curl -fsSL https://raw.githubusercontent.com/fbpuff/Claude-Code-show-context-progress/master/statusline.py -o ~/scripts/statusline.py
```

**前置要求：** Python 3。

### 2. 配置 Claude Code

在 `~/.claude/settings.local.json` 中添加（推荐用 `settings.local.json` 避免被 ccswitch 等工具覆盖）：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/scripts/statusline.py"
  }
}
```

> **Windows 用户**：将 `python3` 替换为完整路径，如 `/c/Users/fbpuf/AppData/Local/Programs/Python/Python313/python.exe`，脚本路径也用绝对路径。

### 3. 重启 Claude Code

完全退出后重新启动，状态栏即出现。

## stdin 数据来源

Claude Code 每次刷新时通过 stdin 传入会话 JSON。本脚本读取以下字段：

| 字段 | 用途 |
|------|------|
| `.model.display_name` | 模型名 |
| `.cwd` | 当前工作目录 |
| `.context_window.used_percentage` | 上下文已用% |
| `.context_window.total_input_tokens` | 会话累计输入 token |
| `.context_window.total_output_tokens` | 最近响应输出 token |
| `.context_window.current_usage.input_tokens` | 当前上下文输入占用 |
| `.context_window.current_usage.output_tokens` | 当前上下文输出占用 |
| `.context_window.context_window_size` | 上下文窗口总大小 |

无需任何 API 调用，纯 stdin 解析，零网络开销。

## 自定义

修改脚本顶部常量：

```python
bar_width = 20         # 进度条宽度（字符数）
```

颜色阈值在脚本 `Color threshold` 段调整。

## 对比其他方案

| | 本脚本 (v3.2) | ccstatusline | claude-hud |
|------|------------|--------------|------------|
| 体积 | 60 行 Python | 大型 npm 包 | Claude Code 插件 |
| 安装 | 单文件下载 | npx / npm install | /plugin install |
| 配置 | 改源码 | TUI 图形界面 | slash command |
| 工具/Agent 追踪 | 不支持 | 不支持 | 支持 |
| 零网络依赖 | ✓ | — | — |
| 颜色进度条 | ✓ | ✓ | ✓ |
| 输入/输出 token | ✓ | ✓ | — |

## Bash 版本

仓库中 `statusline.sh` 是 v1.x 的 Bash + jq 版本，功能为基础进度条 + 百分比，不再维护。建议使用 Python 版本。

## 许可

MIT
