from django.db import models
from monitoring.Issues.models import Issue
from user.models import CustomUser


class Comment(models.Model):
    comment = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    author_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
