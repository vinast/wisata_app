from django.urls import path, include
from .views import *
from .views import infografis



app_name = 'wisata'

urlpatterns = [
    path('', home.HomeViews.as_view(), name='index_home'),
    path('login/', auth.LoginViews.as_view(), name='login_admin'),
    path('logout/', auth.LogoutViews.as_view(), name='logout_admin'),
    path('notifikasi/<int:notification_id>/',notifications.MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),

    path('user/', include([
       path('', master_user.UserViews.as_view(), name='index_user'),
       path('tambah/', master_user.CreateUserView.as_view(), name='tambah_user'),
       path('update/<uuid:user_id>/', master_user.UpdateUserView.as_view(), name='update_user'),
       path('hapus/<uuid:user_id>/', master_user.DeleteUserView.as_view(), name='delete_user'),
       ])), 
    
    path('', include([
       path('wisata/', wisata.WisataViews.as_view(), name='index_wisata'),
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
   
   path('kategori/', include([
       path('', kategori.KategoriViews.as_view(), name='index_kategori'),
       path('tambah/', kategori.KategoriCreateViews.as_view(), name='tambah_kategori'),
       path('edit/<str:id_kategori>/', kategori.KategoriEditViews.as_view(), name='edit_kategori'),
       path('hapus/<str:id_kategori>/', kategori.HapusKategoriViews.as_view(), name='hapus_kategori'),
       path('detail/<slug:slug>/', kategori.KategoriDetailViews.as_view(), name='detail_kategori'),

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
         path('approve/<uuid:id_berita>/', berita.ApproveBeritaViews.as_view(), name='approve_berita'),
   ])),


   path('berita/', include([
       path('', berita.BeritaListViews.as_view(), name='berita_list'),
       path('tambah/', berita.BeritaCreateViews.as_view(), name='tambah_berita'),
       path('edit/<uuid:id_berita>/', berita.BeritaEditViews.as_view(), name='edit_berita'),
       path('hapus/<uuid:id_berita>/', berita.HapusBeritaViews.as_view(), name='hapus_berita'),
       path('detail/<slug:slug>/', berita.BeritaDetailViews.as_view(), name='detail_berita'),
       path('approve/<uuid:id_berita>/', berita.ApproveBeritaViews.as_view(), name='approve_berita'),
   ])),

  path('infografis/', include([
       path('', infografis.InfografisListViews.as_view(), name='infografis_list'),
       path('create/', infografis.InfografisCreateViews.as_view(), name='infografis_create'),
       path('update/<int:infografis_id>/', infografis.InfografisUpdateViews.as_view(), name='infografis_update'),
       path('delete/<int:infografis_id>/', infografis.InfografisDeleteViews.as_view(), name='infografis_delete'),
       path('approve/<int:infografis_id>/', infografis.ApproveInfografisViews.as_view(), name='approve_infografis'),
   ])),

   path('tentang/', include([
       path('', tentang_views.tentang_list, name='tentang_list'),
       path('create/', tentang_views.tentang_create, name='tentang_create'),
       path('edit/<uuid:tentang_id>/', tentang_views.tentang_edit, name='tentang_edit'),
       path('delete/<uuid:tentang_id>/', tentang_views.tentang_delete, name='tentang_delete'),
       path('detail/<uuid:tentang_id>/', tentang_views.tentang_detail, name='tentang_detail'),
   ])),
    

]