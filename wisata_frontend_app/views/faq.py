from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse


class FAQView(View):
    def get(self, request): 
        faq = Faq.objects.filter( deleted_at__isnull=True )    
        data = {

            'faq': faq,
            
        }
        return render(request, 'frontend/faq/faq.html', data)
    