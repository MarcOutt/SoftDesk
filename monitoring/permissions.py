from monitoring.projects.models import Project
from rest_framework.permissions import BasePermission


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            project_id = view.kwargs.get('project_id')
            project = Project.objects.get(project=project_id)
            print(request.user, project.author_user)
            return bool(request.user.contributors.filter(project_id=project_id).exists() or
                        project.author_user == request.user)
