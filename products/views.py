from django.http import HttpResponse
from django.shortcuts import render

from products.services.product_service import get_products


def dashboard(request):
    return render(request, 'products/dashboard.html')


def products(request):
    all_products = get_products()
    context = {'products': all_products}
    return render(request, 'products/products.html', context)


def foo(request):
    products = get_products()
    return HttpResponse(products)
