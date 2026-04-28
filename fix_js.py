import re

with open('apps/explorations/tasks.py', 'r') as f:
    content = f.read()

# Make sure the JS extraction logic works correctly
# Right now, it's defined as a multiline string.
# We should probably pass the function to page.evaluate
content = content.replace("JS_EXTRACT_DOM = '''\n() => {", "JS_EXTRACT_DOM = '''\n() => {\n    const results = [];\n    const els = document.querySelectorAll('a, button, input');\n    let counter = 1;\n    for(let el of els) {\n        if(el.offsetWidth === 0 || el.offsetHeight === 0) continue;\n        let text = el.innerText || el.value || el.getAttribute('aria-label') || el.placeholder || el.name || '';\n        text = text.trim().substring(0, 50);\n        if(!text && el.tagName !== 'INPUT') continue;\n        let aiId = 'ai-id-' + counter++;\n        el.setAttribute('data-ai-id', aiId);\n        results.push({id: aiId, tag: el.tagName.toLowerCase(), text: text, type: el.type || '', href: el.href || ''});\n    }\n    return results;\n}\n'''")

with open('apps/explorations/tasks.py', 'w') as f:
    f.write(content)

