from django.db import models
from user.models import CustomUser


class Project(models.Model):

    choice_type = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('IOS', 'IOS'),
        ('Android', 'Android')
    ]

    project = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=300, choices=choice_type)
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='projects')