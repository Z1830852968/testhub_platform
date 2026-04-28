import os

file_path = 'frontend/src/views/ai-intelligent-mode/testing/AICaseList.vue'
with open(file_path, 'r') as f:
    content = f.read()

replacements = {
    "$t('uiAutomation.common.description')": "$t('project.description')",
    "$t('uiAutomation.common.createTime')": "$t('project.createdAt')",
    "$t('uiAutomation.common.operation')": "$t('project.actions')",
    "$t('uiAutomation.common.run')": "'执行'",
    "$t('uiAutomation.common.edit')": "$t('common.edit')",
    "$t('uiAutomation.common.delete')": "$t('common.delete')",
    "$t('uiAutomation.common.cancel')": "$t('common.cancel')",
    "$t('uiAutomation.common.save')": "$t('common.save')",
    "$t('uiAutomation.ai.caseNamePlaceholder')": "'请输入用例名称'",
    "$t('uiAutomation.ai.caseDescPlaceholder')": "'请输入用例描述'",
    "$t('uiAutomation.ai.taskPlaceholder')": "$t('uiAutomation.ai.taskPlaceholder')",
    "$t('uiAutomation.ai.caseList.messages.deleteConfirm')": "$t('uiAutomation.ai.caseList.messages.deleteConfirm')",
    "import api from '@/api/ui_automation'": "import api from '@/utils/api'",
    "import {\n  getProjects,\n  getAICaseList,\n  createAICase,\n  updateAICase,\n  deleteAICase,\n  batchDeleteAICases,\n  executeAICase\n} from '@/api/ui_automation'": "import api from '@/utils/api'\n\nconst getProjects = (params) => api.get('/projects/', { params })\nconst getAICaseList = (params) => api.get('/ui-automation/ai/cases/', { params })\nconst createAICase = (data) => api.post('/ui-automation/ai/cases/', data)\nconst updateAICase = (id, data) => api.put(`/ui-automation/ai/cases/${id}/`, data)\nconst deleteAICase = (id) => api.delete(`/ui-automation/ai/cases/${id}/`)\nconst batchDeleteAICases = (data) => api.post('/ui-automation/ai/cases/batch_delete/', data)\nconst executeAICase = (id) => api.post(`/ui-automation/ai/cases/${id}/execute/`)"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w') as f:
    f.write(content)

file_path_2 = 'frontend/src/views/ai-intelligent-mode/testing/AIExecutionRecords.vue'
with open(file_path_2, 'r') as f:
    content_2 = f.read()

replacements_2 = {
    "$t('uiAutomation.common.description')": "$t('project.description')",
    "$t('uiAutomation.common.createTime')": "$t('project.createdAt')",
    "$t('uiAutomation.common.operation')": "$t('project.actions')",
    "$t('uiAutomation.common.run')": "'执行'",
    "$t('uiAutomation.common.view')": "$t('common.view')",
    "$t('uiAutomation.common.delete')": "$t('common.delete')",
    "import api from '@/api/ui_automation'": "import api from '@/utils/api'",
    "import {\n  getProjects,\n  getAIExecutionRecords,\n  deleteAIExecutionRecord,\n  batchDeleteAIExecutionRecords\n} from '@/api/ui_automation'": "import api from '@/utils/api'\n\nconst getProjects = (params) => api.get('/projects/', { params })\nconst getAIExecutionRecords = (params) => api.get('/ui-automation/ai/execution-records/', { params })\nconst deleteAIExecutionRecord = (id) => api.delete(`/ui-automation/ai/execution-records/${id}/`)\nconst batchDeleteAIExecutionRecords = (data) => api.post('/ui-automation/ai/execution-records/batch_delete/', data)"
}

for old, new in replacements_2.items():
    content_2 = content_2.replace(old, new)

with open(file_path_2, 'w') as f:
    f.write(content_2)

file_path_3 = 'frontend/src/views/ai-intelligent-mode/testing/AITesting.vue'
with open(file_path_3, 'r') as f:
    content_3 = f.read()

replacements_3 = {
    "import api from '@/api/ui_automation'": "import api from '@/utils/api'",
    "import {\n  getProjects,\n  getAICaseList,\n  createAITask,\n  getAITaskStatus,\n  getAIExecutionRecordDetail,\n  stopAITask\n} from '@/api/ui_automation'": "import api from '@/utils/api'\n\nconst getProjects = (params) => api.get('/projects/', { params })\nconst getAICaseList = (params) => api.get('/ui-automation/ai/cases/', { params })\nconst createAITask = (data) => api.post('/ui-automation/ai/tasks/', data)\nconst getAITaskStatus = (taskId) => api.get(`/ui-automation/ai/tasks/${taskId}/status/`)\nconst getAIExecutionRecordDetail = (id) => api.get(`/ui-automation/ai/execution-records/${id}/`)\nconst stopAITask = (taskId) => api.post(`/ui-automation/ai/tasks/${taskId}/stop/`)"
}

for old, new in replacements_3.items():
    content_3 = content_3.replace(old, new)

with open(file_path_3, 'w') as f:
    f.write(content_3)

