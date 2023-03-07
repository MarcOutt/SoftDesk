from monitoring.projects.models import Project
from monitoring.projects.serializers import ProjectSerializer
from user.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectAPIView(APIView):
    """
    API View permettant de récupérer les projets d'un utilisateur et de créer un nouveau projet.

    Cette vue utilise une requête GET pour récupérer tous les projets créés par l'utilisateur authentifié.
    Une requête POST est utilisée pour créer un nouveau projet en utilisant les informations fournies dans la requête.

    Attributes:
        Aucun attribut de classe n'est utilisé.

    Methods:
        - get(request): Récupère tous les projets d'un utilisateur.
        - post(request): Crée un nouveau projet.

    """

    def get(self, request):
        """
        Récupère tous les projets d'un utilisateur.

        Récupère tous les projets créés par l'utilisateur authentifié en utilisant une requête GET.
        Les projets récupérés sont sérialisés et renvoyés dans une réponse HTTP 200 OK.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.

        Returns:
            Response: Une réponse HTTP contenant la liste des projets de l'utilisateur authentifié sous forme
            sérialisée.
            Si aucun projet n'est trouvé pour l'utilisateur, renvoie une réponse HTTP 204 NO CONTENT

        """
        try:
            user = request.user
            project_title = Project.objects.filter(author_user=user).values_list('title', flat=True)
            return Response(project_title, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Crée un nouveau projet.

        Crée un nouveau projet en utilisant les informations fournies dans la requête POST.
        Si les informations sont valides, un nouveau projet est créé et une réponse HTTP 201 CREATED
        est renvoyée. Sinon, une réponse HTTP 400 BAD REQUEST est renvoyée avec un message d'erreur.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.

        Returns:
            Response: Une réponse HTTP avec un code de statut approprié en fonction du résultat de la tentative de
            création du projet.
            Si le projet est créé avec succès, renvoie une réponse HTTP 201 CREATED. Si les informations fournies
            sont invalides, renvoie une réponse HTTP 400 BAD REQUEST avec un message d'erreur.

        """
        print(request.user)
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectReadUpdateDeleteAPIView(APIView):
    """
    Une vue qui implémente les actions de récupération (GET), de mise à jour (PUT) et de suppression (DELETE)
    d'un projet.

    Attributes:
        None

    Methods:
        get(project_id):
            Récupère un projet.

        put(request, project_id):
            Met à jour un projet.

        delete(project_id):
            Supprime un projet.
    """

    def get(self, request, project_id):
        """
        Récupère un projet.

        Récupère le projet avec l'ID `project_id` et renvoie une réponse HTTP 200 OK avec le projet sérialisé.
        Si le projet n'est pas trouvé, renvoie une réponse HTTP 404 NOT FOUND.

        Args:
            project_id (int): L'ID du projet à récupérer.

        Returns:
            Response: Une réponse HTTP contenant le projet sous forme sérialisée.
            Si le projet n'est pas trouvé, renvoie une réponse HTTP 404 NOT FOUND.

        """

        try:
            project = Project.objects.get(project=project_id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        """
        Met à jour un projet.

        Met à jour le projet avec l'ID `project_id` en utilisant une requête PUT avec les données de la requête.
        Si le projet n'est pas trouvé, renvoie une réponse HTTP 404 NOT FOUND.
        Si les données sont valides, le projet est mis à jour et renvoyé dans une réponse HTTP 200 OK.
        Sinon, renvoie une réponse HTTP 400 BAD REQUEST avec les erreurs de validation.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.
            project_id (int): L'ID du projet à mettre à jour.

        Returns:
            Response: Une réponse HTTP contenant le projet mis à jour sous forme sérialisée.
            Si le projet n'est pas trouvé, renvoie une réponse HTTP 404 NOT FOUND.
            Si les données sont valides, le projet est renvoyé dans une réponse HTTP 200 OK.
            Si les données ne sont pas valides, renvoie une réponse HTTP 400 BAD REQUEST avec les erreurs de
            validation

        """

        try:
            project = Project.objects.get(project=project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        """
        Supprime un projet.

        Supprime le projet avec l'ID `project_id`.
        Si le projet est trouvé et supprimé avec succès, renvoie une réponse HTTP 204 NO CONTENT.
        Sinon, renvoie une réponse HTTP 404 NOT FOUND.

        Args:
            project_id (int): L'ID du projet à supprimer.

        Returns:
            Response: Une réponse HTTP vide (pas de contenu) avec un code de statut HTTP 204 NO CONTENT.
            Si le projet n'est pas trouvé, renvoie une réponse HTTP 404 NOT FOUND.

        """

        try:
            project = Project.objects.get(project=project_id)
            project.delete()
            return Response(content_type={"message": "Le projet a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
