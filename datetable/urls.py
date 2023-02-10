from django.urls import path
from .views import datetable_view, days_view, ajax_get_clients_projects

app_name = "datetable"

urlpatterns = [
    path('datetable/', datetable_view, name="datetable"),
    path('datetable/days', days_view, name="days"),
    path('datetable/days/ajax_get_clients_projects', ajax_get_clients_projects, name="ajax_get_clients_projects")
]