from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from wisata_app.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required
from django.db.models import Count

@method_decorator(custom_login_required, name='dispatch')
class HomeViews(View):
    def get(self, request):     
        # Mengambil total wisata per kategori
        wisata_per_kategori = Wisata.objects.values('kategori').annotate(total=Count('wisata_id')).order_by('kategori')
        
        # Mengambil total wisata
        total_wisata = Wisata.objects.count()
        
        # Mengambil wisata terbaru (5 terakhir)
        wisata_terbaru = Wisata.objects.all().order_by('-updated_at')[:5]
        
        # Mengambil total berita
        total_berita = Berita.objects.filter(kategori='berita').count()
        
        # Mengambil total event
        total_event = Berita.objects.filter(kategori='event').count()
        
        # Mengambil total kritik dan saran
        total_feedback = Kritiksaran.objects.count()
        
        # Mengambil total infografis
        total_infografis = Infografis.objects.count()
        
        # Mengambil berita terbaru (5 terakhir)
        berita_terbaru = Berita.objects.filter(kategori='berita').order_by('-updated_at')[:5]
        
        # Mengambil event terbaru (5 terakhir)
        event_terbaru = Berita.objects.filter(kategori='event').order_by('-updated_at')[:5]
        
        # Menyiapkan data untuk statistik wisata per kategori
        kategori_stats = []
        for item in wisata_per_kategori:
            kategori_stats.append({
                'kategori': item['kategori'],
                'total': item['total'],
                'persentase': round((item['total'] / total_wisata * 100), 1) if total_wisata > 0 else 0
            })
        
        data = {
            'total_wisata': total_wisata,
            'wisata_per_kategori': kategori_stats,
            'total_berita': total_berita,
            'total_event': total_event,
            'total_feedback': total_feedback,
            'total_infografis': total_infografis,
            'wisata_terbaru': wisata_terbaru,
            'berita_terbaru': berita_terbaru,
            'event_terbaru': event_terbaru
        }
        return render(request, 'backend/home/index.html', data)
    

