from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class WisataBahariViews(View):
    def get(self, request):     
        data = {
            
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
    
    