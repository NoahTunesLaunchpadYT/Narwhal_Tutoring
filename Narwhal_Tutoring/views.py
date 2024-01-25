from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib import messages


# Create your views here.
def index(request):
    tutors = User.objects.all()

    for tutor in tutors:
        username = tutor.username
        pfp_url = f"{username}.png"
        # Check if the image file exists
        pfp_path = finders.find(f'images/{pfp_url}')
        print(f"Generated path for {username}: {pfp_path}")
        if pfp_path:
            tutor.pfp_url = pfp_url
        else:
            # Set default pfp_url if the file doesn't exist
            tutor.pfp_url = 'default.png'
        tutor.save()

    return render(request, "Narwhal_Tutoring/index.html", {
        "tutors": tutors
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Narwhal_Tutoring/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Narwhal_Tutoring/login.html")
    


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Narwhal_Tutoring/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)

            # Check if the image file exists before setting pfp_url
            pfp_url = f"{username}.png"
            # Check if the image file exists
            pfp_path = finders.find(f'images/{pfp_url}')
            print(f"Generated path for {username}: {pfp_path}")
            if pfp_path:
                user.pfp_url = pfp_url
            else:
                # Set default pfp_url if the file doesn't exist
                user.pfp_url = 'default.png'
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Narwhal_Tutoring/register.html")
    
def about(request):
    return render(request, "Narwhal_Tutoring/about.html")

def contact(request):
    return render(request, "Narwhal_Tutoring/contact.html")

def tutors(request):
    tutors = User.objects.all()
    return render(request, "Narwhal_Tutoring/tutors.html", {
        "tutors": tutors
    })

def tos(request):
    return render(request, "Narwhal_Tutoring/tos.html")

# views.py
from django.shortcuts import render, redirect
from .models import User, Subject

def dashboard(request):
    subjects = Subject.objects.all()
    times = TimeSlot.objects.all()
    user = request.user

    try:
        availability = user.availability
    except:
        availability = TutorAvailability(tutor=user)
        availability.save()

    if request.method == 'POST':
        # Extract form data from request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        atar = request.POST.get('atar')
        suburb = request.POST.get('suburb')
        selected_subject_ids = request.POST.getlist('subjects')
        description = request.POST.get('description')
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        available = 'available' in request.POST  # Checkbox handling

        # Update the current user instance with the form data
        user.username = username
        user.email = email
        user.address = address
        user.mobile = mobile
        user.atar = atar
        user.suburb = suburb
        user.subjects.set(selected_subject_ids)
        user.description = description
        user.university = university
        user.degree = degree
        user.available = available

        # Save the user instance
        try:
            user.save()
            messages.success(request, 'Profile information updated successfully.')
        except IntegrityError:
            messages.error(request, 'Username already taken.', extra_tags='danger')

        return HttpResponseRedirect(reverse("dashboard"))  # Redirect to the dashboard after successful submission

    return render(request, "Narwhal_Tutoring/dashboard.html", {
        "subjects": subjects,
        "times": times
    })

def submit_timetable(request):
    if request.method == 'POST':
        user = request.user
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        times = TimeSlot.objects.all()
        available_times = []

        for day in days:
            for time in times:
                if request.POST.get(f'{day}-{time}') == 'true':
                    available_times.append(time.id)

            print(f"{user.availability.times[day]}")
            getattr(user.availability, f'{day}_times').set(available_times)
            available_times = []
        
        user.save()

        messages.success(request, 'Timetable updated successfully.')
        return HttpResponseRedirect(reverse("dashboard"))