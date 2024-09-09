from rest_framework import serializers
from .models import User, MandatoryUser,NameRole,Image,Video,OrderVideo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'name', 'username']
        extra_kwargs = {
            'name': {'required': False},
            'username': {'required': False}
        }

class MandatoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MandatoryUser
        fields = ['id','chat_id', 'name', 'url', 'channel_id']


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'role_id', 'name', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class NameRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameRole
        fields = ['id', 'name', 'image']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class OrderVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderVideo
        fields = '__all__'