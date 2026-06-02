import sys, json, os, io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(sys.stdin)
dir_name = os.path.basename(data.get('cwd', '?'))
model = data.get('model', {}).get('display_name', '?')
used = data.get('context_window', {}).get('used_percentage', 0)
remaining = data.get('context_window', {}).get('remaining_percentage', '?')

# Progress bar: 20 chars wide
bar_width = 20
filled = min(int(used) * bar_width // 100, bar_width)
empty = bar_width - filled
bar = '█' * filled + '░' * empty

print(f"{dir_name} | {model} | {bar} {used}% used / {remaining}% remaining")
