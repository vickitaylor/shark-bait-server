from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from sharkapi.models import Certification, Diver
from sharkapi.serializers import CertificationSerializer


class CertTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'skillLevels', 'divers', 'certifications']

    def setUp(self):
        # Grab the first certification object from the database and add their token to the headers
        self.diver = Diver.objects.first()
        token = Token.objects.get(user=self.diver.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_cert(self):
        """Create certification test"""
        url = "/certs"

        # Define the certification properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        cert = {
            "depth": 155
        }

        response = self.client.post(url, cert, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # Get the last certification added to the database, it should be the one just created
        new_cert = Certification.objects.last()

        # Since the create method should return the serialized version of the newly created cert,
        # Use the serializer you're using in the create method to serialize the "new_cert"
        # Depending on your code this might be different
        expected = CertificationSerializer(new_cert)

        # Now we can test that the expected output matches what was actually returned
        self.assertEqual(expected.data, response.data)

    def test_get_cert(self):
        """Get Cert Test
        """
        # Grab a certification object from the database
        cert = Certification.objects.first()

        url = f'/certs/{cert.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the cert through the serializer that's being used in view
        expected = CertificationSerializer(cert)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)

    def test_list_certifications(self):
        """Test list certifications"""
        url = '/certs'

        response = self.client.get(url)

        # Get all the certifications in the database and serialize them to get the expected output
        all_certs = Certification.objects.all()
        expected = CertificationSerializer(all_certs, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_cert(self):
        """test update certifications"""
        # Grab the first cert in the database
        cert = Certification.objects.first()

        url = f'/certs/{cert.id}'

        updated_cert = {
            "depth": 200,
        }

        response = self.client.put(url, updated_cert, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the cert object to reflect any changes in the database
        cert.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_cert['depth'], cert.depth)

    def test_delete_cert(self):
        """Test delete certification"""
        cert = Certification.objects.first()

        url = f'/certs/{cert.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the certification
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
