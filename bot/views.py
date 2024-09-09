from asyncio.log import logger
from rest_framework import generics,viewsets
from .models import User, NameRole, Image, MandatoryUser,Video,OrderVideo
from .serializers import UserSerializer,  ImageSerializer, MandatoryUserSerializer,NameRoleSerializer,VideoSerializer,OrderVideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Received data: {request.data}")
        
        telegram_id = request.data.get('telegram_id')
        username = request.data.get('username')
        
        user = User.objects.filter(telegram_id=telegram_id).first()
        
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
        else:
            serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if not user else status.HTTP_200_OK)
        
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MandatoryUserListCreateView(generics.ListCreateAPIView):
    queryset = MandatoryUser.objects.all()
    serializer_class = MandatoryUserSerializer



class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(APIView):
    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        video = self.get_object(pk)
        return Response({'id': video.id, 'name': video.name, 'video': video.video.url})

class NameRole(viewsets.ModelViewSet):
    queryset = NameRole.objects.all()
    serializer_class = NameRoleSerializer

class ImageDetailView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class OrderVideoListView(generics.ListAPIView):
    queryset = OrderVideo.objects.all()
    serializer_class = OrderVideoSerializer