from datetime import timezone
from django.forms import ValidationError
from django.views import View
from wisata_app.models import Master_User, Wisata, WisataImage
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required





# class WisataDetailViews(View):
#     def get(self, request, id_wisata):
#         try:
#             wisata = Wisata.objects.get(wisata_id=id_wisata, deleted_at__isnull=True)
#             image_wisata = WisataImage.objects.filter(wisata_id=id_wisata)
#         except Wisata.DoesNotExist:
#             return redirect('wisata:wisata_bahari')  # Atau arahkan ke halaman lain jika tidak ditemukan

#         data = {
#             'wisata': wisata,
#             'image_wisata':image_wisata
#         }
#         return render(request, 'backend/wisata/detail_wisata.html', data)


class WisataDetailViews(View):
    def get(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            image_wisata = WisataImage.objects.filter(wisata=wisata)
        except Wisata.DoesNotExist:
            return redirect('wisata:wisata_bahari')  # atau ke halaman 404

        data = {
            'wisata': wisata,
            'image_wisata': image_wisata,
        }
        return render(request, 'backend/wisata/detail_wisata.html', data)

    



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
    

  
class WisataKulinerViews(View):
    def get(self, request):
        kuliner = Wisata.objects.filter(
            deleted_at__isnull=True,
            kategori = "kuliner"
            )
        data ={
            'kuliner' : kuliner,
            }
        return render(request, 'backend/wisata/wisatakulinerview.html', data)

class WisataSejarahViews(View):
    def get(self, request):
        sejarah = Wisata.objects.filter(
            deleted_at__isnull=True,
            kategori = "sejarah"
            )
        data ={
            'sejarah' : sejarah,
            }
        return render(request, 'backend/wisata/wisatasejarahview.html', data)

#create CREATE LAMA
# class WisataCreateViews(View):
#     def post(self, request):
#         frm_nama_wisata = request.POST.get('nama_wisata')
#         frm_kategori = request.POST.get('kategori')
#         frm_deskripsi = request.POST.get('deskripsi')
#         frm_fasilitas = request.POST.get('fasilitas')
#         frm_alamat = request.POST.get('alamat')
#         frm_maps = request.POST.get('maps')
#         frm_harga = request.POST.get('harga')
#         images = request.FILES.getlist('images')


#         try:
            
#             with transaction.atomic():
#                 new_wisata = Wisata.objects.create(
#                     nama_wisata=frm_nama_wisata,
#                     kategori=frm_kategori,
#                     deskripsi=frm_deskripsi,
#                     fasilitas=frm_fasilitas,
#                     alamat=frm_alamat,
#                     maps=frm_maps,
#                     harga=frm_harga,   
#                 )

#                 for image in images:
#                     WisataImage.objects.create(
#                         wisata=new_wisata,
#                         image=image
#                     )
#                 messages.success(request, f" berhasil ditambahkan")
#                 if frm_kategori == "bahari":
#                     return redirect('wisata:wisata_bahari')
#                 elif frm_kategori == "kuliner":
#                     return redirect('wisata:wisata_kuliner')
#                 elif frm_kategori == "sejarah":
#                     return redirect('wisata:wisata_sejarah')
                

#         except Exception as e:
#             print('error kode:', e)
#             messages.error(request, "Gagal menambahkan wisata")
#             if frm_kategori == "bahari":
#                 return redirect('wisata:wisata_bahari')
#             elif frm_kategori == "kuliner":
#                 return redirect('wisata:wisata_kuliner')
#             elif frm_kategori == "sejarah":
#                 return redirect('wisata:wisata_sejarah')
        
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
            if wisata.kategori == "bahari":
                return redirect('wisata:wisata_bahari')
            elif wisata.kategori == "kuliner":
                return redirect('wisata:wisata_kuliner')
            elif wisata.kategori == "sejarah":
                return redirect('wisata:wisata_sejarah')
    def post(self, request,  id_wisata):
        frm_nama_wisata = request.POST.get('nama_wisata')
        frm_kategori = request.POST.get('kategori')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
        frm_harga = request.POST.get('harga')
        images = request.FILES.getlist('images')

        try:
            
            with transaction.atomic():
                wisata = Wisata.objects.get(wisata_id=id_wisata)
                wisata.nama_wisata = frm_nama_wisata
                wisata.kategori = frm_kategori
                wisata.deskripsi = frm_deskripsi
                wisata.fasilitas = frm_fasilitas
                wisata.alamat =frm_alamat
                wisata.maps = frm_maps
                wisata.harga= frm_harga
                wisata.save()

                if "hapus_gambar" in request.POST:
                    image_ids = request.POST.getlist("hapus_gambar")  
                    WisataImage.objects.filter(id__in=image_ids).delete()

            # Tambah gambar baru jika ada
                if images:  
                    for img in images:
                        WisataImage.objects.create(wisata=wisata, image=img)

                

                messages.success(request, "Data Wisata berhasil diubah")
                if wisata.kategori == "bahari":
                    return redirect('wisata:wisata_bahari')
                elif wisata.kategori == "kuliner":
                    return redirect('wisata:wisata_kuliner')
                elif wisata.kategori == "sejarah":
                    return redirect('wisata:wisata_sejarah')

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah Data")
            if frm_kategori == "bahari":
                return redirect('wisata:wisata_bahari')
            elif frm_kategori == "kuliner":
                return redirect('wisata:wisata_kuliner')
            elif frm_kategori == "sejarah":
                return redirect('wisata:wisata_sejarah')
        
class HapusWisataViews(View):
    def get(self, request, id_wisata):
        try:
            wisata = Wisata.objects.get(wisata_id=id_wisata)
            # wisata.deleted_at = timezone.now() 
            # wisata.save() 
            wisata.delete()
            messages.success(request, f"Data Wisata berhasil dihapus")
        except Wisata.DoesNotExist:
            messages.error(request, "Data Wisata tidak ditemukan")
        if wisata.kategori == "bahari":
            return redirect('wisata:wisata_bahari')
        elif wisata.kategori == "kuliner":
            return redirect('wisata:wisata_kuliner')
        elif wisata.kategori == "sejarah":
            return redirect('wisata:wisata_sejarah')
        






class WisataCreateViews(View):
    def post(self, request):
        frm_nama_wisata = request.POST.get('nama_wisata')
        frm_kategori = request.POST.get('kategori')
        frm_deskripsi = request.POST.get('deskripsi')
        frm_fasilitas = request.POST.get('fasilitas')
        frm_alamat = request.POST.get('alamat')
        frm_maps = request.POST.get('maps')
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
                    harga=frm_harga,
                )
                new_wisata.save()

                for image in images:
                    WisataImage.objects.create(
                        wisata=new_wisata,
                        image=image
                    )
                messages.success(request, f" berhasil ditambahkan")
                if frm_kategori == "bahari":
                    return redirect('wisata:wisata_bahari')
                elif frm_kategori == "kuliner":
                    return redirect('wisata:wisata_kuliner')
                elif frm_kategori == "sejarah":
                    return redirect('wisata:wisata_sejarah')
                

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan wisata")
            if frm_kategori == "bahari":
                return redirect('wisata:wisata_bahari')
            elif frm_kategori == "kuliner":
                return redirect('wisata:wisata_kuliner')
            elif frm_kategori == "sejarah":
                return redirect('wisata:wisata_sejarah')