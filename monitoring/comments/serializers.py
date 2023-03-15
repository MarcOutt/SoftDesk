from monitoring.Issues.models import Issue
from monitoring.comments.models import Comment
from rest_framework import serializers
from user.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour la classe Comment.

    Convertit les objets Comment en données JSON et vice versa.

    Attributs:
        description (str): La description du commentaire.

    """

    class Meta:
        model = Comment
        fields = ('comment', 'description',)

    def create(self, validated_data):
        """
        Crée un nouvel objet Comment.

        Crée un nouvel objet Comment avec les données validées fournies.
        Renvoie l'objet Comment créé.

        Args:
            validated_data (dict): Les données validées pour créer un nouvel objet Comment.

        Returns:
            Comment: L'objet Comment créé.

        """

        return Comment.objects.create(description=validated_data['description'],
                                      author_user=self.validate_author_user_id(),
                                      issue=self.validate_issue_id()
                                      )

    def validate_author_user_id(self):
        """
        Valide l'identifiant de l'utilisateur à partir du contexte du sérialiseur.

        Returns:
            CustomUser: L'instance de l'utilisateur correspondant à l'identifiant de l'utilisateur du contexte.

        Raises:
            serializers.ValidationError: Si l'utilisateur n'est pas authentifié.
        """
        author_user_id = self.context['request'].user.id
        try:
            return CustomUser.objects.get(id=author_user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("L'utilisateur n'est pas authentifié.")

    def validate_issue_id(self):
        """
        Valide l'identifiant de la question à partir du contexte du sérialiseur.

        Returns:
            Issue: L'instance du problème correspondant à l'identifiant du problème du contexte.

        Raises:
            serializers.ValidationError: Si le problème n'existe pas.
        """
        issue_id = self.context['request'].parser_context['kwargs']['issue_id']
        try:
            return Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            raise serializers.ValidationError("Le problème n'existe pas.")
