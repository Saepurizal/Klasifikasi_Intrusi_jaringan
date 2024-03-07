from django.urls import path
from . import views

urlpatterns = [
    # ... daftar URL lainnya ...
    path('services/', views.services, name='services'),
]