# views.py
from django.http import JsonResponse
from wisata_app.models import NewsletterSubscriber

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('newsletterEmail')
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})