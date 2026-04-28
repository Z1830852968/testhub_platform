import re

with open('frontend/src/router/index.js', 'r') as f:
    content = f.read()

# Replace missing config components with placeholder or ConfigurationCenter since we don't have them
content = content.replace("() => import('@/views/configuration/PromptConfig.vue')", "() => import('@/views/configuration/ConfigurationCenter.vue')")
content = content.replace("() => import('@/views/configuration/GenerationConfig.vue')", "() => import('@/views/configuration/ConfigurationCenter.vue')")
content = content.replace("() => import('@/views/configuration/APPEnvironmentConfig.vue')", "() => import('@/views/configuration/ConfigurationCenter.vue')")
content = content.replace("() => import('@/views/configuration/AiModeConfig.vue')", "() => import('@/views/configuration/ConfigurationCenter.vue')")
content = content.replace("() => import('@/views/configuration/ScheduledTaskConfig.vue')", "() => import('@/views/configuration/ConfigurationCenter.vue')")

with open('frontend/src/router/index.js', 'w') as f:
    f.write(content)

