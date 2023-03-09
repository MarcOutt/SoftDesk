from http.client import HTTPException

from monitoring.contributors.models import Contributor
from monitoring.permissions import IsContributor
from monitoring.projects.models import Project
from monitoring.projects.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectAPIView(APIView):
    """
    View pour afficher et créer des projets liés à un utilisateur authentifié.

    Permissions (classes) :
        - IsAuthenticated : L'utilisateur doit être authentifié pour accéder à ces vues.

    Attributs de classe :
        - permission_classes : Une liste de classes de permissions qui doivent être satisfaites pour accéder aux vues.

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupère tous les titres de projet associés à l'utilisateur connecté.

        Returns:
            Response: La réponse HTTP contenant les titres des projets de l'utilisateur.
        Raises:
            Project.DoesNotExist: Si aucun projet n'est associé à l'utilisateur connecté.
        """
        user = request.user
        try:
            projects = []
            contributors = Contributor.objects.filter(user=user)
            projects.extend(contributor.project for contributor in contributors)
            created_projects = Project.objects.filter(author_user=user)
            projects.extend(created_projects)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Crée un nouveau projet.

        Args:
            request: L'objet HttpRequest.
        Returns:
            Response: La réponse HTTP contenant les données du nouveau projet créé.
        Raises:
            serializers.ValidationError: Si les données fournies sont invalides.
        """
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectReadUpdateDeleteAPIView(APIView):

    permission_classes = [IsContributor]

    def get(self, request, project_id):
        """
            Récupère les détails du projet avec l'ID spécifié

            Args:
                request: L'objet HttpRequest.
                project_id: L'ID du projet à récupérer.

            Returns:
                Response: La réponse HTTP contenant les détails du projet.

            Raises:
                Project.DoesNotExist: Si aucun projet ne correspond à l'ID spécifié.
                HTTPException: Si l'utilisateur n'est pas autorisé à accéder à ce projet.
        """

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous ne faites pas parti du projet ."}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        """
        Met à jour le projet avec l'ID spécifié

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet à mettre à jour.

        Returns:
            Response: La réponse HTTP contenant les données mises à jour du projet.

        Raises:
            Project.DoesNotExist: Si aucun projet ne correspond à l'ID spécifié.
            HTTPException: Si l'utilisateur n'est pas autorisé à mettre à jour ce projet.
            serializers.ValidationError: Si les données fournies sont invalides.

        """
        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        """
        Supprime le projet avec l'ID spécifié.

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet à supprimer.

        Returns:
            Response: La réponse HTTP indiquant que le projet a été supprimé.
                      Si le projet n'est pas l'auteur du problème, une réponse HTTP 401 Unauthorized
                      Si le projet n'existe pas, une réponse HTTP 404 Not Found est renvoyée.
        """

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."},
                                status=status.HTTP_401_UNAUTHORIZED)
            project.delete()
            return Response({"message": "Le projet a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
