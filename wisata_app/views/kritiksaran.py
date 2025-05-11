from datetime import timezone
from django.views import View
from wisata_app.models import Kritiksaran, Master_User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required





@method_decorator(custom_login_required, name='dispatch')
class KritikSaranViews(View):
    def get(self, request):
        kritiksaran = Kritiksaran.objects.filter(
            deleted_at__isnull=True,
            )
        data ={
            'kritiksaran' : kritiksaran,
            }
        return render(request, 'backend/kritiksaran/kritiksaran.html', data)

@method_decorator(custom_login_required, name='dispatch') 
class KritikSaranCreateViews(View):
    def post(self, request):
        frm_id_pengguna = request.POST.get('id_pengguna')
        frm_kritiksaran = request.POST.get('kritiksaran')


        try:
            id_user = get_object_or_404(Master_User, user_id=frm_id_pengguna)
            with transaction.atomic():
                new_kritiksaran = Kritiksaran.objects.create(
                    pengguna=id_user,
                    kritik=frm_kritiksaran,
                       
                )
                messages.success(request, f"Data berhasil ditambahkan")
                return redirect('wisata:index_kritiksaran')
                

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan kritiksaran")
            return redirect('wisata:index_kritiksaran')
        

# class KritikSaranEditViews(View):
#     def get(self, request, id_kritiksaran):
#         try:
#             kritiksaran = Kritiksaran.objects.get(id=id_kritiksaran)
#             data = {
#                 'id': id_kritiksaran,
#                 'kritiksaran': kritiksaran,
#             }
#             return render(request, 'backend/faq/kritiksaran.html', data)
#         except Kritiksaran.DoesNotExist:
#             messages.error(request, "Data tidak ditemukan")
#             return redirect('wisata:index_kritiksaran')
#     def post(self, request,  id_kritiksaran):
#         frm_pertanyaan = request.POST.get('pertanyaan')
#         frm_jawaban = request.POST.get('jawaban')

#         try:
            
#             with transaction.atomic():
#                 kritiksaran = Kritiksaran.objects.get(id=id_kritiksaran)
#                 kritiksaran.pertanyaan = frm_pertanyaan
#                 kritiksaran.jawaban = frm_jawaban
#                 kritiksaran.save()
#                 messages.success(request, "Data berhasil diubah")
#                 return redirect('wisata:index_kritiksaran')

#         except Exception as e:
#             print('Error:', e)
#             messages.error(request, "Gagal mengubah Data")
#             return redirect('wisata:index_kritiksaran')
        
class HapusKritikSaranViews(View):
    def get(self, request, id_kritiksaran):
        try:
            kritiksaran = Kritiksaran.objects.get(id=id_kritiksaran)
            # kritiksaran.deleted_at = timezone.now() #bikin arsip data, filter by deleted_at nya
            # kritiksaran.save() 
            kritiksaran.delete()
            messages.success(request, f"Data berhasil dihapus")
            return redirect('wisata:index_kritiksaran')
        except Kritiksaran.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_kritiksaran')