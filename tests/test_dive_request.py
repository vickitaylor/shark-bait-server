from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from sharkapi.models import DiveRequest, Diver
from sharkapi.serializers import DiveRequestSerializer
from django.db.models.functions import Lower


class DiveRequestTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'diveSites', 'divers', 'skillLevels', 'diveRequests', 'certifications']

    def setUp(self):
        self.diver = Diver.objects.first()
        token = Token.objects.get(user=self.diver.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_request(self):
        """Create method for dive request test"""
        url = "/requests"

        request = {
            "diver": 1,
            "dive_site": 5,
            "date": "2022-12-01",
            "certification": 2,
            "comments": "",
            "completed": False,
            "completed_comments": ""
        }

        response = self.client.post(url, request, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        new_request = DiveRequest.objects.last()

        expected = DiveRequestSerializer(new_request)

        self.assertEqual(expected.data, response.data)

    def test_get_request(self):
        """Get single dive request Test """
        request = DiveRequest.objects.first()

        url = f'/requests/{request.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = DiveRequestSerializer(request)

        self.assertEqual(expected.data, response.data)

    def test_list_request(self):
        """Test list method for dive requests"""
        url = "/requests"

        response = self.client.get(url)

        all_requests = DiveRequest.objects.all().order_by(Lower("date"))
        expected = DiveRequestSerializer(all_requests, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_request(self):
        """test update method for dive """

        request = DiveRequest.objects.first()

        url = f'/requests/{request.id}'

        updated_request = {
            "diver": request.diver.id,
            "dive_site": request.dive_site.id,
            "date": request.date,
            "certification": request.certification.id,
            "comments": request.comments,
            "completed": request.completed,
            "completed_comments": "comments added"
        }

        response = self.client.put(url, updated_request, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        request.refresh_from_db()

        self.assertEqual(updated_request['completed_comments'], request.completed_comments)

    def test_delete_request(self):
        """Test delete method for dive requests"""
        request = DiveRequest.objects.first()

        url = f'/requests/{request.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
