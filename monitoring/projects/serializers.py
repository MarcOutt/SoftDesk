from monitoring.projects.models import Project
from rest_framework import serializers
from user.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour la classe Project.

    Convertit les objets Project en données JSON et vice versa.

    Attributes:
        title (str): Le titre du projet.
        description (str): La description du projet.
        type (str): Le type du projet.
        author_user (int): L'ID de l'utilisateur qui a créé le projet.
    """

    class Meta:
        model = Project
        fields = ('title', 'description', 'type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Crée un nouvel objet Project.

        Crée un nouvel objet Project avec les données validées fournies.
        Renvoie l'objet Project créé.

        Args:
            validated_data (dict) : Les données validées pour créer un nouvel objet Project.

        Returns:
            Project: L'objet Project créé.

        """

        return Project.objects.create(title=validated_data['title'],
                                      description=validated_data['description'],
                                      type=validated_data['type'],
                                      author_user=self.validate_author_user_id())

    def validate_author_user_id(self):
        """
        Valide l'ID du projet.

        Valide et renvoie l'objet Project correspondant à l'ID du projet fourni dans le contexte de la requête.

        Returns:
            Project: L'objet Project correspondant à l'ID du projet fourni dans le contexte de la requête.

        Raises:
            Project.DoesNotExist: Si aucun projet correspondant n'est trouvé.

        """
        author_user_id = self.context['request'].user.id
        return CustomUser.objects.get(id=author_user_id)
