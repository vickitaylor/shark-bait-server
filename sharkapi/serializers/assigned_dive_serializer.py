from rest_framework import serializers
from sharkapi.models import AssignedDive
from sharkapi.serializers import DiverSerializer
from sharkapi.serializers import DiveRequestSerializer


class AssignedDiveSerializer(serializers.ModelSerializer):

    guide = DiverSerializer()
    dive_request = DiveRequestSerializer()

    class Meta:
        model = AssignedDive
        fields = ('id', 'guide', 'dive_request')
