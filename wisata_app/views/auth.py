from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
import re
from wisata_app.models import Master_User as m_user

# Fungsi utilitas untuk validasi email
def is_valid_email(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, value))

class LoginViews(View):
    """Login untuk admin dan cek role user"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('wisata:index_home')
        return render(request, 'backend/login/login.html')

    def post(self, request):
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email_or_username or not password:
            messages.error(request, "Email/Username dan Password tidak boleh kosong.")
            return redirect(reverse('wisata:login_admin'))
        is_email = is_valid_email(email_or_username)
        user = None
        if is_email:
            user = authenticate(request, email=email_or_username, password=password)
        else:
            try:
                user_obj = m_user.objects.get(username=email_or_username, is_active=True)
                if user_obj.check_password(password):
                    user = user_obj
            except m_user.DoesNotExist:
                pass

        if user:
            if user.role not in ['super_admin', 'admin_prov', 'admin_kab']:
                messages.error(request, "ANDA TIDAK MEMILIKI AKSES ADMIN.")
                return redirect(reverse('wisata:login_admin'))
            login(request, user)
            messages.success(request, f"Selamat Datang, {user.username}!")
            next_url = request.GET.get('next', reverse('wisata:index_home'))
            return redirect(next_url)
        messages.error(request, "Login gagal. Periksa email/username dan password Anda.")
        return redirect(reverse('wisata:login_admin'))


@method_decorator(login_required, name='dispatch')
class LogoutViews(View):
    """Logout untuk user"""

    def get(self, request):
        # Cek role user sebelum logout
        user_role = getattr(request.user, 'role', None)
        
        # Pesan logout berdasarkan role user
        if user_role in ['super_admin', 'admin_prov', 'admin_kab']:
            logout_message = f"Admin {request.user.username}, Anda telah berhasil logout."
        else:
            logout_message = f"User {request.user.username}, Anda telah berhasil logout."
        
        # Logout user
        logout(request)
        
        # Tampilkan pesan logout dan redirect ke halaman login
        messages.info(request, logout_message)
        return redirect(reverse('wisata:login_admin'))
