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
    Une API view qui permet d'afficher et créer des projets liés à un utilisateur authentifié.

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

            Une réponse HTTP 200 OK avec les titres des projets de l'utilisateur créé.
            Si l'utilisateur n'est pas authentifié, une réponse HTTP 401 Unauthorized.
            Si le projet n'existe pas, une réponse HTTP 404 Not Found est renvoyée.
        """

        user = request.user
        try:
            projects = []
            contributors = Contributor.objects.filter(user=user)
            projects.extend(contributor.project for contributor in contributors)
            created_projects = Project.objects.filter(author_user=user)
            projects.extend(created_projects)
            project_titles = [project.title for project in projects]
            return Response(project_titles, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"message": "Le projet n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Crée un nouveau projet.

        Args:
            request: L'objet HttpRequest.
        Returns:
            Une réponse HTTP 200 OK avec le projet créé ou une réponse HTTP 400 Bad Request.
            Si l'utilisateur n'est pas authentifié, une réponse HTTP 401 Unauthorized.
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
            Une réponse HTTP 200 OK avec les détails du projet
            Si l'utilisateur n'est pas l'auteur du projet, une réponse HTTP 401 Unauthorized
            Si le projet n'existe pas, une réponse HTTP 404 Not Found est renvoyée.
        """

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous ne faites pas parti(e) du projet ."},
                                status=status.HTTP_401_UNAUTHORIZED)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"message": "Le projet n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        """
        Met à jour le projet avec l'ID spécifié

        Args :
            request: L'objet HttpRequest.
            project_id: L'ID du projet à mettre à jour.

        Returns:
            Une réponse HTTP 200 OK avec les données mises à jour en cas de succès ou une réponse HTTP 400 Bad Request
            avec les erreurs de validation en cas d'échec.
            Si l'utilisateur n'est pas l'auteur du projet, une réponse HTTP 401 Unauthorized
            Si le projet n'existe pas, une réponse HTTP 404 Not Found est renvoyée.
        """

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du projet."},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Project.DoesNotExist:
            return Response({"message": "Le projet n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        """
        Supprime le projet avec l'ID spécifié.

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet à supprimer.

        Returns:
            Une réponse HTTP 204 no content indiquant que le projet a été supprimé.
            Si l'utilisateur n'est pas l'auteur du projet, une réponse HTTP 401 Unauthorized
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
            return Response({"message": "Le projet n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
