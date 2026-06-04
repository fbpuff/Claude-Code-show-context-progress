import sys, json, os, io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(sys.stdin)
dir_name = os.path.basename(data.get('cwd', '?'))
model = data.get('model', {}).get('display_name', '?')
used = data.get('context_window', {}).get('used_percentage', 0)
remaining = data.get('context_window', {}).get('remaining_percentage', '?')
ctx = data.get('context_window', {})

# Progress bar: 20 chars wide
bar_width = 20
filled = min(int(used) * bar_width // 100, bar_width)
empty = max(bar_width - filled, 0)
bar = "█" * filled + "░" * empty

# Detect provider
extra = ""
model_lower = model.lower()

if "glm" in model_lower:
    # GLM / 智谱AI: show token usage
    tu = ctx.get("tokens_used", 0)
    tt = ctx.get("tokens_total", 0)
    if tu and tt:
        extra = f"tokens {tu}/{tt}"
    else:
        extra = f"tokens {ctx}"  # fallback: show what we have

# Build output
parts = [f"{dir_name} | {model} | {bar} {used}% used / {remaining}% remaining"]
if extra:
    parts.append(extra)

print(" | ".join(parts))
