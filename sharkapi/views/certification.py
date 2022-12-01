from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from sharkapi.models import Certification
from sharkapi.serializers import CertificationSerializer


class CertificationView(ViewSet):
    """ Shark Bait Certification View """

    def list(self, request):
        """ Handles the GET request, to get all certifications from the database, sorted in ascending order by name.

        Returns:
            Response: JSON serialized list of certifications
        """

        certifications = Certification.objects.all().order_by("depth")
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
