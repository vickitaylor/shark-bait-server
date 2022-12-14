from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import DiveSite
from sharkapi.serializers import DiveSiteSerializer


class DiveSiteView(ViewSet):
    """ Shark Bait DiveSite View """

    def list(self, request):
        """ Handles the GET request, to get all dive sites from the database, sorted in ascending order by name.

        Returns:
            Response: JSON serialized list of diveSites
        """

        dive_sites = DiveSite.objects.all().order_by("name")
        serializer = DiveSiteSerializer(dive_sites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ Handles the GET request to a single dive site, if the selected key is not found 404 is returned

        Returns:
            Response:JSON serialized list of the dive site for the selected key
        """

        try:
            site = DiveSite.objects.get(pk=pk)
            serializer = DiveSiteSerializer(site)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DiveSite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
