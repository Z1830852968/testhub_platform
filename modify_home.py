import os

with open('frontend/src/views/Home.vue', 'r') as f:
    content = f.read()

# Remove the blocks
blocks_to_remove = [
    """        <!-- 接口测试 -->
        <div class="nav-card" @click="handleNavigate('api')" role="button" tabindex="0">
          <div class="card-icon api-icon">
            <el-icon><Link /></el-icon>
          </div>
          <h3>{{ $t('home.apiTesting') }}</h3>
          <p>{{ $t('home.apiTestingDesc') }}</p>
        </div>""",
    """        <!-- UI自动化测试 -->
        <div class="nav-card" @click="handleNavigate('ui')" role="button" tabindex="0">
          <div class="card-icon ui-icon">
            <el-icon><Monitor /></el-icon>
          </div>
          <h3>{{ $t('home.uiAutomation') }}</h3>
          <p>{{ $t('home.uiAutomationDesc') }}</p>
        </div>""",
    """        <!-- APP自动化测试 -->
        <div class="nav-card" @click="handleNavigate('app')" role="button" tabindex="0">
          <div class="card-icon app-icon">
            <el-icon><Cellphone /></el-icon>
          </div>
          <h3>APP自动化测试</h3>
          <p>基于Airtest的Android APP自动化测试</p>
        </div>"""
]

for block in blocks_to_remove:
    content = content.replace(block, "")

with open('frontend/src/views/Home.vue', 'w') as f:
    f.write(content)

