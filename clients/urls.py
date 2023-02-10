from django.urls import path
from .views import  ClientCreateView, delete_client, ClientsView

app_name = "clients"

urlpatterns = [
    path('clients/', ClientsView.as_view(), name="clients"),
    path('clients/create_new_client', ClientCreateView.as_view(), name='create_new_client'),
    path('clients/delete_client', delete_client, name='delete_client')
]