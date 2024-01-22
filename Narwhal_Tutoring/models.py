from django.contrib.auth.models import AbstractUser
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    tutor = models.BooleanField(default=False)

    # Tutors Only
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    suburb = models.CharField(max_length=100, null=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors")
    atar = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    university = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=100, null=True)
    available = models.BooleanField(default=False)
    pfp_url = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.username}"
