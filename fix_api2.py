import re

file_path = 'frontend/src/views/ui-automation/ai/AICaseList.vue'
with open(file_path, 'r') as f:
    content = f.read()

import_block = """import {
  getProjects,
  getAICaseList,
  createAICase,
  updateAICase,
  deleteAICase,
  batchDeleteAICases,
  executeAICase
} from '@/api/ui_automation'"""

replacement = """import api from '@/utils/api'

const getProjects = (params) => api.get('/projects/', { params })
const getAICaseList = (params) => api.get('/ui-automation/ai/cases/', { params })
const createAICase = (data) => api.post('/ui-automation/ai/cases/', data)
const updateAICase = (id, data) => api.put(`/ui-automation/ai/cases/${id}/`, data)
const deleteAICase = (id) => api.delete(`/ui-automation/ai/cases/${id}/`)
const batchDeleteAICases = (data) => api.post('/ui-automation/ai/cases/batch_delete/', data)
const executeAICase = (id) => api.post(`/ui-automation/ai/cases/${id}/execute/`)
"""

content = content.replace(import_block, replacement)
with open(file_path, 'w') as f:
    f.write(content)

file_path2 = 'frontend/src/views/ui-automation/ai/AIExecutionRecords.vue'
with open(file_path2, 'r') as f:
    content2 = f.read()

import_block2 = """import {
  getProjects,
  getAIExecutionRecords,
  deleteAIExecutionRecord,
  batchDeleteAIExecutionRecords
} from '@/api/ui_automation'"""

replacement2 = """import api from '@/utils/api'

const getProjects = (params) => api.get('/projects/', { params })
const getAIExecutionRecords = (params) => api.get('/ui-automation/ai/execution-records/', { params })
const deleteAIExecutionRecord = (id) => api.delete(`/ui-automation/ai/execution-records/${id}/`)
const batchDeleteAIExecutionRecords = (data) => api.post('/ui-automation/ai/execution-records/batch_delete/', data)
"""

content2 = content2.replace(import_block2, replacement2)
with open(file_path2, 'w') as f:
    f.write(content2)

