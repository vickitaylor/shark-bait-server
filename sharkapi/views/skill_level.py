from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Lower

from sharkapi.models import SkillLevel
from sharkapi.serializers import SkillLevelSerializer


class SkillLevelView(ViewSet):
    """ Shark Bait Certification View """

    def list(self, request):
        """ Handles the GET request, to get all skill levels from the database, sorted in ascending order by name.

        Returns:
            Response: JSON serialized list of skill levels
        """

        skill_level = SkillLevel.objects.all().order_by(Lower("skill"))
        serializer = SkillLevelSerializer(skill_level, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
