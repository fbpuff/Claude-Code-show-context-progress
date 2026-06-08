import sys, json, os, io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(sys.stdin)
dir_name = os.path.basename(data.get('cwd', '?'))
model = data.get('model', {}).get('display_name', '?')
ctx = data.get('context_window', {})
used_pct = int(ctx.get('used_percentage', 0))
total_input = ctx.get('total_input_tokens', 0)
total_output = ctx.get('total_output_tokens', 0)
current = ctx.get('current_usage', {})
ctx_used = current.get('input_tokens', 0) + current.get('output_tokens', 0)
ctx_total = ctx.get('context_window_size', 0)

# --- ANSI colors ---
GREEN  = '\033[32m'
YELLOW = '\033[33m'
RED    = '\033[31m'
DIM    = '\033[2m'
RESET  = '\033[0m'

# --- Color threshold ---
if used_pct < 60:
    color = GREEN
elif used_pct < 85:
    color = YELLOW
else:
    color = RED

# --- Progress bar ---
bar_width = 20
filled = min(used_pct * bar_width // 100, bar_width)
empty  = bar_width - filled
bar = f"{color}{'█' * filled}{RESET}{DIM}{'░' * empty}{RESET}"

# --- Token formatter ---
def fmt(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}k"
    return str(n)

# --- I/O tokens ---
io_str = ""
if total_input:
    io_str = f" │ {DIM}↓{RESET}{fmt(total_input)}"
    if total_output:
        io_str += f" {DIM}↑{RESET}{fmt(total_output)}"

# --- Context tokens ---
ctx_str = ""
if ctx_used and ctx_total:
    ctx_str = f" │ {DIM}{fmt(ctx_used)}/{fmt(ctx_total)}{RESET}"

# --- Output ---
print(f"[{model}] │ {dir_name}{io_str} │ {bar} {color}{used_pct}%{RESET}{ctx_str}")
