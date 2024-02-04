from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib import messages
import json
from django.utils.timezone import make_aware
from datetime import datetime
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def checkout(request):
    return render(request, 'checkout.html')

@csrf_exempt
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1OfoEqKCFeavPzHiIZflECLS',
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

def success(request):
    return HttpResponse("Success")

def cancel(request):
    return HttpResponse("Cancel")

# Create your views here.
def index(request):
    tutors = User.objects.filter(tutor=True)

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
            return redirect(request.GET.get('next', 'index'))
        else:
            return render(request, "Narwhal_Tutoring/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Narwhal_Tutoring/login.html")
    


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', 'index'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        student1_name = request.POST.get("student1_name", "")
        student2_name = request.POST.get("student2_name", "")
        student3_name = request.POST.get("student3_name", "")
        address = request.POST["address"]
        mobile = request.POST.get('mobile')

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

            # Set additional fields
            user.student1_name = student1_name
            user.student2_name = student2_name
            user.student3_name = student3_name
            user.address = address
            user.mobile = mobile

            # Check if the image file exists before setting pfp_url
            pfp_url = f"{username}.png"
            pfp_path = finders.find(f'images/{pfp_url}')
            if pfp_path:
                user.pfp_url = pfp_url
            else:
                user.pfp_url = 'default.png'

            user.save()
        except IntegrityError:
            return render(request, "Narwhal_Tutoring/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect(request.GET.get('next', 'index'))
    else:
        return render(request, "Narwhal_Tutoring/register.html")
    
def about(request):
    return render(request, "Narwhal_Tutoring/about.html")

def contact(request):
    return render(request, "Narwhal_Tutoring/contact.html")

def tutors(request):
    tutors = User.objects.filter(tutor=True)

    primary_school_subjects = Subject.objects.filter(type="Primary School")
    high_school_subjects = Subject.objects.filter(type="High School")
    atar_subjects = Subject.objects.filter(type="ATAR")

    return render(request, "Narwhal_Tutoring/tutors.html", {
        "tutors": tutors,
        "primary_school_subjects": primary_school_subjects,
        "high_school_subjects": high_school_subjects,
        "atar_subjects": atar_subjects
    })

def tos(request):
    return render(request, "Narwhal_Tutoring/tos.html")

# views.py
from django.shortcuts import render, redirect
from .models import User, Subject

@login_required(login_url='login')
def dashboard(request):
    subjects = Subject.objects.all()
    times = TimeSlot.objects.all()
    user = request.user

    try:
        availability = user.availability
    except TutorAvailability.DoesNotExist:
        availability = TutorAvailability(tutor=user)
        availability.save()

    if request.method == 'POST':
        # Extract form data from request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        # Common fields for both tutor and non-tutor users
        user.username = username
        user.email = email
        user.mobile = mobile

        if user.tutor:
            # Tutor-specific fields
            atar = request.POST.get('atar')
            suburb = request.POST.get('suburb')
            selected_subject_ids = request.POST.getlist('subjects')
            description = request.POST.get('description')
            university = request.POST.get('university')
            degree = request.POST.get('degree')

            user.atar = atar
            user.suburb = suburb
            user.subjects.set(selected_subject_ids)
            user.description = description
            user.university = university
            user.degree = degree
        else:
            # Non-tutor-specific fields
            address = request.POST.get('address')
            student1_name = request.POST.get('student1_name')
            student2_name = request.POST.get('student2_name')
            student3_name = request.POST.get('student3_name')

            user.address = address
            user.student1_name = student1_name
            user.student2_name = student2_name
            user.student3_name = student3_name

        # Save the user instance
        try:
            user.save()
            messages.success(request, 'Profile information updated successfully.')
        except IntegrityError:
            messages.error(request, 'Username already taken.', extra_tags='danger')

        return HttpResponseRedirect(reverse("dashboard"))  # Redirect to the dashboard after successful submission

    return render(request, "Narwhal_Tutoring/dashboard.html", {
        "subjects": subjects,
        "times": times,
        "user": user,
    })
    
def tutor(request, tutor_id):
    times = TimeSlot.objects.all()
    tutors = User.objects.filter(tutor=True)
    
    try:
        tutor = tutors.get(id=tutor_id)
        return render(request, "Narwhal_Tutoring/tutor.html", {
            'tutor': tutor,
            'times': times
        })
    except:
        messages.error(request, f'{tutor_id} is not a tutor.', extra_tags='danger')
        return render(request, "Narwhal_Tutoring/tutor.html")

def save_availability(request):
    if request.method == 'POST':
        print("Posted")
        try:
            data = json.loads(request.body)
            
            # Extracting data from the request
            title = data.get('title', 'Availability')  # Default title if not provided
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            day_of_week = data.get('daysOfWeek', [])[0]  # Assuming daysOfWeek is an array
            group_id = data.get('groupId', '0')  # Default group_id if not provided
            event_id = data.get('id', '0')
            
            # Assuming the logged-in user is the tutor
            tutor = request.user

            print('startTime:')
            print(data.get('startTime'))

            
            # Create and save the Availability instance
            availability = Availability.objects.create(
                tutor=tutor,
                title=title,
                start_time=start_time,
                end_time=end_time,
                group_id=group_id,
                event_id=event_id,
                day_of_week=day_of_week,
            )

            print(f'Start Time: {start_time}')
            print(f'End Time: {end_time}')
            
            return JsonResponse({'message': 'Event saved successfully'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

def delete_availability(request, event_id):
    if request.method == 'DELETE':
        try:
            availability = Availability.objects.get(event_id=event_id)

            # Check if the tutor deleting the availability is the owner of the availability
            if availability.tutor == request.user:
                availability.delete()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        except Availability.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Availability not found'}, status=404)

def get_availability(request, tutor_id):
    if request.method == 'GET':
        # Assuming the logged-in user is the tutor
        tutor = User.objects.get(id=tutor_id)

        # Fetch availability events for the tutor
        availability_events = Availability.objects.filter(tutor=tutor)

        # Convert events to a format suitable for FullCalendar
        events = []
        for availability in availability_events:

            
            events.append({
                'id': availability.event_id,
                'title': availability.title,
                'startTime': availability.start_time,
                'endTime': availability.end_time, 
                'groupId': availability.group_id,
                'daysOfWeek': [availability.day_of_week],
            })

            '''            
            events.append({
                'title': 'Recurring Event',
                'groupId': 'test',
                'daysOfWeek': [availability.day_of_week],
                'startTime': availability.start_time,
                'endTime': availability.end_time, 
            })'''


            print(availability.group_id)
            print(f'Start Time: {availability.start_time}')
            print(f'End Time: {availability.end_time}')

        return JsonResponse(events, safe=False)

def update_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            available = data.get('available', False)

            # Update the user's availability (replace this with your actual logic)
            request.user.available = available
            request.user.save()

            return JsonResponse({'message': 'Availability updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)