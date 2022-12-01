from rest_framework import serializers
from sharkapi.models import SkillLevel


class SkillLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillLevel
        fields = ('id', 'skill')
