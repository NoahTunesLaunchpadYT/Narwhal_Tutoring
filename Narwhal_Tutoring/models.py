from django.contrib.auth.models import AbstractUser
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    # Either Primary School, Highschool, or ATAR
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type} {self.name}"

class User(AbstractUser):

    student1_name = models.CharField(max_length=100, null=True, blank=True)
    student2_name = models.CharField(max_length=100, null=True, blank=True)
    student3_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    tutor = models.BooleanField(default=False)

    # Tutors Only
    mobile = models.CharField(max_length=15, null=True, blank=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors", blank=True)
    atar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    available = models.BooleanField(default=True, blank=True)
    pfp_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"

class Availability(models.Model):
    tutor = models.ForeignKey(User, related_name="availability", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    start_time = models.CharField(max_length=20)  # Adjust the max length as needed
    end_time = models.CharField(max_length=20)    # Adjust the max length as needed
    event_id = models.IntegerField()
    day_of_week = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.start_time}"

class TimeSlot(models.Model):
    time = models.IntegerField()

    def __str__(self):
        return f"{self.time}"
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
 
class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
    
