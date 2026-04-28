import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 静态导入常用组件来避免动态导入问题
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Layout from '@/layout/index.vue'
import ProjectList from '@/views/projects/ProjectList.vue'

/** @type {import('vue-router').RouteRecordRaw[]} */
const routes = [
  {
    path: '/',
    redirect: '/ai-intelligent-mode/projects'
  },
  {
    path: '/home',
    redirect: '/ai-intelligent-mode/projects'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/ai-intelligent-mode',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: 'projects'
      },
      {
        path: 'projects',
        name: 'Projects',
        component: ProjectList
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/projects/ProjectDetail.vue')
      },
      {
        path: 'requirement-analysis',
        name: 'RequirementAnalysis',
        component: () => import('@/views/requirement-analysis/RequirementAnalysisView.vue')
      },
      {
        path: 'testcases',
        name: 'TestCases',
        component: () => import('@/views/testcases/TestCaseList.vue')
      },
      {
        path: 'testcases/create',
        name: 'CreateTestCase',
        component: () => import('@/views/testcases/TestCaseForm.vue')
      },
      {
        path: 'testcases/:id',
        name: 'TestCaseDetail',
        component: () => import('@/views/testcases/TestCaseDetail.vue')
      },
      {
        path: 'testcases/:id/edit',
        name: 'EditTestCase',
        component: () => import('@/views/testcases/TestCaseEdit.vue')
      },
      {
        path: 'testing',
        name: 'AITesting',
        component: () => import('@/views/ai-intelligent-mode/testing/AITesting.vue')
      },
      {
        path: 'cases',
        name: 'AICaseList',
        component: () => import('@/views/ai-intelligent-mode/testing/AICaseList.vue')
      },
      {
        path: 'execution-records',
        name: 'AIExecutionRecords',
        component: () => import('@/views/ai-intelligent-mode/testing/AIExecutionRecords.vue')
      },
      {
        path: 'versions',
        name: 'Versions',
        component: () => import('@/views/versions/VersionList.vue')
      },
      {
        path: 'reviews',
        name: 'Reviews',
        component: () => import('@/views/reviews/ReviewList.vue')
      },
      {
        path: 'reviews/create',
        name: 'CreateReview',
        component: () => import('@/views/reviews/ReviewForm.vue')
      },
      {
        path: 'reviews/:id',
        name: 'ReviewDetail',
        component: () => import('@/views/reviews/ReviewDetail.vue')
      },
      {
        path: 'reviews/:id/edit',
        name: 'EditReview',
        component: () => import('@/views/reviews/ReviewForm.vue')
      },
      {
        path: 'review-templates',
        name: 'ReviewTemplates',
        component: () => import('@/views/reviews/ReviewTemplateList.vue')
      },
      {
        path: 'testsuites',
        name: 'TestSuites',
        component: () => import('@/views/testsuites/TestSuiteList.vue')
      },
      {
        path: 'executions',
        name: 'Executions',
        component: () => import('@/views/executions/ExecutionListView.vue')
      },
      {
        path: 'executions/:id',
        name: 'ExecutionDetail',
        component: () => import('@/views/executions/ExecutionDetailView.vue')
      },
      {
        path: 'reports',
        name: 'AiTestReport',
        component: () => import('@/views/reports/AiTestReport.vue')
      },
      {
        path: 'generated-testcases',
        name: 'GeneratedTestCases',
        component: () => import('@/views/requirement-analysis/GeneratedTestCaseList.vue')
      },
      {
        path: 'task-detail/:taskId',
        name: 'TaskDetail',
        component: () => import('@/views/requirement-analysis/TaskDetail.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/UserProfile.vue')
      },
      {
        path: 'exploration',
        name: 'SystemExploration',
        component: () => import('@/views/ai-intelligent-mode/AISystemExploration.vue')
      },
      {
        path: 'work-results',
        name: 'AIWorkResults',
        component: () => import('@/views/ai-intelligent-mode/AIWorkResults.vue')
      }
    ]
  },
  {
    path: '/configuration',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'ai-model',
        name: 'AiModelConfig',
        component: () => import('@/views/configuration/AIIntelligentModeConfig.vue')
      },
      {
        path: 'prompt-config',
        name: 'PromptConfig',
        component: () => import('@/views/configuration/ConfigurationCenter.vue')
      },
      {
        path: 'generation-config',
        name: 'GenerationConfig',
        component: () => import('@/views/configuration/ConfigurationCenter.vue')
      },
      {
        path: 'ui-env',
        name: 'UiEnvConfig',
        component: () => import('@/views/configuration/UIEnvironmentConfig.vue')
      },
      {
        path: 'app-env',
        name: 'AppEnvConfig',
        component: () => import('@/views/configuration/ConfigurationCenter.vue')
      },
      {
        path: 'ai-mode',
        name: 'AiModeConfig',
        component: () => import('@/views/configuration/ConfigurationCenter.vue')
      },
      {
        path: 'scheduled-task',
        name: 'ScheduledTaskConfig',
        component: () => import('@/views/configuration/ConfigurationCenter.vue')
      },
      {
        path: 'dify',
        name: 'DifyConfig',
        component: () => import('@/views/configuration/DifyConfig.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 只在应用初始化或从登录页面导航时初始化认证
  if (!userStore.user && userStore.accessToken) {
    try {
      await userStore.initAuth()
    } catch (error) {
      console.error('认证初始化失败:', error)
    }
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && userStore.isAuthenticated) {
    next('/ai-intelligent-mode/projects')
  } else {
    next()
  }
})

export default router
