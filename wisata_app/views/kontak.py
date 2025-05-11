from django.views import View
from wisata_app.models import *
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required





@method_decorator(custom_login_required, name='dispatch')
class KontakViews(View):
    def get(self, request):
        kontak = Kontak.objects.all()
        data = {
            'kontak': kontak,
        }
        return render(request, 'backend/kontak/index_kontak.html', data)


@method_decorator(custom_login_required, name='dispatch')
class KontakCreateViews(View):
    def post(self, request):
        frm_alamat = request.POST.get('alamat')
        frm_email = request.POST.get('email')
        frm_phone = request.POST.get('phone')
        frm_instagram = request.POST.get('instagram')
        frm_youtube = request.POST.get('youtube')
        frm_jam_operasional = request.POST.get('jam_operasional')
        frm_link_maps = request.POST.get('link_maps')

        try:
            with transaction.atomic():
                new_kontak = Kontak.objects.create(
                    alamat=frm_alamat,
                    email=frm_email,
                    phone=frm_phone,
                    instagram=frm_instagram,
                    youtube=frm_youtube,
                    jam_operasional=frm_jam_operasional,
                    link_maps=frm_link_maps,
                )
                messages.success(request, "Data kontak berhasil ditambahkan")
                return redirect('wisata:index_kontak')
        except Exception as e:
            print('Error kode:', e)
            messages.error(request, "Gagal menambahkan kontak")
            return redirect('wisata:index_kontak')


class KontakEditViews(View):
    def get(self, request, id_kontak):
        try:
            kontak = Kontak.objects.get(id=id_kontak)
            data = {
                'id': id_kontak,
                'kontak': kontak,
            }
            return render(request, 'backend/kontak/edit_kontak.html', data)
        except Kontak.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_kontak')
    
    def post(self, request, id_kontak):
        frm_alamat = request.POST.get('alamat')
        frm_email = request.POST.get('email')
        frm_phone = request.POST.get('phone')
        frm_instagram = request.POST.get('instagram')
        frm_youtube = request.POST.get('youtube')
        frm_jam_operasional = request.POST.get('jam_operasional')
        frm_link_maps = request.POST.get('link_maps')

        try:
            with transaction.atomic():
                kontak = Kontak.objects.get(id=id_kontak)
                kontak.alamat = frm_alamat
                kontak.email = frm_email
                kontak.phone = frm_phone
                kontak.instagram = frm_instagram
                kontak.youtube = frm_youtube
                kontak.jam_operasional = frm_jam_operasional
                kontak.link_maps = frm_link_maps
                kontak.save()
                messages.success(request, "Data kontak berhasil diubah")
                return redirect('wisata:index_kontak')
        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah kontak")
            return redirect('wisata:index_kontak')


class HapusKontakViews(View):
    def get(self, request, id_kontak):
        try:
            kontak = Kontak.objects.get(id=id_kontak)
            # kontak.deleted_at = timezone.now()  # Menggunakan soft delete (mengarsipkan)
            # kontak.save()  # Menyimpan perubahan
            kontak.delete()
            messages.success(request, "Data kontak berhasil dihapus")
            return redirect('wisata:index_kontak')
        except Kontak.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_kontak')
