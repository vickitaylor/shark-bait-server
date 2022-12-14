from rest_framework import serializers
from sharkapi.models import DiveRequest
from sharkapi.serializers import DiverSerializer
from sharkapi.serializers import DiveSiteSerializer


class DiveRequestSerializer(serializers.ModelSerializer):

    diver = DiverSerializer()
    dive_site = DiveSiteSerializer()

    class Meta:
        model = DiveRequest
        fields = ('id', 'diver', 'dive_site', 'date', 'certification', 'comments', 'completed', 'completed_comments', 'rating')
