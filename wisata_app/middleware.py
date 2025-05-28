from django.contrib import messages

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            if '_session_init_time' not in request.session:
                request.session['_session_init_time'] = request.session.get_expiry_age()
            else:
                # cek waktu expired session
                remaining_time = request.session.get_expiry_age()
                if remaining_time <= 0:
                    messages.info(request, "Silakan Login Kembali Untuk Melanjutkan.")
        response = self.get_response(request)
        return response
