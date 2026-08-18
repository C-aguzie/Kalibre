from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import InviteCode
from .forms import InviteValidationForm, RegisterWithInviteForm
from .emails import send_welcome_email
from scheduling.models import Booking
import uuid

def validate_invite(request):
    form = InviteValidationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        raw_code = form.cleaned_data['code'].strip()
        try:
            code_uuid = uuid.UUID(raw_code)
            invite = InviteCode.objects.get(code=code_uuid)
            if invite.is_valid():
                request.session['invite_code'] = str(invite.code)
                return redirect('register')
            elif invite.is_used:
                messages.error(request, "This invite code has already been used.")
            else:
                messages.error(request, "This invite code has expired.")
        except (InviteCode.DoesNotExist, ValueError):
            messages.error(request, "Invalid invite code.")
    return render(request, 'accounts/validate_invite.html', {'form': form})


def register(request):
    invite_code = request.session.get('invite_code')
    if not invite_code:
        messages.error(request, "You need a valid invite code to register.")
        return redirect('validate_invite')

    try:
        invite = InviteCode.objects.get(code=invite_code)
        if not invite.is_valid():
            messages.error(request, "Your invite code is no longer valid.")
            return redirect('validate_invite')
    except InviteCode.DoesNotExist:
        return redirect('validate_invite')

    form = RegisterWithInviteForm(request.POST or None, initial={'email': invite.email})
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        invite.is_used = True
        invite.save()
        if 'invite_code' in request.session:
            del request.session['invite_code']
        login(request, user)
        try:
            send_welcome_email(user)
        except Exception as e:
            print(f"Email failed: {e}")
        messages.success(request, f"Welcome, {user.username}! Check your email for confirmation.")
        return redirect('dashboard')

    return render(request, 'accounts/register.html', {'form': form, 'invite': invite})


def dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    total = bookings.count()
    return render(request, 'scheduling/dashboard.html', {
        'bookings': bookings,
        'total': total,
    })
