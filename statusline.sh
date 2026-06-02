#!/bin/bash
# Claude Code statusline — directory | model | progress bar | context usage
# Displays: myproject | claude-sonnet-4-6 | ███░░░░░░░░░░░░░░░░░ 15% used / 85% remaining

input=$(cat)
dir=$(echo "$input" | jq -r '.cwd | sub(".*[/\\\\]"; "")')
model=$(echo "$input" | jq -r '.model.display_name')
used=$(echo "$input" | jq -r '.context_window.used_percentage // "0"')
remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // "?"')

# Progress bar: 20 chars wide (each block = 5%)
bar_width=20
filled=$(( used * bar_width / 100 ))
[ "$filled" -gt "$bar_width" ] && filled=$bar_width
empty=$(( bar_width - filled ))

bar=$(printf '█%.0s' $(seq 1 $filled))
bar="${bar}$(printf '░%.0s' $(seq 1 $empty))"

echo "${dir} | ${model} | ${bar} ${used}% used / ${remaining}% remaining"
