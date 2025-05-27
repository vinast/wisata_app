from notifications.models import Notification

def unread_notifications_processor(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')
        unread_count = unread_notifications.count()
    else:
        unread_notifications = []
        unread_count = 0

    return {
        'unread_notifications': unread_notifications[:3],
        'unread_notifications_count': unread_count,
    }
