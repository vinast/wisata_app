from datetime import timezone
from django.views import View
from wisata_app.models import Kategori
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required
from django.db.models.deletion import RestrictedError




@method_decorator(custom_login_required, name='dispatch')
class KategoriDetailViews(View):
    def get(self, request, slug):
        kategori = get_object_or_404(Kategori, slug=slug)

        if not kategori:
            messages.error(request, "Kategori tidak ditemukan")
            return redirect('wisata:index_kategori')

        data = {
            'kategori': kategori,
        }
        return render(request, 'backend/kategori/detail_kategori.html', data)




@method_decorator(custom_login_required, name='dispatch')
class KategoriViews(View):
    def get(self, request):
        kategori = Kategori.objects.filter(
            deleted_at__isnull=True,
            )
        data ={
            'kategori' : kategori,
            }
        return render(request, 'backend/kategori/index_kategori.html', data)


@method_decorator(custom_login_required, name='dispatch')
class KategoriCreateViews(View):
    def post(self, request):
        frm_nama_kategori = request.POST.get('nama_kategori')


        try:
            with transaction.atomic():
                new_kategori = Kategori.objects.create(
                    nama_kategori=frm_nama_kategori, 
                )
                messages.success(request, f"Data berhasil ditambahkan")
                return redirect('wisata:index_kategori')
                

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan kategori")
            return redirect('wisata:index_kategori')
        

class KategoriEditViews(View):
    def get(self, request, id_kategori):
        try:
            kategori = Kategori.objects.get(kategori_id=id_kategori)
            data = {
                'kategori': kategori,
            }
            return render(request, 'backend/kategori/index_kategori.html', data)
        except Kategori.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_kategori')
    def post(self, request,  id_kategori):
        frm_nama_kategori = request.POST.get('nama_kategori')

        try:
            
            with transaction.atomic():
                kategori = Kategori.objects.get(kategori_id=id_kategori)
                kategori.nama_kategori = frm_nama_kategori
                kategori.save()
                messages.success(request, "Data berhasil diubah")
                return redirect('wisata:index_kategori')

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah Data")
            return redirect('wisata:index_kategori')
        
# class HapusKategoriViews(View):
#     def post(self, request, id_kategori):
#         try:
#             kategori = Kategori.objects.get(kategori_id=id_kategori)
#             kategori.delete()
#             messages.success(request, f"Data berhasil dihapus")
#             return redirect('wisata:index_kategori')
#         except Kategori.DoesNotExist:
#             messages.error(request, "Data tidak ditemukan")
#             return redirect('wisata:index_kategori')


class HapusKategoriViews(View):
    def post(self, request, id_kategori):
        kategori = get_object_or_404(Kategori, kategori_id=id_kategori)
        try:
            kategori.delete()
            messages.success(request, "Data berhasil dihapus")
        except RestrictedError:
            messages.error(request, "Gagal hapus kategori! Hapus dulu wisata yang terkait dengan kategori ini.")
        return redirect('wisata:index_kategori')