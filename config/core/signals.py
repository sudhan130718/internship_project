from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def set_otp_verified_for_admin(sender, request, user, **kwargs):
    # Check if this login is via the admin panel
    if request.path.startswith('/admin/'):
        request.session['otp_verified'] = True
        print("Admin login detected. otp_verified =", request.session['otp_verified'])
