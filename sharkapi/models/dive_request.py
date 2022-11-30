from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class DiveRequest(models.Model):
    diver = models.ForeignKey(
        "Diver", on_delete=models.CASCADE, related_name="diver")
    dive_site = models.ForeignKey(
        "DiveSite", on_delete=models.CASCADE, related_name="site")
    date = models.DateField(auto_now=False, auto_now_add=False)
    certification = models.ForeignKey(
        "Certification", on_delete=models.CASCADE, related_name="cert")
    comments = models.TextField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_comments = models.TextField(
        max_length=500, null=True, blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
