from django.db import models
from apps.projects.models import Project

class ExplorationRun(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('stopped', 'Stopped'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='exploration_runs')
    base_url = models.URLField(blank=True, null=True)
    auth_type = models.CharField(max_length=20, default='none')
    auth_username = models.CharField(max_length=100, blank=True, null=True)
    auth_password = models.CharField(max_length=100, blank=True, null=True)
    max_steps = models.IntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exploration_run'
        ordering = ['-created_at']

class FeatureItem(models.Model):
    run = models.ForeignKey(ExplorationRun, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=1000, blank=True)
    screenshot_url = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exploration_feature_item'
        ordering = ['created_at']

class ExplorationArtifact(models.Model):
    run = models.ForeignKey(ExplorationRun, on_delete=models.CASCADE, related_name='artifacts')
    name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=1000)
    artifact_type = models.CharField(max_length=50) # e.g., 'screenshot', 'log'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exploration_artifact'
        ordering = ['created_at']
