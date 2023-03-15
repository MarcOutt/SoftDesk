from monitoring.contributors.models import Contributor
from monitoring.projects.models import Project
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour la classe Contributor.

    Convertit les objets Contributor en données JSON et vice versa.

    Attributes:
        user (int): L'ID de l'utilisateur qui contribue au projet.
        permission (str): Les permissions accordées à l'utilisateur.
        role (str): Le rôle de l'utilisateur dans le projet.
    """

    class Meta:
        model = Contributor
        fields = ('id', 'user', 'permission', 'role')

    def create(self, validated_data):
        """
        Crée un nouvel objet Contributor.

        Crée un nouvel objet Contributor avec les données validées fournies.
        Renvoie l'objet Contributor créé.

        Args:
            validated_data (dict): Les données validées pour créer un nouvel objet Contributor.

        Returns:
            Contributor: L'objet Contributor créé.

        """

        return Contributor.objects.create(user=validated_data['user'],
                                          project=self.validate_project_id(),
                                          permission=validated_data['permission'],
                                          role=validated_data['role'])

    def validate_project_id(self):
        """
        Valide l'ID du projet.

        Valide et renvoie l'objet Project correspondant à l'ID du projet fourni dans le contexte de la requête.

        Returns:
            Project: L'objet Project correspondant à l'ID du projet fourni dans le contexte de la requête.

        Raises:
            Project.DoesNotExist: Si aucun projet correspondant n'est trouvé.

        """

        project_id = self.context['request'].parser_context['kwargs']['project_id']
        return Project.objects.get(pk=project_id)
