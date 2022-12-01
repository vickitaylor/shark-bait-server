from rest_framework import serializers
from django.contrib.auth.models import User

from sharkapi.models import Diver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_staff')

class DiverSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    class Meta:
        model = Diver
        fields = ('id', 'user', 'skill_level')