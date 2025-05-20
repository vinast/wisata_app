from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.core.paginator import Paginator


class WisataDetailViews(View):
    def get(self, request, slug):
        try:
            wisata = Wisata.objects.get(slug=slug, deleted_at__isnull=True)
            image_wisata = WisataImage.objects.filter(wisata=wisata)
            
            # Get the correct URL based on category
            category_url = {
                'bahari': 'app:wisata_bahari_frontend',
                'kuliner': 'app:wisata_kuliner_frontend',
                'sejarah': 'app:wisata_sejarah_frontend'
            }.get(wisata.kategori, 'app:wisata_bahari_frontend')
            
        except Wisata.DoesNotExist:
            return redirect('app:wisata_bahari_frontend')

        data = {
            'wisata': wisata,
            'image_wisata': image_wisata,
            'category_url': category_url
        }
        return render(request, 'frontend/destinasi/detail_wisata.html', data)




class WisataBahariViews(View):
    def get(self, request):
        bahari_list = Wisata.objects.filter(
            kategori="bahari",
            deleted_at__isnull=True
        )
        paginator = Paginator(bahari_list, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'bahari': page_obj
        }
        return render(request, 'frontend/destinasi/wisata_bahari.html', data)

    

class WisataKulinerViews(View):
    def get(self, request):     
        kuliner_list = Wisata.objects.filter(
            kategori="kuliner",
            deleted_at__isnull=True
        )
        paginator = Paginator(kuliner_list, 9)
        page_number = request.GET.get('page')
        kuliner = paginator.get_page(page_number)

        data = {
            'kuliner': kuliner
        }
        return render(request, 'frontend/destinasi/wisata_kuliner.html', data)


class WisataSejarahViews(View):
    def get(self, request):     
        sejarah_list = Wisata.objects.filter(
            kategori="sejarah",
            deleted_at__isnull=True
        )
        paginator = Paginator(sejarah_list, 9)
        page_number = request.GET.get('page')
        sejarah = paginator.get_page(page_number)

        data = {
            'sejarah': sejarah
        }
        return render(request, 'frontend/destinasi/wisata_sejarah.html', data)



