from django.shortcuts import render, redirect
from .models import Booking
from accounts.emails import send_booking_confirmation, send_admin_booking_alert

def home(request):
    return render(request, 'scheduling/home.html')

def services(request):
    return render(request, 'scheduling/services.html')

def about(request):
    return render(request, 'scheduling/about.html')

def contact(request):
    success = False
    if request.method == 'POST':
        success = True
    return render(request, 'scheduling/contact.html', {'success': success})

def booking(request):
    if request.method == 'POST':
        b = Booking.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            service=request.POST.get('service'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            notes=request.POST.get('notes', ''),
        )
        try:
            send_booking_confirmation(b)
            send_admin_booking_alert(b)
        except Exception as e:
            print(f"Email failed: {e}")
        return redirect('booking_success')
    return render(request, 'scheduling/booking.html')

def booking_success(request):
    return render(request, 'scheduling/booking_success.html')
