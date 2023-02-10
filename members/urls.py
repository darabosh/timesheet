from django.urls import path
from .views import members_view, MemberCreateView, delete_member

app_name = "members"

urlpatterns = [
    path('members/', members_view, name="members"),
    path('members/create_new_member', MemberCreateView.as_view(), name='create_new_member'),
    path('members/delete_member', delete_member, name='delete_member')
]