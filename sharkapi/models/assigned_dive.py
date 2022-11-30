from django.db import models


class AssignedDive(models.Model):
    guide = models.ForeignKey(
        "Diver", on_delete=models.CASCADE, related_name="guide")
    dive_request = models.ForeignKey(
        "DiveRequest", on_delete=models.CASCADE, related_name="request")
