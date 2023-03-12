from django.db import models
from monitoring.projects.models import Project
from user.models import CustomUser


class Contributor(models.Model):
    choice = [
        ('Oui', True),
        ('Non', False)
    ]

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=5, choices=choice)
    role = models.CharField(max_length=128)
