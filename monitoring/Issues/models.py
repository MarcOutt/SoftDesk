from django.db import models
from monitoring.projects.models import Project
from user.models import CustomUser


class Issue(models.Model):
    choice_priority = [
        ('HIGHT', 'ELEVEE'),
        ('MEDIUM', 'MOYENNE'),
        ('LOW', 'FAIBLE')
    ]

    choice_tag = [
        ('BUG', 'BUG'),
        ('AMELIORATION', 'IMPROVEMENT'),
        ('TACHE', 'TASK')
    ]

    choice_status = [
        ('A FAIRE', 'TO_DO'),
        ('EN COURS', 'IN_PROGRESS'),
        ('TERMINE', 'DONE')
    ]

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=1000)
    tag = models.CharField(max_length=128, choices=choice_tag)
    priority = models.CharField(max_length=128, choices=choice_priority)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=128, choices=choice_status)
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='issues')
    assignee_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)
