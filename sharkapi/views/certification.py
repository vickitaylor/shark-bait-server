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

    def retrieve(self, request, pk):
        """ Handles the GET request to a single certification, if the selected key is not found 404 is returned

        Returns:
            Response:JSON serialized list of the certification for the selected key
        """

        try:
            certification = Certification.objects.get(pk=pk)
            serializer = CertificationSerializer(certification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Certification.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ Is the POST to create a new certification 

        Returns:
            Response: JSON serialized certification instance
        """

        cert = Certification.objects.create(
            depth=request.data["depth"]
        )

        serializer = CertificationSerializer(cert)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
