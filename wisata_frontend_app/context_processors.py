# app_name/context_processors.py

from wisata_app.models import Kontak, Kategori

def kontak_footer(request):
    return {
        'data_kontak': Kontak.objects.all()
    }

def destination_category(request):
    return {
        'data_kategori': Kategori.objects.all()
    }