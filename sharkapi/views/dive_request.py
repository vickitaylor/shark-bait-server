from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import DiveRequest
from sharkapi.serializers import DiveRequestSerializer


class DiveRequestView(ViewSet):
    """ Shark Bait Dive Request View """

    def list(self, request):
        """ Handles the GET request, to get all dive requests from the database, sorted in ascending order by date.

        Returns:
            Response: JSON serialized list of dive requests
        """

        dive_requests = DiveRequest.objects.all().order_by("date")
        serializer = DiveRequestSerializer(dive_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ Handles the GET request to a single dive request, if the selected key is not found 404 is returned

        Returns:
            Response:JSON serialized list of the dive request for the selected key
        """

        try:
            request = DiveRequest.objects.get(pk=pk)
            serializer = DiveRequestSerializer(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DiveRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
