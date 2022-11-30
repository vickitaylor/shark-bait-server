from django.db import models


class DiveSite(models.Model):
    name = models.TextField(max_length=150)
    price = models.PositiveIntegerField(default=0)
    depth = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1000)
    picture_url = models.TextField(max_length=150)
    fun_facts = models.TextField(max_length=1000)
    will_see = models.TextField(max_length=500)
