from monitoring.Issues.models import Issue
from monitoring.comments.models import Comment
from monitoring.comments.serializers import CommentSerializer
from monitoring.permissions import IsContributor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CommentIssueAPIView(APIView):

    permission_classes = [IsContributor]

    def post(self, request, project_id, issue_id):
        issue = Issue.objects.get(id=issue_id)
        if issue.assignee_user != request.user:
            return Response({"message": "Vous n'êtes pas assigné pour créer un commentaire sur ce problème."},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id):

        try:
            comments = Comment.objects.filter(issue=issue_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentReadUpdateDeleteAPIView(APIView):

    permission_classes = [IsContributor]

    def get(self, request, project_id, issue_id, comment_id):

        try:
            comment = Comment.objects.get(issue=issue_id, comment=comment_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id, issue_id, comment_id):

        try:
            comment = Comment.objects.get(issue=issue_id, comment=comment_id)
            if comment.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du commentaire."},
                                status=status.HTTP_401_UNAUTHORIZED)
        except comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):

        try:
            comment = Comment.objects.get(issue=issue_id, comment=comment_id)
            if comment.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du commentaire."},
                                status=status.HTTP_401_UNAUTHORIZED)
            comment.delete()
            return Response({"message": "Le commentaire a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)