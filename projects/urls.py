from django.urls import path
from .views import projects_view, ProjectCreateView, delete_project

app_name = "projects"

urlpatterns = [
    path('projects/', projects_view, name="projects"),
    path('projects/create_new_project', ProjectCreateView.as_view(), name='create_new_project'),
    path('projects/delete_project', delete_project, name='delete_project')
]