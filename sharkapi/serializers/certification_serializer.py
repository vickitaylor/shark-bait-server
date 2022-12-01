from rest_framework import serializers
from sharkapi.models import Certification


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = ('id', 'depth')
