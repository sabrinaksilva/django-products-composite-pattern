from django.http import HttpResponse
from django.shortcuts import render

from products.services.product_service import get_product_by_id


def dashboard(request):
    return render(request, 'products/dashboard.html')


def products(request):
    return render(request, 'products/products.html')


def foo(request):
    p = get_product_by_id('28b38e4a-7039-475e-a163-4af1a324d0a8')
    return HttpResponse(p)
