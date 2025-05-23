from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Infografis

def infografis_list(request):
    infografis = Infografis.objects.all().order_by('-created_at')
    return render(request, 'backend/infografis/infografis.html', {'infografis': infografis})


@login_required
def infografis_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        gambar = request.FILES.get('gambar')
        
        if title and gambar:
            Infografis.objects.create(
                title=title,
                gambar=gambar
            )
            messages.success(request, 'Infografis berhasil ditambahkan!')
            return redirect('wisata:infografis_list')
        else:
            messages.error(request, 'Semua field harus diisi!')
    
    return render(request, 'backend/infografis/infografis.html')

@login_required
def infografis_update(request, infografis_id):
    infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
    
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

@login_required
def infografis_delete(request, infografis_id):
    infografis = get_object_or_404(Infografis, infografis_id=infografis_id)
    
    if request.method == 'POST':
        infografis.delete()
        messages.success(request, 'Infografis berhasil dihapus!')
        return redirect('wisata:infografis_list')
    
    return render(request, 'backend/infografis/infografis.html', {'infografis': infografis})
