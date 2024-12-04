from django.shortcuts import get_object_or_404

from products.models import Product


## TO-DO: deal not found
def get_product_by_id(product_id=None):
    product = get_object_or_404(Product, id=product_id)
    return product


def get_products():
    products: list[Product] = Product.objects.all()
    return products
