from monitoring.permissions import IsContributor
from monitoring.projects.models import Project
from monitoring.projects.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            project_title = Project.objects.filter(author_user=user).values_list('title', flat=True)
            return Response(project_title, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectReadUpdateDeleteAPIView(APIView):

    permission_classes = [IsContributor]

    def get(self, request, project_id):

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous ne faites pas parti du projet ."}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."}, status=status.HTTP_401_UNAUTHORIZED)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."}, status=status.HTTP_401_UNAUTHORIZED)
            project.delete()
            return Response({"message": "Le projet a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
