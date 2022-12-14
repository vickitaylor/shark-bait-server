from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import AssignedDive, DiveRequest, Diver
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

    def create(self, request):
        """ Is the POST to create a new assigned dive for the user

        Returns:
            Response: JSON serialized assigned dive instance
        """

        dive_request = DiveRequest.objects.get(pk=request.data["dive_request"])
        guide = Diver.objects.get(pk=request.data["guide"])

        assigned_dive = AssignedDive.objects.create(
            guide=guide,
            dive_request=dive_request
        )

        serializer = AssignedDiveSerializer(assigned_dive)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handles the delete request for an assigned dive
        """

        assigned = AssignedDive.objects.get(pk=pk)
        assigned.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
