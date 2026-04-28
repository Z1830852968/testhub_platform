import re

# settings.py
with open('backend/settings.py', 'r') as f:
    content = f.read()

content = content.replace("    'apps.api_testing',\n", "")
content = content.replace("    'apps.ui_automation',\n", "")
content = content.replace("    'apps.app_automation',\n", "")

with open('backend/settings.py', 'w') as f:
    f.write(content)

# urls.py
with open('backend/urls.py', 'r') as f:
    content = f.read()

content = content.replace("    path('api/api-testing/', include('apps.api_testing.urls')),\n", "")
content = content.replace("    path('api/ui-automation/', include('apps.ui_automation.urls')),\n", "")
content = content.replace("    path('api/app-automation/', include('apps.app_automation.urls')),\n", "")

with open('backend/urls.py', 'w') as f:
    f.write(content)

# asgi.py
with open('backend/asgi.py', 'r') as f:
    content = f.read()

content = content.replace("from apps.app_automation import routing as app_automation_routing\n", "")
content = content.replace("            path('ws/app-automation/', URLRouter(app_automation_routing.websocket_urlpatterns)),\n", "")

with open('backend/asgi.py', 'w') as f:
    f.write(content)

