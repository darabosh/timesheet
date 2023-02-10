from django.urls import path
from .views import categories_view

app_name = "categories"

urlpatterns = [
    path('categories/', categories_view, name="categories")
]