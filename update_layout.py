import re

with open('frontend/src/layout/index.vue', 'r') as f:
    content = f.read()

# 1. Remove ai-generation template
start_idx = content.find("          <!-- AI用例生成模块菜单 -->")
end_idx = content.find("          <!-- 接口测试模块菜单 -->")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 2. Update ai-intelligent-mode template
start_idx = content.find("          <!-- AI 智能模式模块菜单 -->")
end_idx = content.find("          <!-- 配置中心模块菜单 -->")

ai_intel_menu = """          <!-- AI 智能模式模块菜单 -->
          <template v-else-if="currentModule === 'ai-intelligent-mode'">
            <el-menu-item index="/ai-intelligent-mode/projects">
              <el-icon><Folder /></el-icon>
              <span>{{ $t('menu.projectManagement') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/requirement-analysis">
              <el-icon><MagicStick /></el-icon>
              <span>{{ $t('menu.aiCaseGeneration') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/testcases">
              <el-icon><Document /></el-icon>
              <span>{{ $t('menu.testCases') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/testing">
              <el-icon><VideoPlay /></el-icon>
              <span>{{ $t('menu.aiIntelligentTesting') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/execution-records">
              <el-icon><Timer /></el-icon>
              <span>{{ $t('menu.aiExecutionRecords') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/reports">
              <el-icon><DataAnalysis /></el-icon>
              <span>{{ $t('menu.testReport') }}</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/exploration">
              <el-icon><Monitor /></el-icon>
              <span>系统自动探索</span>
            </el-menu-item>
            <el-menu-item index="/ai-intelligent-mode/work-results">
              <el-icon><Collection /></el-icon>
              <span>AI工作成果</span>
            </el-menu-item>
          </template>

"""

content = content[:start_idx] + ai_intel_menu + content[end_idx:]

# 3. Update currentModule
content = content.replace("  if (route.path.startsWith('/ai-generation')) return 'ai-generation'\n", "")

# 4. Update moduleName
content = content.replace("    'ai-generation': t('modules.aiGeneration'),\n", "")

# 5. Update routeMap (replace ai-generation with ai-intelligent-mode where applicable)
content = content.replace("'/ai-generation/requirement-analysis'", "'/ai-intelligent-mode/requirement-analysis'")
content = content.replace("'/ai-generation/generated-testcases'", "'/ai-intelligent-mode/generated-testcases'")
content = content.replace("'/ai-generation/projects'", "'/ai-intelligent-mode/projects'")
content = content.replace("'/ai-generation/testcases'", "'/ai-intelligent-mode/testcases'")
content = content.replace("'/ai-generation/versions'", "'/ai-intelligent-mode/versions'")
content = content.replace("'/ai-generation/reviews'", "'/ai-intelligent-mode/reviews'")
content = content.replace("'/ai-generation/review-templates'", "'/ai-intelligent-mode/review-templates'")
content = content.replace("'/ai-generation/testsuites'", "'/ai-intelligent-mode/testsuites'")
content = content.replace("'/ai-generation/executions'", "'/ai-intelligent-mode/executions'")
content = content.replace("'/ai-generation/reports'", "'/ai-intelligent-mode/reports'")

content = content.replace("    // AI智能模式\n    '/ai-intelligent-mode/testing': t('menu.aiIntelligentTesting'),", "    // AI智能模式\n    '/ai-intelligent-mode/exploration': '系统自动探索',\n    '/ai-intelligent-mode/work-results': 'AI工作成果',\n    '/ai-intelligent-mode/testing': t('menu.aiIntelligentTesting'),")

# Profile route fix
content = content.replace("router.push('/ai-generation/profile')", "router.push('/ai-intelligent-mode/profile')")

with open('frontend/src/layout/index.vue', 'w') as f:
    f.write(content)
