from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from wisata_app.models import ROLE_CHOICES, Master_User
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout


class UserViews(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            if request.user.role == 'super_admin':
                users = Master_User.objects.filter(deleted_at__isnull=True)
            elif request.user.role == 'admin_prov':
                users = Master_User.objects.filter(deleted_at__isnull=True).exclude(role='super_admin')
            elif request.user.role == 'admin_kab':
                users = Master_User.objects.filter(deleted_at__isnull=True).exclude(role__in=['super_admin', 'admin_prov'])
            else:
                messages.error(request, "Unauthorized access")
                return redirect('wisata_app:index_home')

            return render(request, 'backend/master_user/index.html', {'users': users})
        except Exception as e:
            messages.error(request, f"Error fetching user list: {e}")
            return redirect('c')


class CreateUserView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'backend/master_user/form.html', {
            'edit': False,
            'roles': [role for role in ROLE_CHOICES if role[0] != 'super_admin'],
        })

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        try:
            with transaction.atomic():
                if Master_User.objects.filter(email=data['email']).exists():
                    messages.error(request, "Email sudah terdaftar")
                    return redirect('ecolota:create_user')

                is_staff_flag = data['role'] in ['admin_prov', 'admin_kab']

                Master_User.objects.create_user(
                    email=data['email'],
                    username=data['username'],
                    phone=data['phone'],
                    role=data['role'],
                    password=data['password'],
                    full_name=data['full_name'],
                    is_staff=is_staff_flag
                )
                messages.success(request, "Akun berhasil ditambahkan.")
                return redirect('wisata_app:index_user')
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")
            return redirect('wisata_app:index_home')



@method_decorator(login_required(), name='dispatch')
class LogoutViews(View):
    def get(self, request):
        logout_message = request.GET.get('logout_message', None)
        if logout_message is not None:
            messages.info(request, logout_message)
        
        logout(request)
        return redirect('wisata_app:index_home')