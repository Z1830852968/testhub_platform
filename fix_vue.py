import re

with open('frontend/src/views/ai-intelligent-mode/testing/AIExecutionReport.vue', 'r') as f:
    content = f.read()

# Fix the broken tags
content = content.replace("</div>   <!-- 任务时间线 -->", "</div>\n\n        <!-- 任务时间线 -->")

# Also, there's an extra </div> at the end of the file or around line 258?
# Let's count divs inside the template.
