from datetime import timezone
from django.views import View
from wisata_app.models import Faq
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required





@method_decorator(custom_login_required, name='dispatch')
class FaqViews(View):
    def get(self, request):
        faq = Faq.objects.filter(
            deleted_at__isnull=True,
            )
        data ={
            'faq' : faq,
            }
        return render(request, 'backend/faq/index_faq.html', data)


@method_decorator(custom_login_required, name='dispatch')
class FaqCreateViews(View):
    def post(self, request):
        frm_pertanyaan = request.POST.get('pertanyaan')
        frm_jawaban = request.POST.get('jawaban')


        try:
            with transaction.atomic():
                new_faq = Faq.objects.create(
                    pertanyaan=frm_pertanyaan,
                    jawaban=frm_jawaban,
                       
                )
                messages.success(request, f"Data berhasil ditambahkan")
                return redirect('wisata:index_faq')
                

        except Exception as e:
            print('error kode:', e)
            messages.error(request, "Gagal menambahkan faq")
            return redirect('wisata:index_faq')
        

class FaqEditViews(View):
    def get(self, request, id_faq):
        try:
            faq = Faq.objects.get(id=id_faq)
            data = {
                'id': id_faq,
                'faq': faq,
            }
            return render(request, 'backend/faq/index_faq.html', data)
        except Faq.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_faq')
    def post(self, request,  id_faq):
        frm_pertanyaan = request.POST.get('pertanyaan')
        frm_jawaban = request.POST.get('jawaban')

        try:
            
            with transaction.atomic():
                faq = Faq.objects.get(id=id_faq)
                faq.pertanyaan = frm_pertanyaan
                faq.jawaban = frm_jawaban
                faq.save()
                messages.success(request, "Data berhasil diubah")
                return redirect('wisata:index_faq')

        except Exception as e:
            print('Error:', e)
            messages.error(request, "Gagal mengubah Data")
            return redirect('wisata:index_faq')
        
class HapusFaqViews(View):
    def post(self, request, id_faq):
        try:
            faq = Faq.objects.get(id=id_faq)
            faq.delete()
            messages.success(request, f"Data berhasil dihapus")
            return redirect('wisata:index_faq')
        except Faq.DoesNotExist:
            messages.error(request, "Data tidak ditemukan")
            return redirect('wisata:index_faq')