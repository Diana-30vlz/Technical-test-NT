# coreApp/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.home, name='home'),#raiz del servidor
    path('api/find-missing-number/', views.find_missing_number_api, name='find_missing_number_api'),
    path('admin/', admin.site.urls)

]
