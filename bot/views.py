from rest_framework import generics
from .models import User, RolesImage, Image, MandatoryUser
from .serializers import UserSerializer, RolesImageSerializer, ImageSerializer, MandatoryUserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MandatoryUserListCreateView(generics.ListCreateAPIView):
    queryset = MandatoryUser.objects.all()
    serializer_class = MandatoryUserSerializer


class RolesImageListCreateView(generics.ListCreateAPIView):
    queryset = RolesImage.objects.all()
    serializer_class = RolesImageSerializer


class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
