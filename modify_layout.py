import re

with open('frontend/src/layout/index.vue', 'r') as f:
    content = f.read()

# 1. Remove the api-testing block
start_api = content.find("          <!-- 接口测试模块菜单 -->")
end_api = content.find("          <!-- UI自动化测试模块菜单 -->")
if start_api != -1 and end_api != -1:
    content = content[:start_api] + content[end_api:]

# 2. Remove the ui-automation block
start_ui = content.find("          <!-- UI自动化测试模块菜单 -->")
end_ui = content.find("          <!-- APP自动化测试模块菜单 -->")
if start_ui != -1 and end_ui != -1:
    content = content[:start_ui] + content[end_ui:]

# 3. Remove the app-automation block
start_app = content.find("          <!-- APP自动化测试模块菜单 -->")
end_app = content.find("          <!-- AI 智能模式模块菜单 -->")
if start_app != -1 and end_app != -1:
    content = content[:start_app] + content[end_app:]

# Fix the first v-else-if to v-if
content = content.replace("<template v-else-if=\"currentModule === 'ai-intelligent-mode'\">", "<template v-if=\"currentModule === 'ai-intelligent-mode'\">")

# 4. Remove currentModule mapping
content = content.replace("  if (route.path.startsWith('/api-testing')) return 'api-testing'\n", "")
content = content.replace("  if (route.path.startsWith('/ui-automation')) return 'ui-automation'\n", "")
content = content.replace("  if (route.path.startsWith('/app-automation')) return 'app-automation'\n", "")

# 5. Remove moduleName mapping
content = content.replace("    'api-testing': t('modules.apiTesting'),\n", "")
content = content.replace("    'ui-automation': t('modules.uiAutomation'),\n", "")
content = content.replace("    'app-automation': 'APP自动化测试',\n", "")

# 6. Remove breadcrumb map entries
# Find start of "    // 接口测试"
start_api_route = content.find("    // 接口测试")
end_api_route = content.find("    // UI自动化测试")
if start_api_route != -1 and end_api_route != -1:
    content = content[:start_api_route] + content[end_api_route:]

start_ui_route = content.find("    // UI自动化测试")
end_ui_route = content.find("    // APP自动化")
if start_ui_route != -1 and end_ui_route != -1:
    content = content[:start_ui_route] + content[end_ui_route:]

start_app_route = content.find("    // APP自动化")
end_app_route = content.find("    // 配置中心")
if start_app_route != -1 and end_app_route != -1:
    content = content[:start_app_route] + content[end_app_route:]

with open('frontend/src/layout/index.vue', 'w') as f:
    f.write(content)

