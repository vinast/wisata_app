from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.core.paginator import Paginator


class PenginapanViews(View):
    def get(self, request):     
        penginapan_list = Penginapan.objects.filter(
            deleted_at__isnull=True
        )
        paginator = Paginator(penginapan_list, 9)
        page_number = request.GET.get('page')
        penginapan = paginator.get_page(page_number)

        data = {
            'penginapan': penginapan
        }
        return render(request, 'frontend/penginapan/penginapan_frontend.html', data)
    



class PenginapanDetailViews(View):
    def get(self, request, slug):
        try:
            penginapan = Penginapan.objects.get(slug=slug, deleted_at__isnull=True)
            image_penginapan = PenginapanImage.objects.filter(penginapan=penginapan)
        except Penginapan.DoesNotExist:
            return redirect('app:penginapan_frontend')  # ← kembali ke list penginapan jika tidak ditemukan

        data = {
            'penginapan': penginapan,
            'image_penginapan': image_penginapan,
        }
        return render(request, 'frontend/penginapan/detail_penginapan.html', data)