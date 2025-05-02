from django.urls import path, include
from .views import *

app_name = 'wisata'


urlpatterns = [
    path('', home.HomeViews.as_view(), name='index_home'),
    path('login/', auth.LoginViews.as_view(), name='login_admin'),
    path('logout/', auth.LogoutViews.as_view(), name='logout_admin'),


    path('user/', include([
       path('', master_user.UserViews.as_view(), name='index_user'),
       path('tambah/', master_user.CreateUserView.as_view(), name='tambah_user'),
       ])), 
    
    path('wisata/', include([
       path('bahari/', wisata.WisataBahariViews.as_view(), name='wisata_bahari'),
       path('kuliner/', wisata.WisataKulinerViews.as_view(), name='wisata_kuliner'),
       path('sejarah/', wisata.WisataSejarahViews.as_view(), name='wisata_sejarah'),
       path('tambah/', wisata.WisataCreateViews.as_view(), name='tambah_wisata'),
       path('edit/<str:id_wisata>/', wisata.WisataEditViews.as_view(), name='edit_wisata'),
       path('hapus/<str:id_wisata>/', wisata.HapusWisataViews.as_view(), name='hapus_wisata'),
       path('detail/<str:id_wisata>', wisata.WisataDetailViews.as_view(), name='detail_wisata'),
       ])),

    path('penginapan/', include([
       path('', penginapan.PenginapanViews.as_view(), name='index_penginapan'),
       path('tambah/', penginapan.PenginapanCreateViews.as_view(), name='tambah_penginapan'),
       path('edit/<str:id_penginapan>/', penginapan.PenginapanEditViews.as_view(), name='edit_penginapan'),
       path('hapus/<str:id_penginapan>/', penginapan.HapusPenginapanViews.as_view(), name='hapus_penginapan'),
       path('detail/<str:id_penginapan>/', penginapan.PenginapanDetailViews.as_view(), name='detail_penginapan'),
       ])), 
    
    path('faq/', include([
       path('', faq.FaqViews.as_view(), name='index_faq'),
       path('tambah/', faq.FaqCreateViews.as_view(), name='tambah_faq'),
       path('edit/<int:id_faq>/', faq.FaqEditViews.as_view(), name='edit_faq'),
       path('hapus/<int:id_faq>/', faq.HapusFaqViews.as_view(), name='hapus_faq'),
       ])), 
    
    path('kritiksaran/', include([
       path('', kritiksaran.KritikSaranViews.as_view(), name='index_kritiksaran'),
       path('tambah/', kritiksaran.KritikSaranCreateViews.as_view(), name='tambah_kritik'),
       path('hapus/<int:id_kritiksaran>/', kritiksaran.HapusKritikSaranViews.as_view(), name='hapus_kritik'),
       ])), 
]