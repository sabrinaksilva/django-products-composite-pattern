from django.http import HttpResponse
from django.shortcuts import render, redirect

from products.forms import ProductForm
from products.services.product_service import ProductService


def dashboard(request):
    return render(request, 'products/dashboard.html')


def products(request):
    all_products = ProductService.get_products()
    context = {'products': all_products}
    return render(request, 'products/products.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            print(f"Created Product: {product}")

            return redirect('products')
        else:
            print("Invalid form:")
            print(form.errors)

    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'products/product-form.html', context)


def foo(request):
    products = ProductService.get_products()
    return HttpResponse(products)
