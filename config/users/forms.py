import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile  # Make sure Profile model has `phone_number`


class ForgotUsernameForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email")

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        help_texts = {
            'username': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    
    def clean_phone_number(self):
       phone = self.cleaned_data.get('phone_number').strip().replace(" ", "")
       if not re.match(r'^\d{10}$', phone):
        raise forms.ValidationError("Enter a valid 10-digit phone number.")

       phone = '+91' + phone
       if Profile.objects.filter(phone_number=phone).exists():
        raise forms.ValidationError("This phone number is already registered.")
       return phone
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()
            phone = self.cleaned_data.get('phone_number')

            # Ensure profile exists or create it
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = phone  # Save/Update phone number
            profile.save()

        return user