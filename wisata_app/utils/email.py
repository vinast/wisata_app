from django.core.mail import send_mail
from wisata_app.models import NewsletterSubscriber

def kirim_email_event_baru(event):
    subject = f"Event Baru: {event.title}"
    message = f"Ada event baru: {event.title}\nTanggal: {event.created_at}\n\n{event.konten}"
    recipient_list = [s.email for s in NewsletterSubscriber.objects.all()]
    if recipient_list:
        send_mail(subject, message, 'noreply@domainanda.com', recipient_list) 