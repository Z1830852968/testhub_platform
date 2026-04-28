import re

with open('frontend/src/router/index.js', 'r') as f:
    content = f.read()

# Remove api-testing
start_idx = content.find("  {\n    path: '/api-testing',")
end_idx = content.find("  {\n    path: '/ui-automation',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# Remove ui-automation
start_idx = content.find("  {\n    path: '/ui-automation',")
end_idx = content.find("  {\n    path: '/app-automation',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# Remove app-automation
start_idx = content.find("  {\n    path: '/app-automation',")
end_idx = content.find("  {\n    path: '/ai-intelligent-mode',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# Also remove import lines
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'views/api-testing/' in line or 'views/ui-automation/' in line or 'views/app-automation/' in line:
        continue
    new_lines.append(line)

with open('frontend/src/router/index.js', 'w') as f:
    f.write('\n'.join(new_lines))

