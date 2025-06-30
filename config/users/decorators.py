from django.shortcuts import redirect

def otp_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('otp_verified'):
            return view_func(request, *args, **kwargs)
        return redirect('login')  # or redirect to 'verify_otp' page
    return wrapper
