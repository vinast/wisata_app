from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan Login Kembali Untuk Melanjutkan.")
            return redirect(f"{reverse('wisata:login_admin')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper



def role_required(allowed_roles=None, check_own_user_id=False, user_id_kwarg='user_id'):
    """
    Decorator untuk membatasi akses berdasarkan role dan optional cek kepemilikan user_id.
    
    allowed_roles: list/tuple of role strings yang boleh akses, e.g. ['super_admin', 'admin_prov']
    check_own_user_id: jika True, cek apakah user_id dari URL sama dengan user yang login.
    user_id_kwarg: nama parameter URL yang berisi user_id, default 'user_id'
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            # Jika user bukan authenticated
            if not user.is_authenticated:
                messages.warning(request, "Silakan Login Kembali Untuk Melanjutkan.")
                return redirect(f"{reverse('wisata:login_admin')}?next={request.path}")

            # super_admin boleh akses semua tanpa batasan
            if user.role == 'super_admin':
                return view_func(request, *args, **kwargs)

            # cek role apakah di allowed_roles
            if user.role not in allowed_roles:
                messages.error(request, "Anda tidak memiliki izin mengakses halaman ini.")
                return redirect('wisata:index_user')  # bisa arahkan ke halaman lain sesuai kebutuhan

            # Jika cek kepemilikan user_id diperlukan
            if check_own_user_id:
                user_id = kwargs.get(user_id_kwarg)
                if not user_id or str(user_id) != str(user.user_id):
                    messages.error(request, "Anda hanya dapat mengakses data Anda sendiri.")
                    return redirect('wisata:index_user')

            # Jika lolos semua cek, akses diperbolehkan
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
