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
       path('update/<uuid:user_id>/', master_user.UpdateUserView.as_view(), name='update_user'),
       path('hapus/<uuid:user_id>/', master_user.DeleteUserView.as_view(), name='delete_user'),
       ])), 
    
    path('wisata-', include([
       path('bahari/', wisata.WisataBahariViews.as_view(), name='wisata_bahari'),
       path('kuliner/', wisata.WisataKulinerViews.as_view(), name='wisata_kuliner'),
       path('sejarah/', wisata.WisataSejarahViews.as_view(), name='wisata_sejarah'),
       path('tambah/', wisata.WisataCreateViews.as_view(), name='tambah_wisata'),
       path('edit/<str:id_wisata>/', wisata.WisataEditViews.as_view(), name='edit_wisata'),
       path('hapus/<str:id_wisata>/', wisata.HapusWisataViews.as_view(), name='hapus_wisata'),
       path('detail/<slug:slug>/', wisata.WisataDetailViews.as_view(), name='detail_wisata'),
       path('reply-rating/<int:rating_id>/', wisata.ReplyRatingView.as_view(), name='reply_rating'),
       ])),

    path('penginapan/', include([
       path('', penginapan.PenginapanViews.as_view(), name='index_penginapan'),
       path('tambah/', penginapan.PenginapanCreateViews.as_view(), name='tambah_penginapan'),
       path('edit/<str:id_penginapan>/', penginapan.PenginapanEditViews.as_view(), name='edit_penginapan'),
       path('hapus/<str:id_penginapan>/', penginapan.HapusPenginapanViews.as_view(), name='hapus_penginapan'),
       path('detail/<slug:slug>/', penginapan.PenginapanDetailViews.as_view(), name='detail_penginapan'),
       path('reply-rating/<uuid:rating_id>/', penginapan.ReplyRatingPenginapanViews.as_view(), name='reply_rating_penginapan'),
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
   
   path('kontak/', include([
      path('', kontak.KontakViews.as_view(), name='index_kontak'),
      path('tambah/', kontak.KontakCreateViews.as_view(), name='tambah_kontak'),
      path('edit/<int:id_kontak>/', kontak.KontakEditViews.as_view(), name='edit_kontak'),
      path('hapus/<int:id_kontak>/', kontak.HapusKontakViews.as_view(), name='hapus_kontak'),
      ])),



   path('event/', include([
         path('', berita.EventListViews.as_view(), name='event_list'),
         path('tambah/', berita.BeritaCreateViews.as_view(), name='tambah_event'),
         path('edit/<uuid:id_berita>/', berita.BeritaEditViews.as_view(), name='edit_event'),
         path('hapus/<uuid:id_berita>/', berita.HapusBeritaViews.as_view(), name='hapus_event'),
         path('detail/<slug:slug>/', berita.BeritaDetailViews.as_view(), name='detail_event'),
   ])),


   path('berita/', include([
       path('', berita.BeritaListViews.as_view(), name='berita_list'),
       path('tambah/', berita.BeritaCreateViews.as_view(), name='tambah_berita'),
       path('edit/<uuid:id_berita>/', berita.BeritaEditViews.as_view(), name='edit_berita'),
       path('hapus/<uuid:id_berita>/', berita.HapusBeritaViews.as_view(), name='hapus_berita'),
       path('detail/<slug:slug>/', berita.BeritaDetailViews.as_view(), name='detail_berita'),
   ])),

  path('infografis/', include([
       path('', infografis.infografis_list, name='infografis_list'),
       path('infografis/<int:infografis_id>/', infografis.infografis_detail, name='infografis_detail'),
       path('infografis/create/', infografis.infografis_create, name='infografis_create'),
       path('infografis/<int:infografis_id>/update/', infografis.infografis_update, name='infografis_update'),
       path('infografis/<int:infografis_id>/delete/', infografis.infografis_delete, name='infografis_delete'),
   ])),

]