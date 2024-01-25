from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("tutors", views.tutors, name='tutors'),
    path("tos", views.tos, name="tos"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("submit-timetable", views.submit_timetable, name="submit-timetable")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)