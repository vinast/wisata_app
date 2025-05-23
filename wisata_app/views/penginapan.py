from datetime import timezone
from django.views import View
from wisata_app.models import Penginapan, PenginapanImage, RatingPenginapan
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required
from django.db.models import Avg





@method_decorator(custom_login_required, name='dispatch')
class PenginapanViews(View):
    def get(self, request):
        penginapan = Penginapan.objects.filter(
            # deleted_at__isnull=True,
            )
        data ={
            'penginapan' : penginapan,
            }
        return render(request, 'backend/penginapan/penginapan.html', data)
    

@method_decorator(custom_login_required, name='dispatch')
class PenginapanDetailViews(View):
    def get(self, request, slug):
        try:
            penginapan = Penginapan.objects.get(slug=slug, deleted_at__isnull=True)
            image_penginapan = PenginapanImage.objects.filter(penginapan=penginapan)
            
            # Get average rating
            avg_rating = penginapan.ratings.aggregate(Avg('rating'))['rating__avg']
            if avg_rating is None:
                avg_rating = 0
            else:
                avg_rating = round(avg_rating, 1)
            
        except Penginapan.DoesNotExist:
            return redirect('wisata:penginapan')

        data = {
            'penginapan': penginapan,
            'image_penginapan': image_penginapan,
            'avg_rating': avg_rating,
        }
        return render(request, 'backend/penginapan/detail_penginapan.html', data)


@method_decorator(custom_login_required, name='dispatch')
class ReplyRatingPenginapanViews(View):
    def post(self, request, rating_id):
        try:
            rating = get_object_or_404(RatingPenginapan, rating_id=rating_id)
            admin_reply = request.POST.get('admin_reply')
            
            if admin_reply:
                rating.admin_reply = admin_reply
                rating.reply_date = timezone.now()
                rating.save()
                messages.success(request, "Balasan berhasil disimpan")
            else:
                messages.error(request, "Balasan tidak boleh kosong")
                
        except Exception as e:
            messages.error(request, f"Gagal menyimpan balasan: {str(e)}")
            
        return redirect('wisata:detail_penginapan', slug=rating.penginapan.slug)


@method_decorator(custom_login_required, name='dispatch')
class PenginapanCreateViews(View):
    def post(self, request):
        frm_nama_penginapan = request.POST.get('nama_penginapan')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
        frm_harga = request.POST.get('harga')
        frm_no_telepon = request.POST.get('no_telepon')
        frm_embed_maps = request.POST.get('embed_maps')
        images = request.FILES.getlist('images')

        try:
            with transaction.atomic():
                new_penginapan = Penginapan(
                    nama_penginapan=frm_nama_penginapan,
                    deskripsi=frm_deskripsi,
                    fasilitas=frm_fasilitas,
                    alamat=frm_alamat,
                    maps=frm_maps,
                    harga=frm_harga,
                    no_telepon=frm_no_telepon,
                    embed_maps=frm_embed_maps,

                )
                new_penginapan.save()  # Panggil save() agar slug otomatis dibuat

                for image in images:
                    PenginapanImage.objects.create(
                        penginapan=new_penginapan,
                        image=image
                    )

                messages.success(request, "Berhasil menambahkan penginapan")
                return redirect('wisata:index_penginapan')

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan penginapan")
            return redirect('wisata:index_penginapan')

            
             
class PenginapanEditViews(View):
    def get(self, request, id_penginapan):
        try:
            penginapan = Penginapan.objects.get(penginapan_id=id_penginapan)
            data = {
                'penginapan_id': id_penginapan,
                'penginapan': penginapan,
            }
            return render(request, 'backend/penginapan/penginapan.html', data)
        except Penginapan.DoesNotExist:
            messages.error(request, "Data Wisata tidak ditemukan")
            return redirect('wisata:index_penginapan')
    def post(self, request,  id_penginapan):
        frm_nama_penginapan = request.POST.get('nama_penginapan')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
        frm_harga = request.POST.get('harga')
        frm_no_telepon =  request.POST.get('no_telepon')
        frm_embed_maps = request.POST.get('embed_maps')
        images = request.FILES.getlist('images')

        try:
            
            with transaction.atomic():
                penginapan = Penginapan.objects.get(penginapan_id=id_penginapan)
                penginapan.nama_penginapan = frm_nama_penginapan
                penginapan.deskripsi = frm_deskripsi
                penginapan.fasilitas = frm_fasilitas
                penginapan.alamat =frm_alamat
                penginapan.maps = frm_maps
                penginapan.harga= frm_harga
                penginapan.no_telepon= frm_no_telepon
                penginapan.embed_maps = frm_embed_maps
                penginapan.save()

                if "hapus_gambar" in request.POST:
                    image_ids = request.POST.getlist("hapus_gambar")  
                    PenginapanImage.objects.filter(id__in=image_ids).delete()

            # Tambah gambar baru jika ada
                if images:  
                    for img in images:
                        PenginapanImage.objects.create(penginapan=penginapan, image=img)

                

                messages.success(request, "Data Penginapan berhasil diubah")
                return redirect('wisata:index_penginapan')

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah Data")
            return redirect('wisata:index_penginapan')
        
class HapusPenginapanViews(View):
    def post(self, request, id_penginapan):
        try:
            penginapan = Penginapan.objects.get(penginapan_id=id_penginapan)
            penginapan.delete()
            messages.success(request, f"Data Penginapan berhasil dihapus")
            return redirect('wisata:index_penginapan')
        except Penginapan.DoesNotExist:
            messages.error(request, "Data Penginapan tidak ditemukan")
            return redirect('wisata:index_penginapan')
        
