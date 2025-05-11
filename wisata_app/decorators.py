from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan login terlebih dahulu.")
            return redirect(f"{reverse('wisata:login_admin')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper