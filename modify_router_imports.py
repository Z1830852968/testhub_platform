import re

with open('frontend/src/router/index.js', 'r') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
for line in lines:
    if 'import' in line and ('views/api-testing/' in line or 'views/ui-automation/' in line or 'views/app-automation/' in line):
        continue
    new_lines.append(line)

with open('frontend/src/router/index.js', 'w') as f:
    f.write('\n'.join(new_lines))

