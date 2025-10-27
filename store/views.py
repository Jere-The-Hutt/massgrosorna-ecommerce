from django.shortcuts import render
from .models import Product


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def library(request):
    products = Product.objects.all()
    return render(request, 'library.html', {'products': products})


def success(request):
    return render(request, 'success.html')
