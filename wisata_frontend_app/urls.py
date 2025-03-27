from django.urls import path, include
from .views import *

app_name = 'app'



urlpatterns = [
    path('', home_frontend.HomeViews.as_view(), name='index_user'),
  
    path('tentang', include([
        path('', tentang_frontend.TentangViews.as_view(), name='tentang_user'),
    ])), 

    path('wisata/', include([
        path('wisata_bahari', wisata_frontend.WisataBahariViews.as_view(), name='wisata_bahari_frontend'),
        path('wisata_kuliner', wisata_frontend.WisataKulinerViews.as_view(), name='wisata_kuliner_frontend'),
        path('wisata_sejarah', wisata_frontend.WisataSejarahViews.as_view(), name='wisata_sejarah_frontend'),
    ])), 

    path('penginapan', include([
        path('', penginapan_frontend.PenginapanViews.as_view(), name='penginapan_frontend'),
    ])), 

    path('kontak', include([
        path('', kontak_frontend.KontakViews.as_view(), name='kontak_frontend'),
    ])), 
    
]