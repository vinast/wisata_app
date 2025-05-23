from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse
from django.db.models import Avg, F, Value, FloatField
from django.db.models.functions import Coalesce
from django.db import connection


class HomeViews(View):
    def get(self, request):     
        # Get top 7 rated destinations
        wisata_populer = Wisata.objects.filter(
            deleted_at__isnull=True
        ).annotate(
            avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
        ).order_by('-avg_rating', '-created_at')[:7]
        
        wisata_random = Wisata.objects.filter(deleted_at__isnull=True).order_by('?')[:3]
        
        # Get approved infografis with debugging
        infografis = Infografis.objects.filter(status='approved').order_by('-created_at')
        
        # Debug: Print the SQL query and count
        print("Infografis Query:", infografis.query)
        print("Infografis Count:", infografis.count())
        
        # Get latest approved berita and events
        berita_terbaru = Berita.objects.filter(
            status='approved'
        ).order_by('-created_at')[:3]

        data = {
            'wisata_populer': wisata_populer,
            'wisata_random': wisata_random,
            'infografis': infografis,
            'berita_terbaru': berita_terbaru
        }
        return render(request, 'frontend/home/index.html', data)
