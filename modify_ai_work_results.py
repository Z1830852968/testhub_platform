import re

with open('frontend/src/views/ai-intelligent-mode/AIWorkResults.vue', 'r') as f:
    content = f.read()

# Add button
button_html = """
              <div class="bottom clearfix">
                <p class="desc">{{ item.description }}</p>
                <el-link type="primary" :href="item.url" target="_blank">{{ item.url }}</el-link>
                <div class="action-buttons" style="margin-top: 10px;">
                  <el-button type="success" size="small" @click="generateTestCase(item)">
                    <el-icon><MagicStick /></el-icon> 一键生成用例
                  </el-button>
                </div>
              </div>
"""

content = content.replace("""              <div class="bottom clearfix">
                <p class="desc">{{ item.description }}</p>
                <el-link type="primary" :href="item.url" target="_blank">{{ item.url }}</el-link>
              </div>""", button_html)

# Add import MagicStick and router
script_import = """import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MagicStick } from '@element-plus/icons-vue'
import api from '@/utils/api'

const router = useRouter()
"""

content = content.replace("""import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'""", script_import)

# Add generateTestCase method
generate_method = """
const generateTestCase = (item) => {
  router.push({
    path: '/ai-intelligent-mode/requirement-analysis',
    query: {
      title: `探索发现功能: ${item.name}`,
      desc: `页面URL: ${item.url}\\n\\n功能描述: ${item.description}\\n\\n请针对此探索出的功能生成详尽的测试用例。`
    }
  })
}
"""

content = content.replace("const loadFeatures", generate_method + "\nconst loadFeatures")

with open('frontend/src/views/ai-intelligent-mode/AIWorkResults.vue', 'w') as f:
    f.write(content)

