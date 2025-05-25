from notifications.models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            unread=True
        ).order_by('-timestamp')[:5]
        unread_notifications_count = Notification.objects.filter(
            recipient=request.user,
            unread=True
        ).count()
    else:
        unread_notifications = []
        unread_notifications_count = 0
        
    return {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
    } 