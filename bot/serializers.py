from rest_framework import serializers
from .models import User, MandatoryUser, RolesImage, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'first_name', 'last_name', 'username']


class MandatoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MandatoryUser
        fields = ['chat_id', 'name', 'url', 'channel_id']


class RolesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolesImage
        fields = ['roleimage_mandatory_id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['role_id', 'image']
