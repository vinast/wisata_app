from django.shortcuts import render
from django.views import View
from django.db.models import Count, Avg, Value, FloatField
from django.db.models.functions import Coalesce
import datetime
from wisata_app.models import Wisata, Penginapan, Berita, Kritiksaran, Infografis, Kategori
from wisata_app.decorators import custom_login_required, role_required
from django.utils.decorators import method_decorator

@method_decorator(custom_login_required, name='dispatch')
@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov']), name='dispatch')
class HomeViews(View):
    def get(self, request):
        selected_category = request.GET.get('category', 'all')
        selected_month = request.GET.get('month')  # misal '05'
        selected_year = request.GET.get('year')    # misal '2025'

        wisata_per_kategori = Wisata.objects.values('kategori_wisata').annotate(total=Count('wisata_id')).order_by('kategori_wisata')
        total_wisata = Wisata.objects.count()
        wisata_terbaru = Wisata.objects.all().order_by('-updated_at')[:5]

        total_berita = Berita.objects.filter(kategori='berita').count()
        total_event = Berita.objects.filter(kategori='event').count()
        total_feedback = Kritiksaran.objects.count()
        total_infografis = Infografis.objects.count()
        berita_terbaru = Berita.objects.filter(kategori='berita').order_by('-updated_at')[:3]
        event_terbaru = Berita.objects.filter(kategori='event').order_by('-updated_at')[:2]

        wisata_query = Wisata.objects.filter(deleted_at__isnull=True)
        penginapan_query = Penginapan.objects.filter(deleted_at__isnull=True)

        # Filter kategori
        if selected_category != 'all' and selected_category != 'penginapan':
            wisata_query = wisata_query.filter(kategori_wisata=selected_category)
        if selected_category == 'penginapan':
            wisata_query = Wisata.objects.none()  # supaya wisata kosong, hanya penginapan tampil

        # Filter bulan & tahun jika ada
        if selected_year:
            wisata_query = wisata_query.filter(updated_at__year=selected_year)
            penginapan_query = penginapan_query.filter(updated_at__year=selected_year)
        if selected_month:
            wisata_query = wisata_query.filter(updated_at__month=selected_month)
            penginapan_query = penginapan_query.filter(updated_at__month=selected_month)

        # Ambil rating wisata dan penginapan setelah filter
        wisata_rating = wisata_query.annotate(
            avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
        ).order_by('-avg_rating')[:10]

        penginapan_rating = []
        if selected_category == 'all' or selected_category == 'penginapan':
            penginapan_rating = penginapan_query.annotate(
                avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
            ).order_by('-avg_rating')[:10]

        # Statistik wisata per kategori (tidak perlu filter bulan/tahun karena untuk statistik keseluruhan)
        kategori_stats = []
        kategori_map = {k.kategori_id: k.nama_kategori for k in Kategori.objects.all()}
        for item in wisata_per_kategori:
            kategori_stats.append({
                'kategori_wisata': item['kategori_wisata'],
                'kategori_nama': kategori_map.get(item['kategori_wisata'], 'Tanpa Kategori'),
                'total': item['total'],
                'persentase': round((item['total'] / total_wisata * 100), 1) if total_wisata > 0 else 0
            })

        # Data untuk grafik rating
        rating_data = []
        for wisata in wisata_rating:
            rating_data.append({
                'nama': wisata.nama_wisata,
                'rating': round(wisata.avg_rating, 1),
                'tipe': 'Wisata',
                'kategori': wisata.kategori_wisata,
                'kategori_nama': kategori_map.get(wisata.kategori_wisata_id, 'Tanpa Kategori'),
            })
        for penginapan in penginapan_rating:
            rating_data.append({
                'nama': penginapan.nama_penginapan,
                'rating': round(penginapan.avg_rating, 1),
                'tipe': 'Penginapan',
                'kategori': 'penginapan',
                'kategori_nama': 'Penginapan',
            })

        # Kirim semua variable yang diperlukan ke template
        current_year = datetime.datetime.now().year
        months = list(range(1, 13))
        years = list(range(2020, current_year + 1))

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
            'selected_month': int(selected_month) if selected_month else None,
            'selected_year': int(selected_year) if selected_year else None,
            'months': months,
            'years': years,
            'data_kategori': Kategori.objects.all(),
        }
        return render(request, 'backend/home/index.html', data)
