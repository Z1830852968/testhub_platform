import os

file_path = 'frontend/src/views/ui-automation/ai/AICaseList.vue'
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
    "$t('uiAutomation.ai.caseList.messages.deleteConfirm')": "$t('uiAutomation.ai.caseList.messages.deleteConfirm')"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w') as f:
    f.write(content)

file_path_2 = 'frontend/src/views/ui-automation/ai/AIExecutionRecords.vue'
with open(file_path_2, 'r') as f:
    content_2 = f.read()

replacements_2 = {
    "$t('uiAutomation.common.description')": "$t('project.description')",
    "$t('uiAutomation.common.createTime')": "$t('project.createdAt')",
    "$t('uiAutomation.common.operation')": "$t('project.actions')",
    "$t('uiAutomation.common.run')": "'执行'",
    "$t('uiAutomation.common.view')": "$t('common.view')",
    "$t('uiAutomation.common.delete')": "$t('common.delete')"
}

for old, new in replacements_2.items():
    content_2 = content_2.replace(old, new)

with open(file_path_2, 'w') as f:
    f.write(content_2)
