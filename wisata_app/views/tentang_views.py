from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import TentangKami, TentangKamiImage
from django.core.paginator import Paginator

@login_required
def tentang_list(request):
    tentang_list = TentangKami.objects.all().order_by('-created_at')
    paginator = Paginator(tentang_list, 10)  # Show 10 items per page
    page = request.GET.get('page')
    tentang = paginator.get_page(page)
    return render(request, 'backend/tentang/tentang.html', {'tentang': tentang})

@login_required
def tentang_create(request):
    if request.method == 'POST':
        visi = request.POST.get('visi')
        misi = request.POST.get('misi')
        deskripsi = request.POST.get('deskripsi')
        images = request.FILES.getlist('images')
        
        tentang = TentangKami.objects.create(
            visi=visi,
            misi=misi,
            deskripsi=deskripsi,
            created_by=request.user.username,
            last_updated_by=request.user.username
        )
        
        for image in images:
            TentangKamiImage.objects.create(
                tentang=tentang,
                image=image
            )
            
        messages.success(request, 'Data berhasil ditambahkan!')
        return redirect('wisata:tentang_list')
    
    return redirect('wisata:tentang_list')

@login_required
def tentang_edit(request, tentang_id):
    tentang = get_object_or_404(TentangKami, tentang_id=tentang_id)
    
    if request.method == 'POST':
        tentang.visi = request.POST.get('visi')
        tentang.misi = request.POST.get('misi')
        tentang.deskripsi = request.POST.get('deskripsi')
        tentang.last_updated_by = request.user.username
        
        images = request.FILES.getlist('images')
        if images:
            # Delete existing images
            tentang.images.all().delete()
            # Add new images
            for image in images:
                TentangKamiImage.objects.create(
                    tentang=tentang,
                    image=image
                )
                
        tentang.save()
        messages.success(request, 'Data berhasil diperbarui!')
        return redirect('wisata:tentang_list')
    
    return redirect('wisata:tentang_list')

@login_required
def tentang_delete(request, tentang_id):
    tentang = get_object_or_404(TentangKami, tentang_id=tentang_id)
    if request.method == 'POST':
        tentang.delete()
        messages.success(request, 'Data berhasil dihapus!')
        return redirect('wisata:tentang_list')
    return redirect('wisata:tentang_list')

@login_required
def tentang_detail(request, tentang_id):
    tentang = get_object_or_404(TentangKami, tentang_id=tentang_id)
    return render(request, 'backend/tentang/detail_tentang.html', {'tentang': tentang})

