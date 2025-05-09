# app_name/context_processors.py

from wisata_app.models import Kontak

def kontak_footer(request):
    return {
        'data_kontak': Kontak.objects.all()
    }