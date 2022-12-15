from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from sharkapi.models import SkillLevel, Diver
from sharkapi.serializers import SkillLevelSerializer
from django.db.models.functions import Lower


class SkillTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'skillLevels', 'divers']

    def setUp(self):
        self.diver = Diver.objects.first()
        token = Token.objects.get(user=self.diver.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_skill(self):
        """Create skill level test"""
        url = "/skill"

        level = {
            "skill": "Ehh..."
        }

        response = self.client.post(url, level, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        new_skill = SkillLevel.objects.last()

        expected = SkillLevelSerializer(new_skill)

        self.assertEqual(expected.data, response.data)

    def test_get_skill(self):
        """Get Skill level Test
        """
        skill = SkillLevel.objects.first()

        url = f'/skill/{skill.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = SkillLevelSerializer(skill)

        self.assertEqual(expected.data, response.data)

    def test_list_skill(self):
        """Test list skill levels"""
        url = "/skill"

        response = self.client.get(url)

        all_skills = SkillLevel.objects.all().order_by(Lower("skill"))
        expected = SkillLevelSerializer(all_skills, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_skill(self):
        """test update skill levels"""

        skill = SkillLevel.objects.first()

        url = f'/skill/{skill.id}'

        updated_skill = {
            "skill": f'{skill.skill} changed'
        }

        response = self.client.put(url, updated_skill, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        skill.refresh_from_db()

        self.assertEqual(updated_skill['skill'], skill.skill)

    def test_delete_skill(self):
        """Test delete skill level"""
        skill = SkillLevel.objects.first()

        url = f'/skill/{skill.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
