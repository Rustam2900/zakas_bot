from django.urls import path
from bot.views import (
    UserListCreateView,
    MandatoryUserListCreateView,
    RolesImageListCreateView,
    ImageListCreateView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),

    path('mandatory-users/', MandatoryUserListCreateView.as_view(), name='mandatory-user-list-create'),

    path('roles-images/', RolesImageListCreateView.as_view(), name='roles-image-list-create'),

    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
]
