from django.urls import path, include
from .views import *

app_name = 'wisata'


urlpatterns = [
    path('', home.HomeViews.as_view(), name='index_home'),
    path('login/', auth.LoginViews.as_view(), name='login_admin'),
    path('logout/', auth.LogoutViews.as_view(), name='logout_admin'),
    
    
]