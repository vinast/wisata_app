from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class TentangViews(View):
    def get(self, request):   
        tentang = TentangKami.objects.all()
        data = {
            'tentang' : tentang, 
        }
        return render(request, 'frontend/tentang/tentang_frontend.html', data)
    