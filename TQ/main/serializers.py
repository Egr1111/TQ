from rest_framework import serializers

from .models import User

class UserSerializerView(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "invited")
        
class UserSerializerAuth(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")