import re

with open('frontend/src/router/index.js', 'r') as f:
    content = f.read()

# Remove the old ai-generation block entirely
# Find the start of { path: '/ai-generation/assistant'
start_idx = content.find("  {\n    path: '/ai-generation/assistant',")
end_idx = content.find("  {\n    path: '/api-testing',")
if start_idx != -1 and end_idx != -1:
    ai_gen_content = content[start_idx:end_idx]
    content = content[:start_idx] + content[end_idx:]

# Find the start of ai-intelligent-mode block
start_idx = content.find("  {\n    path: '/ai-intelligent-mode',")
end_idx = content.find("  {\n    path: '/data-factory',")

ai_intel_content = """  {
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
        component: UiAITesting
      },
      {
        path: 'cases',
        name: 'AICaseList',
        component: UiAICaseList
      },
      {
        path: 'execution-records',
        name: 'AIExecutionRecords',
        component: UiAIExecutionRecords
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
"""

content = content[:start_idx] + ai_intel_content + content[end_idx:]

with open('frontend/src/router/index.js', 'w') as f:
    f.write(content)
