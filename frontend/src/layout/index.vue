<template>
  <div class="layout">
    <el-container class="app-wrapper">
      <!-- 顶部导航栏 -->
      <el-header height="64px" class="app-header">
        <div class="header-left">
          <div class="logo" @click="router.push('/ai-intelligent-mode/projects')">
            <img :src="logoImage" alt="TestHub" class="logo-img" />
          </div>
          
          <el-menu
            mode="horizontal"
            :default-active="currentModule"
            @select="handleModuleChange"
            class="top-menu"
            :ellipsis="false"
          >
            <el-menu-item index="ai-intelligent-mode">
              <el-icon><Cpu /></el-icon>
              <span>{{ $t('modules.aiIntelligentMode') }}</span>
            </el-menu-item>
            <el-menu-item index="configuration">
              <el-icon><Setting /></el-icon>
              <span>{{ $t('modules.configuration') }}</span>
            </el-menu-item>
          </el-menu>
        </div>

        <div class="header-right">
          <!-- 语言切换 -->
          <el-dropdown @command="handleLanguageChange" class="action-item">
            <span class="language-selector">
              <span class="language-flag">{{ appStore.language === 'zh-cn' ? '🇨🇳' : '🇺🇸' }}</span>
              <span class="language-text">{{ currentLanguage }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="zh-cn" :disabled="appStore.language === 'zh-cn'">
                  <span class="dropdown-flag">🇨🇳</span> 简体中文
                </el-dropdown-item>
                <el-dropdown-item command="en" :disabled="appStore.language === 'en'">
                  <span class="dropdown-flag">🇺🇸</span> English
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <!-- 用户信息 -->
          <el-dropdown @command="handleCommand" class="action-item user-dropdown">
            <span class="user-info">
              <el-avatar :size="32" :src="userStore.user?.avatar || defaultAvatar" class="avatar" />
              <span class="username">{{ userStore.user?.username }}</span>
              <el-icon class="arrow-icon"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>{{ $t('nav.profile') }}
                </el-dropdown-item>
                <el-dropdown-item divided command="logout" class="logout-item">
                  <el-icon><SwitchButton /></el-icon>{{ $t('nav.logout') }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-container class="main-container">
        <!-- 侧边栏 -->
        <el-aside width="220px" class="app-sidebar">
          <el-menu
            :default-active="$route.path"
            router
            class="side-menu"
          >
            <!-- AI 智能模式模块菜单 -->
            <template v-if="currentModule === 'ai-intelligent-mode'">
              <div class="menu-group-title">工作空间</div>
              <el-menu-item index="/ai-intelligent-mode/projects">
                <el-icon><Folder /></el-icon>
                <span>{{ $t('menu.projectManagement') }}</span>
              </el-menu-item>
              <el-menu-item index="/ai-intelligent-mode/exploration">
                <el-icon><Monitor /></el-icon>
                <span>系统自动探索</span>
              </el-menu-item>
              <el-menu-item index="/ai-intelligent-mode/work-results">
                <el-icon><Collection /></el-icon>
                <span>AI工作成果</span>
              </el-menu-item>

              <div class="menu-group-title" style="margin-top: 15px;">智能测试</div>
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
            </template>

            <!-- 配置中心模块菜单 -->
            <template v-else-if="currentModule === 'configuration'">
              <div class="menu-group-title">核心配置</div>
              <el-sub-menu index="ai-case-generation">
                <template #title>
                  <el-icon><MagicStick /></el-icon>
                  <span>{{ $t('menu.aiCaseGenerationConfig') }}</span>
                </template>
                <el-menu-item index="/configuration/ai-model">
                  <el-icon><Cpu /></el-icon>
                  <span>{{ $t('menu.aiModelConfig') }}</span>
                </el-menu-item>
                <el-menu-item index="/configuration/prompt-config">
                  <el-icon><Edit /></el-icon>
                  <span>{{ $t('menu.promptConfig') }}</span>
                </el-menu-item>
                <el-menu-item index="/configuration/generation-config">
                  <el-icon><Setting /></el-icon>
                  <span>{{ $t('menu.generationConfig') }}</span>
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item index="/configuration/ai-mode">
                <el-icon><MagicStick /></el-icon>
                <span>{{ $t('menu.aiModeConfig') }}</span>
              </el-menu-item>
              <el-menu-item index="/configuration/dify">
                <el-icon><ChatDotRound /></el-icon>
                <span>{{ $t('menu.difyConfig') }}</span>
              </el-menu-item>

              <div class="menu-group-title" style="margin-top: 15px;">环境与调度</div>
              <el-menu-item index="/configuration/ui-env">
                <el-icon><Monitor /></el-icon>
                <span>{{ $t('menu.uiEnvConfig') }}</span>
              </el-menu-item>
              <el-menu-item index="/configuration/app-env">
                <el-icon><Cellphone /></el-icon>
                <span>APP环境配置</span>
              </el-menu-item>
              <el-menu-item index="/configuration/scheduled-task">
                <el-icon><Timer /></el-icon>
                <span>{{ $t('menu.scheduledTaskConfig') }}</span>
              </el-menu-item>
            </template>
          </el-menu>
        </el-aside>

        <!-- 主体内容区域 -->
        <el-main class="app-main">
          <div class="breadcrumb-wrapper">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/ai-intelligent-mode/projects' }">{{ $t('nav.home') }}</el-breadcrumb-item>
              <el-breadcrumb-item v-if="moduleName">{{ moduleName }}</el-breadcrumb-item>
              <el-breadcrumb-item>{{ breadcrumbTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="page-content-wrapper">
            <router-view v-slot="{ Component }">
              <transition name="fade-transform" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import {
  Monitor, Folder, Document, Flag, Check, Collection, VideoPlay,
  DataAnalysis, ChatDotRound, DocumentCopy, Link, MagicStick,
  Odometer, Timer, Setting, AlarmClock, Bell, Aim, Edit, Cpu, ArrowDown, Cellphone, Connection, FolderOpened, User, SwitchButton
} from '@element-plus/icons-vue'
import logoSvg from '@/assets/images/logo.svg'
import logoHomePng from '@/assets/images/logo_home.png'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()
const { t } = useI18n()

const logoImage = computed(() => {
  return logoHomePng
})

const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 当前语言显示
const currentLanguage = computed(() => {
  return appStore.language === 'zh-cn' ? '简体中文' : 'English'
})

// 切换语言
const handleLanguageChange = (lang) => {
  appStore.setLanguage(lang)
  ElMessage.success(lang === 'zh-cn' ? '语言已切换为中文' : 'Language switched to English')
}

// 当前模块
const currentModule = computed(() => {
  if (route.path.startsWith('/ai-intelligent-mode')) return 'ai-intelligent-mode'
  if (route.path.startsWith('/configuration')) return 'configuration'
  // Default to intelligent mode if unmatched
  return 'ai-intelligent-mode'
})

// 处理顶部导航切换
const handleModuleChange = (index) => {
  if (index === 'ai-intelligent-mode') {
    router.push('/ai-intelligent-mode/projects')
  } else if (index === 'configuration') {
    router.push('/configuration/ai-model')
  }
}

const moduleName = computed(() => {
  const map = {
    'ai-intelligent-mode': t('modules.aiIntelligentMode'),
    'configuration': t('modules.configuration')
  }
  return map[currentModule.value] || ''
})

const breadcrumbTitle = computed(() => {
  const routeMap = {
    // AI智能模式
    '/ai-intelligent-mode/requirement-analysis': t('menu.aiCaseGeneration'),
    '/ai-intelligent-mode/generated-testcases': t('menu.aiGeneratedTestcases'),
    '/ai-intelligent-mode/projects': t('menu.projectManagement'),
    '/ai-intelligent-mode/testcases': t('menu.testCases'),
    '/ai-intelligent-mode/versions': t('menu.versionManagement'),
    '/ai-intelligent-mode/reviews': t('menu.reviewList'),
    '/ai-intelligent-mode/review-templates': t('menu.reviewTemplates'),
    '/ai-intelligent-mode/testsuites': t('menu.suiteManagement'),
    '/ai-intelligent-mode/executions': t('menu.executionRecords'),
    '/ai-intelligent-mode/reports': t('menu.testReport'),

    // 配置中心
    '/configuration/ai-model': t('menu.aiModelConfig'),
    '/configuration/prompt-config': t('menu.promptConfig'),
    '/configuration/generation-config': t('menu.generationConfig'),
    '/configuration/ui-env': t('menu.uiEnvConfig'),
    '/configuration/ai-mode': t('menu.aiModeConfig'),
    '/configuration/scheduled-task': t('menu.scheduledTaskConfig'),
    '/configuration/dify': t('menu.difyConfig'),

    '/profile': t('nav.profile')
  }
  return routeMap[route.path] || route.meta.title || ''
})

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/ai-intelligent-mode/profile')
  }
}
</script>

<style lang="scss" scoped>
.layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #f0f2f5;
}

.app-wrapper {
  height: 100%;
  flex-direction: column;
}

.app-header {
  background: #ffffff;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  z-index: 10;
  position: relative;

  .header-left {
    display: flex;
    align-items: center;
    height: 100%;

    .logo {
      display: flex;
      align-items: center;
      cursor: pointer;
      margin-right: 40px;
      transition: opacity 0.3s;

      &:hover {
        opacity: 0.8;
      }

      .logo-img {
        height: 40px;
        object-fit: contain;
      }

      .logo-text {
        font-size: 20px;
        font-weight: 600;
        color: #1f1f1f;
        letter-spacing: 0.5px;
      }
    }

    .top-menu {
      border-bottom: none;
      height: 64px;
      
      .el-menu-item {
        height: 64px;
        line-height: 64px;
        font-size: 15px;
        font-weight: 500;
        padding: 0 20px;
        color: #5c6b77 !important;
        border-bottom: 2px solid transparent;

        .el-icon {
          margin-right: 6px;
          font-size: 18px;
        }

        &.is-active {
          color: #1890ff !important;
          border-bottom-color: #1890ff;
          background-color: transparent !important;
        }

        &:hover {
          color: #1890ff !important;
          background-color: #f8faff !important;
        }
      }
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;

    .action-item {
      height: 100%;
      display: flex;
      align-items: center;
      padding: 0 12px;
      cursor: pointer;
      transition: all 0.3s;
      border-radius: 6px;

      &:hover {
        background: #f5f7fa;
      }
    }

    .language-selector {
      display: flex;
      align-items: center;
      color: #5c6b77;
      font-size: 14px;
      font-weight: 500;

      .language-flag {
        font-size: 18px;
        margin-right: 6px;
      }
    }

    .user-info {
      display: flex;
      align-items: center;
      
      .avatar {
        border: 1px solid #e8e8e8;
      }

      .username {
        margin: 0 10px;
        color: #1f1f1f;
        font-size: 14px;
        font-weight: 500;
      }

      .arrow-icon {
        color: #8c8c8c;
        font-size: 12px;
      }
    }
  }
}

.main-container {
  height: calc(100vh - 64px);
  overflow: hidden;
}

.app-sidebar {
  background: #ffffff;
  box-shadow: 2px 0 8px 0 rgba(29,35,41,.05);
  z-index: 9;
  display: flex;
  flex-direction: column;

  .side-menu {
    border-right: none;
    padding: 12px 0;
    flex: 1;
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 6px;
    }
    &::-webkit-scrollbar-thumb {
      background: #dcdfe6;
      border-radius: 3px;
    }

    .menu-group-title {
      font-size: 12px;
      color: #909399;
      padding: 8px 24px;
      margin-bottom: 4px;
      letter-spacing: 1px;
    }

    .el-menu-item, :deep(.el-sub-menu__title) {
      height: 44px;
      line-height: 44px;
      margin: 4px 12px;
      border-radius: 6px;
      color: #4e5969;
      
      &:hover {
        color: #1890ff;
        background-color: #f0f7ff;
      }

      &.is-active {
        background-color: #e6f4ff;
        color: #1890ff;
        font-weight: 500;
      }

      .el-icon {
        font-size: 16px;
      }
    }
  }
}

.app-main {
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f0f2f5;

  .breadcrumb-wrapper {
    padding: 16px 24px;
    background: #ffffff;
    border-bottom: 1px solid #f0f0f0;

    :deep(.el-breadcrumb) {
      font-size: 14px;
      
      .el-breadcrumb__inner {
        color: #8c8c8c;
        font-weight: normal;

        &.is-link:hover {
          color: #1890ff;
        }
      }

      .el-breadcrumb__item:last-child .el-breadcrumb__inner {
        color: #262626;
        font-weight: 500;
      }
    }
  }

  .page-content-wrapper {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    
    /* Fade Transform Animation */
    .fade-transform-leave-active,
    .fade-transform-enter-active {
      transition: all 0.3s;
    }

    .fade-transform-enter-from {
      opacity: 0;
      transform: translateX(-20px);
    }

    .fade-transform-leave-to {
      opacity: 0;
      transform: translateX(20px);
    }
  }
}

/* Custom Dropdown Styles */
.dropdown-flag {
  margin-right: 8px;
  font-size: 16px;
}

.logout-item {
  color: #ff4d4f !important;
  
  &:hover {
    background-color: #fff1f0 !important;
    color: #ff4d4f !important;
  }
}
</style>
