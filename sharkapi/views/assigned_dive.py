from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import AssignedDive
from sharkapi.serializers import AssignedDiveSerializer


class AssignedDiveView(ViewSet):
    """ Shark Bait Assigned Dive View """

    def list(self, request):
        """ Handles the GET request, to get all assigned dives from the database, sorted in ascending order by date.

        Returns:
            Response: JSON serialized list of Assigned Dives
        """

        AssignedDives = AssignedDive.objects.all().order_by("dive_request__date")
        serializer = AssignedDiveSerializer(AssignedDives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
