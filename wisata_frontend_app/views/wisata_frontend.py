from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class WisataDetailViews(View):
    def get(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            image_wisata = WisataImage.objects.filter(wisata=wisata)
        except Wisata.DoesNotExist:
            return redirect('app:wisata_bahari_frontend')  # atau ke halaman 404

        data = {
            'wisata': wisata,
            'image_wisata': image_wisata,
        }
        return render(request, 'frontend/destinasi/detail_wisata.html', data)

class WisataBahariViews(View):
    def get(self, request):
        bahari = Wisata.objects.filter(
            kategori="bahari",
            deleted_at__isnull=True
        )
        data = {
            'bahari': bahari
        }
        return render(request, 'frontend/destinasi/wisata_bahari.html', data)

    

class WisataKulinerViews(View):
    def get(self, request):     
        data = {
            
        }
        return render(request, 'frontend/destinasi/wisata_kuliner.html', data)

class WisataSejarahViews(View):
    def get(self, request):     
        data = {
            
        }
        return render(request, 'frontend/destinasi/wisata_sejarah.html', data)



class DetailWisata(View):   
    def get(self, request):
        data = {

        }
        return render(request, 'frontend/destinasi/detail_wisata.html', data)    