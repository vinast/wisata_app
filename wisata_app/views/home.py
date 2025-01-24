from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from wisata_app.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime



@method_decorator(login_required(), name='dispatch')
class HomeViews(View):
    def get(self, request):     
        data = {
            
        }
        return render(request, 'backend/home/index.html', data)
    

