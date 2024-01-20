from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.conf import settings
import os
from django.contrib.staticfiles import finders


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
        except IntegrityError as e:
            return render(request, "Narwhal_Tutoring/register.html", {
                "message": e
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Narwhal_Tutoring/register.html")