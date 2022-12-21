from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from sharkapi.models import DiveSite, Diver
from sharkapi.serializers import DiveSiteSerializer
from django.db.models.functions import Lower


class DiveSiteTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'diveSites', 'divers', 'skillLevels']

    def setUp(self):
        self.diver = Diver.objects.first()
        token = Token.objects.get(user=self.diver.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_site(self):
        """Create site level test"""
        url = "/sites"

        site = {
            "name": "test",
            "price": 120,
            "depth": 40,
            "description": "test",
            "picture_url": "test.jpg",
            "fun_facts": "test",
            "will_see": "test"
        }

        response = self.client.post(url, site, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        new_site = DiveSite.objects.last()

        expected = DiveSiteSerializer(new_site)

        self.assertEqual(expected.data, response.data)

    def test_get_site(self):
        """Get Dive Site Test
        """
        site = DiveSite.objects.first()

        url = f'/sites/{site.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = DiveSiteSerializer(site)

        self.assertEqual(expected.data, response.data)

    def test_list_site(self):
        """Test list method for dive sites"""
        url = "/sites"

        response = self.client.get(url)

        all_sites = DiveSite.objects.all().order_by(Lower("name"))
        expected = DiveSiteSerializer(all_sites, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_site(self):
        """test update for dive sites"""

        site = DiveSite.objects.first()

        url = f'/sites/{site.id}'

        updated_site = {
            "name": f'{site.name} updated',
            "price": site.price,
            "depth": site.depth,
            "description": site.description,
            "picture_url": site.picture_url,
            "fun_facts": site.fun_facts,
            "will_see": site.will_see
        }

        response = self.client.put(url, updated_site, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        site.refresh_from_db()

        self.assertEqual(updated_site['name'], site.name)

    def test_delete_site(self):
        """Test delete method for dive sites"""
        site = DiveSite.objects.first()

        url = f'/sites/{site.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
