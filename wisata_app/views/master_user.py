from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from wisata_app.models import Master_User, ROLE_CHOICES
from django.utils import timezone
from wisata_app.decorators import role_required

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class UserViews(View):
    def get(self, request):
        users = Master_User.objects.filter(deleted_at__isnull=True)
        
        if request.user.role == 'super_admin':
            pass
        elif request.user.role == 'admin_prov':
            users = users.exclude(role='super_admin')
        elif request.user.role == 'admin_kab':
            users = users.exclude(role__in=['super_admin', 'admin_prov'])
        else:
            users = users.filter(role='user')

        return render(request, 'backend/master_user/index.html', {
            'user': users,
            'roles': ROLE_CHOICES,
        })


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov']), name='dispatch')
class CreateUserView(View):
    def post(self, request):
        data = request.POST
        try:
            with transaction.atomic():
                if Master_User.objects.filter(email=data['email']).exists():
                    messages.error(request, "Email sudah terdaftar.")
                    return redirect('index_user')

                is_staff_flag = data['role'] in ['admin_prov', 'admin_kab']

                Master_User.objects.create_user(
                    email=data['email'],
                    username=data['username'],
                    phone=data['phone'],
                    role=data['role'],
                    password=data['password'],
                    is_staff=is_staff_flag
                )
                messages.success(request, "User berhasil ditambahkan.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")
        return redirect('wisata:index_user')


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(allowed_roles=['super_admin', 'admin_kab'], check_own_user_id=True), name='dispatch')
class UpdateUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(Master_User, user_id=user_id)
        try:
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.save()
            messages.success(request, "User berhasil diperbarui.")
        except Exception as e:
            messages.error(request, f"Gagal memperbarui user: {e}")
        return redirect('wisata:index_user')


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class DeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(Master_User, user_id=user_id)
        # user.deleted_at = timezone.now()
        # user.save()
        user.delete()
        messages.success(request, "User berhasil dihapus.")
        return redirect('wisata:index_user')
