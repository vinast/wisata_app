from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Infografis
from ..decorators import role_required

@role_required(['super_admin', 'admin_prov', 'admin_kab'])
def infografis_list(request):
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
        
    return render(request, 'backend/infografis/infografis.html', {'infografis': infografis})

@role_required(['super_admin', 'admin_prov', 'admin_kab'])
def infografis_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        gambar = request.FILES.get('gambar')
        
        if title and gambar:
            Infografis.objects.create(
                title=title,
                gambar=gambar,
                created_by=request.user
            )
            messages.success(request, 'Infografis berhasil ditambahkan!')
            return redirect('wisata:infografis_list')
        else:
            messages.error(request, 'Semua field harus diisi!')
    
    return render(request, 'backend/infografis/infografis.html')

@role_required(['super_admin', 'admin_prov', 'admin_kab'])
def infografis_update(request, infografis_id):
    infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
    user = request.user
    
    # Check if user has permission to edit this infografis
    if user.role == 'admin_kab' and infografis.created_by != user:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit infografis ini!')
        return redirect('wisata:infografis_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        gambar = request.FILES.get('gambar')
        
        if title:
            infografis.title = title
            if gambar:
                infografis.gambar = gambar
            infografis.save()
            messages.success(request, 'Infografis berhasil diperbarui!')
            return redirect('wisata:infografis_list')
        else:
            messages.error(request, 'Judul harus diisi!')
    
    return render(request, 'backend/infografis/infografis.html', {'infografis': infografis})

@role_required(['super_admin', 'admin_prov', 'admin_kab'])
def infografis_delete(request, infografis_id):
    infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
    user = request.user
    
    # Check if user has permission to delete this infografis
    if user.role == 'admin_kab' and infografis.created_by != user:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus infografis ini!')
        return redirect('wisata:infografis_list')
    
    if request.method == 'POST':
        infografis.delete()
        messages.success(request, 'Infografis berhasil dihapus!')
        return redirect('wisata:infografis_list')
    
    return render(request, 'backend/infografis/infografis.html', {'infografis': infografis})
