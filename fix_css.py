import re

with open('frontend/src/layout/index.vue', 'r') as f:
    content = f.read()

# Let's fix the logo-img css slightly
content = content.replace(".logo-img {\n        height: 32px;\n        margin-right: 12px;\n      }", ".logo-img {\n        height: 40px;\n        object-fit: contain;\n      }")

with open('frontend/src/layout/index.vue', 'w') as f:
    f.write(content)

