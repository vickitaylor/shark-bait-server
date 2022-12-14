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

        assigned_dives = AssignedDive.objects.all().order_by("dive_request__date")
        serializer = AssignedDiveSerializer(assigned_dives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk):
        """ Handles the GET request to a single assigned dive, if the selected key is not found 404 is returned

        Returns:
            Response:JSON serialized list of the dive for the selected key
        """

        try:
            assigned_dive = AssignedDive.objects.get(pk=pk)
            serializer = AssignedDiveSerializer(assigned_dive)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AssignedDive.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
