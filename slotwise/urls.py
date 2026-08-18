from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from scheduling import views as scheduling_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', account_views.dashboard, name='dashboard'),
    path('', scheduling_views.home, name='home'),
    path('services/', scheduling_views.services, name='services'),
    path('about/', scheduling_views.about, name='about'),
    path('contact/', scheduling_views.contact, name='contact'),
    path('booking/', scheduling_views.booking, name='booking'),
    path('booking/success/', scheduling_views.booking_success, name='booking_success'),
]
