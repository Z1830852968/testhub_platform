import re

with open('frontend/src/views/ai-intelligent-mode/testing/AIExecutionReport.vue', 'r') as f:
    content = f.read()

# Replace the extra div
content = content.replace("            </div>\n          </div>\n        </div>\n\n        <!-- 任务时间线 -->", "            </div>\n          </div>\n\n        <!-- 任务时间线 -->")

with open('frontend/src/views/ai-intelligent-mode/testing/AIExecutionReport.vue', 'w') as f:
    f.write(content)

