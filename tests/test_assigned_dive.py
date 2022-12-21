from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from sharkapi.models import AssignedDive, Diver
from sharkapi.serializers import AssignedDiveSerializer


class AssignedDiveTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'diveSites', 'divers', 'skillLevels', 'diveRequests', 'certifications', 'assignedDives']

    def setUp(self):
        self.diver = Diver.objects.first()
        token = Token.objects.get(user=self.diver.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_assign(self):
        """Create method for assigned dive test"""
        url = "/assigned"

        assign = {
            "guide": 5,
            "dive_request": 2
        }

        response = self.client.post(url, assign, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        new_assign = AssignedDive.objects.last()

        expected = AssignedDiveSerializer(new_assign)

        self.assertEqual(expected.data, response.data)

    def test_get_assigned(self):
        """Get single assigned dive Test """
        assigned = AssignedDive.objects.first()

        url = f'/assigned/{assigned.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = AssignedDiveSerializer(assigned)

        self.assertEqual(expected.data, response.data)

    def test_list_assigned(self):
        """Test list method for assigned dives"""
        url = "/assigned"

        response = self.client.get(url)

        all_assigned = AssignedDive.objects.all().order_by("dive_request__date")
        expected = AssignedDiveSerializer(all_assigned, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    # def test_change_assigned(self):
    #     """test update method for assigned dive """

    #     assigned = AssignedDive.objects.first()

    #     url = f'/assigned/{assigned.id}'

    #     updated_assignment = {
    #         "guide": assigned.guide,
    #         "dive_request": 1
    #     }

    #     response = self.client.put(url, updated_assignment, format='json')

    #     self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    #     assigned.refresh_from_db()

    #     self.assertEqual(updated_assignment['dive_request'], assigned.dive_request)

    def test_delete_assigned(self):
        """Test delete method for assigned dives"""
        assigned = AssignedDive.objects.first()

        url = f'/assigned/{assigned.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
