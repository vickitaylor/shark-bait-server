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

        diveRequests = DiveRequest.objects.all().order_by("date")
        serializer = DiveRequestSerializer(diveRequests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
