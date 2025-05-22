from uuid import UUID
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils.decorators import method_decorator
from wisata_app.decorators import role_required
from wisata_app.models import Berita 

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class BeritaListViews(View):
    def get(self, request):
        berita = Berita.objects.filter(kategori='berita')
        context = {
            'berita_list': berita
            
        }
        return render(request, 'backend/berita/berita.html', context)



@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class EventListViews(View):
    def get(self, request):
        event = Berita.objects.filter(kategori='event')
        context = {
            'event_list': event
            
        }
        return render(request, 'backend/berita/event.html', context)
    


@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class BeritaCreateViews(View):
    def get(self, request):
        if 'event' in request.path:
             kategori = 'event'
        else:
             kategori = 'berita'
        context = {
            'kategori': kategori,
        
        }
        return render(request, 'backend/berita/tambah_berita_event.html', context)

    def post(self, request):
        frm_title = request.POST.get('judul')
        frm_kategori = request.POST.get('kategori')
        frm_konten = request.POST.get('isi')
        frm_tags = request.POST.get('tags')
        frm_thumbnail = request.FILES.get('thumbnail')
        username = getattr(request.user, 'username', 'admin')
        try:
            with transaction.atomic():
                new_berita = Berita(
                    title=frm_title,
                    kategori=frm_kategori,
                    konten=frm_konten,
                    tags=frm_tags,
                    thumbnail=frm_thumbnail,
                    created_by=username,
                    last_updated_by=username,
                )
                new_berita.save()
                messages.success(request, "Berita berhasil ditambahkan")
                return redirect(self.redirect_url_by_kategori(frm_kategori))
        except Exception as e:
            print("Error:", e)
            messages.error(request, "Gagal menambahkan Berita")
            return redirect(self.redirect_url_by_kategori(frm_kategori))

    def redirect_url_by_kategori(self, kategori):
        if kategori == 'berita':
            return 'wisata:berita_list'
        elif kategori == 'event':
            return 'wisata:event_list'
        return 'wisata:berita_list'
    



@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class BeritaEditViews(View):
    def get(self, request, id_berita: UUID):
        berita = Berita.objects.get(berita_id=id_berita)
        context = {
            'berita': berita,
            'kategori': berita.kategori,
        
        }
        return render(request, 'backend/berita/edit_berita_event.html', context)

    def post(self, request, id_berita):
        frm_title = request.POST.get('judul')
        frm_kategori = request.POST.get('kategori')
        frm_konten = request.POST.get('isi')
        frm_tags = request.POST.get('tags')
        frm_thumbnail = request.FILES.get('thumbnail')
        username = getattr(request.user, 'username', 'admin')

        try:
            with transaction.atomic():
                berita = get_object_or_404(Berita, pk=id_berita)
                berita.title = frm_title
                berita.kategori = frm_kategori
                berita.konten = frm_konten
                berita.tags = frm_tags
                if frm_thumbnail:
                    berita.thumbnail = frm_thumbnail
                berita.last_updated_by = username
                berita.save()

                messages.success(request, "Berita berhasil diperbarui")
                return redirect(self.redirect_url_by_kategori(frm_kategori))
        except Exception as e:
            print("Error:", e)
            messages.error(request, "Gagal mengubah Berita")
            return redirect(self.redirect_url_by_kategori(frm_kategori))

    def redirect_url_by_kategori(self, kategori):
        if kategori == 'berita':
            return 'wisata:berita_list'
        elif kategori == 'event':
            return 'wisata:event_list'
        return 'wisata:berita_list'



@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class HapusBeritaViews(View):
    def get(self, request, id_berita):
        try:
            berita = Berita.objects.get(pk=id_berita)
            kategori = berita.kategori
            berita.delete()
            messages.success(request, "Berita berhasil dihapus")
        except Berita.DoesNotExist:
            messages.error(request, "Berita tidak ditemukan")
            kategori = 'berita'
        return redirect(self.redirect_url_by_kategori(kategori))

    def redirect_url_by_kategori(self, kategori):
        if kategori == 'berita':
            return 'wisata:berita_list'
        elif kategori == 'event':
            return 'wisata:event_list'
        return 'wisata:berita_list'




@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class BeritaDetailViews(View):
    def get(self, request, slug):
        berita = get_object_or_404(Berita, slug=slug)
        context = {'berita': berita}
        return render(request, 'backend/berita/detail_berita_event.html', context)
