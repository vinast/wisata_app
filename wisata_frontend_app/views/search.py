from django.http import JsonResponse
from wisata_app.models import Wisata, Penginapan, Berita

def search_json_api(request):
    query = request.GET.get('q', '').strip()
    kategori = request.GET.get('kategori', 'all')

    data = {
        'wisata': [],
        'penginapan': [],
        'berita': [],
        'event': []
    }

    if len(query) >= 2:
        if kategori in ['all', 'wisata']:
            data['wisata'] = list(
                Wisata.objects.filter(nama_wisata__icontains=query)
                .values('nama_wisata', 'slug')[:5]
            )
        
        if kategori in ['all', 'penginapan']:
            data['penginapan'] = list(
                Penginapan.objects.filter(nama_penginapan__icontains=query)
                .values('nama_penginapan', 'slug')[:5]
            )
        
        if kategori in ['all', 'berita']:
            data['berita'] = list(
                Berita.objects.filter(
                    title__icontains=query,
                    kategori='berita',
                    status='approved'
                ).values('title', 'slug')[:5]
            )

        if kategori in ['all', 'event']:
            data['event'] = list(
                Berita.objects.filter(
                    title__icontains=query,
                    kategori='event',
                    status='approved'
                ).values('title', 'slug')[:5]
            )

    return JsonResponse(data)

