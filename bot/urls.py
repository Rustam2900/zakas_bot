from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserListCreateView,
    MandatoryUserListCreateView,
    ImageListCreateView,
    CreateUserView,
    NameRole,
    ImageDetailView,
    Video,
    VideoListCreateView,
    VideoDetailView,
    OrderVideoListView
)

router = DefaultRouter()
router.register(r'roles', NameRole, basename='role')

urlpatterns = [
    #for user
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('mandatory-users/', MandatoryUserListCreateView.as_view(), name='mandatory-user-list-create'),
    #for image
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    #for video
    path('video/', VideoListCreateView.as_view(), name='videos'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('ordervideo/', OrderVideoListView.as_view(), name='ordervideo'),
]

urlpatterns += router.urls
