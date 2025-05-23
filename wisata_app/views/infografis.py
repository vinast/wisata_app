from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from ..models import Infografis
from ..decorators import role_required

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class InfografisListViews(View):
    def get(self, request):
        user = request.user
        
        # Super admin can see all infografis
        if user.role == 'super_admin':
            infografis = Infografis.objects.all().order_by('-created_at')
        # Admin kecamatan can only see their own infografis
        elif user.role == 'admin_kab':
            infografis = Infografis.objects.filter(created_by=user).order_by('-created_at')
        # Admin provinsi can see all infografis
        else:  # admin_prov
            infografis = Infografis.objects.all().order_by('-created_at')
            
        context = {
            'infografis_list': infografis,
            'user_role': user.role
        }
        return render(request, 'backend/infografis/infografis.html', context)

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class InfografisCreateViews(View):
    def get(self, request):
        return render(request, 'backend/infografis/infografis.html')

    def post(self, request):
        title = request.POST.get('title')
        gambar = request.FILES.get('gambar')
        
        if title and gambar:
            # Set initial status based on user role
            initial_status = 'approved' if request.user.role in ['super_admin', 'admin_prov'] else 'pending'
            
            infografis = Infografis.objects.create(
                title=title,
                gambar=gambar,
                created_by=request.user,
                status=initial_status
            )
            
            # If auto-approved, set approved_by and approved_at
            if initial_status == 'approved':
                infografis.approved_by = request.user
                infografis.approved_at = timezone.now()
                infografis.save()
                messages.success(request, 'Infografis berhasil ditambahkan!')
            else:
                messages.success(request, 'Infografis berhasil ditambahkan dan menunggu persetujuan!')
                
            return redirect('wisata:infografis_list')
        else:
            messages.error(request, 'Semua field harus diisi!')
            return redirect('wisata:infografis_list')

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class InfografisUpdateViews(View):
    def get(self, request, infografis_id):
        infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
        user = request.user
        
        # Check if user has permission to edit this infografis
        if user.role == 'admin_kab' and infografis.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk mengedit infografis ini!')
            return redirect('wisata:infografis_list')
            
        context = {'infografis': infografis}
        return render(request, 'backend/infografis/infografis.html', context)

    def post(self, request, infografis_id):
        infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
        user = request.user
        
        # Check if user has permission to edit this infografis
        if user.role == 'admin_kab' and infografis.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk mengedit infografis ini!')
            return redirect('wisata:infografis_list')
            
        title = request.POST.get('title')
        gambar = request.FILES.get('gambar')
        
        if title:
            infografis.title = title
            if gambar:
                infografis.gambar = gambar
                
            # If admin kabupaten edits, set status back to pending
            if user.role == 'admin_kab':
                infografis.status = 'pending'
                infografis.approved_by = None
                infografis.approved_at = None
                infografis.rejection_reason = None
                
            infografis.save()
            messages.success(request, 'Infografis berhasil diperbarui!')
        else:
            messages.error(request, 'Judul harus diisi!')
            
        return redirect('wisata:infografis_list')

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class InfografisDeleteViews(View):
    def post(self, request, infografis_id):
        infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
        user = request.user
        
        # Check if user has permission to delete this infografis
        if user.role == 'admin_kab' and infografis.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk menghapus infografis ini!')
            return redirect('wisata:infografis_list')
        
        infografis.delete()
        messages.success(request, 'Infografis berhasil dihapus!')
        return redirect('wisata:infografis_list')

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov']), name='dispatch')
class ApproveInfografisViews(View):
    def post(self, request, infografis_id):
        infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
        action = request.POST.get('action')
        
        if action == 'approve':
            infografis.status = 'approved'
            infografis.approved_by = request.user
            infografis.approved_at = timezone.now()
            infografis.rejection_reason = None
            messages.success(request, "Infografis berhasil disetujui")
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', '')
            infografis.status = 'rejected'
            infografis.rejection_reason = rejection_reason
            messages.success(request, "Infografis berhasil ditolak")
            
        infografis.save()
        return redirect('wisata:infografis_list')
