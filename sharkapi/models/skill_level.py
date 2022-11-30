from django.db import models


class SkillLevel(models.Model):
    skill = models.TextField(max_length=150)
