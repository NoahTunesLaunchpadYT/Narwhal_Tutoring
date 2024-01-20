from django.contrib.auth.models import AbstractUser
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

class User(AbstractUser):
    description = models.CharField(max_length=2000, blank=True)
    tutor = models.BooleanField(default=False)

    # Tutors Only
    suburb = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors", blank=True)
    atar = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    available = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.username}"
