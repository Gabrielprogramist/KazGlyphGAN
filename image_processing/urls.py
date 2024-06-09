# image_processing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('publications/', views.publications, name='publications'),
    path('find_images/', views.find_images, name='find_images'),
    path('reset_folders/', views.reset_folders, name='reset_folders'),
]
