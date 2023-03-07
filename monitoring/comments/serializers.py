from monitoring.Issues.models import Issue
from monitoring.comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('description', 'author_user')

    def create(self, validated_data):
        return Comment.objects.create(description=validated_data['description'],
                                      author_user=validated_data['author_user'],
                                      issue=self.validate_issue_id()
                                      )

    def validate_issue_id(self):
        issue_id = self.context['request'].parser_context['kwargs']['issue_id']
        return Issue.objects.get(pk=issue_id)
