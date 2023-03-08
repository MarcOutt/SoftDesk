from monitoring.Issues.models import Issue
from monitoring.Issues.serializers import IssueSerializer
from monitoring.permissions import IsContributor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class IssueProjectAPIView(APIView):

    permission_classes = [IsContributor]

    def post(self, request, project_id):
        serializer = IssueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):

        try:
            issues = Issue.objects.filter(project=project_id)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IssueUpdateDeleteAPIView(APIView):

    permission_classes = [IsContributor]

    def put(self, request, project_id, issue_id):

        try:
            issue = Issue.objects.get(project=project_id, id=issue_id)
            if issue.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du problème."},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):

        try:
            issue = Issue.objects.get(project=project_id, id=issue_id)
            if issue.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du problème."},
                                status=status.HTTP_401_UNAUTHORIZED)
            issue.delete()
            return Response({"message": "Le problème a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)