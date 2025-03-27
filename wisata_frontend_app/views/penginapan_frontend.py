from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class PenginapanViews(View):
    def get(self, request):     
        data = {
            
        }
        return render(request, 'frontend/penginapan/penginapan_frontend.html', data)
    