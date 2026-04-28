import re

file_path = 'frontend/src/views/ui-automation/ai/AITesting.vue'
with open(file_path, 'r') as f:
    content = f.read()

import_block = """import {
  getProjects,
  getAICaseList,
  createAITask,
  getAITaskStatus,
  getAIExecutionRecordDetail,
  stopAITask
} from '@/api/ui_automation'"""

replacement = """import api from '@/utils/api'

// Define the API functions inline to avoid broken imports
const getProjects = (params) => api.get('/projects/', { params })
const getAICaseList = (params) => api.get('/ui-automation/ai/cases/', { params })
const createAITask = (data) => api.post('/ui-automation/ai/tasks/', data)
const getAITaskStatus = (taskId) => api.get(`/ui-automation/ai/tasks/${taskId}/status/`)
const getAIExecutionRecordDetail = (id) => api.get(`/ui-automation/ai/execution-records/${id}/`)
const stopAITask = (taskId) => api.post(`/ui-automation/ai/tasks/${taskId}/stop/`)
"""

content = content.replace(import_block, replacement)

with open(file_path, 'w') as f:
    f.write(content)

