from rest_framework import serializers
from sharkapi.models import DiveSite


class DiveSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiveSite
        fields = ('id', 'name', 'price', 'depth', 'description', 'picture_url', 'fun_facts', 'will_see')
