from http.client import HTTPException

from monitoring.Issues.models import Issue
from monitoring.Issues.serializers import IssueSerializer
from monitoring.permissions import IsContributor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class IssueProjectAPIView(APIView):
    """
    Vue API pour les `Issue` associées à un projet spécifique.

    Attributes:
        permission_classes (list): Liste de classes de permission qui spécifient les permissions
            requises pour accéder à cette vue.
    """

    permission_classes = [IsContributor]

    def post(self, request, project_id):
        """
        Crée une nouvelle instance de `Issue` associée au projet spécifié.

        Args:
            request (HttpRequest): L'objet de requête HTTP.
            project_id (int): L'ID du projet associé à l'Issue.

        Returns:
            Response: La réponse HTTP contenant les données de l'Issue créée,
                ou une réponse d'erreur si les données fournies ne sont pas valides.
        """
        serializer = IssueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):
        """
        Récupère toutes les instances de `Issue` associées au projet spécifié.

        Args:
            request (HttpRequest): L'objet de requête HTTP.
            project_id (int): L'ID du projet associé aux 'Issue'.

        Returns:
            Response: La réponse HTTP contenant les données de toutes les `Issue` associées
                au projet spécifié, ou une réponse d'erreur si aucun `Issue` n'a été trouvé
                pour ce projet.
        """
        try:
            issues = Issue.objects.filter(project=project_id)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IssueUpdateDeleteAPIView(APIView):
    """
    Une API view qui permet à un contributeur de mettre à jour et supprimer un problème pour un projet spécifié.
    """
    permission_classes = [IsContributor]

    def put(self, request, project_id, issue_id):
        """
        Met à jour un problème pour un projet spécifié. Le contributeur doit être l'auteur du problème pour effectuer
        cette action.

        Args:
            request: L'objet Request Django.
            project_id: L'identifiant du projet auquel le problème appartient.
            issue_id: L'identifiant du problème à mettre à jour.

        Returns:
            Une réponse HTTP 200 OK avec les données mises à jour en cas de succès ou une réponse HTTP 400 Bad Request
            avec les erreurs de validation en cas d'échec.
            Si le contributeur n'est pas l'auteur du problème, une réponse HTTP 401 Unauthorized
            Si le problème n'existe pas, une réponse HTTP 404 Not Found est renvoyée.

        """
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
        """
        Supprime un problème pour un projet spécifié. Le contributeur doit être l'auteur du problème pour effectuer
        cette action.

        Args:
            request: L'objet Request Django.
            project_id: L'identifiant du projet auquel le problème appartient.
            issue_id: L'identifiant du problème à supprimer.

        Returns:
            Une réponse HTTP 204 No Content si le problème est supprimé avec succès ou une réponse HTTP 401 Unauthorized
            si le contributeur n'est pas l'auteur du problème.
            Si le problème n'existe pas, une réponse HTTP 404 Not Found est renvoyée.

        Raises:
            HTTPException: Si le contributeur n'est pas l'auteur du problème
        """
        try:
            issue = Issue.objects.get(project=project_id, id=issue_id)
            if issue.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du problème."},
                                status=status.HTTP_401_UNAUTHORIZED)
            issue.delete()
            return Response({"message": "Le problème a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        except Issue.DoesNotExist:
            return Response({"message": "Le problème n'existe pas."}, status=status.HTTP_404_NOT_FOUND)