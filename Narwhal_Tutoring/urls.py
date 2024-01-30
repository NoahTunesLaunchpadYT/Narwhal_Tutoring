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
    path("submit-timetable", views.submit_timetable, name="submit-timetable"),
    path("tutor/<int:tutor_id>", views.tutor, name='tutor'),
    path('save_availability/', views.save_availability, name='save_availability'),
    path('delete_availability/<int:event_id>/', views.delete_availability, name='delete_availability'),
    path('get_availability/', views.get_availability, name='get_availability')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)