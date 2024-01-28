from django.contrib.auth.models import AbstractUser
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    # Either Primary School, Highschool, or ATAR
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):

    student1_name = models.CharField(max_length=100, null=True)
    student2_name = models.CharField(max_length=100, null=True)
    student3_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)

    tutor = models.BooleanField(default=False)

    # Tutors Only
    mobile = models.CharField(max_length=15, null=True)
    suburb = models.CharField(max_length=100, null=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors", blank=True)
    atar = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    university = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=100, null=True)
    available = models.BooleanField(default=True)
    pfp_url = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.username}"

class TimeSlot(models.Model):
    time = models.IntegerField()

    def __str__(self):
        return f"{self.time}"

class TutorAvailability(models.Model):
    tutor = models.OneToOneField(User, related_name="availability", on_delete=models.CASCADE)

    monday_times = models.ManyToManyField(TimeSlot, related_name="monday")
    tuesday_times = models.ManyToManyField(TimeSlot, related_name="tuesday")
    wednesday_times = models.ManyToManyField(TimeSlot, related_name="wednesday")
    thursday_times = models.ManyToManyField(TimeSlot, related_name="thursday")
    friday_times = models.ManyToManyField(TimeSlot, related_name="friday")
    saturday_times = models.ManyToManyField(TimeSlot, related_name="saturday")
    sunday_times = models.ManyToManyField(TimeSlot, related_name="sunday")

    times = {'monday': monday_times,
             'tuesday': tuesday_times,
             'wednesday': wednesday_times,
             'thursday': thursday_times,
             'friday': friday_times,
             'saturday': saturday_times,
             'sunday': sunday_times
             }
    
    def __str__(self):
        return f"{self.tutor}'s availability"
