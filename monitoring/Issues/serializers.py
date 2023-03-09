
from monitoring.Issues.models import Issue
from monitoring.projects.models import Project
from rest_framework import serializers
from user.models import CustomUser


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle `Issue`. Il sérialise et désérialise les données
    en format JSON, et valide également les données avant de créer une instance
    de `Issue`.

    Attributs:
        Meta (classe): Classe interne qui définit les métadonnées du serializer.
    """

    class Meta:
        """
        Métadonnées du `IssueSerializer`. Il définit le modèle et les champs qui
        doivent être inclus dans la sortie sérialisée.
        """
        model = Issue
        fields = ('title', 'desc', 'tag', 'priority', 'status',
                  'assignee_user')

    def create(self, validated_data):
        """
        Crée et renvoie une nouvelle instance de `Issue` avec les données validées.

        Args:
            validated_data (dict): Un dictionnaire de données validées.

        Returns:
            Issue: Une nouvelle instance du modèle `Issue` avec les données validées.
        """
        return Issue.objects.create(title=validated_data['title'],
                                    desc=validated_data['desc'],
                                    tag=validated_data['tag'],
                                    priority=validated_data['priority'],
                                    project=self.validate_project_id(),
                                    status=validated_data['status'],
                                    author_user=self.validate_author_user_id(),
                                    assignee_user=validated_data['assignee_user'])

    def validate_author_user_id(self):
        """
        Valide l'ID de l'utilisateur auteur.

        Returns:
            CustomUser: L'instance de `CustomUser` qui correspond à l'ID de
                l'utilisateur auteur validé.
        """
        author_user_id = self.context['request'].user.id
        return CustomUser.objects.get(id=author_user_id)

    def validate_project_id(self):
        """
        Valide l'ID du projet.

        Returns:
            Project: L'instance de `Project` qui correspond à l'ID de projet validé.
        """
        project_id = self.context['request'].parser_context['kwargs']['project_id']
        return Project.objects.get(pk=project_id)