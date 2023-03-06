from monitoring.contributors.models import Contributor
from monitoring.contributors.serializers import ContributorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ContributorProjectAPIView(APIView):

    def post(self, request, project_id):
        serializer = ContributorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):

        try:
            contributors = Contributor.objects.filter(project_id=project_id)
            contributor_last_names = [contributor.user_id.last_name for contributor in contributors]
            return Response(contributor_last_names, status=status.HTTP_200_OK)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteContributorProjectAPIView(APIView):

    def delete(self, request, project_id, user_id):
        try:
            contributor = Contributor.objects.get(project_id=project_id, user_id=user_id)
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


