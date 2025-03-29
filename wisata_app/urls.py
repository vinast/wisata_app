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
       ])), 
    
    
]