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
        user = request.user
        
        # Super admin can see all berita
        if user.role == 'super_admin':
            berita = Berita.objects.filter(kategori='berita')
        # Admin kecamatan can only see their own berita
        elif user.role == 'admin_kab':
            berita = Berita.objects.filter(kategori='berita', created_by=user)
        # Admin provinsi can see all berita
        else:  # admin_prov
            berita = Berita.objects.filter(kategori='berita')
            
        context = {
            'berita_list': berita
        }
        return render(request, 'backend/berita/berita.html', context)

@method_decorator(role_required(allowed_roles=['super_admin', 'admin_prov', 'admin_kab']), name='dispatch')
class EventListViews(View):
    def get(self, request):
        user = request.user
        
        # Super admin can see all events
        if user.role == 'super_admin':
            event = Berita.objects.filter(kategori='event')
        # Admin kecamatan can only see their own events
        elif user.role == 'admin_kab':
            event = Berita.objects.filter(kategori='event', created_by=user)
        # Admin provinsi can see all events
        else:  # admin_prov
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
        username = getattr(request.user, 'username', 'admin')[:100]
        
        try:
            with transaction.atomic():
                new_berita = Berita(
                    title=frm_title,
                    kategori=frm_kategori,
                    konten=frm_konten,
                    tags=frm_tags,
                    thumbnail=frm_thumbnail,
                    created_by=request.user,
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
        berita = get_object_or_404(Berita, berita_id=id_berita)
        user = request.user
        
        # Check if user has permission to edit this berita
        if user.role == 'admin_kab' and berita.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk mengedit berita ini!')
            return redirect(self.redirect_url_by_kategori(berita.kategori))
            
        context = {
            'berita': berita,
            'kategori': berita.kategori,
        }
        return render(request, 'backend/berita/edit_berita_event.html', context)

    def post(self, request, id_berita):
        berita = get_object_or_404(Berita, berita_id=id_berita)
        user = request.user
        
        # Check if user has permission to edit this berita
        if user.role == 'admin_kab' and berita.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk mengedit berita ini!')
            return redirect(self.redirect_url_by_kategori(berita.kategori))
            
        frm_title = request.POST.get('judul')
        frm_kategori = request.POST.get('kategori')
        frm_konten = request.POST.get('isi')
        frm_tags = request.POST.get('tags')
        frm_thumbnail = request.FILES.get('thumbnail')
        username = getattr(request.user, 'username', 'admin')[:50]

        try:
            with transaction.atomic():
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
    def post(self, request, id_berita):
        try:
            berita = get_object_or_404(Berita, berita_id=id_berita)
            user = request.user
            
            # Check if user has permission to delete this berita
            if user.role == 'admin_kab' and berita.created_by != user:
                messages.error(request, 'Anda tidak memiliki izin untuk menghapus berita ini!')
                return redirect(self.redirect_url_by_kategori(berita.kategori))
                
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
        user = request.user
        
        # Check if user has permission to view this berita
        if user.role == 'admin_kab' and berita.created_by != user:
            messages.error(request, 'Anda tidak memiliki izin untuk melihat berita ini!')
            return redirect(self.redirect_url_by_kategori(berita.kategori))
            
        context = {'berita': berita}
        return render(request, 'backend/berita/detail_berita_event.html', context)
        
    def redirect_url_by_kategori(self, kategori):
        if kategori == 'berita':
            return 'wisata:berita_list'
        elif kategori == 'event':
            return 'wisata:event_list'
        return 'wisata:berita_list'
