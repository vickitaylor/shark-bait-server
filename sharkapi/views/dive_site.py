from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import DiveSite
from sharkapi.serializers import DiveSiteSerializer


class DiveSiteView(ViewSet):
    """ Shark Bait DiveSite View """

    def list(self, request):
        """ Handles the GET request, to get all divesites from the database, sorted in ascending order by name.

        Returns:
            Response: JSON serialized list of diveSites
        """

        diveSites = DiveSite.objects.all().order_by("name")
        serializer = DiveSiteSerializer(diveSites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
