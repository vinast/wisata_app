from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from wisata_app.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from notifications.signals import notify
from django.contrib.auth.models import User
from random import sample
import random





class WisataDetailViews(View):
    def get(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            image_wisata = WisataImage.objects.filter(wisata=wisata)


            # Get average rating
            avg_rating = wisata.ratings.aggregate(Avg('rating'))['rating__avg'] or 0

            # Get recent ratings
            recent_ratings = wisata.ratings.all()[:5]

            # 🆕 Split fasilitas
            fasilitas_list = [f.strip() for f in wisata.fasilitas.split(',')] if wisata.fasilitas else []

            # Rekomendasi penginapan berdasarkan desa/kecamatan
            alamat = wisata.alamat or ""
            desa = kecamatan = None
            
            # Ambil nama desa dengan lebih akurat
            if "Desa" in alamat:
                after = alamat.split("Desa", 1)[1]
                desa = after.split(",")[0].strip()
                print(f"Desa yang ditemukan: {desa}")
            
            # Ambil nama kecamatan dengan lebih akurat
            if "Kecamatan" in alamat:
                after = alamat.split("Kecamatan", 1)[1]
                kecamatan = after.split(",")[0].strip()
                print(f"Kecamatan yang ditemukan: {kecamatan}")
            
            rekomendasi_penginapan = []
            
            # Cari penginapan berdasarkan desa
            if desa:
                rekomendasi_penginapan = Penginapan.objects.filter(alamat__icontains=desa)[:4]
                print(f"Penginapan berdasarkan desa '{desa}': {rekomendasi_penginapan.count()}")
            
            # Jika tidak ada, cari berdasarkan kecamatan
            if not rekomendasi_penginapan and kecamatan:
                rekomendasi_penginapan = Penginapan.objects.filter(alamat__icontains=kecamatan)[:4]
                print(f"Penginapan berdasarkan kecamatan '{kecamatan}': {rekomendasi_penginapan.count()}")
            
            # Fallback ke random jika tidak ada yang cocok
            if not rekomendasi_penginapan:
                # Ambil 1 penginapan populer + 3 random
                popular_penginapan = Penginapan.objects.annotate(
                    avg_rating=Avg('ratings__rating')
                ).order_by('-avg_rating')[:5]  # Ambil 5 teratas
                
                if len(popular_penginapan) > 0:
                    # Ambil 1 penginapan populer
                    popular_one = random.choice(popular_penginapan)
                    
                    # Ambil 3 penginapan random (exclude yang sudah dipilih)
                    remaining_penginapan = list(Penginapan.objects.exclude(pk=popular_one.pk))
                    if len(remaining_penginapan) >= 3:
                        random_three = random.sample(remaining_penginapan, 3)
                        rekomendasi_penginapan = [popular_one] + random_three
                    else:
                        rekomendasi_penginapan = [popular_one] + remaining_penginapan
                else:
                    # Jika tidak ada rating, ambil 4 random
                    all_penginapan = list(Penginapan.objects.all())
                    rekomendasi_penginapan = random.sample(all_penginapan, 4) if len(all_penginapan) > 4 else all_penginapan
                print("Menggunakan 1 populer + 3 random")

        except Wisata.DoesNotExist:
            return redirect('app:index_user')

        data = {
            'wisata': wisata,
            'image_wisata': image_wisata,
            'avg_rating': round(avg_rating, 1),
            'recent_ratings': recent_ratings,
            'fasilitas_list': fasilitas_list,  # �� kirim ke template
            'rekomendasi_penginapan': rekomendasi_penginapan,  # 🆕 kirim ke template
        }
        return render(request, 'frontend/destinasi/detail_wisata.html', data)
    
    def post(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            
            rating = request.POST.get('rating')
            visitor_name = request.POST.get('visitor_name')
            visitor_email = request.POST.get('visitor_email')
            comment = request.POST.get('comment')
            
            rating_obj = RatingWisata.objects.create(
                wisata=wisata,
                rating=rating,
                visitor_name=visitor_name,
                visitor_email=visitor_email,
                comment=comment,
                ip_address=self.get_client_ip(request)  # Ini harus ada methodnya
            )
            
            # NOTIFIKASI DIHAPUS
            
            avg_rating = wisata.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            
            return JsonResponse({
                'status': 'success',
                'message': 'Rating berhasil disimpan',
                'avg_rating': round(avg_rating, 1)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class WisataViews(View):
    def get(self, request, slug):
            temp_kategori = get_object_or_404(Kategori, slug=slug)

            wisata = Wisata.objects.filter(
                kategori_wisata=temp_kategori.kategori_id,
                deleted_at__isnull=True
            ).annotate(
                avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
            ).order_by('-avg_rating', '-created_at')

            paginator = Paginator(wisata, 9)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            data = {
                'wisata_view': page_obj,
                'wisata': wisata,
                'temp_kategori': temp_kategori,
            }
            return render(request, 'frontend/destinasi/wisata_frontend.html', data)

    

































# class WisataBahariViews(View):
#     def get(self, request):
#         bahari_list = Wisata.objects.filter(
#             deleted_at__isnull=True
#         ).annotate(
#             avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
#         ).order_by('-avg_rating', '-created_at')
        
#         paginator = Paginator(bahari_list, 9)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         data = {
#             'bahari': page_obj
#         }
#         return render(request, 'frontend/destinasi/wisata_bahari.html', data)

    

# class WisataKulinerViews(View):
#     def get(self, request):     
#         kuliner_list = Wisata.objects.filter(
#             kategori="kuliner",
#             deleted_at__isnull=True
#         ).annotate(
#             avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
#         ).order_by('-avg_rating', '-created_at')
        
#         paginator = Paginator(kuliner_list, 9)
#         page_number = request.GET.get('page')
#         kuliner = paginator.get_page(page_number)

#         data = {
#             'kuliner': kuliner
#         }
#         return render(request, 'frontend/destinasi/wisata_kuliner.html', data)


# class WisataSejarahViews(View):
#     def get(self, request):     
#         sejarah_list = Wisata.objects.filter(
#             kategori="sejarah",
#             deleted_at__isnull=True
#         ).annotate(
#             avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
#         ).order_by('-avg_rating', '-created_at')
        
#         paginator = Paginator(sejarah_list, 9)
#         page_number = request.GET.get('page')
#         sejarah = paginator.get_page(page_number)

#         data = {
#             'sejarah': sejarah
#         }
#         return render(request, 'frontend/destinasi/wisata_sejarah.html', data)



