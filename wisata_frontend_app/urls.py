from django.urls import path, include
from .views import *

app_name = 'app'



urlpatterns = [
    path('', home_frontend.HomeViews.as_view(), name='index_user'),
  
    path('tentang', include([
        path('', tentang_frontend.TentangViews.as_view(), name='tentang_user'),
    ])), 

    path('wisata/', include([
        path('wisata-bahari', wisata_frontend.WisataBahariViews.as_view(), name='wisata_bahari_frontend'),
        path('wisata-kuliner', wisata_frontend.WisataKulinerViews.as_view(), name='wisata_kuliner_frontend'),
        path('wisata-sejarah', wisata_frontend.WisataSejarahViews.as_view(), name='wisata_sejarah_frontend'),
        path('detail-wisata', wisata_frontend.DetailWisata.as_view(), name='detail_wisata_frontend'),
    ])), 

    path('penginapan', include([
        path('', penginapan_frontend.PenginapanViews.as_view(), name='penginapan_frontend'),
    ])), 

    path('kontak', include([
        path('', kontak_frontend.KontakViews.as_view(), name='kontak_frontend'),
    ])), 
    
]