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

    def retrieve(self, request, pk):
        """ Handles the GET request to a single skill level, if the selected key is not found 404 is returned

        Returns:
            Response:JSON serialized list of the skill level for the selected key
        """

        try:
            skill = SkillLevel.objects.get(pk=pk)
            serializer = SkillLevelSerializer(skill)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SkillLevel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ Is the POST to create a new skill level

        Returns:
            Response: JSON serialized skill level instance
        """

        skill = SkillLevel.objects.create(
            skill=request.data["skill"]
        )

        serializer = SkillLevelSerializer(skill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """ Handles the PUT request for the selected skill level. 

        Returns:
            Response: Empty body with a 204 status code
        """

        skill_level = SkillLevel.objects.get(pk=pk)

        skill_level.skill = request.data["skill"]

        skill_level.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles the delete request for a skill level
        """

        skill = SkillLevel.objects.get(pk=pk)
        skill.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
