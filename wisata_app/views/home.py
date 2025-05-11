from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from wisata_app.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator
from wisata_app.decorators import custom_login_required





@method_decorator(custom_login_required, name='dispatch')
class HomeViews(View):
    def get(self, request):     
        data = {
            
        }
        return render(request, 'backend/home/index.html', data)
    

