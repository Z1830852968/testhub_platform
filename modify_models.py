import re

with open('apps/requirement_analysis/models.py', 'r') as f:
    content = f.read()

# Update ROLE_CHOICES
content = content.replace("('reviewer', '测试评审专家'),\n        ('browser_use_text', 'Browser Use - 文本模式'),", "('reviewer', '测试评审专家'),\n        ('browser_use_text', 'Browser Use - 文本模式'),\n        ('explorer', 'AI网页探索专家'),")

with open('apps/requirement_analysis/models.py', 'w') as f:
    f.write(content)

with open('apps/explorations/models.py', 'r') as f:
    exp_content = f.read()

# Add fields to ExplorationRun
run_fields = """    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='exploration_runs')
    base_url = models.URLField(blank=True, null=True)
    auth_type = models.CharField(max_length=20, default='none')
    auth_username = models.CharField(max_length=100, blank=True, null=True)
    auth_password = models.CharField(max_length=100, blank=True, null=True)
    max_steps = models.IntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')"""

exp_content = exp_content.replace("    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='exploration_runs')\n    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')", run_fields)

with open('apps/explorations/models.py', 'w') as f:
    f.write(exp_content)
