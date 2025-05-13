from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


# class HomeViews(View):
#     def get(self, request):     
#         data = {
            
#         }
#         return render(request, 'frontend/home/index.html', data)


class HomeViews(View):
    def get(self, request):     
        wisata_terbaru = Wisata.objects.filter(deleted_at__isnull=True).order_by('-created_at')[:4]
        wisata_random = Wisata.objects.filter(deleted_at__isnull=True).order_by('?')[:3]

        data = {
            'wisata_terbaru': wisata_terbaru,
            'wisata_random': wisata_random
        }
        return render(request, 'frontend/home/index.html', data)
