from monitoring.Issues.models import Issue
from monitoring.comments.models import Comment
from monitoring.comments.serializers import CommentSerializer
from monitoring.permissions import IsContributor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CommentIssueAPIView(APIView):
    """
    APIView pour les opérations de création et de récupération de commentaires liés à un problème spécifié.

    Requiert que l'utilisateur soit contributeur du projet associé au problème.

    """

    permission_classes = [IsContributor]

    def post(self, request, project_id, issue_id):
        """
        Crée un nouveau commentaire pour le problème spécifié.

        Vérifie que l'utilisateur est assigné à la question et valide les données du sérialiseur.
        Crée un nouvel objet Comment avec les données validées fournies.
        Renvoie les données JSON de l'objet Comment créé et un code d'état HTTP 201 si les données sont valides,
        sinon les erreurs de validation et un code d'état HTTP 400.

        Args:
            request (Request): La requête HTTP envoyée par le client.
            project_id (int): L'ID du projet associé à la question.
            issue_id (int): L'ID du problème pour lequel créer un commentaire.

        Returns:
            Response: Les données JSON de l'objet Comment créé et un code d'état HTTP 201 si les données sont valides,
            sinon les erreurs de validation et un code d'état HTTP 400.

        """
        issue = Issue.objects.get(id=issue_id)
        if issue.assignee_user != request.user:
            return Response({"message": "Vous n'êtes pas assigné(e) pour créer un commentaire sur ce problème."},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id):
        """
        Récupère tous les commentaires associés au problème spécifié.

        Récupère tous les objets Comment associés au problème spécifié, il les sérialise et renvoie les données JSON
        des objets Comment et un code d'état HTTP 200 si des commentaires existent pour le problème,
        sinon un code d'état HTTP 404.

        Args:
            request (Request): La requête HTTP envoyée par le client.
            project_id (int): L'ID du projet associé à la question.
            issue_id (int): L'ID du problème pour lequel récupérer les commentaires.

        Returns:
            Response: Les données JSON des objets Comment et un code d'état HTTP 200 si des commentaires existent,
            sinon un code d'état HTTP 404.
        """
        try:
            comments = Comment.objects.filter(issue=issue_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentReadUpdateDeleteAPIView(APIView):
    """
    APIView pour les opérations de récupération, de mise à jour et de suppression de commentaires liés à un problème
    spécifié.

    Requiert que l'utilisateur soit contributeur du projet associé au problème.

    """
    permission_classes = [IsContributor]

    def get(self, request, project_id, issue_id, comment_id):
        """
        Récupère les détails du commentaire spécifié.

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet contenant le commentaire.
            issue_id: L'ID de l'issue contenant le commentaire.
            comment_id: L'ID du commentaire à récupérer.

        Returns:
            Response: La réponse HTTP contenant les détails du commentaire.

        Raises:
            Comment.DoesNotExist: Si aucun commentaire ne correspond à l'ID spécifié.
        """

        try:
            comments = Comment.objects.get(issue=issue_id, comment=comment_id)
            serializer = CommentSerializer(comments)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id, issue_id, comment_id):
        """
        Met à jour le commentaire spécifié.

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet contenant le commentaire.
            issue_id: L'ID de l'issue contenant le commentaire.
            comment_id: L'ID du commentaire à mettre à jour.

        Returns:
            Response: La réponse HTTP contenant les données mises à jour du commentaire.

        Raises:
            Comment.DoesNotExist: Si aucun commentaire ne correspond à l'ID spécifié.
            serializers.ValidationError: Si les données fournies sont invalides.
        """

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
        """
        Supprime le commentaire spécifié.

        Args:
            request: L'objet HttpRequest.
            project_id: L'ID du projet contenant le commentaire.
            issue_id: L'ID de l'issue contenant le commentaire.
            comment_id: L'ID du commentaire à supprimer.

        Returns:
            Response: La réponse HTTP indiquant que le commentaire a été supprimé avec succès.

        Raises:
            Comment.DoesNotExist: Si aucun commentaire ne correspond à l'ID spécifié.
        """

        try:
            comment = Comment.objects.get(issue=issue_id, comment=comment_id)
            if comment.author_user != request.user:
                return Response({"message": "Vous n'êtes pas l'auteur du commentaire."},
                                status=status.HTTP_401_UNAUTHORIZED)
            comment.delete()
            return Response(content_type={"message": "Le commentaire a été supprimé avec succès."},
                            status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
