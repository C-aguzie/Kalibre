from django.core.mail import send_mail
from django.conf import settings
import threading

def _send(subject, message, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email error: {e}")

def send_async(subject, message, recipient_list):
    t = threading.Thread(target=_send, args=(subject, message, recipient_list))
    t.daemon = True
    t.start()

def send_welcome_email(user):
    send_async(
        subject='Welcome to Kalibre — Your account is ready',
        message=f'''Hi {user.username},

Your staff account on Kalibre has been created successfully.

You can now log in and manage appointments from your dashboard.

— The Kalibre Team''',
        recipient_list=[user.email],
    )

def send_booking_confirmation(booking):
    send_async(
        subject='Booking Confirmed — Kalibre',
        message=f'''Hi {booking.name},

Thanks for booking with us. Here are your appointment details:

Service: {booking.service}
Date: {booking.date}
Time: {booking.time}

We'll be in touch to confirm your slot. If you need to reschedule, just reply to this email.

— The Kalibre Team''',
        recipient_list=[booking.email],
    )

def send_admin_booking_alert(booking):
    send_async(
        subject=f'New Booking — {booking.name}',
        message=f'''A new booking has been submitted on Kalibre.

Client: {booking.name}
Email: {booking.email}
Service: {booking.service}
Date: {booking.date}
Time: {booking.time}
Notes: {booking.notes or "None"}

Log in to your dashboard to manage this booking.''',
        recipient_list=[settings.EMAIL_HOST_USER],
    )
