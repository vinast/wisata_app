from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from wisata_app.models import Berita
from django.core.paginator import Paginator


class BeritaViews(View):
    def get(self, request):
        # Get category from query parameter, default to 'all'
        category = request.GET.get('category', 'all')
        
        # Base queryset - only show approved berita
        berita_list = Berita.objects.filter(status='approved').order_by('-created_at')
        
        # Filter by category if not 'all'
        if category != 'all':
            berita_list = berita_list.filter(kategori=category)
        
        # Pagination
        paginator = Paginator(berita_list, 9)  # Show 9 items per page
        page = request.GET.get('page')
        berita_list = paginator.get_page(page)
        
        # Get all categories for the filter (only from approved berita)
        categories = Berita.objects.filter(status='approved').values_list('kategori', flat=True).distinct()
        
        data = {
            'berita_list': berita_list,
            'categories': categories,
            'current_category': category,
        }
        return render(request, 'frontend/berita/berita_frontend.html', data)



class DetailBeritaViews(View):
    def get(self, request, slug=None):
        berita = get_object_or_404(Berita, slug=slug)
        
        # Get 3 random berita from the same category, excluding current berita
        random_berita = Berita.objects.filter(kategori=berita.kategori).exclude(berita_id=berita.berita_id).order_by('?')[:3]
        
        # Get the latest berita/event based on the current berita's category
        latest_berita = Berita.objects.filter(kategori=berita.kategori).order_by('-created_at').first()
        
        data = {
            'berita': berita,
            'random_berita': random_berita,
            'latest_berita': latest_berita,
        }
        return render(request, 'frontend/berita/detail_berita.html', data)