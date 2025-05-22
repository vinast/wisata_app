from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from wisata_app.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required
from django.db.models import Count, Avg, F, Value, FloatField
from django.db.models.functions import Coalesce
import datetime

@method_decorator(custom_login_required, name='dispatch')
class HomeViews(View):
    def get(self, request):     
        # Get selected category from request
        selected_category = request.GET.get('category', 'all')

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
        berita_terbaru = Berita.objects.filter(kategori='berita').order_by('-updated_at')[:3]
        
        # Mengambil event terbaru (5 terakhir)
        event_terbaru = Berita.objects.filter(kategori='event').order_by('-updated_at')[:2]

        # Mengambil wisata dengan rating tertinggi berdasarkan kategori
        wisata_query = Wisata.objects.filter(deleted_at__isnull=True)
        if selected_category != 'all' and selected_category != 'penginapan':
            wisata_query = wisata_query.filter(kategori=selected_category)
        
        wisata_rating = wisata_query.annotate(
            avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
        ).order_by('-avg_rating')[:10]

        # Mengambil penginapan dengan rating tertinggi jika kategori yang dipilih adalah 'penginapan' atau 'all'
        penginapan_rating = []
        if selected_category == 'all' or selected_category == 'penginapan':
            penginapan_rating = Penginapan.objects.filter(
                deleted_at__isnull=True
            ).annotate(
                avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
            ).order_by('-avg_rating')[:10]
        
        # Menyiapkan data untuk statistik wisata per kategori
        kategori_stats = []
        for item in wisata_per_kategori:
            kategori_stats.append({
                'kategori': item['kategori'],
                'total': item['total'],
                'persentase': round((item['total'] / total_wisata * 100), 1) if total_wisata > 0 else 0
            })

        # Menyiapkan data untuk grafik rating
        rating_data = []
        for wisata in wisata_rating:
            rating_data.append({
                'nama': wisata.nama_wisata,
                'rating': round(wisata.avg_rating, 1),
                'tipe': 'Wisata',
                'kategori': wisata.kategori
            })
        for penginapan in penginapan_rating:
            rating_data.append({
                'nama': penginapan.nama_penginapan,
                'rating': round(penginapan.avg_rating, 1),
                'tipe': 'Penginapan',
                'kategori': 'penginapan'
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
            'event_terbaru': event_terbaru,
            'wisata_rating': rating_data,
            'selected_category': selected_category,
        }
        return render(request, 'backend/home/index.html', data)
    

