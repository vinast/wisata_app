from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth import get_user_model
from .models import RatingPenginapan, RatingWisata
from django.urls import reverse

User = get_user_model()

@receiver(post_save, sender=RatingPenginapan)
def notify_on_new_rating_penginapan(sender, instance, created, **kwargs):
    if created:
        penginapan = instance.penginapan
        pengelola = instance.pengelola
        # super_admin_users = User.objects.filter(role='super_admin')
        super_admin_users = User.objects.filter(role__in=['super_admin', 'admin_prov'])

        # if pengelola:  # Tambahkan pengecekan
        detail_url = reverse('wisata:detail_penginapan', args=[penginapan.slug])
            
        notify.send(
                instance,
                recipient=super_admin_users,
                verb=f"{instance.visitor_name} Memberikan Rating Untuk Penginapan '{penginapan.nama_penginapan}'",
                target=penginapan,
                # target_url=detail_url  # bisa ditambahkan jika kamu ingin
            )
        # else:
        #     print("❌ Pengelola tidak ditemukan pada RatingPenginapan:", instance)



@receiver(post_save, sender=RatingWisata)
def notify_on_new_rating_wisata(sender, instance, created, **kwargs):
    if created:
        wisata = instance.wisata
        pengelola = instance.pengelola
        # super_admin_users = User.objects.filter(role='super_admin')
        super_admin_users = User.objects.filter(role__in=['super_admin', 'admin_prov'])

        # if pengelola:  # Tambahkan pengecekan
        detail_url = reverse('wisata:detail_wisata', args=[wisata.slug])
            
        notify.send(
                instance,
                recipient=super_admin_users,
                verb=f"{instance.visitor_name} Memberikan Rating Untuk Wisata '{wisata.nama_wisata}'",
                target=wisata,
                # target_url=detail_url  # bisa ditambahkan jika kamu ingin
            )
        # else:
        #     print("❌ Pengelola tidak ditemukan pada RatingPenginapan:", instance)