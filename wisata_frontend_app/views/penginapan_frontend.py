from django.shortcuts import render, redirect
from django.views import View
from wisata_app.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from django.utils import timezone


class PenginapanViews(View):
    def get(self, request):     
        penginapan_list = Penginapan.objects.filter(
            deleted_at__isnull=True
        ).annotate(
            avg_rating=Coalesce(Avg('ratings__rating'), Value(0.0), output_field=FloatField())
        ).order_by('-avg_rating', '-created_at')
        
        paginator = Paginator(penginapan_list, 9)
        page_number = request.GET.get('page')
        penginapan = paginator.get_page(page_number)

        data = {
            'penginapan': penginapan
        }
        return render(request, 'frontend/penginapan/penginapan_frontend.html', data)
    



class PenginapanDetailViews(View):
    def get(self, request, slug):
        try:
            penginapan = Penginapan.objects.get(slug=slug, deleted_at__isnull=True)
            image_penginapan = PenginapanImage.objects.filter(penginapan=penginapan)
            
            # Get average rating
            avg_rating = penginapan.ratings.aggregate(Avg('rating'))['rating__avg']
            if avg_rating is None:
                avg_rating = 0
            else:
                avg_rating = round(avg_rating, 1)
            
            # Get recent ratings
            recent_ratings = penginapan.ratings.all().order_by('-created_at')
            
        except Penginapan.DoesNotExist:
            return redirect('app:penginapan_frontend')

        data = {
            'penginapan': penginapan,
            'image_penginapan': image_penginapan,
            'avg_rating': avg_rating,
            'recent_ratings': recent_ratings,
        }
        return render(request, 'frontend/penginapan/detail_penginapan.html', data)
        
    def post(self, request, slug):
        try:
            penginapan = Penginapan.objects.get(slug=slug, deleted_at__isnull=True)
            
            # Get form data
            visitor_name = request.POST.get('visitor_name')
            visitor_email = request.POST.get('visitor_email')
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            # Create new rating
            RatingPenginapan.objects.create(
                penginapan=penginapan,
                visitor_name=visitor_name,
                visitor_email=visitor_email,
                rating=rating,
                comment=comment,
                created_at=timezone.now()
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Terima kasih atas ulasan Anda!'
            })
            
        except Penginapan.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Penginapan tidak ditemukan'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)