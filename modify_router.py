import re

with open('frontend/src/router/index.js', 'r') as f:
    content = f.read()

# 1. Remove ai-generation
start_idx = content.find("  {\n    path: '/ai-generation/assistant',")
end_idx = content.find("  {\n    path: '/api-testing',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 2. Remove api-testing
start_idx = content.find("  {\n    path: '/api-testing',")
end_idx = content.find("  {\n    path: '/ui-automation',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 3. Remove ui-automation
start_idx = content.find("  {\n    path: '/ui-automation',")
end_idx = content.find("  {\n    path: '/app-automation',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 4. Remove app-automation
start_idx = content.find("  {\n    path: '/app-automation',")
end_idx = content.find("  {\n    path: '/ai-intelligent-mode',")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 5. We need to add exploration and work-results to ai-intelligent-mode
# Wait, instead of hardcoding the entire ai-intelligent-mode block, we can just insert the two routes at the end of its children array.
insert_pos = content.find("      {\n        path: 'profile',\n        name: 'Profile',\n        component: () => import('@/views/profile/UserProfile.vue')\n      }\n    ]\n  },")

if insert_pos != -1:
    new_routes = """      {
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
  },"""
    content = content[:insert_pos] + new_routes + content[insert_pos + len("      {\n        path: 'profile',\n        name: 'Profile',\n        component: () => import('@/views/profile/UserProfile.vue')\n      }\n    ]\n  },"):]

with open('frontend/src/router/index.js', 'w') as f:
    f.write(content)

