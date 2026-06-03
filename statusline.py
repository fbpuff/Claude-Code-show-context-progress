import sys, json, os, io, time

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(sys.stdin)
dir_name = os.path.basename(data.get('cwd', '?'))
model = data.get('model', {}).get('display_name', '?')
used = data.get('context_window', {}).get('used_percentage', 0)
remaining = data.get('context_window', {}).get('remaining_percentage', '?')
cost_usd = data.get('cost', {}).get('total_cost_usd', 0)

# Progress bar: 20 chars wide
bar_width = 20
filled = min(int(used) * bar_width // 100, bar_width)
empty = max(bar_width - filled, 0)
bar = '█' * filled + '░' * empty

# Cumulative cost in CNY
cost_cny = round(cost_usd * 7.2, 2)

# DeepSeek balance — GET https://api.deepseek.com/user/balance
# Response: {"balance_infos": [{"currency": "CNY", "total_balance": "110.00", ...}]}
balance_str = ""
cache_file = os.path.expanduser("~/.claude/balance_cache.json")

try:
    fetch_new = True
    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime < 60:
            fetch_new = False

    if fetch_new:
        token = os.environ.get('ANTHROPIC_AUTH_TOKEN', '')
        if token:
            import urllib.request
            req = urllib.request.Request(
                "https://api.deepseek.com/user/balance",
                method="GET",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json"
                }
            )
            resp = urllib.request.urlopen(req, timeout=5)
            body = json.loads(resp.read())
            if body.get('is_available') and body.get('balance_infos'):
                total = body['balance_infos'][0]['total_balance']
                with open(cache_file, 'w') as f:
                    f.write(total)
except Exception:
    pass

# Read cached balance
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r') as f:
            cached = f.read().strip()
            if cached:
                balance_str = f"¥{cached}"
    except Exception:
        pass

if balance_str:
    print(f"{dir_name} | {model} | {bar} {used}% used / {remaining}% remaining | cost ¥{cost_cny:.2f} / bal {balance_str}")
else:
    print(f"{dir_name} | {model} | {bar} {used}% used / {remaining}% remaining | cost ¥{cost_cny:.2f}")
