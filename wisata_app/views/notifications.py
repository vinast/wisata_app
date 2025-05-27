from django.shortcuts import redirect, get_object_or_404
from django.views import View
from wisata_app.models import Wisata, Penginapan
from notifications.models import Notification
from django.urls import reverse

class MarkNotificationAsReadView(View):
    def get(self, request, notification_id):
        if request.user.is_authenticated:
            notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
            notification.mark_as_read()

            target_url = getattr(notification, 'target_url', None)

            if not target_url and notification.target:
                if isinstance(notification.target, Wisata):
                    target_url = reverse('wisata:detail_wisata', args=[notification.target.slug])
                    default_redirect = 'wisata:index_wisata'
                elif isinstance(notification.target, Penginapan):
                    target_url = reverse('wisata:detail_penginapan', args=[notification.target.slug])
                    default_redirect = 'wisata:index_penginapan'
                else:
                    default_redirect = 'wisata:index_home'
            else:
                default_redirect = 'wisata:index_home'

            return redirect(target_url or default_redirect)
        return redirect('wisata:index_home')
