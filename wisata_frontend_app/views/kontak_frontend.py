from django.db import transaction 
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from wisata_app.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction  
from django.conf import settings
import requests # type: ignore


class KontakViews(View):
    def get(self, request):     
        kontak = Kontak.objects.filter(deleted_at__isnull=True)
        data = {
            'kontak': kontak,
        }
        return render(request, 'frontend/kontak/kontak_frontend.html', data)


# class KritikSaranCreateViews(View):
#     def post(self, request):
#         frm_id_pengguna = request.POST.get('id_pengguna')
#         frm_kritiksaran = request.POST.get('kritiksaran')

#         try:
#             # cek id_pengguna
#             if frm_id_pengguna:
#                 id_user = get_object_or_404(Master_User, user_id=frm_id_pengguna)
#             else:
#                 id_user = None  # anonim

#             with transaction.atomic():  # ✅ pakai transaction.atomic
#                 Kritiksaran.objects.create(
#                     pengguna=id_user,
#                     kritik=frm_kritiksaran,
#                 )

#             messages.success(request, "Data berhasil ditambahkan")
#             return redirect('wisata:index_kritiksaran')

#         except Exception as e:
#             print('error kode:', e)
#             messages.error(request, "Gagal menambahkan kritiksaran")
#             return redirect('wisata:index_kritiksaran')


class KritikSaranCreateViews(View):
    def post(self, request):
        frm_id_pengguna = request.POST.get('id_pengguna')
        frm_kritiksaran = request.POST.get('kritiksaran')

        # ✅ Tambahkan verifikasi Turnstile
        if not self.verify_turnstile(request):
            messages.error(request, "Verifikasi reCAPTCHA gagal. Silakan coba lagi.")
            return redirect('wisata:index_kritiksaran')

        try:
            if frm_id_pengguna:
                id_user = get_object_or_404(Master_User, user_id=frm_id_pengguna)
            else:
                id_user = None  # anonim

            with transaction.atomic():
                Kritiksaran.objects.create(
                    pengguna=id_user,
                    kritik=frm_kritiksaran,
                )

            messages.success(request, "Data berhasil ditambahkan")
            return redirect('wisata:index_kritiksaran')

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan kritiksaran")
            return redirect('wisata:index_kritiksaran')

    def verify_turnstile(self, request):
        """Verifikasi Cloudflare Turnstile."""
        turnstile_response = request.POST.get("cf-turnstile-response")
        data = {
            "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
            "response": turnstile_response,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
        try:
            response = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", data=data)
            return response.json().get("success", False)
        except requests.RequestException:
            return False

        