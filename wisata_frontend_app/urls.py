from django.urls import path, include
from .views import *

app_name = 'app'



urlpatterns = [
    path('', home_frontend.HomeViews.as_view(), name='index_user'),
    path('faq/', faq.FAQView.as_view(), name='faq_frontend'),
    path('api/search-json/', search.search_json_api, name='search_json_api'),
    
  
    path('tentang-kami/', include([
        path('', tentang_frontend.TentangViews.as_view(), name='tentang_user'),
    ])), 

    path('wisata/', include([
        # path('<str:id_kategori>/', wisata_frontend.WisataViews.as_view(), name='wisata_frontend'),
        path('<slug:slug>', wisata_frontend.WisataDetailViews.as_view(), name='detail_wisata_frontend'),
        path('<slug:slug>/', wisata_frontend.WisataViews.as_view(), name='wisata_frontend'),
    ])), 

    path('penginapan/', include([
        path('', penginapan_frontend.PenginapanViews.as_view(), name='penginapan_frontend'),
        path('<slug:slug>', penginapan_frontend.PenginapanDetailViews.as_view(), name='detail_penginapan_frontend'),
    ])), 

    path('kontak/', include([
        path('', kontak_frontend.KontakViews.as_view(), name='kontak_frontend'),
        path('kritik-saran', kontak_frontend.KritikSaranCreateViews.as_view(), name='kritik_saran'),
    ])), 

    path('berita/', include([
        path('', berita_frontend.BeritaViews.as_view(), name='berita_frontend'),
        path('detail-berita/<slug:slug>/', berita_frontend.DetailBeritaViews.as_view(), name='detail_berita'),
    ])), 



    path('newsletter/subscribe/', newsletter.subscribe_newsletter, name='newsletter_subscribe'),

    
]