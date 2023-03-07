from monitoring.contributors.models import Contributor
from monitoring.projects.models import Project
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('user', 'permission', 'role')

    def create(self, validated_data):
        return Contributor.objects.create(user=validated_data['user'],
                                          project=self.validate_project_id(),
                                          permission=validated_data['permission'],
                                          role=validated_data['role'])

    def validate_project_id(self):
        project_id = self.context['request'].parser_context['kwargs']['project']
        return Project.objects.get(pk=project_id)
