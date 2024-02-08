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
    except Availability.DoesNotExist:
        availability = Availability(tutor=user)
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
    tutors = User.objects.filter(tutor=True)
    
    
    try:
        tutor = tutors.get(id=tutor_id)
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        
        context = {
            "product": product,
            "prices": prices,
            'tutor': tutor,
        }

        return render(request, "Narwhal_Tutoring/tutor.html", context)
    except Exception as e:
        messages.error(request, f'{e}', extra_tags='danger')
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
                'display': 'background',
            })

        return JsonResponse(events, safe=False)
    
def get_client_calendar(request):
    if request.method == 'GET':
        user = request.user

        # Fetch events for the tutor
        carts = user.carts.all()

        # Convert events to a format suitable for FullCalendar
        events = []

        for cart in carts:
            for lesson in cart.lessons.all():
                events.append({
                    'id': lesson.event_id,
                    'title': lesson.tutor.username,
                    'groupId': 'booked',
                    'start': lesson.start_time,
                    'end': lesson.end_time, 
                })

        return JsonResponse(events, safe=False)


def get_calendar(request, tutor_id):
    if request.method == 'GET':
        tutor = User.objects.get(id=tutor_id)

        # Fetch events for the tutor
        availability_events = Availability.objects.filter(tutor=tutor)
        lesson_events = tutor.lessons.all()

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
                'display': 'background'
            })

        for lesson in lesson_events:
            if lesson.cart.paid == True:
                events.append({
                    'id': lesson.event_id,
                    'title': 'Booked',
                    'groupId': 'booked',
                    'start': lesson.start_time,
                    'end': lesson.end_time, 
                    'backgroundColor': 'red',
                })

        return JsonResponse(events, safe=False)

def get_availability_and_lessons(request, tutor_id):
    print("Getting availabilities and lessons.")
    if request.method == 'GET':
        tutor = User.objects.get(id=tutor_id)

        # Fetch events for the tutor
        availability_events = Availability.objects.filter(tutor=tutor)
        lesson_events = tutor.lessons.all()

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
                'display': 'background'
            })

        for lesson in lesson_events:
            if lesson.cart.paid == True:
                events.append({
                    'id': lesson.event_id,
                    'title': lesson.cart.user.username,
                    'start': lesson.start_time,
                    'end': lesson.end_time, 
                })

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
    
def create_checkout_session(request):
    user = request.user
    try:
        # Try to get the single cart associated with the user
        cart_instance = user.carts.get(paid=False)
        # Now, cart_instance holds the single Cart instance
    except Cart.DoesNotExist:
        # Handle the case where no cart is found
        print("No cart found for this user.")
    except Cart.MultipleObjectsReturned:
        # Handle the case where multiple carts are found (unexpected)
        print("Multiple carts found for this user. Investigate the data.")

    lessons = cart_instance.lessons.all()
    total_duration = sum((lesson.end_time - lesson.start_time).total_seconds() / 3600 for lesson in lessons)
    

    if total_duration < 5:
        price = Price.objects.get(price=3500)
    elif total_duration < 10:
        price = Price.objects.get(price=3150)
    else:
        price = Price.objects.get(price=3000)
    
    quantity = int(total_duration/0.5)

    if settings.DEBUG:
        domain = "http://127.0.0.1:8000"
    else:
        domain = "https://" + request.get_host()
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price.stripe_price_id,
                'quantity': quantity,
            },
        ],
        mode='payment',
        success_url=domain + f'/success/{cart_instance.id}', #FIX THIS
        cancel_url=domain + '/cancel/',
    )

    # Add a success message if needed
    messages.success(request, "Checkout session created successfully.")

    return redirect(checkout_session.url)

@login_required(login_url='login')
def success(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))

    if cart.user != request.user:
        print("Error: cart user isn't request user")
        return HttpResponseRedirect(reverse('index'))
    
    if cart.paid == True:
        print("Error: cart already paid for")
        message = None
    else:
        message = "Your payment has been successful!"
    
    cart.paid = True
    cart.save()
    
    tutor = cart.lessons.all()[0].tutor

    return render(request, 'Narwhal_Tutoring/success.html', {
        "tutor": tutor,
        "message": message
    })

def cancel(request):
    return render(request, 'Narwhal_Tutoring/cancel.html')

def save_lessons_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        lessons_data = data.get('lessons_data', [])

        tutor_id = data.get('tutorId')
        tutor = User.objects.get(id=tutor_id)

        user = request.user
        Cart.objects.filter(user=user, paid=False).delete()
        cart = Cart.objects.create(user=user, paid=False)

        for lesson_data in lessons_data:
            if lesson_data.get('title') != 'Availability' and lesson_data.get('title') != "Booked":
                Lesson.objects.create(
                    cart=cart,
                    tutor=tutor,
                    name=lesson_data.get('title', 'Lesson'),
                    start_time=lesson_data.get('start'),
                    end_time=lesson_data.get('end'),
                    event_id=lesson_data.get('id', 0)
                )

        lessons = Lesson.objects.filter(tutor=tutor)
        print("Save completed: ")
        print(lessons)

        return JsonResponse({'message': 'Lessons saved to cart successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})