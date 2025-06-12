from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class TentangViews(View):
    def get(self, request):   
        # tentang = TentangKami.objects.filter(deleted_at__isnull=True)
        # tentang_image = TentangKamiImage.objects.filter(tentang=tentang)
        data = {
            # 'tentang' : tentang, 
            # 'tentang_image' : tentang_image,
            
        }
        return render(request, 'frontend/tentang/tentang_frontend.html', data)
    