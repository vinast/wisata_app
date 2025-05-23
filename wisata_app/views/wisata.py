from datetime import timezone
from django.views import View
from wisata_app.models import Master_User, Wisata, WisataImage, RatingWisata
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required
from django.db.models import Avg
from django.utils import timezone





@method_decorator(custom_login_required, name='dispatch')
class WisataDetailViews(View):
    def get(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            image_wisata = WisataImage.objects.filter(wisata=wisata)
            
            # Calculate average rating
            avg_rating = wisata.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            
        except Wisata.DoesNotExist:
            return redirect('wisata:wisata_bahari')  # atau ke halaman 404

        data = {
            'wisata': wisata,
            'image_wisata': image_wisata,
            'avg_rating': round(avg_rating, 1)
        }
        return render(request, 'backend/wisata/detail_wisata.html', data)

    


@method_decorator(custom_login_required, name='dispatch')
class WisataBahariViews(View):
    def get(self, request):
        bahari = Wisata.objects.filter(
            # deleted_at__isnull=True,
            kategori = "bahari"
            )
        data ={
            'bahari' : bahari,
            }
        return render(request, 'backend/wisata/wisatabahariview.html', data)
    

@method_decorator(custom_login_required, name='dispatch')
class WisataKulinerViews(View):
    def get(self, request):
        kuliner = Wisata.objects.filter(
            # deleted_at__isnull=True,
            kategori = "kuliner"
            )
        data ={
            'kuliner' : kuliner,
            }
        return render(request, 'backend/wisata/wisatakulinerview.html', data)

@method_decorator(custom_login_required, name='dispatch')
class WisataSejarahViews(View):
    def get(self, request):
        sejarah = Wisata.objects.filter(
            # deleted_at__isnull=True,
            kategori = "sejarah"
            )
        data ={
            'sejarah' : sejarah,
            }
        return render(request, 'backend/wisata/wisatasejarahview.html', data)


 #Edit     
class WisataEditViews(View):
    def get(self, request, id_wisata):
        try:
            wisata = Wisata.objects.get(wisata_id=id_wisata)
            data = {
                'wisata_id': id_wisata,
                'wisata': wisata,
            }
            return render(request, 'user/userview.html', data)
        except Wisata.DoesNotExist:
            messages.error(request, "Data Wisata tidak ditemukan")
            return redirect('wisata:wisata_bahari')  # fallback redirect

    def post(self, request, id_wisata):
        frm_nama_wisata = request.POST.get('nama_wisata')
        frm_kategori = request.POST.get('kategori')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
        frm_embed_maps = request.POST.get('embed_maps')
        frm_jam_operasional = request.POST.get('jam_operasional')
        frm_harga = request.POST.get('harga')
        images = request.FILES.getlist('images')

        try:
            with transaction.atomic():
                wisata = Wisata.objects.get(wisata_id=id_wisata)
                wisata.nama_wisata = frm_nama_wisata
                wisata.kategori = frm_kategori
                wisata.deskripsi = frm_deskripsi
                wisata.fasilitas = frm_fasilitas
                wisata.alamat = frm_alamat
                wisata.maps = frm_maps
                wisata.embed_maps = frm_embed_maps
                wisata.jam_operasional = frm_jam_operasional
                wisata.harga = frm_harga
                wisata.save()

                if "hapus_gambar" in request.POST:
                    image_ids = request.POST.getlist("hapus_gambar")
                    WisataImage.objects.filter(id__in=image_ids).delete()

                if images:
                    for img in images:
                        WisataImage.objects.create(wisata=wisata, image=img)

                messages.success(request, "Data Wisata berhasil diubah")

                return redirect(self.redirect_url_by_kategori(wisata.kategori))

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah Data")
            return redirect(self.redirect_url_by_kategori(frm_kategori))

    def redirect_url_by_kategori(self, kategori):
        if kategori == "bahari":
            return 'wisata:wisata_bahari'
        elif kategori == "kuliner":
            return 'wisata:wisata_kuliner'
        elif kategori == "sejarah":
            return 'wisata:wisata_sejarah'
        return 'wisata:wisata_bahari'





class WisataCreateViews(View):
    def post(self, request):
        frm_nama_wisata = request.POST.get('nama_wisata')
        frm_kategori = request.POST.get('kategori')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
        frm_embed_maps = request.POST.get('embed_maps')
        frm_jam_operasional = request.POST.get('jam_operasional')
        frm_harga = request.POST.get('harga')
        images = request.FILES.getlist('images')

        try:
            with transaction.atomic():
                new_wisata = Wisata(
                    nama_wisata=frm_nama_wisata,
                    kategori=frm_kategori,
                    deskripsi=frm_deskripsi,
                    fasilitas=frm_fasilitas,
                    alamat=frm_alamat,
                    maps=frm_maps,
                    embed_maps=frm_embed_maps,
                    jam_operasional=frm_jam_operasional,
                    harga=frm_harga,
                )
                new_wisata.save()

                for image in images:
                    WisataImage.objects.create(
                        wisata=new_wisata,
                        image=image
                    )

                messages.success(request, "Data Wisata berhasil ditambahkan")
                return redirect(self.redirect_url_by_kategori(frm_kategori))

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal menambahkan Wisata")
            return redirect(self.redirect_url_by_kategori(frm_kategori))

    def redirect_url_by_kategori(self, kategori):
        if kategori == "bahari":
            return 'wisata:wisata_bahari'
        elif kategori == "kuliner":
            return 'wisata:wisata_kuliner'
        elif kategori == "sejarah":
            return 'wisata:wisata_sejarah'
        return 'wisata:wisata_bahari'






class HapusWisataViews(View):
    def post(self, request, id_wisata):
        try:
            wisata = Wisata.objects.get(wisata_id=id_wisata)
            kategori = wisata.kategori
            wisata.delete()
            messages.success(request, f"Data Wisata berhasil dihapus")
        except Wisata.DoesNotExist:
            messages.error(request, "Data Wisata tidak ditemukan")
            return redirect('wisata:wisata_bahari')
            
        if kategori == "bahari":
            return redirect('wisata:wisata_bahari')
        elif kategori == "kuliner":
            return redirect('wisata:wisata_kuliner')
        elif kategori == "sejarah":
            return redirect('wisata:wisata_sejarah')
        elif kategori == "budaya":
            return redirect('wisata:wisata_budaya')
        elif kategori == "alam":
            return redirect('wisata:wisata_alam')
        elif kategori == "religi":
            return redirect('wisata:wisata_religi')
        return redirect('wisata:wisata_bahari')

@method_decorator(custom_login_required, name='dispatch')
class ReplyRatingView(View):
    def post(self, request, rating_id):
        rating = get_object_or_404(RatingWisata, id=rating_id)
        admin_reply = request.POST.get('admin_reply')
        
        if admin_reply:
            rating.admin_reply = admin_reply
            rating.reply_date = timezone.now()
            rating.save()
            messages.success(request, 'Balasan berhasil disimpan')
        else:
            messages.error(request, 'Balasan tidak boleh kosong')
            
        return redirect('wisata:detail_wisata', slug=rating.wisata.slug)
        
