
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from monitoring.Issues.views import IssueProjectAPIView, IssueUpdateDeleteAPIView
from monitoring.comments.views import CommentIssueAPIView, CommentReadUpdateDeleteAPIView
from monitoring.contributors.views import ContributorProjectAPIView, DeleteContributorProjectAPIView
from monitoring.projects.views import ProjectAPIView, ProjectReadUpdateDeleteAPIView
from rest_framework import permissions
from user.views import UserCreateAPIView, LoginAPIView


schema_view = get_schema_view(
    # Le générateur de schéma à utiliser pour générer la documentation Swagger
    info=openapi.Info(
        title="SoftDesk API",
        default_version='v1',
        description="Une description de mon API",
    ),

    # Les permissions à utiliser pour accéder à la documentation Swagger
    permission_classes=[permissions.AllowAny],

    # Optionnel : les URL des vues à inclure dans la documentation Swagger
    patterns=[
        path('signup/', UserCreateAPIView.as_view(), name='signup'),
        path('login/', LoginAPIView.as_view(), name='login'),
        path('projects/', ProjectAPIView.as_view(), name='project'),
        path('projects/<int:project_id>/', ProjectReadUpdateDeleteAPIView.as_view(), name='rud_project'),
        path('projects/<int:project_id>/', ContributorProjectAPIView.as_view(), name='contributor'),
        path('projects/<int:project_id>/users/<int:user_id>', DeleteContributorProjectAPIView.as_view(),
             name='contributor'),
    ],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/', UserCreateAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),

    path('projects/', ProjectAPIView.as_view(), name='project'),

    path('projects/<int:project_id>/', ProjectReadUpdateDeleteAPIView.as_view(), name='rud_project'),

    path('projects/<int:project_id>/users/', ContributorProjectAPIView.as_view(), name='contributor'),
    path('projects/<int:project_id>/users/<int:user_id>', DeleteContributorProjectAPIView.as_view(),
         name='delete_contributor'),

    path('projects/<int:project_id>/issues/', IssueProjectAPIView.as_view(), name='issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssueUpdateDeleteAPIView.as_view(), name='ud_issue'),

    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentIssueAPIView.as_view(), name='ud_issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/',
         CommentReadUpdateDeleteAPIView.as_view(), name='ud_issue'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
