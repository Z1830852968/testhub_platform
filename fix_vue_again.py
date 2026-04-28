import re

with open('frontend/src/views/ai-intelligent-mode/testing/AIExecutionReport.vue', 'r') as f:
    content = f.read()

# Let's count all <div> and </div> tags in the template block
template_match = re.search(r'<template>.*?</template>', content, re.DOTALL)
if template_match:
    template = template_match.group(0)
    div_count = len(re.findall(r'<div', template))
    end_div_count = len(re.findall(r'</div', template))
    print(f"<div>: {div_count}, </div>: {end_div_count}")

# Remove one </div> before <div v-else class="report-error">
content = content.replace("        </div>\n      </div>\n\n      <div v-else class=\"report-error\">", "        </div>\n\n      <div v-else class=\"report-error\">")

with open('frontend/src/views/ai-intelligent-mode/testing/AIExecutionReport.vue', 'w') as f:
    f.write(content)

