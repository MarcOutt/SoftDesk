from monitoring.contributors.models import Contributor
from monitoring.contributors.serializers import ContributorSerializer
from monitoring.permissions import IsContributor
from monitoring.projects.models import Project
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ContributorProjectAPIView(APIView):

    permission_classes = [IsContributor]

    def post(self, request, project_id):
        project = Project.objects.get(project=project_id)
        if project.author_user != request.user:
            return Response({"message": "Vous n'êtes pas l'auteur du projet."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ContributorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):

        try:
            contributors = Contributor.objects.filter(project=project_id)
            contributor_last_names = [contributor.user.last_name for contributor in contributors]
            return Response(contributor_last_names, status=status.HTTP_200_OK)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteContributorProjectAPIView(APIView):

    def delete(self, request, project_id, user_id):
        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."}, status=status.HTTP_401_UNAUTHORIZED)
            contributor = Contributor.objects.get(project_id=project_id, user_id=user_id)
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


