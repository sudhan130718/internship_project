from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import rotate_token
import pdb

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             print(" Login successful for:", user)
#             login(request, user)
#             rotate_token(request)

#             if user.is_staff:
#                 print("Redirecting to admin_dashboard")
#                 return redirect('admin_dashboard')
#             else:
#                 print("Redirecting to home")
#                 return redirect('home')
#         else:
#             print(" Form is not valid:", form.errors)
#     else:
#         form = AuthenticationForm()

#     return render(request, 'users/login.html', {'form': form})



from users.utils import send_otp_sms
import random
from django.core.mail import send_mail
def login_view(request):
    show_otp = False
    error_message = ""

    if request.method == 'POST':
        # If OTP is not sent yet → first step
        if not request.session.get('otp_sent'):
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                request.session['user_id'] = user.id

                if user.is_staff:
                    # ✅ Admin login → skip OTP
                    request.session['otp_verified'] = True
                    return redirect('admin_dashboard')

                # 🔐 Regular user → send OTP
                otp = str(random.randint(100000, 999999))
                request.session['otp'] = otp
                request.session['otp_sent'] = True
                request.session['otp_verified'] = False

                phone = user.profile.phone_number
                if not phone.startswith('+'):
                    phone = '+91' + phone
                send_otp_sms(phone, f"Your OTP is {otp}")

                show_otp = True
            else:
                error_message = "Invalid username or password"
                form = AuthenticationForm()
        else:
            # Step 2: OTP Verification
            form = AuthenticationForm()  # Not used in OTP step
            entered_otp = request.POST.get('otp')
            correct_otp = request.session.get('otp')

            if entered_otp == correct_otp:
                request.session['otp_verified'] = True

                # Send confirmation email
                send_mail(
                    subject="Login Successful",
                    message="Wholesale Toy Website: You have logged in successfully.",
                    from_email=None,  # uses DEFAULT_FROM_EMAIL from settings
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

                # Send confirmation SMS
                phone = request.user.profile.phone_number
                if not phone.startswith('+'):
                    phone = '+91' + phone
                send_otp_sms(phone, "Wholesale Toy Website: Logged in successfully.")

                # Clean up
                request.session.pop('otp', None)
                request.session.pop('otp_sent', None)

                return redirect('home')
            else:
                show_otp = True
                error_message = "Invalid OTP"

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {
        'form': form,
        'show_otp': show_otp,
        'error_message': error_message,
    })




def logout_view(request):
    if request.method == 'POST':
        # ✅ Store phone number BEFORE logout
        if request.user.is_authenticated:
            phone = request.user.profile.phone_number
            if not phone.startswith('+'):
                phone = '+91' + phone
        else:
            phone = None

        # 🔒 Logout the user
        logout(request)

        # ✅ Send logout SMS after logout
        if phone:
            send_otp_sms(phone, "Wholesale Toy Website: Logged out successfully.")

        return redirect('login')
    else:
        return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

from .forms import ForgotUsernameForm
from django.contrib import messages
from django.contrib.auth.models import User

def forgot_username_view(request):
    if request.method == 'POST':
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_mail(
                    subject='Your Username',
                    message=f'Hello, your username is: {user.username}',
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Your username has been sent to your email.')
            except User.DoesNotExist:
                messages.error(request, 'No user with this email exists.')
    else:
        form = ForgotUsernameForm()

    return render(request, 'users/forgot_username.html', {'form': form})