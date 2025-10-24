from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('library/', views.library, name='library'),
    path('success/', views.success, name='success'),
]
