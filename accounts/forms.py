from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InviteValidationForm(forms.Form):
    code = forms.CharField(
        max_length=100,
        label="Invite Code",
        widget=forms.TextInput(attrs={'placeholder': 'Paste your invite code here'})
    )

class RegisterWithInviteForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
