from django.shortcuts import render
from wisata_app.models import Wisata, Penginapan
from django.db.models import Q

# def search_view(request):
#     query = request.GET.get('q')
#     results = []

#     if query:
#         results = Wisata.objects.filter(nama_wisata__icontains=query)

#     return render(request, 'frontend/search/search_frontend.html', {
#         'query': query,
#         'results': results,
#     })


def search_view(request):
    query = request.GET.get('q', '')  # Get the search query from the URL

    results_wisata = []
    results_penginapan = []

    if query:
        # Search for tourist attractions (Wisata)
        results_wisata = Wisata.objects.filter(nama_wisata__icontains=query)
        
        # Search for accommodations (Penginapan)
        results_penginapan = Penginapan.objects.filter(nama_penginapan__icontains=query)

    return render(request, 'frontend/search/search_frontend.html', {
        'query': query,
        'results_wisata': results_wisata,
        'results_penginapan': results_penginapan,
    })



# def SearchView(request):
#     query = request.GET.get('q', '')  # Mengambil query atau string kosong jika tidak ada query
#     wisata_results = []
#     penginapan_results = []

#     if query:  # Hanya lakukan pencarian jika query tidak kosong
#         wisata_results = Wisata.objects.filter(
#             Q(nama_wisata__icontains=query)  # Pencarian hanya berdasarkan nama_wisata
#         ).distinct()

#         penginapan_results = Penginapan.objects.filter(
#             Q(nama_penginapan__icontains=query)  # Pencarian hanya berdasarkan nama_penginapan
#         ).distinct()

#     return render(request, 'frontend/search/search_frontend.html', {
#         'query': query,
#         'wisata_results': wisata_results,
#         'penginapan_results': penginapan_results,
#     })

