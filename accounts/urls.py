from django.urls import path
from . import views

urlpatterns = [
    path('invite/', views.validate_invite, name='validate_invite'),
    path('register/', views.register, name='register'),
]
