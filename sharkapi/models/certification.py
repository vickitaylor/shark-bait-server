from django.db import models

class Certification(models.Model):
    depth = models.PositiveIntegerField(default=0)
