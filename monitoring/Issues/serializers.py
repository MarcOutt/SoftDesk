
from monitoring.Issues.models import Issue
from monitoring.projects.models import Project
from rest_framework import serializers


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('title', 'desc', 'tag', 'priority', 'status', 'author_user',
                  'assignee_user')

    def create(self, validated_data):
        return Issue.objects.create(title=validated_data['title'],
                                    desc=validated_data['desc'],
                                    tag=validated_data['tag'],
                                    priority=validated_data['priority'],
                                    project=self.validate_project_id(),
                                    status=validated_data['status'],
                                    author_user=validated_data['author_user'],
                                    assignee_user=validated_data['assignee_user']
                                    )

    def validate_project_id(self):
        project_id = self.context['request'].parser_context['kwargs']['project_id']
        return Project.objects.get(pk=project_id)