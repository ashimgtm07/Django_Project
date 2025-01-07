from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.map, name='home'),
    path('about/', views.about, name='about'),
    path('documents/', views.doc, name='documents'),
    path('fetch-hospitals/', views.fetch_hospitals, name='fetch_hospitals'),
    path('submit_location/', views.submit_location, name='submit_location'),
    path('guidelines/', views.guidelines, name='guidelines'),
]