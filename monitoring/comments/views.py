from monitoring.comments.models import Comment
from monitoring.comments.serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CommentIssueAPIView(APIView):

    def post(self, request, project_id, issue_id):
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

    def get(self, request, project_id, issue_id, comment_id):

        try:
            comments = Comment.objects.get(issue=issue_id, comment=comment_id)
            serializer = CommentSerializer(comments)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id, issue_id, comment_id):

        try:
            comment = Comment.objects.get(issue=issue_id, comment=comment_id)
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
            comment.delete()
            return Response(content_type={"message": "Le commentaire a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)