from http.client import HTTPException

from monitoring.contributors.models import Contributor
from monitoring.contributors.serializers import ContributorSerializer
from monitoring.permissions import IsContributor
from monitoring.projects.models import Project
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ContributorProjectAPIView(APIView):
    """
    APIView pour les opérations liées aux contributeurs d'un projet.

    Les utilisateurs qui ne sont pas contributeurs ne peuvent pas effectuer les actions dans cette vue.

    Attributes:
        permission_classes (list): Les classes de permissions pour les utilisateurs qui effectuent les actions.
    """

    permission_classes = [IsContributor]

    def post(self, request, project_id):
        """
        Crée un nouveau contributeur pour le projet avec l'ID donné.

        Les auteurs du projet sont les seuls utilisateurs autorisés à ajouter des contributeurs à un projet.

        Args:
            request (Request): La requête HTTP pour créer un nouveau contributeur.
            project_id (int): L'ID du projet pour lequel le contributeur sera créé.

        Returns:
            Response: Une réponse HTTP contenant les données JSON du contributeur créé avec un code de statut 201
            CREATED si les données de requête sont valides. Sinon, retourne une réponse avec un code de statut 400 BAD
            REQUEST.

        """

        project = Project.objects.get(project=project_id)
        if project.author_user != request.user:
            return Response({"message": "Vous n'êtes pas l'auteur du projet."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ContributorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):
        """
        Récupère les noms des contributeurs pour le projet avec l'ID donné.

        Args:
            request (Request): La requête HTTP pour récupérer les noms des contributeurs.
            project_id (int): L'ID du projet pour lequel les noms des contributeurs seront récupérés.

        Returns:
            Response: Une réponse HTTP contenant une liste de noms de contributeurs sous forme de données JSON
                      avec un code de statut 200 OK si les données sont trouvées. Sinon, retourne une réponse avec
                      un code de statut 404 NOT FOUND.

        """

        try:
            contributors = Contributor.objects.filter(project=project_id)
            contributor_last_names = [contributor.user.last_name for contributor in contributors]
            return Response(contributor_last_names, status=status.HTTP_200_OK)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteContributorProjectAPIView(APIView):
    """Classe pour supprimer un collaborateur d'un projet.

    Cette classe permet de supprimer un collaborateur d'un projet en envoyant une requête DELETE.

    Attributes:
        Aucun attribut.
    """

    def delete(self, request, project_id, user_id):
        """Supprime un collaborateur d'un projet.

        Cette méthode supprime le collaborateur spécifié du projet spécifié.

        Args:
            request (Request): L'objet Request Django pour cette requête.
            project_id (int): L'ID du projet à partir duquel supprimer le collaborateur.
            user_id (int): L'ID de l'utilisateur à supprimer du projet.

        Returns:
            Response: Un objet Response Django indiquant si la suppression a réussi ou non.

        """

        try:
            project = Project.objects.get(project=project_id)
            if project.author_user != request.user:
                raise HTTPException({"message": "Vous n'êtes pas assigné pour supprimer un contributeur."})
            contributor = Contributor.objects.get(project_id=project_id, user_id=user_id)
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contributor.DoesNotExist:
            return Response({"message": "Le contributeur n'existe pas."}, status=status.HTTP_404_NOT_FOUND)


