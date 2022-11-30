from django.db import models
from django.contrib.auth.models import User


class Diver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_level = models.ForeignKey("SkillLevel", on_delete=models.CASCADE, related_name="level")
