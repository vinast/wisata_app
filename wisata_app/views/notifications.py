from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt  # Kalau pakai JS CSRF token, bisa hilangkan ini
def mark_as_read(request, notification_id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.mark_as_read()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notifikasi tidak ditemukan'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)
