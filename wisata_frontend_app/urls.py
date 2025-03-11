from django.urls import path, include
from .views import *

app_name = 'app'



urlpatterns = [
    path('', home_frontend.HomeViews.as_view(), name='index_user'),
  
    path('tentang/', include([
        path('', tentang_frontend.TentangViews.as_view(), name='tentang_user'),
    ])), 
    
]